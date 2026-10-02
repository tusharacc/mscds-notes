# Computer Systems - Week 6: Pipelining Hazards

## Overview

Week 6 focuses on the detailed study of pipelining hazards in computer architecture, specifically data hazards and control hazards. Building upon the five-stage pipeline design from previous lectures, this week explores how these hazards impact performance and various techniques to mitigate them.

---

## Table of Contents

1. [Introduction to Pipelining Hazards](#introduction-to-pipelining-hazards)
2. [Data Hazards](#data-hazards)
3. [Bypassing (Forwarding)](#bypassing-forwarding)
4. [Data Hazard Examples](#data-hazard-examples)
5. [Control Hazards](#control-hazards)
6. [Control Hazard Mitigation Techniques](#control-hazard-mitigation-techniques)

---

## Introduction to Pipelining Hazards

### Five-Stage Pipeline Recap

The standard five-stage pipeline consists of:

1. **IF (Instruction Fetch)**: Fetch instruction from instruction memory
2. **DR (Decode/Register Read)**: Decode instruction and read register operands
3. **ALU (Execute)**: Perform arithmetic or logical operations
4. **DM (Data Memory)**: Access data memory (for load/store instructions)
5. **RW (Register Write)**: Write results back to registers

**Key Assumptions:**
- Register read happens in the second half of a cycle
- Register write happens in the first half of a cycle
- Instructions flow through the pipeline like water through a pipe
- Each stage is separated by latches (L2, L3, L4, L5)

### Types of Hazards

1. **Structural Hazards**: Multiple instructions competing for the same hardware resource
   - Solution: Add more hardware (e.g., separate instruction and data memory)

2. **Data Hazards**: An instruction depends on data from a previous instruction that hasn't completed yet
   - More complex to handle, requires stalling or bypassing

3. **Control Hazards**: The pipeline doesn't know which instruction to fetch next due to branches/jumps
   - Requires special handling techniques

---

## Data Hazards

### Definition

A data hazard occurs when an instruction cannot continue because a value it needs is not yet produced by an earlier instruction.

### Key Concepts

**Producer and Consumer:**
- **Producer**: Instruction that generates/writes a value to a register
- **Consumer**: Instruction that reads/uses that value from a register

**Example:**
```assembly
I1: ADD $3, $1, $2    # Producer of $3
I2: SUB $5, $3, $4    # Consumer of $3
```

### Point of Production (POP) and Point of Consumption (POC)

- **POP**: The earliest point in the pipeline where a value becomes available
- **POC**: The point where an instruction needs to consume/use that value

**Critical Rule**: POC must occur AFTER POP for correct execution

### Without Bypassing

When no bypassing is available:
- Values are exchanged between instructions only through registers
- Consumer must wait until producer completes the register write stage
- This leads to pipeline stalls (bubbles)

**Example Execution:**

```
Cycle:  1    2    3    4    5    6    7    8    9
I1:    IF   DR   ALU  DM   RW
I2:         IF   DR   DR   DR   ALU  DM   RW
I3:              IF   IF   IF   DR   ALU  DM   RW
```

**Analysis:**
- I1 produces $3 in cycle 5 (first half)
- I2 can only read $3 in cycle 5 (second half)
- I2 stalls in DR stage for 3 cycles total (2 extra cycles = 2 stalls)
- I3 must wait for I2 to vacate DR stage
- **CPI (Cycles Per Instruction)**: ~1.66 (instead of ideal 1.0)

---

## Bypassing (Forwarding)

### Concept

Instead of waiting for a value to be written to a register and then read back, bypass the value directly from where it's produced in the pipeline to where it's needed.

### Key Insight

Values are available in pipeline latches (L3, L4, L5) before being written to registers. We can route these values directly to subsequent instructions using multiplexers.

### How Bypassing Works

1. **Identify POP**: Determine where the producer makes the value available
2. **Identify POC**: Determine where the consumer needs the value
3. **Route value**: If POP occurs before POC, bypass directly from the appropriate latch

### Bypassing Rules

For an ALU instruction consuming values:

- **Value from immediate previous instruction**: Bypass from L4
- **Value from 2 instructions back**: Bypass from L5
- **Value from 3+ instructions back**: Read from register (via L3) - value already written

### Example with Bypassing

```
Cycle:  1    2    3    4    5    6    7
I1:    IF   DR   ALU  DM   RW
I2:         IF   DR   ALU  DM   RW
I3:              IF   DR   ALU  DM   RW
```

**Benefits:**
- No stalls!
- I2 gets $3 directly from L4 at cycle 4
- I3 gets $3 directly from L5 at cycle 5
- **CPI**: 1.0 (ideal)

### ALU with Multiplexers

To support bypassing, the ALU must have multiplexers on its inputs that can select from:
- L3 (normal register read)
- L4 (bypass from previous instruction)
- L5 (bypass from 2 instructions back)

---

## Data Hazard Examples

### Example 0: Basic ADD-ADD Dependency

```assembly
ADD $1, $2, $3    # I1: produces $1
ADD $5, $1, $4    # I2: consumes $1
```

**Without Bypassing:**
- POP: End of cycle 5 (RW stage)
- POC: Beginning of cycle 5 (ALU stage) - cannot proceed
- Stalls: 2 cycles

**With Bypassing:**
- POP: End of cycle 3 (ALU stage)
- POC: Beginning of cycle 4 (ALU stage)
- Stalls: 0 cycles

### Example 1: ADD followed by LOAD

```assembly
ADD $1, $2, $3         # I1: produces $1
LW $4, 8($1)          # I2: consumes $1 (as base address)
```

**Without Bypassing:**
- POP: End of cycle 5 (RW stage)
- POC: Middle of cycle 5 (DR stage) for reading
- Stalls: 2 cycles

**With Bypassing:**
- POP: End of cycle 3 (ALU stage)
- POC: Beginning of cycle 4 (ALU stage - computes $1+8)
- Stalls: 0 cycles
- **Note**: For LOAD, the address calculation happens in ALU stage

### Example 2: LOAD-LOAD Dependency

```assembly
LW $1, 8($2)          # I1: produces $1
LW $4, 8($1)          # I2: consumes $1
```

**Analysis:**
- I1's POP: End of DM stage (cycle 4) - L5
- I2's POC: Beginning of ALU stage - must calculate $1+8
- Even with bypassing, I2 must stall 1 cycle to align ALU after I1's DM

**Without Bypassing:**
- Stalls: 2 cycles

**With Bypassing:**
- Stalls: 1 cycle (can bypass from L5)

### Example 3: LOAD-STORE Dependency

```assembly
LW $1, 8($2)          # I1: produces $1
SW $1, 8($3)          # I2: consumes $1 (value to store)
```

**Case 1: Dependency on loaded value ($1)**
- POP: End of DM stage (L5)
- POC: DM stage of I2 (when value is written to memory)
- With bypassing: 0 stalls (bypass from L5 to DM)

**Case 2: If changed to LW $3, 8($2) and SW $1, 8($3)**
- Dependency on address register ($3)
- POP: End of DM stage (L5)
- POC: ALU stage of I2 (computes $3+8)
- With bypassing: 1 stall (must wait for value in L5)

### Example 4: Variable Pipeline Stages

Consider a pipeline with:
- 2 IF stages
- 2 Decode stages
- 1 Register Read stage
- 1 ALU stage
- 2 DM stages (for LOAD)
- 1 RW stage

**ADD instruction**: 7 stages (skips DM)
**LOAD instruction**: 9 stages (includes 2 DM stages)

```assembly
LW $1, 8($2)          # I1: 9 stages
ADD $4, $1, $3        # I2: 7 stages, consumes $1
```

**Without Bypassing:**
- I1 completes RW at cycle 9
- I2 must read in cycle 9
- I2 stalls in decode: 6 decode cycles instead of 2
- Stalls: 4 cycles

**With Bypassing:**
- I1's POP: End of DM stage (cycle 7)
- I2's POC: ALU stage
- Align I2's ALU after I1's DM
- I2 stalls in decode: 4 decode cycles instead of 2
- Stalls: 2 cycles

---

## Control Hazards

### Definition

Control hazards occur when the pipeline must decide which instruction to fetch next, but the decision depends on a branch or jump instruction that hasn't been fully evaluated yet.

### The Problem

In a typical pipeline:
- Branch decision is resolved in the DR stage (cycle 2)
- But the next instruction (IF) has already been fetched in cycle 2
- If the branch is taken, the fetched instruction is incorrect and must be squashed

**Example:**
```
Cycle:  1    2    3    4    5
BR:    IF   DR   ALU  DM   RW
I2:         IF   ?    ?    ?
              ^-- May need to be cancelled
```

---

## Control Hazard Mitigation Techniques

Assume: 100 instructions total, 20 are branch instructions

### Option 1: Do Nothing (Stall)

**Strategy**: When a branch is encountered, stall the pipeline until the branch is resolved.

**Execution:**
- Every branch causes 1 stall cycle
- 20 branches = 20 stalls
- **Total cycles**: 100 + 20 = 120 cycles

**Pros**: Simple, always correct
**Cons**: Worst performance

### Option 2: Predict Not Taken (Default)

**Strategy**: Always fetch the next sequential instruction (PC+4) while resolving the branch.

**Execution:**
- If branch is not taken: No penalty (instruction already fetched)
- If branch is taken: 1 stall (must squash and fetch correct instruction)

**Example scenario:**
- 8 branches taken (penalty)
- 12 branches not taken (no penalty)
- **Total cycles**: 100 + 8 = 108 cycles

**Pros**: Better than doing nothing
**Cons**: Depends on branch behavior

### Option 3: Branch Delay Slot (Compiler-Assisted)

**Strategy**: Execute a useful instruction in the slot immediately after the branch, regardless of branch outcome.

The compiler tries to find an instruction that:
- Can be safely moved into the delay slot
- Does not affect the branch decision
- Will execute correctly regardless of branch outcome

#### Sub-option A: Move from Before Branch

```assembly
# Before:
ADD $1, $2, $3      # Safe to move
BEQ $2, $0, LABEL

# After:
BEQ $2, $0, LABEL
ADD $1, $2, $3      # In delay slot
```

**Requirements:**
- Instruction must not affect branch condition
- Must not depend on branch outcome

**Result**: If always successful, **Total cycles**: 100 cycles (ideal!)

#### Sub-option B: Move from Taken Branch (Prefetch from target)

```assembly
BEQ $2, $0, LABEL
# Delay slot: fetch first instruction from LABEL
```

**Execution:**
- Prefetch an instruction from the branch target (LABEL)
- If branch taken: Useful work done
- If branch not taken: Must squash and penalty incurred

**Example:**
- 80% branches taken (16 successes)
- 20% branches not taken (4 penalties)
- **Total cycles**: 100 + 4 = 104 cycles

**Requirements:**
- Moved instruction must not affect the not-taken path

#### Sub-option C: Move from Not-Taken Path

```assembly
BEQ $2, $0, LABEL
# Delay slot: fetch next sequential instruction
```

**Execution:**
- Prefetch instruction from fall-through path
- If branch not taken: Useful work done
- If branch taken: Must squash and penalty incurred

**Example:**
- 80% branches taken (16 penalties)
- 20% branches not taken (4 successes)
- **Total cycles**: 100 + 16 = 116 cycles

**Note**: Only effective if branch is mostly not taken

#### Sub-option D: No Operation (NOP)

If no suitable instruction can be found:
```assembly
BEQ $2, $0, LABEL
NOP                 # Do nothing in delay slot
```

- **Total cycles**: 100 + 20 = 120 cycles (same as Option 1)

### Option 4: Branch Prediction (Dynamic/Hardware)

**Strategy**: Use runtime history to predict branch direction.

**Mechanism:**
- Maintain a history table of branch outcomes
- Predict based on past behavior
- If correct: No penalty
- If incorrect: Squash and fetch correct instruction

**Example:**
- 90% prediction accuracy (18 correct, 2 incorrect)
- **Total cycles**: 100 + 2 = 102 cycles

**Pros**: Best performance when prediction is accurate
**Cons**: Requires additional hardware

---

## Performance Summary

### Data Hazards

| Scenario | Without Bypassing | With Bypassing |
|----------|-------------------|----------------|
| ADD-ADD | 2 stalls | 0 stalls |
| ADD-LOAD | 2 stalls | 0 stalls |
| LOAD-LOAD | 2 stalls | 1 stall |
| LOAD-STORE (value) | 2 stalls | 0 stalls |
| LOAD-STORE (address) | 2 stalls | 1 stall |

**Key Takeaway**: Bypassing significantly reduces or eliminates data hazard penalties.

### Control Hazards (100 instructions, 20 branches)

| Strategy | Total Cycles | Notes |
|----------|-------------|-------|
| Stall | 120 | Worst case |
| Predict Not Taken | 108 | 8 taken, 12 not taken |
| Delay Slot (before) | 100 | Best case if always successful |
| Delay Slot (taken) | 104 | 80% taken rate |
| Delay Slot (not taken) | 116 | 20% not taken rate |
| Delay Slot (NOP) | 120 | No suitable instruction |
| Branch Prediction | 102 | 90% accuracy |

**Key Takeaway**: Branch prediction and effective delay slot usage provide the best performance.

---

## Important Formulas

### CPI Calculation
```
CPI = Total Cycles / Total Instructions
```

### Stall Cycles
```
Stall Cycles = Actual Cycles in Stage - Expected Cycles in Stage
```

### Total Execution Time
```
Total Cycles = Ideal Cycles + Stall Cycles from Data Hazards + Stall Cycles from Control Hazards
```

---

## Key Principles

1. **Bypassing Effectiveness**: Value can be bypassed only if POP occurs before POC
2. **Latch Selection**: Distance between producer and consumer determines which latch to bypass from
3. **Instruction Type Matters**: Different instructions have different POP locations:
   - ALU instructions: POP at end of ALU stage
   - LOAD instructions: POP at end of DM stage
   - Both cases: RW stage as final POP

4. **Control Hazard Strategy**: Choose based on:
   - Branch frequency
   - Branch predictability
   - Available compiler optimizations
   - Hardware capabilities

5. **In-Order Execution**: Instructions must proceed through stages in order; one instruction cannot advance if the next stage is occupied

---

## Conclusion

Week 6 provides critical insights into how hazards impact pipeline performance and the various techniques to mitigate them. Bypassing/forwarding is essential for minimizing data hazard stalls, while control hazards require a combination of compiler techniques (branch delay slots) and hardware support (branch prediction) for optimal performance. Understanding the point of production and point of consumption is key to analyzing and resolving data dependencies in pipelined processors.
