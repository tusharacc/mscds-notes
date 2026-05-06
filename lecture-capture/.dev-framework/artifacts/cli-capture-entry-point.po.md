# PO Requirements: CLI Capture Entry Point

## Problem Statement

The current lecture capture workflow requires too many manual steps across multiple apps:
1. Open OBS → validate config → start recording
2. Open browser → navigate to LMS → log in → find video → press play
3. Watch lecture
4. Stop OBS recording
5. Stop browser
6. Run `python pipeline.py <file> --course X`

The user needs a **single CLI command** that reduces this to: run command → watch lecture → close browser → done.

---

## User Stories

- **As a student**, I want to run one command that starts recording and opens the LMS, so I don't have to manage multiple apps manually.
- **As a student**, I want my LMS login session to persist between runs, so I only log in once.
- **As a student**, I want the pipeline to start automatically when I close the browser, so I don't have to trigger post-processing manually.
- **As a student**, I want to specify the course name once per command, not once per pipeline step.

---

## Functional Requirements

### FR1 — Single entry point
- New script: `capture.py`
- Usage: `python capture.py --course <CourseName> [--no-slides]`
- Accepts all existing pipeline flags (`--course`, `--no-slides`)

### FR2 — OBS control via WebSocket
- Connect to OBS via WebSocket (OBS 28+ built-in, default port 4455)
- Verify OBS is running; if not, launch it and wait for it to be ready
- Start recording programmatically
- Stop recording programmatically when triggered
- Discover the output file path from OBS after recording stops

### FR3 — Chrome launch with persistent session
- Launch Chrome with `--no-sandbox` flag
- Use a fixed `--user-data-dir` (e.g. `~/.lecture-capture-chrome/`) so session cookies persist
- Open to the configured LMS URL on launch
- First run: user logs in manually (session saved automatically)
- Subsequent runs: session already active, user lands on LMS directly

### FR4 — Pipeline trigger on browser close
- Monitor the Chrome process
- When Chrome exits (user closes the window), automatically stop OBS recording
- Automatically invoke the existing pipeline on the recorded file
- Pass `--course` and `--no-slides` flags through

### FR5 — Configuration
- Add to `config.yaml`:
  - `obs.websocket_host` (default: `localhost`)
  - `obs.websocket_port` (default: `4455`)
  - `obs.websocket_password`
  - `lms.url` — the LMS base URL
  - `chrome.profile_dir` (default: `~/.lecture-capture-chrome`)
  - `chrome.no_sandbox` (default: `true`)

---

## Non-Functional Requirements

- **NFR1**: OBS must already be installed; `capture.py` does not install it
- **NFR2**: Chrome must already be installed
- **NFR3**: OBS WebSocket must be enabled by the user once in OBS settings
- **NFR4**: `capture.py` must work on macOS (primary target: M3 MacBook)
- **NFR5**: Should not require root/sudo

---

## Acceptance Criteria

- [ ] `python capture.py --course PythonCore` starts OBS recording and opens Chrome to LMS URL
- [ ] Chrome opens with a persistent profile — login on first run, auto-session on subsequent runs
- [ ] Closing Chrome automatically stops OBS and triggers the pipeline
- [ ] Pipeline output (`transcript.txt`, `notes.txt`, optionally `slides.pdf`) is uploaded to Drive
- [ ] `--no-slides` flag is passed through to the pipeline correctly
- [ ] Config values for OBS WebSocket and LMS URL are read from `config.yaml`
- [ ] Helpful error if OBS WebSocket is not reachable (with setup instructions)
- [ ] Helpful error if `ANTHROPIC_API_KEY` is not set

---

## Edge Cases

- OBS is not running when `capture.py` is called → launch OBS, wait for WebSocket to become available
- OBS WebSocket password is wrong → clear error message
- Chrome crashes instead of being cleanly closed → still trigger pipeline on the recorded file
- Recording file is empty (< 1MB) → warn user and skip pipeline
- LMS URL not set in config → error with instruction to set it

---

## Dependencies

- `obsws-python` — OBS WebSocket client library (new dependency)
- Existing: `pipeline.py` and all stages remain unchanged
- OBS 28+ (WebSocket built-in)
- Google Chrome installed at standard macOS path

---

## Out of Scope (Next Iteration)

- Playwright automation to navigate LMS and start video playback
- Auto-detection of lecture end (stop recording when video finishes)
