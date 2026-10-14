# [Search in a Rotated Sorted Array](https://www.fastprep.io/problems/amazon-search-rotated-sorted-array)

**Medium** | **NN minutes** | **Array, Binary Search**

Given an integer array nums that was sorted in strictly increasing order and then rotated at an unknown pivot, and an integer target, return the index of target.

Return -1 when target does not appear in nums.

All values in nums are distinct. Your solution must run in O(log n) time.

## Examples

### Example 1

**Input:** `nums = [4,5,6,7,0,1,2]`, `target = 0`

**Output:** `4`

**Explanation:** The target 0 appears at index 4.

### Example 2

**Input:** `nums = [4,5,6,7,0,1,2]`, `target = 3`

**Output:** `-1`

**Explanation:** The target 3 is absent, so the result is -1.

### Example 3

**Input:** `nums = [1]`, `target = 0`

**Output:** `-1`

**Explanation:** The only array value is 1, so 0 is absent.

## Constraints

- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- `nums contains distinct values.`
- `nums was sorted in strictly increasing order and rotated at an unknown pivot.`
- `-10^9 <= target <= 10^9`

## Solutions

### Linear Scan

#### Derivation

The most direct reading of the problem ignores the rotated structure entirely and [walks the array](https://en.wikipedia.org/wiki/Linear_search) comparing each element to `target`:

1. Iterate over the array in index order.
2. Return the index as soon as an element equals `target`.
3. Return `-1` if the loop finishes without a match.

This is always correct and needs no reasoning about rotation, but it examines up to every element, so it costs `O(n)`. The problem explicitly demands `O(log n)`, so this baseline serves as a correctness reference for the logarithmic solutions below rather than an acceptable submission.

#### Walkthrough

Let us scan Example 1 by hand: `nums = [4,5,6,7,0,1,2]`, `target = 0`. The loop compares each element in index order and stops at the first match:

```text
index 0   value 4   4 != 0, continue
index 1   value 5   5 != 0, continue
index 2   value 6   6 != 0, continue
index 3   value 7   7 != 0, continue
index 4   value 0   0 == 0, return 4
```

The scan walks straight past the rotation point without noticing it and returns `4`, the expected Output. Example 2, `target = 3`, runs off the end of the same array without a match and returns `-1`.

#### Solution

The code is the scan from the walkthrough: one comparison per element until the first match.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int], target: int) -> int:
        for position, value in enumerate(nums):
            if value == target:
                return position
        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every element may be examined once in the worst case, when `target` sits at the end or is absent.

##### Space Complexity: `O(1)`

Only the loop position and the current value are held.

#### Key Insights

- Correct on any array, rotated or not, which makes it the oracle for testing the binary-search variants.
- It fails the stated `O(log n)` requirement, so its role on the page is calibration: the logarithmic solutions must reproduce exactly these answers while touching `O(log n)` elements.
- The distinct-values guarantee of this problem is never used here, a first hint that the structure the constraint creates is what the faster solutions exploit.

### Find Pivot then Binary Search

#### Derivation

The Linear Scan discards the one guarantee the input offers: apart from a single descending step at the rotation point, the array is sorted. If that step's position were known, the problem would collapse into ordinary [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) over two sorted runs. So ask: can the pivot be located in `O(log n)` on its own? It can, because the pivot is the index of the minimum, and comparing `nums[mid]` against `nums[right]` always reveals which side of `mid` the minimum lies on: a midpoint larger than the right endpoint sits in the left run, before the step, so the minimum is strictly right of it; otherwise the minimum is at `mid` or left of it. That decomposes the problem into two independent phases, each a standard binary search:

1. If `nums[left] <= nums[right]`, the array is not rotated (the pivot is
   index `0`). Otherwise binary search for the minimum: move `left = mid + 1`
   when `nums[mid] > nums[right]`, and set `right = mid` otherwise; the loop
   ends with `left == right` on the pivot.
