# [Sort Colors](https://leetcode.com/problems/sort-colors/)

**Medium** | **30 minutes** | **Array, Two Pointers, Sorting**

**Pattern:** [Two Pointers](../patterns/two_pointers/intuition.md)

**Algorithm:** [Dutch national flag problem](https://en.wikipedia.org/wiki/Dutch_national_flag_problem) · [Two-pointer technique](https://usaco.guide/silver/two-pointers)

**Practice:** [`practice/sort_colors/solution.py`](../../practice/sort_colors/solution.py)

Given an array `nums` with `n` objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.

We will use the integers `0`, `1`, and `2` to represent the color red, white, and blue, respectively.

You must solve this problem without using the library's sort function.

## Examples

### Example 1

**Input:** `nums = [2,0,2,1,1,0]`

**Output:** `[0,0,1,1,2,2]`

### Example 2

**Input:** `nums = [2,0,1]`

**Output:** `[0,1,2]`

## Constraints

- `n == nums.length`
- `1 <= n <= 300`
- `nums[i]` is either `0`, `1`, or `2`.

## Follow-up

Could you come up with a one-pass algorithm using only constant extra space?

## Deriving the Solution

The values are already the sort keys: the colors are encoded as `0`, `1`, and `2`, and ascending numeric order is exactly the required red-white-blue order. The problem forbids the library sort, so every solution is a hand-written way of putting three known values in order.

1. **Start literal.** "Sort it yourself" invites writing a general sort by
   hand. Selection sort needs no insight about the values: repeatedly find the minimum of the unsorted tail and swap it forward, at `O(n^2)` comparisons: see [Selection Sort](#selection-sort).
2. **Spot the waste.** Comparing elements is unnecessary when only three
   distinct values exist: the sorted array is fully determined by how many `0`s, `1`s, and `2`s it holds.
3. **Count instead of compare.** Tally the three colors in one pass, then
   overwrite the array with that many `0`s, `1`s, and `2`s in a second pass: `O(n)` time, but two passes: see [Counting Sort](#counting-sort).
4. **Partition in one pass.** The follow-up asks for a single pass. Instead of
   counting first and writing later, classify each element as it is examined, swapping `0`s toward the front and `2`s toward the back while `1`s settle in the middle. Three pointers carve the array into regions and one sweep sorts it: see [Dutch National Flag Algorithm](#dutch-national-flag-algorithm).

## Solutions

### Selection Sort

#### Derivation

The problem forbids the library sort, so the most direct response is to [write a sort by hand](https://en.wikipedia.org/wiki/Sorting_algorithm). [Selection sort](https://en.wikipedia.org/wiki/Selection_sort) is the simplest to derive: it needs no extra structure and no insight about the values, it just repeatedly finds the minimum of the unsorted region and swaps it to the front. With only `0`, `1`, and `2` present this still produces the correct red-white-blue order because ascending numeric order is exactly the required color order.

1. Treat the prefix before index `i` as already sorted.
2. Scan the unsorted tail `i+1 .. n-1` to find `smallest`, the index of the
   smallest value there.
3. Swap that smallest value into position `i`, growing the sorted prefix by
   one.
4. Repeat until the whole array is sorted.

#### Walkthrough

Let us watch Selection Sort run on Example 1: `nums = [2,0,2,1,1,0]`. The outer loop fixes one position `i` at a time. For each `i` it scans the tail `i+1 .. n-1` to find `smallest`, the index of the minimum value there, then swaps `nums[i]` with `nums[smallest]`. Everything before `i` stays sorted.

Each row shows the state after the swap at that `i`:

| `i` | `smallest` (min in tail) | swap | `nums` after swap |
|-----|--------------------------|------|-------------------|
| `0` | `1` (value `0`) | `nums[0] <-> nums[1]` | `[0,2,2,1,1,0]` |
| `1` | `5` (value `0`) | `nums[1] <-> nums[5]` | `[0,0,2,1,1,2]` |
| `2` | `3` (value `1`) | `nums[2] <-> nums[3]` | `[0,0,1,2,1,2]` |
| `3` | `4` (value `1`) | `nums[3] <-> nums[4]` | `[0,0,1,1,2,2]` |
| `4` | `4` (already min) | `nums[4] <-> nums[4]` | `[0,0,1,1,2,2]` |
| `5` | `5` (last element) | `nums[5] <-> nums[5]` | `[0,0,1,1,2,2]` |

At `i=0` the smallest value in the whole array is the `0` at index `1`, so it swaps to the front. At `i=1` the next smallest is the `0` at index `5`. By `i=4` the tail is already in order, so the remaining swaps are no-ops (`smallest == i`). The array is returned in place as `[0,0,1,1,2,2]`, which matches the expected Output.

#### Solution

The code is the walkthrough's outer loop written down: find `smallest` in the tail, swap it to index `i`.

```python
from typing import List


class Solution:
    def sortColors(self, nums: List[int]) -> None:
        n = len(nums)
        for i in range(n):
            # Find the smallest color in the unsorted tail
            smallest = i
            for j in range(i + 1, n):
                if nums[j] < nums[smallest]:
                    smallest = j
            # Swap it into place at the sorted boundary
            nums[i], nums[smallest] = nums[smallest], nums[i]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

For each of the `n` positions the inner loop scans the remaining tail, giving the quadratic `n + (n-1) + ... + 1` comparisons of any selection sort.

##### Space Complexity: `O(1)`

Sorting happens in place with only a few index variables; no auxiliary array is allocated.

#### Key Insights

- Self-derivable baseline: it solves the problem by literally sorting by hand, using no property of the three-color constraint.
- The ascending integer encoding (`0`, `1`, `2`) means a plain numeric sort already yields the red-white-blue order.
- It is correct but wasteful: it re-scans the tail for every position and ignores that only three distinct values exist.

### Counting Sort

#### Derivation

Selection Sort ignores the one special property this input has: only three distinct values exist. Comparing elements is wasted work when the sorted result is fully determined by how many of each color the array holds, so [count the occurrences of each color](https://en.wikipedia.org/wiki/Counting_sort) in one pass, then rebuild the array from the tallies in a second pass. The counting makes this specialized sort more efficient than any general-purpose comparison sort, at the price of traversing the data twice.

1. Allocate `count = [0, 0, 0]`, one slot per color.
2. First pass: for each `num` in `nums`, increment `count[num]`.
3. Second pass: walk `color` through `0`, `1`, `2`, writing `count[color]`
   copies of `color` into `nums` at the running position `index`.

#### Walkthrough

Let us run Counting Sort on Example 1: `nums = [2,0,2,1,1,0]`. The first pass tallies each color as it is seen:

```text
num = 2    count = [0, 0, 1]
num = 0    count = [1, 0, 1]
num = 2    count = [1, 0, 2]
num = 1    count = [1, 1, 2]
num = 1    count = [1, 2, 2]
num = 0    count = [2, 2, 2]
```

The tallies say the sorted array is two `0`s, then two `1`s, then two `2`s. The second pass writes exactly that, advancing `index` once per element written:

```text
color = 0   writes indices 0-1   nums = [0, 0, 2, 1, 1, 0]
color = 1   writes indices 2-3   nums = [0, 0, 1, 1, 1, 0]
color = 2   writes indices 4-5   nums = [0, 0, 1, 1, 2, 2]
```

After the rebuild the array reads `[0,0,1,1,2,2]` in place, matching the expected Output.

#### Solution

The code is the two passes from the walkthrough: tally, then rebuild.

```python
from typing import List


class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Counting sort approach - count occurrences then rebuild array
        """
        # Count occurrences of each color
        count = [0, 0, 0]  # count[0], count[1], count[2]

        # First pass: count all colors
        for num in nums:
            count[num] += 1

        # Second pass: rebuild the array
        index = 0
        for color in range(3):  # 0, 1, 2
            for _ in range(count[color]):
                nums[index] = color
                index += 1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Two separate passes through the array, one to count and one to rebuild.

##### Space Complexity: `O(1)`

Uses a fixed-size counting array of 3 elements regardless of input size.

#### Key Insights

- **Constraint exploitation**: Takes advantage of the limited range of values (only 0, 1, 2) rather than using general sorting
- **Multiple passes for simplicity**: Counting sort uses two passes for simpler, easier-to-verify logic
- **Generalizes cleanly**: Counting sort extends naturally if the number of distinct values grows
- **Easier to debug**: The two-pass structure provides an intuitive implementation that is easy to verify and debug

### Dutch National Flag Algorithm

#### Derivation

Counting Sort makes one pass to learn the tallies and a second pass to write them back. The follow-up asks whether the second pass can be avoided: can each element land in its final region the moment it is examined? The [classic algorithm](https://en.wikipedia.org/wiki/Dutch_national_flag_problem) designed by Edsger Dijkstra does exactly that with three pointers that partition the array into three regions in a single pass: `left` (boundary between 0s and 1s), `right` (boundary between 1s and 2s), and `current` (element being examined). A `0` belongs at the front, so swap it to `left`; a `2` belongs at the back, so swap it to `right`; a `1` is already in the middle, so leave it. The key subtlety is that when swapping a 2 to the right, we must re-examine the swapped element without advancing `current`.

1. Initialize `left = 0`, `right = len(nums) - 1`, `current = 0`.
2. While `current <= right`, inspect `nums[current]`.
3. On a `0`, swap `nums[left]` with `nums[current]`, then advance both `left`
   and `current`.
4. On a `1`, advance `current` alone.
5. On a `2`, swap `nums[current]` with `nums[right]` and decrement `right`,
   leaving `current` in place to re-examine the value that arrived.

#### Invariant

Three pointers cut the array into four regions, and the loop preserves this at every step:

$$ \underbrace{[\,0,\ \textit{left}\,)}_{\text{all } 0} \quad \underbrace{[\,\textit{left},\ \textit{current}\,)}_{\text{all } 1} \quad \underbrace{[\,\textit{current},\ \textit{right}\,]}_{\text{unexamined}} \quad \underbrace{(\,\textit{right},\ n\,)}_{\text{all } 2} $$

```text
nums[0 .. left - 1]        all 0
nums[left .. current - 1]  all 1
nums[current .. right]     unexamined
nums[right + 1 .. n - 1]   all 2
```

The loop runs while the unexamined region is non-empty (\(\textit{current} \le \textit{right}\)) and shrinks it by one each pass, which is what guarantees termination and the single-pass bound.

The asymmetry in the code follows directly. Swapping a `0` leftward exchanges it with a position in the all-`1` region, whose value is already known to be `1`, so `current` may advance immediately. Swapping a `2` rightward brings back a value from the **unexamined** region, which has not been classified yet, so `current` must hold still and re-examine it. Advancing there would step over an unclassified element and break the invariant.

At exit \(\textit{current} > \textit{right}\), the unexamined region is empty and the three colour regions tile the array in order.

#### Walkthrough

Let us run the single pass on Example 1: `nums = [2,0,2,1,1,0]`, starting with `left = 0`, `right = 5`, `current = 0`. Each line shows the value examined, the action taken, and the state after it:

```text
nums[0]=2   swap with nums[right=5], right=4   nums=[0,0,2,1,1,2]  current stays 0
nums[0]=0   swap with nums[left=0], left=1     nums unchanged      current -> 1
nums[1]=0   swap with nums[left=1], left=2     nums unchanged      current -> 2
nums[2]=2   swap with nums[right=4], right=3   nums=[0,0,1,1,2,2]  current stays 2
nums[2]=1   already in place                   nums unchanged      current -> 3
nums[3]=1   already in place                   nums unchanged      current -> 4
current=4 > right=3: loop exits
```

The first line is the moment the Invariant warns about: the swap with `right` pulls the unexamined `0` from index `5` into position `0`, and because `current` holds still, the very next line classifies that `0` and sends it into the low region. The two swaps with `left` are self-swaps (`left == current` while no `1` has yet been seen), which still advance both boundaries correctly. The same pattern repeats at `current = 2`: the `2` swaps rightward, `current` stays, and the arriving `1` is classified on the next line. The array ends as `[0,0,1,1,2,2]` in place, matching the expected Output.

#### Solution

The code is the three-way branch from the walkthrough, one case per color.

```python
from typing import List


class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Dutch National Flag Algorithm - Three-way partitioning in one pass
        """
        left = 0        # Everything before left is 0
        right = len(nums) - 1  # Everything after right is 2
        current = 0     # Current element being processed

        while current <= right:
            if nums[current] == 0:
                # Move 0 to the left region
                nums[left], nums[current] = nums[current], nums[left]
                left += 1
                current += 1  # Safe to advance since we know nums[left] was processed
            elif nums[current] == 1:
                # 1 is already in correct position, just move forward
                current += 1
            else:  # nums[current] == 2
                # Move 2 to the right region
                nums[current], nums[right] = nums[right], nums[current]
                right -= 1
                # Don't advance current! We need to process the swapped element
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Single pass through the array with each element processed at most twice.

##### Space Complexity: `O(1)`

Only uses three pointer variables.

#### Key Insights

- **Single-pass efficiency**: Dutch Flag achieves optimal efficiency with one pass, satisfying the follow-up constraint
- **Three-way partitioning**: The algorithm demonstrates elegant three-way partitioning that generalizes to quicksort optimizations
- **Constraint exploitation**: Takes advantage of the limited range of values (only 0, 1, 2) rather than using general sorting
- **Pointer movement strategy**: Careful pointer advancement prevents infinite loops and ensures correctness; when swapping a 2 to the right, `current` must stay put since the swapped-in element is unexamined

## Comparison of Solutions

### Time Complexity

- **Selection Sort**: `O(n^2)` - For every position it rescans the unsorted tail to find the minimum
- **Counting Sort**: `O(n)` - Two separate passes, one to count and one to rebuild
- **Dutch National Flag Algorithm**: `O(n)` - Single pass with each element processed at most twice

### Space Complexity

- **Selection Sort**: `O(1)` - Sorts in place with only index variables
- **Counting Sort**: `O(1)` - Fixed-size counting array of three elements
- **Dutch National Flag Algorithm**: `O(1)` - Only three pointer variables

### Trade-offs

- Selection Sort is the simplest to derive because it sorts by hand and uses no property of the values, but its quadratic comparison count makes it the slowest
- The Counting Sort approach is simpler to reason about and verify than Dutch Flag, at the cost of a second traversal of the array
- The Dutch National Flag algorithm sorts in a single pass but requires careful pointer management to remain correct

### When to Use Each

- **Selection Sort**: Only as a from-scratch baseline; never the right call at scale, but it answers "sort it yourself" with zero cleverness
- **Counting Sort**: When implementation clarity and ease of debugging matter more than minimizing passes
- **Dutch National Flag Algorithm**: When a true one-pass, in-place solution is required (satisfies the follow-up constraint)

### Optimization Notes

- Selection Sort ignores the three-value constraint entirely; both linear solutions exploit the limited value range (only `0`, `1`, `2`) to beat general-purpose `O(n log n)` sorting
- The Dutch National Flag algorithm is the recommended solution because it achieves one pass with constant space
- The critical pitfall in Dutch Flag is advancing `current` after swapping a `2` to the right: the swapped-in element is unexamined, so `current` must stay put
- Counting Sort generalizes cleanly if the number of distinct values grows, whereas Dutch Flag is tailored to three-way partitioning
