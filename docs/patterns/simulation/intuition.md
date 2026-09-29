# Simulation: Pattern Intuition Guide

> *"There is no shortcut. The problem describes a process: your job is to become the machine that runs it, faithfully and without error."*

---

## The Situation That Calls for Simulation

Imagine someone hands you a board game with a thick rulebook. They don't ask you to invent a winning strategy or to find a clever closed-form answer. They ask you to play out a specific sequence of turns *exactly as written* and report the final state of the board.

You can't reason your way to the answer with a formula. There is no elegant insight that collapses the work into a single step. The only correct move is to read the rules, set up the board, and advance turn by turn, respecting every condition.

**This is the essence of Simulation.**

You encounter this pattern whenever:
- The problem **describes a procedure** and asks for its outcome
- There is **no obvious data structure or formula** that shortcuts the work
- Correctness depends on **precise state tracking and boundary handling**, not on a flash of algorithmic insight
- The difficulty lives in the **details**: corner cases, ordering, off-by-one errors

The key realization: *You are not solving a puzzle. You are modeling a process. The challenge is fidelity, not cleverness.*

---

## The Core Insight: State, Transitions, Boundaries


Every simulation problem reduces to three questions. Answer them precisely before writing a single line of logic.

### 1. What is the state?
The state is the minimal set of variables that fully describes the current situation. For a spiral traversal, the state is four wall positions. For binary addition, it is the current digit positions and a carry. For parsing, it is your position in the input plus an accumulated result.

*If two situations have identical state, your code must treat them identically.* Choosing the right state is the whole game.

### 2. What are the transition rules?
Given the current state, how do you produce the next state? This is the rulebook translated into code. Each transition advances the process by one well-defined step.

### 3. When do you stop, and where are the edges?
Termination conditions and boundaries determine when the loop ends and what happens at the limits. Most simulation bugs hide here: one step too many, one step too few, or a wall crossed that should have held.

Once these three are nailed down, the algorithm writes itself: **set up the initial state, then advance step by step until a termination condition is met.**

---

## Mental Models

Different simulation problems feel different. Recognizing the shape tells you how to structure the state.

### Model 1: Boundary Shrinking: "Four Walls Closing In"

**The situation**: You traverse a matrix in spiral order. You don't track every visited cell. Instead you maintain four walls (`top`, `bottom`, `left`, `right`) that enclose the unvisited region. After walking along an edge, that wall steps inward.

**The mental model**:
```
┌─────────────────────────────────────────────┐
│  top ───────────────────────────────────►   │
│  ▲           unvisited region            ▼   │
│  left                                  right  │
│  ▲                                        ▼   │
│  ◄─────────────────────────────── bottom     │
└─────────────────────────────────────────────┘

Walk right along top → top++       Walk left along bottom → bottom--
Walk down along right → right--     Walk up along left → left++
```

**The decision rule**: Repeat the four directional walks while `top <= bottom` and `left <= right`. After each walk, retreat the corresponding wall. When the walls cross, every cell is visited.

**Why it works**: The walls are the state. They encode exactly which region remains. Shrinking a wall is the transition; the crossing of walls is the termination condition.

### Model 2: Digit-by-Digit with Carry: "Grade-School Arithmetic"

**The situation**: You add two binary strings. There is no built-in big-number trick to lean on: you do it the way you learned addition as a child, one column at a time, right to left, carrying the overflow.

**The mental model**:
```
        1 0 1 1
      +   1 0 1     process columns right → left;
      ─────────     carry feeds into the next column
      1 0 0 0 0
```

**The decision rule**: Walk both strings from the rightmost digit. At each column, sum the two digits plus the incoming carry. The result digit is `total % 2`; the new carry is `total // 2`. Continue until both strings are exhausted *and* the carry is zero.

**Why it works**: The state is the pair of positions plus a single carry bit. The carry is the entire memory of the past needed to compute the future. Forget it, and the answer is wrong.

### Model 3: The Parsing State Machine: "atoi"

