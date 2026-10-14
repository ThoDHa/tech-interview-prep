# [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/)

**Hard** | **40 minutes** | **Array, Binary Search, Divide and Conquer**

**Pattern:** [Binary Search](../patterns/binary_search/intuition.md)

**Algorithm:** [Binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) · [Divide-and-conquer algorithm](https://en.wikipedia.org/wiki/Divide-and-conquer_algorithm) · [Heap (data structure)](https://en.wikipedia.org/wiki/Heap_(data_structure))

**Practice:** [`practice/median_of_two_sorted_arrays/solution.py`](../../practice/median_of_two_sorted_arrays/solution.py)

You are given two integer arrays `nums1` and `nums2` of size `m` and `n` respectively, where each is sorted in ascending order. Return the [median](https://en.wikipedia.org/wiki/Median) value among all elements of the two arrays.

Your solution should run in $O(log (m+n))$ time.

## Examples

### Example 1

**Input:** `nums1 = [1,2], nums2 = [3]`

**Output:** `2.0`

**Explanation:** Among `[1, 2, 3]` the median is `2`.

### Example 2

**Input:** `nums1 = [1,3], nums2 = [2,4]`

**Output:** `2.5`

**Explanation:** Among `[1, 2, 3, 4]` the median is `(2 + 3) / 2 = 2.5`.

## Constraints

- `nums1.length == m`
- `nums2.length == n`
- `0 <= m <= 1000`
- `0 <= n <= 1000`
- `1 <= m + n <= 2000`
- `-10^6 <= nums1[i], nums2[i] <= 10^6`

## Deriving the Solution

The median is the value splitting the combined multiset in half: position `(m + n) / 2` in the merged order (adjusted for even totals). Merging to find it is easy; the challenge is finding it without merging, in logarithmic time. The key reformulation: the median is fully determined by a **cut** through the two arrays, a choice of how many elements each array contributes to the left half. Every solution below decides that cut; they differ in how they search for the correct one.

1. **Start literal.** Merge the arrays and read the middle. `O(m + n)`, which
   is correct and simple but ignores that both inputs are already sorted: see
   [Merge and Select](#merge-and-select).
2. **Search the cut, not the value.** A valid cut with `i` elements from `nums1`
   and `j` from `nums2` is exactly one where every left-side element is `<=`
   every right-side element. Because both arrays are sorted, that test touches
   only the four boundary values around the cut, and binary search on the
   smaller array finds the cut in `O(log(min(m, n)))`: see
   [Partition Binary Search](#partition-binary-search).
3. **Squeeze the constants.** Heap-based approaches reach `O(k log k)` for the
   first `k = (m + n) / 2` elements; they generalize to streaming medians but
   do not beat the partition search here: see
   [Two-Heaps Selection](#two-heaps-selection).

## Solutions

### Merge and Select

#### Derivation

The most direct reading merges the two sorted arrays with the standard two-pointer merge, stopping as soon as the median positions are reachable:

1. Walk both arrays with pointers, always advancing the smaller head.
2. Stop when `k = (m + n) // 2 + 1` values have been consumed.
3. For an odd total, the median is the `k`-th consumed value; for an even
   total, it is the mean of the `(k-1)`-th and `k`-th.

Merging only `k` values (rather than all of them) keeps the constant half the size, though the asymptotics are unchanged.

#### Walkthrough

Trace the partial merge on Example 2: `nums1 = [1,3]`, `nums2 = [2,4]`, total `4`, so `k = 4 // 2 + 1 = 3`:

```text
i=0 j=0   heads 1, 2   take 1   consumed [1]
i=1 j=0   heads 3, 2   take 2   consumed [1, 2]
i=1 j=1   heads 3, 4   take 3   consumed [1, 2, 3]
```

Three values consumed: the median for an even total is the mean of the last two, `(2 + 3) / 2 = 2.5`, matching the expected Output for Example 2.

#### Solution

The code is the partial merge with a running pair of the last two consumed values.

```python
from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        total = len(nums1) + len(nums2)
        k = total // 2 + 1
        previous = current = 0
        i = j = 0
        for _ in range(k):
            previous = current
            if i < len(nums1) and (j >= len(nums2) or nums1[i] <= nums2[j]):
                current = nums1[i]
                i += 1
            else:
                current = nums2[j]
                j += 1
        if total % 2 == 1:
            return float(current)
        return (previous + current) / 2
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m + n)`

The merge consumes up to `(m + n) / 2 + 1` values, a linear count.

##### Space Complexity: `O(1)`

Only the two pointers and the running pair of consumed values.

#### Key Insights

- Partial merging beats full merging by a constant but cannot beat the linear
  bound; the sortedness of the inputs is left mostly unused.
- The two-value rolling pair avoids storing the consumed prefix.
- This is the correct baseline: every faster version must produce identical
  answers on it.

### Two-Heaps Selection

#### Derivation

A heap mediates between "unsorted, need order statistics" and "sorted, need one value". Maintaining a max-heap of the smaller half and a min-heap of the larger half of everything consumed so far makes the median readable from the heap roots at any moment. Streaming every element of both arrays through the two-heap insertion discipline yields the median once all have arrived:

1. Push each arriving `value` into `smaller` (the max-heap, stored negated).
2. Move `smaller`'s maximum into `larger` (the min-heap): the max of the small
   half belongs in the large half if the order invariant was violated.
3. If `larger` now outgrows `smaller`, move its minimum back: the small half
   always holds the ceiling half of the elements.
4. After all elements: an odd total reads `smaller`'s root; an even total reads
   the mean of both roots.

#### Walkthrough

Trace the heap build on Example 1: `nums1 = [1,2]`, `nums2 = [3]`, total `3` (odd). Each row shows the element arriving, the two-heap discipline applied, and the balanced state, with `smaller` drawn as the max-heap it represents:

```text
push 1   smaller [1]    larger []     move max 1 -> larger; larger outgrows,
                                      move 1 back
         smaller [1]    larger []
push 2   smaller [2, 1] larger []     move max 2 -> larger
         smaller [1]    larger [2]
push 3   smaller [3, 1] larger [2]    move max 3 -> larger; larger outgrows,
                                      move 2 back
         smaller [2, 1] larger [3]
```

Every element lands in `smaller` first, so the order check (step 2) never misses a violation. The final state has `smaller` holding `{2, 1}` and `larger` holding `{3}`: the halves split `{1, 2, 3}` correctly at `2`. The total is odd, so the median is `smaller`'s root, `2`. As a float that is `2.0`, matching the expected Output for Example 1.

#### Solution

The code is the fill loop with the two-heap discipline from the walkthrough.

```python
import heapq
from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        smaller, larger = [], []
        for value in nums1 + nums2:
            heapq.heappush(smaller, -value)
            # The max of the small half belongs in the large half
            heapq.heappush(larger, -heapq.heappop(smaller))
            # The large half never outgrows the small half
            if len(larger) > len(smaller):
                heapq.heappush(smaller, -heapq.heappop(larger))
        if (len(nums1) + len(nums2)) % 2 == 1:
            return float(-smaller[0])
        return (larger[0] - smaller[0]) / 2
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((m + n) log(m + n))`

Every element is pushed once, and each push or pop costs logarithmic time in the combined size.

##### Space Complexity: `O(m + n)`

Both heaps together hold every element.

#### Key Insights

- The two-heap invariant (halves differ by at most one, every `smaller` value
  `<=` every `larger` value) is the same median machinery that powers Find
  Median from Data Stream.
- It makes no use of the inputs being sorted, which is exactly why it cannot
  win here; its home turf is unsorted streams.
- Negated max-heap values are Python's standard `heapq` idiom.

### Partition Binary Search

#### Derivation

The merge scans left halves element by element, but the half's membership can be described without naming its elements: a cut contributing `i` elements of `nums1` and `j` elements of `nums2`, with `i + j = half = (m + n + 1) // 2`, is valid precisely when nothing on the right exceeds anything on the left. Sortedness makes the test local, touching only the four values at the cut's edges, with `±inf` sentinels standing in wherever a side is empty:

- `left1 = nums1[i - 1]` (or `-inf` when `i = 0`) and `right1 = nums1[i]` (or
  `+inf` when `i = m`);
- `left2 = nums2[j - 1]` (or `-inf`) and `right2 = nums2[j]` (or `+inf`).

The cut is valid iff `left1 <= right2` and `left2 <= right1`. Monotonicity of the test in `i` (taking more from `nums1` raises `left1` and lowers `j`, lowering `left2`) is what licenses binary search. Searching over the **shorter** array bounds the search range and keeps `j = half - i` inside `nums2` automatically:

1. Ensure `nums1` is the shorter array, swapping if needed.
2. Binary search `i` in `[0, m]` for a valid cut (`j = half - i`).
3. On validity: odd total reads `max(left1, left2)`; even total reads the mean
   of `max(left1, left2)` and `min(right1, right2)`.
4. If `left1 > right2`, too many came from `nums1`: `right = i - 1`; otherwise
   `left = i + 1`.

#### Walkthrough

Trace the cut search on Example 2: `nums1 = [1,3]`, `nums2 = [2,4]`, `m = n = 2`, `half = (2 + 2 + 1) // 2 = 2`. The lengths are equal, so no swap:

```text
left=0 right=2   i=1, j=1
   left1 = nums1[0] = 1    right1 = nums1[1] = 3
   left2 = nums2[0] = 2    right2 = nums2[1] = 4
   1 <= 4 and 2 <= 3: valid cut
even total: median = (max(1, 2) + min(3, 4)) / 2 = (2 + 3) / 2 = 2.5
```

The cut splits both arrays after their first element: the left half holds `{1, 2}`, the right half `{3, 4}`, and the four boundary values agree on the split. The median `(2 + 3) / 2 = 2.5` matches the expected Output for Example 2, found without merging anything.

Run the single-probe case on Example 1: `nums1 = [1,2]`, `nums2 = [3]`. Now `nums1` is longer, so the swap makes `nums1 = [3]`, `nums2 = [1,2]`, `m = 1`, `n = 2`, `half = (3 + 1) // 2 = 2`:

```text
left=0 right=1   i=0, j=2
   left1 = -inf            right1 = nums1[0] = 3
   left2 = nums2[1] = 2    right2 = +inf
   -inf <= +inf and 2 <= 3: valid cut
odd total: median = max(-inf, 2) = 2 -> 2.0
```

The first probe already lands on the valid cut, with the `i = 0` sentinel letting `nums1` contribute nothing. The median `2.0` matches the expected Output for Example 1.

#### Solution

The code is the walkthrough's cut search over the shorter array, with the sentinels as `±inf`.

```python
from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        m, n = len(nums1), len(nums2)
        half = (m + n + 1) // 2
        left, right = 0, m
        while left <= right:
            take1 = (left + right) // 2
            take2 = half - take1
            left1 = nums1[take1 - 1] if take1 > 0 else float("-inf")
            right1 = nums1[take1] if take1 < m else float("inf")
            left2 = nums2[take2 - 1] if take2 > 0 else float("-inf")
            right2 = nums2[take2] if take2 < n else float("inf")
            if left1 <= right2 and left2 <= right1:
                if (m + n) % 2 == 1:
                    return float(max(left1, left2))
                return (max(left1, left2) + min(right1, right2)) / 2
            if left1 > right2:
                right = take1 - 1
            else:
                left = take1 + 1
        raise ValueError("unreachable: sorted inputs always admit a valid cut")
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log(min(m, n)))`

The binary search always runs over the shorter array, halving the smaller length; everything inside a probe is constant time.

##### Space Complexity: `O(1)`

Only the boundary indices and the four cut values.

#### Key Insights

- Framing the median as a cut, not a value, converts a selection problem into
  a search problem with a monotone predicate.
- The `±inf` sentinels absorb every edge case: empty arrays, cuts at either end
  of an array, one array fully inside the left half.
- Searching the shorter array is what keeps `take2` in range with no extra
  clamping code.
- This is the follow-up's `O(log(m + n))` answer (log of the smaller length is
  at most log of the total), and it is the standard follow-up to Find Median
  from Data Stream in interview settings.

## Comparison of Solutions

### Time Complexity

- **Merge and Select**: `O(m + n)` - consumes half the merged sequence.
- **Two-Heaps Selection**: `O((m + n) log(m + n))` - a heap push per element.
- **Partition Binary Search**: `O(log(min(m, n)))` - binary search on the cut.

### Space Complexity

- **Merge and Select**: `O(1)` - two pointers and a rolling pair.
- **Two-Heaps Selection**: `O(m + n)` - both heaps hold all elements.
- **Partition Binary Search**: `O(1)` - boundary indices and cut values.

### Trade-offs

- Merge and select is the simplest correct thing and the natural oracle, but it
  abandons the logarithmic requirement entirely.
- The two-heap version pays superlinear time and linear memory for machinery
  this problem does not need; it earns its keep on streams, not on arrays.
- The partition search is the only sublinear option; its cost is the care the
  sentinel bookkeeping demands.

### When to Use Each

- **Merge and Select**: Prototyping and cross-checking the fast version; also
  fine when inputs are small and the logarithmic demand is hypothetical.
- **Two-Heaps Selection**: When the data arrives as a stream, or when the same
  code must serve both this problem and Find Median from Data Stream.
- **Partition Binary Search**: The answer to the problem as stated, including
  its explicit complexity requirement (recommended here).

### Optimization Notes

- Swapping to make `nums1` shorter guarantees `0 <= take2 <= n` for every `i`
  in `[0, m]`, which is what lets the sentinels be the only edge handling.
- `half = (m + n + 1) // 2` rounds up so that odd totals put the median in the
  left half, making the odd case a single `max` read.
- The `float(...)` wrap on the odd case keeps the return type uniform: LeetCode
  expects `2.0`, not `2`, and `2.5` for even totals anyway.
