# [Longest Subarray with K Distinct Values](https://www.fastprep.io/problems/amazon-longest-subarray-with-k-distinct)

**Medium** | **NN minutes** | **Array, Hash Table, Sliding Window**

Given an integer array nums and an integer k, return the longest contiguous subarray containing exactly k distinct values.

If several subarrays have the same maximum length, return the one with the smallest starting index. Return an empty array when no subarray contains exactly k distinct values.

## Examples

### Example 1

**Input:** `nums = [1,2,1,2,3]`, `k = 2`

**Output:** `[1,2,1,2]`

**Explanation:** The prefix [1,2,1,2] has exactly two distinct values and is the longest valid subarray.

### Example 2

**Input:** `nums = [1,2,1,3,4]`, `k = 3`

**Output:** `[1,2,1,3]`

**Explanation:** Two length-four windows are valid. The earliest one starts at index 0.

### Example 3

**Input:** `nums = [1,1,1]`, `k = 2`

**Output:** `[]`

**Explanation:** No subarray contains two distinct values.

## Constraints

- `1 <= nums.length <= 100000.`
- `-10^9 <= nums[i] <= 10^9.`
- `1 <= k <= nums.length.`

## Solutions

### Brute Force

#### Derivation

The most literal reading tries every subarray: fix a start, extend an end, and keep a set of the distinct values seen so far. Two early exits keep the scan honest: the moment the set holds more than `k` values the subarray is invalid and no extension of it can recover, so the inner loop breaks; while the set holds exactly `k` values, every current end is a valid candidate and the longest one at this start is recorded before the set can overflow:

1. Track `best_start` and `best_length`, initially `0` and `0`, so an empty slice
   is the fallback answer when nothing qualifies.
2. For each `start`, grow `window_values`, a set of the values in
   `nums[start .. end]`.
3. Break the inner loop when `len(window_values) > k`: extending only ever adds
   values.
4. When `len(window_values) == k`, compare `end - start + 1` against
   `best_length` and keep the larger.
5. Return `nums[best_start : best_start + best_length]`.

The strict `>` comparison carries the tie-break: because `start` increases across iterations, a later equal-length candidate never displaces an earlier one, so the smallest starting index wins.

#### Walkthrough

Let us run the Brute Force on Example 1: `nums = [1,2,1,2,3]`, `k = 2`. Each line is one inner-loop visit, showing the set after absorbing the new value and the decision taken:

```text
start=0   end=0  {1}         1 distinct, below k
          end=1  {1,2}       == k -> length 2, best = (start 0, length 2)
          end=2  {1,2}       == k -> length 3, best = (start 0, length 3)
          end=3  {1,2}       == k -> length 4, best = (start 0, length 4)
          end=4  {1,2,3}     > k -> break
start=1   end=2  {2}
          end=3  {1,2}       == k -> length 2, not > 4
          end=4  {1,2,3}     > k -> break
start=2   end=3  {1,2}       == k -> length 2, not > 4
          end=4  {1,2,3}     > k -> break
start=3   end=4  {2,3}       == k -> length 2, not > 4
start=4   end=4  {3}         1 distinct, below k
```

No later start beats the length-4 window recorded at `start=0`, and the scan ends with `best = (start 0, length 4)`. The returned slice is `nums[0:4] = [1,2,1,2]`, matching Example 1's Output.

#### Solution

The code is the walkthrough's double loop with its two early exits: the overflow `break` and the exact-match candidate record.

```python
from typing import List


class Solution:
    def longestSubarrayWithKDistinct(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        best_start, best_length = 0, 0

        for start in range(n):
            window_values = set()
            for end in range(start, n):
                window_values.add(nums[end])
                if len(window_values) > k:
                    break
                if len(window_values) == k:
                    length = end - start + 1
                    if length > best_length:
                        best_start, best_length = start, length

        return nums[best_start:best_start + best_length]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each start scans forward until the set overflows or the array ends; with few distinct values overall (the case that rewards this problem) the inner loop runs nearly to the end for every start, so the work is quadratic in the worst case.

##### Space Complexity: `O(k)`

The set never holds more than `k + 1` values: the overflow check breaks the loop the moment one value too many enters.

#### Key Insights

- The overflow `break` is sound because distinctness is monotone under extension: a superset of an invalid window is invalid.
- Recording only on strict improvement is what implements the smallest-starting-index tie-break for free.
- The quadratic cost comes from rebuilding every window from its start, work the sliding window refuses to repeat.

### Binary Search on Answer Length

#### Derivation

The Brute Force pays `O(n)` per start. A different cut: ask a yes-or-no question about a length, "is there a valid subarray of length at least `L`?", and note the predicate is monotone. If a valid subarray has length `W >= L`, that same subarray also has length `W >= L - 1`, so every false must sit above every true and [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) applies. Each feasibility check is a fixed-width scan: slide a window of length exactly `L` across the array, maintaining its value counts incrementally (remove the outgoing value, add the incoming one), and report the first position where the window holds exactly `k` distinct values. After the search pins down the maximum length, the recorded position from its winning check supplies the smallest starting index:

1. Define `earliest_start(length)` as above, returning `-1` when no window of
   exactly that length qualifies.
2. Binary search `low` in `1..n`: on a hit record `(start, mid)` and search
   higher (`low = mid + 1`); on a miss search lower (`high = mid - 1`).
3. Return `nums[best_start : best_start + best_length]`, the empty slice when
   no length qualified.

The witness argument closes the loop: the search stops at the largest `L` whose check succeeded, and the witness for that check is a valid subarray of length exactly `L`, because anything longer would have made the next length up succeed too.

#### Walkthrough

Let us binary search Example 2: `nums = [1,2,1,3,4]`, `k = 3`. Three checks, each scanning fixed windows of length `mid`:

```text
low=1 high=5   mid=3   windows: [1,2,1]->2  [2,1,3]->3  <- hit at start 1
               feasible -> best = (start 1, length 3), low=4
