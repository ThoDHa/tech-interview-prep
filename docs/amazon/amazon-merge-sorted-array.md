# [Merge Sorted Array](https://www.fastprep.io/problems/amazon-merge-sorted-array)

**Easy** | **NN minutes** | **Array, Two Pointers, Sorting**

You are given two integer arrays nums1 and nums2, each sorted in non-decreasing order, and two integers m and n representing the number of valid elements in the arrays.

Merge the valid elements of nums1 and all elements of nums2 into nums1 in non-decreasing order.

nums1 has length m + n. Its first m elements are valid input values, while its final n positions are placeholders that should be ignored before the merge.nums2 has length n.Modify nums1 in place, then return the merged nums1.

## Examples

### Example 1

**Input:** `nums1 = [1,2,3,0,0,0]`, `m = 3`, `nums2 = [2,5,6]`, `n = 3`

**Output:** `[1,2,2,3,5,6]`

**Explanation:** The valid portions are [1,2,3] and [2,5,6]. Their merged order is [1,2,2,3,5,6].

### Example 2

**Input:** `nums1 = [1]`, `m = 1`, `nums2 = []`, `n = 0`

**Output:** `[1]`

**Explanation:** The second array is empty, so nums1 remains unchanged.

### Example 3

**Input:** `nums1 = [0]`, `m = 0`, `nums2 = [1]`, `n = 1`

**Output:** `[1]`

**Explanation:** nums1 has no valid input elements. Its single position is merge capacity for the value from nums2.

## Constraints

- `nums1.length == m + n`
- `nums2.length == n`
- `0 <= m, n <= 200`
- `1 <= m + n <= 200`
- `-10^9 <= nums1[i], nums2[j] <= 10^9`
- `The first m elements of nums1 and all elements of nums2 are sorted in non-decreasing order.`

## Solutions

### Merge into an Auxiliary Array

#### Derivation

