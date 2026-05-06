# Architect Design: week4-5-transcript-concept-html

## System Design

Single static HTML file (`week4_week5_probability_notes.html`) at project root.
No build toolchain — pure HTML/CSS/JS with MathJax 3 via CDN.

## Document Structure

```
<html>
  <head>
    MathJax 3 config + CDN script
    Embedded CSS (color categories, layout, sticky nav)
  </head>
  <body>
    <nav> Sticky TOC with anchor links to all sections </nav>
    <main>
      [15 concept sections, each with subsections]
    </main>
  </body>
</html>
```

## Section Order & Anchor IDs

1. `#classical-prob` — Classical Probability & Equally Likely Outcomes
2. `#combinatorial-prob` — Combinatorial Probability
3. `#sample-space` — Sample Space Construction
4. `#conditional-prob` — Conditional Probability
5. `#total-prob` — Law of Total Probability
6. `#bayes` — Bayes' Theorem (merged week4-video4 + w5-video1)
7. `#chain-rule` — Chain Rule (Multiplication Rule)
8. `#independence` — Independence of Events
9. `#weighted-sampling` — Weighted / Non-Uniform Sampling
10. `#random-variables` — Random Variables
11. `#pmf` — Probability Mass Function
12. `#expectation` — Expectation
13. `#linearity` — Linearity of Expectation
14. `#distributions` — Special Distributions (Bernoulli, Binomial, Geometric)
15. `#markov` — Markov Inequality & Tail Inequalities

## Color-Coding System (CSS classes)

| Category | CSS class | Color scheme |
|---|---|---|
| Definition | `.def-block` | Blue-tinted left border (#3b82f6), bg #eff6ff |
| Axiom / Theorem | `.axiom-block` | Amber border (#f59e0b), bg #fffbeb |
| Worked Example | `.example-block` | Green border (#22c55e), bg #f0fdf4 |
| Key Formula / Result | `.formula-block` | Violet border (#8b5cf6), bg #f5f3ff |
| Practice Problem | `.practice-block` | Grey border (#9ca3af), bg #f9fafb |

Each block has a small colored pill badge ("Definition", "Axiom", "Example", etc.) top-right.

## MathJax Configuration

- MathJax 3, loaded from `cdn.jsdelivr.net`
- Inline math: `\(...\)`
- Display math: `\[...\]`
- Config: `tex-mml-chtml` renderer, `ams` extension for `\begin{align}` environments

## Component Breakdown

Each concept section contains 1–N of:
- A `.def-block` for the definition
- One or more `.axiom-block` for axioms/theorems
- One or more `.example-block` for worked examples (each with problem → derivation → result)
- A `.formula-block` for the key formula box
- Optionally a `.practice-block` for exercises mentioned in lecture

## Tech Decisions

- **No external CSS framework** — keeps the file fully self-contained after MathJax loads.
- **Sticky left-rail TOC** on ≥1024px screens; collapses to top nav on mobile.
- **Smooth scroll** via CSS `scroll-behavior: smooth`.
- **`<details>/<summary>`** used for long derivations to allow collapsing — but expanded by default.
- All 52 concepts from PO inventory mapped to sections; none deferred.

## Open Questions

None — requirements fully specified by PO.
