# [Minimum Operations to Make an Array Continuous](https://www.fastprep.io/problems/amazon-minimum-operations-to-make-array-continuous)

**Hard** | **NN minutes** | **Array, Sorting, Binary Search, Sliding Window**

You are given a non-empty integer array nums of length n. In one operation, you may replace any one element with any integer.

An array is continuous when both conditions hold:

All n elements are unique.The difference between the maximum and minimum elements is exactly n - 1.Return the minimum number of replacement operations needed to make nums continuous.

## Examples

### Example 1

**Input:** `nums = [4,2,5,3]`

**Output:** `0`

**Explanation:** The values are already the unique consecutive set {2,3,4,5}.

### Example 2

**Input:** `nums = [1,2,3,5,6]`

**Output:** `1`

**Explanation:** Replace 1 with 4 to obtain the continuous set {2,3,4,5,6}.

### Example 3

**Input:** `nums = [1,10,100,1000]`

**Output:** `3`

**Explanation:** At most one existing value can be retained inside any interval containing four consecutive integers, so three elements must be replaced.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-minimum-operations-to-make-array-continuous; fill them in. -->

## Solutions

### Brute Force Window Scan

#### Derivation

The replacement target is fully determined once we know which elements survive: the survivors must be distinct values that fit inside some block of `total` consecutive integers, and every other element can be rewritten to fill the gaps. A block of `total` consecutive integers contains at most `total` distinct values, and only values already present in `nums` are worth keeping, so every candidate survivor set is a run of consecutive entries inside the sorted distinct values of `nums`. The most literal reading is therefore: enumerate every window of the sorted distinct array, keep the largest window whose span fits, and replace everything else:

1. Build `unique_values = sorted(set(nums))`; a duplicate can never keep two
   survivors, so deduplicating first loses nothing.
2. Set `span_limit = total - 1`, the largest legal difference inside the final
   block.
3. For every `window_start`, extend `window_end` upward while
   `unique_values[window_end] - unique_values[window_start] <= span_limit`,
   tracking the largest window length in `best_kept`; break the inner loop at
   the first value that overshoots, because longer `window_end` values only
   widen the span.
4. Return `total - best_kept`: each surviving value keeps one element, and the
   remaining `total - best_kept` elements each cost one replacement.

#### Walkthrough

Example 3, `nums = [1,10,100,1000]`, has `total = 4` and `span_limit = 3`; the sorted distinct values are `[1, 10, 100, 1000]`:

```text
window_start=0 (value 1):    window_end=1: 10 - 1 = 9 > 3   -> break, best_kept stays 1
window_start=1 (value 10):   window_end=2: 100 - 10 = 90 > 3  -> break
window_start=2 (value 100):  window_end=3: 1000 - 100 = 900 > 3  -> break
window_start=3 (value 1000): span to itself is 0 <= 3, best_kept = 1
```

No pair of values lands within a span of `3`, so no window ever grows past one value. The function returns `total - best_kept = 4 - 1 = 3`, matching the expected Output.

#### Solution

The code is the double scan from the walkthrough: outer loop picks `window_start`, inner loop stretches `window_end` until the span breaks.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        unique_values = sorted(set(nums))
        total = len(nums)
        span_limit = total - 1
        best_kept = 1

        for window_start in range(len(unique_values)):
            for window_end in range(window_start, len(unique_values)):
                if unique_values[window_end] - unique_values[window_start] > span_limit:
                    break
                best_kept = max(best_kept, window_end - window_start + 1)

        return total - best_kept
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Sorting costs `O(n log n)`, but the nested scan over distinct values dominates in the worst case: when many distinct values cluster inside a span of `n - 1`, the inner loop walks a long stretch for every `window_start`.

##### Space Complexity: `O(n)`

The sorted copy of the distinct values; `set` and `sorted` each hold up to `n` elements.

#### Key Insights

- The answer is `total - best_kept`, not a count of edits computed one element at a time: once the survivor set is fixed, every other element can always be rewritten into the gaps of the consecutive block.
- Duplicates never survive twice; each kept value retains one element, which is why working over distinct values is safe.
- Breaking the inner loop at the first overshoot is correct because the span `unique_values[window_end] - unique_values[window_start]` only grows as `window_end` advances.

