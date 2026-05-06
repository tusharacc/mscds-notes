#!/usr/bin/env python3
"""
Lecture Capture — Single Entry Point
=====================================
Usage:
    python capture.py --course <CourseName> [--no-slides]
    python capture.py --course PythonCore
    python capture.py --course StatsCourse --no-slides

Workflow:
    1. Starts OBS recording via WebSocket (launches OBS if not running)
    2. Opens Chrome to your LMS (persistent session — login once, auto after)
    3. You watch the lecture, then close Chrome when done
    4. OBS recording stops automatically
    5. Pipeline runs automatically on the recorded file

One-time setup required in OBS:
    Tools → WebSocket Server Settings → Enable → set password → note port (4455)
    Then set obs.websocket_password in config.yaml
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

_CHROME_PATHS_MAC = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]


def load_config(config_path: Path) -> dict:
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    for key in ("inbox", "output"):
        cfg["paths"][key] = str(Path(cfg["paths"][key]).expanduser())
    return cfg


def _find_chrome() -> str:
    for path in _CHROME_PATHS_MAC:
        if Path(path).exists():
            return path
    raise RuntimeError(
        "Google Chrome not found. Install it at https://www.google.com/chrome/ "
        "or check the path in capture.py."
    )


def _obs_is_running() -> bool:
    result = subprocess.run(["pgrep", "-x", "OBS"], capture_output=True)
    return result.returncode == 0


def _launch_obs() -> None:
    print("  Launching OBS...")
    subprocess.Popen(["open", "-a", "OBS"])


def _connect_obs(host: str, port: int, password: str, retries: int = 20):
    """Connect to OBS WebSocket, retrying until OBS is ready."""
    import obsws_python as obs

    for attempt in range(retries):
        try:
            client = obs.ReqClient(host=host, port=port, password=password, timeout=3)
            return client
        except Exception:
            if attempt < retries - 1:
                time.sleep(1)
    raise RuntimeError(
        f"Could not connect to OBS WebSocket at {host}:{port}.\n"
        "Make sure:\n"
        "  1. OBS is running\n"
        "  2. Tools → WebSocket Server Settings → Enable WebSocket server is checked\n"
        "  3. The password in config.yaml matches the one set in OBS\n"
        "  4. The port is 4455 (or update obs.websocket_port in config.yaml)"
    )


def _start_recording(client) -> None:
    status = client.get_record_status()
    if status.output_active:
        print("  OBS is already recording — continuing with existing session.")
        return
    client.start_record()
    print("  OBS recording started.")


def _stop_recording(client) -> str | None:
    """Stop OBS recording and return the output file path."""
    try:
        response = client.stop_record()
        output_path = getattr(response, "output_path", None)
        return output_path
    except Exception as e:
        print(f"  Warning: could not stop OBS cleanly: {e}")
        return None


def _launch_chrome(lms_url: str, profile_dir: Path, no_sandbox: bool) -> subprocess.Popen:
    chrome_bin = _find_chrome()
    profile_dir.mkdir(parents=True, exist_ok=True)

    args = [
        chrome_bin,
        f"--user-data-dir={profile_dir}",
        "--new-window",
    ]
    if no_sandbox:
        args.append("--no-sandbox")
    if lms_url:
        args.append(lms_url)

    print(f"  Opening Chrome → {lms_url or '(no LMS URL set)'}")
    if not lms_url:
        print("  Tip: set lms.url in config.yaml to auto-open your LMS next time.")

    return subprocess.Popen(args)


def _wait_for_chrome(proc: subprocess.Popen) -> None:
    print("  Waiting for you to finish watching and close Chrome...")
    proc.wait()
    print("  Chrome closed.")


def _find_latest_recording(cfg: dict) -> Path | None:
    """Find the most recently modified video file in OBS default output dirs."""
    search_dirs = [
        Path.home() / "Movies",
        Path(cfg["paths"]["inbox"]),
    ]
    candidates = []
    for d in search_dirs:
        if d.exists():
            for ext in ("*.mp4", "*.mov", "*.mkv"):
                candidates.extend(d.glob(ext))

    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def main():
    parser = argparse.ArgumentParser(description="Lecture Capture — Single Entry Point")
    parser.add_argument("--course", required=True, help="Course name (e.g. PythonCore)")
    parser.add_argument("--no-slides", action="store_true",
                        help="Skip slide extraction (for handwritten/whiteboard lectures)")
    args = parser.parse_args()

    config_path = Path(__file__).parent / "config.yaml"
    cfg = load_config(config_path)

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set. Add it to the .env file.")
        sys.exit(1)

    obs_cfg = cfg.get("obs", {})
    lms_cfg = cfg.get("lms", {})
    chrome_cfg = cfg.get("chrome", {})

    host = obs_cfg.get("websocket_host", "localhost")
    port = obs_cfg.get("websocket_port", 4455)
    password = obs_cfg.get("websocket_password", "")
    lms_url = lms_cfg.get("url", "")
    profile_dir = Path(chrome_cfg.get("profile_dir", "~/.lecture-capture-chrome")).expanduser()
    no_sandbox = chrome_cfg.get("no_sandbox", True)
    startup_wait = obs_cfg.get("startup_wait_seconds", 10)

    print(f"\n{'='*60}")
    print(f"  Course:  {args.course}")
    print(f"  Mode:    {'transcript only' if args.no_slides else 'slides + transcript'}")
    print(f"{'='*60}\n")

    # --- Step 1: Ensure OBS is running ---
    print("[1/4] Connecting to OBS...")
    if not _obs_is_running():
        if obs_cfg.get("launch_if_not_running", True):
            _launch_obs()
            print(f"  Waiting {startup_wait}s for OBS to start...")
            time.sleep(startup_wait)
        else:
            print("ERROR: OBS is not running. Start OBS and try again.")
            sys.exit(1)

    obs_client = _connect_obs(host, port, password)
    print("  Connected to OBS.")

    # --- Step 2: Start recording ---
    print("\n[2/4] Starting OBS recording...")
    _start_recording(obs_client)

    # --- Step 3: Open Chrome → LMS ---
    print("\n[3/4] Opening Chrome...")
    chrome_proc = _launch_chrome(lms_url, profile_dir, no_sandbox)
    _wait_for_chrome(chrome_proc)

    # --- Step 4: Stop recording + run pipeline ---
    print("\n[4/4] Stopping OBS recording...")
    recorded_file = _stop_recording(obs_client)

    if not recorded_file:
        print("  OBS did not return a file path — scanning for latest recording...")
        latest = _find_latest_recording(cfg)
        if latest:
            recorded_file = str(latest)
            print(f"  Found: {recorded_file}")
        else:
            print("ERROR: Could not find the recorded file. Check OBS output directory.")
            sys.exit(1)

    recorded_path = Path(recorded_file)
    size_mb = recorded_path.stat().st_size / (1024 * 1024) if recorded_path.exists() else 0
    if size_mb < 1:
        print(f"WARNING: Recording is very small ({size_mb:.1f} MB). It may be empty.")
        print("  Skipping pipeline. Check OBS settings and try again.")
        sys.exit(1)

    print(f"  Recording: {recorded_path.name} ({size_mb:.1f} MB)")
    print("\nStarting pipeline...\n")

    # Build pipeline command, passing through flags
    pipeline_cmd = [
        sys.executable,
        str(Path(__file__).parent / "pipeline.py"),
        str(recorded_path),
        "--course", args.course,
    ]
    if args.no_slides:
        pipeline_cmd.append("--no-slides")

    result = subprocess.run(pipeline_cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
