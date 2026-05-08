# Developer Artifact: bugfix-mobile-badge-overlaps-block-title

## Bug Summary

On mobile, the block-title text (e.g. "Sample Space and Event") is visually obscured
by the absolutely-positioned badge label (e.g. "DEFINITION", "KEY FORMULA") in the
top-right corner of each colored block.

## Root Cause Analysis

`.block-badge` is `position: absolute; top: .75rem; right: .85rem` inside each block.
The blocks have `padding-right: 1.3rem` (~21px) on all screen sizes. Badge labels
like "KEY FORMULA" at `.58rem` font size with `.2rem .65rem` padding are ~80px wide.

On mobile (375px screen), the effective content area inside a block is ~294px wide.
The badge occupies ~95px from the right edge (`right: .85rem` + badge width). With
only 21px of right padding on the block, the `.block-title` text — which follows the
badge in normal document flow — wraps into the badge's overlapping region, causing
the title to appear hidden behind or clipped by the badge.

The `@media (max-width: 960px)` rule had no override for block padding.

## Fix Implementation

Added `padding-right: 5.5rem` to all five block types in the mobile breakpoint:

```css
@media (max-width: 960px) {
  .def-block, .axiom-block, .example-block, .formula-block, .practice-block {
    padding-right: 5.5rem;
  }
}
```

`5.5rem` ≈ 88px — clears the widest badge label ("KEY FORMULA") plus the `.85rem`
right offset, with a small margin of safety. Block content remains readable at all
widths ≥ 320px.

## Files Changed

| File | Change |
|---|---|
| `discrete_mathematics/index.html` | Added `padding-right: 5.5rem` to block elements in `@media (max-width: 960px)` |

## Testing Notes

Verify at 375px (iPhone SE), 390px (iPhone 14), and 414px (iPhone 14 Plus) widths:
- Block title text should be fully visible and not overlapping the badge
- Badge should remain in the top-right corner, clear of the title
- No content clipping or horizontal overflow
