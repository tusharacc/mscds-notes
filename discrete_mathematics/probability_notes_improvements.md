
# Probability Notes — Structural Improvements & Thinking Framework

These sections are designed to improve:
- problem solving intuition
- event construction
- reasoning discipline

---

# 1. Conditioning Changes the Universe

For conditional probability:

P(E | F)

the event F becomes the new universe.

Instead of asking:

“How likely is E overall?”

we ask:

“Among only the outcomes where F happened, how many also satisfy E?”

## Mental Model

- Before conditioning → entire sample space
- After conditioning → only outcomes inside F

## Example — Lunch Box Problem

Suppose:
- Friend 1 loses with probability 0.2
- Friend 2 loses with probability 0.2

Let:
- L = “At least one lunch box lost”
- F2 = “Second friend lost the lunch box”

The required probability is:

P(F2 ∩ F1^c | L)

NOT simply:

P(F2)=0.2

because conditioning changes the universe.

---

# 2. Ordered vs Unordered Counting

## Ordered Outcomes

Outcomes are different if position changes.

Example:

(1,4) ≠ (4,1)

Use ordered counting for:
- dice rolls
- coin toss sequences
- passwords
- birthdays in sequence
- permutations

---

## Unordered Outcomes

Outcomes are identical if they contain the same objects.

Use unordered counting for:
- poker hands
- committees
- lottery selections
- card subsets
- combinations

---

## Before Counting, Ask

1. Does order matter?
2. Am I counting sequences or subsets?
3. Can two outcomes differ only by rearrangement?

If order matters → permutations.

If order does not matter → combinations.

---

# 3. Population Weighting in Bayes Problems

Suppose:
- Machine A produces 25% of bolts with 5% defect rate.
- Machine B produces 35% of bolts with 4% defect rate.
- Machine C produces 40% of bolts with 2% defect rate.

The defect contribution is NOT determined only by:

P(D | A)

but by:

P(D ∩ A)=P(D|A)P(A)

because population size matters.

---

# 4. Tree Rule — Sequential Probability

In a probability tree:
- Each edge has a conditional probability.
- A complete outcome corresponds to a root-to-leaf path.

The probability of a path is:

P(path) = product of edge probabilities

If an event can happen through multiple paths:

P(E)=sum of valid path probabilities

---

# 5. Mutually Exclusive vs Independent

## Mutually Exclusive Events

Events cannot happen together.

A ∩ B = ∅

---

## Independent Events

Occurrence of one event does not change probability of the other.

P(A ∩ B)=P(A)P(B)

---

## Important Observation

Mutually exclusive events are usually NOT independent.

---

# 6. Probability Problem Solving Framework

## Five-Step Strategy

1. Define events clearly.
2. Identify whether order matters.
3. Determine if conditioning exists.
4. Construct sample space or tree.
5. Only then apply formulas.

---

# 7. Common Intuition Traps

## Conditioning Trap

Students often compute P(A)
when the problem asks for P(A|B).

---

## Order vs Combination Trap

Many counting mistakes occur because ordered outcomes are treated as unordered.

---

## Ignoring Population Weights

A larger group with smaller defect rate may still contribute more defective items overall.

---

## Using Formulas Too Early

Probability formulas are compressed summaries of reasoning.

First:
1. Define events
2. Construct sample space
3. Identify dependencies
4. Then apply formulas
