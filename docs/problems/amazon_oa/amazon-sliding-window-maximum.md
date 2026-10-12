# [Sliding Window Maximum](https://www.fastprep.io/problems/amazon-sliding-window-maximum)

**Hard** | **NN minutes** | **Array, Sliding Window, Queue**

Given an integer array nums and a window size k, return the maximum value in every contiguous window of length k, from left to right.

## Examples

### Example 1

**Input:** `nums = [1,3,-1,-3,5,3,6,7]`, `k = 3`

**Output:** `[3,3,5,5,6,7]`

### Example 2

**Input:** `nums = [1]`, `k = 1`

**Output:** `[1]`

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-sliding-window-maximum; fill them in. -->

## Solutions

### Brute Force

#### Derivation

The most literal reading of the statement: one maximum is wanted for every window of `k` consecutive elements, and the maximum of a window is found by looking at all of its elements. So look at all of them, one window at a time:

1. Walk `start` over every window start, from `0` through `len(nums) - k`.
2. Set `window_max = nums[start]`, then scan `position` from `start + 1`
   through `start + k - 1`, raising `window_max` whenever `nums[position]`
   is larger.
3. Append `window_max` to `window_maxima` and move to the next start.

#### Walkthrough

Example 1, `nums = [1,3,-1,-3,5,3,6,7]`, `k = 3`. The scan slides the window one start at a time and rescans every element inside it:

```text
start 0   window [1, 3, -1]    window_max = 3
start 1   window [3, -1, -3]   window_max = 3
start 2   window [-1, -3, 5]   window_max = 5
start 3   window [-3, 5, 3]    window_max = 5
start 4   window [5, 3, 6]     window_max = 6
start 5   window [3, 6, 7]     window_max = 7
```

The collected maxima `[3, 3, 5, 5, 6, 7]` match the expected Output for Example 1.

#### Solution

```python
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        window_count = len(nums) - k + 1
        window_maxima = []
        for start in range(window_count):
            window_max = nums[start]
            for position in range(start + 1, start + k):
                if nums[position] > window_max:
                    window_max = nums[position]
            window_maxima.append(window_max)
        return window_maxima
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × k)`

Each of the `n - k + 1` windows is rescanned in full, and every element belongs to up to `k` windows.

##### Space Complexity: `O(1)`

Only the loop positions and the running maximum live outside the output list.

#### Key Insights

- Adjacent windows share `k - 1` of their `k` elements, and the brute force re-reads all of them on every slide; that overlap is exactly what the later approaches stop paying for.
- Correctness needs no invariant: each window's maximum is recomputed from scratch, so nothing can go stale.
- The approach is a legitimate interview starting point and a correctness oracle for checking the faster versions on small inputs.

### Max-Heap with Lazy Deletion

#### Derivation

The rescan is the flaw: neighboring windows differ by one leaving element and one entering element, yet the brute force re-reads everything in between. A max-heap over the values seen so far answers "largest so far" in logarithmic time, but a binary heap cannot evict the entries that slid out of the window, because they sit buried below larger values. The repair is lazy deletion: carry each value's `index` alongside it, and before trusting the root, pop while the root's index has left the window. Entries that expired while buried are harmless: they can only surface after every larger value above them, and the expiry check removes them at that moment. Python's `heapq` module is a min-heap, so values are pushed negated:

1. For each `index` of `nums`, push `(-value, index)` onto `max_heap`.
2. Pop from the heap while the root's index satisfies
   `max_heap[0][1] <= index - k`: that value left the window.
3. Once `index >= k - 1`, the negated root `-max_heap[0][0]` is the window
   maximum; append it to `window_maxima`.

#### Walkthrough

Example 1, `nums = [1,3,-1,-3,5,3,6,7]`, `k = 3`, one line per index:

```text
i=0  push (-1, 0)   root (-1, 0)   index 0 in window   i < 2
i=1  push (-3, 1)   root (-3, 1)   i < 2
i=2  push (-1, 2)   root (-3, 1)   index 1 in window   -> record 3
i=3  push (-3, 3)   root (-3, 1)   index 1 in window   -> record 3
i=4  push (-5, 4)   root (-5, 4)                       -> record 5
i=5  push (-3, 5)   root (-5, 4)                       -> record 5
i=6  push (-6, 6)   root (-6, 6)                       -> record 6
i=7  push (-7, 7)   root (-7, 7)                       -> record 7
```

The recorded values `[3, 3, 5, 5, 6, 7]` match the expected Output. Note the stale entry `(-3, 1)`, out of the window from `i = 4` onward: nothing pops it here, because the larger value `5` surfaces ahead of it and every later root is younger. It simply occupies memory, which is the lazy approach's known cost.

The expiry branch never fires on Example 1, so a tailored decreasing tail shows it working. With `nums = [5, 4, 3, 2]` and `k = 3`:

```text
i=2  root (-5, 0)   0 <= -1 is false                    -> record 5
i=3  push (-2, 3)   root (-5, 0)   0 <= 0 is true  -> pop
                    root (-4, 1)   1 <= 0 is false      -> record 4
```

The expired root is popped exactly when it surfaces, and the next root is already a live window member.

#### Solution

