#!/usr/bin/env python3
"""
Lecture Capture Pipeline
========================
Usage:
    python pipeline.py <video.mp4> [--course COURSE_NAME]
    python pipeline.py --auth       # First-time Google Drive OAuth setup

The video filename should follow the convention:
    <course>_<topic>_<YYYY-MM-DD>.mp4
    e.g.  ml_backprop_2026-04-05.mp4

If --course is not provided, it is inferred from the filename prefix.
"""

import argparse
import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

# Load .env from the project directory
load_dotenv(Path(__file__).parent / ".env")


def load_config(config_path: Path) -> dict:
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    # Expand ~ in paths
    for key in ("inbox", "output"):
        cfg["paths"][key] = str(Path(cfg["paths"][key]).expanduser())
    return cfg


def run_auth(cfg: dict) -> None:
    """Trigger Google OAuth flow to cache credentials."""
    from stages.upload_drive import _authenticate
    creds_file = Path(__file__).parent / cfg["google_drive"]["credentials_file"]
    token_file = Path(__file__).parent / cfg["google_drive"]["token_file"]
    if not creds_file.exists():
        print(f"ERROR: credentials file not found at {creds_file}")
        print("Download OAuth 2.0 client secrets from Google Cloud Console and place it there.")
        sys.exit(1)
    _authenticate(creds_file, token_file)
    print("Authentication successful. Token cached.")


def run_pipeline(video_path: Path, course_name: str, cfg: dict, no_slides: bool = False) -> None:
    from stages.extract_audio import extract_audio
    from stages.extract_slides import extract_slides
    from stages.transcribe import transcribe
    from stages.generate_notes import generate_notes
    from stages.upload_drive import upload_to_drive

    lecture_slug = video_path.stem  # e.g. ml_backprop_2026-04-05
    output_dir = Path(cfg["paths"]["output"]) / lecture_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    total_stages = 4 if no_slides else 5

    print(f"\n{'='*60}")
    print(f"  Lecture: {video_path.name}")
    print(f"  Course:  {course_name}")
    print(f"  Mode:    {'transcript only (no slides)' if no_slides else 'full (slides + transcript)'}")
    print(f"  Output:  {output_dir}")
    print(f"{'='*60}\n")

    # --- Stage 1: Audio extraction ---
    print(f"[1/{total_stages}] Extracting audio...")
    wav_path = extract_audio(video_path, output_dir)
    print()

    # --- Stage 2: Slide extraction (skipped for handwritten lectures) ---
    slides_pdf = None
    slide_texts = []
    if no_slides:
        print(f"[2/{total_stages}] Slides: SKIPPED (transcript-only mode)")
        print()
    else:
        print(f"[2/{total_stages}] Extracting slides...")
        slide_cfg = cfg["slide_extraction"]
        slides_pdf, slide_texts = extract_slides(
            video_path,
            output_dir,
            scene_threshold=slide_cfg["scene_threshold"],
            hash_distance=slide_cfg["hash_distance"],
            min_ocr_words=slide_cfg["min_ocr_words"],
        )
        print()

    # --- Stage 3: Transcription ---
    stage = 3 if not no_slides else 2
    print(f"[{stage}/{total_stages}] Transcribing audio...")
    tx_cfg = cfg["transcription"]
    transcript_path, _ = transcribe(
        wav_path,
        output_dir,
        model_name=tx_cfg["whisper_model"],
        language=tx_cfg.get("language"),
    )
    print()

    # --- Stage 4: Notes generation ---
    stage = 4 if not no_slides else 3
    print(f"[{stage}/{total_stages}] Generating notes with Claude...")
    notes_path = generate_notes(
        transcript_path,
        slide_texts,
        output_dir,
        model=cfg["notes"]["claude_model"],
    )
    print()

    # --- Stage 5: Google Drive upload ---
    stage = 5 if not no_slides else 4
    print(f"[{stage}/{total_stages}] Uploading to Google Drive...")
    drive_cfg = cfg["google_drive"]
    creds_file = Path(__file__).parent / drive_cfg["credentials_file"]
    token_file = Path(__file__).parent / drive_cfg["token_file"]

    if not creds_file.exists():
        print("  SKIP: Google Drive credentials not configured.")
        print(f"  Run `python pipeline.py --auth` after placing OAuth credentials at {creds_file}")
    else:
        files_to_upload = [f for f in [slides_pdf, transcript_path, notes_path] if f]
        folder_url = upload_to_drive(
            files=files_to_upload,
            course_name=course_name,
            lecture_slug=lecture_slug,
            credentials_file=creds_file,
            token_file=token_file,
            root_folder_name=drive_cfg["root_folder_name"],
        )
        print()
        print(f"NotebookLM Drive folder: {folder_url}")

    print(f"\nDone. Output files in: {output_dir}")
    if slides_pdf:
        print(f"  slides.pdf      — {slides_pdf.stat().st_size // 1024} KB")
    print(f"  transcript.txt  — {transcript_path.stat().st_size // 1024} KB")
    print(f"  notes.md        — {notes_path.stat().st_size // 1024} KB")


def main():
    parser = argparse.ArgumentParser(description="Lecture Capture Pipeline")
    parser.add_argument("video", nargs="?", help="Path to lecture video file (MP4 or MOV)")
    parser.add_argument("--course", help="Course name (inferred from filename if omitted)")
    parser.add_argument("--auth", action="store_true", help="Run Google Drive OAuth setup")
    parser.add_argument("--no-slides", action="store_true",
                        help="Skip slide extraction (use for handwritten/whiteboard lectures)")
    args = parser.parse_args()

    config_path = Path(__file__).parent / "config.yaml"
    cfg = load_config(config_path)

    if args.auth:
        run_auth(cfg)
        return

    if not args.video:
        parser.print_help()
        sys.exit(1)

    video_path = Path(args.video).expanduser().resolve()
    if not video_path.exists():
        print(f"ERROR: File not found: {video_path}")
        sys.exit(1)
    if video_path.suffix.lower() not in (".mp4", ".mov", ".mkv", ".avi"):
        print(f"ERROR: Unsupported video format: {video_path.suffix}. Use MP4, MOV, MKV, or AVI.")
        sys.exit(1)

    # Infer course name from filename prefix (e.g. "ml" from "ml_backprop_2026-04-05.mp4")
    course_name = args.course or video_path.stem.split("_")[0].upper()

    # Ensure ANTHROPIC_API_KEY is set
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
        print("Export it before running: export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    run_pipeline(video_path, course_name, cfg, no_slides=args.no_slides)


if __name__ == "__main__":
    main()
