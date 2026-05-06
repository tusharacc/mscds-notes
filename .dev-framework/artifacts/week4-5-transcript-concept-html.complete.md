# Complete: week4-5-transcript-concept-html

**Completed:** 2026-05-06  
**Output:** `discrete_mathematics.html`  
**Branch:** `feature/week4-5-transcript-concept-html`

---

## What Was Built

A self-contained, scholarly HTML reference document covering all probability theory concepts
from Weeks 4–5 of the MScDS programme at IIIT Hyderabad. Designed to grow: future weeks
can be appended following the embedded template.

---

## Phase Summary

| Phase | Outcome |
|---|---|
| **PO** | Requirements gathered: single HTML, MathJax 3, full derivations, color-coded blocks, no concept omitted, week-based structure for future additions |
| **Architect** | Two-column layout (sticky TOC + main), 15 concept sections inside a week wrapper, 5 semantic block classes, MathJax config design |
| **Developer** | Built `discrete_mathematics.html` (~950 lines); resolved MathJax `tags:'ams'` equation-numbering bug; merged Bayes content from two separate lecture videos; implemented 12-row Monty Hall table, all derivations, all distributions |
| **Reviewer** | Approved; 0 High/Medium issues; 4 Low issues filed as BUG-001–004 |
| **Tester** | 16 test cases written across structure, math rendering, content correctness, visual system, and extensibility |
| **Executor** | 16/16 PASS — all mathematical results verified correct |
| **Frontend Design** | CSS redesigned post-executor: Playfair Display + Lora typography, warm parchment palette, hover-lift on blocks, staggered fadeUp animation, BUG-004 patched |
| **PO Approval** | APPROVED — all acceptance criteria met |

---

## Key Decisions

- `tags: 'none'` + `\begin{align*}` prevents equation auto-numbering in MathJax 3
- `<details open>` on all derivation blocks — expanded by default, collapsible by user
- `data-week` attribute on `<section class="week-section">` enables per-week CSS theming
- Bayes' theorem from two lecture videos merged into single `#bayes` section with 4 examples
- Large HTML comment template at bottom of `<main>` documents exactly how to add future weeks

---

## Open Bugs (deferred)

| ID | Description |
|---|---|
| BUG-001 | `.toc-week.upcoming` CSS class defined but unused |
| BUG-002 | Week banner CSS missing for future `data-week="6"` etc. |
| BUG-003 | `--week-accent-2/3/4` CSS variables unused in live rules |

All Low severity. Address when adding Week 6 content.
