# PO Requirements: Practice Problem Booklet

**Workspace**: practice-problem-booklet
**Phase**: PO (complete)
**Date**: 2026-05-17

---

## Problem Statement

The user has two probability textbook PDFs without worked solutions. Extract substantive exercises,
generate hints + full step-by-step solutions (verified against web sources), and produce a single
GitHub Pages HTML file plus a printable PDF booklet — hosted in the existing MscDS repo.

## Source Material
- `ProbabilityChapter/mit_notes_probability.pdf` — 196 pages, text-based LaTeX
- `ProbabilityChapter/probability_chapter_notes.pdf` — 39 pages, text-based

## Decisions (locked)
| Decision | Choice |
|---|---|
| Output structure | One combined booklet, organised by topic |
| Question granularity | Substantive problems only (multi-step, ~80–120 questions) |
| Location | `practice/index.html` inside existing MscDS repo |
| Verification | Claude base knowledge + web search (StackExchange / MIT OCW) |
| Design system | Existing MscDS CSS variables + MathJax 3 + new print CSS |

## User Stories
- As a student, I want a single booklet of ~80–120 real probability problems organised by topic so I can practise systematically.
- As a student, I want each problem to show a hint first, then the full worked solution, so I can attempt it before reading the answer.
- As a student, I want to know how confident the solution is (verified / partial / unverified) so I don't internalise a wrong answer.
- As a student, I want to print the booklet as a PDF for offline study.
- As a student, I want problems that cover the same concept from both PDFs to appear together, not duplicated.

## Functional Requirements

### FR1 — Question Extraction
- Read both PDFs, extract every numbered exercise / problem set question
- Filter: include only multi-step questions requiring concept application
- Exclude: definition-restatement questions, trivial one-liners, proofs that are purely algebraic manipulation
- Tag each question with source (MIT / ProbNotes), chapter/section, and a topic label

### FR2 — Topic Organisation
- Group questions into topic buckets (e.g. Counting & Combinatorics, Conditional Probability,
  Random Variables & Expectation, Distributions, Variance)
- Topics derived from the content of both PDFs, not just their chapter headings
- Deduplication: if the same problem (or a near-identical variant) appears in both PDFs, keep one
  instance and note "also appears in [other source]"

### FR3 — Solution Generation
For each question:
1. Claude generates a full solution: approach, working, final answer
2. Claude generates a short 1–2 sentence hint (sufficient to unblock, not to give away answer)
3. Web search for a similar problem on Math StackExchange or MIT OCW
4. Compare Claude answer vs. web source

### FR4 — Confidence Tiers
- ✓ High: Claude and web source agree — cite the web source
- ⚠ Partial: Answers differ — show both workings, flag discrepancy
- ○ Unverified: No web match found — show Claude working only, note "not independently verified"

### FR5 — HTML Output (`practice/index.html`)
- Matches existing MscDS design system (CSS variables, fonts, MathJax 3)
- TOC sidebar with topic groups (same pattern as discrete_mathematics/index.html)
- Each question has: source badge, topic badge, problem statement, collapsible hint, full solution, confidence badge + citation
- Responsive: mobile TOC drawer (same pattern as existing pages)

### FR6 — Print / PDF CSS
- `@media print` stylesheet:
  - Remove sidebar, header nav, collapsible toggles
  - Hints printed in lighter grey or italic before solution (always expanded in print)
  - Each question starts on a new page if solution is long; short questions may share a page
  - Page numbers, section headers in print margin
  - MathJax renders correctly in print (already works in Chrome print-to-PDF)

## Non-Functional Requirements
- Page count target: printable booklet ≤ 80 pages (A4, 12pt, reasonable margins)
- Math rendering: MathJax 3 (existing CDN, same as notes pages)
- Accessibility: confidence badges use both colour and icon/text (not colour alone)
- Accuracy: every ⚠ flagged item clearly shows both answers — user decides which to trust

## Acceptance Criteria
- [ ] `practice/index.html` exists and opens in browser without errors
- [ ] All MathJax renders correctly (no \(...\) raw text visible)
- [ ] ≥ 60 substantive questions extracted and solved
- [ ] Every question has a hint, full solution, and confidence badge
- [ ] TOC sidebar navigates to topic sections
- [ ] Mobile TOC drawer works (same as discrete_mathematics page)
- [ ] Print preview (Chrome) renders clean booklet with no nav UI visible
- [ ] No duplicate questions (same problem from both PDFs appears once)

## Edge Cases
- Question spans multiple pages of PDF: treat as one question
- Sub-parts (a), (b), (c): keep as one entry unless each sub-part is independently substantive
- Question requires a figure/diagram: describe the diagram in text; skip if diagram is essential and unrepresentable
- Formula-heavy questions: ensure LaTeX is correct in MathJax rendering before committing

## Dependencies
- Existing `discrete_mathematics/index.html` as design reference
- MathJax 3 CDN (already used)
- Web search capability (for solution verification)
- `ProbabilityChapter/` folder with two PDFs (not committed to git — large binary files)
