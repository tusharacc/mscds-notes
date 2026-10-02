# Week 4: Floating Point Arithmetic

## Overview
This week covers floating point number representation and arithmetic in computer systems, including the IEEE 754 standard, floating point operations, and optimization techniques.

---

## 4.1.1 Sign and Magnitude Representation

### Introduction to Floating Point Numbers

**Why Floating Point?**
- Used to represent rational and real numbers (not just integers)
- Example: 3.5 × 10⁹ can be written as (3 × 10⁰ + 5 × 10⁻¹) × 10⁹

### Normalized Scientific Notation
- **Decimal**: Single non-zero digit to the left of the decimal point
- **Binary**: Single non-zero digit to the left of the binary point
- Binary Example: 1.010011₂ × 2⁻⁵
  - Expanded: (1 × 2⁰ + 0 × 2⁻¹ + 1 × 2⁻² + 0 × 2⁻³ + 0 × 2⁻⁴ + 1 × 2⁻⁵ + 1 × 2⁻⁶) × 2⁻⁵

### IEEE 754 Standard

**Purpose:**
- Standardizes floating point representation across different architectures
- Ensures program portability and reproducibility across systems

**Single Precision Format (32 bits):**
```
[Sign: 1 bit][Exponent: 8 bits][Fraction: 23 bits]
```

- **Sign bit**: 0 = positive, 1 = negative
- **Exponent**: 8 bits (values 0-255)
- **Fraction**: 23 bits (represents mantissa after the implicit 1)

### Representation Details

**Key Assumptions:**
- Normalized numbers always have form: 1.xxxx₂
- The leading 1 is implicit (not stored) - saves 1 bit
- IEEE 754 representation: (-1)^S × (1 + F) × 2^(E-127)
  - S = sign bit
  - F = fraction field
  - E = exponent field value

**Example: 1.01001₂ × 2⁻⁵**
- Sign: 0 (positive)
- Fraction: 01001 followed by zeros (store only the part after "1.")
- Exponent: -5 (stored with bias)

### Exponent Bits and Range

**Why 8 bits for exponent?**
- More exponent bits = wider range (not more numbers)
- 8 bits: Range from 2⁻¹²⁷ to 2¹²⁸
- 10 bits: Range from 2⁻⁵¹¹ to 2⁵¹²
- Same 2³² total numbers, just spread differently
- Trade-off: More exponent bits = wider range but less precision

**Overflow and Underflow:**
- **Overflow**: Result larger than maximum representable value
- **Underflow**: Result smaller than minimum representable value

### Double Precision Format (64 bits)

```
[Sign: 1 bit][Exponent: 11 bits][Fraction: 52 bits]
```

- Uses two 32-bit registers
- Exponent range: 2⁻¹⁰²³ to 2¹⁰²⁴
- Higher precision with 52 fraction bits (vs 23 in single precision)

---

## 4.1.2 Exponent Representation

### Biased Notation

**Why Use Bias?**
- Allows easy comparison of floating point numbers by looking at exponent
- Facilitates sorting and comparison operations
- Makes exponent field interpretable as unsigned integer for comparison

**Single Precision (8-bit exponent):**
- Range: 0 to 255 (unsigned)
- Bias: 127
- Actual exponent range: -127 to +128
- Representation: 0 = negative, 1 prefix = positive

**Bias Calculation:**
- **Storing**: Actual exponent + 127 = stored value
  - Example: Exponent 0 → Store 127 (01111111₂)
  - Example: Exponent 128 → Store 255 (11111111₂)
- **Reading**: Stored value - 127 = actual exponent
  - Example: Read 127 → Exponent is 0
  - Example: Read 129 → Exponent is 2

**Double Precision:**
- Bias: 1023
- 11-bit exponent field

### IEEE 754 Complete Formula

**Single Precision:**
```
(-1)^S × (1 + F) × 2^(E-127)
```

**Double Precision:**
```
(-1)^S × (1 + F) × 2^(E-1023)
```

### Special Cases

