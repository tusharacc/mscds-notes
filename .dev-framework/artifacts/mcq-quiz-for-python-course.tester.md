# Tester Artifact: mcq-quiz-for-python-course

## Test Plan
Open `python/quiz/index.html` directly in a browser (file://) or via a local server / GitHub Pages. All tests are manual UI verification unless marked otherwise.

---

## Test Cases

### TC-01 — Start screen renders correctly
**Input:** Open the page fresh.
**Expected:**
- "Python MCQ Quiz" heading visible
- Week pills for all 10 weeks displayed
- "94 questions across all 10 weeks" text visible
- "5 random questions" text visible
- "Start Quiz" button present and enabled

---

### TC-02 — Quiz starts on button click
**Input:** Click "Start Quiz".
**Expected:**
- Start screen disappears
- Question card appears showing "Question 1 of 5"
- Week badge shows a valid week number (1–10)
- Exactly 4 option buttons present, all enabled
- "Submit Answer" button present and disabled
- 5 progress dots visible; first dot filled (gold)

---

### TC-03 — Option selection enables Submit
**Input:** Click any option button.
**Expected:**
- Clicked button gets highlighted (amber/gold border)
- All other buttons lose highlight
- "Submit Answer" button becomes enabled

---

### TC-04 — Changing selection before submit
**Input:** Click option A, then click option C.
**Expected:**
- Option A loses highlight
- Option C is highlighted
- Only one option selected at a time
- Submit button remains enabled

---

### TC-05 — Correct answer feedback
**Input:** Identify the correct answer from the question bank; select it; click Submit.
**Expected:**
- Correct option turns green (`.correct-ans`)
- Result badge shows "✓ Correct"
- Explanation text appears below with amber border
- All 4 option buttons disabled (cannot re-click)
- "Submit Answer" row hidden
- "Next Question →" button appears

---

### TC-06 — Incorrect answer feedback
**Input:** Deliberately select a wrong option; click Submit.
**Expected:**
- Selected wrong option turns red (`.wrong-ans`)
- Correct option turns green regardless
- Result badge shows "✗ Incorrect"
- Explanation still shown
- "Next Question →" button appears

---

### TC-07 — Progress dots update correctly
**Input:** Answer Q1 correctly, Q2 incorrectly, then view Q3.
**Expected:**
- Q1 dot is green
- Q2 dot is red
- Q3 dot is filled gold (current)
- Q4, Q5 dots are empty (grey)

---

### TC-08 — Navigation through all 5 questions
**Input:** Answer all 5 questions one by one.
**Expected:**
- "Next Question →" label on questions 1–4
- "See Results" label on question 5
- Progress counter shows "Question N of 5" correctly for each N

---

### TC-09 — Score summary screen
**Input:** Complete all 5 questions.
**Expected:**
- Score ring shows "X/5" where X is actual correct count
- Score message matches bracket (100%, ≥80%, ≥60%, <60%)
- Per-question breakdown shows 5 rows
- Each row shows pass (green) or fail (red) with week number
- Incorrect rows show the correct answer
- "Retake Quiz" button present
- "← Back to Notes" link present

---

### TC-10 — Retake picks new questions
**Input:** Complete quiz; click "Retake Quiz"; note question 1; repeat 3 times.
**Expected:**
- Page does NOT reload (URL stays same, no flash)
- Question 1 of 5 is shown immediately after click
- Over 3 retakes, at least one session differs from the others (randomisation check)

---

### TC-11 — Back to Notes link
**Input:** On summary screen, click "← Back to Notes".
**Expected:**
- Navigates to `../index.html` (the notes page)

---

### TC-12 — Question bank coverage
**Input:** Inspect source; count `week:` occurrences by value.
**Expected:**
- Total questions: 94
- Week 1: 12, Week 2: 8, Week 3: 8, Week 4: 10, Week 5: 10
- Week 6: 10, Week 7: 10, Week 8: 8, Week 9: 12, Week 10: 6

---

### TC-13 — Option shuffling
**Input:** Note the position of the correct answer for a known question across 3 sessions.
**Expected:**
- Correct answer appears in different positions (A/B/C/D) across multiple sessions

---

### TC-14 — Mobile layout at 375px
**Input:** Set browser viewport to 375px wide; open page.
**Expected:**
- No horizontal scrollbar on main content
- Option buttons stack vertically and are fully readable
- Submit button full width (hint text hidden per CSS)
- Score ring and summary readable without overflow

---

### TC-15 — Keyboard accessibility
**Input:** Tab through the page without using mouse.
**Expected:**
- "Start Quiz" button reachable and activatable with Enter/Space
- Option buttons reachable with Tab; selectable with Enter/Space
- Submit button reachable after option selected; activatable with Enter
- "Next Question" / "See Results" reachable and activatable
- Focus outline visible on all interactive elements

---

### TC-16 — No Submit without selection
**Input:** Load question; do NOT select any option; attempt to click Submit.
**Expected:**
- Submit button is disabled — cannot be clicked
- No answer is recorded; question stays in pre-answer state

---

### TC-17 — Design consistency
**Input:** Open notes page (`python/index.html`) side by side with quiz page.
**Expected:**
- Same font family (Playfair Display headings, Lora body)
- Same background colour (#faf6ef parchment)
- Amber/gold accent colour consistent
- Overall visual language matches

---

### TC-18 — Edge case: bank smaller than session size (code review)
**Input:** Inspect `pickSession` function in source.
**Expected:**
- `Math.min(n, shuffled.length)` used — function safely handles bank < 5 without error (EC1)
