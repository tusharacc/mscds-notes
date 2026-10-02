# Week 3: Computer Arithmetic - Number Systems and Operations

## Table of Contents
1. [Number Representation](#number-representation)
2. [ASCII vs Binary](#ascii-vs-binary)
3. [Two's Complement](#twos-complement)
4. [Signed and Unsigned Numbers](#signed-and-unsigned-numbers)
5. [Sign Extension](#sign-extension)
6. [Alternative Representations](#alternative-representations)
7. [Addition and Subtraction](#addition-and-subtraction)
8. [Multiplication](#multiplication)
9. [Division](#division)

---

## Number Representation

### Binary Number System

Computers understand only 0s and 1s, using the **binary number system**. A 32-bit number has:
- **Most Significant Bit (MSB)**: Leftmost bit
- **Least Significant Bit (LSB)**: Rightmost bit

### Converting Binary to Decimal

Each bit has a position value represented as powers of 2:

```
Value = (bit₀ × 2⁰) + (bit₁ × 2¹) + (bit₂ × 2²) + ... + (bit₃₁ × 2³¹)
```

**Example**: For a 32-bit word
- Range: 0 to 2³² - 1
- Total numbers representable: 2³² numbers

---

## ASCII vs Binary

### Storage Efficiency Comparison

**Example**: Representing 1 billion (10⁹)

**ASCII Representation**:
- Each digit requires 8 bits (1 byte)
- 10 digits total
- **Total storage**: 80 bits

**Binary Representation**:
- 1 billion ≈ 10³ × 10³ × 10³ ≈ 2¹⁰ × 2¹⁰ × 2¹⁰ = 2³⁰
- **Total storage**: 30 bits

**Conclusion**: Binary is much more storage-efficient than ASCII for numeric representation.

---

## Two's Complement

### Unsigned Representation

With 32 bits, we can represent:
- Range: 0 to 2³² - 1
- All numbers are positive

### Signed Representation (Two's Complement)

To represent both positive and negative numbers:
- **MSB = 0**: Positive number
- **MSB = 1**: Negative number

**Range Division**:
- Positive numbers: 0 to 2³¹ - 1 (2³¹ values including 0)
- Negative numbers: -2³¹ to -1 (2³¹ values)

### Mathematical Model

```
Value = (x₀ × 2⁰) + (x₁ × 2¹) + ... + (x₃₀ × 2³⁰) + (x₃₁ × -2³¹)
```

The MSB has a negative weight of -2³¹.

### Computing Negative Values

To find -x from x:

**Method 1**: Invert and Add 1
```
1. Invert all bits (x̄)
2. Add 1 to the result
Result: -x = x̄ + 1
```

**Mathematical Proof**:
```
x + x̄ = -1 (all 1s in binary)
x̄ = -1 - x
x̄ + 1 = -x
```

**Example**: Finding -3
```
x = 3:     0000...0011
x̄:         1111...1100
x̄ + 1:     1111...1101 (this is -3)
```

**Example**: Finding -5 and -6
```
5:         0000...0101
-5 = 5̄ + 1: 1111...1011

Alternative for -6:
Since x̄ = -1 - x
If x = 5, then x̄ = -6
Therefore: 1111...1010 (this is -6)
```

### Verification Examples

**Example 1**: 1 + (-2) = -1
```
  0000...0001  (1)
+ 1111...1110  (-2)
--------------
  1111...1111  (-1) ✓
```

**Example 2**: 2 + (-1) = 1
```
  0000...0010  (2)
+ 1111...1111  (-1)
--------------
1 0000...0001  (discard 33rd bit)
  0000...0001  (1) ✓
```

---

## Signed and Unsigned Numbers

### When to Use Each

**Unsigned Numbers**:
- Use when all values are positive (e.g., counting events)
- Provides twice the range for positive numbers
- Range: 0 to 2³² - 1

**Signed Numbers**:
- Use when both positive and negative values needed
- MSB indicates sign
- Range: -2³¹ to 2³¹ - 1

### MIPS Instructions

Different instructions for signed vs unsigned:

**Example**: Set on Less Than (SLT)

```assembly
slt $t0, $t1, $0    # Signed: Sets $t0=1 if $t1 < 0
sltu $t0, $t1, $0   # Unsigned: Different result for same bits
```

For the bit pattern `1000...0000`:
- **Signed interpretation**: Negative number (MSB=1) → less than 0 → set $t0=1
- **Unsigned interpretation**: Large positive number → greater than 0 → set $t0=0

**Important**: The compiler tracks whether variables are signed or unsigned and generates appropriate instructions.

---

## Sign Extension

### Purpose

When converting a smaller bit-width signed number to a larger bit-width, we need to preserve the sign.

### Process

**Rule**: Copy the MSB to fill all additional bits on the left.

**Example 1**: Extending +2 from 16-bit to 32-bit
```
16-bit: 0000 0000 0000 0010
32-bit: 0000 0000 0000 0000 0000 0000 0000 0010
        └─────────────┘
        MSB (0) copied
```

**Example 2**: Extending -2 from 16-bit to 32-bit
```
16-bit: 1111 1111 1111 1110
32-bit: 1111 1111 1111 1111 1111 1111 1111 1110
        └─────────────┘
        MSB (1) copied
```

**Note**: For unsigned numbers, simply pad with zeros. Sign extension is crucial only for signed numbers.

---

## Alternative Representations

### One's Complement

**Method**: Negative number represented by inverting all bits of x.

**Problem**: Two representations for zero
- +0: 0000...0000
- -0: 1111...1111

### Sign and Magnitude

**Method**:
- MSB represents sign (0=positive, 1=negative)
- Remaining 31 bits represent magnitude

**Problem**:
- Complex arithmetic operations
- Two representations for zero
- Requires additional conversion steps

### Why Two's Complement is Preferred

1. **Single zero representation**: Only one way to represent 0
2. **Simple arithmetic**: Addition and subtraction work naturally
3. **No special conversion**: Math operations work directly
4. **Hardware efficiency**: Simpler circuitry design

---

## Addition and Subtraction

### Binary Addition

Process similar to decimal addition with carries:

```
  Bit₁   1 0 1 1
+ Bit₂   0 1 1 0
  ----   -------
  Sum    1 0 0 1
  Carry  1 1 1 0
```

**Algorithm**:
1. Add corresponding bits
2. Generate carry if sum ≥ 2
3. Propagate carry to next position

### Subtraction as Addition

```
a - b = a + (-b)
```

Where `-b` is computed using two's complement:
```
-b = b̄ + 1
```

**Example**: 5 - 3 = 5 + (-3)
```
  0101  (5)
+ 1101  (-3)
------
  0010  (2) ✓
```

### Overflow Detection

**Unsigned Numbers**:
- Overflow when carry out of MSB occurs (33rd bit generated)

**Signed Numbers**:
- Overflow when sign changes unexpectedly
- **Positive + Positive = Negative** → Overflow
- **Negative + Negative = Positive** → Overflow
- **Positive + Negative** → Never overflows

### MIPS Overflow Handling

**Instructions with overflow detection**:
```assembly
add  $s0, $s1, $s2   # Throws exception on overflow
addi $s0, $s1, 100   # Throws exception on overflow
sub  $s0, $s1, $s2   # Throws exception on overflow
```

**Instructions without overflow detection**:
```assembly
addu  $s0, $s1, $s2  # No exception (useful for addresses)
addiu $s0, $s1, 100  # No exception
subu  $s0, $s1, $s2  # No exception
```

---

## Multiplication

### Binary Multiplication Basics

Similar to decimal multiplication with shift-and-add:

```
    1000  (multiplicand)
  × 1001  (multiplier)
  ------
    1000  (1 × 1000, shift 0)
   0000   (0 × 1000, shift 1)
  0000    (0 × 1000, shift 2)
 1000     (1 × 1000, shift 3)
--------
1001000  (product)
```

**Key Rule**: n-bit × n-bit = up to 2n-bit result

Examples:
- 2-bit × 2-bit = 4-bit max
- 3-bit × 3-bit = 6-bit max
- 32-bit × 32-bit = 64-bit max

### Multiplication Algorithm (Version 1: Basic)

**Hardware Requirements**:
- 64-bit multiplicand register (with left shift)
- 32-bit multiplier register (with right shift)
- 64-bit ALU
- 64-bit product register

**Algorithm**:
```
For each bit of multiplier (32 iterations):
    1. Test LSB of multiplier
    2. If LSB = 1: Product = Product + Multiplicand
    3. Shift multiplicand left by 1
    4. Shift multiplier right by 1
```

**Example**: 1000 × 1001

| Step | Multiplicand | Multiplier | Product | Action |
|------|-------------|-----------|---------|--------|
| 0 | 0000 1000 | 1001 | 0000 0000 | Initialize |
| 1 | 0000 1000 | 1001 | 0000 1000 | LSB=1, add |
| 2 | 0001 0000 | 0100 | 0000 1000 | LSB=0, skip |
| 3 | 0010 0000 | 0010 | 0000 1000 | LSB=0, skip |
| 4 | 0100 0000 | 0001 | 0100 1000 | LSB=1, add |

Final: 01001000 = 72 in decimal

### Multiplication Algorithm (Version 2: Optimized)

**Optimization**: Share 64-bit register between product and multiplier

**Hardware Requirements**:
- 32-bit multiplicand register (no shift needed)
- 32-bit ALU
- 64-bit product/multiplier register (combined)

**Key Insight**:
- As multiplier bits are consumed (shifted right), product bits are generated (shifted right)
- Initial: [32-bit product = 0][32-bit multiplier]
- Final: [64-bit product][0-bit multiplier]

**Benefits**:
- Less hardware (32-bit instead of 64-bit components)
- More efficient design
- Faster operation

### Multiplication Algorithm (Version 3: Parallel)

**Combinational Multiplier**: No clock cycles, faster but more expensive

**Design**:
- Multiple adders in parallel (one per bit)
- Each multiplier bit ANDed with multiplicand
- Results added using tree of adders

**Performance**:
- Sequential (clocked): 32 cycles for 32-bit
- Parallel: Combinational delays only

**Trade-off**:
- Speed: Much faster
- Cost: More transistors/gates
- Delay: Reduced to log₂(32) adder delays with tree structure

### MIPS Multiplication Instructions

```assembly
mult  $s2, $s3   # Signed multiplication
multu $s2, $s3   # Unsigned multiplication
```

**Result Storage**:
- No destination register specified
- Result stored in two special 32-bit registers:
  - **HI**: Upper 32 bits
  - **LO**: Lower 32 bits

**Retrieving Results**:
```assembly
mfhi $s0   # Move from HI to $s0
mflo $s1   # Move from LO to $s1
```

### Signed Multiplication

Two's complement multiplication works with the same algorithm!

**Alternative approach**:
1. Convert negative numbers to positive
2. Perform unsigned multiplication
3. Adjust sign of result

**Sign rule**:
- Same signs → Positive product
- Different signs → Negative product

---

## Division

### Division Basics

**Components**:
- **Dividend**: Number to be divided
- **Divisor**: Number dividing the dividend
- **Quotient**: Result of division
- **Remainder**: What's left over

**Example**: 795 ÷ 31
```
     025  (quotient)
   ------
31 | 795
     62↓  (31 × 2 = 62)
    ---
     175
     155  (31 × 5 = 155)
     ---
      20  (remainder)
```

### Binary Division Algorithm

**Rules**:
1. Shift divisor right and compare with current dividend
2. If divisor > dividend: Shift 0 into quotient
3. If divisor ≤ dividend: Subtract to get new dividend, shift 1 into quotient
4. Repeat for n bits (32 for 32-bit numbers)

**Example**: 1001010 ÷ 1000 (74 ÷ 8 in decimal)

```
Step 1: Compare 1 with 1000 → 1000 > 1, shift 0 into quotient
Step 2: Compare 10 with 1000 → 1000 > 10, shift 0 into quotient
Step 3: Compare 100 with 1000 → 1000 > 100, shift 0 into quotient
Step 4: Compare 1001 with 1000 → 1001 > 1000, subtract, shift 1
        1001 - 1000 = 1
Step 5: Compare 10 with 1000 → 1000 > 10, shift 0 into quotient
Step 6: Compare 100 with 1000 → 1000 > 100, shift 0 into quotient
Step 7: Compare 1010 with 1000 → 1010 > 1000, subtract, shift 1
        1010 - 1000 = 10

Quotient: 0001001 (9)
Remainder: 10 (2)
Verification: 8 × 9 + 2 = 74 ✓
```

### Detailed Example: 7 ÷ 2

Using 4-bit arithmetic (extended to 8-bit for operations):

| Iteration | Divisor | Remainder | Quotient | Operation |
|-----------|---------|-----------|----------|-----------|
| Init | 0010 0000 | 0000 0111 | 0000 | Initialize |
| 1 | 0010 0000 | 0000 0111 | 0000 | Rem-Div < 0, shift 0 |
| | | | | Restore remainder |
| 2 | 0001 0000 | 0000 0111 | 0000 | Rem-Div < 0, shift 0 |
| | | | | Restore remainder |
| 3 | 0000 1000 | 0000 0111 | 0000 | Rem-Div < 0, shift 0 |
| | | | | Restore remainder |
| 4 | 0000 0100 | 0000 0111 | 0001 | Rem-Div ≥ 0, shift 1 |
| | | 0000 0011 | | New remainder = 3 |
| 5 | 0000 0010 | 0000 0011 | 0011 | Rem-Div ≥ 0, shift 1 |
| | | 0000 0001 | | New remainder = 1 |

**Result**: Quotient = 0011 (3), Remainder = 0001 (1) ✓

### Division Algorithm Steps

**Detailed Process**:
```
Repeat for n bits:
    1. Remainder = Remainder - Divisor
    2. Test Remainder:
       a. If Remainder < 0:
          - Shift 0 into quotient
          - Restore: Remainder = Remainder + Divisor
       b. If Remainder ≥ 0:
          - Shift 1 into quotient
    3. Shift divisor right by 1 bit
```

### Division Hardware (Version 1: Basic)

**Components**:
- 64-bit divisor register (with right shift)
- 64-bit ALU (for subtraction)
- 64-bit remainder register
- 32-bit quotient register
- Control unit

**Initial Setup**:
- Divisor: [32-bit value][32 zeros]
- Remainder: [32 zeros][32-bit dividend]

**Process**:
- Compare by subtraction
- Examine sign bit of result
- Restore if negative
- Shift quotient accordingly

### Division Hardware (Version 2: Optimized)

**Optimizations**:
- 32-bit divisor register (no need for 64-bit)
- 32-bit ALU
- 64-bit remainder register (shared with quotient space)
- Shift remainder left instead of divisor right

**Key Insight**:
- Instead of shifting divisor right, shift remainder left
- Saves hardware complexity
- Same result with less circuitry

### MIPS Division Instructions

```assembly
div  $s2, $s3   # Signed division
divu $s2, $s3   # Unsigned division
```

**Result Storage** (like multiplication):
- **HI register**: Remainder
- **LO register**: Quotient

**Retrieving Results**:
```assembly
mfhi $s0   # Get remainder
mflo $s1   # Get quotient
```

### Signed Division

**Sign Convention**: Dividend and remainder must have the same sign

**Examples**:

| Dividend | Divisor | Quotient | Remainder | Verification |
|----------|---------|----------|-----------|--------------|
| +7 | +2 | +3 | +1 | 2×3 + 1 = 7 ✓ |
| -7 | +2 | -3 | -1 | 2×(-3) + (-1) = -7 ✓ |
| +7 | -2 | -3 | +1 | (-2)×(-3) + 1 = 7 ✓ |
| -7 | -2 | +3 | -1 | (-2)×3 + (-1) = -7 ✓ |

**Why not (-7) ÷ 2 = -4 remainder +1?**
- While mathematically valid: 2×(-4) + 1 = -7
- **Convention**: Dividend and remainder have same sign
- Therefore: (-7) ÷ 2 = -3 remainder -1

**Quotient Sign Rule**:
- Same signs → Positive quotient
- Different signs → Negative quotient

**Implementation**:
1. Convert to positive values
2. Perform unsigned division
3. Adjust signs according to rules

---

## Summary

### Key Concepts Covered

1. **Number Systems**:
   - Binary representation
   - ASCII vs Binary efficiency
   - Unsigned vs Signed numbers

2. **Two's Complement**:
   - Standard representation for signed integers
   - Simple arithmetic operations
   - Single zero representation

3. **Arithmetic Operations**:
   - Addition/Subtraction with overflow detection
   - Multiplication: 32-bit × 32-bit → 64-bit
   - Division: Quotient and remainder

4. **Hardware Implementations**:
   - Sequential algorithms (clocked)
   - Optimized designs (reduced hardware)
   - Parallel implementations (faster, more expensive)

5. **MIPS Instructions**:
   - Separate signed/unsigned versions
   - Special registers (HI/LO) for 64-bit results
   - Overflow handling options

### Important Formulas

**Two's Complement**:
```
-x = x̄ + 1
Value = Σ(xᵢ × 2ⁱ) + x₃₁ × (-2³¹)
```

**Arithmetic**:
```
a - b = a + (-b) = a + (b̄ + 1)
n-bit × n-bit → 2n-bit result
```

### Next Topics

The next week will cover **floating-point arithmetic** to handle real numbers and decimal calculations, as integers are now well understood.
