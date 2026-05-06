# Tester Artifact: week4-5-transcript-concept-html

## Test Plan

Test the single output file `discrete_mathematics.html` against the PO acceptance criteria.
Tests are grouped into: Structure, Content, Math Rendering, Visual/UX, and Extensibility.

---

## Test Cases

### TC-01 · File opens standalone in browser
- **Input:** Open `discrete_mathematics.html` by double-clicking (file:// URL, no server)
- **Expected:** Page renders fully; no blank white screen; title shows "Discrete Mathematics — Course Notes"
- **Edge case:** Test without internet (MathJax CDN unavailable) — page text/structure should still render; math will show raw LaTeX (acceptable degradation)

---

### TC-02 · MathJax renders all formulas
- **Input:** Open file with internet connection; wait 3–5 seconds for MathJax to load
- **Expected:** All `\(...\)` inline math and `\[...\]` display math blocks render as typeset equations, not raw LaTeX strings
- **Spot-check formulas:**
  - §1: \(P(E) = |E|/|S|\)
  - §6 medical test: multi-line align block renders without equation numbers
  - §14 screw pack: multi-line align block renders without equation numbers
  - §15 Markov proof: long inline chain renders on one display line

---

### TC-03 · No spurious equation numbers
- **Input:** Open file; inspect all `\begin{align*}` blocks (§6 medical test, §14 screw pack)
- **Expected:** No "(1)", "(2)", "(3)" labels appear next to any equation line
- **Pass condition:** Zero equation number annotations visible anywhere in the document

---

### TC-04 · Sticky TOC navigation
- **Input:** Click each of the 15 TOC links in the left rail
- **Expected:** Page scrolls to the correct section; the section heading is visible below any sticky elements (not hidden behind the TOC header)
- **Edge case:** Click "15 · Markov Inequality" — page scrolls to bottom section correctly

---

### TC-05 · Color coding — all 5 block types present and visually distinct
- **Input:** Visually scan the rendered page
- **Expected:**
  - Blue left-border + blue-tinted background → Definition blocks
  - Amber left-border + cream background → Axiom/Theorem blocks
  - Green left-border + pale-green background → Example blocks
  - Violet left-border + lavender background → Key Formula blocks
  - Grey left-border + off-white background → Practice blocks
- **Spot-check:** §1 has both Definition and Axiom blocks; §6 has Example blocks; §14 has both Definition and Key Formula blocks

---

### TC-06 · Legend matches rendered blocks
- **Input:** Compare the legend dots in the page header with the actual block colors
- **Expected:** Each legend dot color matches the corresponding block border/badge color exactly

---

### TC-07 · All 15 concept sections present
- **Input:** Check page source or inspect TOC
- **Expected:** All 15 anchor IDs exist and are non-empty:
  `#classical-prob`, `#combinatorial-prob`, `#sample-space`, `#conditional-prob`, `#total-prob`, `#bayes`, `#chain-rule`, `#independence`, `#weighted-sampling`, `#random-variables`, `#pmf`, `#expectation`, `#linearity`, `#distributions`, `#markov`

---

### TC-08 · Bayes theorem content is merged (not split across two sections)
- **Input:** Navigate to §6 (Bayes' Theorem)
- **Expected:** The section contains all 4 examples — Monty Hall (Bayes approach), Student Exam, Medical Diagnostic Test, Police Inspector — within a single `#bayes` section, not split between two sections
- **Failure condition:** Any Bayes example appears in a separate section outside §6

---

### TC-09 · All derivations use `<details open>` (expanded by default)
- **Input:** Open page fresh; navigate to §2 (N-ball K-pick) and §6 (medical test)
- **Expected:** All derivation sub-sections are expanded on load (details[open] attribute); user can collapse them
- **Spot-check:** N-ball "Derivation 1" and "Derivation 2" both expanded; medical test "Full derivation" expanded

---

### TC-10 · Monty Hall 12-outcome table completeness and correctness
- **Input:** Navigate to §3; inspect the sample space table
- **Expected:**
  - Exactly 12 rows present
  - Probability column: 6 rows show \(\tfrac{1}{18}\), 6 rows show \(\tfrac{1}{9}\)
  - "Switch wins?" column: exactly 6 rows say "Yes" (the off-diagonal outcomes)
  - Sum notation below table confirms total = 1

---

### TC-11 · Key mathematical results correct
- **Input:** Read the following result-lines
- **Expected values:**

| Location | Result |
|---|---|
| §2 N-ball/K-pick | \(K/N\) |
| §3 Monty Hall | Switch wins with prob \(2/3\) |
| §6 Medical test | \(95/294 \approx 0.323\) |
| §6 Student exam | \(mp / (p(m-1)+1)\) |
| §7 Chain rule (2 red) | \(14/33\) |
| §7 Chain rule (2 red + white) | \(28/165\) |
| §12 Die roll expectation | \(3.5\) |
| §13 Expected edges | \(n(n-1)/4\) |
| §13 Expected triangles | \(n(n-1)(n-2)/48\) |
| §14 Binomial \(\mathbb{E}[X]\) | \(kp\) |
| §14 Geometric \(\mathbb{E}[X]\) | \(1/p\) |
| §14 Screw pack returns | \(\approx 4{,}000\) per million |

---

### TC-12 · Responsive layout — TOC hides on narrow screens
- **Input:** Resize browser window to < 960px width (or use DevTools mobile emulation)
- **Expected:** TOC rail disappears; main content fills full width; all content remains readable

---

### TC-13 · Week banner renders correctly
- **Input:** Observe the top of the content area below the page header
- **Expected:** A sky-blue banner with "Weeks 4–5" label and "Probability Theory" heading is visible before the first concept section

---

### TC-14 · Future-week template comment is present
- **Input:** View page source (Ctrl+U)
- **Expected:** A large HTML comment block near the bottom of `<main>` shows the template for adding future week sections, including the TOC group pattern and the `<section class="week-section">` pattern

---

### TC-15 · PMF tables render correctly
- **Input:** Navigate to §11 (PMF) and §12 (Expectation — Sequential Exam)
- **Expected:**
  - §11 table has 3 rows (\(v\) = 0, 1, 2) with correct probabilities (\(\tfrac{1}{4}\), \(\tfrac{1}{2}\), \(\tfrac{1}{4}\)) and alternating row shading
  - §12 exam table has 3 rows (0, \(V_1\), \(V_1+V_2\)) with correct probability expressions

---

### TC-16 · Practice blocks styled consistently
- **Input:** Navigate to §2 (Practice block at bottom) and §15 (Practice block at bottom)
- **Expected:** Both blocks have grey left border, off-white background, and grey "PRACTICE" badge — consistent styling, no `border:none` anomalies