### Binary Search per Value

#### Derivation

The brute force re-derives, for every `window_start`, the same fact a sorted array can answer directly: how many distinct values fit inside `[unique_values[window_start], unique_values[window_start] + span_limit]`? [Binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) answers that count in one lookup, because the right boundary of the window is a value, not an index: everything from `window_start` up to (but not including) `bisect_right(unique_values, window_start + span_limit)` fits. The window search disappears into a single `bisect` call per start:

1. Build `unique_values = sorted(set(nums))` and `span_limit = total - 1` as
   before.
2. For each index `window_start`, compute `kept_end = bisect_right(unique_values,
   unique_values[window_start] + span_limit)`; all values in
   `unique_values[window_start:kept_end]` fit inside one legal block.
3. Track the largest `kept_end - window_start` in `best_kept`.
4. Return `total - best_kept`.

#### Walkthrough

Example 2, `nums = [1,2,3,5,6]`, gives `unique_values = [1,2,3,5,6]`, `total = 5`, `span_limit = 4`. Each row is one `window_start` and the window its binary search produces:

```text
window_start=0  value 1:   bound 1+4=5   bisect_right -> 4  window [1,2,3,5]    kept 4
window_start=1  value 2:   bound 2+4=6   bisect_right -> 5  window [2,3,5,6]    kept 4
window_start=2  value 3:   bound 3+4=7   bisect_right -> 5  window [3,5,6]      kept 3
window_start=3  value 5:   bound 5+4=9   bisect_right -> 5  window [5,6]        kept 2
window_start=4  value 6:   bound 6+4=10  bisect_right -> 5  window [6]          kept 1
```

`best_kept` reaches `4` on the first two starts: the survivor set `{1,2,3,5}` or `{2,3,5,6}` spans exactly `4 - 0 = 4` or `6 - 2 = 4`, both legal. The function returns `5 - 4 = 1`, matching the expected Output.

#### Solution

The code is the per-start lookup from the walkthrough, with `bisect_right` supplying the window's right edge.

```python
from bisect import bisect_right
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        unique_values = sorted(set(nums))
        total = len(nums)
        span_limit = total - 1
        best_kept = 1

        for window_start in range(len(unique_values)):
            kept_end = bisect_right(unique_values, unique_values[window_start] + span_limit)
            best_kept = max(best_kept, kept_end - window_start)

        return total - best_kept
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting costs `O(n log n)` and each of the up-to-`n` distinct values triggers one `O(log n)` binary search.

##### Space Complexity: `O(n)`

The sorted copy of the distinct values.

#### Key Insights

- A window defined by values instead of indices (`value + span_limit` as the upper bound) turns "how far can this window extend" into one `bisect_right` call.
- `bisect_right` rather than `bisect_left` is what makes the boundary inclusive: a value equal to the bound has span exactly `span_limit` and must be kept.
- The improvement over the brute force is per-start work dropping from a linear stretch to a logarithmic lookup, at the cost of trusting the sorted-order invariant.

### Sliding Window over Unique Values

#### Derivation

The binary search still pays `O(log n)` per start for information the previous start already possessed: as `window_start` moves right, the right edge of the window can only move right or stay, never retreat. That monotonicity is exactly the invariant a [sliding window](https://en.wikipedia.org/wiki/Two-pointer_technique) exploits: advance `window_end` once per step and let `window_start` creep forward only when the span breaks, so both pointers together traverse the array once:

1. Build `unique_values = sorted(set(nums))`, `span_limit = total - 1`, and
   `best_kept = 1`.
2. Advance `window_end` across `unique_values`; before measuring, shrink the
   window by moving `window_start` forward while
   `unique_values[window_end] - unique_values[window_start] > span_limit`.
3. After the shrink, the window `[window_start, window_end]` is the longest
   legal window ending at `window_end`; record its length in `best_kept`.
4. Return `total - best_kept`.

#### Walkthrough

Example 2 again, `unique_values = [1,2,3,5,6]` with `span_limit = 4`. Each line is one `window_end` step, showing the shrink pass and the window it leaves behind:

```text
window_end=0  value 1:  1 - 1 = 0 <= 4   no shrink   window [1]        best_kept = 1
window_end=1  value 2:  2 - 1 = 1 <= 4   no shrink   window [1,2]      best_kept = 2
window_end=2  value 3:  3 - 1 = 2 <= 4   no shrink   window [1,2,3]    best_kept = 3
window_end=3  value 5:  5 - 1 = 4 <= 4   no shrink   window [1,2,3,5]  best_kept = 4
window_end=4  value 6:  6 - 1 = 5 > 4    window_start -> 1
                        6 - 2 = 4 <= 4   stop        window [2,3,5,6]  best_kept = 4
