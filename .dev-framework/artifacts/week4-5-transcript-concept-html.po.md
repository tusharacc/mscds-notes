# PO Requirements: week4-5-transcript-concept-html

## Problem Statement

The user has Whisper-generated transcripts for 8 lecture videos across two weeks of an MScDS probability course at IIIT Hyderabad. They need a single, condensed HTML reference document that captures every concept and example from these transcripts — even concepts discussed briefly — validated against web knowledge, with full derivation steps and professional math rendering. The document is for personal revision/study.

## Source Files

**Week 4** (`week4_transcripts/`):
- `video1_intro_prob3.txt` — Equally likely outcomes, combinatorial probability, N-ball K-pick, card problems
- `video2_cond_prob1.txt` — Monty Hall problem, independence axiom, intro to conditional probability
- `video3_cond_prob2.txt` — Conditional probability examples (coins, dice, balls), law of total probability, Bayes rule derivation, Monty Hall via Bayes
- `video4_bayes_examples.txt` — Bayes theorem applied: student exam, medical diagnostic test, police inspector/suspect

**Week 5** (`week5_transcripts/`):
- `w5_video1_bayes_examples2.txt` — Generalized Bayes (multiple partitions), chain rule, independence of events, weighted sampling
- `w5_video2_random_variables.txt` — Random variables, PMF, expectation, examples (20-ball, dice, coin tosses)
- `w5_video3_rv_linearity.txt` — Linearity of expectation, Bernoulli RVs, random graphs (edges + triangles), hat-check problem, stock price RV
- `w5_video4_linearity_contd.txt` — Screw pack problem, Markov inequality, tail inequalities, binomial behavior

## User Stories

- As a student, I want a single HTML file so I can open it in any browser without dependencies beyond MathJax CDN.
- As a student, I want every concept captured (no matter how briefly mentioned) so I can use this as a complete revision sheet.
- As a student, I want full derivation steps for examples so I can follow the logic, not just the final answer.
- As a student, I want concepts from the two Bayes theorem videos merged into one section so related content is co-located.
- As a student, I want color-coded sections by concept category so I can visually distinguish definitions, axioms, examples, and theorems.

## Functional Requirements

1. **Single HTML output file** at `week4_week5_probability_notes.html` in the project root.
2. **MathJax rendering** via CDN for all mathematical expressions (inline `\(...\)` and display `\[...\]`).
3. **Concept sections** (subsections, not one-per-video):
   - Classical Probability & Equally Likely Outcomes
   - Combinatorial Probability (N-ball/K-pick, card problems)
   - Sample Space Construction (enumeration, tree method)
   - Conditional Probability (definition, formula, examples)
   - Law of Total Probability
   - Bayes' Theorem (merged from video4 + w5_video1)
   - Chain Rule (Multiplication Rule)
   - Independence of Events
   - Weighted / Non-Uniform Sampling
   - Random Variables (definition, types, range)
   - Probability Mass Function (PMF)
   - Expectation
   - Linearity of Expectation
   - Special Distributions (Bernoulli, Binomial, Geometric)
   - Markov Inequality & Tail Inequalities
4. **Every example** from all 8 transcripts included with:
   - Problem statement
   - Full step-by-step derivation
   - Final result highlighted
5. **Every axiom** explicitly labeled, including: equally likely probability, independence and product, conditional probability, monotonicity (E ⊆ F → P(E) ≤ P(F)), linearity of expectation, Markov inequality.
6. **Concept validation**: each concept description validated/enriched using knowledge and web search — no factual errors.
7. **Color coding by category**:
   - Definitions → one color (e.g., blue-tinted)
   - Axioms / Theorems → another (e.g., amber/orange)
   - Worked Examples → another (e.g., green-tinted)
   - Key Results / Formulas → another (e.g., purple/violet)
   - Homework/exercises mentioned → grey
8. **Navigation**: sticky table of contents or anchor links for all sections.

## Non-Functional Requirements

- Self-contained: only external dependency is MathJax CDN.
- Readable offline once loaded (MathJax cached by browser).
- Clean, modern styling — not a raw dump of text.
- Must render correctly in Chrome/Safari/Firefox.

## Acceptance Criteria

- [ ] All 8 transcript files fully processed; no concept omitted.
- [ ] Bayes theorem content from video4 and w5_video1 appears in a single merged section.
- [ ] All mathematical formulas render via MathJax (not plain text).
- [ ] Full derivation shown for: N-ball K-pick, Monty Hall (both tree and Bayes approaches), student exam, medical test, police inspector, red/white ball chain rule, linearity of expectation (binomial E[X]=kp), Markov inequality.
- [ ] Color coding visually distinguishes all four categories.
- [ ] Table of contents with anchor links to each section.
- [ ] File opens standalone in a browser.

