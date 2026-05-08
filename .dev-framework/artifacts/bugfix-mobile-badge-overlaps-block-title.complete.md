# Complete: bugfix-mobile-badge-overlaps-block-title

**Completed:** 2026-05-08  
**Branch:** `bugfix/bugfix-mobile-badge-overlaps-block-title`

---

## Bug Fixed

On mobile (≤960px), `.block-badge` pill labels (e.g. "KEY FORMULA") were
`position: absolute` inside blocks that had only `1.3rem` right padding. The
badge overlapped the `.block-title` text, hiding it on narrow screens.

---

## Fix

Added `padding-right: 5.5rem` (≈88px) to all five block types inside the
`@media (max-width: 960px)` rule in `discrete_mathematics/index.html`.

```css
@media (max-width: 960px) {
  .def-block, .axiom-block, .example-block, .formula-block, .practice-block {
    padding-right: 5.5rem;
  }
}
```

`5.5rem` reserves enough space to clear the widest badge label ("Key Formula"
≈80px) plus the `.85rem` right offset, with a confirmed 5.6px margin of safety.

---

## Phase Summary

| Phase | Outcome |
|---|---|
| **Developer** | Root cause identified; `padding-right: 5.5rem` fix applied to mobile breakpoint |
| **Reviewer** | APPROVED — 0 High, 0 Medium; 2 Low filed as deferred notes |
| **Tester** | 10 test cases written covering 375/390/414/320px widths, desktop/tablet regression, long titles, badge position, content clipping |
| **Executor** | 10/10 PASS — all cases verified via CSS coordinate analysis |
| **PO Approval** | APPROVED |

---

## Files Changed

| File | Change |
|---|---|
| `discrete_mathematics/index.html` | +3 lines CSS in `@media (max-width: 960px)` block |

---

## Deferred

- L-001: Tablet widths 961–1200px may have residual overlap. Deferred to future enhancement.
