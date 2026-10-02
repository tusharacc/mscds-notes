# Week 7: Advanced Processor Optimization Techniques

## Table of Contents
1. [Branch Predictors](#branch-predictors)
2. [Bimodal Predictor](#bimodal-predictor)
3. [Out-of-Order Execution](#out-of-order-execution)
4. [Out-of-Order Execution Example](#out-of-order-execution-example)
5. [Cache Hierarchy](#cache-hierarchy)

---

## Branch Predictors

### Overview
Branch predictors are hardware modules designed to predict whether a branch instruction will be taken or not taken, helping to minimize pipeline stalls caused by control hazards.

### Control Hazard Handling Strategies

There are four main approaches to handling control hazards:

1. **Stall (Panic Approach)**
   - Introduce a stall cycle when a branching decision is happening
   - No useful work is done during the stall

2. **Assume Branch Not Taken**
   - Fetch the next instruction in program sequence (PC + 4)
   - If branch is actually taken, hardware must cancel the wrong path instruction

3. **Compiler-Assisted Approach**
   - Compiler fills the branch delay slot with an independent instruction
   - Move an instruction from before the branch into the delay slot
   - Execute something meaningful while the decision is being made
   - Ensure program state is preserved if prediction is wrong

4. **Hardware-Assisted Approach (Branch Prediction)**
   - Hardware predicts the direction a branch will take
   - Uses historical data and sophisticated algorithms
   - Modern branch predictors achieve ~95-96% accuracy

### How Branch Predictors Work

In a pipeline without branch prediction:
- **Cycle 1**: Fetch branch instruction, PC points to next instruction (PC + 4)
- **Cycle 2**: Branch resolved, next instruction fetched
- If branch taken: Must cancel fetched instruction and fetch from branch target

With branch prediction:
- Replace simple PC + 4 logic with a branch predictor module
- Predictor uses history to guess whether branch will be taken
- Fetch appropriate instruction based on prediction
- Only ~4-5% of predictions are wrong (resulting in wasted cycles)

### Branch Predictor Evolution
- Designed originally in the 1980s and early 1990s
- Modern predictors achieve 95-96% accuracy
- Only about 4% of the time will a wrong prediction occur
- Wrong predictions result in stall cycles or wasted work

---

## Bimodal Predictor

### Basic Concept

A bimodal predictor uses **saturating counters** to track branch behavior and make predictions.

### Saturating Counters

**Definition**: A 2-bit counter that can only change values until it reaches extreme ends.

**Possible Values** (for 2-bit counter):
- 00 (0)
- 01 (1)
- 10 (2)
- 11 (3)

**Behavior**:
- **Increment**: 00 → 01 → 10 → 11 → 11 (saturates at 11)
- **Decrement**: 11 → 10 → 01 → 00 → 00 (saturates at 00)

### Counter Update Rules

- **Branch Taken**: Increment counter by 1
- **Branch Not Taken**: Decrement counter by 1

### Prediction Logic

Based on counter value:

| Counter Value | State | Prediction |
|--------------|-------|------------|
| 11 | Strongly biased toward taken | Taken |
| 10 | Weakly biased toward taken | Taken |
| 01 | Weakly biased toward not taken | Not Taken |
| 00 | Strongly biased toward not taken | Not Taken |

### Simple Example (4 Branches)

```
Branch 1: Counter = 11 → Predict: Taken (fetch from branch target)
Branch 2: Counter = 00 → Predict: Not Taken (fetch PC + 4)
Branch 3: Counter = 10 → Predict: Taken (weakly biased)
Branch 4: Counter = 01 → Predict: Not Taken (weakly biased)
```

### Generalized Branch Predictor

**Implementation Details**:
- Table with 16,000 entries (16K = 2^14 entries)
- Each entry is a 2-bit saturating counter
- Can accommodate up to 2^14 branches in a program

**Addressing Challenge**:
- PC is 32 bits, but we only need 14 bits to index into the table
- Use subset of PC bits to identify which counter to use
- **Problem**: Different branches may map to the same counter (collision)

### Advanced Prediction Techniques

To improve uniqueness and reduce collisions:

1. **History-Based Prediction**
   - **Global History**: Combine branch PC with history of 14 neighboring branches
   - **Local History**: Combine branch PC with last 14 visits to the same branch
   - Use XOR operation to combine PC with history (14-bit XOR 14-bit = 14-bit)

2. **Tournament Predictor**
   - Meta-predictor that predicts which prediction strategy works best
   - Chooses between:
     - Simple branch PC only
     - Branch PC + neighboring branch history
     - Branch PC + local branch history

### Context Switching Behavior

**Question**: What happens when program P1 switches to program P2?

**Two Approaches**:

1. **Save and Restore** (Not Used)
   - Save all counter values to memory
   - Initialize counters for P2
   - Restore when switching back
   - **Problem**: Too costly, requires moving large amounts of data

2. **Leave As-Is** (Actual Approach)
   - Counters remain unchanged during context switch
   - P1's trained values become initialization for P2
   - P2 must retrain counters based on its own execution
   - **Advantage**: No data movement overhead
   - **Trade-off**: Initial predictions for P2 may be less accurate

---

## Out-of-Order Execution

### Motivation

**In-Order Execution Limitation**:
- Instructions must execute in program order
- If instruction I1 is stalled at stage 2, instruction I2 cannot proceed even if independent
- Resources may be idle while waiting for dependencies

**Out-of-Order Execution Benefit**:
- Independent instructions can overtake stalled instructions
- Better hardware utilization
- Improved performance through parallelism

### Prerequisites for Out-of-Order Execution

**Multiple Execution Units** in parallel:
- Integer Adder (1 cycle)
- Floating Point Adder (4 cycles)
- Multiplier (7 cycles)
- Divider (25 cycles)

Different operations take different amounts of time, creating opportunities for parallel execution.

### Example Scenario

```
I1: DIV $1, $2, $3    ; Takes 25 cycles
I2: ADD $4, $5, $6    ; Takes 1 cycle, independent of I1
```

**Execution Flow**:
- **Cycle 1**: I1 enters IF stage
- **Cycle 2**: I1 in DR, I2 enters IF
- **Cycle 3**: I1 enters divider, I2 in DR
- **Cycle 4**: I1 in divider, I2 enters adder
- **Cycle 5**: I1 still in divider, I2 completes!

**Problem**: I2 finishes before I1, but we can't commit out of order!

### Three-Phase Execution Model

1. **In-Order Issue**: Instructions enter pipeline in program order
2. **Out-of-Order Completion**: Instructions may finish in any order
3. **In-Order Commit**: Results written to registers in program order

### Why In-Order Commit is Required

1. **Debugging and Program Understanding**
   - Programmers expect registers to change in program order
   - Makes debugging possible and predictable

2. **Dependency Management**
   - Later instructions may depend on earlier ones
   - Out-of-order commits could violate data dependencies

3. **Branch Misprediction Recovery**
   - If branch prediction is wrong, must roll back changes
   - Permanent register changes can't be undone
   - Need to preserve old values for the correct path

### Out-of-Order Processor Architecture

#### Key Components

1. **Branch Prediction and Instruction Fetch**
   - Predicts branch direction
   - Fetches instructions speculatively
   - Fills instruction fetch queue with up to 5 instructions

2. **Instruction Fetch Queue**
   - Stores fetched instructions
   - Runs ahead of program execution
   - Size limited by hardware (e.g., 5 instructions)
   - Optimizes fetch time

3. **Decode and Rename Stage**
   - Decodes instructions
   - **Renames** destination registers to temporary locations
   - Places instructions in both:
     - **Issue Queue**
     - **Reorder Buffer (ROB)**

4. **Issue Queue**
   - Holds instructions waiting to execute
   - Checks which instructions are ready (operands available)
   - Dispatches ready instructions to available ALU units
   - Can dispatch multiple instructions per cycle (superscalar)

5. **Reorder Buffer (ROB)**
   - Stores instructions in program order
   - Each entry has a temporary location (e.g., T1, T2, T3, ...)
   - Receives results from ALU units
   - Commits results to registers in program order
   - Separate from the 32 architectural registers

6. **ALU Units** (Multiple in Parallel)
   - Execute instructions
   - Write results to ROB (not directly to registers)
   - Broadcast completion to Issue Queue

### Register Renaming Example

```
Original Program:
I1: ADD $1, $2, $3    ; $1 = $2 + $3
I2: SUB $4, $1, $5    ; $4 = $1 - $5

After Renaming:
I1: ADD T1, $2, $3    ; T1 = $2 + $3
I2: SUB T2, T1, $5    ; T2 = T1 - $5
```

**Process**:
1. I1 writes result to T1 in ROB (not $1 directly)
2. I2 reads from T1 (renamed from $1)
3. I2 writes result to T2 in ROB
4. When I1 ready to commit: T1 → $1
5. When I2 ready to commit: T2 → $4

### Broadcast and Wake-up Mechanism

When an instruction completes in ALU:
1. Write result to ROB entry
2. **Broadcast** completion to Issue Queue
3. Issue Queue scans for dependent instructions
4. Wake up and dispatch newly ready instructions

### Branch Misprediction Handling

If branch prediction is wrong:
1. All speculatively executed work must be discarded
2. Flush instruction fetch queue
3. Flush issue queue
4. Clear ROB entries for wrong-path instructions
5. Restart fetch from correct path

**Cost**: Wasted cycles and energy consumption

### Performance vs. Power Trade-off

**Advantages**:
- Better performance through parallel execution
- Higher instruction throughput

**Disadvantages**:
- More complex circuitry
- Higher power consumption
- Energy wasted on mispredictions and cancellations
- More hardware resources required

---

## Out-of-Order Execution Example

### Background: Bypassing Review

**Pipeline Stages**: IF → DR → ALU → DM → RW

**ADD followed by ADD**:
- Point of Production: End of ALU stage (Cycle 3)
- Point of Consumption: Start of ALU stage (Cycle 3)
- **No stall required**: Result can be bypassed directly

**LOAD followed by ADD**:
- Point of Production: End of DM stage (Cycle 4)
- Point of Consumption: Start of ALU stage (Cycle 3)
- **1 stall cycle required**: ADD must wait for LOAD to complete

### Example Program (8 Instructions)

```
I1: ADD R1, R2, R3      ; R1 = R2 + R3
I2: ADD R4, R1, R5      ; R4 = R1 + R5  (depends on I1)
I3: ADD R5, R4, R6      ; R5 = R4 + R6  (depends on I2)
I4: ADD R7, R5, R8      ; R7 = R5 + R8  (depends on I3)
I5: LW  R4, 0(R9)       ; R4 = MEM[R9]  (independent)
I6: ADD R8, R4, R10     ; R8 = R4 + R10 (depends on I5)
I7: LW  R10, 4(R11)     ; R10 = MEM[R11+4] (independent)
I8: ADD R12, R10, R13   ; R12 = R10 + R13 (depends on I7)
```

**Dependencies**:
- Chain 1: I1 → I2 → I3 → I4
- Chain 2: I5 → I6
- Chain 3: I7 → I8
- I5 and I7 are independent of early instructions

### In-Order Execution Performance

**Execution Timeline**:

```
Cycle | Instruction Completing
------|----------------------
  5   | I1 (ADD)
  6   | I2 (ADD) - no stall
  7   | I3 (LW) - no stall
  8   | (stall) - LW followed by ADD
  9   | I4 (ADD)
 10   | I5 (ADD)
 11   | I6 (LW)
 12   | (stall) - LW followed by ADD
 13   | I7 (ADD)
 14   | I8 (ADD)
```

**Performance Calculation**:
- Total cycles: 14
- Warm-up cycles: 4
- Useful work: 14 - 4 = 10 cycles
- CPI: 10/8 = **1.25 cycles per instruction**
- **Best possible in-order CPI**: 1.0 (one instruction per cycle)

**Stalls**: 2 stalls introduced (cycles 8 and 12)

### Out-of-Order Execution Performance

**Key Insight**: I5 and I7 only depend on I2 (R4 produced in I2)

**Execution Timeline**:

```
Cycle | Instructions Completing
------|------------------------
  5   | I1 (ADD)
  6   | I2 (ADD)
  7   | I3 (ADD), I5 (LW), I7 (LW) - parallel execution!
  8   | (stall) - waiting for I3
  9   | I4 (ADD)
 10   | I6 (ADD), I8 (ADD) - parallel execution!
```

**Parallel Execution**:
- **Cycle 7**: I3, I5, and I7 can all execute in parallel (sufficient hardware)
- **Cycle 10**: I6 and I8 can execute in parallel

**Performance Calculation**:
- Total cycles: 10
- Warm-up cycles: 4
- Useful work: 10 - 4 = 6 cycles
- CPI: 6/8 = **0.75 cycles per instruction**

**Improvement**:
- In-order: 1.25 CPI
- Out-of-order: 0.75 CPI
- **Better than 1.0 CPI** through superscalar execution

### Further Optimization Potential

With even more hardware resources:
- Eliminate remaining stalls
- Could achieve: 0.5 CPI
- Trade-off: More hardware cost and power consumption

### Key Takeaways

1. **Superscalar Execution**: Multiple instructions complete per cycle
2. **Issue Queue Intelligence**: Identifies independent instructions
3. **Hardware Requirements**: Need multiple ALU units for parallel execution
4. **Performance Gain**: 40% improvement (1.25 → 0.75 CPI)
5. **ROB Ensures Correctness**: Results commit in program order despite out-of-order completion

### Signaling and Communication

**Broadcast Mechanism**:
- When I1 finishes, broadcasts completion to Issue Queue
- Issue Queue scans for instructions waiting on I1
- Dependent instructions can now be dispatched
- Multiple instructions may wake up simultaneously

**Example**:
- I2 waits for T1 (result of I1)
- I1 completes → broadcasts "T1 ready"
- Issue Queue dispatches I2 to ALU

---

## Cache Hierarchy

### Motivation

All previous optimizations (pipelining, bypassing, out-of-order execution) are **wasted** if memory access is slow.

**Problem**: Memory access can take hundreds of cycles, negating all performance improvements.

**Solution**: Cache hierarchy provides fast access to frequently used data.

### Memory System Architecture

**Components**:

1. **Processor Core** (on-chip)
   - Contains all pipeline stages
   - Registers, ALU, control logic

2. **DIMM (Dual Inline Memory Module)** (off-chip)
   - High density, low cost
   - Large capacity (e.g., 16 GB)
   - **Slow access**: ~300 cycles
   - Multiple memory chips on dedicated module

**Bandwidth Limitation**: Communication between processor and DIMM is limited

### Cache Hierarchy Levels

```
CPU → Registers → L1 Cache → L2 Cache → L3 Cache → Main Memory → Swap (Disk/SSD)
```

#### Detailed Breakdown

| Level | Size | Access Time | Location | Characteristics |
|-------|------|-------------|----------|-----------------|
| **Registers** | 32-64 bytes | 1 cycle | On-chip | Smallest, fastest |
| **L1 Cache** | 32 KB | 1-2 cycles | On-chip | Small, very fast |
| **L2 Cache** | 256 KB - 2 MB | ~10 cycles | On-chip | Medium size |
| **L3 Cache** | 4-16 MB | ~30 cycles | On-chip | Larger, shared |
| **Main Memory (DRAM)** | 8-64 GB | ~300 cycles | Off-chip (DIMM) | Large, slower |
| **SSD/Flash** | 512 GB - 1 TB | Microseconds | Off-chip | Very large |
| **Hard Disk** | 1-10 TB | Milliseconds (millions of cycles) | Off-chip | Largest, slowest |

**Volatility**:
- Registers, Caches, DRAM: **Volatile** (data lost when powered off)
- SSD, Hard Disk: **Non-volatile** (data persists)

### Cache Design Principles

#### 1. Temporal Locality

**Principle**: If you access data recently, you're likely to access it again soon.

**Cache Strategy**:
- Store recently accessed data in cache
- Keep it available for future accesses
- Exploit reuse patterns in programs

**Example**:
```c
for (int i = 0; i < 1000; i++) {
    sum += array[i];  // 'sum' accessed repeatedly
}
```

#### 2. Spatial Locality

**Principle**: If you access data at address A, you're likely to access data at nearby addresses (A+1, A+2, etc.).

**Cache Strategy**:
- Don't fetch just the requested 4 bytes
- Fetch an entire **cache line** (32-64 bytes)
- Bring neighboring data preemptively

**Example**:
```c
for (int i = 0; i < 100; i++) {
    sum += array[i];  // Access array[0], array[1], array[2], ...
}
```

**Block Fetching**:
- Memory access takes 300 cycles
- Instead of fetching 4 bytes, fetch 64 bytes
- Same 300-cycle cost, but 16x more data
- Future accesses to neighboring addresses are cache hits

### Cache Performance Example

#### Without Cache

```
Access time per instruction: 300 cycles
100 instructions: 30,000 cycles
```

#### With L1 Cache (32 KB, 95% hit rate)

**Calculation**:
- **95% of accesses**: Hit in L1 → 1 cycle
- **5% of accesses**: Miss in L1 → 1 cycle (check) + 300 cycles (fetch from memory) = 301 cycles

**Average Access Time**:
```
Average = (0.95 × 1) + (0.05 × 301)
        = 0.95 + 15.05
        = 16 cycles
```

**Improvement**: 300 cycles → 16 cycles (**18.75x speedup**)

#### With Multi-Level Cache

Adding L2 cache (2 MB, 99% hit rate for L1 misses):
- 95% hit in L1: 1 cycle
- 4.95% hit in L2: 1 + 10 = 11 cycles
- 0.05% miss in both: 1 + 10 + 300 = 311 cycles

**Average**: ~1.5 cycles (massive improvement!)

### Design Trade-offs

**Adding More Cache Levels**:

**Pros**:
- Better performance
- Fewer memory accesses
- Lower average latency

**Cons**:
- Limited on-chip area
- More cache = less space for other components (e.g., more cores)
- Diminishing returns beyond certain point
- Higher cost and complexity

**Design Decision**: Balance between cache size and number of cores

### Modern Cache Hierarchy

**Typical Modern Processor**:
- **L1**: 32 KB instruction + 32 KB data (per core)
- **L2**: 256 KB - 1 MB (per core)
- **L3**: 4-32 MB (shared across cores)
- **L4**: Optional, 128 MB (some high-end processors)

**Evolution**:
- Deeper hierarchies (L3, L4, even L5 in some systems)
- Larger cache sizes over time
- Better replacement policies and prefetching algorithms

### Cache Hierarchy Impact on Performance

**Key Points**:
1. Memory latency can dominate execution time
2. Cache hit rate is critical for performance
3. Each cache level serves as a buffer against slower memory
4. Temporal and spatial locality are fundamental to cache effectiveness
5. Cache design is a balance of size, speed, and cost

---

## Summary

Week 7 covered three major processor optimization techniques:

### 1. Branch Prediction
- Achieves 95-96% accuracy in modern processors
- Uses saturating counters and history-based prediction
- Critical for avoiding pipeline stalls on control hazards
- Tournament predictors combine multiple strategies

### 2. Out-of-Order Execution
- Enables parallel execution of independent instructions
- Three-phase model: in-order issue, out-of-order completion, in-order commit
- Requires sophisticated hardware: ROB, issue queue, register renaming
- Can achieve CPI < 1.0 through superscalar execution
- Trade-off: higher performance but increased power consumption

### 3. Cache Hierarchy
- Multiple levels of progressively larger, slower caches
- Exploits temporal and spatial locality
- Can reduce average memory access time from 300 cycles to <2 cycles
- Critical for realizing benefits of other optimizations
- Design trade-offs between cache size and number of cores

**Overall Impact**: These techniques work together to deliver the high performance of modern processors, enabling complex applications and multi-tasking while managing power consumption and hardware costs.