low=4 high=5   mid=4   windows: [1,2,1,3]->3  <- hit at start 0
               feasible -> best = (start 0, length 4), low=5
low=5 high=5   mid=5   windows: [1,2,1,3,4]->4  no window has 3 distinct
               infeasible -> high=4
low=5 > high=4 -> stop
```

The search settles on length `4` with start `0`, so the returned slice is `nums[0:4] = [1,2,1,3]`, matching Example 2's Output. The slide discipline inside a check is incremental: moving from `[1,2,1]` to `[2,1,3]` removes one `1` (its count drops to `1`, not to zero, so the entry stays) and adds one `3`, which is why each window costs constant work.

#### Solution

The code is the fixed-width sliding check, wrapped in the binary search that bisects the width.

```python
from typing import List


class Solution:
    def longestSubarrayWithKDistinct(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)

        def earliest_start(length: int) -> int:
            window_counts = {}
            for position in range(length):
                window_counts[nums[position]] = window_counts.get(nums[position], 0) + 1
            if len(window_counts) == k:
                return 0
            for start in range(1, n - length + 1):
                outgoing = nums[start - 1]
                window_counts[outgoing] -= 1
                if window_counts[outgoing] == 0:
                    del window_counts[outgoing]
                incoming = nums[start + length - 1]
                window_counts[incoming] = window_counts.get(incoming, 0) + 1
                if len(window_counts) == k:
                    return start
            return -1

        best_start, best_length = 0, 0
        low, high = 1, n
        while low <= high:
            mid = (low + high) // 2
            start = earliest_start(mid)
            if start != -1:
                best_start, best_length = start, mid
                low = mid + 1
            else:
                high = mid - 1

        return nums[best_start:best_start + best_length]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

The search runs `O(log n)` rounds and each round slides a fixed window across the array once, at constant dict work per step.

##### Space Complexity: `O(n)`

The count map holds one entry per distinct value inside the current `mid`-length window; an invalid window can hold up to `mid` distinct values, and `mid` reaches `n`.

#### Key Insights

- The monotone predicate is about existence at a length, not about the windows themselves: a longer valid subarray is a witness for every smaller length, which is why the bisection is sound despite exact-`k` validity not being closed under shrinking a window by one element.
- Each round's answer is discarded except the last winner, whose recorded start is the smallest starting index among windows of the maximal length.
- The fixed-width scan trades the shrink logic of a variable window for a log-factor of extra scans; it buys a question ("does length `L` exist?") that is easier to reason about than the variable-window invariant.

### Sliding Window with Exactly-K Shrink

#### Derivation

