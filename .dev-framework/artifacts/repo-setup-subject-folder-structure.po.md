# PO Artifact: repo-setup-subject-folder-structure

## Problem Statement

Set up a public GitHub repository (`mscds-notes`) with a subject-based folder structure
for MScDS notes. Discrete Mathematics is the first subject; Python, Algorithms, etc. will
follow. Videos stay local (gitignored). Transcripts and HTML notes are committed.
GitHub Pages serves the rendered HTML. README provides direct links per subject.

---

## Functional Requirements

### FR-1 · GitHub repository
- Create public repo named `mscds-notes` using `gh repo create`
- Push existing local git history to the remote

### FR-2 · Folder structure
Top-level layout (subject folders at root):
```
mscds-notes/
├── .gitignore
├── README.md
├── discrete_mathematics/
│   ├── index.html          ← renamed from discrete_mathematics.html
│   ├── week4/              ← contents of week4_transcripts/ (txt files only)
│   └── week5/              ← contents of week5_transcripts/ (txt files only)
├── python/                 ← empty placeholder (.gitkeep)
└── lecture-capture/        ← existing pipeline code, stays untouched
```
Future subjects follow the same pattern: `subject_name/index.html` + `subject_name/weekN/`.

### FR-3 · Move & rename operations
- Move `week4_transcripts/` → `discrete_mathematics/week4/`
- Move `week5_transcripts/` → `discrete_mathematics/week5/`
- Move `discrete_mathematics.html` → `discrete_mathematics/index.html`
- Update any internal hrefs/paths in `index.html` if needed (MathJax CDN is external; no internal paths expected)

### FR-4 · Week folder naming convention
All week folders use `weekN` (e.g., `week4`, `week5`, `week6`). No underscores, no suffixes like `_transcripts`.

### FR-5 · .gitignore
Ignore all MP4 files globally:
```
*.mp4
```
Additionally ignore OS/editor noise: `.DS_Store`, `*.pyc`, `__pycache__/`.

### FR-6 · GitHub Pages
- Enable GitHub Pages on the `main` branch, serving from root `/`
- Rendered URL pattern: `https://{username}.github.io/mscds-notes/discrete_mathematics/`
- The `index.html` at each subject root is served automatically by Pages

### FR-7 · README
- Brief description of the repo
- Table of subjects with:
  - Subject name
  - GitHub Pages link to rendered HTML
  - Status (e.g., Weeks 4–5 complete)
- Instructions for adding new weeks (one-liner)

---

## Non-Functional Requirements

- HTML (`discrete_mathematics/index.html`) must be mobile-responsive — already implemented via `@media (max-width: 960px)`; verify it still renders correctly after the move
- No build step — pure static HTML served by GitHub Pages
- `.mp4` files must never appear in git history (gitignore must be in place before any `git add`)

---

## Acceptance Criteria

| # | Criterion |
|---|---|
| AC-1 | `mscds-notes` public repo exists on GitHub and is accessible without login |
| AC-2 | `discrete_mathematics/index.html` exists and is the moved/renamed `discrete_mathematics.html` |
| AC-3 | `discrete_mathematics/week4/` and `discrete_mathematics/week5/` exist with `.txt` transcript files |
| AC-4 | No `.mp4` files appear in the git index (`git ls-files *.mp4` returns empty) |
| AC-5 | GitHub Pages is enabled; `https://{username}.github.io/mscds-notes/discrete_mathematics/` renders the HTML |
| AC-6 | README contains a working GitHub Pages link per subject |
| AC-7 | `python/` placeholder folder exists (`.gitkeep`) |
| AC-8 | `week4_transcripts/` and `week5_transcripts/` directories are removed |
| AC-9 | `lecture-capture/` pipeline code is untouched |

---

## Edge Cases & Risks

### ⚠️ No `lecture_videos` folder found
The request mentioned deleting a folder called `lecture_videos`. No such folder exists.
The third folder is `lecture-capture/` which contains the automated pipeline code
(`capture.py`, `pipeline.py`, `credentials/`, etc.) — **this must NOT be deleted**.
**Action:** `lecture-capture/` is left in place. If there is another folder to delete,
the developer must confirm with the user before removing it.

### MathJax CDN path
`index.html` uses an external CDN for MathJax — no path changes needed after the move.

### Git history
`discrete_mathematics.html` is being moved via `git mv` to preserve history.
Same for transcript folders.

### GitHub Pages propagation delay
After enabling Pages, the URL may take 1–2 minutes to go live.

---

## Dependencies

- `gh` CLI authenticated (`gh auth status` passes)
- GitHub account has permission to create public repos
- Local git repo at `/Users/tusharsaurabh/Documents/Projects/MscDS` (exists, confirmed)
