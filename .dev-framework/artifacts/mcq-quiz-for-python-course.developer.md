# Developer Artifact: mcq-quiz-for-python-course

## Implementation Plan
Single HTML file at `python/quiz/index.html`. All CSS, JS, and question bank embedded inline.
State machine: START → QUESTION(n) → ANSWERED(n) → SUMMARY → START.
Fisher-Yates shuffle picks 5 random questions per session; options shuffled per question; correct answer tracked by value string.

## Files Changed
- `python/quiz/index.html` — created (1734 lines)

## Code Summary
- `QUESTIONS[]` — 94 questions as JS objects {week, q, options[4], answer, explanation}
- `shuffle(arr)` — Fisher-Yates implementation
- `pickSession(bank, n)` — picks n random questions, shuffles each question's options
- `renderStart()` — start screen with week pills and Start button
- `renderQuestion()` — renders current question with progress dots, week badge, options
- `submitAnswer(idx)` — reveals correct/wrong state, shows explanation, wires Next button
- `renderSummary()` — score ring, per-question breakdown, Retake + Back to Notes buttons
- `startQuiz()` — entry point, resets state, calls renderQuestion()

## Decisions Made
- Correct answer tracked by value string (not index) — survives option shuffling
- `innerHTML` used only for fixed question bank strings, never user input — XSS-safe
- Options disabled after submission to prevent re-selection
- Score message varies by percentage bracket (100%, ≥80%, ≥60%, <60%)
- Strip HTML tags in summary breakdown to show plain text question preview