**The situation**: You convert a messy string into an integer. The input may have leading spaces, an optional sign, digits, then trailing garbage. You move through a fixed sequence of phases, and each phase has its own rule.

**The mental model**:
```
   skip whitespace ──► optional sign ──► consume digits ──► stop
                                              │
                          non-digit or end → stop
                          overflow → clamp to limit
```

**The decision rule**: Skip leading whitespace. Read at most one `+` or `-`. Read consecutive digits, accumulating the number. Stop at the first non-digit or the end of input. Clamp the result to the signed 32-bit range if it overflows.

**Why it works**: Each phase is a state. The transition from phase to phase is strictly one-directional: once you've passed the sign, you never look for another. The accumulation and the clamping are the rules that live inside the digit phase. The [String to Integer (atoi)](../../problems/string_to_integer_atoi.md) problem page makes this literal with an explicit table-driven State Machine (DFA) approach: the states and transitions written out as a lookup table.

---

## Pattern Recognition Signals

When you see these phrases, think **Simulation**:

### Signal: "Traverse in this specific order"
> *"Return all elements of the matrix in spiral order"* *"Visit the grid in a zigzag / diagonal / clockwise pattern"*

**Action**: Model the traversal directly with position state and explicit boundaries.

### Signal: "Perform these steps" / "Apply these operations"
> *"Carry out the following sequence of moves"* *"Process each instruction and report the final result"*

**Action**: Translate each described step into a transition on your state.

### Signal: "Parse / convert this format"
> *"Convert the string to an integer"* *"Interpret this input according to these formatting rules"*

**Action**: Build a state machine that walks the input phase by phase.

### Signal: "No obvious data structure or formula: just follow the rules"
> *"Given the rules above, determine the outcome"*

**Action**: Stop searching for cleverness. Identify state, transitions, and boundaries, then advance step by step.

---

## Worked Traces

### Trace 1: Boundary Shrinking: Spiral Matrix

**Problem**: Return the elements of the matrix in spiral order. **Input**: rows `[1, 2, 3]`, `[4, 5, 6]`, `[7, 8, 9]`.

State: `top=0`, `bottom=2`, `left=0`, `right=2`. Output collected as we go.

```
┌──────────────────────────────────────────────────────────────┐
│ Walk right along top (cols 0..2): 1,2,3 → top=1             │
│ Walk down along right (rows 1..2): 6,9 → right=1           │
│ Walk left along bottom (cols 1..0): 8,7 → bottom=1        │
│ Walk up along left (row 1): 4 → left=1                     │
│ Walk right along top (row 1, col 1): 5 → top=2            │
│ Now top(2) > bottom(1) → STOP.                             │
│ output = [1, 2, 3, 6, 9, 8, 7, 4, 5]                        │
└──────────────────────────────────────────────────────────────┘
```

The critical guard: after shrinking a wall, re-check the loop condition *before* the next walk. Skipping this check is the source of the dreaded double-printed middle row.

```python
def spiral_order(matrix):
    if not matrix or not matrix[0]:
        return []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    result = []
    while top <= bottom and left <= right:
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1
    return result
```

### Trace 2: The State Machine: atoi

**Problem**: Convert a string to a 32-bit signed integer. **Input**: `"   -042"`, then `"4193 with words"`, then `"99999999999"`.

```
┌──────────────────────────────────────────────────────────────┐
│ "   -042":                                                   │
│   skip whitespace → index 3; sign '-' → -1; digits 0,4,2     │
│   end of string → stop. Result = -42                         │
│ "4193 with words":                                           │
│   no whitespace; '4' not a sign → +1; digits 4,41,419,4193   │
│   next char ' ' non-digit → stop. Result = 4193             │
│ "99999999999":                                               │
│   digits accumulate past 2,147,483,647                       │
│   overflow → clamp to INT_MAX = 2147483647                  │
└──────────────────────────────────────────────────────────────┘
```

