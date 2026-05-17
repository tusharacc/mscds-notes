# Dev Framework Checkpoint
**Date**: 2026-05-17
**Workspace**: (none)
**Phase**: —
**Branch**: main
**Workflow**: —

## Done this session
- feat(discrete-maths): add Week 6 — Variance, Distributions, and Matrices
  - §18 Variance (definition, E[X²]−μ² formula, dice example, moments)
  - §19 Bernoulli & Binomial variance + casino dice game worked example
  - §20 Poisson distribution
  - §21 Geometric distribution — tail-probability derivation, tail-sum expectation proof, ball-urn example
  - §22 Negative Binomial distribution
  - §23 Hypergeometric distribution & variance additivity for independent RVs
  - §24 Vectors (arrays, addition, scalar multiplication, inner product)
  - §25 Matrices (addition, multiplication as inner products, dimension rule, non-commutativity, associativity, operation count)
  - New TOC groups (Week 6a · Variance & Distributions, Week 6b · Linear Algebra)
  - New banner CSS for data-week="6a" (green) and data-week="6b" (amber)
- Staged transcript folders: discrete_mathematics/week6/ and python/week5/

## Where things stand
No active dev-framework workspace. Work done directly on main.

**discrete_mathematics/index.html** now covers:
  - Weeks 4–5 (§1–§17): Classical probability, conditional probability, Bayes, RVs, expectation, Markov, problem-solving framework
  - Week 6a (§18–§23): Variance, Bernoulli/Binomial/Poisson/Geometric/Negative Binomial/Hypergeometric, variance additivity
  - Week 6b (§24–§25): Vectors, matrices and operations

**python/index.html** covers Weeks 4–5 (§1–§13) and is complete for available transcripts:
  - While/for loops, range(), loop invariants, isSorted
  - Bubble sort (one pass, naive, optimised with early termination), loop invariant assertions
  - Python lists: creation, access, slicing, append/insert/extend, concatenation, repetition, remove/pop/clear, count/index/in

## Pending decisions
- [ ] Python: list sorting, reversing, and copying (slice-copy pitfall) are covered in the
      next lecture after 5.2.1 — add when that transcript arrives
- [ ] Python week5/ folder contains .mp4 files but no transcript subfolders for the videos
      themselves — only the transcripts/ subfolder with .txt files is staged

## Next action
When new transcripts arrive (Python Week 6, Discrete Maths Week 7+):
run `/dev new-feature` to open a workspace, read transcripts, and extend the
relevant subject's index.html with new sections.
