# [Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/)

**Easy** | **15 minutes** | **Divide and Conquer, Bit Manipulation**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Algorithm:** [Popcount](https://en.wikipedia.org/wiki/Hamming_weight) · [Bitwise operation](https://en.wikipedia.org/wiki/Bitwise_operation)

**Practice:** [`practice/number_of_1_bits/solution.py`](../../practice/number_of_1_bits/solution.py)

You are given an unsigned integer `n`. Return the number of `1` bits in its binary representation.

You may assume `n` is a non-negative integer which fits within 32-bits.

## Examples

### Example 1

**Input:** `n = 23`

**Output:** `4`

**Explanation:** The binary representation of `23` is `10111`, which contains four `1` bits.

### Example 2

**Input:** `n = 2147483645`

**Output:** `30`

**Explanation:** The binary representation of `2147483645` is `1111111111111111111111111111101`, which contains thirty `1` bits.

## Constraints

- `0 <= n <= 2^31 - 1`.

## Deriving the Solution

The population count of a fixed-width integer needs no search at all: the answer is a property of the bit pattern, and every solution below reads it off the pattern differently, one position at a time, one set bit at a time, or in a single built-in call.

1. **Start literal.** A 32-bit integer has 32 positions, so check each one:
   mask with `1 << i`, add the bit to a running total. Correct and hard to get
   wrong, but it always runs all 32 positions, set or not: see
   [Bit Masking](#bit-masking).
2. **Stop at the top bit.** The positions above `n`'s highest set bit are all
   zero, so the same mask-and-shift loop can end once the value itself reaches
   zero instead of running a fixed 32 passes: see
   [Shift and Count](#shift-and-count).
3. **Skip the zero runs.** Both scans pay for every position, yet the zeros
   between set bits contribute nothing. Subtracting one from `n` turns its
   lowest set bit off, so `n & (n - 1)` erases exactly that bit; looping until
   zero visits each set bit once and no gap: see
   [Brian Kernighan Erase Loop](#brian-kernighan-erase-loop).
4. **Or hand the count to the library.** The whole question is Python's
   `bin(n).count("1")`: format the integer as a bit string and count the
   `1` characters: see [Built-in Count](#built-in-count).

## Solutions

### Bit Masking

#### Derivation

The most direct reading fixes the width at 32 and interrogates every position: bit `i` is `(n >> i) & 1`, and the population count is the sum of those 32 bits. Nothing about the loop can go wrong at the edges, which makes this the reference implementation every faster idea has to match. The steps:

1. Initialize the accumulator `total` to `0`.
2. For each position `i` from `0` through `31`, add `(n >> i) & 1` to `total`.
3. Return `total`.

#### Walkthrough

Let us mask Example 1 by hand: `n = 23`, which is `10111` in binary, expected Output `4`. The scan runs all five low positions explicitly (positions 5 through 31 each contribute `0`):

```text
i=0   n >> 0 = 10111   & 1 = 1   total = 1
i=1   n >> 1 = 01011   & 1 = 1   total = 2
i=2   n >> 2 = 00101   & 1 = 1   total = 3
i=3   n >> 3 = 00010   & 1 = 0   total = 3
i=4   n >> 4 = 00001   & 1 = 1   total = 4
i=5   n >> 5 = 00000   & 1 = 0   total = 4
```

The total reaches `4` after position `4` and never moves again: positions `5` through `31` all mask to `0`. The function returns `4`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's fixed 32-position mask scan.

```python
class Solution:
    def hammingWeight(self, n: int) -> int:
        total = 0
        for i in range(32):
            total += (n >> i) & 1
        return total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)`, 32 iterations

The loop runs exactly 32 times whatever the value, because the width is fixed. The bound is constant, though the constant is larger than the set-bit count when the value is sparse.

##### Space Complexity: `O(1)`

Only the running total and the loop index.

#### Key Insights

- Reads like the definition: sum the 32 bits, one mask per position.
- The iteration count never adapts: `n = 0` pays the full 32 passes.
- The baseline the erase loop must beat and match in results.

### Shift and Count

#### Derivation

The Bit Masking scan keeps walking after the value is exhausted: every position above the highest set bit masks to zero. Shifting `n` right by one drops its lowest bit, so the value itself announces when the scan is done: while `n` is nonzero there is at least one set bit left to count. The low bit test `n & 1` replaces the masked read, and the fixed 32 becomes a data-driven loop. The steps:

1. Initialize the accumulator `total` to `0`.
2. While `n` is nonzero: add `n & 1` to `total`, then shift `n` right by one.
3. Return `total`.

#### Walkthrough

Let us shift Example 1 by hand: `n = 23` = `10111`, expected Output `4`:

```text
n = 10111   n & 1 = 1   total = 1   n >>= 1 -> 01011
n = 01011   n & 1 = 1   total = 2   n >>= 1 -> 00101
n = 00101   n & 1 = 1   total = 3   n >>= 1 -> 00010
n = 00010   n & 1 = 0   total = 3   n >>= 1 -> 00001
n = 00001   n & 1 = 1   total = 4   n >>= 1 -> 00000
n = 00000   loop exits
```

The loop runs five passes, one per bit of `23`, and stops the moment `n` hits zero instead of walking on to position 31. The accumulated `total` is `4`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's shift-until-zero loop.

```python
class Solution:
    def hammingWeight(self, n: int) -> int:
        total = 0
        while n:
            total += n & 1
            n >>= 1
        return total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

The loop runs once per bit of `n`, which is its bit length, about `log2(n) + 1` positions; at most 32 within the constraint. For a value like `2^30` this is 31 passes versus the mask scan's fixed 32, and for `0` it is none at all.

##### Space Complexity: `O(1)`

Only the running total and the shrinking copy of `n`.

#### Key Insights

- The value drives the loop: no fixed width, and `n = 0` exits immediately.
- Still pays for every zero below the top bit; the set bits alone would be enough, which is what the erase loop exploits.
- In fixed-width languages this loop is where a signed right shift would sign-extend forever; the problem's unsigned guarantee is what makes `while n` terminate.

### Brian Kernighan Erase Loop

#### Derivation

Both scans above charge every position for work only the set bits need. The [Kernighan](https://en.wikipedia.org/wiki/Hamming_weight) observation removes the zeros from the bill entirely: subtracting one from `n` flips its lowest set bit to `0` and every bit below it to `1`, so ANDing the two keeps only the bits above that lowest set bit. One line, `n &= n - 1`, erases exactly one set bit; loop until `n` is zero and the number of erases is the population count. The steps:

1. Initialize the counter `count` to `0`.
2. While `n` is nonzero: apply `n &= n - 1` and increment `count`.
3. Return `count`.

#### Invariant

Each iteration preserves one property: `count` equals the number of set bits erased so far, and `n` holds the original value with exactly those bits cleared:

$$ \textit{count} + \text{popcount}(\textit{n}) = \text{popcount}(\textit{n}_0) \;\Rightarrow\; \textit{count} = \text{popcount}(\textit{n}_0) \text{ when } \textit{n} = 0 $$

```text
count + popcount(n) = popcount(original n)
    each pass: n loses exactly one set bit (the lowest), count gains 1
    at loop exit: popcount(n) = 0, so count = popcount(original n)
```

The erase step preserves the invariant because `n & (n - 1)` drops the population count by exactly one: subtracting one borrows through the trailing zeros and turns off the lowest set bit, and the AND discards every bit the subtraction disturbed below it. The loop exits when `n` reaches zero, at which point the invariant reads `count = popcount(original)`, which the return reports.

#### Walkthrough

Let us erase Example 1 bit by bit: `n = 23` = `10111`, expected Output `4`. Each line is one loop pass, showing the subtraction and the erase:

```text
pass 1   n = 10111   n - 1 = 10110   erase -> 10110   count = 1
pass 2   n = 10110   n - 1 = 10101   erase -> 10100   count = 2
pass 3   n = 10100   n - 1 = 10011   erase -> 10000   count = 3
pass 4   n = 10000   n - 1 = 01111   erase -> 00000   count = 4
n = 0    loop exits
```

Four passes, one per set bit: the zero in the middle of `10111` is never visited. Pass 1 erases the lowest of the three low ones, pass 2 the next, pass 3 the top bit's neighbors, and pass 4 the top bit itself, where the borrow fills all four lower positions with ones so the AND clears everything. The final `count` is `4`, matching the expected Output for Example 1. Example 2 shows the gap the loop closes: `2147483645` holds 30 set bits in 31 positions, and the loop finishes in 30 passes where the shift loop needs 31.

#### Solution

The code is the walkthrough's erase loop: one line inside the loop does all the work.

```python
class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0
        while n:
            n &= n - 1
            count += 1
        return count
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(k)`, one pass per set bit

Each iteration erases exactly one set bit, so the loop runs `k` times, the population count of `n`; at most 32 within the constraint, and zero passes for `n = 0`. This is optimal for a loop-based scan: no algorithm that inspects bits one at a time can visit fewer than the set bits themselves.

##### Space Complexity: `O(1)`

The counter and the eroding copy of `n`.

#### Key Insights

- `n & (n - 1)` is the whole trick: it clears the lowest set bit and nothing else, so the loop visits set bits only, skipping zero runs entirely.
- The worst case matches the shift scan (all 31 bits set) and the best case is dramatic: `n = 1` finishes in one pass where both scans mask all 32 positions.
- The same idiom powers two classic tests: `n & (n - 1) == 0` is true exactly for powers of two, and repeated application enumerates the set bits.

### Built-in Count

#### Derivation

The question is a format-and-count: render `n` in base two and count the `1` characters. Python's [`bin`](https://docs.python.org/3/library/functions.html#bin) produces exactly that string, prefixed with `0b`, and `str.count` tallies a substring. The core logic moves entirely into the standard library. The steps:

1. Format `n` with `bin(n)`, yielding a string like `"0b10111"`.
2. Strip the `"0b"` prefix with a slice.
3. Count the `"1"` characters and return the result.

#### Walkthrough

Here the built-ins are themselves the technique, so the trace opens them up on Example 1: `n = 23`, expected Output `4`:

```text
bin(23)          "0b10111"        positional binary format, "0b" prefixed
bin(23)[2:]      "10111"          prefix stripped
"10111".count("1")   4            one, one, zero, one, one
```

The count of `1` characters in the rendered digits is `4`, matching the expected Output for Example 1. Example 2 exercises the same path on a full-width value: `bin(2147483645)[2:]` renders thirty `1` digits and one `0`, and the count returns `30`.

#### Solution

The code compresses the walkthrough's format and tally into one expression.

```python
class Solution:
    def hammingWeight(self, n: int) -> int:
        return bin(n)[2:].count("1")
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

`bin` renders one character per bit, and `count` scans the string once: both linear in the bit length, so at most 32 steps within the constraint, with the work hidden inside C-level string routines.

##### Space Complexity: `O(log n)`

The rendered bit string holds one character per bit before it is counted, which is more working memory than any of the loop-based scans use.

#### Key Insights

- The shortest correct solution: the entire algorithm is one library call.
- Allocates a string the arithmetic solutions never need; in an interview this one-liner is the companion fact, not the answer being taught.
- Python 3.10 and later offer `n.bit_count()` as a direct hardware population count; `bin(n).count("1")` is the version that works on every supported Python.

## Comparison of Solutions

The practice harness's `practice/number_of_1_bits/reference.py` implements the **Brian Kernighan Erase Loop** solution.

### Time Complexity

- **Bit Masking**: `O(1)` - always exactly 32 mask-and-shift passes.
- **Shift and Count**: `O(log n)` - one pass per bit of `n`, stopping at the top set bit.
- **Brian Kernighan Erase Loop**: `O(k)` - one pass per set bit, `k <= log n`.
- **Built-in Count**: `O(log n)` - render plus scan of a bit-length string.

### Space Complexity

- **Bit Masking**: `O(1)` - the running total and index.
- **Shift and Count**: `O(1)` - the total and the shrinking value.
- **Brian Kernighan Erase Loop**: `O(1)` - the counter and the eroding value.
- **Built-in Count**: `O(log n)` - the rendered bit string.

### Trade-offs

- The Bit Masking scan is the hardest to get wrong and the slowest to care: it pays all 32 positions even for `n = 0`.
- The Shift and Count loop adapts to the value's bit length but still walks every zero below the top bit.
- The Brian Kernighan loop visits only the set bits, which is the best a loop can do, at the cost of knowing the `n & (n - 1)` erase identity.
- The Built-in Count is a single call but materializes a string and hides the algorithm entirely.

### When to Use Each

- **Bit Masking**: when the width is contractual (a register, a wire format) and every position must be examined or taught.
- **Shift and Count**: as the natural cleanup of the mask scan when no fixed width matters.
- **Brian Kernighan Erase Loop** (recommended): the canonical interview answer; it meets every input's lower bound of one pass per set bit with `O(1)` space.
- **Built-in Count**: in production Python, where `bin(n).count("1")` or `n.bit_count()` is the right call and the bit-twiddling is documentation.

### Optimization Notes

- `n & (n - 1)` doubles as a membership test: it equals `0` exactly when `n` is zero or a power of two, the idiom behind constant-time power-of-two checks.
- The erase loop's iteration count is the answer itself; that is why Kernighan's loop is also a way to enumerate set bit positions, appending the erased bit's index each pass.
- For dense fixed-width words, SWAR tricks (pairwise folds over masks like `0x55555555`) compute the count in `O(log w)` adds without any loop, and hardware popcount instructions do it in one; Python's `int.bit_count()` exposes exactly that.
- The divide-by-two scan (`n % 2` plus `n //= 2`) is the shift loop with division syntax; it computes the same answer but signals the wrong idea in a bit-manipulation setting.
