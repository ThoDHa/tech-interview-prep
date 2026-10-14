# [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/)

**Hard** | **40 minutes** | **Array, Queue, Sliding Window, Heap (Priority Queue), Monotonic Queue**

**Pattern:** [Sliding Window](../patterns/sliding_window/intuition.md), [Heap / Priority Queue](../patterns/heap/intuition.md)

**Algorithm:** [Sliding window](https://usaco.guide/gold/sliding-window) · [Heap (data structure)](https://en.wikipedia.org/wiki/Heap_(data_structure)) · [Double-ended queue](https://en.wikipedia.org/wiki/Double-ended_queue)

**Practice:** [`practice/sliding_window_maximum/solution.py`](../../practice/sliding_window_maximum/solution.py)

You are given an array of integers `nums` and an integer `k`. There is a sliding window of size `k` that starts at the left edge of the array. The window slides one position to the right until it reaches the right edge of the array.

Return a list that contains the maximum element in the window at each step.

## Examples

### Example 1

**Input:** `nums = [1,2,1,0,4,2,6], k = 3`

**Output:** `[2,2,4,4,6]`

**Explanation:** Window position            Max
---------------           -----
[1  2  1] 0  4  2  6        2
 1 [2  1  0] 4  2  6        2
 1  2 [1  0  4] 2  6        4
 1  2  1 [0  4  2] 6        4
 1  2  1  0 [4  2  6]       6

## Constraints

- `1 <= nums.length <= 100,000`
- `-10,000 <= nums[i] <= 10,000`
- `1 <= k <= nums.length`

## Deriving the Solution

A window's maximum changes only at its edges: sliding right by one drops the element that leaves and adds the element that enters, and the answer for every window is the largest value currently inside it. Every solution below maintains that maximum per window position; they differ in how much work the edge movement triggers.

1. **Start literal.** Recompute `max` over each window from scratch. With `n`
   windows of `k` elements each, that costs `O(n * k)`, which degrades on large
   `k`: see [Brute Force](#brute-force).
2. **Spot the waste.** Consecutive windows share `k - 1` of their `k` elements,
   yet the brute force re-reads all of them. The incoming and outgoing elements
   are the only real information in a slide, so a structure updated per edge
   should answer each maximum without rescanning the window.
3. **Repair with a heap.** Keep every window element in a max-heap; the root is
   the maximum. The root can name an element that already left, so each pop
   lazily discards stale entries by index. Each push costs `O(log n)` and stale
   entries linger, so the heap grows beyond the window: better, not optimal:
   see [Max-Heap](#max-heap).
4. **Keep only candidates.** A value `nums[j]` dominated by a newer, larger
   `nums[i]` (`j < i`, `nums[j] <= nums[i]`) can never be a future answer: the
   newer value outlives it inside every window they share. Discarding dominated
   values leaves a deque of indices whose values are strictly decreasing, with
   the window maximum at the front. Each index enters and leaves once, so the
   whole sweep is `O(n)`: see [Monotonic Deque](#monotonic-deque).

## Solutions

### Brute Force

#### Derivation

The most direct reading of the problem computes, for each window position, the maximum of the `k` values inside it. The window starting at index `i` spans `nums[i .. i + k - 1]`, and there are `n - k + 1` such positions:

1. For each start index `i` from `0` to `len(nums) - k`.
2. Compute `max(nums[i : i + k])` over the window's values.
3. Append that maximum to the result list.

#### Walkthrough

Run the per-window scans on Example 1: `nums = [1,2,1,0,4,2,6]`, `k = 3`, which has `7 - 3 + 1 = 5` windows. Each row shows the window slice and the `max` computed over it:

```text
i=0   nums[0:3] = [1, 2, 1]   max = 2
i=1   nums[1:4] = [2, 1, 0]   max = 2
i=2   nums[2:5] = [1, 0, 4]   max = 4
i=3   nums[3:6] = [0, 4, 2]   max = 4
i=4   nums[4:7] = [4, 2, 6]   max = 6
```

The five per-window maxima collected in order are `[2, 2, 4, 4, 6]`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's slice-and-max per window position.

```python
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        result = []
        for i in range(len(nums) - k + 1):
            # Recompute the maximum over the whole window slice
            result.append(max(nums[i : i + k]))
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * k)`

There are `n - k + 1` windows, and each `max` call scans all `k` window values.

##### Space Complexity: `O(1)`

Beyond the output list, only the loop index and the slice boundary are stored.

#### Key Insights

- Directly restates the problem; hard to get wrong.
- Every slide re-reads `k - 1` values already seen, which is the wasted work.
- Fine for tiny inputs, but at the constraint sizes (`n` up to `100,000`) a
  large `k` makes it impractically slow.

### Max-Heap

#### Derivation

The brute force wastes its scan on values that cannot matter: the maximum of the previous window is still the maximum of the new one unless the outgoing element was the maximum. A [max-heap](https://en.wikipedia.org/wiki/Priority_queue) turns "find the largest" into a constant-time root read: push every value with its index, and the root is the window maximum. The wrinkle is eviction: a heap knows priorities, not positions, so an element that slid out of the window still sits there. Each query therefore pops the root until the root's index re-enters the window, discarding stale entries lazily:

1. For each window start `i`, push `(nums[i + k - 1], i + k - 1)`; the heap
   holds every value seen so far, newest on top only if largest.
2. Before reading the answer for window `i`, pop every heap top whose index
   `j <= i - k`: those elements have left the window.
3. The surviving root `(nums[j], j)` holds the window maximum; record `nums[j]`.

#### Walkthrough

Trace the lazy eviction on a tailored prefix of Example 1, `nums = [1, 2, 1, 0]`, `k = 3`, which shows the blind spot: an entry that has left the window survives as long as it stays buried below the root. The heap holds `(-value, index)` pairs, so the root is the largest value, and value ties surface the older index (the smaller tuple):

```text
i=0  push (-1, 0)   root (-1, 0)   stale check 0 <= -3: no pop   no emission (i < 2)
i=1  push (-2, 1)   root (-2, 1)   stale check 1 <= -2: no pop   no emission (i < 2)
i=2  push (-1, 2)   root (-2, 1)   stale check 1 <= -1: no pop   -> answer 2
i=3  push (0, 3)    root (-2, 1)   stale check 1 <= 0: no pop    -> answer 2
```

At `i = 3` the window is `[2, 1, 0]`, and the entry `(-1, 0)` has left it: its index `0` satisfies `0 <= 3 - 3`. But it sits below the root, and the eviction loop only ever inspects the root `(-2, 1)`, whose index `1` is still inside the window (`1 <= 0` is false). No pop fires, the answer `2` is read, and the stale entry lingers, which is exactly the deferred work the deque section's index `0` avoids by being evicted at `i = 1`. The first two rows also show the emission guard: nothing is recorded until `i = 2` completes the first window. The recorded answers `2, 2` are the full run's output for `nums = [1,2,1,0]` with `k = 3`: the window `[1, 2, 1]` reads `2`, and the window `[2, 1, 0]` reads `2`.

#### Solution

The code is the push-per-slide and pop-stale-roots loop from the walkthrough, with a heap of `(-value, index)` pairs so Python's min-heap behaves as a max-heap (value ties surface the older index first, the smaller tuple, so an expiring older twin is discarded before a fresh younger one):

```python
import heapq
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        heap = []
        result = []
        for i, value in enumerate(nums):
            heapq.heappush(heap, (-value, i))
            while heap[0][1] <= i - k:
                # The root's element has left the window; discard it lazily
                heapq.heappop(heap)
            if i >= k - 1:
                result.append(-heap[0][0])
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Each of the `n` pushes costs `O(log n)`. A single element may be popped once, but only when it surfaces at the root, and the interleaved pop sequences still bound the total at `O(n log n)`.

##### Space Complexity: `O(n)`

Stale entries are evicted only when they reach the root, so the heap can hold every element at once.

#### Key Insights

- Converts a per-window scan into a per-slide update, with the root as the answer.
- Lazy eviction: the heap evicts by index check at query time, not at slide time.
- The `(-value, index)` pair is the standard idiom for max-heaps in Python and
  breaks value ties toward the older index, the smaller tuple.

### Monotonic Deque

#### Derivation

The heap's weakness is the stale entries it cannot see. The observation that removes them entirely: if `nums[j] <= nums[i]` for `j < i`, then `nums[j]` can never be a window maximum again. Every future window containing `j` also contains `i` (windows only advance rightward), and `i`'s value is at least as large. So the only indices worth remembering are those that are still in the window and larger than everything after them, which is precisely a [deque](https://en.wikipedia.org/wiki/Double-ended_queue) of indices holding a strictly decreasing sequence of values:

1. For each new index `i`, pop from the back while `nums[back] <= nums[i]`:
   those values are dominated forever.
2. Push `i` to the back.
3. Pop from the front while `front <= i - k`: the front left the window.
4. Once the first window completes (`i >= k - 1`), record `nums[front]`, which
   is the maximum by the decreasing invariant.

Steps 1 and 3 sound similar but act on opposite ends: step 1 evicts dominated values before they ever become stale, step 3 evicts genuinely expired ones. Each index is appended once and popped at most once from either end, which is what makes the whole sweep linear.

#### Walkthrough

Trace the deque by hand on Example 1: `nums = [1,2,1,0,4,2,6]`, `k = 3`. Each row shows the deque after the back-pops, the new index, the front-expiry check, and the answer once `i >= 2`:

```text
i=0  value 1   back-pops: none       deque [0]        front 0 in window   -
i=1  value 2   pop 0 (1 <= 2)        deque [1]        front 1 in window   -
i=2  value 1   back-pops: none       deque [1, 2]     front 1 in window   -> nums[1] = 2
i=3  value 0   back-pops: none       deque [1, 2, 3]  front 1 > 0         -> nums[1] = 2
i=4  value 4   pop 3 (0 <= 4), pop 2 (1 <= 4), pop 1 (2 <= 4)
                                     deque [4]        front 4 in window   -> nums[4] = 4
i=5  value 2   back-pops: none       deque [4, 5]     front 4 in window   -> nums[4] = 4
i=6  value 6   pop 5 (2 <= 6), pop 4 (4 <= 6)
                                     deque [6]        front 6 in window   -> nums[6] = 6
```

The trickiest step is `i = 4`: value `4` dominates the entire surviving deque `[2, 1, 0]`, so all three indices are discarded at once and `4` becomes the sole candidate. The recorded answers `[2, 2, 4, 4, 6]` match the expected Output for Example 1, and note how the index `0` (value `1`) was evicted at `i = 1` before it could ever go stale, exactly the work the heap defers.

#### Solution

The code is the walkthrough's four beats per slide: back-pops on the new value, append, front-expiry pop, then the answer read.

```python
from collections import deque
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        window = deque()
        result = []
        for i, value in enumerate(nums):
            # Discard values the new element dominates forever
            while window and nums[window[-1]] <= value:
                window.pop()
            window.append(i)
            if window[0] <= i - k:
                window.popleft()
            if i >= k - 1:
                result.append(nums[window[0]])
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each index is appended to the deque exactly once and popped at most once (from either end), so the total deque work across the whole run is `O(n)`.

##### Space Complexity: `O(k)`

The deque holds indices of the current window only: every index older than `i - k` is popped, and every dominated index is discarded eagerly.

#### Key Insights

- The dominance rule `nums[j] <= nums[i]` for `j < i` is what turns a heap into
  a deque: dominated values never need lazy eviction because they never survive.
- The deque stores indices, not values, so window expiry is one comparison at
  the front.
- Each element enters and leaves the deque at most once, the amortization that
  makes the monotonic technique linear; the same pattern solves problems from
  sliding-window minimum to largest rectangle in histogram.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n * k)` - rescans all `k` window values for each of the `n - k + 1` windows.
- **Max-Heap**: `O(n log n)` - one push per element plus lazy root evictions.
- **Monotonic Deque**: `O(n)` - each index enters and leaves the deque once.

### Space Complexity

- **Brute Force**: `O(1)` - only the loop index and slice bounds.
- **Max-Heap**: `O(n)` - stale entries survive until they surface at the root.
- **Monotonic Deque**: `O(k)` - only live, undominated indices of the current window.

### Trade-offs

- The brute force solution has no moving parts but pays `k` reads per slide,
  which collapses at the top of the constraint range.
- The max-heap solution is short and generalizes to any "extremum over a
  window" query, but stale entries inflate memory to `O(n)` and each push pays
  a logarithmic factor.
- The monotonic deque solution is linear in time and bounded by the window in
  space, at the cost of a data structure and invariant that must be reasoned
  about carefully.

### When to Use Each

- **Brute Force**: Prototyping, correctness cross-checks, or windows so small
  that `k` is effectively constant.
- **Max-Heap**: When a heap is already available and the sequence is short, or
  when the query is "largest element ever seen near position i" rather than
  strictly within a window.
- **Monotonic Deque**: The default for production and interviews; any problem
  asking for per-window extrema at the constraint sizes (recommended here).

### Optimization Notes

- The back-pop condition `nums[window[-1]] <= value` keeps the deque strictly
  decreasing; `>=` would make it non-increasing, which is equally correct but
  pops more on ties.
- The front-expiry test is a single comparison `window[0] <= i - k` because the
  window advances by exactly one per slide; a general range would need a `while`.
- The answer is read from `nums[window[0]]`, never stored in the deque: storing
  values alongside indices would double the structure for no benefit.
