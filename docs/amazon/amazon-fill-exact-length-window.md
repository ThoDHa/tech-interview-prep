# [Fill One Exact-Length Binary Window](https://www.fastprep.io/problems/amazon-fill-exact-length-window)

**Easy** | **NN minutes** | **String, Prefix Sum**

Given a binary string log and an integer k, choose exactly one contiguous substring of length k. Change every 0 inside it to 1. Ones inside the window and all characters outside it stay unchanged.

## Examples

### Example 1

**Input:** `log = "11001"`, `k = 2`

**Output:** `5`

**Explanation:** Choose the two zeros at indices 2 and 3 in 11001. Filling that length-2 window gives 11111, so the answer is 5.

## Constraints

- `For this exercise, assume 1 <= log.length <= 100000.`
- `1 <= k <= log.length.`
- `Every character of log is 0 or 1.`

## Deriving the Solution

Filling a window can only turn zeros into ones, so the question "which window is best?" decomposes: the string's ones outside the window never change, the ones inside stay ones, and the window contributes its own length minus the ones it already held. The whole problem is one number per window, its zero count, and the ladder is about computing those numbers without rebuilding anything:

1. **Start literal.** Rebuild the filled string for every candidate window and count its ones: correct, and it re-reads the whole string per window: see [Rebuild Every Window](#rebuild-every-window).
2. **Decompose the answer.** The result is `total ones + zeros in the chosen window`, and a window's zero count is `k` minus its one count, which is a range sum over the string: prefix sums answer every window in one subtraction: see [Prefix Sums](#prefix-sums).
3. **Hand the running total to the library.** `itertools.accumulate` builds the prefix array from one expression: see [Accumulate Prefix Sums](#accumulate-prefix-sums).

## Solutions

### Rebuild Every Window

#### Derivation

The statement's most literal reading: try every window by doing exactly what the operation says. Splice the string with the window's zeros replaced, count the ones of the result, and keep the best:

1. For each `start` from 0 through `len(log) - k`:
2. Build `filled = log[:start] + log[start:start + k].replace("0", "1") + log[start + k:]`.
3. Keep the maximum of `filled.count("1")` over all windows.

#### Walkthrough

Example 1 (`log = "11001"`, `k = 2`), all four windows rebuilt:

```text
start 0   fill "11" -> 11101   ones 4
start 1   fill "10" -> 11101   ones 4
start 2   fill "00" -> 11111   ones 5   <- best
start 3   fill "01" -> 11011   ones 4
```

The best rebuild is `11111` with 5 ones, matching the expected Output: the window over indices 2 and 3 swallows both zeros.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, log: str, k: int) -> int:
        best = 0
        for start in range(len(log) - k + 1):
            filled = log[:start] + log[start:start + k].replace("0", "1") + log[start + k:]
            best = max(best, filled.count("1"))
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

`n - k + 1` windows, each rebuild and count reading the whole length-`n` string.

##### Space Complexity: `O(n)`

One rebuilt string at a time.

#### Key Insights

- The rebuilds share almost everything: consecutive windows differ in two boundary characters, yet each is assembled and counted from scratch.
- The count of ones outside the window is the same for every window, which is the observation the next approach factors out.

### Prefix Sums

#### Derivation

Spelling out what the rebuild computes: outside the window nothing changes, inside it every character becomes a one. So the rebuilt count is `ones(log) + zeros in the window`, and only the second term depends on the window. A window's zero count is `k` minus its one count, and a range's one count is a difference of two prefix sums, `prefix[s + k] - prefix[s]`. One array built in one pass, one subtraction per window:

1. Build `prefix` of length `n + 1`, where `prefix[i]` counts the ones in `log[:i]`; `prefix[n]` is the string's total ones.
2. For each `start`, the window's ones are `prefix[start + k] - prefix[start]`, its zeros `k` minus that.
3. Return `total_ones + max(0, best window zeros)` over all `start`.

#### Formula

The decomposition the code evaluates, with `n = len(log)` and `W(s) = log[s:s+k]`:

$$ \text{answer} = \text{ones}(\log) + \max_s\ \big(k - (\text{prefix}[s + k] - \text{prefix}[s])\big) $$

```text
answer    = ones(log) + max over s of (k - (prefix[s + k] - prefix[s]))
prefix[0] = 0
prefix[i] = prefix[i - 1] + (log[i - 1] == '1')
```

`ones(log)` is `prefix[n]`, so the same array serves both terms; the max is taken over the `n - k + 1` legal window starts, and it is at least the zeros of any single window, never negative since `k >= 1`.

#### Walkthrough

Example 1 (`log = "11001"`, `k = 2`). The prefix array grows left to right:

```text
log        1  1  0  0  1
prefix  0  1  2  2  2  3        total ones = prefix[5] = 3

start 0   ones in window = prefix[2] - prefix[0] = 2   zeros 0   -> 3 + 0
start 1   ones in window = prefix[3] - prefix[1] = 1   zeros 1   -> 3 + 1
start 2   ones in window = prefix[4] - prefix[2] = 0   zeros 2   -> 3 + 2
start 3   ones in window = prefix[5] - prefix[3] = 1   zeros 1   -> 3 + 1
```

The best window is start 2 with 2 zeros, so the answer is `3 + 2 = 5`, matching the expected Output.

#### Solution

The code is the formula written down: build `prefix` once, then one subtraction and one comparison per window.

```python
from typing import List


class Solution:
    def solve(self, log: str, k: int) -> int:
        prefix: List[int] = [0]
        for digit in log:
            prefix.append(prefix[-1] + (digit == "1"))
        total_ones = prefix[-1]
        best_zeros = 0
        for start in range(len(log) - k + 1):
            ones_in_window = prefix[start + k] - prefix[start]
            best_zeros = max(best_zeros, k - ones_in_window)
        return total_ones + best_zeros
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass builds the prefix array; one pass over the `n - k + 1` windows does constant work each.

##### Space Complexity: `O(n)`

The prefix array of `n + 1` running totals.

#### Key Insights

- "Fill the zeros in one window" converts to "add the window's zero count to the total": the window is the only thing that varies, so only it needs computing.
- Maximizing zeros and minimizing ones are the same question under `zeros = k - ones`; both are range sums, and range sums are what prefix arrays exist for.
- The rebuild's `O(n^2)` collapses because prefix sums precompute every range answer the windows will ever ask.

### Accumulate Prefix Sums

#### Derivation

The Prefix Sums version builds its array with an explicit loop appending each running total. [`itertools.accumulate`](https://docs.python.org/3/library/itertools.html#itertools.accumulate) expresses exactly that: a running binary operation over the input. Mapping the digits to their indicator first (`digit == "1"` as 0/1) lets `accumulate` emit the prefix array in one expression, and the window loop is unchanged:

1. Build `prefix` as `[0]` extended by `accumulate(digit == "1" for digit in log)`, the digit indicators accumulated in place so positions align with the string.
2. Evaluate the windows exactly as in the Prefix Sums version.

#### Walkthrough

Example 1 again. `accumulate` consumes the digit indicators (`1` for a one, `0` for a zero) and emits `[1, 2, 2, 2, 3]`, which the leading 0 splices into `[0, 1, 2, 2, 2, 3]`, the same array as the Prefix Sums trace; the window evaluation and the answer `3 + 2 = 5` are identical.

#### Solution

```python
from itertools import accumulate
from typing import List


class Solution:
    def solve(self, log: str, k: int) -> int:
        prefix = [0, *accumulate(digit == "1" for digit in log)]
        total_ones = prefix[-1]
        best_zeros = 0
        for start in range(len(log) - k + 1):
            ones_in_window = prefix[start + k] - prefix[start]
            best_zeros = max(best_zeros, k - ones_in_window)
        return total_ones + best_zeros
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

`accumulate` makes one pass over the digits; the window loop is unchanged.

##### Space Complexity: `O(n)`

The same prefix array, built by the library iterator.

#### Key Insights

- `accumulate` is the running-total loop with the bookkeeping removed; the algorithm and its bounds are the previous section's.
- The digits enter `accumulate` as their 0/1 indicators, zeros included: filtering the zeros out would shift every prefix index off the string's positions, turning the window differences into counts between consecutive ones.
- The library iterator cannot fill a leading 0, so the explicit `[0, ...]` splice remains, exactly as the hand-rolled version's seed.

## Comparison of Solutions

### Time Complexity

- **Rebuild Every Window**: `O(n^2)` - a full rebuild and count per window.
- **Prefix Sums**: `O(n)` - one build pass and constant work per window.
- **Accumulate Prefix Sums**: `O(n)` - the same passes with the build loop handed to the library.

### Space Complexity

- **Rebuild Every Window**: `O(n)` - one rebuilt string at a time.
- **Prefix Sums**: `O(n)` - the prefix array.
- **Accumulate Prefix Sums**: `O(n)` - the same array from an iterator.

### Trade-offs

- **Rebuild Every Window**: the operation performed literally and the easiest to trust; quadratic work rules it out on long logs.
- **Prefix Sums**: linear time from one observation about what the fill actually changes.
- **Accumulate Prefix Sums**: identical bounds with the build loop removed; relies on `itertools`, at none of the hand-rolled version's readability cost.

### When to Use Each

- **Rebuild Every Window**: as the baseline to state first, and as the independent checker for the other two.
- **Prefix Sums (Recommended)**: the interview answer: state the decomposition, build the array, one subtraction per window.
- **Accumulate Prefix Sums**: the idiomatic Python form once the approach is settled.

### Optimization Notes

- **Prefix Sums** is the recommended choice: linear time, one array, and every window answered by a single subtraction.
- The window's zero count can be computed directly as `(prefix[s + k] - prefix[s])` subtracted from `k`; keeping zeros in the expression mirrors the statement's wording and avoids one sign slip.
- Two sliding-window variants reach the same bound without an array: a running count over the first window moved by its two edges, or `max` over `itertools.pairwise` of the prefix array at distance `k`; both are bookkeeping choices, not complexity changes.
