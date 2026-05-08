
# Probability Notes — Improvement Pack With Representative Problems

This addendum is meant to be inserted into the probability notes after the core definitions.  
It keeps only a few carefully chosen problems, but each one covers a major concept and is solved using more than one technique.

---

# 1. How to Use These Problems

Before solving any probability problem, follow this checklist:

1. Define the events.
2. Decide whether outcomes are ordered or unordered.
3. Check whether the question is conditional.
4. Decide whether a tree, table, counting formula, or Bayes' theorem is most natural.
5. Only then start algebra.

---

# 2. Problem A — Conditional Probability: Lunch Box Problem

## Problem

Two lunch boxes are sent through two friends separately.  
Each friend independently loses the lunch box with probability \(0.2\).

Given that a lunch box is lost, what is the probability that it was lost only by the second friend?

---

## Events

Let:

\[
F_1 = \text{first friend loses the box}
\]

\[
F_2 = \text{second friend loses the box}
\]

We need:

\[
P(F_2 \cap F_1^c \mid F_1 \cup F_2)
\]

The condition is:

\[
F_1 \cup F_2
\]

meaning at least one lunch box was lost.

---

## Technique 1 — Conditional Probability Formula

\[
P(F_2 \cap F_1^c \mid F_1 \cup F_2)
=
\frac{P(F_2 \cap F_1^c)}{P(F_1 \cup F_2)}
\]

First compute numerator:

\[
P(F_2 \cap F_1^c)
=
P(F_2)P(F_1^c)
=
0.2 \times 0.8
=
0.16
\]

Now compute denominator:

\[
P(F_1 \cup F_2)
=
1-P(F_1^c \cap F_2^c)
\]

\[
=
1-(0.8)(0.8)
=
1-0.64
=
0.36
\]

Therefore:

\[
P(F_2 \cap F_1^c \mid F_1 \cup F_2)
=
\frac{0.16}{0.36}
=
\frac{4}{9}
\]

---

## Technique 2 — Reduced Sample Space Table

| First Friend | Second Friend | Probability | Included after condition? |
|---|---|---:|---|
| Not lost | Not lost | \(0.8 \cdot 0.8 = 0.64\) | No |
| Lost | Not lost | \(0.2 \cdot 0.8 = 0.16\) | Yes |
| Not lost | Lost | \(0.8 \cdot 0.2 = 0.16\) | Yes |
| Lost | Lost | \(0.2 \cdot 0.2 = 0.04\) | Yes |

After conditioning on “a box is lost,” remove the first row.

Reduced probability mass:

\[
0.16+0.16+0.04=0.36
\]

Desired row:

\[
0.16
\]

So:

\[
\frac{0.16}{0.36}=\frac{4}{9}
\]

---

## Learning Point

Do not answer \(0.2\).  
That is the probability the second friend loses the box before receiving any information.

After hearing that at least one box was lost, the sample space changes.

---

# 3. Problem B — Bayes and Population Weighting: Defective Bolts

## Problem

Machines A, B, and C manufacture 25%, 35%, and 40% of bolts respectively.

Their defective rates are:

\[
P(D\mid A)=0.05,\quad P(D\mid B)=0.04,\quad P(D\mid C)=0.02
\]

A bolt is chosen randomly and found defective.  
What is the probability that it was manufactured by A or C?

---

## Events

Let:

\[
D = \text{bolt is defective}
\]

We need:

\[
P(A \cup C \mid D)
\]

Since a bolt can come from only one machine:

\[
P(A \cup C \mid D)=P(A\mid D)+P(C\mid D)
\]

---

## Technique 1 — Bayes' Theorem

\[
P(A \cup C \mid D)
=
\frac{P((A\cup C)\cap D)}{P(D)}
\]

The numerator is:

\[
P(A\cap D)+P(C\cap D)
\]

\[
=
P(D\mid A)P(A)+P(D\mid C)P(C)
\]

\[
=
0.05(0.25)+0.02(0.40)
\]

\[
=
0.0125+0.008
=
0.0205
\]

Now compute denominator using total probability:

