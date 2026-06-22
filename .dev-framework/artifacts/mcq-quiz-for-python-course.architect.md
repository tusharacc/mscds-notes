# Architect Artifact: mcq-quiz-for-python-course

## System Design

Single-file delivery: everything — HTML, CSS, JS, and the full 94-question bank — lives in `python/quiz/index.html`. No build step, no imports, no fetch calls.

**State machine (client-side JS):**
```
START → QUESTION(n) → ANSWERED(n) → QUESTION(n+1) → ... → SUMMARY → START
```

State values:
- `bank[]` — full question array (loaded at parse time)
- `session[]` — 5 shuffled questions for this attempt
- `current` — index 0–4 into session
- `answers[]` — user's picks per question
- `screen` — `'start' | 'question' | 'answered' | 'summary'`

## Components

| Component | Implementation |
|-----------|---------------|
| Question bank | `const QUESTIONS = [...]` — plain JS array at top of `<script>` block |
| Shuffler | Fisher-Yates on bank to pick 5; Fisher-Yates on each question's options array |
| Quiz engine | ~80 lines of vanilla JS — startQuiz(), renderQuestion(), submitAnswer(), nextQuestion(), showSummary(), retake() |
| Renderer | DOM manipulation only — single `#quiz-root` div swapped via innerHTML |
| Screens | Four HTML templates as JS template literals: Start, Question, Answered, Summary |

## Data Models

Each question object:
```js
{
  week: 3,
  q: "What does `x := 5` do?",        // may contain <code> tags
  options: [                            // always 4 items
    "Assigns 5 to x and evaluates to 5",
    "Raises a SyntaxError",
    "Assigns 5 to x but evaluates to None",
    "Creates an immutable binding"
  ],
  answer: "Assigns 5 to x and evaluates to 5",  // matches one option by value
  explanation: "The walrus operator := is an expression..."
}
```

Correct answer stored by value (not index) so option shuffling never breaks it.

## API Contracts

None — fully static, no network calls after initial page load.

## Tech Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Framework | None — vanilla JS | Consistent with notes site; no build tooling |
| Styling | Inline `<style>` reusing notes CSS variables | Single-file; design consistency |
| Question storage | JS array in `<script>` | Avoids fetch/CORS on GitHub Pages |
| Option shuffling | Fisher-Yates per question at session-start | Correct answer not always in same position |
| Correct answer tracking | By value string match | Survives option shuffle |
| Fonts | Same Google Fonts CDN as notes page | Visual consistency |
| Progress indicator | "Question N of 5" + filled dots | No library needed |

## File Layout

```
python/
  quiz/
    index.html   ← single deliverable
```

## Open Questions

None — all requirements fully specified in PO artifact.
