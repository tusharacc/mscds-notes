# Week 2: Control Instructions and Advanced MIPS Programming

## Overview
Week 2 covers control flow in MIPS assembly language, including branching, procedure calls, memory management, and advanced topics like character handling and endianness. This week builds on the foundational MIPS concepts to enable complex program structures.

---

## Table of Contents
1. [Control Instructions](#control-instructions)
2. [Branching and Loops](#branching-and-loops)
3. [Procedure Calls](#procedure-calls)
4. [Jump and Link](#jump-and-link)
5. [Data Movement Among Registers](#data-movement-among-registers)
6. [Character Handling](#character-handling)
7. [Advanced Topics](#advanced-topics)

---

## Control Instructions

### Instruction Formats

MIPS instructions are encoded as 32-bit binary numbers. There are two main types:

#### R-Type Instructions (Register Type)
Used for operations involving multiple registers (e.g., ADD, SUB).

**Format (32 bits total):**
- **Opcode (6 bits)**: Identifies the operation (e.g., 000000 for ADD)
- **Source Register 1 (5 bits)**: First source register (RS)
- **Source Register 2 (5 bits)**: Second source register (RT)
- **Destination Register (5 bits)**: Result destination (RD)
- **Shift Amount (5 bits)**: Number of positions to shift (0-31)
- **Function Code (6 bits)**: Specifies operation variant

**Example:** `ADD $t0, $s1, $s2`
- Adds values in $s1 and $s2, stores result in $t0

**Why 5 bits for registers?**
- MIPS has 32 registers
- 2^5 = 32, so 5 bits can uniquely identify each register

#### I-Type Instructions (Immediate Type)
Used for operations with constants or memory access (e.g., ADDI, LW, SW).

**Format (32 bits total):**
- **Opcode (6 bits)**: Identifies the operation
- **Source Register (5 bits)**: Source register
- **Target Register (5 bits)**: Destination register
- **Immediate/Constant (16 bits)**: Constant value or offset

**Example:** `ADDI $s3, $t0, 32`
- Adds 32 to $t0, stores result in $s3

### Logical Operations

**Shift Left Logical (SLL)**
- Shifts bits to the left, fills with zeros
- Equivalent to multiplication by powers of 2
- Example: `101` (5) shifted left by 1 = `1010` (10)
- Shifting left by n positions = multiplying by 2^n

**Shift Right Logical (SRL)**
- Shifts bits to the right, discards rightmost bits
- Equivalent to division by powers of 2
- Example: `1010` (10) shifted right by 1 = `101` (5)
- Shifting right by n positions = dividing by 2^n

**Bitwise Operations**
- **AND**: Bit-by-bit AND operation
- **OR**: Bit-by-bit OR operation
- **NOT**: Bit-by-bit NOT operation

---

## Branching and Loops

### Conditional Branching

Conditional branches jump to a label only if a condition is satisfied.

**Branch on Equal (BEQ)**
```assembly
BEQ $s1, $s2, L1    # If $s1 == $s2, jump to label L1
```

**Branch on Not Equal (BNE)**
```assembly
BNE $s1, $s2, L1    # If $s1 != $s2, jump to label L1
```

**Set on Less Than (SLT)**
```assembly
SLT $t0, $s1, $s2   # If $s1 < $s2, set $t0 = 1, else $t0 = 0
```

Note: SLT itself is not a branching instruction but sets a value that can be used with BEQ/BNE for comparison-based branching.

**Branch on Less Than (BLT) - Pseudo Instruction**
```assembly
BLT $a0, 1, label   # Implemented as:
                    # SLTI $t0, $a0, 1
                    # BEQ $t0, $zero, label
```

### Unconditional Branching

**Jump (J)**
```assembly
J L1                # Unconditionally jump to label L1
```

**Jump Register (JR)**
```assembly
JR $s0              # Jump to address stored in $s0
```
- Used when the target address is computed at runtime

### If-Then-Else Example

**C Code:**
```c
if (i == j) {
    f = g + h;
} else {
    f = g - h;
}
```

**Assembly Version 1 (using BNE):**
```assembly
        BNE  $s3, $s4, else    # If i != j, go to else
        ADD  $s0, $s1, $s2     # f = g + h
        J    exit              # Jump to exit
else:   SUB  $s0, $s1, $s2     # f = g - h
exit:   # Continue execution
```

**Assembly Version 2 (using BEQ):**
```assembly
        BEQ  $s3, $s4, then    # If i == j, go to then
        SUB  $s0, $s1, $s2     # f = g - h
        J    exit
then:   ADD  $s0, $s1, $s2     # f = g + h
exit:   # Continue execution
```

### While Loop Example

**C Code:**
```c
while (save[i] == k) {
    i = i + 1;
}
```

**Assembly Version 1:**
```assembly
loop:   SLL  $t1, $s3, 2       # $t1 = i * 4 (multiply by 4)
        ADD  $t1, $t1, $s6     # $t1 = address of save[i]
        LW   $t0, 0($t1)       # Load save[i] into $t0
        BNE  $t0, $s5, exit    # If save[i] != k, exit
        ADDI $s3, $s3, 1       # i = i + 1
        J    loop              # Jump back to loop
exit:   # Continue
```

**Assembly Version 2 (Optimized):**
```assembly
        SLL  $t1, $s3, 2       # Initial: $t1 = i * 4
        ADD  $t1, $t1, $s6     # $t1 = address of save[i]
loop:   LW   $t0, 0($t1)       # Load save[i]
        BNE  $t0, $s5, exit    # If save[i] != k, exit
        ADDI $s3, $s3, 1       # i = i + 1
        ADDI $t1, $t1, 4       # Move to next array element
        J    loop
exit:   # Continue
```

**Optimization:** Moving shift operations outside the loop and incrementing by 4 directly instead of recalculating the address each iteration.

---

## Procedure Calls

### Memory Organization

Memory is organized into distinct regions:

1. **Code Segment**: Stores program instructions
2. **Global Data**: Stores global variables
3. **Heap**: Grows upward (low to high addresses) for dynamic allocation
4. **Stack**: Grows downward (high to low addresses) for procedure calls

### Stack Frames (Activation Records)

Each procedure call creates a stack frame containing:
- Local variables
- Saved registers
- Return address
- Arguments (if more than 4)
- Frame pointer (points to start of frame)
- Stack pointer (points to end/top of frame)

### Argument and Return Value Registers

**Argument Registers:** `$a0 - $a3`
- Used to pass the first 4 arguments to a procedure
- Additional arguments are stored on the stack

**Return Value Registers:** `$v0 - $v1`
- Used to return values from a procedure

### Calling Convention

When procedure A calls procedure B:

1. **Caller (A) prepares:**
   - Saves caller-saved registers (`$t0-$t9`, `$a0-$a3`, `$ra`)
   - Places arguments in `$a0-$a3`
   - Executes `JAL` (Jump and Link)

2. **Callee (B) executes:**
   - Allocates stack space (decrements `$sp`)
   - Saves callee-saved registers (`$s0-$s7`, `$fp`)
   - Executes procedure body
   - Places return values in `$v0-$v1`
   - Restores saved registers
   - Deallocates stack space (increments `$sp`)
   - Returns via `JR $ra`

3. **Caller (A) resumes:**
   - Retrieves return values from `$v0-$v1`
   - Restores caller-saved registers

---

## Jump and Link

### Program Counter (PC)

The Program Counter is a special register that:
- Stores the address of the currently executing instruction
- Automatically increments by 4 after each instruction (since each instruction is 4 bytes)
- Is updated during jumps and branches

### Jump and Link (JAL) Instruction

**Syntax:** `JAL procedure_label`

**Operation:**
1. Saves return address: `$ra = PC + 4`
2. Jumps to target: `PC = address of procedure_label`

**Return from Procedure:**
```assembly
JR $ra              # Jump to address in $ra
```

### Nested Procedure Calls

When procedure A calls B, which calls C:
- Each call overwrites `$ra`
- **Solution:** Save `$ra` on the stack before making another call

**Example:**
```assembly
# Procedure A calls B
procedureA:
    ADDI $sp, $sp, -4      # Allocate stack space
    SW   $ra, 0($sp)       # Save return address
    JAL  procedureB        # Call B
    LW   $ra, 0($sp)       # Restore return address
    ADDI $sp, $sp, 4       # Deallocate stack space
    JR   $ra               # Return to caller

# Procedure B calls C
procedureB:
    ADDI $sp, $sp, -4      # Allocate stack space
    SW   $ra, 0($sp)       # Save return address
    JAL  procedureC        # Call C
    LW   $ra, 0($sp)       # Restore return address
    ADDI $sp, $sp, 4       # Deallocate stack space
    JR   $ra               # Return to A
```

### Why Save on Stack?

Registers are like a "scratchpad" that gets overwritten when procedures switch. The stack provides persistent storage that survives procedure calls.

---

## Data Movement Among Registers

### Register Classification

**32 MIPS Registers:**

| Register | Number | Name | Purpose | Saved By |
|----------|--------|------|---------|----------|
| `$zero` | 0 | Zero | Constant 0 | N/A |
| `$at` | 1 | Assembler Temporary | Reserved for assembler | N/A |
| `$v0-$v1` | 2-3 | Values | Return values | Caller |
| `$a0-$a3` | 4-7 | Arguments | Function arguments | Caller |
| `$t0-$t7` | 8-15 | Temporaries | Temporary values | Caller |
| `$s0-$s7` | 16-23 | Saved | Preserved across calls | Callee |
| `$t8-$t9` | 24-25 | Temporaries | More temporary values | Caller |
| `$k0-$k1` | 26-27 | Kernel | Reserved for OS | N/A |
| `$gp` | 28 | Global Pointer | Points to global data | N/A |
| `$sp` | 29 | Stack Pointer | Points to top of stack | Callee |
| `$fp` | 30 | Frame Pointer | Points to start of frame | Callee |
| `$ra` | 31 | Return Address | Return address | Caller |

### Caller-Saved vs Callee-Saved

**Caller-Saved Registers:** `$t0-$t9`, `$a0-$a3`, `$ra`
- If the caller needs these values after a call, it must save them
- Callee can freely overwrite them

**Callee-Saved Registers:** `$s0-$s7`, `$fp`, `$sp`
- If the callee uses these, it must save and restore them
- Caller can rely on these values being preserved

### Leaf Function Example

A leaf function doesn't call other functions.

**C Code:**
```c
int leaf_example(int g, int h, int i, int j) {
    int f;
    f = (g + h) - (i + j);
    return f;
}
```

**Assembly (Conservative - Saves Registers):**
```assembly
leaf_example:
    ADDI $sp, $sp, -12     # Allocate 12 bytes (3 registers)
    SW   $s0, 0($sp)       # Save $s0
    SW   $t0, 4($sp)       # Save $t0
    SW   $t1, 8($sp)       # Save $t1

    ADD  $t0, $a0, $a1     # $t0 = g + h
    ADD  $t1, $a2, $a3     # $t1 = i + j
    SUB  $s0, $t0, $t1     # $s0 = $t0 - $t1
    ADD  $v0, $s0, $zero   # Move result to $v0

    LW   $t1, 8($sp)       # Restore $t1
    LW   $t0, 4($sp)       # Restore $t0
    LW   $s0, 0($sp)       # Restore $s0
    ADDI $sp, $sp, 12      # Deallocate stack space
    JR   $ra               # Return
```

**Assembly (Optimized - No Stack):**
```assembly
leaf_example:
    ADD  $t0, $a0, $a1     # $t0 = g + h
    ADD  $t1, $a2, $a3     # $t1 = i + j
    SUB  $v0, $t0, $t1     # $v0 = $t0 - $t1
    JR   $ra               # Return
```

**Optimization:** Since we use only temporary registers and return directly in `$v0`, no stack operations are needed.

### Recursive Function Example (Factorial)

**C Code:**
```c
int factorial(int n) {
    if (n < 1) return 1;
    else return n * factorial(n - 1);
}
```

**Assembly:**
```assembly
fact:
    SLTI $t0, $a0, 1       # Set $t0 = 1 if n < 1
    BEQ  $t0, $zero, L1    # If n >= 1, go to L1
    ADDI $v0, $zero, 1     # Return 1
    JR   $ra               # Return

L1: ADDI $sp, $sp, -8      # Allocate stack space
    SW   $ra, 4($sp)       # Save return address
    SW   $a0, 0($sp)       # Save n

    ADDI $a0, $a0, -1      # n = n - 1
    JAL  fact              # Call factorial(n-1)

    LW   $a0, 0($sp)       # Restore n
    LW   $ra, 4($sp)       # Restore return address
    ADDI $sp, $sp, 8       # Deallocate stack space

    MUL  $v0, $v0, $a0     # $v0 = factorial(n-1) * n
    JR   $ra               # Return
```

**Key Points:**
- Must save `$ra` because we make another call
- Must save `$a0` (n) to use it after recursive call
- Return value from recursive call is in `$v0`

---

## Character Handling

### Byte Operations

Characters in C use ASCII format (8 bits = 1 byte per character).

**Load Byte (LB):** Loads 1 byte from memory
**Store Byte (SB):** Stores 1 byte to memory
**Load Halfword (LH):** Loads 2 bytes (16 bits)
**Store Halfword (SH):** Stores 2 bytes (16 bits)

**ASCII Values:**
- Uppercase 'A' = 65
- Lowercase 'a' = 97
- Null character '\0' = 0 (terminates strings)

### String Copy Example

**C Code:**
```c
void strcpy(char x[], char y[]) {
    int i = 0;
    while ((x[i] = y[i]) != '\0') {
        i = i + 1;
    }
}
```

**Assembly:**
```assembly
strcpy:
    ADDI $sp, $sp, -4      # Allocate stack space
    SW   $s0, 0($sp)       # Save $s0

    ADD  $s0, $zero, $zero # i = 0

L1: ADD  $t1, $a1, $s0     # $t1 = address of y[i]
    LB   $t2, 0($t1)       # Load byte y[i] into $t2
    ADD  $t3, $a0, $s0     # $t3 = address of x[i]
    SB   $t2, 0($t3)       # Store byte to x[i]
    BEQ  $t2, $zero, exit  # If y[i] == '\0', exit
    ADDI $s0, $s0, 1       # i = i + 1
    J    L1                # Loop back

exit:
    LW   $s0, 0($sp)       # Restore $s0
    ADDI $sp, $sp, 4       # Deallocate stack space
    JR   $ra               # Return
```

**Key Points:**
- `$a0` points to x[0], `$a1` points to y[0]
- Characters are 1 byte apart, so adding i gives the address of the ith character
- Use LB/SB instead of LW/SW for byte operations
- Save `$s0` since it's a callee-saved register

---

## Advanced Topics

### Large Constants

MIPS immediate instructions use 16-bit constants. For 32-bit constants:

**Load Upper Immediate (LUI)**
```assembly
LUI  $t0, 0xAAAA        # Load upper 16 bits
ORI  $t0, $t0, 0xBBBB   # OR in lower 16 bits
# Result: $t0 = 0xAAAABBBB
```

**How it works:**
1. LUI loads 16 bits into upper half: `$t0 = 0xAAAA0000`
2. ORI ORs lower 16 bits: `$t0 = 0xAAAA0000 | 0x0000BBBB = 0xAAAABBBB`

**For large branch offsets:**
- If target address > 16 bits, load address into register and use JR

### RISC vs CISC

**RISC (Reduced Instruction Set Computer):**
- Simple instructions (e.g., MIPS)
- Fixed instruction size (32 bits)
- Fewer instructions, each does less
- Faster clock speeds, easier to pipeline
- Examples: MIPS, ARM, RISC-V

**CISC (Complex Instruction Set Computer):**
- Complex instructions (e.g., x86)
- Variable instruction size
- More instructions, each can do more
- Examples: x86, x86-64

**Modern Intel Processors:**
- Externally use x86 (CISC) for backward compatibility
- Internally convert x86 to micro-operations (RISC-like)
- Best of both worlds: compatibility + performance

### Endianness

Endianness defines byte order when storing multi-byte data.

**Little-Endian:**
- First byte read goes into the **least significant** position
- Used by: x86, x86-64
- Example: Reading bytes `45 7B 87 7F` from addresses 200-203
  - Register: `0x7F877B45`

**Big-Endian:**
- First byte read goes into the **most significant** position
- Used by: MIPS, IBM, network protocols
- Example: Reading bytes `45 7B 87 7F` from addresses 200-203
  - Register: `0x457B877F`

**Memory Layout:**
```
Address:  200  201  202  203
Bytes:    45   7B   87   7F

Little-Endian Register: [7F][87][7B][45]
                         MSB          LSB

Big-Endian Register:    [45][7B][87][7F]
                         MSB          LSB
```

### Program Compilation and Execution

**Step 1: Compilation**
```
C Program (x.c) → Compiler → Assembly (x.s)
```
- Converts high-level code to assembly language
- Uses pseudo-instructions and labels

**Step 2: Assembly**
```
Assembly (x.s) → Assembler → Object File (x.o)
```
- Converts assembly to machine code (binary)
- Replaces pseudo-instructions with real instructions
- Replaces labels with addresses
- Creates object file with unresolved external references

**Step 3: Linking**
```
Object Files (x.o, y.o) + Libraries → Linker → Executable (a.out)
```
- Resolves external references
- Links multiple object files
- Includes library functions (e.g., printf)
- Produces single executable file

**Step 4: Loading**
```
Executable (a.out) → Loader → Memory → Execution
```
- Loads program into memory
- Allocates and initializes registers
- Handles dynamic linking
- Begins execution

**External References:**
- If x.o uses variable Q defined in y.o, linker finds Q's address in y.o and updates x.o
- If using printf(), linker includes printf's code from standard library

---

## Key Takeaways

1. **Control Flow:** MIPS provides conditional (BEQ, BNE, SLT) and unconditional (J, JR, JAL) branching
2. **Procedure Calls:** Use JAL to call, JR $ra to return; save important values on stack
3. **Register Conventions:** Caller saves $t, $a, $ra; Callee saves $s registers
4. **Stack Management:** Grows downward; decrement $sp to allocate, increment to deallocate
5. **Character Handling:** Use LB/SB for byte operations; strings end with '\0'
6. **Large Constants:** Use LUI + ORI for 32-bit constants
7. **Endianness:** Little-endian (x86) vs Big-endian (MIPS)
8. **Compilation Process:** Compiler → Assembler → Linker → Loader → Execution

---

## Summary

Week 2 deepens understanding of MIPS assembly by introducing control flow mechanisms essential for implementing high-level programming constructs. Students learn how to translate if-statements, loops, and function calls into assembly, manage the stack for nested procedure calls, handle characters and strings efficiently, and understand the compilation pipeline from source code to execution. The material also covers practical topics like dealing with large constants, register saving conventions, and architectural differences between RISC and CISC systems.
