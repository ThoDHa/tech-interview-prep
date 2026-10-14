# [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/)

**Medium** | **30 minutes** | **Array, Binary Search**

**Pattern:** [Binary Search](../patterns/binary_search/intuition.md)

**Algorithm:** [Binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm)

**Practice:** [`practice/search_in_rotated_sorted_array/solution.py`](../../practice/search_in_rotated_sorted_array/solution.py)

There is an integer array `nums` sorted in ascending order (with distinct values).

Prior to being passed to your function, `nums` is possibly rotated at an unknown pivot index `k` (`1 <= k < nums.length`) such that the resulting array is `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]` (0-indexed). For example, `[0,1,2,4,5,6,7]` might be rotated at pivot index `3` and become `[4,5,6,7,0,1,2]`.

Given the array `nums` after the possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.

You must write an algorithm with `O(log n)` runtime complexity.

## Examples

### Example 1

**Input:** `nums = [4,5,6,7,0,1,2]`, `target = 0`

**Output:** `4`

### Example 2

**Input:** `nums = [4,5,6,7,0,1,2]`, `target = 3`

**Output:** `-1`

### Example 3

**Input:** `nums = [1]`, `target = 0`

**Output:** `-1`

## Constraints

- `1 <= nums.length <= 5000`
- `-10^4 <= nums[i] <= 10^4`
- All values of `nums` are unique.
- `nums` is an ascending array that is possibly rotated.
- `-10^4 <= target <= 10^4`

## Deriving the Solution

Rotating a sorted array of distinct values leaves two ascending runs laid end to end, with a single descending step at the pivot. Every logarithmic solution below exploits the consequence of that shape: any midpoint splits the array so that at least one of the two halves is fully sorted, and a sorted half can be tested against its endpoints.

