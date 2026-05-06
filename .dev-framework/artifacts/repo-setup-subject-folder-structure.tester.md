# Tester Artifact: repo-setup-subject-folder-structure

## Test Plan

Validate the repository structure, gitignore behaviour, remote repo, GitHub Pages,
and README against the PO acceptance criteria. Tests are grouped into: Local Structure,
Git Index, Remote & Pages, README, and Extensibility.

---

## Test Cases

### TC-01 · Public repo exists and is accessible
- **Input:** Open `https://github.com/tusharacc/mscds-notes` in a browser (or `gh repo view tusharacc/mscds-notes`)
- **Expected:** Repo is public, no login required to view it
- **Pass condition:** Visibility shows "Public"

---

### TC-02 · `discrete_mathematics/index.html` exists
- **Input:** `ls discrete_mathematics/index.html`
- **Expected:** File exists at that path
- **Pass condition:** Command exits 0, file present

---

### TC-03 · No old transcript directories remain
- **Input:** `ls week4_transcripts/ week5_transcripts/`
- **Expected:** Both commands fail with "No such file or directory"
- **Pass condition:** Both directories are gone from the working tree

---

### TC-04 · Transcript txt files are in the new week folders
- **Input:** `ls discrete_mathematics/week4/` and `ls discrete_mathematics/week5/`
- **Expected:**
  - `week4/` contains 4 `.txt` files and 4 `.mp4` files (mp4s present locally)
  - `week5/` contains 4 `.txt` files and 4 `.mp4` files
- **Pass condition:** All 8 txt files present in correct locations

---

### TC-05 · No mp4 files tracked in git index
- **Input:** `git ls-files | grep '\.mp4$'`
- **Expected:** Empty output — zero mp4s tracked
- **Pass condition:** Command produces no output

---

### TC-06 · mp4 files still exist locally (not deleted)
- **Input:** `ls discrete_mathematics/week4/*.mp4` and `ls discrete_mathematics/week5/*.mp4`
- **Expected:** 4 mp4 files in each folder — gitignored but intact on disk
- **Pass condition:** 8 mp4 files found locally

---

### TC-07 · `.gitignore` ignores mp4 globally
- **Input:** `git check-ignore -v discrete_mathematics/week4/video1_intro_prob3.mp4`
- **Expected:** Output shows `.gitignore:1:*.mp4` (or similar) — file is gitignored
- **Pass condition:** The mp4 is matched by a gitignore rule

---

### TC-08 · `python/` placeholder exists
- **Input:** `ls python/.gitkeep`
- **Expected:** File exists
- **Pass condition:** Command exits 0

---

### TC-09 · `lecture-capture/` is untouched
- **Input:** `ls lecture-capture/`
- **Expected:** Contains `capture.py`, `pipeline.py`, `config.yaml`, `requirements.txt`, `SETUP.md`, `credentials/`, `stages/`
- **Pass condition:** Directory structure unchanged from pre-feature state

---

### TC-10 · `lecture-capture/credentials/` is not tracked in git
- **Input:** `git ls-files lecture-capture/credentials/`
- **Expected:** Empty output
- **Pass condition:** No credential files appear in the git index

---

### TC-11 · GitHub Pages is enabled on `main`
- **Input:** `gh api repos/tusharacc/mscds-notes/pages`
- **Expected:** JSON shows `"source": {"branch": "main", "path": "/"}` and `"public": true`
- **Pass condition:** Pages configured correctly

---

### TC-12 · GitHub Pages URL renders the HTML
- **Input:** Open `https://tusharacc.github.io/mscds-notes/discrete_mathematics/` in browser
- **Expected:** Discrete Mathematics notes page loads with Playfair Display headings, all 15 TOC entries, MathJax renders
- **Edge case:** Allow up to 5 minutes for Pages to propagate after first push
- **Pass condition:** Page renders visually (not a 404)

---

### TC-13 · README exists and contains Pages link
- **Input:** `cat README.md | grep tusharacc.github.io`
- **Expected:** Output contains `https://tusharacc.github.io/mscds-notes/discrete_mathematics/`
- **Pass condition:** Link is present

---

### TC-14 · README subjects table is correct
- **Input:** Read `README.md`
- **Expected:** Table has "Discrete Mathematics" row with working Pages link and "python" row marked "Coming soon"
- **Pass condition:** Both rows present with correct content

---

### TC-15 · `discrete_mathematics/index.html` is mobile-responsive
- **Input:** Open `https://tusharacc.github.io/mscds-notes/discrete_mathematics/` in browser DevTools, emulate mobile (375px width)
- **Expected:** TOC rail hides, content fills full width, text remains readable
- **Pass condition:** No horizontal overflow, no obscured content at 375px

---

### TC-16 · No mp4 blobs in git history
- **Input:** `git log --all --full-history -- "*.mp4" | head -5`
- **Expected:** Empty output — history rewrite removed all mp4 references
- **Pass condition:** No commits reference mp4 files
