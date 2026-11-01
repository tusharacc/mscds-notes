# Lecture Capture - Two-Step Workflow

Complete automation from LMS video extraction to processed lecture notes.

**Why two steps?** Video URLs are only visible in network traffic when you click to play them, not in the HTML. This requires interactive browser automation.

## Quick Start

### 1. Install Dependencies

```bash
cd lecture-capture
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure LMS URL

Edit `config.yaml`:
```yaml
lms:
  url: "https://your-lms-url.edu"
```

### 3. Set API Key

Create `.env` file:
```bash
ANTHROPIC_API_KEY=sk-ant-...
```

### 4. Two-Step Workflow

**Step 1: Extract video URLs** (interactive)
```bash
python extract_urls.py --course MDS201 --weeks 11 12
```

This:
- Opens browser to LMS
- You log in (session is saved)
- You navigate and click on videos
- Script captures URLs from network traffic
- Press Ctrl+C when done
- Saves to `videos.json`

**Step 2: Download and process** (automated)
```bash
python download_and_process.py videos.json
```

This:
- Downloads all videos with progress bars
- Runs full pipeline on each video
- Generates transcripts, slides, notes

## Detailed Workflow

### Step 1: Interactive URL Extraction

```bash
# Extract URLs for specific weeks
python extract_urls.py --course MDS201 --weeks 11 12

# Week range
python extract_urls.py --course MDS201 --weeks 11-15

# Custom output file
python extract_urls.py --course MDS201 --weeks 11 --output week11.json
```

**What happens:**
1. Browser opens to your LMS
2. Log in manually (first time only - session persists)
3. Navigate to your course
4. Click each video to start playback (even briefly)
5. Script monitors network traffic and captures video URLs
6. Press Ctrl+C when you've clicked all videos
7. URLs saved to `videos.json`

**Network Monitor Features:**
- Detects video files (`.mp4`, `.mov`, `.webm`, `.m3u8`)
- Captures streaming URLs (HLS/DASH)
- Extracts metadata (week number, title, filename)
- Shows real-time capture count

### Step 2: Download and Process

```bash
# Full processing (download + pipeline)
python download_and_process.py videos.json

# Download only (no pipeline)
python download_and_process.py videos.json --download-only

# Handwritten lectures (no slides)
python download_and_process.py videos.json --no-slides

# Process specific weeks only
python download_and_process.py videos.json --weeks 11 12
```

**What happens:**
1. Loads URLs from JSON file
2. Uses saved browser session for authentication
3. Downloads each video with progress tracking
4. Runs full pipeline on each video:
   - Audio extraction
   - Slide extraction (if enabled)
   - Transcription (Whisper)
   - Notes generation (Claude)
   - Upload to Google Drive
5. Shows summary of successes/failures

## JSON Format

After Step 1, `videos.json` will look like this:

```json
{
  "course": "MDS201",
  "weeks": [11, 12],
  "total_videos": 4,
  "videos": [
    {
      "url": "https://lms.example.edu/video.mp4",
      "filename": "lecture_11_part1.mp4",
      "week": 11,
      "title": "Lecture 11 Part 1",
      "content_type": "video/mp4"
    }
  ]
}
```

You can manually edit this file to:
- Add or correct week numbers
- Fix filenames
- Remove unwanted videos
- Add custom metadata

See `videos.example.json` for a complete example.

## Architecture

```
Step 1: extract_urls.py
├── Playwright browser automation
├── Network traffic monitoring
├── Video URL detection
└── JSON output

Step 2: download_and_process.py
├── Load URLs from JSON
├── Get authentication cookies from browser
├── Download videos (httpx)
└── Run pipeline.py on each video
```

## File Structure

```
lecture-capture/
├── agent.py              # Unified automation script
├── pipeline.py           # Processing pipeline
├── capture.py            # OBS recording automation
├── config.yaml           # Configuration
├── .env                  # API keys
├── credentials/
│   └── session.json      # Browser session (auto-created)
└── stages/
    ├── extract_audio.py
    ├── extract_slides.py
    ├── transcribe.py
    ├── generate_notes.py
    └── upload_drive.py
```

## Troubleshooting

### Step 1: URL Extraction Issues

**"No videos captured"**
- Make sure you're actually clicking on videos to start playback
- Check the network monitor output - it should show captured URLs in real-time
- Try clicking on a video and watching for network activity
- Some LMS may use JavaScript players - click multiple times if needed

**"Network monitor not detecting videos"**
- Check if your LMS uses a different video format (e.g., embedded YouTube)
- Look at browser DevTools → Network tab to see what requests are made
- Update `VIDEO_EXTENSIONS` in `extract_urls.py` if needed
- Try opening DevTools and filtering by "media" to see video URLs manually

**"Browser session not persisting"**
- Check that `credentials/browser-session/` directory exists
- Try deleting the directory and logging in again
- Some LMS may have session timeouts - you may need to re-login

### Step 2: Download & Process Issues

**"Download failed"**
- Verify session cookies are still valid (may expire after some time)
- Re-run Step 1 to refresh authentication
- Check if video URLs have expiration tokens
- Try downloading immediately after URL extraction

**"Authentication error"**
- Browser session may have expired
- Delete `credentials/browser-session/` and run Step 1 again
- Check if LMS requires additional headers (User-Agent, Referer)

**"Pipeline failed"**
- Ensure ANTHROPIC_API_KEY is set in `.env`
- Check video file is valid (not corrupted) - play it manually
- Verify sufficient disk space for processing
- Check `~/lectures/output/` for partial outputs

**"Week numbers not detected"**
- URLs may not contain week info
- Manually edit `videos.json` to add week numbers
- Or organize files manually after download

## Tips for Best Results

1. **Keep browser open** during Step 1 until you've clicked all videos
2. **Run Step 2 immediately** after Step 1 while session is fresh
3. **Save videos.json** - you can re-run Step 2 without re-extracting URLs
4. **Test with one week** first before processing entire course
5. **Check videos.json** after Step 1 to verify URLs were captured correctly

## Legacy Scripts

These manual scripts are now replaced by the two-step workflow:

- `download.sh` - Manual URL download with hardcoded session IDs
- `transcribe.sh` - Batch Whisper transcription
- `agent.py.old` - Previous approach (archived)

Use the new two-step workflow for automated URL extraction and processing.