1. **Start literal.** Ignore the structure and scan for `target` element by
   element. Always correct, but `O(n)` violates the required `O(log n)` bound: see [Linear Scan](#linear-scan).
2. **Restore the order first.** The pivot (the index of the minimum) is itself
   findable by a binary search, and it splits the array into two plain sorted runs. Binary search the runs with the standard algorithm: `O(log n)`, at the cost of two or three separate passes: see [Find Pivot then Binary Search](#find-pivot-then-binary-search).
3. **Handle the rotation inside one search.** The two-phase split pays a
   constant factor to avoid thinking about the pivot during the lookup. The sharper observation is that no pivot-finding is needed: at every probe, at least one half around `mid` is sorted, and comparing `target` against that half's exact endpoint bounds tells which half to discard. One pass, same `O(log n)`: see [Modified Binary Search](#modified-binary-search).

## Solutions

### Linear Scan

#### Derivation

The most direct reading of the problem ignores the rotated-sorted structure entirely and simply [walks the array](https://en.wikipedia.org/wiki/Linear_search) looking for `target`:

1. Iterate over the array, tracking each index.
2. Return the index as soon as an element equals `target`.
3. Return `-1` if the loop finishes without a match.

This always produces the correct answer and is the natural starting point, but it discards the ordering information that makes a logarithmic solution possible. The problem explicitly requires `O(log n)` runtime, so this baseline serves as a correctness reference rather than an acceptable submission.

#### Walkthrough

Let us scan Example 1 by hand: `nums = [4,5,6,7,0,1,2]`, `target = 0`. The loop compares each element to `target` in index order and stops at the first match:

```text
i = 0   num = 4   4 != 0, continue
i = 1   num = 5   5 != 0, continue
i = 2   num = 6   6 != 0, continue
i = 3   num = 7   7 != 0, continue
i = 4   num = 0   0 == 0, return 4
```

The scan walks straight past the pivot without noticing it and returns `4`, the expected Output. The cost is visible in the trace: five comparisons where the binary-search solutions below need three.

#### Solution

The code is the scan from the walkthrough: one comparison per element until the first match.

```python
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        for i, num in enumerate(nums):
            if num == target:
                return i
        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every element may be examined once in the worst case, when `target` is at the end or absent.

##### Space Complexity: `O(1)`

Only a loop index and the current value are stored.

#### Key Insights

- It is the easiest solution to reason about and verify, which makes it a useful oracle for testing the faster approaches.
- It violates the required `O(log n)` bound, demonstrating exactly what the binary-search refinements need to improve upon.
- It needs no special handling for rotation, single-element arrays, or non-rotated input.

### Find Pivot then Binary Search

#### Derivation

The Linear Scan discards the one guarantee the input offers: apart from a single descending step at the pivot, the array is sorted. If that step's position were known, the problem would collapse into ordinary [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) territory. So ask: can the pivot itself be found in `O(log n)`? It can, because the pivot is the unique minimum, and comparing `nums[mid]` to `nums[right]` always tells which side of `mid` it lies on. That decomposes the problem into two independent phases, each a familiar binary search:

1. Locate the rotation pivot, the index of the smallest element. If `nums[left] <= nums[right]` the array is not rotated and the pivot is index `0`. Otherwise binary search for the point where the descending step occurs: when `nums[mid] > nums[right]` the pivot lies to the right, so move `left = mid + 1`; otherwise the pivot is at `mid` or to its left, so set `right = mid`.
2. The pivot splits the array into two sorted runs, `[0, pivot - 1]` and `[pivot, n - 1]`. Run a standard binary search over the first run, and if the target is not found there, run it over the second.

Because each run is strictly ascending, the inner searches are ordinary binary searches with no rotation handling, which keeps the logic easy to verify.

#### Walkthrough

Let us trace both phases on Example 1: `nums = [4,5,6,7,0,1,2]`, `target = 0`. The indices are `0:4 1:5 2:6 3:7 4:0 5:1 6:2`.

**Phase 1, find the pivot.** First check `nums[left] <= nums[right]`, that is `nums[0]=4 <= nums[6]=2`: false, so the array is rotated and we binary search for the smallest element. Each step compares `nums[mid]` against `nums[right]`: if `nums[mid] > nums[right]` the smallest element is to the right (`left = mid + 1`), otherwise it is at `mid` or to its left (`right = mid`).

| Step | `left` | `right` | `mid` | `nums[mid]` | `nums[right]` | Decision |
|------|--------|---------|-------|-------------|---------------|----------|
| 1 | `0` | `6` | `3` | `7` | `2` | `7 > 2`, pivot right: `left = 4` |
| 2 | `4` | `6` | `5` | `1` | `2` | `1 <= 2`, pivot here/left: `right = 5` |
| 3 | `4` | `5` | `4` | `0` | `1` | `0 <= 1`, pivot here/left: `right = 4` |

Now `left == right == 4`, the loop ends, and `pivot = 4`: the index of the smallest value `0`.

**Phase 2, search the two sorted runs.** The pivot splits the array into `[0, 3] = [4,5,6,7]` and `[4, 6] = [0,1,2]`. Since `pivot > 0`, search the first run `binary_search(0, 3)`:

| Step | `start` | `end` | `mid` | `nums[mid]` | Decision |
|------|---------|-------|-------|-------------|----------|
| 1 | `0` | `3` | `1` | `5` | `5 > 0`: `end = 0` |
| 2 | `0` | `0` | `0` | `4` | `4 > 0`: `end = -1` |

The window empties, so the first run returns `-1`. Now search the second run `binary_search(4, 6)`:

| Step | `start` | `end` | `mid` | `nums[mid]` | Decision |
|------|---------|-------|-------|-------------|----------|
| 1 | `4` | `6` | `5` | `1` | `1 > 0`: `end = 4` |
| 2 | `4` | `4` | `4` | `0` | `0 == 0`: return `4` |

The search returns `4`, which matches the expected Output of `4`.

#### Solution

The code is the two phases from the walkthrough as helper closures: `find_pivot` first, then `binary_search` over each sorted run.

```python
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        def find_pivot() -> int:
            left, right = 0, len(nums) - 1
            if nums[left] <= nums[right]:  # not rotated
                return 0
            while left < right:
                mid = (left + right) // 2
                if nums[mid] > nums[right]:
                    left = mid + 1
                else:
                    right = mid
            return left

        def binary_search(start: int, end: int) -> int:
            while start <= end:
                mid = (start + end) // 2
                if nums[mid] == target:
                    return mid
                elif nums[mid] < target:
                    start = mid + 1
                else:
                    end = mid - 1
            return -1

        pivot = find_pivot()

        if pivot > 0:
            result = binary_search(0, pivot - 1)
            if result != -1:
                return result

        return binary_search(pivot, len(nums) - 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

Finding the pivot is one binary search and the value lookup is at most two more, each `O(log n)`, so the total is `O(log n)`.

##### Space Complexity: `O(1)`

Only constant pointer state is used; the helper closures allocate no additional data structures.

#### Key Insights

- A rotated ascending array of distinct values has exactly one pivot where `nums[i - 1] > nums[i]`, and that pivot is the unique minimum.
- Comparing `nums[mid]` against `nums[right]` (rather than `nums[left]`) reliably tells which side the pivot is on during the pivot search.
- Separating pivot-finding from the value lookup keeps each binary search standard, trading a slightly larger constant factor for conceptual clarity.

### Modified Binary Search

#### Derivation

The two-phase approach spends a whole [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) locating the pivot before it looks at `target` at all, and may run two more searches after it. Ask whether the pivot needs to be found at all: the rotation can be handled inside a single search. The key observation is that for any `mid`, at least one of the two halves `[left, mid]` and `[mid, right]` is fully sorted, and a sorted half can be tested exactly against its endpoints. The Invariant below states why that test is trustworthy; the loop it justifies is:

1. Compute `mid` and return immediately if `nums[mid]` equals `target`.
2. If `nums[left] <= nums[mid]`, the left half is sorted. When `nums[left] <= target < nums[mid]`, the target can only be in that sorted half, so set `right = mid - 1`; otherwise discard it with `left = mid + 1`.
3. Otherwise the right half is sorted. When `nums[mid] < target <= nums[right]`, search right with `left = mid + 1`; otherwise search left with `right = mid - 1`.
4. Return `-1` when the window empties.

Every decision is made against the exact bounds of a provably sorted half, so the target is never discarded by mistake.

#### Invariant

A rotation by \(r\) of a sorted array means:

$$ \text{nums}[i] = \text{sorted}\bigl[(i + r) \bmod n\bigr] $$

```text
nums[i] = sorted[(i + r) mod n]   for 0 <= i < n
          where r is the rotation amount and n = len(nums)
```

so the array is two ascending runs laid end to end, with a single descending step at the pivot. Any split point `mid` therefore leaves the pivot in at most one of the two halves. That gives the property the search rests on:

$$ \text{at least one of } [\textit{left},\ \textit{mid}] \text{ and } [\textit{mid},\ \textit{right}] \text{ is fully sorted} $$

```text
at least one of nums[left .. mid] and nums[mid .. right] is fully sorted
```

The test `nums[left] <= nums[mid]` identifies which. It holds exactly when the left half contains no pivot, so that half is ascending and its contents are bounded by its endpoints. For a target known to sit somewhere in the current window, membership in that sorted range is then a two-sided comparison:

$$ \text{if } \text{nums}[\textit{left}] \le \text{nums}[\textit{mid}] \text{ and } \textit{target} \in \text{nums}[\,\textit{left} .. \textit{right}\,], \text{ then } \bigl(\text{its index lies in } [\,\textit{left},\ \textit{mid}\,) \iff \text{nums}[\textit{left}] \le \textit{target} < \text{nums}[\textit{mid}]\bigr) $$

```text
if nums[left] <= nums[mid]                  (the left half is sorted)
   and target is present in nums[left .. right], then
       target lies in nums[left .. mid - 1]  <=>  nums[left] <= target < nums[mid]
```

Both hypotheses are load-bearing. Without presence, the right-hand side can be satisfied by a value that is absent from the array: in `[1, 3, 5]` with `left = 0` and `mid = 2`, the comparison `1 <= 2 < 5` passes, yet `2` occurs nowhere in `nums[0 .. 1]`. Without sortedness the failure runs the other way, since the endpoints no longer bound the half: in `[4, 5, 1, 2, 3]` with `left = 0`, `mid = 2` and `right = 4`, the target `5` does sit in `nums[0 .. 1]`, yet `4 <= 5 < 1` is false. Two facts license the equivalence once both hold. The loop invariant carried over from plain binary search guarantees that a target present in `nums` is present in the current window, and the values are distinct, so a target inside the sorted half's value range cannot also lie in the other half (every element of the unsorted half is either above `nums[mid]` or below `nums[left]`).

Each iteration discards a half only after proving the target cannot be in it: by exact bounds when that half is sorted, and by elimination otherwise. Both directions do work. The forward direction discards the sorted half when the comparison fails, and the reverse direction, the one needing presence, discards the other half when it holds. The loop invariant is preserved unchanged, so the \(O(\log n)\) bound carries over.

The non-strict `<=` in the sortedness test matters at `left == mid`, which happens whenever the window narrows to one or two elements. Using `<` there would misclassify a single-element half as unsorted and send the search down the wrong branch.

#### Walkthrough

Let us run the single-pass search on Example 1: `nums = [4,5,6,7,0,1,2]`, `target = 0`. Each probe computes `mid`, checks for a direct hit, identifies the sorted half with `nums[left] <= nums[mid]`, and tests `target` against that half's endpoint bounds:

```text
left=0  right=6  mid=3   nums[mid]=7 != 0
                         nums[left]=4 <= 7: left half [0..3] sorted
                         4 <= 0 < 7 false: not in the sorted half, left = 4
left=4  right=6  mid=5   nums[mid]=1 != 0
                         nums[left]=0 <= 1: left half [4..5] sorted
                         0 <= 0 < 1 true: in the sorted half, right = 4
left=4  right=4  mid=4   nums[mid]=0 == target, return 4
```

The first probe lands in the left run `[4,5,6,7]`; the bound test proves `0` cannot be there, so the whole run is discarded in one step. The second probe's window `[0,1,2]` no longer contains the pivot, so the search behaves exactly like plain binary search from there. The direct hit at `mid = 4` returns `4`, matching the expected Output of `4`.

#### Solution

The code is the probe loop from the walkthrough: hit check, sorted-half test, then the two-sided bound comparison.

```python
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                return mid

            if nums[left] <= nums[mid]:  # left half is sorted
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:  # right half is sorted
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

Each iteration eliminates half of the remaining window, giving a single logarithmic pass.

##### Space Complexity: `O(1)`

Only the two pointers and a midpoint are stored.

#### Key Insights

- In a rotated sorted array, at least one half around `mid` is always sorted, which is what lets a single binary search proceed without first locating the pivot.
- Using exact, inclusive-or-exclusive bounds (`nums[left] <= target < nums[mid]` and `nums[mid] < target <= nums[right]`) is what prevents both infinite loops and skipped answers.
- Computing `mid = left + (right - left) // 2` avoids potential integer overflow in languages with fixed-width integers.

## Comparison of Solutions

### Time Complexity

- **Linear Scan**: `O(n)` - examines every element in the worst case.
- **Find Pivot then Binary Search**: `O(log n)` - two or three binary searches of the same order.
- **Modified Binary Search**: `O(log n)` - a single binary-search pass.

### Space Complexity

- **Linear Scan**: `O(1)` - a single loop variable.
- **Find Pivot then Binary Search**: `O(1)` - constant pointer state.
- **Modified Binary Search**: `O(1)` - constant pointer state.

### Trade-offs

- **Linear Scan** is trivially correct and needs no corner-case reasoning, but it fails the required `O(log n)` bound and is unacceptable on large inputs.
- **Find Pivot then Binary Search** keeps each phase a standard binary search, so it is easy to derive and debug and the pivot-finding helper is reusable, at the cost of a worse constant factor from making two passes.
- **Modified Binary Search** completes in one pass for the best constant factor, but its branching is denser and the boundary conditions are easier to get wrong.

### When to Use Each

- **Linear Scan**: Only as a correctness oracle, for tiny inputs, or when the array is known to be unsorted.
- **Find Pivot then Binary Search**: When clarity and maintainability are prioritized, or when teaching the decomposition (Recommended for first attempts).
- **Modified Binary Search**: When the single-pass optimum is required and the denser logic is acceptable.

### Optimization Notes

- The **Modified Binary Search** is the optimal choice when performance matters: it handles rotation within one binary-search pass, eliminating the second traversal of the two-phase approach while preserving `O(log n)` time and `O(1)` space.
- Implementation detail: at each step decide which half is sorted by comparing `nums[left]` to `nums[mid]`, then test whether the target falls inside that sorted range to choose which half to discard, because at least one half is always sorted.
- Interview strategy: present **Linear Scan** to confirm the contract, then derive **Find Pivot then Binary Search** for clarity, and finish with **Modified Binary Search** as the optimization.
- Common pitfall: all binary-search variants must handle non-rotated and single-element arrays, and the boundary comparisons must use the correct inclusive or exclusive bounds to avoid infinite loops or missed targets.