```python
INT_MAX = 2**31 - 1
INT_MIN = -2**31

def my_atoi(s):
    i, n = 0, len(s)
    while i < n and s[i] == ' ':      # skip whitespace
        i += 1
    sign = 1
    if i < n and s[i] in '+-':         # optional sign
        sign = -1 if s[i] == '-' else 1
        i += 1
    value = 0
    while i < n and s[i].isdigit():    # consume digits
        value = value * 10 + int(s[i])
        i += 1
    value *= sign
    return max(INT_MIN, min(INT_MAX, value))   # clamp overflow
```

Notice how each phase advances `i` and never revisits earlier phases. The state is `(i, sign, value)`, and the transitions are strictly forward.

---

## Common Pitfalls

### Pitfall 1: Off-by-One on Boundaries
The most common simulation failure. Decide upfront whether your bounds are inclusive or exclusive and stay consistent. In spiral traversal, walking `range(left, right + 1)` is inclusive; forgetting the `+ 1` drops the last column. Re-checking the loop condition after each wall moves prevents revisiting a row or column.

### Pitfall 2: Integer Overflow
Whenever you accumulate digits or sums, the value can exceed the allowed range. Clamp to the signed limit (`INT_MAX` / `INT_MIN`) the moment overflow is possible, not after the damage is done. In languages with fixed-width integers, detect overflow *before* the multiply-and-add, not after.

### Pitfall 3: Dropping the Final Carry
In digit-by-digit addition, the loop must continue while *either* string has digits remaining *or* the carry is nonzero. Stopping when the strings run out loses the leading `1` in cases like `1 + 1 = 10`.

### Pitfall 4: Edge Cases That Break the Setup
Simulation lives and dies on corner cases. Always check:
- **Empty input**: zero-length string or matrix. Return the empty result without touching `matrix[0]`.
- **Leading / trailing whitespace**: skip leading; treat trailing as a stop signal.
- **Signs**: a lone `+` or `-` with no digits yields zero; two signs is invalid.
- **Leading zeros**: `"0042"` is `42`, not an error.
- **Single element**: a 1×1 matrix or one-character string must not fall through your loop conditions.
- **When to stop**: the first non-digit, the crossing of walls, or the exhaustion of input. Define this precisely.

### Pitfall 5: Forgetting to Advance State
A simulation that never updates its position loops forever. Every iteration must make measurable progress toward termination: a wall must move, an index must increment, a carry must resolve.

---

## Corner Cases

- Empty input: zero-length string, empty matrix, or matrix of empty rows
- Single element: a 1x1 matrix or one-character string must not fall through the loop guards
- Input already in its final state: zero iterations, correct result
- Walls adjacent after a shrink (spiral): mid-loop boundary re-checks before each walk
- Values at the extremes: accumulation past 32-bit limits; a final carry beyond the top digit
- Input at the grammar's edge (atoi): lone sign, sign with no digits, garbage after digits, leading zeros

---

## Practice Progression

Master simulation through this sequence:

1. **Spiral Matrix**: The canonical boundary-shrinking traversal. Maintain four walls and retreat each after its walk. Learn to re-check the loop condition mid-iteration to avoid double-visiting cells.

2. **Add Binary**: Digit-by-digit processing with carry. Walk both strings right to left, sum with carry, and remember to emit the final carry. Trains careful state tracking and termination.

3. **String to Integer (atoi)**: The parsing state machine. Skip whitespace, read an optional sign, consume digits, stop at the first non-digit, and clamp on overflow. The definitive exercise in precise phase handling and corner cases.

Work them in this order: spiral builds boundary discipline, binary addition builds carry discipline, and atoi forces you to handle every messy edge at once.

---

## The Unifying Principle

Simulation rewards **discipline over insight**.

There is no trick waiting to be discovered. The whole problem is already written in the description; your task is to translate it into state, transitions, and boundaries, then execute faithfully.

Before writing code, answer three questions: *What is my state? How does it change? When do I stop?* Get those right, and the implementation is mechanical. Get any one wrong, and no amount of cleverness will save you.

> **Model the process exactly. Track the state honestly. Guard every boundary.** **The machine does not improvise, and neither should you.**