The Brute Force rebuilds every window from its start, yet consecutive windows share all but one element: `[left .. right]` and `[left .. right + 1]` differ by a single arrival, and `[left + 1 .. right]` differs from `[left .. right]` by a single departure. A [sliding window](https://usaco.guide/silver/two-pointers) keeps one running window and pays for each element's entry and exit exactly once. The discipline rests on the same monotonicity the Brute Force used: distinctness never decreases when the window grows and never increases when it shrinks. So for each `right`, the window is grown to include `nums[right]`, then `left` advances, evicting values whose counts drop to zero, until the window holds at most `k` distinct values. Two outcomes are possible at that moment, and both are handled: exactly `k` distinct values means the window ending at `right` is valid with the smallest possible `left` for this `right` (the previous `left` had `k + 1`), so it is a candidate; fewer than `k` means no window ending at `right` can be valid, because every smaller `left` holds no more elements:

1. Keep `window_counts`, a dict of value -> count inside the window.
2. For each `right`, add `nums[right]` to `window_counts`.
3. While `len(window_counts) > k`, evict `nums[left]` (deleting its entry when
   the count reaches zero) and advance `left`.
4. When `len(window_counts) == k`, compare `right - left + 1` against
   `best_length` with a strict `>`, keeping the earlier window on ties.
5. Return `nums[best_start : best_start + best_length]`.

Each element enters once and leaves once, so the two pointers together make one linear pass.

#### Walkthrough

Let us slide the window over Example 1: `nums = [1,2,1,2,3]`, `k = 2`. Each line is one arrival, showing the count map, the shrink that follows it, and the decision:

```text
right=0 value 1   counts {1:1}              distinct 1 < k, extend
right=1 value 2   counts {1:1, 2:1}         distinct == k -> length 2, best = (0, 2)
right=2 value 1   counts {1:2, 2:1}         distinct == k -> length 3, best = (0, 3)
right=3 value 2   counts {1:2, 2:2}         distinct == k -> length 4, best = (0, 4)
right=4 value 3   counts {1:2, 2:2, 3:1}    distinct 3 > k, shrink:
                    evict nums[0]=1  {1:1, 2:2, 3:1}  still 3 distinct
                    evict nums[1]=2  {1:1, 2:1, 3:1}  still 3 distinct
                    evict nums[2]=1  {2:1, 3:1}       2 distinct, left=3
                  length 2, not > 4
```

The shrink stops exactly when the third distinct value leaves, and the recovered window `[2,3]` is far shorter than the recorded best. The final slice is `nums[0:4] = [1,2,1,2]`, matching Example 1's Output. For Example 3 (`nums = [1,1,1]`, `k = 2`) the count map never reaches 2 distinct values, no candidate is ever recorded, and the `0`-length fallback returns the empty slice `[]`.

#### Solution

The code is the walkthrough's arrival-evict-record loop over one shared count map.

```python
from typing import List


class Solution:
    def longestSubarrayWithKDistinct(self, nums: List[int], k: int) -> List[int]:
        window_counts = {}
        left = 0
        best_start, best_length = 0, 0

        for right, value in enumerate(nums):
            window_counts[value] = window_counts.get(value, 0) + 1

            while len(window_counts) > k:
                outgoing = nums[left]
                window_counts[outgoing] -= 1
                if window_counts[outgoing] == 0:
                    del window_counts[outgoing]
                left += 1

            if len(window_counts) == k:
                length = right - left + 1
                if length > best_length:
                    best_start, best_length = left, length

        return nums[best_start:best_start + best_length]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each element is added to the count map once when `right` absorbs it and removed once when `left` evicts it, so the total work across both pointers is linear; dict operations are constant time on average.

##### Space Complexity: `O(k)`

The count map holds at most `k + 1` entries: the shrink loop runs the moment one value too many enters, and it evicts until the overflow is gone.

#### Key Insights

- The shrink only ever needs to restore the at-most-`k` invariant; once it holds, exactly-`k` is either true or unreachable for this `right`, so no extra probing is needed.
- After the shrink, `left` is minimal for the current `right`, which is what makes the recorded length the longest valid window ending there; across all `right`, the global maximum falls out.
- Deleting a count-map entry when its count reaches zero keeps `len(window_counts)` a true distinct-value counter; leaving zero-count entries behind would silently break the `> k` test.
- The strict `>` in the candidate check preserves the smallest-starting-index tie-break without any extra bookkeeping.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - every start rebuilds its window from scratch until the set overflows.
- **Binary Search on Answer Length**: `O(n log n)` - `O(log n)` feasibility rounds, each one linear fixed-window scan.
- **Sliding Window with Exactly-K Shrink**: `O(n)` - each element enters and leaves the window once.

### Space Complexity

- **Brute Force**: `O(k)` - the value set breaks at `k + 1` entries.
- **Binary Search on Answer Length**: `O(n)` - the fixed window's count map can hold up to `mid` distinct values for an invalid window.
- **Sliding Window with Exactly-K Shrink**: `O(k)` - the count map breaks at `k + 1` entries before the shrink restores the invariant.

### Trade-offs

- The Brute Force approach is the shortest to derive and carries the tie-break naturally, but the full-input constraint of `10^5` elements makes its quadratic worst case unusable in an OA setting.
- The Binary Search on Answer Length approach replaces window reasoning with a monotone existence question, which is easier to argue correct, at the cost of a `log n` factor and a fixed-window count map that loses the `O(k)` space bound.
- The Sliding Window with Exactly-K Shrink approach is linear in time and near-constant in space, but its correctness rests on the subtler invariant that the post-shrink `left` is minimal for each `right`.

### When to Use Each

- **Brute Force**: As a correctness reference while designing tests, or when the input is known to stay small.
- **Binary Search on Answer Length**: When the interviewer frames the problem as an existence question, or as a stepping stone: the monotone-predicate argument is worth rehearsing even when the linear solution exists.
- **Sliding Window with Exactly-K Shrink (Recommended)**: The default for the real OA: single pass, `O(k)` memory, and the same discipline transfers to the whole family of distinct-value window problems.

### Optimization Notes

- The Brute Force recomputes each window from its start; the sliding window reuses all but one element per step, which is where the quadratic-to-linear drop comes from.
- All three approaches return the answer as a single slice of the input, so the subarray is never copied element by element: `nums[best_start:best_start + best_length]` with `best_length = 0` doubles as the empty-array fallback for Example 3.
- The exactly-`k` family has a well-known counting variant (number of subarrays with exactly `k` distinct, via at-most-`k` minus at-most-`k-1`); that trick does not transfer to finding the longest window, because the two at-most windows it subtracts do not identify a subarray.
- In the sliding window, the count-map entry deletion on zero is the load-bearing line: with it, `len(window_counts)` is the distinct count; without it, every window's history accumulates and the overflow test never fires.
