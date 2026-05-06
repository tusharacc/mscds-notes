"""Stage 2: Extract unique slide frames from a lecture video and compile to PDF."""

import subprocess
import json
from pathlib import Path

import imagehash
import img2pdf
import pytesseract
from PIL import Image
from tqdm import tqdm


def _get_video_duration(video_path: Path) -> float:
    """Return video duration in seconds via ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        str(video_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed:\n{result.stderr}")
    info = json.loads(result.stdout)
    return float(info["format"]["duration"])


def _extract_scene_frames(video_path: Path, frames_dir: Path, threshold: float) -> list[Path]:
    """Use ffmpeg scene detection to extract candidate keyframes."""
    frames_dir.mkdir(parents=True, exist_ok=True)

    # Use ffmpeg scene filter to detect cuts, save frames as timestamped PNGs
    output_pattern = str(frames_dir / "frame_%08d.png")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", f"select='gt(scene,{threshold})',showinfo",
        "-vsync", "vfr",
        output_pattern,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg scene extraction failed:\n{result.stderr}")

    frames = sorted(frames_dir.glob("frame_*.png"))
    return frames


def _dedup_frames(frames: list[Path], hash_distance: int) -> list[Path]:
    """Remove near-duplicate frames using perceptual hashing."""
    unique: list[tuple[imagehash.ImageHash, Path]] = []
    for frame_path in tqdm(frames, desc="Deduplicating frames"):
        img = Image.open(frame_path)
        h = imagehash.phash(img)
        is_dup = any(abs(h - prev_h) <= hash_distance for prev_h, _ in unique)
        if not is_dup:
            unique.append((h, frame_path))
    return [p for _, p in unique]


def _is_slide_frame(frame_path: Path, min_words: int) -> bool:
    """Return True if the frame contains enough text to be a slide."""
    img = Image.open(frame_path)
    text = pytesseract.image_to_string(img)
    word_count = len(text.split())
    return word_count >= min_words


def extract_slides(
    video_path: Path,
    output_dir: Path,
    scene_threshold: float = 0.4,
    hash_distance: int = 8,
    min_ocr_words: int = 20,
) -> tuple[Path, list[str]]:
    """Extract unique slide frames and compile into a PDF.

    Args:
        video_path: Input MP4 file.
        output_dir: Directory to write frames and final PDF.
        scene_threshold: ffmpeg scene change sensitivity (0-1).
        hash_distance: Perceptual hash Hamming distance for dedup.
        min_ocr_words: Minimum word count to keep a frame as a slide.

    Returns:
        Tuple of (path to slides.pdf, list of OCR text per slide).
    """
    frames_dir = output_dir / "frames"

    print("Extracting scene change frames...")
    raw_frames = _extract_scene_frames(video_path, frames_dir, scene_threshold)
    print(f"  Found {len(raw_frames)} candidate frames")

    print("Deduplicating frames...")
    unique_frames = _dedup_frames(raw_frames, hash_distance)
    print(f"  {len(unique_frames)} unique frames after dedup")

    print("Filtering for slide frames (OCR check)...")
    slide_frames = [f for f in tqdm(unique_frames, desc="OCR filter")
                    if _is_slide_frame(f, min_ocr_words)]
    print(f"  {len(slide_frames)} slide frames retained")

    if not slide_frames:
        raise RuntimeError(
            "No slide frames detected. Try lowering scene_threshold or min_ocr_words in config.yaml."
        )

    # OCR text per slide for notes generation
    slide_texts = []
    for f in slide_frames:
        text = pytesseract.image_to_string(Image.open(f))
        slide_texts.append(text.strip())

    # Compile to PDF
    pdf_path = output_dir / "slides.pdf"
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert([str(p) for p in slide_frames]))
    print(f"  Slides PDF: {pdf_path} ({len(slide_frames)} pages)")

    return pdf_path, slide_texts
