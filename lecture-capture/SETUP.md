# Setup Guide

## 1. System dependencies

```bash
brew install ffmpeg tesseract
```

## 2. Python environment

```bash
cd lecture-capture
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. OBS Studio

1. Download from https://obsproject.com
2. Add a **Display Capture** source (your full screen)
3. Add an **Audio Output Capture** source (system audio)
4. Set output format: **Settings → Output → Recording Format = MP4**
5. Recommended: set a hotkey for Start/Stop Recording

## 4. Anthropic API key

```bash
export ANTHROPIC_API_KEY=sk-ant-...
# Add to ~/.zshrc to persist
```

## 5. Google Drive (for NotebookLM)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project → Enable **Google Drive API**
3. Create **OAuth 2.0 credentials** (Desktop app type)
4. Download the JSON → save as `credentials/google_oauth.json`
5. Run first-time auth:
   ```bash
   python pipeline.py --auth
   ```
   A browser window will open — sign in and grant Drive access.

6. In NotebookLM: create a new notebook → **Add Source → Google Drive** → navigate to `NotebookLM Sources / <CourseName>`

## 6. Run the pipeline

```bash
# Watch a lecture in OBS, then:
python pipeline.py ~/lectures/inbox/ml_backprop_2026-04-05.mp4

# Specify course name explicitly:
python pipeline.py ~/lectures/inbox/dl_attention_2026-04-06.mp4 --course DeepLearning
```

## Tuning slide extraction

If you get too many/few slides, adjust in `config.yaml`:

| Too many slides (duplicates) | Lower `hash_distance` (e.g. 5) or raise `scene_threshold` (e.g. 0.5) |
|---|---|
| Missing slides | Raise `hash_distance` (e.g. 12) or lower `scene_threshold` (e.g. 0.3) |
| Faces/videos included | Raise `min_ocr_words` (e.g. 30) |
| Slides filtered out | Lower `min_ocr_words` (e.g. 10) |

## Whisper model tradeoffs

| Model | Speed (1hr lecture) | Accuracy |
|---|---|---|
| `medium` | ~20 min on CPU | Good for English |
| `large-v3` | ~50 min on CPU | Best for technical/accented speech |
| `base` | ~8 min on CPU | Decent, may miss technical terms |