**1. Zero (0)**
- All bits zero: Sign=0, Exponent=0, Fraction=0
- Implicit 1 is NOT added
- Special code for representing zero

**2. Denormalized Numbers (Denorms)**
- Exponent = 0, Fraction ≠ 0
- Represents very small values
- True exponent: 2⁻¹²⁷ (very small)
- Used for gradual underflow

**3. Infinity**
- Exponent = all 1s (255), Fraction = 0
- Sign bit determines +∞ or -∞
- Results from overflow or division by zero

**4. Not a Number (NaN)**
- Exponent = all 1s (255), Fraction ≠ 0
- Results from undefined operations:
  - 0/0
  - ∞ - ∞
  - sqrt(-1)

### Reserved Values and Actual Range

**Reserved Exponent Values:**
- 0: Reserved for zero and denorms
- 255: Reserved for infinity and NaN
- Usable range: 1 to 254

**Actual Exponent Range:**
- Stored values: 1 to 254
- True exponents: -126 to +127 (after subtracting bias 127)
- Adjusted from original -127 to +128 due to reserved values

**True Range:**
- Largest: (1 + 1) × 2¹²⁷ = 2 × 2¹²⁷
- Smallest: 1 × 2⁻¹²⁶ (plus denorms)

### Conversion Examples

**Decimal to Binary Fraction:**

*Integer part* (divide by 2):
- 17₁₀ → 10001₂

*Fractional part* (multiply by 2):
- 0.75₁₀:
  - 0.75 × 2 = 1.5 → 1, remainder 0.5
  - 0.5 × 2 = 1.0 → 1, remainder 0
  - Result: 0.11₂

- 0.63₁₀:
  - 0.63 × 2 = 1.26 → 1, remainder 0.26
  - 0.26 × 2 = 0.52 → 0, remainder 0.52
  - 0.52 × 2 = 1.04 → 1, remainder 0.04
  - Result: 0.101000...₂

**Binary to Normalized Form:**
- 0.11₂ = 1.1₂ × 2⁻¹

**Example: -0.75 in Single Precision**
1. Binary: -0.11₂ = -1.1₂ × 2⁻¹
2. Sign: 1 (negative)
3. Fraction: 1 (after the implicit "1.")
4. Exponent: -1 + 127 = 126 = 01111110₂

```
[1][01111110][10000000000000000000000]
```

**Example: -0.75 in Double Precision**
1. Sign: 1
2. Exponent: -1 + 1023 = 1022 = 01111111110₂
3. Fraction: 1 followed by 51 zeros

```
[1][01111111110][1000000000000000000000000000000000000000000000000000]
```

**Example: Reading Single Precision to Decimal**

Given: `[1][10000001][01000000000000000000000]`

1. Sign: 1 → negative
2. Exponent: 10000001₂ = 129₁₀ → 129 - 127 = 2
3. Fraction: 01000... = 0 × 2⁻¹ + 1 × 2⁻² = 0.25
4. Value: 1 + 0.25 = 1.25
5. Result: -1 × 1.25 × 2² = -1.25 × 4 = -5

---

## 4.1.3 Floating Point Addition and Multiplication

### Floating Point Addition

**Example: 9.999 × 10¹ + 1.610 × 10⁻¹**

**Steps:**

1. **Align Exponents** (convert to larger exponent)
   - 9.999 × 10¹ (unchanged)
   - 1.610 × 10⁻¹ → 0.01610 × 10¹
   - Lost precision: dropped the last digit (1→0.016)

2. **Add Significands**
   - 9.999 + 0.016 = 10.015 × 10¹

3. **Normalize**
   - 10.015 × 10¹ → 1.0015 × 10²
   - Shift decimal point left, increment exponent

4. **Check for Overflow/Underflow**
   - Verify result is within representable range

5. **Round**
   - Limited to 4 decimal digits: 1.0015 → 1.002
   - Result: 1.002 × 10²

**Key Challenges:**
- **Precision Loss**: Occurs during alignment and rounding
- **Guard Bits**: Extra bits in hardware adder (beyond 32 bits) help minimize rounding errors
- More fraction bits = better precision in results

