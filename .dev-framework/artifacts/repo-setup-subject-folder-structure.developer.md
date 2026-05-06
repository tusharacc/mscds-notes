# Developer Artifact: repo-setup-subject-folder-structure

## Implementation Plan

Executed in strict order to avoid committing mp4s into history at any point.

## Files Changed

| File / Path | Action |
|---|---|
| `.gitignore` | Created — excludes `*.mp4`, `.venv/`, `.DS_Store`, `*.pyc` |
| `discrete_mathematics/index.html` | Moved from `discrete_mathematics.html` via `git mv` |
| `discrete_mathematics/week4/` | Moved from `week4_transcripts/` via `git mv` |
| `discrete_mathematics/week5/` | Moved from `week5_transcripts/` via `git mv` |
| `python/.gitkeep` | Created — placeholder for future subject |
| `README.md` | Created — subject table with GitHub Pages links |

## Code Summary

**`.gitignore`** — global exclusions for mp4/mov/avi, macOS artefacts, Python venv, pyc files.

**`README.md`** — subject table linking to `https://tusharacc.github.io/mscds-notes/discrete_mathematics/`. Instructions for adding new weeks. Note that mp4s are local-only.

**GitHub remote** — `https://github.com/tusharacc/mscds-notes` (public).

**GitHub Pages** — enabled on `main` branch, root `/`. URL: `https://tusharacc.github.io/mscds-notes/`.

## Decisions Made

### History rewrite required
The mp4s were already committed in earlier commits (before this feature). Even after
`git rm --cached`, the blobs remained in git history and GitHub rejected the push
(files 100–200 MB, exceeding GitHub's 100 MB hard limit).

**Fix:** `git-filter-repo --invert-paths --path-glob '*.mp4' --force` rewrote all commits
to permanently exclude mp4 blobs. `git-filter-repo` removed the origin remote as a safety
measure; it was re-added manually before pushing.

### Push strategy
Feature branch pushed directly as `main` on the remote:
```
git push origin feature/repo-setup-subject-folder-structure:main
```
No separate merge commit needed — all history is on this branch.

### `index.html` naming
Named `index.html` (not `discrete_mathematics.html`) so GitHub Pages serves it at
`https://tusharacc.github.io/mscds-notes/discrete_mathematics/` without a filename in the URL.

### `lecture-capture/` untouched
The folder named `lecture_videos` referenced in requirements does not exist.
The actual third folder (`lecture-capture/`) contains the automated pipeline code
and was left completely untouched.