2. The pivot splits the array into the sorted runs `nums[0 .. pivot - 1]` and
   `nums[pivot .. len(nums) - 1]`. Run a standard binary search over the first
   run and, when it misses, over the second.

Each phase reuses textbook logic with no rotation handling, which is the approach's main virtue: every line is individually familiar.

#### Walkthrough

Let us trace both phases on Example 1: `nums = [4,5,6,7,0,1,2]`, `target = 0`. The values by index are `0:4 1:5 2:6 3:7 4:0 5:1 6:2`.

**Phase 1, find the pivot.** The pre-check `nums[0] = 4 <= nums[6] = 2` is false, so the array is rotated and the minimum search starts. Each step compares `nums[mid]` against `nums[right]`:

| Step | `left` | `right` | `mid` | `nums[mid]` | `nums[right]` | Decision |
|------|--------|---------|-------|-------------|---------------|----------|
| 1 | `0` | `6` | `3` | `7` | `2` | `7 > 2`: minimum is right of `mid`, `left = 4` |
| 2 | `4` | `6` | `5` | `1` | `2` | `1 <= 2`: minimum at `mid` or left, `right = 5` |
| 3 | `4` | `5` | `4` | `0` | `1` | `0 <= 1`: minimum at `mid` or left, `right = 4` |

The window has narrowed to `left == right == 4`, and `nums[4] = 0` is indeed the minimum: `pivot = 4`.

**Phase 2, search the two sorted runs.** The runs are `nums[0 .. 3] = [4,5,6,7]` and `nums[4 .. 6] = [0,1,2]`. The first run's search, `binary_search(0, 3)`:

| Step | `start` | `end` | `mid` | `nums[mid]` | Decision |
|------|---------|-------|-------|-------------|----------|
| 1 | `0` | `3` | `1` | `5` | `5 > 0`: `end = 0` |
| 2 | `0` | `0` | `0` | `4` | `4 > 0`: `end = -1` |

The window empties, so the first run returns `-1`. The second run's search, `binary_search(4, 6)`:

| Step | `start` | `end` | `mid` | `nums[mid]` | Decision |
|------|---------|-------|-------|-------------|----------|
| 1 | `4` | `6` | `5` | `1` | `1 > 0`: `end = 4` |
| 2 | `4` | `4` | `4` | `0` | `0 == 0`: return `4` |

The search returns `4`, matching the expected Output.

#### Solution

