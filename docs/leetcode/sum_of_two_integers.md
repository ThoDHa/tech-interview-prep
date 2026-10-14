# [Sum of Two Integers](https://leetcode.com/problems/sum-of-two-integers/)

**Medium** | **25 minutes** | **Math, Bit Manipulation**

**Pattern:** [Simulation](../patterns/simulation/intuition.md)

**Algorithm:** [Half-adder](https://en.wikipedia.org/wiki/Adder_(electronics)#Half-adder) · [Bitwise operation](https://en.wikipedia.org/wiki/Bitwise_operation) · [Two's complement](https://en.wikipedia.org/wiki/Two%27s_complement)

**Practice:** [`practice/sum_of_two_integers/solution.py`](../../practice/sum_of_two_integers/solution.py)

Given two integers `a` and `b`, return the sum of the two integers without using the `+` and `-` operators.

## Examples

### Example 1

**Input:** `a = 1, b = 1`

**Output:** `2`

### Example 2

**Input:** `a = 4, b = 7`

**Output:** `11`

## Constraints

- `-1000 <= a, b <= 1000`

## Deriving the Solution

The ban on `+` and `-` pushes the question down to the level the operators hide: addition is a per-bit circuit, and every solution below rebuilds that circuit, once per column, recursively, or iterated until the carries run out.

1. **Start literal.** Do what the pen does: walk the 32 bit columns left to
   right, writing each column's sum bit and forwarding its carry. Correct and
   explicit: see [Schoolbook Column Addition](#schoolbook-column-addition).
2. **Spot the column rule.** Each column's behavior is a [half-adder](https://en.wikipedia.org/wiki/Adder_(electronics)#Half-adder):
   the sum bit is the exclusive or of the two input bits, the carry is their
   AND. Run the whole 32-bit word through one half-adder step per pass, with
   the carry fed back in, until no column produces one: see
   [Recursive Half-Adder](#recursive-half-adder).
3. **Unroll the recursion into a loop.** The recursion's depth is the carry
   chain's length, at most the word width, so a loop with the same two steps
   reaches the same fixed point without stack: see
   [Masked Half-Adder Loop](#masked-half-adder-loop).

## Solutions

### Schoolbook Column Addition

#### Derivation

The most literal simulation of pencil-and-paper addition in base two. Each bit column reads the two operands' bits plus the incoming carry, writes the sum bit, and forwards the new carry. The sum bit is the exclusive or of the three inputs, and the carry out is the majority: at least two of the three must be set. The steps:

1. Initialize `total = 0` and `carry = 0`.
2. For each column `i` from `0` through `31`: read `abit` and `bbit`, compute
   `s = abit ^ bbit ^ carry`, set `total`'s bit `i` to `s`, and update
   `carry` to the majority of the three bits.
3. Interpret `total` as a signed 32-bit value and return it: subtract
   `2^32` when its top bit is set.

#### Walkthrough

Let us add Example 2 by hand: `a = 4` = `100`, `b = 7` = `111`, expected Output `11`. Column by column from the right, with `carry` entering as `0`:

```text
col 0   a=0  b=1  carry=0   s = 0^1^0 = 1   carry out = 0   total = 0001
col 1   a=0  b=1  carry=0   s = 0^1^0 = 1   carry out = 0   total = 0011
col 2   a=1  b=1  carry=0   s = 1^1^0 = 0   carry out = 1   total = 0011
col 3   a=0  b=0  carry=1   s = 0^0^1 = 1   carry out = 0   total = 1011
```

Column 2 is where the carries earn their keep: `1 + 1` writes `0` and forwards `1`, which column 3 turns into the leading `1`. The total `1011` is `11`, matching the expected Output for Example 2. Negative operands ride through unchanged: Python sign-extends every negative shift, so a negative `a` reads `abit = 1` from column 31 upward, and the walk keeps producing the correct two's complement columns all the way through the sign region.

#### Solution

The code is the walkthrough's column walk with the majority carried along, plus the two's complement re-read on the way out. Negative inputs stream through unchanged: Python sign-extends every right shift, so each negative operand supplies `1` bits across the whole sign region and `total` ends holding the correct 32-bit pattern, which only needs re-signing.

```python
class Solution:
    def getSum(self, a: int, b: int) -> int:
        total = 0
        carry = 0
        for i in range(32):
            abit = (a >> i) & 1
            bbit = (b >> i) & 1
            s = abit ^ bbit ^ carry
            total |= s << i
            carry = (abit & bbit) | (carry & (abit ^ bbit))
        return total - (1 << 32) if total >> 31 else total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)`, 32 iterations

One constant-work step per column; the width is fixed at 32, so the pass count never varies with the values.

##### Space Complexity: `O(1)`

The two accumulators `total` and `carry`.

#### Key Insights

- The three-input exclusive or and the majority function are the whole truth table of addition, written once per column.
- The carry update `(abit & bbit) | (carry & (abit ^ bbit))` is the majority function: a carry is born when both operand bits are set, and an incoming carry survives when exactly one operand bit is set.
- Python's negative integers are sign-extended to infinity, so `(a >> i) & 1` reads `1` across the whole sign region of a negative operand; the walk assembles the correct 32-bit pattern, and the final conversion re-signs it for Python's open-ended integers.

### Recursive Half-Adder

#### Derivation

The column walk re-derives what a half-adder already knows: the sum bit of a column is the exclusive or of its two input bits, and the carry is their AND. Applied to whole words, one half-adder step adds everything that needs no carry and computes everything that does; feeding the carry back in and repeating finishes the job. That feedback loop is a recursion: `add(a, b)` is `a` when the carry `b` dies, otherwise the same question with the partial sum `a ^ b` and the carry `(a & b) << 1`. Each round moves every carry at least one column left, so the recursion bottoms out within the word's width. The steps:

1. Base case: when `b == 0`, no carry remains and `a` is the sum.
2. Recursive case: recurse on the carryless sum `a ^ b` and the carry
   `(a & b) << 1`.
3. The recursion's final `a` is the sum.

#### Walkthrough

Let us recurse Example 1: `a = 1`, `b = 1`, expected Output `2`:

```text
add(1, 1)
  a ^ b     = 0    (1 ^ 1:  both bits set, sum bit 0)
  (a & b)<<1 = 2   (1 & 1:  both bits set, carry left 1)
add(0, 2)
  a ^ b      = 2   (0 ^ 2:  no overlap, sum takes b's bit)
  (a & b)<<1 = 0   (0 & 2:  no overlap, no carry)
add(2, 0)
  b == 0 -> return 2
```

The first pass strips the `+` into a pure carry, the second folds the carry in, and the third finds nothing left to carry: the answer `2` matches the expected Output for Example 1. Example 2 collapses in two rounds the same way: `add(4, 7)` recurses to `add(3, 8)` (sum bits `011`, carry `1000`), then `add(11, 0)`, returning `11`, matching the expected Output.

#### Solution

The code is the walkthrough's two-line recursion.

```python
class Solution:
    def getSum(self, a: int, b: int) -> int:
        if b == 0:
            return a
        return self.getSum(a ^ b, (a & b) << 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)`, at most 33 frames

Every recursion round shifts the carry at least one column left, so a carry born in column 0 survives at most 32 rounds; the depth is bounded by the word width plus one base-case frame.

##### Space Complexity: `O(1)` in hardware, `O(width)` stack in Python

The values themselves are two registers, but each recursive frame holds its own copy on the call stack: up to 33 frames within the constraint, far below Python's default recursion limit.

#### Key Insights

- `a ^ b` and `(a & b) << 1` decompose addition exactly: the first adds where adding is safe, the second records where it is not.
- This is the formulation to reach for when the mask machinery is not needed and the interviewer wants the circuit made visible.
- On negative inputs, Python's unbounded integers keep `(a & b) << 1` growing the sign extension forever: the recursion never bottoms out. The fix, applied in the next solution, is to keep the word masked to 32 bits and re-sign the result once at the end.

### Masked Half-Adder Loop

#### Derivation

The recursion is the right circuit with the wrong memory: each frame exists only to hand two numbers to the next round, which is a loop. Unrolling removes the stack. Python needs one more repair: its integers have no fixed width, so the sign-extended shadow of a negative operand makes the carry chain march left forever. Masking both operands and every intermediate to 32 bits gives the arithmetic a finite word to live in; at the end, the 32-bit pattern is read as two's complement, negated back if its top bit is set. The steps:

1. Mask `a` and `b` to their low 32 bits.
2. While `b` is nonzero: compute the carry
   `((a & b) << 1) & 0xFFFFFFFF`, replace `a` with
   `(a ^ b) & 0xFFFFFFFF`, and replace `b` with the carry.
3. When the loop exits, `a` holds the 32-bit pattern; return `a` as-is if
   its top bit is clear, else `~(a ^ 0xFFFFFFFF)` to sign it negative.

#### Walkthrough

Let us loop Example 2: `a = 4`, `b = 7`, expected Output `11`:

```text
round 1   a = 100   b = 111   a^b = 011   carry = 1000
          a = 3     b = 8
round 2   a = 0011  b = 1000  a^b = 1011  carry = 0000
          a = 11    b = 0     loop exits
```

Two rounds: the first strips the two overlapping low bits into a carry of `8`, the second merges `3` and `8` with no fresh overlap. The exit value `11` matches the expected Output for Example 2. Example 1 runs the same two-round shape (`1, 1` to `0, 2` to `2`), and negatives exercise the mask: `-12 + -8` churns the carry up through the sign-extended high bits for several rounds, the loop dies when the carry leaves the 32-bit word, and the final pattern's top bit routes the value through the `~(a ^ MASK)` repair, returning `-20`.

#### Solution

The code is the walkthrough's loop with the mask on every write and the sign repair on the way out.

```python
MASK = 0xFFFFFFFF
SIGN_BIT = 1 << 31


class Solution:
    def getSum(self, a: int, b: int) -> int:
        a &= MASK
        b &= MASK
        while b:
            carry = ((a & b) << 1) & MASK
            a = (a ^ b) & MASK
            b = carry
        return a if a < SIGN_BIT else ~(a ^ MASK)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)`, at most 32 passes

Each pass shifts the carry at least one column left within the masked word, so a carry born anywhere can survive at most 32 passes; over the constraint range the worst case is exactly 32 passes, reached by pairs whose carry chain crosses the sign boundary, and every pair finishes inside that constant bound.

##### Space Complexity: `O(1)`

The two working registers; the loop replaces the recursion's stack.

#### Key Insights

- The mask is the whole Python-specific lesson: fixing the word to 32 bits turns the carry into a quantity that provably dies, where unbounded integers would chase it left forever.
- The sign repair `~(a ^ MASK)` is two's complement re-read: XOR with the all-ones mask flips all 32 bits and `~` negates the flipped pattern, converting a negative-pattern word back to Python's signed integer.
- This is the production-grade shape: iterative, constant stack, and explicit about the width the problem's 32-bit contract implies.

## Comparison of Solutions

The practice harness's `practice/sum_of_two_integers/reference.py` implements the **Masked Half-Adder Loop** solution.

### Time Complexity

- **Schoolbook Column Addition**: `O(1)` - one pass over 32 fixed columns.
- **Recursive Half-Adder**: `O(1)` - at most 33 frames, one carry shift per round.
- **Masked Half-Adder Loop**: `O(1)` - at most 32 passes of the same two steps.

### Space Complexity

- **Schoolbook Column Addition**: `O(1)` - two accumulators.
- **Recursive Half-Adder**: `O(1)` registers, `O(width)` stack frames.
- **Masked Half-Adder Loop**: `O(1)` - two working registers, no stack.

### Trade-offs

- The Schoolbook Column Addition spells out every truth table entry, which makes it the most teachable and the most verbose; it also never needs masking, since it touches each column exactly once.
- The Recursive Half-Adder is the circuit distilled to two lines, the clearest statement of the XOR/AND decomposition, but it cannot handle negatives in Python without the mask.
- The Masked Half-Adder Loop is the recursion unrolled plus the width fixed: the only formulation that is simultaneously loop-safe, negative-safe, and stack-free.

### When to Use Each

- **Schoolbook Column Addition**: when teaching binary addition from zero, or when the carry-majority rule deserves center stage.
- **Recursive Half-Adder**: in languages with fixed-width integers, where it is the canonical two-line answer.
- **Masked Half-Adder Loop** (recommended): the Python answer; it is the recursion made safe for unbounded integers and negative operands alike.

### Optimization Notes

- The half-adder steps do not actually need the 32-pass bound as a loop condition: the carry reaching zero is the only exit test, and the bound is a proof about when that must happen, not a counter the code maintains.
- `a & b` shrinking to zero is the recursion invariant in disguise: the AND's set bits are exactly the columns still owing a carry, and each pass moves them left.
- In languages with hardware carry flags, compilers lower `a + b` to one instruction; this problem's value is the decomposition, not a faster add.
- The same XOR/AND pair underlies subtraction when the second operand is two's-complement negated, which itself takes an XOR plus an add: a deeper rabbit hole the `+`/`-` ban usually closes.
