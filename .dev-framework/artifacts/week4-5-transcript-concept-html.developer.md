# Developer Artifact: week4-5-transcript-concept-html

## Implementation Plan

1. ✅ Generate `week4_week5_probability_notes.html` at project root
2. ✅ Embed all CSS inline in `<style>` block (no external stylesheets)
3. ✅ Configure MathJax 3 via CDN with TeX-MML-CHTML renderer
4. ✅ Build sticky TOC with 15 anchor links
5. ✅ Implement all 15 concept sections with color-coded blocks
6. ✅ Include all 52 concepts and every worked example with full derivations
7. ✅ MathJax inline `\(...\)` and display `\[...\]` used throughout

## Files Changed

- `week4_week5_probability_notes.html` — created (single self-contained file, ~650 lines)

## Code Summary

### Structure
Single HTML file with:
- `<head>`: MathJax 3 config + CDN script + embedded CSS (~120 lines)
- `<nav class="toc-rail">`: sticky left TOC, 15 anchor links
- `<main>`: 15 concept sections, each using colored block components

### CSS Design System
Five semantic block classes:
| Class | Category | Color |
|---|---|---|
| `.def-block` | Definition | Blue (#3b82f6) |
| `.axiom-block` | Axiom/Theorem | Amber (#f59e0b) |
| `.example-block` | Worked Example | Green (#22c55e) |
| `.formula-block` | Key Formula | Violet (#8b5cf6) |
| `.practice-block` | Practice/HW | Grey (#9ca3af) |

Each block has a `.block-badge` pill positioned top-right.

### Sections Implemented (all 15)
1. Classical Probability & Equally Likely Outcomes — Kolmogorov axioms, P(E)=|E|/|S|, monotonicity axiom
2. Combinatorial Probability — N-ball K-pick (two derivations), 52-card deck (two derivations)
3. Sample Space Construction — Tree method, Monty Hall full 12-outcome table
4. Conditional Probability — Definition, two-coin, two-dice, red/blue balls
5. Law of Total Probability — Two-part and k-partition forms
6. Bayes' Theorem — Rule + 4 examples: Monty Hall (Bayes), student exam, medical test, police inspector
7. Chain Rule — Definition + red/white balls two-step derivation
8. Independence of Events — Pairwise and mutual independence
9. Weighted/Non-Uniform Sampling — Balls with weights R and W
10. Random Variables — Definition, types, 3 canonical examples, highest-ball problem
11. PMF — Definition, normalization axiom, two-coin PMF table
12. Expectation — Definition, die roll, two coin tosses, sequential exam question
13. Linearity of Expectation — Theorem, expected edges, expected triangles, hat-check, stock price
14. Special Distributions — Bernoulli, Binomial (PMF, linearity proof E[X]=kp, screw pack), Geometric (PMF, E[X]=1/p)
15. Markov Inequality — Theorem + proof, equivalent forms, binomial application, screw pack bound, tail inequalities preview

### Concepts Coverage
All 52 concepts from PO inventory implemented. Bayes theorem content from week4-video4 and w5-video1 merged into §6.

## Decisions Made

- Used `<details open>` for long derivations — readable by default, collapsible for review.
- Probability table for Monty Hall included inline (all 12 outcomes with switch-wins column).
- MathJax `\begin{align}...\end{align}` used for multi-line derivations (medical test, Markov proof).
- Responsive: TOC rail hidden on ≤900px screens (CSS media query); content remains fully readable on mobile.
- `crossorigin="anonymous"` on MathJax CDN script (no SRI hash available for MathJax CDN, but origin isolation is maintained).
- `scroll-margin-top: 1.5rem` on sections to prevent sticky TOC overlap during anchor navigation.
