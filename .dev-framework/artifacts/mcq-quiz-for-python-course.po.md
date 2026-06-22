# PO Artifact: mcq-quiz-for-python-course

## Problem Statement

The student has an upcoming test in the MScDS Python Core & Applied Concepts course (IIIT Hyderabad). The test format is multiple-choice questions. A static quiz page is needed that draws from a bank of up to 100 MCQs covering Weeks 1–10 of the course, presents 5 random questions per session, scores the attempt, and explains every answer (correct or not). The page must be hostable on GitHub Pages and match the existing parchment aesthetic of the notes site.

---

## User Stories

1. **As a student**, I want to attempt 5 random MCQs so I can practise without being overwhelmed.
2. **As a student**, I want to see whether my answer is correct immediately after submitting it, along with a clear explanation, so I can learn from each question.
3. **As a student**, I want a final score summary at the end so I know how well I did overall.
4. **As a student**, I want to retake the quiz (get a fresh random 5) without reloading the page so I can keep practising.
5. **As a student**, I want questions that include code snippets so I practise reading Python code, not just theory.
6. **As a student**, I want the quiz to cover all 10 weeks so every topic I'll be tested on is represented.

---

## Functional Requirements

### Question Bank
- FR1: The question bank contains **80–100 MCQs** (hard cap: 100) drawn from Weeks 1–10 content.
- FR2: Each question has exactly **4 answer options** (A, B, C, D).
- FR3: Each question has exactly **1 correct answer**.
- FR4: Each question has an **explanation** (2–4 sentences) that is shown after the user answers, regardless of whether they were right or wrong.
- FR5: Questions are tagged by **week** (1–10) so the bank can be maintained per-week.
- FR6: Questions include a mix of:
  - Conceptual/definition questions
  - Code-reading questions ("What does this snippet output / raise?")
  - Comparative questions ("Which of the following is true about X vs Y?")

### Quiz Session
- FR7: On page load, **5 questions are randomly selected** from the full bank (no repetition within a session).
- FR8: Questions are presented **one at a time** — the user sees Question N, picks an answer, submits, sees feedback, then proceeds to Question N+1.
- FR9: After the user picks an option and clicks **"Submit Answer"**, the chosen option is highlighted (green = correct, red = incorrect), the correct answer is marked, and the explanation is revealed.
- FR10: A **"Next Question"** button appears after feedback is shown; it advances to the next question.
- FR11: After Question 5, a **Score Summary screen** is shown: X / 5 correct, with a brief per-question recap (question text, user's answer, correct answer, pass/fail indicator).
- FR12: A **"Retake Quiz"** button on the summary screen picks a fresh random 5 and restarts the session without a full page reload.
- FR13: No timer — untimed practice.

### Navigation & Integration
- FR14: The page lives at `python/quiz/index.html` in the existing repo, matching the existing `quiz/index.html` path already linked from the notes TOC.
- FR15: The page uses the same parchment design system (Playfair Display + Lora fonts, `--page-bg: #faf6ef`, same block colours, same CSS variable palette) as `python/index.html`.
- FR16: A **back link** to the notes page (`../index.html`) is present in the header.

### Hosting
- FR17: Fully static — HTML + CSS + vanilla JS, no build step, no external runtime dependencies beyond Google Fonts.
- FR18: Deployable to GitHub Pages as-is.

---

## Non-Functional Requirements

- NFR1: All 100 questions embedded directly in the HTML file as a JS array — no fetch/API calls needed.
- NFR2: Page must be functional on mobile (responsive layout matching the notes site breakpoint at 960px).
- NFR3: Keyboard accessible — options selectable with keyboard, submit triggerable with Enter.
- NFR4: No frameworks (React, Vue, etc.) — vanilla JS only, consistent with the rest of the site.
- NFR5: Page load under 2 s on a standard connection (fonts are the only external dependency).

---

## Acceptance Criteria

- AC1: Opening the page shows a "Start Quiz" screen with the quiz title and a start button.
- AC2: Clicking Start presents Question 1 of 5, with 4 labelled options.
- AC3: Selecting an option and clicking Submit immediately colours the options (green/red), marks the correct answer, and reveals the explanation.
- AC4: Clicking Next advances to the next question; the previous question is no longer visible.
- AC5: After Question 5, the Score Summary screen shows X/5 and a per-question breakdown.
- AC6: Clicking Retake picks a new random 5 and shows Question 1 again.
- AC7: Running the quiz multiple times, questions vary (randomisation confirmed over ≥ 3 retakes).
- AC8: The page renders correctly on a 375 px wide viewport (iPhone SE).
- AC9: The design matches the parchment aesthetic — fonts, background colour, and block styles consistent with `python/index.html`.
- AC10: The question bank contains at least 80 questions covering all 10 weeks.

---

## Edge Cases

- EC1: If the bank has fewer than 5 questions for some reason, sample all available rather than crashing.
- EC2: Fisher-Yates shuffle (or equivalent) used to ensure uniform random distribution — no bias toward early questions.
- EC3: Retake must not repeat the same 5 questions as the previous session if the bank has ≥ 10 questions.
- EC4: Options must be shuffled per question (correct answer not always in the same position).

---

## Question Bank Coverage Plan

| Week | Topic | Target questions |
|------|-------|-----------------|
| 1 | Python Foundations (act of programming, syntax/semantics, errors, features, variables, types) | 12 |
| 2 | Expressions & Anonymous Functions (operators, walrus, lambda) | 8 |
| 3 | Reasoning About Code (assignment semantics, conditionals, assertions) | 8 |
| 4 | Loops & Reasoning (while, for, range, invariants, isSorted) | 10 |
| 5 | Sorting & Lists (bubble sort, list ops) | 10 |
| 6 | Lists II & Functions (sorting, copy, functions as abstraction) | 10 |
| 7 | Function Deep Dive (defaults, mutable pitfall, return values) | 10 |
| 8 | Dictionaries | 8 |
| 9 | Recursion & BSTs (BST, recursive insert, AVL) | 12 |
| 10 | Spectral Soil Modeler project | 6 |
| **Total** | | **94** |

---

## Dependencies

- Existing `python/index.html` — design system reference
- Existing `quiz/index.html` path — already linked from notes TOC (FR14 must match this path)
- Google Fonts CDN (Playfair Display + Lora) — same as notes page
- GitHub Pages — target hosting environment