```python
import heapq
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        max_heap = []
        window_maxima = []
        for index, value in enumerate(nums):
            heapq.heappush(max_heap, (-value, index))
            while max_heap[0][1] <= index - k:
                heapq.heappop(max_heap)
            if index >= k - 1:
                window_maxima.append(-max_heap[0][0])
        return window_maxima
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Each of the `n` pushes costs `O(log n)` in the worst case; every entry is popped at most once, so the expiry checks amortize to constant time per element.

##### Space Complexity: `O(n)`

Stale entries survive until they surface at the root, so the heap can hold every element of a decreasing input.

#### Key Insights

- Lazy deletion trades memory for simplicity: instead of removing expired entries from the middle of the heap, wait until they surface and discard them then.
- Pairing every value with its index is what makes expiry a single comparison at the root.
- The heap generalizes to any "extremum over the last `k` items" query, including ones with no monotonic structure to exploit.

### Monotonic Deque

#### Derivation

The heap's remaining waste is the stale entries it must carry. The observation that removes them: if `nums[j] <= nums[i]` for `j < i`, then `nums[j]` can never be a window maximum again. Every future window that contains `j` also contains `i` (windows only advance rightward), and `i`'s value is at least as large. So the only indices worth remembering are those still in the window whose values exceed everything after them, which is a [deque](https://en.wikipedia.org/wiki/Double-ended_queue) of indices holding a strictly decreasing sequence of values:

1. For each new `index`, pop from the back while
   `nums[candidates[-1]] <= value`: those values are dominated forever.
2. Append `index`.
3. Pop from the front while `candidates[0] <= index - k`: the front left the
   window.
4. Once the first window completes (`index >= k - 1`), record
   `nums[candidates[0]]`, the maximum by the decreasing invariant.

Steps 1 and 3 act on opposite ends for opposite reasons: the back-pop evicts dominated values before they can go stale, the front-pop removes genuinely expired ones. Each index is appended once and popped at most once from either end, which is what makes the whole sweep linear.

#### Walkthrough

Example 1, `nums = [1,3,-1,-3,5,3,6,7]`, `k = 3`. Each line shows the back-pops, the deque after appending, and the recorded maximum once `i >= 2`:

```text
i=0  value 1    back-pops: none                  candidates [0]
i=1  value 3    pop 0 (1 <= 3)                   candidates [1]
i=2  value -1   back-pops: none                  candidates [1, 2]     -> record nums[1] = 3
i=3  value -3   back-pops: none                  candidates [1, 2, 3]  -> record nums[1] = 3
i=4  value 5    pop 3 (-3 <= 5), pop 2 (-1 <= 5), pop 1 (3 <= 5)
                                                 candidates [4]        -> record nums[4] = 5
i=5  value 3    back-pops: none                  candidates [4, 5]     -> record nums[4] = 5
i=6  value 6    pop 5 (3 <= 6), pop 4 (5 <= 6)   candidates [6]        -> record nums[6] = 6
i=7  value 7    pop 6 (6 <= 7)                   candidates [7]        -> record nums[7] = 7
```

The decisive step is `i = 4`: the value `5` dominates every surviving candidate `[3, -1, -3]`, so all three indices are discarded at once and `5` becomes the sole candidate. The recorded answers `[3, 3, 5, 5, 6, 7]` match the expected Output, and no entry was ever allowed to go stale.

#### Solution

The code is the walkthrough's four beats per slide: back-pops on the new value, append, front-expiry pop, then the answer read.

```python
from collections import deque
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        candidates = deque()
        window_maxima = []
        for index, value in enumerate(nums):
            while candidates and nums[candidates[-1]] <= value:
                candidates.pop()
            candidates.append(index)
            if candidates[0] <= index - k:
                candidates.popleft()
            if index >= k - 1:
                window_maxima.append(nums[candidates[0]])
        return window_maxima
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each index is appended to the deque exactly once and popped at most once, so the total deque work across the run is linear.

##### Space Complexity: `O(k)`

The deque holds indices of the current window only: expired indices are popped from the front and dominated ones from the back.

#### Key Insights

- The dominance rule `nums[j] <= nums[i]` for `j < i` turns the heap's lazy eviction into eager eviction: dominated values never enter the structure at all.
- The deque stores indices rather than values, so window expiry is one comparison at the front.
- The front-expiry test can be an `if` because the window advances one element per slide, so at most the front can expire on any step.
- Each element enters and leaves the deque at most once, the amortization that makes monotonic techniques linear; the same pattern solves sliding-window minimum and largest rectangle in histogram.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n × k)` - rescans all `k` window values for each of the `n - k + 1` windows.
- **Max-Heap with Lazy Deletion**: `O(n log n)` - one logarithmic push per element plus amortized pops.
- **Monotonic Deque**: `O(n)` - each index enters and leaves the deque once.

### Space Complexity

- **Brute Force**: `O(1)` - only loop positions and the running maximum.
- **Max-Heap with Lazy Deletion**: `O(n)` - stale entries survive until they surface at the root.
- **Monotonic Deque**: `O(k)` - only live, undominated indices of the current window.

### Trade-offs

- **Brute Force**: no moving parts and trivially correct, but it pays `k` reads per slide and collapses at the top of the constraint range.
- **Max-Heap with Lazy Deletion**: short to write and generalizes to any window-extremum query, but stale entries inflate memory to `O(n)` and each push pays a logarithmic factor.
- **Monotonic Deque**: linear time bounded by the window in space, at the cost of an invariant that must be reasoned about carefully.

### When to Use Each

- **Brute Force**: prototyping, correctness cross-checks, or windows so small that `k` is effectively constant.
- **Max-Heap with Lazy Deletion**: when a heap is already available and the input is short, or when the query has no monotonic structure to exploit.
- **Monotonic Deque (Recommended)**: the default for interviews and production whenever per-window extrema are wanted at scale.

### Optimization Notes

- The back-pop condition `nums[candidates[-1]] <= value` keeps the deque strictly decreasing; using `<` instead would keep equal values, which is equally correct but holds redundant entries.
- The expiry test fits an `if` because one element enters per slide; a variable window size would need a `while`.
- The heap version must run its expiry check before every root read; checking once per window is not enough, because several expired entries can sit stacked at the top.
