# Workspace: practice-problem-booklet

**Type**: feature
**Created**: 2026-05-17
**Phase**: po
**Status**: active

## Feature Summary
Extract practice problems from two probability PDFs (MIT Notes and Probability Chapter Notes),
generate hints + step-by-step solutions, verify via web search, and output as GitHub Pages HTML
with print-ready PDF booklet styling.

## Source PDFs
- `ProbabilityChapter/mit_notes_probability.pdf` — 196 pages, text-based (LaTeX)
- `ProbabilityChapter/probability_chapter_notes.pdf` — 39 pages, text-based

## Design Constraints
- Output uses existing MscDS design system (CSS variables, block-badges, MathJax 3)
- Verification: Claude base knowledge + web search (Math StackExchange, MIT OCW)
- Confidence tiers: ✓ High / ⚠ Partial / ○ Unverified
- Print CSS for PDF booklet output
