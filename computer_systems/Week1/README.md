# Week 1: Computer Systems - Introduction to Computer Architecture and MIPS

## Table of Contents
1. [Introduction and Motivation](#introduction-and-motivation)
2. [Clocks and Cycles](#clocks-and-cycles)
3. [MIPS Instruction Set Architecture](#mips-instruction-set-architecture)
4. [Operands and Registers](#operands-and-registers)
5. [Memory Addressing](#memory-addressing)
6. [Memory Organization](#memory-organization)

---

## Introduction and Motivation

### Why Study Hardware?

Understanding computer hardware is crucial for several reasons:

1. **Decline of Moore's Law**
   - Moore's Law states that the number of transistors on a chip roughly doubles every 18-24 months
   - Historically, this provided automatic 2x performance improvement every 2 years
   - Today, Moore's Law is declining due to physical limitations
   - Programmers can no longer rely on automatic hardware improvements for performance gains
   - Understanding hardware architecture is essential for optimizing programs

2. **Multi-core Processors**
   - Modern processors are multi-core systems
   - Programmers must split code into multiple threads
   - Each thread runs on a different processor core
   - Requires understanding of hardware to take full advantage

3. **Diverse Platforms**
   - Programs run on PCs, mobile devices, tablets, and cloud infrastructure
   - Each platform has different underlying architecture
   - Understanding hardware enables better performance reasoning across platforms

### Performance Improvements Through Hardware Understanding

**Matrix Vector Multiplication Example** (from Patterson and Hennessy):
- Naive implementation: baseline performance (z)
- Data level parallelism: 3.8x improvement
- Loop unrolling + out-of-order execution: 2.3x additional improvement
- Cache blocking (memory optimization): 2.5x additional improvement
- Thread level parallelism: 14x additional improvement
- **Total improvement: 200x faster than original**

### Historical Performance Trends

**Performance Growth (1970s-2014)**:
- **1970s-2003**: ~50% improvement per year (following Moore's Law)
- **Post-2003**: ~22% improvement per year (declining growth)

**Reasons for Slowdown**:
1. All "low-hanging fruit" optimization techniques had been exhausted
2. Power wall became a limiting factor

### The Power Wall

**Dynamic Power Formula**:
```
Power = Activity × Capacitance × Voltage² × Frequency
```

**Key Points**:
- As transistors became smaller, more could fit on a chip (Moore's Law)
- Smaller transistors = reduced capacitance
- Frequency increased as transistors became faster
- Operating voltage decreased initially
- Power dissipation increased to ~100-150 watts per mm²

**Thermal Challenges**:
- At 100W/mm², heat dissipation became critical
- Simple cooling (heat sink + fan) works up to 150W
- Liquid cooling is expensive and affects overall cost
- Voltage could not be reduced below ~1V
- Frequency growth was stopped to maintain power within safe limits
- Result: Frequency became constant, limiting performance gains

---

## Clocks and Cycles

### What is a Clock?

A **clock** is an oscillating voltage signal that controls all circuitry in a processor.

**Clock Characteristics**:
- Voltage continuously oscillates between high and low states
- One complete cycle: high → low → high
- Clock guides when circuitry performs operations
- All components are synchronized to the clock

### Clock Cycle Operation

**How Circuitry Uses Clocks**:
1. At the beginning of each clock cycle (rising edge), circuitry examines inputs
2. Performs its designated operation
3. Produces output before the next clock cycle begins
4. Each operation must complete within one cycle

**Example: Adder Circuit**:
- If an adder takes 800 picoseconds to complete an operation
- Clock width is set to 800 picoseconds
- Adder completes one operation per clock cycle

### Clock Speed and Performance

**Calculating Operations Per Second**:
```
Clock Speed = 1 / Clock Width
```

**Example**:
- Clock width = 800 picoseconds = 800 × 10⁻¹² seconds
- Clock speed = 1 / (800 × 10⁻¹²) = 1.25 × 10⁹ Hz = 1.25 GHz
- Adder can perform 1.25 billion operations per second (assuming 1 CPI)

### CPI (Cycles Per Instruction)

**Definition**: Number of clock cycles required to complete one instruction

**Scenarios**:
- **CPI = 1**: Operation completes in one cycle (ideal case)
- **CPI > 1**: Operation takes multiple cycles (e.g., waiting for data from memory)
- **CPI < 1**: Possible with parallelism (multiple operations per cycle)

**Setting Clock Width**:
- Clock width is typically set to accommodate the slowest circuitry
- If Circuit A takes 600ps and Circuit B takes 800ps, clock width = 800ps

### CPU Performance Equation

**Basic Performance Formula**:
```
CPU Execution Time = CPU Cycles × Clock Cycle Time
```

Where:
```
Clock Cycle Time = 1 / Clock Speed
```

**Example 1**: Computing Clock Cycles
- Processor: 3 GHz (3 billion cycles/second)
- Program runs for 10 seconds
- Assuming 1 CPI: 3 billion × 10 = 30 billion clock cycles

**Example 2**: Computing Execution Time
- Clock cycles: 2 billion
- Processor: 1.5 GHz
- Execution time = (2 × 10⁹) / (1.5 × 10⁹) = 1.33 seconds

---

## MIPS Instruction Set Architecture

### What is an ISA?

**Instruction Set Architecture (ISA)** is:
- A critical interface between software and hardware
- A set of instructions the processor understands
- A contract between high-level programming languages and underlying hardware

### Types of Instruction Sets

**RISC (Reduced Instruction Set Computer)**:
- Example: MIPS
- Simpler, regular instructions
- Limited number of basic operations
- Hardware-friendly design

**CISC (Complex Instruction Set Computer)**:
- Example: x86
- More complex instructions
- Can perform complicated operations directly

**Other ISAs**: ARM (mobile devices), IBM Power

### ISA Design Principles

1. **Keep Hardware Simple**
   - Hardware only needs to understand primitive operations
   - Complex expressions built from basic operations
   - Simpler hardware = less energy consumption, less circuitry

2. **Keep Instructions Regular**
   - Instructions follow consistent syntax
   - Simplifies decoding and scheduling
   - Makes hardware design easier

### High-Level to Assembly Translation

**Example: C to Assembly**
```c
A = B + C;
```

**Compilation Steps**:
1. **High-level code**: `A = B + C` (programmer-friendly)
2. **Assembly code**: `add A, B, C` (human-readable machine instruction)
3. **Machine code**: `00000000101001000100000000100000` (32-bit binary)

**Assembly Instruction Format**:
- Operation: `add`
- Destination operand: `A`
- Source operands: `B`, `C`

### Complex Expression Evaluation

**Example 1: Multiple Additions**
```c
A = B + C + D + E;
```

**Method 1** (Register-efficient):
```assembly
add A, B, C      # A = B + C
add A, A, D      # A = A + D = B + C + D
add A, A, E      # A = A + E = B + C + D + E
```
- Uses only 4 registers (B, C, D, E) plus A
- More efficient with limited registers

**Method 2** (Using temporary):
```assembly
add A, B, C      # A = B + C
add F, D, E      # F = D + E (temporary)
add A, A, F      # A = A + F = B + C + D + E
```
- Uses 5 registers (B, C, D, E, F) plus A
- Requires additional temporary register F
- Less register-efficient but allows parallel evaluation

### Floating-Point Considerations

**Important**: Floating-point operations are not always associative or commutative.

**Example**:
```c
F = (G + H) - (I + J);
```

**Correct Translation** (respecting parentheses):
```assembly
add T0, G, H     # T0 = G + H
add T1, I, J     # T1 = I + J
sub F, T0, T1    # F = T0 - T1
```

**Alternative** (may produce different results):
```assembly
add F, G, H      # F = G + H
sub F, F, I      # F = F - I
sub F, F, J      # F = F - J
```

Compilers must use parentheses to determine correct evaluation order.

---

## Operands and Registers

### Memory vs. Registers

**Memory**:
- Large storage space (e.g., 8 GB)
- Slower access
- Stores all program variables and data

**Registers**:
- Small, fast storage on the processor
- Limited number (32 registers in MIPS, 8 in x86)
- Processor scratch pad for computations
- 32-bit wide storage locations in MIPS

### Processor-Memory Interaction

**Data Flow**:
1. Processor fetches variable values from memory
2. Loads values into registers
3. Performs operations on register values
4. Stores results back to memory

**Why Registers Are Important**:
- Memory access is expensive (slow)
- Repeatedly accessed variables should stay in registers
- Limited register count requires careful management

### MIPS Register Architecture

**Register Count**: 32 registers

**Register Types** (naming conventions):
- `$S0-$S7`: Saved registers (for variables)
- `$T0-$T9`: Temporary registers (for intermediate results)
- Special register `$0`: Always contains value 0

**Register Width**: 32 bits (1 word = 4 bytes)

### Memory Address Space

**32-bit System Addressing**:
- Address range: 0 to 2³² - 1
- Total addresses: 2³² ≈ 4.29 billion
- Calculation: 2³² = 2¹⁰ × 2¹⁰ × 2¹⁰ × 2² = 1K × 1K × 1K × 4 = 4 GB

**Memory Capacity**:
- If each address points to 1 byte: 4 GB memory
- If each address points to 4 bytes: 16 GB memory
- Modern 64-bit systems support much larger memory

### Load and Store Operations

**Key Concept**: Values must be loaded from memory before operations can be performed.

**Load Word (lw)**:
```assembly
lw $S0, offset($base_register)
```
- Loads a word (4 bytes) from memory into a register
- Uses base address + offset to locate data

**Store Word (sw)**:
```assembly
sw $S0, offset($base_register)
```
- Stores a word from register to memory
- Uses base address + offset to specify location

**Example**: `A = B + C` in assembly
```assembly
lw $S1, 4($T0)       # Load B from memory (offset 4 from base)
lw $S2, 8($T0)       # Load C from memory (offset 8 from base)
add $S0, $S1, $S2    # A = B + C
sw $S0, 0($T0)       # Store A to memory (offset 0 from base)
```

### Immediate Operands

**Add Immediate (addi)**:
```assembly
addi $S0, $S1, 1000
```
- Adds constant value 1000 to register $S1
- Stores result in $S0
- One operand is a constant instead of a register

**Loading Constants**:
```assembly
addi $S0, $0, 1000
```
- Adds 1000 to special register $0 (which always = 0)
- Result: $S0 = 1000
- MIPS requires at least one operand to be a register

### Storage Units

**Bit and Byte Relationships**:
- 8 bits (lowercase b) = 1 Byte (uppercase B)
- 1 word = 32 bits = 4 Bytes
- 1 kilobyte (KB) = 1024 bytes = 2¹⁰ bytes
- 1 megabyte (MB) = 1024 KB = 2²⁰ bytes
- 1 gigabyte (GB) = 1024 MB = 2³⁰ bytes

---

## Memory Addressing

### Compiler Memory Organization

When you declare variables in a program, the compiler must:
1. Allocate space in memory for each variable
2. Track the location of each variable
3. Generate appropriate load/store instructions

### Virtual Memory Address Space

**Virtual Memory**:
- Large, contiguous memory region
- Program thinks it has exclusive access
- Not actual physical memory (handled by OS)
- Typical range: 0 to 64 GB (for example)

### Variable Allocation

**Process**:
1. Compiler starts at base address (e.g., address 0)
2. Allocates space for each variable sequentially
3. Maintains a symbol table with variable offsets

**Example**:
```c
int a, b, c;
int d[10];
```

**Memory Layout**:
| Variable | Offset from Base | Size    |
|----------|------------------|---------|
| a        | 0                | 4 bytes |
| b        | 4                | 4 bytes |
| c        | 8                | 4 bytes |
| d[0-9]   | 12               | 40 bytes|

### Base Address Register

**Convention**: Base address stored in a temporary register (e.g., `$T0`)

All memory accesses calculated relative to base address:
- Variable `a` at offset 0: `$T0 + 0`
- Variable `b` at offset 4: `$T0 + 4`
- Variable `c` at offset 8: `$T0 + 8`
- Array `d[0]` at offset 12: `$T0 + 12`

### Complete Example: A = B + C

**C Code**:
```c
int a, b, c;
a = b + c;
```

**Assembly Translation**:
```assembly
# Assume base address in $T0
lw $S0, 4($T0)       # Load b (offset 4)
lw $S1, 8($T0)       # Load c (offset 8)
add $S2, $S0, $S1    # a = b + c
sw $S2, 0($T0)       # Store a (offset 0)
```

**Explanation**:
1. Load word at `$T0 + 4` (variable b) into `$S0`
2. Load word at `$T0 + 8` (variable c) into `$S1`
3. Add `$S0` and `$S1`, store result in `$S2`
4. Store `$S2` at `$T0 + 0` (variable a)

### Array Access

**Example**: Accessing `d[2]`
```assembly
# d[0] is at offset 12, d[2] is at offset 12 + (2 × 4) = 20
lw $S0, 20($T0)      # Load d[2]
```

**General Formula**:
```
Address of d[i] = base_address + offset_d + (i × element_size)
```

---

## Memory Organization

### Memory Regions for a Program

A program's virtual memory is organized into distinct regions:

```
High Address (64 GB)
│
├─────────────────────┐
│   Stack (grows ↓)   │ Local variables, function calls
├─────────────────────┤
│                     │ (Free space)
├─────────────────────┤
│   Heap (grows ↑)    │ Dynamically allocated data (malloc)
├─────────────────────┤
│   Global Data       │ Global variables
├─────────────────────┤
│   Text (Code)       │ Program instructions
└─────────────────────┘
Low Address (0)
```

### 1. Text Segment (Code)

**Purpose**: Stores program instructions

**Example**:
- 400 instructions × 4 bytes/instruction = 1600 bytes
- Located at addresses 0-1599

### 2. Global Data Region

**Purpose**: Stores global variables

**Global Pointer ($GP)**:
- Special register pointing to start of global data
- Calculated as: size of text segment
- Example: If text = 1600 bytes, $GP = 1600

**Example**:
```c
int a, b, c;  // Global variables
```

**Memory Layout**:
| Variable | Address Range | Offset from $GP |
|----------|---------------|-----------------|
| a        | 1600-1603     | 0               |
| b        | 1604-1607     | 4               |
| c        | 1608-1611     | 8               |

**Assembly Code for Global Variables**:
```assembly
# Initialize global pointer
addi $GP, $0, 1000    # $GP = base of global region

# A = B + C (global variables)
lw $S2, 4($GP)        # Load B (offset 4)
lw $S3, 8($GP)        # Load C (offset 8)
add $S1, $S2, $S3     # A = B + C
sw $S1, 0($GP)        # Store A (offset 0)
```

### 3. Stack Region

**Purpose**: Stores local variables and function call information

**Stack Pointer ($SP)**:
- Points to the top of the stack (current end)
- Stack grows from high to low addresses
- Decremented to allocate space (grow stack)
- Incremented to deallocate space (shrink stack)

**Frame Pointer ($FP)**:
- Points to the start of current function's activation record
- Helps access local variables and parameters

### Activation Records

**Definition**: Memory space allocated for a function when called

**Contents of Activation Record**:
- Local variables
- Function parameters
- Return address
- Saved register values

**Stack Growth**:
```
High Address
│
├─────────────────┐
│   main()        │ ← $FP points here
│   (local vars)  │
├─────────────────┤ ← $SP points here
│   function2()   │
│   (local vars)  │
├─────────────────┤
│   function3()   │
│   (local vars)  │
└─────────────────┘ ← $SP moves down as stack grows
```

**Stack Operations**:
- **Function Call**: Allocate new activation record (decrement $SP)
- **Function Return**: Deallocate activation record (increment $SP)

### 4. Heap Region

**Purpose**: Stores dynamically allocated memory

**Characteristics**:
- Grows from low to high addresses (opposite of stack)
- Managed by programmer (malloc, free in C)
- Used for data structures with dynamic size

**Example**:
```c
int *array = (int *)malloc(100 * sizeof(int));
```
- Memory allocated in heap
- Pointer `array` stored on stack (if local) or global region (if global)

### Complete Example: Global Array Access

**C Code**:
```c
int a, b, c;
int d[10];  // Global array

// Example operation
d[3] = d[2] + a;
```

**Memory Layout**:
| Item  | Offset from $GP | Size      |
|-------|-----------------|-----------|
| a     | 0               | 4 bytes   |
| b     | 4               | 4 bytes   |
| c     | 8               | 4 bytes   |
| d[0]  | 12              | 4 bytes   |
| d[1]  | 16              | 4 bytes   |
| d[2]  | 20              | 4 bytes   |
| d[3]  | 24              | 4 bytes   |
| ...   | ...             | ...       |

**Assembly Code**:
```assembly
# Set up pointer to d[0]
addi $S4, $GP, 12     # $S4 = address of d[0]

# d[3] = d[2] + a
lw $T0, 8($S4)        # Load d[2] (offset 8 from d[0])
lw $S1, 0($GP)        # Load a (stored in $S1 earlier or load from GP)
add $T0, $T0, $S1     # d[3] = d[2] + a
sw $T0, 12($S4)       # Store to d[3] (offset 12 from d[0])
```

### Number Systems Review

**Decimal (Base 10)**:
- Digits: 0-9
- Example: 35₁₀ = 3×10¹ + 5×10⁰ = 30 + 5

**Binary (Base 2)**:
- Digits: 0, 1
- Example: 100011₂ = 1×2⁵ + 0×2⁴ + 0×2³ + 0×2² + 1×2¹ + 1×2⁰ = 32 + 2 + 1 = 35₁₀

**Hexadecimal (Base 16)**:
- Digits: 0-9, A-F (where A=10, B=11, C=12, D=13, E=14, F=15)
- Notation: 0x prefix (e.g., 0x23)
- Example: 0x23 = 2×16¹ + 3×16⁰ = 32 + 3 = 35₁₀

**Conversion Table**:
| Decimal | Binary | Hexadecimal |
|---------|--------|-------------|
| 0       | 0000   | 0x0         |
| 1       | 0001   | 0x1         |
| 10      | 1010   | 0xA         |
| 15      | 1111   | 0xF         |
| 35      | 100011 | 0x23        |

---

## Key Takeaways

1. **Hardware Understanding is Critical**: With Moore's Law declining, programmers must understand hardware to optimize performance

2. **Clocks Synchronize Everything**: All processor operations are synchronized to clock cycles; performance depends on clock speed and CPI

3. **ISA Bridges Software and Hardware**: MIPS provides a simple, regular instruction set that makes hardware design efficient

4. **Registers Are Scarce**: Only 32 registers in MIPS; careful management is essential for performance

5. **Memory is Hierarchical**: Fast registers on chip, slower main memory off chip; frequent data should stay in registers

6. **Virtual Memory Provides Abstraction**: Programs work with virtual addresses; OS manages actual physical memory

7. **Compiler Manages Memory**: Compiler allocates variables, maintains symbol tables, and generates appropriate load/store instructions

8. **Stack and Heap Grow Oppositely**: Stack (local data) grows downward, heap (dynamic data) grows upward, preventing collision

---

## Additional Resources

- **Textbook**: "Computer Organization and Design: The Hardware/Software Interface" by Patterson and Hennessy
- **MIPS ISA**: Study the complete MIPS instruction set for more operations
- **Practice**: Convert simple C programs to MIPS assembly to reinforce concepts

---

*These notes cover the foundational concepts of computer systems architecture, focusing on the MIPS instruction set as a teaching tool for understanding how software interfaces with hardware.*
