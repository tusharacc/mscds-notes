# Tester Artifact: bugfix-mobile-badge-overlaps-block-title

## Test Plan

Verify that badge labels no longer overlap block titles on mobile screen widths,
and that no desktop or tablet regressions were introduced.

---

## Test Cases

### TC-01 — Badge clears block title at iPhone SE width (375px)
- **Setup:** Open `discrete_mathematics/index.html` in Chrome DevTools, set viewport to 375px wide
- **Action:** Scroll to any colored block (Definition, Axiom, Key Formula, Example, Practice)
- **Expected:** Block title text is fully visible; no characters hidden behind or clipped by the badge pill
- **Blocks to check:** "Sample Space and Event" (Definition), "Kolmogorov Axioms" (Axiom), "Equally Likely Outcomes" (Key Formula)

### TC-02 — Badge clears block title at iPhone 14 width (390px)
- **Setup:** Viewport at 390px
- **Action:** Inspect all block types
- **Expected:** Same as TC-01 — title fully visible, badge top-right and non-overlapping

### TC-03 — Badge clears block title at iPhone 14 Plus width (414px)
- **Setup:** Viewport at 414px
- **Action:** Inspect all block types
- **Expected:** Same as TC-01

### TC-04 — Widest badge label does not overlap ("KEY FORMULA" / "Key Formula")
- **Setup:** Viewport at 375px
- **Action:** Locate the "Key Formula" block (violet) on the page
- **Expected:** The pill label is fully in the top-right corner, the title text starts below or to the left of it with no overlap

### TC-05 — No horizontal overflow at 320px (minimum supported width)
- **Setup:** Viewport at 320px
- **Action:** Inspect all colored blocks
- **Expected:** No horizontal scrollbar appears; block content stays within viewport

### TC-06 — Desktop layout unchanged (1280px)
- **Setup:** Viewport at 1280px
- **Action:** Inspect all block types
- **Expected:** Blocks render as before the fix — no unexpected right-padding increase visible on desktop

### TC-07 — Tablet layout unchanged (1024px)
- **Setup:** Viewport at 1024px (just above 960px breakpoint)
- **Action:** Inspect all block types
- **Expected:** No change from desktop behavior; mobile breakpoint not triggered

### TC-08 — Block title text wraps correctly on narrow widths
- **Setup:** Viewport at 375px
- **Action:** Find a block with a long title (e.g. "N Balls, K Picks — Probability of Picking the Special Ball")
- **Expected:** Title wraps within its content area (left of badge), does not extend under the badge

### TC-09 — Badge position unchanged (still top-right of block)
- **Setup:** Viewport at 375px
- **Action:** Inspect `.block-badge` elements using DevTools
- **Expected:** Badge remains `position: absolute; top: .75rem; right: .85rem` — not repositioned by the fix

### TC-10 — No content clipping inside blocks
- **Setup:** Viewport at 375px
- **Action:** Check block body text (definitions, formulas, bullet lists) for clipping
- **Expected:** All block body text is fully readable; no overflow:hidden clipping
