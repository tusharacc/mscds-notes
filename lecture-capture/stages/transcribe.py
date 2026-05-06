"""Stage 3: Transcribe audio using local OpenAI Whisper."""

import json
from pathlib import Path

import whisper
from tqdm import tqdm


def _format_timestamp(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"[{h:02d}:{m:02d}:{s:02d}]"


def transcribe(
    wav_path: Path,
    output_dir: Path,
    model_name: str = "medium",
    language: str | None = "en",
) -> tuple[Path, list[dict]]:
    """Transcribe audio and write transcript.txt + segments.json.

    Args:
        wav_path: Input WAV file (16kHz mono).
        output_dir: Directory to write output files.
        model_name: Whisper model size.
        language: ISO language code, or None for auto-detect.

    Returns:
        Tuple of (path to transcript.txt, list of segment dicts with start/end/text).
    """
    print(f"Loading Whisper model '{model_name}'...")
    model = whisper.load_model(model_name)

    print("Transcribing... (this may take a while for long lectures)")
    options = {"language": language} if language else {}
    result = model.transcribe(str(wav_path), verbose=False, **options)

    segments: list[dict] = result["segments"]

    # Write timestamped transcript
    transcript_path = output_dir / "transcript.txt"
    with open(transcript_path, "w", encoding="utf-8") as f:
        for seg in segments:
            ts = _format_timestamp(seg["start"])
            f.write(f"{ts} {seg['text'].strip()}\n")

    # Write raw segments JSON (used for slide-transcript alignment later)
    segments_path = output_dir / "segments.json"
    with open(segments_path, "w", encoding="utf-8") as f:
        json.dump(segments, f, indent=2, ensure_ascii=False)

    print(f"  Transcript: {transcript_path}")
    word_count = sum(len(s["text"].split()) for s in segments)
    print(f"  {len(segments)} segments, ~{word_count} words")

    return transcript_path, segments
