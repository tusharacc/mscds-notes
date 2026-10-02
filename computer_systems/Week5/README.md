# Week 5: Computer Architecture and Pipelining

## Table of Contents
1. [Von Neumann Architecture](#von-neumann-architecture)
2. [Amdahl's Law and Design Principles](#amdahls-law-and-design-principles)
3. [Latches and Clocks](#latches-and-clocks)
4. [Pipelining Concepts](#pipelining-concepts)
5. [5-Stage Pipeline Design](#5-stage-pipeline-design)
6. [Pipeline Hazards and Conflicts](#pipeline-hazards-and-conflicts)

---

## Von Neumann Architecture

### Overview
The Von Neumann architecture, proposed by John von Neumann in 1945, is the foundation of modern computer design. It introduces the concept of **stored-program computers**, where both instructions and data are stored in memory, allowing computers to be reprogrammed for different tasks.

### Fixed vs. Stored-Program Computers
- **Fixed Program Computers**: Designed for specific tasks (e.g., calculators) and cannot be reprogrammed
- **Stored Program Computers**: Can change functionality by loading different programs and data into memory

### Key Components

#### 1. Central Processing Unit (CPU)
The CPU is the "brain" of the computer, responsible for executing program instructions. It consists of:

**Control Unit**
- Controls operations of different computer components
- Provides timing and control signals
- Coordinates when components should perform operations
- Directs data flow between components

**Arithmetic Logic Unit (ALU)**
- Performs arithmetic operations (addition, subtraction, etc.)
- Performs logical operations (AND, OR, NOT)
- Executes mathematical and logical computations

**Registers** (High-speed storage areas)
- **MAR (Memory Address Register)**: Holds the memory location of data to access
- **MDR (Memory Data Register)**: Holds data being transferred to/from memory
- **Accumulator**: Stores intermediate results from ALU operations
- **Program Counter (PC)**: Contains the address of the next instruction to execute
- **CIR (Current Instruction Register)**: Contains the current instruction during processing

#### 2. Buses
Buses connect different components and enable data transmission:
- **Address Bus**: Carries addresses of data (not the data itself)
- **Data Bus**: Carries actual data between processor, memory, and I/O devices
- **Control Bus**: Carries control signals and status signals to coordinate activities

#### 3. Memory Unit
- **Primary Memory (RAM)**: Fast, directly accessible to CPU
- **Secondary Memory**: Slower (e.g., hard disk, SSD)
- Each memory partition has a unique binary address
- Data is loaded from secondary memory to RAM for faster CPU access

#### 4. Input/Output Devices
Components for user interaction and external data exchange.

---

## Amdahl's Law and Design Principles

### Amdahl's Law
**Key Principle**: Performance improvements are limited by the component's contribution to overall system performance.

**Example**:
- Web server: 40% CPU time, 60% I/O time
- Original execution: 100 seconds (40s CPU + 60s I/O)
- With 10x faster CPU: 64 seconds (4s CPU + 60s I/O)
- Improvement: Only 36% reduction despite 10x CPU enhancement
- **Maximum possible improvement**: 40% (limited by CPU's contribution)

**Lesson**: Focus optimization efforts on frequently accessed components and bottlenecks.

### Energy and Power Principles

**Energy Consumption**
- Energy = Power × Time
- Systems consume energy even when idle (energy leakage)
- Example: 100W system executing for 10s = 1000 joules
- With 2x performance (5s execution) = 500 joules
- **Performance improvements reduce energy consumption**

### 90-10 Rule
- **10% of program code accounts for 90% of execution time**
- Focus optimization on frequently visited code segments
- Small portions of code are executed repeatedly in loops

### Principle of Locality

**Temporal Locality**
- If data/code is accessed, it will likely be reused in the near future
- Recently accessed items have high probability of being accessed again

**Spatial Locality**
- If data/code is accessed, nearby data/code will likely be accessed next
- Sequential memory access patterns

---

## Latches and Clocks

### Why Do We Need Clocks?

In a microprocessor, different components (instruction memory, registers, ALU, data memory) operate in sequence. Each circuit may have different processing times, creating coordination challenges.

**Clock Purpose**: Synchronize all circuitry so each unit knows:
- When to accept input (rising edge)
- How much time to execute logic
- When to produce output (end of cycle)

### Clock Cycle Structure
```
Rising Edge → High Voltage → Low Voltage → End of Cycle
     ↑            ↑              ↑              ↑
  Input     Execute Logic   Process Output   Complete
```

### Combinational vs. Sequential Circuits

**Combinational Circuits**
- Output is purely a function of input values
- Example: AND gate
- Output changes when input changes (after logic delay)

**Sequential Circuits**
- Output is a function of input AND internal state
- Requires synchronization across multiple stages
- Instructions flow through different circuitry sequentially

### Latches: The Storage Solution

**Purpose**: Ensure circuit inputs don't change during a clock cycle

**Key Functions**:
- Act as storage devices separating circuits
- Store values and keep them stable for entire cycle
- Update values at rising edge of clock
- Prevent input changes from propagating mid-cycle

**Example**:
```
Latch stores: 8, 6 (at rising edge)
   ↓
Combinational Circuit (e.g., adder)
   ↓
Output: 14 (stored in next latch at next rising edge)
```

### Single-Cycle Design

In single-cycle design, an instruction completes in one clock cycle:

**Execution Flow**:
1. **Rising Edge**: Update Program Counter, write previous result to register file
2. **First Half**: Fetch instruction from memory, read register file
3. **Mid-Cycle**: ALU performs computation
4. **Falling Edge**: Latch ALU output to address register
5. **Second Half**: Access data memory, prepare for register write
6. **Next Rising Edge**: Write result back to register file

**Required Latches**:
- Program Counter latch
- Register file latch (for writing)
- Address register latch (for data memory)

---

## Pipelining Concepts

### Multi-Stage Circuit Design

Instead of executing entire instruction in one cycle, break execution into multiple stages with latches between each stage.

**5 Stages**:
1. **IF (Instruction Fetch)**: Fetch instruction from memory
2. **ID (Instruction Decode)**: Read from register file
3. **EX (Execute)**: ALU operation
4. **MEM (Memory)**: Access data memory
5. **WB (Write Back)**: Write result to register file

**Each stage has one full cycle to complete its operation.**

### Pipelining Analogy: Car Manufacturing

**Unpipelined**:
- One car every 24 hours
- Throughput: 1 car / 24 hours

**Pipelined** (3 teams: Engine, Chassis, Cosmetics):
- Each team takes 8 hours
- Once Team A finishes car 1, passes to Team B, starts car 2
- Throughput: 1 car / 8 hours
- **3x performance improvement**

### Performance Analysis

**Single-Stage Design**:
- One instruction: 1000 picoseconds
- Throughput: 1 billion instructions/second

**3-Stage Pipelined Design**:
- Each stage: ~333 picoseconds
- One instruction still takes ~1000 picoseconds total
- But throughput: 3 billion instructions/second
- **3x throughput improvement**

**Why the Improvement?**
- While I1 is in ALU stage, I2 can start in IM stage
- While I1 is in DM stage, I2 is in ALU, I3 is in IM
- All stages work in parallel on different instructions

### Key Assumptions for Ideal Performance

1. **No instruction dependencies**: Instructions are independent
2. **No latch overhead**: Latches introduce minimal delay
3. **Balanced stages**: Each stage takes roughly equal time

### Reality Check: Overheads and Limits

**Latch Overhead**:
- Each latch adds delay (e.g., 50 picoseconds)
- More stages = more latches = more overhead
- Single instruction may take longer than unpipelined version

**Optimal Pipeline Depth**:
- Performance peaks at 15-25 stages
- Beyond this, latch overhead and dependencies reduce gains
- More stages = higher power consumption

**Performance vs. Stages**:
- Performance gain tapers off with more stages
- Diminishing returns after optimal depth

### Pipeline Metrics Summary

**Changes with Pipelining**:
- Time per instruction: Slightly increases (latch overhead)
- Cycles per instruction: Increases (more smaller cycles)
- Average CPI: Roughly same (1 instruction/cycle at steady state)
- Clock speed: Increases significantly
- Total execution time: Decreases (higher throughput)
- Speedup: Proportional to number of stages (ideal case)

---

## 5-Stage Pipeline Design

### The Five Stages

Each instruction flows through five stages, with each stage taking one cycle:

1. **IF (Instruction Fetch)**: Fetch instruction from instruction memory
2. **ID (Instruction Decode/Register Read)**: Read required registers
3. **EX (Execute)**: ALU performs computation
4. **MEM (Memory Access)**: Load/store operations
5. **WB (Write Back)**: Write result to register file

### Pipeline Operation

**Cycle-by-Cycle Execution**:

```
Cycle 1: I1[IF]
Cycle 2: I1[ID] → I2[IF]
Cycle 3: I1[EX] → I2[ID] → I3[IF]
Cycle 4: I1[MEM] → I2[EX] → I3[ID] → I4[IF]
Cycle 5: I1[WB] → I2[MEM] → I3[EX] → I4[ID] → I5[IF]
```

At Cycle 5, the pipeline is "warmed up" - all stages are actively processing different instructions simultaneously.

### Register Read/Write Timing

**Critical Design Decision**: Register operations take half a cycle each

**Timing Convention**:
- **Write**: First half of cycle
- **Read**: Second half of cycle

**Why This Matters**:

Example: I1 writes to R1, I4 reads from R1
```
Cycle 5: I1 writes R1 (first half) → I4 reads R1 (second half) ✓
```

This allows I4 to get updated value from I1 in the same cycle!

**Dependency Rules**:
- Instructions dependent on I1's result can start at I4 or later
- If instruction starts at I3, it reads stale value (I1 hasn't written yet)
- If full cycle needed for read/write, dependent instruction must wait one more cycle

### Data Memory Bypass

**Bypass Line**: ALU output can skip memory stage for non-memory instructions

**Example - ADD instruction**:
- Cycle 1: IF
- Cycle 2: ID (read registers)
- Cycle 3: EX (perform addition)
- Cycle 4: MEM - **BYPASS** (no memory access needed)
- Cycle 5: WB (write result)

**Why Not Skip to Cycle 4 for WB?**
- Could create register write conflicts
- Maintains pipeline uniformity and predictability
- Instruction stays idle but waits for proper cycle

### Program Counter (PC) Management

**Normal Operation**: PC increments by 4 (32-bit = 4 bytes)
```
PC → PC+4 → PC+8 → PC+12 ...
```

**Branch Instructions**: PC may jump to different location

### Branch Instructions and Pipeline Stalls

**Problem**: Branch decision happens after instruction is fetched

**Scenario 1 - Branch completes in Cycle 2**:
```
Cycle 1: Branch[IF] - Next PC+4 instruction starts
Cycle 2: Branch[ID] - Decision made, but PC+4 already fetched
Result: 1 stall cycle (PC+4 instruction wasted)
```

**Scenario 2 - Branch completes in Cycle 4** (more realistic):
```
Cycle 1: Branch[IF] → PC+4[waiting]
Cycle 2: Branch[ID] → PC+4[IF]
Cycle 3: Branch[EX] → PC+4[ID] → PC+8[IF]
Cycle 4: Branch[MEM] - Decision made!
Result: 3 stall cycles (PC+4, PC+8, PC+12 all wasted)
```

**Stall Cycles = (Branch Decision Cycle - 1)**

### Instruction Examples

#### ADD Instruction: `add r3, r1, r2`
- **IF**: Fetch instruction
- **ID**: Read r1, r2
- **EX**: Compute r1 + r2
- **MEM**: Idle (no memory access)
- **WB**: Write result to r3

#### BRANCH Instruction: `beq r1, r2, offset`
- **IF**: Fetch instruction
- **ID**: Read r1, r2, compare, update PC (complete!)
- **EX**: Idle
- **MEM**: Idle
- **WB**: Idle

#### LOAD Instruction: `lw r6, 8(r3)` (Load Word)
- **IF**: Fetch instruction
- **ID**: Read r3 (base address)
- **EX**: Compute r3 + 8
- **MEM**: Read data from memory[r3+8]
- **WB**: Write data to r6

#### STORE Instruction: `sw r6, 8(r3)` (Store Word)
- **IF**: Fetch instruction
- **ID**: Read r3, r6
- **EX**: Compute r3 + 8
- **MEM**: Write r6 to memory[r3+8]
- **WB**: Not needed (completes in 4 cycles)

---

## Pipeline Hazards and Conflicts

### Overview

Pipeline hazards are situations where the next instruction cannot proceed in the next clock cycle, causing performance degradation.

### Three Types of Hazards

#### 1. Structural Hazards

**Definition**: Different instructions in different stages conflict over the same hardware resource.

**Example Problem**:
- I1 in MEM stage (accessing unified memory for data)
- I4 in IF stage (accessing same memory for instruction)
- **Conflict**: Both need memory access simultaneously

**Solution**: Separate instruction and data memory
- **I-Cache**: Instruction cache/memory
- **D-Cache**: Data cache/memory
- Allows simultaneous access without conflicts

**Alternative**: Multi-port memory (expensive)

#### 2. Data Hazards

**Definition**: An instruction cannot continue because required data hasn't been generated by earlier instruction.

**Example**:
```
I1: add r3, r1, r2    # writes to r3
I2: add r5, r3, r4    # needs r3 from I1
```

**Problem**: I2 needs r3, but I1 hasn't written it yet

**Timing Analysis**:

*If half-cycle read/write*:
```
Cycle 5: I1[WB] writes r3 (first half)
         I4[ID] can read r3 (second half) ✓
```
- Dependent instruction can start 3 cycles after (at I4 position)

*If full-cycle read/write*:
```
Cycle 5: I1[WB] writes r3 (full cycle)
Cycle 6: I5[ID] can read r3 ✓
```
- Dependent instruction must wait 4 cycles (at I5 position)

**Consequence**: Pipeline stalls until data is available

#### 3. Control Hazards

**Definition**: Fetch operation cannot continue because branch outcome is unknown.

**Example**:
```
I1: beq r1, r2, label  # branch instruction
I2: add r3, r4, r5     # next sequential instruction
```

**Problem**: Don't know if I2 should execute until branch decision is made

**Scenarios**:

*Branch taken*:
- Instructions after branch are wrong path
- Must flush pipeline
- Restart from branch target

*Branch not taken*:
- Continue with sequential instructions
- No problem

**Stall Cycles**: Depends on when branch is resolved
- If resolved in ID stage (Cycle 2): 1 stall
- If resolved in EX stage (Cycle 3): 2 stalls
- If resolved in MEM stage (Cycle 4): 3 stalls

### Handling Hazards

**Structural Hazards**: Add more hardware resources
- Separate caches
- Multiple ports
- Dedicated functional units

**Data Hazards**:
- Pipeline stalls (wait for data)
- Forwarding/bypassing (pass data directly between stages)
- Compiler instruction scheduling (reorder independent instructions)

**Control Hazards**:
- Pipeline stalls (wait for branch decision)
- Branch prediction (guess outcome)
- Delayed branches (execute useful instructions after branch)
- Early branch resolution (compute branch in earlier stage)

### Impact on Performance

Hazards reduce the ideal pipeline speedup because:
- Pipeline must stall (insert bubbles)
- Some work is wasted (wrong-path instructions)
- CPI increases above ideal value of 1
- Actual speedup < number of pipeline stages

**Real-world Performance**:
- 5-stage pipeline: ~3-4x speedup (not 5x)
- Hazards prevent achieving theoretical maximum
- More stages = more hazard opportunities

---

## Summary

Week 5 covered the fundamental concepts of computer architecture and pipelining:

1. **Von Neumann Architecture**: The foundational model for modern computers with stored programs, CPU components (ALU, Control Unit, Registers), memory hierarchy, and buses.

2. **Amdahl's Law**: Performance improvements are bounded by the contribution of the enhanced component. Focus optimization on bottlenecks and frequently used components.

3. **Clocks and Latches**: Essential for synchronizing circuit operations. Latches store values between pipeline stages and ensure stable inputs during clock cycles.

4. **Pipelining**: Breaking instruction execution into stages allows multiple instructions to execute simultaneously, significantly improving throughput (3x for 3-stage, ideally 5x for 5-stage).

5. **5-Stage Pipeline**: IF → ID → EX → MEM → WB. Each stage processes different instructions in parallel. Register timing (half-cycle read/write) enables efficient data flow.

6. **Pipeline Hazards**: Structural (resource conflicts), Data (dependencies), and Control (branches) hazards limit ideal performance. Solutions include resource duplication, forwarding, and branch prediction.

Understanding these concepts is crucial for appreciating modern processor design and performance optimization strategies.
