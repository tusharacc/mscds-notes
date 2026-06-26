# PO Requirements: mcq-quiz-for-discrete-math

## Problem Statement

Students studying Discrete Mathematics (MScDS, IIIT Hyderabad) need a self-paced interactive quiz to test their understanding across all lecture weeks. The existing Python quiz (`python/quiz/index.html`) provides the UX reference. This quiz covers Weeks 4–11 of the course, which spans Probability (Wks 4–6) and Linear Algebra (Wks 7–11).

## User Stories

- As a student, I want to practice MCQs from every lecture week so I can identify weak topics before exams.
- As a student, I want immediate feedback (correct/incorrect + explanation) after each answer so I can learn from mistakes.
- As a student, I want a final score summary so I can track overall performance.
- As a student, I want some questions with multiple correct answers so I practice the harder question format used in exams.
- As a student, I want practice-problem-derived questions so I can connect worked examples to exam-style MCQs.

## Functional Requirements

### Question Bank
- **Total:** ~90 questions distributed across Weeks 4–11
- **Types:**
  - Single-choice (radio): ~54 questions (~60%)
  - Multiple-choice (checkbox, ≥2 correct): ~27 questions (~30%)
  - Practice-derived (adapted from `probability_notes_representative_problems.md`): ~9 questions (~10%, can be single or multi)
- **Coverage:** Each week must have at least 8 questions; heavier weeks (9, 10) may have more
- **Week breakdown (suggested):**
  - Week 4: Conditional probability, Bayes' theorem — ~10 Qs
  - Week 5: Random variables, linearity of expectation — ~10 Qs
  - Week 6: Variance, distributions, matrix operations — ~10 Qs
  - Week 7: Linear dependence, vector spaces, dual space — ~10 Qs
  - Week 8: Column/null space, rank-nullity, linear transforms — ~12 Qs
  - Week 9: Determinants, eigenvalues/eigenvectors, norms, dot products, orthogonality — ~14 Qs
  - Week 10: Orthonormal basis, Gram-Schmidt, least squares — ~12 Qs
  - Week 11: Basis changes, linear transforms from different bases — ~10 Qs (2 lectures only)

### Quiz Behavior
- Start screen with title, question count, and "Begin Quiz" button
- Questions shown one at a time with week label and question number
- Single-choice: radio buttons; user selects one
- Multiple-choice: checkboxes; user selects all that apply; clearly labelled "Select all that apply"
- "Submit Answer" button reveals: correct/incorrect indicator, correct answer(s) highlighted, brief explanation
- "Next Question" button advances to next
- Progress bar or counter (e.g. "12 / 90")
- Final score screen: X/90 correct, percentage, per-week breakdown, "Restart" button

### Math Rendering
- MathJax 3 required — many questions involve LaTeX notation (matrices, integrals, eigen equations, norms)
- Inline math: `\( \)`, display math: `\[ \]`

### Output File
- `discrete_mathematics/quiz/index.html` — single self-contained HTML file (no external JS beyond CDN fonts + MathJax)
- Back-link to `../index.html` (the course notes page)

## Non-Functional Requirements

- Same parchment visual design as `python/quiz/index.html` (CSS variables, Playfair Display + Lora fonts, color scheme)
- Week accent colors: reuse the 8-color palette from the Python quiz, cycling if needed
- Mobile-friendly (max-width 700px centered layout)
- No build step — plain HTML/CSS/JS
- MathJax loads from CDN (`cdn.jsdelivr.net/npm/mathjax@3`)

## Acceptance Criteria

- [ ] Exactly one HTML file at `discrete_mathematics/quiz/index.html`
- [ ] ~90 questions total; split is approximately 54/27/9
- [ ] All 8 weeks (4–11) represented with ≥8 questions each
- [ ] Multiple-choice questions clearly labelled "Select all that apply"
- [ ] Submitting a multiple-choice answer with wrong selections marks as incorrect
- [ ] Each question shows an explanation after submission
- [ ] Math notation renders correctly in browser (MathJax)
- [ ] Final screen shows total score and per-week breakdown
- [ ] Visual design matches the Python quiz aesthetic
- [ ] Back link works (relative path `../index.html`)

## Edge Cases

- Multiple-choice: partial credit not awarded — all correct options must be selected and no wrong ones
- Questions with LaTeX must not break layout on mobile
- If MathJax CDN fails, raw LaTeX should still be readable (fallback graceful degradation)

## Dependencies

- **Source transcripts:** `discrete_mathematics/Week{4-11}/*.txt` — questions generated from lecture content
- **Practice problems:** `discrete_mathematics/probability_notes_representative_problems.md` — source for ~9 practice-derived questions
- **Reference quiz:** `python/quiz/index.html` — UI/UX and CSS reference
- **Course notes page:** `discrete_mathematics/index.html` — back-link target
