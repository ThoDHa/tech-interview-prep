# [Last Stone Weight](https://leetcode.com/problems/last-stone-weight/)

**Easy** | **15 minutes** | **Array, Heap (Priority Queue)**

**Pattern:** [Simulation](../patterns/simulation/intuition.md), [Heap / Priority Queue](../patterns/heap/intuition.md)

**Algorithm:** [Simulation](https://en.wikipedia.org/wiki/Simulation) · [Heap (data structure)](https://en.wikipedia.org/wiki/Heap_(data_structure)) · [Sorting](https://en.wikipedia.org/wiki/Sorting_algorithm)

**Practice:** [`practice/last_stone_weight/solution.py`](../../practice/last_stone_weight/solution.py)

You are given an array of integers `stones` where `stones[i]` represents the weight of the `ith` stone.

We want to run a simulation on the stones as follows:

* At each step we choose the **two heaviest stones**, with weight `x` and `y` and smash them togethers
* If `x == y`, both stones are destroyed
* If `x < y`, the stone of weight `x` is destroyed, and the stone of weight `y` has new weight `y - x`.

Continue the simulation until there is no more than one stone remaining.

Return the weight of the last remaining stone or return `0` if none remain.

## Examples

### Example 1

**Input:** `stones = [2,3,6,2,4]`

**Output:** `1`

**Explanation:** We smash 6 and 4 and are left with a 2, so the array becomes [2,3,2,2].
We smash 3 and 2 and are left with a 1, so the array becomes [1,2,2].
We smash 2 and 2, so the array becomes [1].

### Example 2

**Input:** `stones = [1,2]`

**Output:** `1`

## Constraints

- `1 <= stones.length <= 20`
- `1 <= stones[i] <= 100`

## Deriving the Solution

The whole problem is one repeated action: pick the two heaviest stones and replace them with their difference. Every solution below runs that loop; they differ only in how the two heaviest stones are found.

1. **Start literal.** Read the rule directly: scan the whole list for the two
   largest values, compute the outcome, and put any survivor back. Each round costs a full double scan of `O(n)`, and up to `n - 1` rounds run: see [Brute Force](#brute-force).
2. **Sort to find the pair faster.** Sorting once per round puts the heaviest
   pair at the end of the list, where `pop` retrieves them in `O(1)`; the sort itself is `O(n log n)` per round: see [Sort Each Round](#sort-each-round).
3. **Keep the order maintained.** A max-heap keeps the heaviest stone
   addressable in `O(1)` and repairs itself in `O(log n)`, so every round costs
   `O(log n)` instead of a resort: see [Max-Heap Simulation](#max-heap-simulation).

## Solutions

### Brute Force

#### Derivation

The most literal reading acts the rule out with the tools already at hand: to smash the two heaviest stones, look at every stone to find the heaviest, look again to find the second heaviest, and write the outcome back into the list. Python's `max` and `remove` express exactly that, so no extra structure is needed:

1. While `stones` holds at least two entries, scan for the heaviest value
   `first = max(stones)` and remove one occurrence of it with
   `stones.remove(first)`.
2. Scan the shortened list for `second = max(stones)` and remove it too.
3. If `first != second`, append the survivor `first - second`; if they are
   equal, both are destroyed and nothing is appended.
4. When fewer than two stones remain, return the last stone's weight, or `0`
   when the list is empty.

The list shrinks by one or two entries per round, so the loop always terminates.

#### Walkthrough

Let us run the smash loop by hand on Example 1: `stones = [2,3,6,2,4]`. Each row shows the pair the two `max` scans select, the survivor they produce, and the list the next round starts from:

```text
round 1   first=6, second=4   survivor 6-4=2   stones = [2, 3, 2, 2]
round 2   first=3, second=2   survivor 3-2=1   stones = [2, 2, 1]
round 3   first=2, second=2   both destroyed   stones = [1]
```

Round 3 destroys both stones because `first == second`, leaving a single stone of weight `1`, which is the expected Output for Example 1. The same trace matches the problem statement's own narration of this example.

#### Solution

```python
from typing import List


class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        while len(stones) > 1:
            first = max(stones)
            stones.remove(first)
            second = max(stones)
            stones.remove(second)
            if first != second:
                stones.append(first - second)
        return stones[0] if stones else 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

Each round performs two `max` scans and two `remove` scans, all `O(n)`, and up to `n - 1` rounds run because every round after a destruction reduces the count by exactly one. With `n <= 20` the constant factor keeps this instant.

##### Space Complexity: `O(1)`

The list is updated in place; only the scalar trackers `first` and `second` are extra.

#### Key Insights

- The simulation is the problem statement translated line by line, which makes
  it the easiest solution to get right under time pressure.
- `stones.remove(first)` removes one occurrence, which is exactly the semantics
  the rule needs for duplicate weights.
- The quadratic cost is invisible at `n <= 20` but would dominate at the scales
  the heap solution handles.

### Sort Each Round

#### Derivation

The brute force spends its whole budget on one question: where are the two heaviest stones? Sorting answers it as a side effect. After `stones.sort()`, the heaviest sits at the end and the second heaviest just before it, so `pop` retrieves both in constant time, and any surviving stone can be appended knowing the next round's sort will restore order. The repair is replacing the four linear scans with one sort per round:

1. While `stones` holds at least two entries, sort it ascending with
   `stones.sort()`.
2. `pop` the heaviest stone `first` and the second heaviest `second` from the
   end of the list.
3. If `first != second`, append the survivor `first - second`; the next
   iteration's sort re-positions it.
4. When fewer than two stones remain, return the last stone's weight, or `0`
   when the list is empty.

#### Walkthrough

Let us trace the sort-and-pop loop on Example 1: `stones = [2,3,6,2,4]`. Each row shows the list as sorted, the two stones popped off the end, and what the working list holds afterwards:

```text
round 1   sorted [2, 2, 3, 4, 6]   pop 6, pop 4   survivor 2 -> [2, 3, 2, 2]
round 2   sorted [2, 2, 2, 3]      pop 3, pop 2   survivor 1 -> [2, 2, 1]
round 3   sorted [1, 2, 2]         pop 2, pop 2   destroyed -> [1]
```

One stone of weight `1` remains, matching the expected Output for Example 1. Note that a surviving stone is appended unsorted (round 1 leaves `[2, 3, 2, 2]`); the correctness does not depend on it because every round re-sorts before popping.

#### Solution

```python
from typing import List


class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        while len(stones) > 1:
            stones.sort()
            first = stones.pop()
            second = stones.pop()
            if first != second:
                stones.append(first - second)
        return stones[0] if stones else 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n² log n)`

Each round sorts the whole list at `O(n log n)` and up to `n - 1` rounds run, for `O(n² log n)` overall. On this problem's tiny inputs that is still instantaneous, but the sort repeats work the heap below avoids.

##### Space Complexity: `O(n)` or `O(1)`

`stones.sort()` sorts in place, and its Timsort implementation still allocates up to `O(n)` scratch in the worst case; nearly-sorted inputs stay at `O(1)`. No other structures are created.

#### Key Insights

- Sorting converts the expensive "find the two heaviest" scan into two constant-
  time pops at the price of one sort per round.
- The survivor is appended out of order on purpose: correctness only needs the
  list sorted when the next pair is chosen, not between rounds.
- The idea is a stepping stone toward the heap: both maintain "the heaviest is
  cheap to retrieve", the heap just does it incrementally.

### Max-Heap Simulation

#### Derivation

The sort-each-round solution re-sorts stones whose positions have not changed, only to learn the heaviest stone's identity again. A [heap](https://en.wikipedia.org/wiki/Heap_(data_structure)) is the structure built for exactly this rhythm: the maximum is always at the top, and each push or pop repairs the order in `O(log n)` without touching the rest. Python's `heapq` module provides only a min-heap, and the weights are all positive, so negating every weight mirrors the order: the most negative element is the largest original. With that trick, each smash is two pops and at most one push:

1. Build `heap` by negating every weight and heapifying it, an `O(n)` operation.
2. While `heap` holds at least two entries, pop the heaviest
   `first = -heappop(heap)` and the second heaviest `second = -heappop(heap)`,
   negating back to positive weights.
3. If `first != second`, push the survivor back as `-(first - second)`.
4. When the loop ends, return `-heap[0]` if one stone remains, or `0` if the
   heap emptied.

#### Walkthrough

Let us trace the heap through Example 1: `stones = [2,3,6,2,4]`. The heap stores negated weights; every state below shows its contents as the original positive weights, so the heaviest stone is always the first value listed:

```text
build       heap = [6, 4, 3, 2, 2]                (as weights)
round 1     pop 6, pop 4    survivor 2 -> push    heap = [3, 2, 2, 2]
round 2     pop 3, pop 2    survivor 1 -> push    heap = [2, 2, 1]
round 3     pop 2, pop 2    both destroyed        heap = [1]
```

The heap ends holding a single weight `1`, so the function returns `-heap[0] = 1`, matching the expected Output for Example 1. Had round 3's pair been equal, the heap would have emptied and the function would have returned `0` instead.

#### Solution

The code is the negated heap driven by the walkthrough's pop-pop-push loop.

```python
import heapq
from typing import List


class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        heap = [-stone for stone in stones]
        heapq.heapify(heap)
        while len(heap) > 1:
            first = -heapq.heappop(heap)
            second = -heapq.heappop(heap)
            if first != second:
                heapq.heappush(heap, -(first - second))
        return -heap[0] if heap else 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Heapifying the `n` weights is `O(n)`, and the simulation runs up to `n - 1` rounds, each doing two pops and at most one push at `O(log n)` apiece.

##### Space Complexity: `O(n)`

The negated copy `heap` holds all `n` weights; it replaces the input list rather than growing past it.

#### Key Insights

- Negating every weight turns Python's min-heap into a max-heap; this is the
  standard idiom because `heapq` ships no max-heap variant.
- The heap never re-examines stones it does not have to: after each smash only
  `O(log n)` sift work restores the order, versus a full resort.
- Returning `-heap[0]` only when the heap is non-empty handles both endings of
  the simulation: one survivor or total destruction.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n²)` - each round scans the list twice to find the pair.
- **Sort Each Round**: `O(n² log n)` - each round re-sorts the whole list.
- **Max-Heap Simulation**: `O(n log n)` - heapify once, then `O(log n)` per
  smash.

### Space Complexity

- **Brute Force**: `O(1)` - the list is updated in place.
- **Sort Each Round**: `O(n)` - Timsort's scratch space.
- **Max-Heap Simulation**: `O(n)` - the negated copy of the weights.

### Trade-offs

- The brute force is the plainest transcription of the rules and uses no extra
  structures, but its repeated scans are the slowest of the three.
- Sort Each Round is the shortest to write and reads cleanly, yet it sorts
  stones that never moved, paying more than the heap for the same information.
- The Max-Heap Simulation pays a negation idiom and an `O(n)` copy up front and
  buys the best asymptotics and the fastest per-round repair.

### When to Use Each

- **Brute Force**: The first pass in an interview to lock in correctness on
  this problem's tiny constraints (`n <= 20`).
- **Sort Each Round**: A quick improvement when the input is already small and
  code brevity matters more than the last log factor.
- **Max-Heap Simulation** (recommended): The standard answer; it scales to
  large inputs and is the pattern to reach for whenever "repeatedly take the
  max" appears in a problem.

### Optimization Notes

- The negation trick is a two-way contract: values are stored negated, so every
  read pushes or pops through a unary minus. Missing one negation silently
  produces a min-heap of negatives.
- With `stones[i] <= 100`, a 101-slot counting array plus a scan from the top
  also finds each round's pair in `O(100)` per round without a heap; it wins
  only under this problem's artificially small weight bound.
- `heapq.heapify` builds the heap bottom-up in `O(n)`, beating the `O(n log n)`
  of pushing weights one at a time.
