# [Find Minimum In Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)

**Medium** | **25 minutes** | **Array, Binary Search**

**Pattern:** [Binary Search](../patterns/binary_search/intuition.md)

**Algorithm:** [Binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm)

**Practice:** [`practice/find_minimum_in_rotated_sorted_array/solution.py`](../../practice/find_minimum_in_rotated_sorted_array/solution.py)

You are given an array of length `n` which was originally sorted in ascending order. It has now been **rotated** between `1` and `n` times. For example, the array `nums = [1,2,3,4,5,6]` might become:

* `[3,4,5,6,1,2]` if it was rotated `4` times.
* `[1,2,3,4,5,6]` if it was rotated `6` times.

Notice that rotating the array `4` times moves the last four elements of the array to the beginning. Rotating the array `6` times produces the original array.

Assuming all elements in the rotated sorted array `nums` are **unique**, return the minimum element of this array.

A solution that runs in `O(n)` time is trivial, can you write an algorithm that runs in `O(log n) time`?

## Examples

### Example 1

**Input:** `nums = [3,4,5,6,1,2]`

**Output:** `1`

### Example 2

**Input:** `nums = [4,5,0,1,2,3]`

**Output:** `0`

### Example 3

**Input:** `nums = [4,5,6,7]`

**Output:** `4`

## Constraints

- `1 <= nums.length <= 1000`
- `-1000 <= nums[i] <= 1000`

## Deriving the Solution

A rotated sorted array is two ascending runs glued together, every value in the first run greater than every value in the second, and the minimum is the first value of the second run. The rotation point (where the runs meet) is therefore the answer's location, and each solution below hunts for it; they differ in how many values they must examine to find the seam.