The most literal reading of "merge two sorted sequences" is the textbook two-pointer walk taught for [merge sort](https://en.wikipedia.org/wiki/Merge_algorithm)'s combine step: hold a read finger on each valid prefix, repeatedly copy the smaller front element into an output list, and drain whichever array still has elements. The twist here is in-place storage, so after the merged order is built the result is copied back into `nums1`:

1. Start `first = 0` at the head of the valid part of `nums1` and
   `second = 0` at the head of `nums2`.
2. While both fingers are valid, append the smaller front element to `merged`
   and advance that finger; `<=` keeps the merge stable.
3. Append the remainder of `nums1[:m]`, then the remainder of `nums2`.
4. Copy `merged` back into `nums1` with slice assignment and return `nums1`.

#### Walkthrough

Example 1: `nums1 = [1,2,3,0,0,0]` with `m = 3`, `nums2 = [2,5,6]` with `n = 3`. Each line is one append to `merged`:

```text
first=1, second=2   1 <= 2 -> take 1 from nums1   merged = [1]
first=2, second=2   2 <= 2 -> take 2 from nums1   merged = [1,2]
first=3, second=2   2 < 3  -> take 2 from nums2   merged = [1,2,2]
first=3, second=5   3 < 5  -> take 3 from nums1   merged = [1,2,2,3]
nums1 drained       drain nums2: 5, then 6        merged = [1,2,2,3,5,6]
```

The copy-back makes `nums1 = [1,2,2,3,5,6]`, the expected Output.

#### Solution

The code is the three-loop walk from the walkthrough plus the copy-back.

```python
from typing import List


class Solution:
    def mergeSortedArray(self, nums1: List[int], m: int, nums2: List[int], n: int) -> List[int]:
        merged: List[int] = []
        first = 0
        second = 0

        while first < m and second < n:
            if nums1[first] <= nums2[second]:
                merged.append(nums1[first])
                first += 1
            else:
                merged.append(nums2[second])
                second += 1
        while first < m:
            merged.append(nums1[first])
            first += 1
        while second < n:
            merged.append(nums2[second])
            second += 1

        nums1[:] = merged
        return nums1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m + n)`

Every valid element is appended exactly once and copied back exactly once.

##### Space Complexity: `O(m + n)`

The auxiliary list holds the full merged result.

#### Key Insights

- The merge itself needs only the two read fingers; the output buffer is what costs the extra space.
- `nums1[:] = merged` mutates the caller's list object in place, honoring the contract even though a temporary was used.
- The two drain loops cover the asymmetric endings: at most one of them does any work.

### Backward Two-Pointer Merge

#### Derivation

The auxiliary-array merge overwrites nothing only because it builds elsewhere, and the trailing placeholder slots of `nums1` are exactly free space of the right size. The insight is to fill that space from the right: the largest remaining element of either array belongs at index `m + n - 1`, and that slot currently holds a placeholder, so writing there destroys nothing. Placing from largest to smallest means the write pointer can never collide with the valid part of `nums1` before that part is exhausted:

1. Set `write = m + n - 1`, `first = m - 1`, `second = n - 1`, all reading
   from the backs.
2. While `second >= 0`, compare `nums1[first]` and `nums2[second]`; move the
   larger to `nums1[write]` and decrement that finger and `write`.
3. When `nums1`'s valid part is exhausted (`first < 0`), the remaining
   `nums2` prefix copies straight down; when `nums2` is exhausted the loop
   ends and the rest of `nums1` already sits where it belongs.
4. Return `nums1`.

#### Walkthrough

Example 1. Each line is one placement at `write`; `f`, `s`, `w` are `first`, `second`, `write`:

```text
start                 nums1 = [1,2,3,_,_,_]  f=2 s=2 w=5
w=5   max(3, 6) = 6   nums1 = [1,2,3,_,_,6]  f=2 s=1 w=4
w=4   max(3, 5) = 5   nums1 = [1,2,3,_,5,6]  f=2 s=0 w=3
w=3   max(3, 2) = 3   nums1 = [1,2,3,3,5,6]  f=1 s=0 w=2
w=2   max(2, 2) = 2'  nums1 = [1,2,2,3,5,6]  f=1 s=-1 -> loop ends
```

The strict `>` comparison sends ties to `nums2`, so at `w=2` the `nums2` 2 moves first (marked `2'`); with `second` now `-1` the loop stops and `nums1 = [1,2,2,3,5,6]`, the expected Output, with every write having landed on a placeholder or an already-moved value.

#### Solution

The code is the backward placement loop from the walkthrough. The guard `first >= 0` folds both comparison branches into one condition.

```python
from typing import List


class Solution:
    def mergeSortedArray(self, nums1: List[int], m: int, nums2: List[int], n: int) -> List[int]:
        write = m + n - 1
        first = m - 1
        second = n - 1

        while second >= 0:
            if first >= 0 and nums1[first] > nums2[second]:
                nums1[write] = nums1[first]
                first -= 1
            else:
                nums1[write] = nums2[second]
                second -= 1
            write -= 1

        return nums1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m + n)`

Each placement consumes exactly one element of `nums2` (or moves a `nums1` element aside), and every element is written at most once.

##### Space Complexity: `O(1)`

Three integer fingers, no auxiliary storage.

#### Key Insights

- Filling from the back converts the placeholder tail from an obstacle into the merge buffer itself.
- The loop condition is `second >= 0`, not `write >= 0`: once `nums2` is drained, whatever remains in `nums1` is already in sorted position.
- Elements of `nums1` may be shifted (the 3 above moved from index 2 to 3), but only after their slot's final value was already copied out, so nothing is lost.

### Sorted Concatenation One-Liner

#### Derivation

The whole task reduces to one expression: the valid prefix of `nums1` glued to `nums2`, sorted. Sorting discards the "already sorted" structure the other approaches exploit, but for an OA-scale input it is the shortest correct answer. Slice assignment writes the result back into the caller's list:

1. Build `nums1[:m] + nums2`, the multiset of values to merge.
2. Sort it and assign the result back into `nums1` with `nums1[:]`.
3. Return `nums1`.

#### Walkthrough

Example 1, no fingers to trace; the expression does all the work:

```text
nums1[:m] + nums2 = [1,2,3] + [2,5,6] = [1,2,3,2,5,6]
sorted(...)                          = [1,2,2,3,5,6]
nums1[:] = ...                       -> nums1 = [1,2,2,3,5,6]
```

The returned list is the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def mergeSortedArray(self, nums1: List[int], m: int, nums2: List[int], n: int) -> List[int]:
        nums1[:] = sorted(nums1[:m] + nums2)
        return nums1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((m + n) log (m + n))`

One sort over the combined element count, dominating the concatenation.

##### Space Complexity: `O(m + n)`

The concatenated list and the sorted result.

#### Key Insights

- Correctness needs no structure, which is why the one-liner is a safe sanity oracle for the in-place merges.
- The `nums1[:] =` slice assignment is what keeps the in-place contract; `nums1 = sorted(...)` would rebind the local name only.

## Comparison of Solutions

### Time Complexity

- **Merge into an Auxiliary Array**: `O(m + n)` - single pass plus an equal-length copy-back.
- **Backward Two-Pointer Merge**: `O(m + n)` - single pass, each element written once.
- **Sorted Concatenation One-Liner**: `O((m + n) log (m + n))` - sorting the combined values.

### Space Complexity

- **Merge into an Auxiliary Array**: `O(m + n)` - auxiliary list the size of the result.
- **Backward Two-Pointer Merge**: `O(1)` - three index fingers.
- **Sorted Concatenation One-Liner**: `O(m + n)` - the concatenated and sorted temporaries.

### Trade-offs

- **Merge into an Auxiliary Array**: the clearest statement of the textbook merge, at the cost of an output buffer and a copy-back.
- **Backward Two-Pointer Merge**: optimal time and constant space with no copy-back, at the cost of reasoning about which writes are safe.
- **Sorted Concatenation One-Liner**: minimal code and hard to get wrong, but it ignores both arrays' sortedness and pays a log factor.

### When to Use Each

- **Backward Two-Pointer Merge (Recommended)**: the interview answer: in place, `O(m + n)` time, `O(1)` space, and the placeholder tail is the point of the question.
- **Merge into an Auxiliary Array**: when in-place is not required, or as the stepping stone that motivates the backward trick.
- **Sorted Concatenation One-Liner**: for a quick OA submission or as a test oracle; mention its `log` cost if asked for complexity.

### Optimization Notes

- The backward merge's loop runs while `second >= 0`; looping on `write >= 0` instead adds useless iterations and, worse, needs a separate guard to avoid comparing exhausted fingers.
- The comparison `nums1[first] > nums2[second]` with the tie taking from `nums2` mirrors the forward merge's stable `<=`; stability is invisible in the integer result but matters if the element type carries identity.
- Both linear approaches are asymptotically optimal: any correct merge must inspect every element at least once.
- In production, `heapq.merge` or `list.sort` over the concatenation in C-backed CPython is usually faster in wall-clock terms than a pure-Python two-pointer loop; the hand-written merge is the interview artifact.
