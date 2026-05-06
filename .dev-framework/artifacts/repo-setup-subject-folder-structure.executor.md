# Executor Artifact: repo-setup-subject-folder-structure

## Execution Summary

All 16 test cases executed against the live implementation.

**Overall Status: ALL PASS — 16/16**

---

## Test Results

| TC | Name | Result | Evidence |
|----|------|--------|---------|
| TC-01 | Public repo exists | **PASS** | `gh repo view` → visibility: PUBLIC |
| TC-02 | `discrete_mathematics/index.html` exists | **PASS** | File present at correct path |
| TC-03 | Old transcript dirs removed | **PASS** | `week4_transcripts/` and `week5_transcripts/` → "No such file or directory" |
| TC-04 | Txt files in new week folders | **PASS** | 4 txt files in `week4/`, 4 in `week5/` |
| TC-05 | No mp4s tracked in git index | **PASS** | `git ls-files \| grep .mp4` → empty |
| TC-06 | Mp4s still exist locally | **PASS** | 4 mp4s in `week4/`, 4 in `week5/` — gitignored but on disk |
| TC-07 | `.gitignore` matches mp4s | **PASS** | `.gitignore:2:*.mp4` — matched by line 2 rule |
| TC-08 | `python/.gitkeep` exists | **PASS** | File present |
| TC-09 | `lecture-capture/` untouched | **PASS** | All 7 expected items present: `capture.py`, `config.yaml`, `credentials/`, `pipeline.py`, `requirements.txt`, `SETUP.md`, `stages/` |
| TC-10 | Credentials not tracked in git | **PASS** | `git ls-files lecture-capture/credentials/` → 0 files |
| TC-11 | GitHub Pages enabled on `main` | **PASS** | API returns `{branch: "main", path: "/", public: true, status: "built"}` |
| TC-12 | Pages URL returns 200 | **PASS** | `curl` → HTTP 200 at `https://tusharacc.github.io/mscds-notes/discrete_mathematics/` |
| TC-13 | README contains Pages link | **PASS** | Link present: `https://tusharacc.github.io/mscds-notes/discrete_mathematics/` |
| TC-14 | README subject table correct | **PASS** | "Discrete Mathematics" row with link; "Python" row with "Coming soon" |
| TC-15 | Mobile responsive breakpoint | **PASS** | `@media (max-width: 960px)` at line 268 of `index.html` |
| TC-16 | No mp4 blobs in git history | **PASS** | `git log --all --full-history -- "*.mp4"` → 0 commits |

---

## Issues Found

None. All acceptance criteria pass.

**Open bugs** (filed by reviewer, deferred):
- BUG-005: `config.yaml` password field public (Low)
- BUG-006: Root gitignore missing explicit `lecture-capture/credentials/` entry (Low)

---

## Overall Status

**PASS — ready for PO approval.**