## Concept Inventory (complete list — nothing may be omitted)

**Week 4:**
- Equally likely outcomes formula P(E) = |E|/|S|
- Coin toss probability and fair coin assumption
- N balls K picks: P(special ball picked) = K/N (two derivations: first principles + combinatorial)
- 52-card deck: P(3 red and 3 black from 6 picks) (two derivations)
- Sample space as vectors (maintaining position integrity)
- Tree method for sample space construction
- Monty Hall problem (full sample space enumeration, probability assignment, switching wins with P=2/3)
- Axiom of independence and product
- Conditional probability definition: P(E|F) = P(E∩F)/P(F)
- Two-coin example with conditioning
- Two-dice example: P(one die odd | sum even)
- Red/blue ball without replacement: P(first ball blue | k of N are blue) = k/N
- Law of total probability: P(E) = P(E|A)P(A) + P(E|Aᶜ)P(Aᶜ)
- Bayes' rule: P(F|E) = P(E|F)P(F) / P(E)
- Full Bayes formula (expanded denominator)
- Monty Hall re-derived using Bayes' rule
- Axiom: E ⊆ F → P(E) ≤ P(F)
- Bayes example 1: Student knows answer (result: mp/(p(m-1)+1))
- Bayes example 2: Medical diagnostic test (95% accurate, 0.5% prevalence, false positive 1%) → P(D|positive) ≈ 95/294
- Bayes example 3: Police inspector (60% prior guilty, left-handed evidence, 20% base rate) → P(guilty|left-handed) ≥ 60/68

**Week 5:**
- Generalized Bayes with k-partition: P(E) = Σ P(E|Fᵢ)P(Fᵢ)
- Chain rule: P(E1∩E2∩...∩En) product form
- Independence: P(E|F)=P(E), generalized mutual independence
- Bag with 8 red + 4 white balls, P(first 2 red) = 14/33 (chain rule)
- P(first 2 red, 3rd white) = 28/165 (chain rule extended)
- Weighted sampling: balls with weights R and W, non-uniform probabilities
- Random variable definition (function from Ω to ℝ)
- Indicator random variables
- Geometric RV (tosses until first heads, range = ℕ)
- PMF definition and normalization property
- 20-ball problem: P(highest = k) = C(k-1,2)/C(20,3)
- Expectation: E[X] = Σ v·P(X=v)
- E[X] for dice = 3.5 (expected value need not be in range)
- E[X] for 2 coin tosses (number of heads) = 1
- Exam with two sequential questions (conditional structure): PMF and expected marks
- Binomial distribution: k experiments, P(X=i) = C(k,i)pⁱ(1-p)^(k-i), sum=1 via binomial theorem
- Expected number of trials to first heads (geometric): E[X] = 1/p
- Linearity of expectation: E[ΣXᵢ] = ΣE[Xᵢ] regardless of dependence
- Bernoulli RV definition
- E[X] for binomial via linearity = kp
- Heterogeneous Bernoulli: E[X] = Σpᵢ
- Expected number of edges in random graph = C(n,2)·½
- Expected number of triangles in random graph = C(n,3)·⅛ (and generalization to p)
- Hat-check (derangement-like) problem: expected # picking own name = 1
- Stock price random variable: E[X_d] = (pr + (1-p)/r)^d × 100
- Screw pack problem: P(return) ≈ 0.004, expected returns from 1M packs ≈ 4000
- Markov inequality: P(X ≥ a) ≤ E[X]/a
- Application of Markov: P(X > (1+ε)E[X]) ≤ 1/(1+ε)
- Coin tosses: P(#heads > 3k/4) ≤ 2/3
- Tail inequalities concept (preview of future content)
- Binomial distribution peaks near k/2 (intuition)

## Edge Cases

- Concepts mentioned only in passing (e.g., "tail inequalities are covered in future sessions") should still be noted with a brief definition and a "preview" label.
- Exercises/homework problems mentioned in lectures should be listed in a grey-styled "Practice Problems" callout within the relevant section.
- When two approaches derive the same result (e.g., N-ball K-pick via first principles and combinatorial formula), both must be shown.

## Dependencies

- MathJax 3.x CDN (internet required for first load)
- Source transcripts in `week4_transcripts/` and `week5_transcripts/`
- Output: `week4_week5_probability_notes.html` at project root
