"""Stage 4: Generate structured notes from transcript + slide OCR via Claude."""

from pathlib import Path

import anthropic


_NOTES_PROMPT = """\
You are a study assistant helping a Masters in Data Science student at IIIT Hyderabad \
create concise, high-quality notes from a lecture.

Below is the full lecture transcript (with timestamps) followed by OCR text extracted from the lecture slides.

---
TRANSCRIPT:
{transcript}

---
SLIDE TEXT (OCR, in order):
{slide_text}

---

Produce structured notes in Markdown with exactly these sections in order:

## Summary
3-5 sentences capturing the main topic and what was taught.

## Key Concepts
Bullet list. Each bullet: **term** — one-sentence definition.

## Formulas & Derivations
List any mathematical formulas, equations, or derivations. Use LaTeX inline math (`$...$`) \
or display math (`$$...$$`). If none, write "None."

## Important Details
Bullet list of facts, caveats, or points the lecturer emphasized or repeated. \
Include specific numbers, names, or examples mentioned.

## Questions to Review
5 self-test questions (numbered) that cover the key ideas. Include the answers in a \
collapsed section below each question using HTML details tags:
<details><summary>Answer</summary>answer here</details>

Be precise and technical. Use domain terminology. Do not pad with filler.
"""


def generate_notes(
    transcript_path: Path,
    slide_texts: list[str],
    output_dir: Path,
    model: str = "claude-sonnet-4-6",
) -> Path:
    """Generate structured notes using Claude.

    Args:
        transcript_path: Path to the timestamped transcript.txt.
        slide_texts: List of OCR text strings, one per slide.
        output_dir: Directory to write notes.md.
        model: Claude model ID.

    Returns:
        Path to notes.md.
    """
    transcript = transcript_path.read_text(encoding="utf-8")

    # Keep slide text concise — join with slide separators
    slide_text_combined = "\n\n---\n".join(
        f"[Slide {i+1}]\n{t}" for i, t in enumerate(slide_texts) if t.strip()
    )

    prompt = _NOTES_PROMPT.format(
        transcript=transcript,
        slide_text=slide_text_combined or "(no slide text extracted)",
    )

    print(f"Generating notes with {model}...")
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    notes_content = message.content[0].text
    notes_path = output_dir / "notes.txt"
    notes_path.write_text(notes_content, encoding="utf-8")
    print(f"  Notes: {notes_path}")

    return notes_path
