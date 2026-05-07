# Complete: repo-setup-subject-folder-structure

**Completed:** 2026-05-07  
**Branch:** `feature/repo-setup-subject-folder-structure`

---

## What Was Built

A public GitHub repository (`mscds-notes`) with subject-based folder structure,
GitHub Pages serving rendered HTML notes, and a clean git history with all
video files excluded.

---

## Live Outputs

| Artefact | URL |
|---|---|
| GitHub repo | https://github.com/tusharacc/mscds-notes |
| Discrete Mathematics notes | https://tusharacc.github.io/mscds-notes/discrete_mathematics/ |

---

## Phase Summary

| Phase | Outcome |
|---|---|
| **PO** | Requirements: public repo `mscds-notes`, subject folders, `weekN` convention, GitHub Pages, README with links, mp4 gitignored |
| **Architect** | `index.html` naming for clean Pages URLs; `git mv` for history preservation; `git filter-repo` for mp4 purge; push feature branch as `main` |
| **Developer** | Implemented all moves; discovered mp4 blobs blocked push (files up to 200 MB); resolved with `git filter-repo`; Pages enabled via `gh api`; all 9 AC met |
| **Reviewer** | Approved — 0 High/Medium; BUG-005 and BUG-006 filed (config.yaml password field, root gitignore gap) |
| **Tester** | 16 test cases written covering structure, git hygiene, Pages, README, mobile responsiveness, history cleanliness |
| **Executor** | 16/16 PASS — all verified live |
| **PO Approval** | APPROVED |

---

## Key Decisions

- `index.html` at subject root — GitHub Pages serves it at directory URL without filename
- `git filter-repo` to purge mp4 blobs from entire history before push (unplanned but required)
- Feature branch pushed directly as `main` — all history on one branch, no extra merge
- `lecture-capture/` left completely untouched — contains pipeline code, not notes

---

## Open Bugs (deferred)

| ID | Description |
|---|---|
| BUG-001 | `.toc-week.upcoming` CSS class unused (discrete_mathematics) |
| BUG-002 | Week banner CSS missing for future `data-week="6"` |
| BUG-003 | `--week-accent-2/3/4` CSS vars unused in live rules |
| BUG-005 | `lecture-capture/config.yaml` has plaintext OBS password field (now public) |
| BUG-006 | Root `.gitignore` doesn't explicitly cover `lecture-capture/credentials/` |

Address BUG-001/002/003 when adding Week 6 content. Address BUG-005/006 in next enhancement cycle.

---

## Adding the Next Subject

1. Create `subject_name/` folder with `index.html` and `week1/`, `week2/` etc.
2. Add a row to the README subjects table with the Pages URL
3. Commit and push — Pages updates automatically
