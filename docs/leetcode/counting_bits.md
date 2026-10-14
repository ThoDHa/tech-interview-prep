# [Counting Bits](https://leetcode.com/problems/counting-bits/)

**Easy** | **15 minutes** | **Dynamic Programming, Bit Manipulation**

**Pattern:** [DP 1D Linear](../patterns/dp_1d_linear/intuition.md)

**Algorithm:** [Popcount](https://en.wikipedia.org/wiki/Hamming_weight) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Bitwise operation](https://en.wikipedia.org/wiki/Bitwise_operation)

**Practice:** [`practice/counting_bits/solution.py`](../../practice/counting_bits/solution.py)

Given an integer `n`, count the number of `1`'s in the binary representation of every number in the range `[0, n]`.

Return an array `output` where `output[i]` is the number of `1`'s in the binary representation of `i`.

## Examples

### Example 1

**Input:** `n = 4`

**Output:** `[0,1,1,2,1]`

**Explanation:** 0 --> 0
1 --> 1
2 --> 10
3 --> 11
4 --> 100

## Constraints

- `0 <= n <= 1000`

## Deriving the Solution

The answer is not one number but `n + 1` of them, and that shape is the whole hint: every value from `0` to `n` sits in the table, so the popcount of `i` can be assembled from the popcounts of smaller values already sitting beside it. Every solution below computes each entry either in isolation or from its neighbors.

1. **Start literal.** The definition is a per-value question: render each of the
   `n + 1` integers in binary and count the `1` digits. Correct, and the work
   repeats structure every value shares with its neighbors: see
   [Per-Value Count](#per-value-count).
2. **Spot the overlap.** Appending a bit to a binary string preserves the
   string's ones and adds the new bit's value, so `popcount(i)` relates to
   `popcount` of a smaller number by one addition. That relation is a
   recurrence, and a table walk fills every entry in constant work: see
   [Bottom-Up DP](#bottom-up-dp).
3. **Read the recurrence off the lowest set bit.** Two one-line identities
   expose the smaller neighbor: shifting right drops the last bit
   (`dp[i] = dp[i >> 1] + (i & 1)`), and clearing the lowest set bit with
   `i & (i - 1)` erases exactly one `1` (`dp[i] = dp[i & (i - 1)] + 1`). The
   second form skips every trailing zero, so each entry reads a neighbor of
   equal-or-lower popcount: see
   [Bottom-Up DP with Lowest Set Bit](#bottom-up-dp-with-lowest-set-bit).
4. **Fold to the top power of two instead.** A third framing watches for
   powers of two: between `high` and `2 * high` every value is `high` plus a
   smaller value, so `dp[i] = dp[i - high] + 1` with `high` doubling as the
   range grows: see [Bottom-Up DP with Offset](#bottom-up-dp-with-offset).
5. **Or map the whole range at once.** Python 3.10's `int.bit_count()` is a
   direct hardware popcount, turning the table into one list comprehension:
   see [Built-in Popcount](#built-in-popcount).

## Solutions

### Per-Value Count

#### Derivation

The most direct reading answers the question `n + 1` times, once per value, with no memory of the previous answers: each `i` is formatted in binary and its `1` digits are counted. The steps:

1. For each `i` from `0` through `n`, format it with `bin(i)` and strip the
   `"0b"` prefix.
2. Count the `"1"` characters.
3. Collect the counts into `output` in order and return it.

#### Walkthrough

Let us run the per-value count on Example 1: `n = 4`, expected Output `[0,1,1,2,1]`:

```text
i = 0    bin -> "0"      ones = 0    output = [0]
i = 1    bin -> "1"      ones = 1    output = [0, 1]
i = 2    bin -> "10"     ones = 1    output = [0, 1, 1]
i = 3    bin -> "11"     ones = 2    output = [0, 1, 1, 2]
i = 4    bin -> "100"    ones = 1    output = [0, 1, 1, 2, 1]
```

Each row is computed with no help from the rows before it. The final `output` is `[0, 1, 1, 2, 1]`, matching the expected Output for Example 1, and reproducing the Explanation's `0 --> 0, 1 --> 1, 2 --> 10, 3 --> 11, 4 --> 100` column by column.

#### Solution

The code is the walkthrough's per-row format and tally.

```python
from typing import List


class Solution:
    def countBits(self, n: int) -> List[int]:
        output = []
        for i in range(n + 1):
            output.append(bin(i)[2:].count("1"))
        return output
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Each of the `n + 1` values is rendered in `O(log i)` bits and scanned over those bits, so the total is the sum of the bit lengths, about `n log n` at the top of the range.

##### Space Complexity: `O(n)`

The output list holds `n + 1` entries, which the problem requires; nothing else grows with the input.

#### Key Insights

- Answers each value in isolation, which is the definition and also the waste: every row rediscovers structure its neighbors already encode.
- Simple to write and verify; the correct baseline for the DP versions below.
- The per-row cost is `O(log i)`, so the total is a factor `log n` above the theoretical minimum of one constant step per entry.

### Bottom-Up DP

#### Derivation

The per-value scan ignores the table's structure, but appending one bit to a binary string preserves the ones already there and adds the new bit's value. Shifting `i` right by one drops its last bit, so `i >> 1` is a smaller value whose popcount is already in the table, and the dropped bit is `i & 1`. That is a recurrence: `dp[i] = dp[i >> 1] + (i & 1)`, with `dp[0] = 0` seeding the table. Fill upward and every entry is one lookup plus one addition:

1. Allocate `dp` of length `n + 1` with `dp[0] = 0`.
2. For each `i` from `1` through `n`, set
   `dp[i] = dp[i >> 1] + (i & 1)`.
3. Return `dp`.

#### Recurrence

Let `dp[i]` be the number of `1` bits in the binary representation of `i`:

$$ dp[i] = \begin{cases}
0, & i = 0 \\[4pt]
dp[\lfloor i / 2 \rfloor] + (i \bmod 2), & i > 0
\end{cases} $$

```text
dp[0] = 0
dp[i] = dp[i >> 1] + (i & 1)   for i > 0
```

The base case encodes that `0` has no set bits. The transition says appending one bit to `i >> 1`'s binary string yields `i`'s string: the existing ones survive unchanged and the appended bit contributes `i & 1`. The answer is the whole table, which is what the return hands back.

#### Walkthrough

Let us fill the table on Example 1: `n = 4`, expected Output `[0,1,1,2,1]`:

```text
dp[0] = 0                          (seed)
i=1  (1)   i >> 1 = 0   (i & 1)=1  dp[1] = dp[0] + 1 = 1
i=2  (10)  i >> 1 = 1   (i & 1)=0  dp[2] = dp[1] + 0 = 1
i=3  (11)  i >> 1 = 1   (i & 1)=1  dp[3] = dp[1] + 1 = 2
i=4  (100) i >> 1 = 2   (i & 1)=0  dp[4] = dp[2] + 0 = 1
```

Each row reads a strictly smaller index already finalized, so no second pass is ever needed. The filled table is `[0, 1, 1, 2, 1]`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's table fill.

```python
from typing import List


class Solution:
    def countBits(self, n: int) -> List[int]:
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i >> 1] + (i & 1)
        return dp
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One constant-work transition per index: a shift, a mask, an addition, and one table write. Total work is linear where the per-value scan paid an extra `log` factor.

##### Space Complexity: `O(n)`

The output table itself; the iteration carries no additional state beyond the loop index.

#### Key Insights

- The DP insight in its plainest form: `i`'s bits are `i >> 1`'s bits plus one more, so its popcount inherits.
- `dp` is both the memo and the answer, the linear-DP ideal where nothing computed is ever discarded.
- Halving steps through the string from the left; the next solution steps from the right and skips zeros.

### Bottom-Up DP with Lowest Set Bit

#### Derivation

The shift recurrence reads the neighbor by dropping the last bit, trailing zeros and all. The erase identity from Number of 1 Bits, `i & (i - 1)`, is more surgical: it clears exactly the lowest set bit, so `dp[i] = dp[i & (i - 1)] + 1` says `i`'s popcount is one more than the value that differs from it by that single bit. Every read lands on an entry whose popcount is already settled and at most `dp[i]`, and for powers of two the read is `dp[0]`, the immediate base case. The steps:

1. Allocate `dp` of length `n + 1` with `dp[0] = 0`.
2. For each `i` from `1` through `n`, set
   `dp[i] = dp[i & (i - 1)] + 1`.
3. Return `dp`.

#### Recurrence

Let `dp[i]` be the number of `1` bits in the binary representation of `i`:

$$ dp[i] = \begin{cases}
0, & i = 0 \\[4pt]
dp[i \,\&\, (i - 1)] + 1, & i > 0
\end{cases} $$

```text
dp[0] = 0
dp[i] = dp[i & (i - 1)] + 1   for i > 0
```

The transition erases `i`'s lowest set bit with the Kernighan identity: `i & (i - 1)` has exactly the bits of `i` minus one of them, so its popcount is already tabulated and `dp[i]` is that entry plus the erased bit. The answer is the whole table.

#### Walkthrough

Let us refill Example 1 with the erase recurrence: `n = 4`, expected Output `[0,1,1,2,1]`. Each row shows the low-bit erase happening inside the index:

```text
dp[0] = 0                                  (seed)
i=1  (001)  i & (i-1) = 001 & 000 = 000    dp[1] = dp[0] + 1 = 1
i=2  (010)  i & (i-1) = 010 & 001 = 000    dp[2] = dp[0] + 1 = 1
i=3  (011)  i & (i-1) = 011 & 010 = 010    dp[3] = dp[2] + 1 = 2
i=4  (100)  i & (i-1) = 100 & 011 = 000    dp[4] = dp[0] + 1 = 1
```

Watch the reads: the powers of two (`1`, `2`, `4`) all read `dp[0]`, because a power of two is one set bit on top of zero; `3` reads `dp[2]`, differing from it by exactly its lowest one. The filled table is `[0, 1, 1, 2, 1]`, matching the expected Output for Example 1, entry for entry with the shift version.

#### Solution

The code is the walkthrough's fill with the erase identity in the index.

```python
from typing import List


class Solution:
    def countBits(self, n: int) -> List[int]:
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i & (i - 1)] + 1
        return dp
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One constant-work transition per index: one subtraction, one AND, one addition, and one write, the same bill as the shift version entry for entry.

##### Space Complexity: `O(n)`

The output table; nothing beyond it.

#### Key Insights

- The same table as the shift recurrence, computed through the Number of 1 Bits erase identity: the two problems share one primitive.
- Powers of two resolve in a single read of `dp[0]`, the pattern the recurrence exploits most visibly.
- The read target's popcount never exceeds the written entry's, which makes the table's growth monotone and the recurrence easy to trust.

### Bottom-Up DP with Offset

#### Derivation

A third framing watches the range's shape instead of a single index's bits. Between a power of two `high` and the next power `2 * high`, every value `i` is `high + (i - high)`: the top bit of `high` stamped onto a smaller value already in the table. So `dp[i] = dp[i - high] + 1`, where `high` doubles each time `i` reaches the next power of two. The recurrence carries the range's structure explicitly and reads its neighbor at a fixed distance below. The steps:

1. Allocate `dp` of length `n + 1` with `dp[0] = 0`; set `high = 1`.
2. For each `i` from `1` through `n`: when `i` reaches `2 * high`, double `high`.
3. Set `dp[i] = dp[i - high] + 1`.
4. Return `dp`.

#### Walkthrough

Let us fill Example 1 with the offset walk: `n = 4`, expected Output `[0,1,1,2,1]`:

```text
dp[0] = 0   high = 1                                (seed)
i=1  high=1   dp[1] = dp[0] + 1 = 1
i=2  2*high reached -> high = 2
             dp[2] = dp[0] + 1 = 1
i=3  high=2   dp[3] = dp[1] + 1 = 2
i=4  2*high reached -> high = 4
             dp[4] = dp[0] + 1 = 1
```

Each value's popcount is one more than the same value with its top bit stripped: `3 = 2 + 1` reads `dp[1]`, and `4`, a fresh power of two, reads `dp[0]` again with `high` now `4`. The filled table is `[0, 1, 1, 2, 1]`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's offset walk: one doubling check, one read, one add.

```python
from typing import List


class Solution:
    def countBits(self, n: int) -> List[int]:
        dp = [0] * (n + 1)
        high = 1
        for i in range(1, n + 1):
            if high * 2 == i:
                high = i
            dp[i] = dp[i - high] + 1
        return dp
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One comparison, one read, and one addition per index; the doublings are at most one per entry and `O(log n)` in total.

##### Space Complexity: `O(n)`

The output table plus one scalar `high`.

#### Key Insights

- Encodes the binary structure at the range level: powers of two are the seams, and every entry inside a block reads its in-block twin.
- The guard `high * 2 == i` fires exactly at each power of two, so `high` tracks the largest power of two not exceeding `i` with no separate scan.
- Same asymptotics as the bit-level recurrences; which one reads clearest is a matter of taste, the block view or the bit view.

### Built-in Popcount

#### Derivation

The whole task is a batched popcount, and Python 3.10 ships a direct one: `int.bit_count()` counts an integer's set bits without rendering a string, backed by a single hardware instruction where available. The per-value loop collapses to one comprehension over the range:

1. Iterate `i` over `0..n` inclusive.
2. Call `i.bit_count()` on each.
3. Collect the results into the returned list.

#### Walkthrough

Here the built-in is the technique, so the trace opens it up on Example 1: `n = 4`, expected Output `[0,1,1,2,1]`:

```text
0.bit_count()   0     (no bits set)
1.bit_count()   1     (0b1)
2.bit_count()   1     (0b10)
3.bit_count()   2     (0b11)
4.bit_count()   1     (0b100)
comprehension   [0, 1, 1, 2, 1]
```

Each call is the hardware popcount of that value, and the collected list is `[0, 1, 1, 2, 1]`, matching the expected Output for Example 1.

#### Solution

The code is the whole problem in one expression.

```python
from typing import List


class Solution:
    def countBits(self, n: int) -> List[int]:
        return [i.bit_count() for i in range(n + 1)]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One native popcount per value, constant work per call; the loop's total is linear, and the constant is the smallest of any solution here.

##### Space Complexity: `O(n)`

The output list, which the problem requires.

#### Key Insights

- The direct transcription of the task onto the standard library, with the recurrence-learning opportunity traded for brevity and speed.
- Unlike the Per-Value Count's string round trip, `bit_count()` never materializes bits as characters.
- Requires Python 3.10 or newer; `bin(i).count("1")` is the portable stand-in at the same asymptotics with a larger constant.

## Comparison of Solutions

The practice harness's `practice/counting_bits/reference.py` implements the **Bottom-Up DP with Lowest Set Bit** solution.

### Time Complexity

- **Per-Value Count**: `O(n log n)` - each value independently rendered and scanned over its bits.
- **Bottom-Up DP**: `O(n)` - one constant transition per entry.
- **Bottom-Up DP with Lowest Set Bit**: `O(n)` - one constant transition per entry.
- **Bottom-Up DP with Offset**: `O(n)` - one constant transition per entry plus at most one doubling.
- **Built-in Popcount**: `O(n)` - one native popcount per value.

### Space Complexity

- **Per-Value Count**: `O(n)` - the output list.
- **Bottom-Up DP**: `O(n)` - the output table.
- **Bottom-Up DP with Lowest Set Bit**: `O(n)` - the output table.
- **Bottom-Up DP with Offset**: `O(n)` - the output table plus one scalar.
- **Built-in Popcount**: `O(n)` - the output list.

### Trade-offs

- The Per-Value Count is the definition written down; it pays an extra `log` factor for ignoring that its answers share structure.
- The three DP variants reach the same linear-time table through three lenses: the dropped last bit, the erased lowest set bit, and the top-bit offset. Same asymptotics, different reads.
- The Built-in Popcount matches the DP time with the smallest constant, but skips the recurrence the problem exists to teach.

### When to Use Each

- **Per-Value Count**: a correctness baseline, or a language without cheap bit tricks.
- **Bottom-Up DP**: when the shift relation is the easiest to explain; it generalizes to "popcount of i in terms of any prefix property of i >> 1".
- **Bottom-Up DP with Lowest Set Bit** (recommended): the canonical answer, connecting the problem to the Kernighan erase identity and reading the most predictable neighbors.
- **Bottom-Up DP with Offset**: when presenting to an audience that thinks in blocks rather than bits; the doubling guard is its whole machinery.
- **Built-in Popcount**: in production Python 3.10+, where `bit_count()` is the right call and the interview is over.

### Optimization Notes

- All three recurrences write each entry exactly once and read only finalized entries, so they extend to streaming: `dp` can be emitted incrementally for an unknown upper bound.
- The DP table needs no extra memory beyond the required output; beware solutions that build a second table, which doubles allocation for no benefit.
- The table is highly compressible: `dp[2^k .. 2^(k+1) - 1]` equals `dp[0 .. 2^k - 1]` each plus one, so the whole table is derivable block by block if only queries are needed.
- For repeated queries on arbitrary `i` below a known cap, precompute the table once and answer each query in `O(1)`; the per-value approaches would redo the work per query.
