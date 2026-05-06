"""Stage 1: Extract 16kHz mono WAV from an MP4 for Whisper."""

import subprocess
from pathlib import Path


def extract_audio(video_path: Path, output_dir: Path) -> Path:
    """Extract audio from video as 16kHz mono WAV.

    Args:
        video_path: Input MP4 file.
        output_dir: Directory to write the WAV file.

    Returns:
        Path to the extracted WAV file.
    """
    wav_path = output_dir / (video_path.stem + ".wav")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-ar", "16000",       # 16 kHz sample rate (Whisper requirement)
        "-ac", "1",            # mono
        "-c:a", "pcm_s16le",   # uncompressed PCM
        str(wav_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg audio extraction failed:\n{result.stderr}")
    return wav_path