```

The single shrink at `window_end = 4` drops the stale value `1`, and the window settles at `[2,3,5,6]` with span exactly `4`. No later step can beat it, so the function returns `5 - 4 = 1`, matching the expected Output. (Example 1 ends with the full window `[2,3,4,5]` and `best_kept = 4`, returning `0`; Example 3 never grows past `best_kept = 1` and returns `3`.)

#### Solution

The code is the walkthrough's two pointers: `window_end` advances every iteration, `window_start` only when the span forces it.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        unique_values = sorted(set(nums))
        total = len(nums)
        span_limit = total - 1
        best_kept = 1
        window_start = 0

        for window_end in range(len(unique_values)):
            while unique_values[window_end] - unique_values[window_start] > span_limit:
                window_start += 1
            best_kept = max(best_kept, window_end - window_start + 1)

        return total - best_kept
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting dominates; the sweep is linear because `window_start` and `window_end` each move forward at most `len(unique_values)` times.

##### Space Complexity: `O(n)`

The sorted copy of the distinct values.

#### Key Insights

- Sorting first is what creates the window property: in the original order the right edge could jump anywhere, but sorted spans only grow with `window_end`.
- The while-loop shrink keeps both pointers honest: each pointer advances at most once per element, so the sweep is `O(n)` despite the nested loop.
- A single-element window is always legal (span `0`), which is why `best_kept` starts at `1` and the answer for an already-scattered array is `total - 1`.

## Comparison of Solutions

### Time Complexity

- **Brute Force Window Scan**: `O(n^2)` - sorting is `O(n log n)` but the nested start/end scan over clustered distinct values dominates.
- **Binary Search per Value**: `O(n log n)` - one `O(log n)` `bisect_right` per distinct value on top of the sort.
- **Sliding Window over Unique Values**: `O(n log n)` - the sort dominates and the two-pointer sweep is linear.

### Space Complexity

- **Brute Force Window Scan**: `O(n)` - the sorted copy of the distinct values.
- **Binary Search per Value**: `O(n)` - the sorted copy of the distinct values.
- **Sliding Window over Unique Values**: `O(n)` - the sorted copy of the distinct values.

### Trade-offs

- **Brute Force Window Scan**: the most transparent translation of the problem into loops, and fine for small inputs, but quadratic behavior appears exactly when values cluster, the case real tests love.
- **Binary Search per Value**: logarithmic per-start work with a one-line core, but each lookup re-derives a boundary the neighboring start nearly shared.
- **Sliding Window over Unique Values**: asymptotically optimal after the sort and the shortest of the three, at the cost of reasoning about two pointers moving under an invariant instead of one self-contained lookup.

### When to Use Each

- **Brute Force Window Scan**: as the correctness baseline you write first and diff against; also fine when the distinct values are known to be scattered (few legal windows).
- **Binary Search per Value**: when the window-boundary formulation is easiest to argue, or when you need arbitrary "how many values fit above `v`" queries rather than one sweep.
- **Sliding Window over Unique Values (Recommended)**: the interview answer and the one to write under time pressure: linear after sorting, no library reliance beyond `sorted`.

### Optimization Notes

- Deduplicate before scanning: duplicates can never both survive, and skipping them can shrink the swept array dramatically for repeated-heavy inputs.
- `span_limit = total - 1` is fixed for the whole run, so precompute it once; recomputing `total - 1` inside the inner loop is the usual micro-slip.
- The `while` in the sliding window cannot run past `window_end` because `unique_values[window_end] - unique_values[window_end] = 0 <= span_limit` always holds, so no bounds guard is needed.
- All three approaches return `total - best_kept`; compute `best_kept` in whichever style you can defend fastest rather than micro-optimizing the constant.