\[
P(D)=P(D\mid A)P(A)+P(D\mid B)P(B)+P(D\mid C)P(C)
\]

\[
=
0.05(0.25)+0.04(0.35)+0.02(0.40)
\]

\[
=
0.0125+0.014+0.008
=
0.0345
\]

Therefore:

\[
P(A\cup C\mid D)
=
\frac{0.0205}{0.0345}
=
\frac{41}{69}
\]

---

## Technique 2 — Convert Percentages to Counts

Assume 10,000 bolts.

| Machine | Production Share | Number of Bolts | Defect Rate | Defective Bolts |
|---|---:|---:|---:|---:|
| A | 25% | 2500 | 5% | 125 |
| B | 35% | 3500 | 4% | 140 |
| C | 40% | 4000 | 2% | 80 |

Total defective bolts:

\[
125+140+80=345
\]

Defective bolts from A or C:

\[
125+80=205
\]

So:

\[
P(A\cup C\mid D)
=
\frac{205}{345}
=
\frac{41}{69}
\]

---

## Learning Point

You cannot add \(5\%+4\%+2\%\).  
Those are conditional defect rates, not shares of the total output.

Always weight conditional rates by population size.

---

# 4. Problem C — Law of Total Probability: Box Selection Problem

## Problem

Box I contains:

\[
6R,\ 4B,\ 3G
\]

If the ball from Box I is red, choose from Box II.  
If blue, choose from Box III.  
If green, choose from Box IV.

Box III contains:

\[
1B,\ 3G,\ 2W
\]

Box IV contains:

\[
10G,\ 10O,\ 4W
\]

Find the probability of seeing a white ball.

---

## Events

White can happen only through two paths:

\[
B \text{ from Box I} \rightarrow W \text{ from Box III}
\]

or

\[
G \text{ from Box I} \rightarrow W \text{ from Box IV}
\]

---

## Technique 1 — Tree / Path Method

Box I total:

\[
6+4+3=13
\]

Probability of blue from Box I:

\[
P(B)=\frac{4}{13}
\]

Probability of white from Box III:

\[
P(W\mid B)=\frac{2}{6}=\frac{1}{3}
\]

First path:

\[
P(B\cap W)=\frac{4}{13}\cdot\frac{1}{3}
=
\frac{4}{39}
\]

Probability of green from Box I:

\[
P(G)=\frac{3}{13}
\]

Probability of white from Box IV:

\[
P(W\mid G)=\frac{4}{24}=\frac{1}{6}
\]

Second path:

\[
P(G\cap W)=\frac{3}{13}\cdot\frac{1}{6}
=
\frac{3}{78}
\]

Total:

\[
P(W)=\frac{4}{39}+\frac{3}{78}
\]

\[
=
\frac{8}{78}+\frac{3}{78}
=
\frac{11}{78}
\]

---

## Technique 2 — Law of Total Probability

Let the first ball from Box I determine the partition:

\[
R,\ B,\ G
\]

Then:

\[
P(W)=P(W\mid R)P(R)+P(W\mid B)P(B)+P(W\mid G)P(G)
\]

Since Box II has no white ball in this problem:

\[
P(W\mid R)=0
\]

Therefore:

\[
P(W)=0\cdot\frac{6}{13}
+
\frac{2}{6}\cdot\frac{4}{13}
+
\frac{4}{24}\cdot\frac{3}{13}
\]

\[
=
0+\frac{4}{39}+\frac{3}{78}
=
\frac{11}{78}
\]

---

## Learning Point

When an event can happen through multiple branches, compute every valid path and add them.

---

# 5. Problem D — Bayes With Tree: Rain, Traffic, and Being Late

## Problem

It rains every third day:

\[
P(R)=\frac{1}{3}
\]

On a rainy day, heavy traffic occurs with probability \(0.5\).  
On a non-rainy day, heavy traffic occurs with probability \(0.25\).

Late probabilities:

- Rainy and traffic: \(0.5\)
- Rainy and no traffic: \(0.25\)
- Not rainy and traffic: \(0.25\)
- Not rainy and no traffic: \(0.125\)