1. **Start literal.** Scan every element, keeping the smallest seen. `O(n)`,
   which ignores that the array is nearly sorted: see [Linear Scan](#linear-scan).
2. **Spot the order.** The runs are individually sorted, so a comparison
   against a run boundary can discard half the array at once: the question
   becomes "is `mid` left or right of the seam?".
3. **Answer it with the right sentinel.** `nums[mid] > nums[right]` means `mid`
   sits in the first run (the seam is strictly to its right); otherwise `mid`
   is in the second run, whose first element, the minimum, is at `mid` or left
   of it. The comparison never needs a boundary special case, and the closed
   interval converges onto the seam in `O(log n)`: see
   [Binary Search on Right Slope](#binary-search-on-right-slope).

## Solutions

### Linear Scan

#### Derivation

The most direct reading walks the array once, tracking the smallest value seen. The rotation is irrelevant to this approach; it works on any array:

1. Initialize `smallest = nums[0]`.
2. For each value, replace `smallest` whenever a smaller one appears.
3. Return `smallest`.

#### Walkthrough

Trace the scan on Example 1: `nums = [3,4,5,6,1,2]`:

```text
start    smallest = 3
value 4  4 < 3? no    smallest = 3
value 5  5 < 3? no    smallest = 3
value 6  6 < 3? no    smallest = 3
value 1  1 < 3? yes   smallest = 1
value 2  2 < 1? no    smallest = 1
```

The minimum `1` arrives mid-array and the scan keeps it through the end, matching the expected Output for Example 1.

#### Solution

The code is the running minimum from the walkthrough. Python's built-in `min(nums)` computes the same thing in one call; the explicit loop shows the work that call performs.

```python
from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        smallest = nums[0]
        for value in nums:
            if value < smallest:
                smallest = value
        return smallest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every element is examined once.

##### Space Complexity: `O(1)`

One accumulator variable.

#### Key Insights

- Correct on any array, rotated or not; the price is never using order.
- For the constraint `n <= 1000` it is fast enough in practice, but the problem
  explicitly asks for `O(log n)` and interviewers expect the binary search.
- The follow-up question ("can you beat `O(n)`?") is the real problem.

### Binary Search on Right Slope

#### Derivation

The scan ignores the defining property: except at one seam, a value's right neighbor is larger. Binary search can find that seam if each probe can tell which side of it `mid` falls on. Compare `nums[mid]` with the right sentinel `nums[right]`:

- `nums[mid] > nums[right]`: the descending drop lies strictly after `mid`
  (an ascending run cannot contain a larger-then-smaller pair), so the minimum
  is in `(mid, right]`: `left = mid + 1`.
- `nums[mid] < nums[right]`: the segment `mid..right` is ascending throughout,
  so its first element, `nums[mid]`, is the smallest of that segment. The
  overall minimum is either that or something left of `mid`:
  `right = mid` (keeping `mid`, since it might be the answer).

Why the right sentinel and not the left? Comparing against `nums[left]` cannot distinguish "mid is in the second run" from "the whole window is one sorted run", and the distinction needs a boundary special case that the right comparison gets for free. The loop keeps a closed interval `[left, right]` known to contain the minimum and halves it until `left == right`:

1. Set `left = 0`, `right = len(nums) - 1`.
2. While `left < right`, probe `mid = (left + right) // 2`.
3. Apply the two-way rule above.
4. Return `nums[left]`.

#### Walkthrough

Trace the search on Example 1: `nums = [3,4,5,6,1,2]`:

```text
left=0 right=5  mid=2  nums[2]=5 > nums[5]=2  seam right of mid  -> left=3
left=3 right=5  mid=4  nums[4]=1 < nums[5]=2  ascending segment  -> right=4
left=3 right=4  mid=3  nums[3]=6 > nums[4]=1  seam right of mid  -> left=4
left=4 right=4  loop ends -> return nums[4] = 1
```

Every probe sent the interval toward the seam: the first probe saw `5 > 2` (a first-run value against a second-run value), the second locked onto the ascending segment containing the minimum, the third pinned `left` onto it. The result `1` matches the expected Output for Example 1.

Run the same trace on Example 3, an array never rotated past its start: `nums = [4,5,6,7]`:

```text
left=0 right=3  mid=1  nums[1]=5 < nums[3]=7  ascending  -> right=1
left=0 right=1  mid=0  nums[0]=4 < nums[1]=5  ascending  -> right=0
left=0 right=0  loop ends -> return nums[0] = 4
```

With no seam inside the window, every probe declares the segment ascending and slides `right` leftward, never skipping past the true minimum at `nums[0]`. The result `4` matches the expected Output for Example 3, and the case shows why `right = mid` (not `mid - 1`) is load-bearing: discarding `mid` there would throw the minimum away.

#### Solution

The code is the walkthrough's closed-interval loop with the right-sentinel rule.

```python
from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[right]:
                # The drop is strictly after mid: discard mid and left of it
                left = mid + 1
            else:
                # mid..right ascends: the minimum is at mid or left of it
                right = mid
        return nums[left]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

The interval halves on every probe; a size-`n` window survives `ceil(log2 n)` iterations at most.

##### Space Complexity: `O(1)`

Only the two boundary indices are stored.

#### Key Insights

- The right sentinel sorts every probe into its run in one comparison, no
  pre-checks, no boundary special case.
- `right = mid` (never `mid - 1`) is what makes the un-rotated case safe: the
  minimum can be the probe itself.
- `left < right` pairs with the closed-interval updates so the loop ends with
  `left == right` on the minimum; writing `while left <= right` with these
  updates would loop forever.
- The same skeleton solves finding the rotation count (`left - 0` after a small
  tweak) and the rotated binary search for a target.

## Comparison of Solutions

### Time Complexity

- **Linear Scan**: `O(n)` - touches every element.
- **Binary Search on Right Slope**: `O(log n)` - halves the interval per probe.

### Space Complexity

- **Linear Scan**: `O(1)` - one accumulator.
- **Binary Search on Right Slope**: `O(1)` - two boundary indices.

### Trade-offs

- The scan is universal (works on unsorted input) but discards the structure
  the problem provides.
- The binary search needs uniqueness of the seam: with duplicates, the
  `nums[mid] == nums[right]` case can neither confirm nor discard a side and
  the `O(log n)` guarantee degrades to `O(n)` (as in LeetCode's Find Minimum in
  Rotated Sorted Array II).
- Both use constant space; the binary search's extra cost is reasoning, not
  memory.

### When to Use Each

- **Linear Scan**: A one-line `min(nums)` suffices when the constraint size is
  trivial and no logarithmic requirement exists.
- **Binary Search on Right Slope**: The expected answer and required whenever the
  problem (as here) states the `O(log n)` follow-up (recommended here).

### Optimization Notes

- `mid = (left + right) // 2` rounds down, which keeps the probe strictly left
  of `right` when the window has two elements; that rounding is what makes the
  `right = mid` update terminate.
- Overflow-safe midpoints (`left + (right - left) // 2`) are unnecessary in
  Python but are the portable spelling for C++/Java ports.
- The uniqueness assumption is what makes `nums[mid] != nums[right]` always
  true inside the loop; variants with duplicates must add an explicit
  equality branch that shrinks the window by one.
