# Architect Artifact: repo-setup-subject-folder-structure

## System Design

A purely structural change: reorganise the local git repository into a subject-based
hierarchy, publish it as a public GitHub remote, and serve rendered HTML via GitHub Pages.
No build pipeline. No frameworks. Pure static files.

---

## Target Directory Layout

```
/Users/tusharsaurabh/Documents/Projects/MscDS/   ← repo root
├── .gitignore
├── README.md
├── discrete_mathematics/
│   ├── index.html              ← renamed from /discrete_mathematics.html
│   ├── week4/                  ← renamed from /week4_transcripts/
│   │   ├── video1_intro_prob3.txt
│   │   ├── video2_cond_prob1.txt
│   │   ├── video3_cond_prob2.txt
│   │   └── video4_bayes_examples.txt
│   └── week5/                  ← renamed from /week5_transcripts/
│       ├── w5_video1_bayes_examples2.txt
│       ├── w5_video2_random_variables.txt
│       ├── w5_video3_rv_linearity.txt
│       └── w5_video4_linearity_contd.txt
├── python/
│   └── .gitkeep                ← placeholder for future content
├── lecture-capture/            ← existing pipeline; untouched
└── .dev-framework/             ← untouched
```

### Not committed / ignored
- All `*.mp4` files (gitignored, remain on disk locally)
- `.venv/`, `.DS_Store`, `__pycache__/`, `*.pyc`

---

## Components

### C-1 · `.gitignore`
```
# Videos — large files, local only
*.mp4

# macOS
.DS_Store

# Python
.venv/
__pycache__/
*.pyc
*.pyo
```

### C-2 · Git move operations
Use `git mv` to preserve history on moved files:
```bash
# 1. Untrack any already-committed mp4s without deleting local copies
git ls-files --error-unmatch '*.mp4' 2>/dev/null && git rm --cached '*.mp4' || true

# 2. Create subject folder and move HTML
mkdir -p discrete_mathematics
git mv discrete_mathematics.html discrete_mathematics/index.html

# 3. Move transcript folders → subject week folders
git mv week4_transcripts discrete_mathematics/week4
git mv week5_transcripts discrete_mathematics/week5

# 4. Placeholder for future subjects
mkdir python && touch python/.gitkeep
```

### C-3 · README.md
Markdown table linking each subject to its GitHub Pages URL.
GitHub Pages URL pattern for this repo: `https://tusharacc.github.io/mscds-notes/{subject}/`

### C-4 · GitHub remote + Pages
```bash
# Create public repo from current directory
gh repo create mscds-notes --public --source=. --remote=origin --push

# Enable GitHub Pages (branch: main, path: /)
gh api repos/tusharacc/mscds-notes/pages \
  --method POST \
  -f build_type=legacy \
  -f "source[branch]=main" \
  -f "source[path]=/"
```

The developer branch (`feature/repo-setup-subject-folder-structure`) contains all the work.
After local changes are committed, push directly as `main`:
```bash
git push origin feature/repo-setup-subject-folder-structure:main
```

---

## Tech Decisions

| Decision | Choice | Reason |
|---|---|---|
| HTML filename | `index.html` | GitHub Pages serves it at the directory URL — no filename needed in links |
| Pages branch | `main` root `/` | Simplest setup; no separate `gh-pages` branch needed |
| Subject placeholder | `.gitkeep` in `python/` | Git can't track empty directories |
| MP4 untracking | `git rm --cached` | Removes from index, keeps local file intact |
| Repo push | Push feature branch as `main` | All history is on this branch; no extra merge needed |

---

## Open Questions

- None. All requirements are unambiguous.

---

## Implementation Map (for Developer)

1. Write `.gitignore`
2. Commit `.gitignore`
3. Untrack any already-indexed mp4s (`git rm --cached`)
4. `git mv discrete_mathematics.html discrete_mathematics/index.html`
5. `git mv week4_transcripts discrete_mathematics/week4`
6. `git mv week5_transcripts discrete_mathematics/week5`
7. `mkdir python && touch python/.gitkeep`
8. Write `README.md`
9. Commit all changes
10. `gh repo create mscds-notes --public --source=. --remote=origin --push` (pushes current branch)
11. `git push origin feature/repo-setup-subject-folder-structure:main` (makes main match)
12. Enable GitHub Pages via `gh api`
13. Verify Pages URL renders the HTML
