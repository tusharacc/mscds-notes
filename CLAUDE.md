# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a learning resource repository for the MScDS programme at IIIT Hyderabad. It contains:
- Course notes generated from lecture transcripts (HTML format)
- Interactive quizzes and practice problem booklets
- Automated lecture capture and processing pipeline
- Published via GitHub Pages at https://tusharacc.github.io/mscds-notes/

## Repository Structure

```
discrete_mathematics/    # Notes + transcripts (Weeks 1-7: Probability, Linear Algebra)
python/                  # Notes + transcripts (Weeks 1-10: Foundations to Applied Project)
computer_systems/        # Notes + transcripts (Weeks 1-10: MIPS, Pipelining, Networking)
DSA/                     # Data Structures & Algorithms course materials
practice/                # Solved problem booklets (Probability, Linear Algebra)
quiz/                    # Interactive quiz modules
lecture-capture/         # Automated lecture processing pipeline
```

## Course Content Conventions

Each course directory follows this pattern:
- `index.html` — Main notes page (self-contained, MathJax 3 for equations)
- `WeekN/` or `weekN/` — Transcript files (`.txt`) and source materials
- `quiz/index.html` — Interactive MCQ quiz for that course

## Common Commands

### Lecture Capture Pipeline

The pipeline converts lecture videos into notes, transcripts, and slides for NotebookLM.

**Environment setup:**
```bash
# Create virtual environment (first time)
python -m venv .venv
source .venv/bin/activate

# Install dependencies
cd lecture-capture
pip install -r requirements.txt
```

**First-time Google Drive setup:**
```bash
cd lecture-capture
python pipeline.py --auth
```

**Process a recorded lecture:**
```bash
# Full mode (slides + transcript)
python lecture-capture/pipeline.py path/to/video.mp4 --course CourseName

# Transcript-only mode (for handwritten/whiteboard lectures)
python lecture-capture/pipeline.py path/to/video.mp4 --course CourseName --no-slides
```

**Automated capture workflow:**
```bash
# Starts OBS, opens Chrome to LMS, records, then processes
python lecture-capture/capture.py --course PythonCore
python lecture-capture/capture.py --course StatsCourse --no-slides
```

### Transcription Scripts

Each course directory has utility scripts for batch processing:

**Download videos from LMS:**
```bash
cd discrete_mathematics  # or python/, computer_systems/, DSA/
./download.sh
```

**Transcribe videos with Whisper:**
```bash
cd discrete_mathematics
./transcribe.sh  # Processes videos in specified week folders
```

### HTML Generation

**Regenerate course index page:**
```bash
cd computer_systems
python generate_html.py  # Converts Week*/README.md to index.html
```

Note: `discrete_mathematics/index.html` and `python/index.html` are manually maintained.

## Lecture Capture Architecture

### Pipeline Stages (pipeline.py)

Five-stage processing pipeline for lecture videos:

1. **Audio extraction** — Extract WAV from video (FFmpeg via moviepy)
2. **Slide extraction** — Detect scene changes, deduplicate frames via perceptual hashing, OCR with Tesseract, generate PDF
3. **Transcription** — OpenAI Whisper (configurable model: tiny → large-v3)
4. **Notes generation** — Claude API generates structured notes from transcript + slide text
5. **Drive upload** — Upload to Google Drive folder for NotebookLM ingestion

**Configuration:** `lecture-capture/config.yaml`
- Paths, Whisper model, scene detection thresholds
- OBS WebSocket settings
- Google Drive OAuth credentials

**Individual stages:** See `lecture-capture/stages/{extract_audio,extract_slides,transcribe,generate_notes,upload_drive}.py`

### Capture Workflow (capture.py)

Automated end-to-end lecture recording:

1. Launch OBS (if not running) and connect via WebSocket
2. Start OBS recording
3. Open Chrome with persistent session to LMS URL
4. Wait for user to close Chrome
5. Stop recording, find output file
6. Run pipeline.py on recorded video

**Dependencies:**
- OBS with WebSocket server enabled (Tools → WebSocket Server Settings)
- `obsws-python` for OBS control
- Chrome/Chromium installed

## Environment Variables

Create `lecture-capture/.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-...
```

Required for notes generation stage (Claude API).

## Video Naming Convention

For manual pipeline runs, follow this format:
```
<course>_<topic>_<YYYY-MM-DD>.mp4
```
Example: `ml_backprop_2026-04-05.mp4`

Course name is auto-extracted from filename prefix if `--course` is omitted.

## Adding New Course Content

1. Create `course_name/weekN/` directory
2. Add transcript `.txt` files to the week folder
3. Update `course_name/index.html` following the existing structure
4. Commit and push — GitHub Pages auto-deploys

## Technology Stack

- **Backend:** Python 3.x
- **Transcription:** OpenAI Whisper (torch backend)
- **OCR:** Tesseract via pytesseract
- **Image processing:** Pillow, imagehash
- **AI:** Anthropic Claude API
- **Automation:** obsws-python for OBS control
- **Frontend:** Self-contained HTML with MathJax 3, no build step
- **Deployment:** GitHub Pages (automatic from main branch)

## Design Philosophy

- **Self-contained pages:** All HTML files standalone (no server, no bundler)
- **MathJax for math:** Renders LaTeX notation in browser
- **No build step:** Direct edit-commit-deploy workflow
- **Separation of concerns:** Videos stored locally, only transcripts/notes committed
- **Pipeline modularity:** Each stage can be run independently for debugging