Given that you arrived late, what is the probability it rained?

---

## Events

Let:

\[
R = \text{rain}
\]

\[
L = \text{late}
\]

We need:

\[
P(R\mid L)
\]

---

## Technique 1 — Tree Method

First compute:

\[
P(L\mid R)
\]

On rainy days:

\[
P(L\mid R)=0.5(0.5)+0.5(0.25)
\]

\[
=
0.25+0.125
=
0.375
=
\frac{3}{8}
\]

So:

\[
P(R\cap L)=P(R)P(L\mid R)
=
\frac{1}{3}\cdot\frac{3}{8}
=
\frac{1}{8}
\]

Now compute:

\[
P(L\mid R^c)
\]

On non-rainy days:

\[
P(L\mid R^c)=0.25(0.25)+0.75(0.125)
\]

\[
=
0.0625+0.09375
=
0.15625
=
\frac{5}{32}
\]

So:

\[
P(R^c\cap L)=P(R^c)P(L\mid R^c)
=
\frac{2}{3}\cdot\frac{5}{32}
=
\frac{5}{48}
\]

Total probability of being late:

\[
P(L)=\frac{1}{8}+\frac{5}{48}
=
\frac{6}{48}+\frac{5}{48}
=
\frac{11}{48}
\]

Now apply Bayes:

\[
P(R\mid L)=\frac{P(R\cap L)}{P(L)}
\]

\[
=
\frac{\frac{1}{8}}{\frac{11}{48}}
=
\frac{1}{8}\cdot\frac{48}{11}
=
\frac{6}{11}
\]

---

## Technique 2 — Bayes Formula Directly

\[
P(R\mid L)=\frac{P(L\mid R)P(R)}
{P(L\mid R)P(R)+P(L\mid R^c)P(R^c)}
\]

Substitute:

\[
P(R\mid L)=
\frac{\frac{3}{8}\cdot\frac{1}{3}}
{\frac{3}{8}\cdot\frac{1}{3}+\frac{5}{32}\cdot\frac{2}{3}}
\]

\[
=
\frac{\frac{1}{8}}
{\frac{1}{8}+\frac{5}{48}}
=
\frac{6}{11}
\]

---

## Learning Point

Bayes' theorem is often just a compact way of summing paths in a tree.

---

# 6. Problem E — Ordered vs Unordered: Birthday Problem

## Problem

There are 365 days in a year.  
How many possible birthday sequences are there for 30 people?

---

## Technique 1 — Multiplication Principle

Each person has 365 choices.

Since there are 30 people:

\[
365\cdot365\cdots365
\]

30 times:

\[
365^{30}
\]

---

## Why This Is Ordered

The birthday assignment:

\[
(\text{Jan 1}, \text{Feb 2})
\]

is different from:

\[
(\text{Feb 2}, \text{Jan 1})
\]

because Person 1 and Person 2 swapped birthdays.

Therefore birthdays of people form a sequence, not a set.

---

## Extension — No Repeated Birthdays

Number of birthday sequences with no repeated birthdays:

\[
365\cdot364\cdot363\cdots336
\]

There are 30 factors.

Equivalently:

\[
P(365,30)=\frac{365!}{335!}
\]

Probability of no repeated birthdays:

\[
\frac{365\cdot364\cdot363\cdots336}{365^{30}}
\]

To avoid overflow, compute as:

\[
1\cdot\frac{364}{365}\cdot\frac{363}{365}\cdots\frac{336}{365}
\]

---

## Learning Point

The word “sequence” means order matters.

---

# 7. Problem F — Ordered vs Unordered: Dice vs Cards

## Dice Example

For two dice:

\[
(1,4)\neq(4,1)
\]

because die 1 and die 2 are distinguishable.

So the sample space has:

\[
6\cdot6=36
\]

outcomes.

---

## Card Hand Example

For a 5-card poker hand, order does not matter.

The hand:

\[
\{A,K,Q,J,10\}
\]

is the same no matter the order in which cards are dealt.

