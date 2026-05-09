# Dev Framework Checkpoint
**Date**: 2026-05-09
**Workspace**: (none)
**Phase**: —
**Branch**: main
**Workflow**: —

## Done this session
- feat(python): add Week 4–5 study notes page
- fix(discrete-maths): split TOC into separate Week 4 and Week 5 groups

## Where things stand
No active dev-framework workspace. All three previous workspaces are archived
(bugfix-mobile-badge-overlaps-block-title, repo-setup-subject-folder-structure,
week4-5-transcript-concept-html). This session's work was done directly on main:

1. **python/index.html** — full study notes page for Python Weeks 4–5. Covers
   while loops, for loops, range(), loop invariants (formal + assert-encoded),
   isSorted, bubble sort (naive + optimized), two-level loop invariants, and
   Python list operations (create, access, modify, search). Matches the
   discrete_mathematics design system exactly (same fonts, CSS variables,
   block-badge types, mobile TOC drawer, progress bar, active-section tracking).

2. **discrete_mathematics/index.html TOC** — split the single "Weeks 4–5 ·
   Probability" TOC group into two separate groups matching the Python style:
   - Week 4 · Probability Foundations (§1–§8)
   - Week 5 · Random Variables & Expectation (§9–§17)

3. **README.md** — updated Python row from "Coming soon" to live GitHub Pages link.

## Pending decisions
- [ ] Python Week 4–5 transcripts only partially covered (5.2.1 Lists covers
      only creation/modification/search — list sorting/copying/reversing deferred
      to next lecture; add when week 6 transcripts arrive)
- [ ] No formal dev-framework workspace was opened for this session's work;
      consider whether to retroactively create one or just track via git log
- [ ] GitHub Pages for python/ may still be propagating (pushed ~end of session)

## Next action
When new transcripts arrive (Week 6+): run `/dev new-feature` to open a workspace,
read transcripts, and extend the relevant subject's index.html with new sections.