**Algorithm Summary:**
1. Convert to larger exponent
2. Add the numbers
3. Normalize the result
4. Check for overflow
5. Round and re-normalize if needed

### Floating Point Multiplication

**Example: 32.56 × 27.29**

**Steps:**

1. **Convert to Normalized Form**
   - 32.56 = 3.256 × 10¹
   - 27.29 = 2.729 × 10¹

2. **Important: Exponent Bias Handling**
   - When reading from register: subtract bias (127 or 1023)
   - Get true exponent value before computation
   - Critical step often overlooked

3. **Multiply Significands and Add Exponents**
   - Significands: 3.256 × 2.729
   - Exponents: 1 + 1 = 2
   - Result form: (product) × 10²

4. **Normalize**
   - Locate decimal/binary point
   - Adjust exponent based on shift

5. **Assign Sign**
   - Same as integer multiplication
   - XOR of sign bits

**Key Difference from Integer Multiplication:**
- In integers: separate handling of high/low bits
- In floating point: direct storage in single register

### MIPS Floating Point Instructions

**Arithmetic Operations:**
```assembly
add.s  F1, F2, F3    # F1 = F2 + F3 (single precision)
add.d  F2, F4, F6    # F2 = F4 + F6 (double precision)
sub.s  F1, F2, F3    # F1 = F2 - F3 (single precision)
sub.d  F2, F4, F6    # F2 = F4 - F6 (double precision)
mul.s  F1, F2, F3    # F1 = F2 × F3 (single precision)
mul.d  F2, F4, F6    # F2 = F4 × F6 (double precision)
div.s  F1, F2, F3    # F1 = F2 ÷ F3 (single precision)
div.d  F2, F4, F6    # F2 = F4 ÷ F6 (double precision)
```

**Comparison Operations:**
```assembly
c.eq.s  F1, F2       # Compare F1 == F2 (single precision)
c.eq.d  F2, F4       # Compare F2 == F4 (double precision)
bc1t    label        # Branch if comparison true
bc1f    label        # Branch if comparison false
```

**Key Differences from Integer Instructions:**
- Comparison + branch split into two instructions
- Legacy from coprocessor architecture (FPU was separate)
- Coprocessor sets internal flag bit
- Branch instruction reads coprocessor flag

**Registers:**
- **F0-F31**: 32 floating point registers
- Single precision: Uses one register
- Double precision: Uses two consecutive registers (must start with even register)
  - Examples: F4-F5, F6-F7, F10-F11
  - Convention: First register must be even

**Load/Store Operations:**
```assembly
lwc1  F4, addr(S1)   # Load word to coprocessor 1 (FPU)
swc1  F4, addr(S1)   # Store word from coprocessor 1 (FPU)
```
- Address registers are still integers
- At least one operand must be integer (for addressing)

---

## 4.1.4 Fixed Point and Subword Parallelism

### Fixed Point Representation

**Motivation:**
- Floating point operations are slower (alignment, normalization, rounding)
- Alternative: Convert all numbers to integers with same scaling factor

**Concept:**
- Every number multiplied by same factor
- Use integer-only arithmetic
- Convert back when storing result

**Example: Factor = 1/1000**

| Decimal Value | Fixed Point Representation |
|---------------|---------------------------|
| 1.46          | 1460 / 1000               |
| 1.7198        | 1720 / 1000               |
| 5.624         | 5624 / 1000               |

**Advantages:**
- Faster execution (simple integer addition)
- Saves cycles (no exponent matching, normalization)
- Single conversion step when storing

**Disadvantages:**
- Lower precision (rounding errors)
- Increased programming effort
- Loses some accuracy (e.g., 1.7198 → 1.720)

**Use Cases:**
- Performance-critical applications
- Embedded systems
- DSP applications
- When speed > precision

### Fahrenheit to Celsius Example

**C Code:**
```c
float f2c(float fahrenheit) {
    return ((fahrenheit - 32.0) * 5.0) / 9.0;
}
```