So total poker hands:

\[
\binom{52}{5}
\]

---

## Four of a Kind

In poker, “four of a kind” means four cards of the same rank, not same suit.

Example:

\[
7\spadesuit,\ 7\heartsuit,\ 7\diamondsuit,\ 7\clubsuit
\]

There are 13 possible ranks.

Once the rank is chosen, the four cards are forced.

The fifth card can be any of the remaining 48 cards.

So favorable hands:

\[
13\cdot48
\]

Probability:

\[
\frac{13\cdot48}{\binom{52}{5}}
\]

---

## Learning Point

Always ask:

> Am I counting arrangements, or am I counting collections?

---

# 8. Problem G — Inclusion-Exclusion and Independence

## Problem

Let three events \(A,B,C\) satisfy:

- \(A\) and \(C\) are independent.
- \(B\) and \(C\) are independent.
- \(A\cap B=\varnothing\)
- \(P(A\cup C)=\frac{2}{3}\)
- \(P(B\cup C)=\frac{3}{4}\)
- \(P(A\cup B\cup C)=\frac{11}{12}\)

Find:

\[
P(A),\ P(B),\ P(C)
\]

---

## Technique 1 — Inclusion-Exclusion

The formula is:

\[
P(A\cup B\cup C)
=
P(A)+P(B)+P(C)
-
P(A\cap B)
-
P(A\cap C)
-
P(B\cap C)
+
P(A\cap B\cap C)
\]

Since:

\[
A\cap B=\varnothing
\]

we also have:

\[
A\cap B\cap C=\varnothing
\]

So:

\[
P(A\cap B)=0
\]

\[
P(A\cap B\cap C)=0
\]

Because \(A\) and \(C\) are independent:

\[
P(A\cap C)=P(A)P(C)
\]

Because \(B\) and \(C\) are independent:

\[
P(B\cap C)=P(B)P(C)
\]

So:

\[
P(A\cup B\cup C)
=
P(A)+P(B)+P(C)-P(A)P(C)-P(B)P(C)
\]

---

## Technique 2 — Test Options Efficiently

Suppose one option is:

\[
P(A)=\frac{1}{3},\quad P(B)=\frac{1}{2},\quad P(C)=\frac{1}{2}
\]

Check:

\[
P(A\cup C)=P(A)+P(C)-P(A)P(C)
\]

\[
=
\frac{1}{3}+\frac{1}{2}-\frac{1}{6}
=
\frac{2}{3}
\]

Correct.

Now:

\[
P(B\cup C)=\frac{1}{2}+\frac{1}{2}-\frac{1}{4}
=
\frac{3}{4}
\]

Correct.

Finally:

\[
P(A\cup B\cup C)
=
\frac{1}{3}+\frac{1}{2}+\frac{1}{2}
-
\frac{1}{6}
-
\frac{1}{4}
\]

\[
=
\frac{11}{12}
\]

Correct.

Therefore:

\[
\boxed{
P(A)=\frac{1}{3},\quad P(B)=\frac{1}{2},\quad P(C)=\frac{1}{2}
}
\]

---

## Learning Point

If \(A\cap B=\varnothing\), then:

\[
A\cap B\cap C=\varnothing
\]

because triple intersection is contained inside \(A\cap B\).

---

# 9. Final Summary of Techniques

| Technique | Best Used When |
|---|---|
| Direct counting | Equally likely outcomes |
| Permutations | Ordered selections |
| Combinations | Unordered selections |
| Tree method | Sequential conditional processes |
| Law of total probability | Multiple routes to same event |
| Bayes theorem | Given evidence, infer cause |
| Inclusion-exclusion | Union of overlapping events |
| Frequency table | Percentages and population weights |
| Complement method | “At least one” or “no repeat” problems |

---

# 10. Personal Study Advice

Your current strength is that you try to understand why a formula works.

Keep doing that.

For each problem, write:

1. What is the sample space?
2. What is the event?
3. Is order important?
4. Is this conditional?
5. Which method best matches the structure?

This will build durable intuition instead of formula memorization.
