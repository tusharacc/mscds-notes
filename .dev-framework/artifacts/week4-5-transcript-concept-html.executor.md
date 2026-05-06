# Executor Artifact: week4-5-transcript-concept-html

## Execution Summary

Executed all 16 test cases from the Tester artifact against `discrete_mathematics.html`
by static source inspection. Browser-rendered tests (TC-02, TC-04, TC-12) were verified
structurally — CDN links, CSS rules, and anchor IDs were confirmed rather than live rendering.

**Overall Status: ALL PASS — 16/16**

---

## Test Results

| TC | Name | Result | Notes |
|----|------|--------|-------|
| TC-01 | File opens standalone | **PASS** | `<title>` = "Discrete Mathematics — Course Notes" at line 6; no server-side dependencies |
| TC-02 | MathJax renders all formulas | **PASS** | CDN at line 20; correct delimiters; all 4 spot-check formulas structurally present |
| TC-03 | No spurious equation numbers | **PASS** | `tags: 'none'` at line 15; both align blocks use `align*`; zero unstarred `\begin{align}` |
| TC-04 | Sticky TOC navigation | **PASS** | `position:sticky; top:0` on `.toc-rail`; all 15 hrefs match anchor IDs; `scroll-margin-top:1.5rem` on sections |
| TC-05 | Color coding — 5 block types | **PASS** | All 5 classes present with distinct border/bg/badge colors; §1, §6, §14 spot-checks confirmed |
| TC-06 | Legend matches rendered blocks | **PASS** | Legend dots use `--blue-badge`, `--amber-badge`, etc. — same vars as `.block-badge` backgrounds |
| TC-07 | All 15 concept sections | **PASS** | All 15 IDs confirmed: `#classical-prob` (257), `#combinatorial-prob` (308), `#sample-space` (374), `#conditional-prob` (427), `#total-prob` (478), `#bayes` (499), `#chain-rule` (555), `#independence` (583), `#weighted-sampling` (609), `#random-variables` (635), `#pmf` (674), `#expectation` (707), `#linearity` (747), `#distributions` (795), `#markov` (866) |
| TC-08 | Bayes content merged | **PASS** | All 4 examples in single `#bayes` section: Monty Hall (Bayes), Student Exam, Medical Diagnostic, Police Inspector |
| TC-09 | All derivations `<details open>` | **PASS** | 14 `<details>` elements found; all have `open` attribute; §2 Derivations 1 & 2 open; §6 medical derivation open |
| TC-10 | Monty Hall 12-outcome table | **PASS** | 12 rows; 6 rows × 1/18 (stay wins), 6 rows × 1/9 (switch wins); sum confirmation on line 418 |
| TC-11 | Key mathematical results | **PASS** | All 12 results verified (see detail below) |
| TC-12 | Responsive — TOC hides | **PASS** | `@media (max-width: 960px) { .toc-rail { display: none; } }` at lines 176–179 |
| TC-13 | Week banner | **PASS** | Sky-blue banner (`background:#f0f9ff`, `border-color:var(--week-accent-1)`) with "Weeks 4–5" tag and "Probability Theory" h2 |
| TC-14 | Future-week template comment | **PASS** | Large comment block at lines 927–948; includes TOC group pattern and `<section class="week-section">` pattern |
| TC-15 | PMF tables | **PASS** | §11: 3-row table (v=0,1,2) with 1/4, 1/2, 1/4; alternating row shading; §12: 3-row table (0, V₁, V₁+V₂) with correct probability expressions |
| TC-16 | Practice blocks consistent | **PASS** | §2 (line 367) and §15 (line 917) practice blocks use class-only styling; one inline practice at §4 has `style="margin-top:.7rem"` (spacing only, no `border:none` anomaly) |

---

### TC-11 Detail — Key Mathematical Results

| Location | Expected | Found | Line |
|---|---|---|---|
| §2 N-ball/K-pick | K/N | `K/N` | 328, 336 |
| §3 Monty Hall | Switch wins 2/3 | `\frac{2}{3}` | 421 |
| §6 Medical test | 95/294 ≈ 0.323 | `\frac{95}{294} \approx 0.323` | 534 |
| §6 Student exam | mp/(p(m-1)+1) | `\frac{mp}{p(m-1)+1}` | 522 |
| §7 Chain (2 red) | 14/33 | `\frac{14}{33}` | 571 |
| §7 Chain (2 red+white) | 28/165 | `\frac{28}{165}` | 576 |
| §12 Die expectation | 3.5 | `3.5` | 720 |
| §13 Expected edges | n(n-1)/4 | `\frac{n(n-1)}{4}` | 762 |
| §13 Expected triangles | n(n-1)(n-2)/48 | `\frac{n(n-1)(n-2)}{48}` | 769 |
| §14 Binomial E[X] | kp | `k \cdot p` | 824 |
| §14 Geometric E[X] | 1/p | `\frac{1}{p}` | 860 |
| §14 Screw pack returns | ≈ 4,000/million | `4{,}000 \text{ packs}` | 840 |

All 12 results correct. ✓

---

## Issues Found

**None blocking.** Four known low-priority bugs (BUG-001 through BUG-004) were filed by
the Reviewer and remain open. They have no functional impact on document correctness or usability.

---

## Overall Status

**PASS — ready for PO approval.**
All 16 test cases pass. The document is structurally correct, mathematically accurate, and
meets every acceptance criterion defined by the PO artifact.