The code is the two phases from the walkthrough as helper closures: `find_pivot` first, then `binary_search` over each sorted run in turn.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int], target: int) -> int:
        def find_pivot() -> int:
            left, right = 0, len(nums) - 1
            if nums[left] <= nums[right]:
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
                if nums[mid] < target:
                    start = mid + 1
                else:
                    end = mid - 1
            return -1

        pivot = find_pivot()
        if pivot > 0:
            first_run = binary_search(0, pivot - 1)
            if first_run != -1:
                return first_run
        return binary_search(pivot, len(nums) - 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

Finding the pivot is one binary search and the lookup at most two more, each halving the window, so the total remains logarithmic.

##### Space Complexity: `O(1)`

The two closures keep only pointer variables and allocate no data structures.

#### Key Insights

- A rotated ascending array of distinct values has exactly one descending step, and the index below to the step's left boundary is the unique minimum; finding it reduces rotation to a plain split point.
- Comparing `nums[mid]` against `nums[right]`, not `nums[left]`, is what makes the pivot search decisive: `nums[mid] > nums[left]` holds on both sides of the pivot, but `nums[mid] > nums[right]` only before it.
- Separating the phases keeps every line textbook, trading a constant-factor overhead (up to three logarithmic passes) for conceptual clarity.

### Modified Binary Search

#### Derivation

The two-phase approach spends an entire binary search locating the pivot before `target` is consulted, and may run two more searches afterwards. Ask whether the pivot needs to be found at all. The sharper observation: at any probe, at least one of the halves around `mid` is fully sorted, because the single descending step can lie in at most one half. A sorted half is exactly bounded by its endpoints, so a two-sided comparison of `target` against those endpoints decides, with certainty, whether `target` could live in that half; whichever way the comparison falls, half the window is discarded. The rotation is thereby handled inside one search, with no pivot pass:

1. Keep an inclusive window `left .. right`. Compute `mid` and return `mid`
   immediately when `nums[mid] == target`.
2. When `nums[left] <= nums[mid]`, the left half is sorted: if
   `nums[left] <= target < nums[mid]`, `target` can only be there, so set
   `right = mid - 1`; otherwise discard that half with `left = mid + 1`.
3. Otherwise the right half is sorted: if `nums[mid] < target <= nums[right]`,
   search right with `left = mid + 1`; otherwise `right = mid - 1`.
4. Return `-1` when the window empties.

#### Invariant

A rotation by \(r\) of a sorted array of distinct values means:

$$ \text{nums}[i] = \text{sorted}\bigl[(i + r) \bmod n\bigr] $$

```text
nums[i] = sorted[(i + r) mod n]   for 0 <= i < n
          where r is the rotation amount and n = len(nums)
```

so the array is two ascending runs laid end to end, with one descending step at the pivot. Any split point `mid` leaves the step in at most one half, which yields the property the search rests on:

$$ \text{at least one of } [\textit{left},\ \textit{mid}] \text{ and } [\textit{mid},\ \textit{right}] \text{ is fully sorted} $$

```text
at least one of nums[left .. mid] and nums[mid .. right] is fully sorted
```

The test `nums[left] <= nums[mid]` identifies which half is sorted: it holds exactly when the left half contains no step, and a step-free ascending run is bounded by its endpoints. Under that bound, membership of the half reduces to one comparison chain:

$$ \text{target} \in \text{nums}[\,\textit{left} .. \textit{mid} - 1\,] \iff \text{nums}[\textit{left}] \le \textit{target} < \text{nums}[\textit{mid}] $$

```text
target lies in nums[left .. mid - 1]  <=>  nums[left] <= target < nums[mid]
```

Both directions of the loop's branching are licensed by the surrounding invariant. The forward direction discards the sorted half when the comparison fails: an ascending run cannot hold a value outside its own endpoint bounds. The reverse direction discards the unsorted half when the comparison holds: the window invariant (a `target` present in `nums` stays present in the current window) guarantees `target` is somewhere in the window, the sorted half cannot hold it when the comparison passes only against that half's range, and distinctness means it cannot hide in the unsorted half either, since every element there is either above `nums[mid]` or below `nums[left]` (the run before the step is entirely above the run after it). Each branch therefore discards half the window without ever discarding a window that could contain `target`, which preserves both the invariant and the `O(log n)` bound.

The non-strict `<=` in the sortedness test matters when `left == mid`, which happens whenever the window narrows to one or two elements: using `<` there would misclassify a single-element half as unsorted and send the search down the wrong branch.

#### Walkthrough

Let us run the single-pass search on Example 1: `nums = [4,5,6,7,0,1,2]`, `target = 0`. Each probe computes `mid`, checks for a direct hit, identifies the sorted half, and tests `target` against that half's endpoint bounds:

```text
left=0  right=6  mid=3   nums[mid]=7 != 0
                         nums[left]=4 <= 7: left half [0..3] sorted
                         4 <= 0 < 7 false: 0 not in the sorted half, left = 4
left=4  right=6  mid=5   nums[mid]=1 != 0
                         nums[left]=0 <= 1: left half [4..5] sorted
                         0 <= 0 < 1 true:   0 must be in the sorted half, right = 4
left=4  right=4  mid=4   nums[mid]=0 == target, return 4
```

The first probe lands in the left run `[4,5,6,7]`; the bound test proves `0` cannot live there, so the whole run is discarded in one step, the same work the pivot-finding pass did, now folded into a single comparison. The window `[0,1,2]` no longer contains the step, so the search proceeds as plain binary search. The direct hit at `mid = 4` returns `4`, matching the expected Output.

For the miss path, Example 2 with `target = 3` on the same array:

```text
left=0  right=6  mid=3   nums[mid]=7 != 3
                         left half sorted; 4 <= 3 < 7 false, left = 4
left=4  right=6  mid=5   nums[mid]=1 != 3
                         left half sorted; 0 <= 3 < 1 false, left = 6
left=6  right=6  mid=6   nums[mid]=2 != 3
                         left half (single element) sorted; 2 <= 3 < 2 false, left = 7
left > right: window empty, return -1
```

Every probe survives the bounds check before discarding, and the window empties without ever discarding a half that could contain `3`. The function returns `-1`, matching the expected Output.

#### Solution

The code is the probe loop from the walkthrough: hit check, sorted-half test, then the two-sided bound comparison.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                return mid

            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

Each iteration discards half of the current window, giving a single logarithmic pass with no separate pivot search.

##### Space Complexity: `O(1)`

Only the two window pointers and the midpoint are stored.

#### Key Insights

- At least one half around `mid` is always sorted, and a sorted half can be rejected with a single two-sided comparison against its exact endpoints; that is the entire mechanism.
- Both bound tests are half-open by design (`<= target <` and `< target <=`): each excludes `nums[mid]`, which the hit check already settled, and each side's exact endpoints are what make the discard safe rather than heuristic.
- The non-strict `nums[left] <= nums[mid]` sortedness test carries the small-window cases (`left == mid`), where a strict comparison would misroute the search.
- Computing `mid = left + (right - left) // 2` avoids integer overflow in fixed-width languages; Python does not overflow, but the habit transfers.

## Comparison of Solutions

### Time Complexity

- **Linear Scan**: `O(n)` - every element may be examined once.
- **Find Pivot then Binary Search**: `O(log n)` - up to three binary searches, each logarithmic.
- **Modified Binary Search**: `O(log n)` - one binary-search pass.

### Space Complexity

- **Linear Scan**: `O(1)` - a loop position and the current value.
- **Find Pivot then Binary Search**: `O(1)` - pointer state only.
- **Modified Binary Search**: `O(1)` - two window pointers and a midpoint.

### Trade-offs

- **Linear Scan** is trivially correct with zero corner-case reasoning, but it fails the stated `O(log n)` requirement outright.
- **Find Pivot then Binary Search** keeps every phase textbook and the pivot helper reusable (the same minimum search powers related rotated-array problems), at the cost of up to three passes and a rotation pre-check.
- **Modified Binary Search** finishes in one pass with the best constant factor, but its branching packs both sortedness detection and range testing into a few dense comparisons that are easy to get subtly wrong.

### When to Use Each

- **Linear Scan**: only as a correctness oracle for testing, or on inputs far too small for the logarithmic bound to matter.
- **Find Pivot then Binary Search**: when clarity beats constant factors, when the pivot is itself needed downstream, or when composing from known-correct pieces under time pressure.
- **Modified Binary Search**: the interview target when the `O(log n)` requirement is stated, as here; one pass, no auxiliary structures.

### Optimization Notes

- The **Modified Binary Search** is the optimal choice: it absorbs pivot handling into the main loop, removing the separate pass while keeping time and space at their bounds.
- Every binary-search variant must survive the degenerate inputs the constraints allow: a single element, an unrotated (already sorted) array, and a target absent from the array.
- The most common defect in this family is a strict sortedness test (`nums[left] < nums[mid]`), which misclassifies one- and two-element windows and can loop forever; the non-strict comparison is not a style choice.
- The pivot-finding search from the two-phase approach is independently reusable for the rotated-minimum problem family, which is a reason to know it even though this problem does not require it.
