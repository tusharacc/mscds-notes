# MScDS Notes — IIIT Hyderabad

Course notes for the Master of Science in Data Science (MScDS) programme at IIIT Hyderabad.
Notes are generated from lecture transcripts, enriched with derivations and worked examples,
and rendered as self-contained HTML documents.

**[Open Study Hub →](https://tusharacc.github.io/mscds-notes/)**

## Notes

| Subject | Link | Coverage |
|---|---|---|
| Discrete Mathematics | [View notes](https://tusharacc.github.io/mscds-notes/discrete_mathematics/) | Weeks 1–7: Probability, random variables, linear algebra |
| Python | [View notes](https://tusharacc.github.io/mscds-notes/python/) | Weeks 1–10: Foundations, expressions, loops, sorting, lists, functions, dictionaries, recursion, applied project |

## Practice Problems

| Booklet | Link | Content |
|---|---|---|
| Probability | [Open booklet](https://tusharacc.github.io/mscds-notes/practice/) | 40 solved problems — sample spaces, Bayes, expectations, variance, deviation bounds |
| Linear Algebra | [Open booklet](https://tusharacc.github.io/mscds-notes/practice/linear-algebra.html) | 40 solved problems — matrices, inverses, linear systems, vector spaces, transformations |

## Quizzes

| Subject | Link | Content |
|---|---|---|
| General Practice Quiz | [Open quiz](https://tusharacc.github.io/mscds-notes/quiz/) | 10-question sessions — MCQ with instant feedback + worked problems with self-marking. Covers Probability and Linear Algebra. |
| Discrete Mathematics Quiz | [Open quiz](https://tusharacc.github.io/mscds-notes/discrete_mathematics/quiz/) | MCQ quiz covering Weeks 1–3 — Probability, random variables, Bayes theorem, conditional probability |
| Python Quiz | [Open quiz](https://tusharacc.github.io/mscds-notes/python/quiz/) | 94 MCQs covering Weeks 1–10 — Foundations, expressions, loops, functions, dictionaries, recursion |

## Structure

```
discrete_mathematics/   ← notes + transcripts
python/                 ← notes + transcripts
practice/               ← solved problem booklets
quiz/                   ← interactive quiz module
```

Each page is a standalone HTML file — no server required.
All pages are served via GitHub Pages at the links above.

## Adding a new week

1. Create `subject_name/weekN/` and add transcript `.txt` files
2. Update `subject_name/index.html` with new content following the existing section template
3. Commit and push — GitHub Pages updates automatically

## Notes

- Video files (`.mp4`) are excluded from this repository and stored locally only
- All mathematical notation uses [MathJax 3](https://www.mathjax.org/)