**MIPS Assembly:**
```assembly
# Assume: fahrenheit in F12
lwc1   F16, const5(GP)      # Load 5.0 into F16
lwc1   F18, const9(GP)      # Load 9.0 into F18
div.s  F16, F16, F18        # F16 = 5.0 / 9.0
lwc1   F18, const32(GP)     # Load 32.0 into F18
sub.s  F18, F12, F18        # F18 = fahrenheit - 32.0
mul.s  F0, F18, F16         # F0 = F18 * F16 (result)
# Return (F0 contains result)
```

**Key Observations:**
- All operations use even registers (compatible with single/double precision)
- Load operations fetch floating point values (5.0, 9.0, 32.0, not integers)
- Division and multiplication have three operands (unlike integer operations)
- Integer operations: mult/div store in HI/LO registers
- Floating point: direct storage in destination register

### Subword Parallelism

**Motivation:**
- Many data types don't need full 32-bit width:
  - Pixel values: 8 bits (1 byte)
  - Audio samples: 16 bits (half word)
- Wasteful to use full 32-bit adder for 8-bit values

**Concept:**
Partition a 32-bit register and ALU to perform multiple operations simultaneously.

**Example: 32-bit Register as Four 8-bit Values**
```
[a: 8 bits][b: 8 bits][c: 8 bits][d: 8 bits]
+
[a': 8 bits][b': 8 bits][c': 8 bits][d': 8 bits]
=
[a+a': 8 bits][b+b': 8 bits][c+c': 8 bits][d+d': 8 bits]
```

**Implementation:**
- Partition carry chain in ALU
- Prevent carry propagation between subwords
- Perform 4 parallel 8-bit additions instead of 1 32-bit addition

**Configurations:**
- 64-bit adder → 4 × 16-bit adders
- 64-bit adder → 8 × 8-bit adders
- 32-bit adder → 4 × 8-bit adders

**Benefits:**
1. **Parallel Operations**: Multiple additions in one instruction
2. **Efficient Loading**: Load 4 values in single fetch
3. **Better Throughput**: Process more data per cycle

**Applications:**
- Image processing (pixel operations)
- Audio processing (sample manipulation)
- Video encoding/decoding
- SIMD (Single Instruction, Multiple Data) operations

**Example Use Case:**
```
Load word: Fetches 4 pixels (32 bits total)
Add instruction: Performs 4 parallel 8-bit additions
Result: 4 processed pixels in one operation cycle
```

---

## Summary

### Key Concepts Covered

1. **IEEE 754 Standard**
   - Ensures portability across systems
   - Sign-magnitude representation
   - Single precision (32-bit) and double precision (64-bit)

2. **Representation Components**
   - Sign bit (1 bit)
   - Exponent (8 or 11 bits, biased)
   - Fraction (23 or 52 bits, implicit leading 1)

3. **Special Values**
   - Zero, denorms, infinity, NaN
   - Reserved exponent values (0 and max)

4. **Arithmetic Operations**
   - Addition: Align exponents, add, normalize, round
   - Multiplication: Multiply significands, add exponents, normalize
   - Precision loss is inevitable

5. **Optimization Techniques**
   - Fixed point: Trade precision for speed
   - Subword parallelism: Process multiple values simultaneously

6. **MIPS Support**
   - Dedicated floating point registers (F0-F31)
   - Separate instructions for single/double precision
   - Coprocessor-based comparison and branching

### Important Formulas

**Single Precision:**
```
Value = (-1)^S × (1 + F) × 2^(E-127)
```

**Double Precision:**
```
Value = (-1)^S × (1 + F) × 2^(E-1023)
```

**Range:**
- Single: ≈ 2⁻¹²⁶ to 2¹²⁷
- Double: ≈ 2⁻¹⁰²² to 2¹⁰²³

### Practical Considerations

- **Precision vs Range**: More exponent bits = wider range but less precision
- **Performance**: Floating point slower than integer operations
- **Optimization**: Fixed point and subword parallelism for speed-critical code
- **Portability**: IEEE 754 ensures consistent behavior across platforms
