# [Minimum Stick Connection Cost](https://www.fastprep.io/problems/amazon-minimum-stick-connection-cost)

**unknown difficulty** | **NN minutes** | **unknown categories**

You are given an integer array sticks, where each element is the length of a stick.

You may connect any two sticks with lengths x and y. The new stick has length x + y, and the cost of this operation is also x + y.

Return the minimum total cost required to connect all sticks into one stick.

## Examples

### Example 1

**Input:** `sticks = [2, 4, 3]`

**Output:** `14`

**Explanation:** Connect 2 and 3 for cost 5, then connect 5 and 4 for cost 9. The total cost is 14.

### Example 2

**Input:** `sticks = [1, 8, 3, 5]`

**Output:** `30`

**Explanation:** One optimal sequence is 1 + 3 = 4, then 4 + 5 = 9, then 8 + 9 = 17, for total cost 4 + 9 + 17 = 30.

## Constraints

- `1 <= sticks.length <= 10^4`
- `1 <= sticks[i] <= 10^4`

## Solutions

### Repeated Scan for the Two Shortest Sticks

#### Derivation

The most literal reading of the cost rule gives the plan: keep merging until one stick remains, and at every step merge the two cheapest sticks available, because a stick merged now pays its length again in every later merge, so short sticks should be merged early and long sticks late (the same exchange argument that orders [Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding)). A first version can simply re-examine the whole list every round, pick out the two smallest lengths, and put their sum back:

1. Copy `sticks` into `lengths` so the merge can append to it.
2. While `lengths` holds more than one stick, find `shortest` and
   `second_shortest` with two `min` scans and remove both with `remove`.
3. Add `combined_length = shortest + second_shortest` to `total_cost` and append
   `combined_length` to `lengths`.
4. When one stick remains, return `total_cost`.

Every round pays two `min` scans and two `remove` scans over `lengths`, and there are `n - 1` rounds, so the total work is quadratic in the number of sticks.

#### Walkthrough

Example 1, `sticks = [2, 4, 3]`:

```text
start       lengths = [2, 4, 3]                    total_cost = 0
merge 1     shortest = 2, second_shortest = 3
            remove both, combined_length = 5       total_cost = 5
            lengths = [4, 5]
merge 2     shortest = 4, second_shortest = 5
            remove both, combined_length = 9       total_cost = 14
            lengths = [9]
one stick   return 14
```

The scan finds the same merge order the Explanation describes (5 first, then 9), and `total_cost` ends at `14`, matching the expected Output.

#### Solution

The code is the walkthrough's loop: scan out the two smallest lengths, merge them, put the sum back.

```python
from typing import List


class Solution:
    def solve(self, sticks: List[int]) -> int:
        lengths = list(sticks)
        total_cost = 0

        while len(lengths) > 1:
            shortest = min(lengths)
            lengths.remove(shortest)
            second_shortest = min(lengths)
            lengths.remove(second_shortest)
            combined_length = shortest + second_shortest
            total_cost += combined_length
            lengths.append(combined_length)

        return total_cost
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n - 1` merges runs two `min` scans and two `remove` scans, each linear in the current list length.

##### Space Complexity: `O(n)`

`lengths` holds a copy of the input and nothing else grows with it.

#### Key Insights

- The greedy rule (always merge the two cheapest) is what makes the answer minimal; this version only pairs it with the slowest possible bookkeeping.
- Each merge appends one length and removes two, so the list shrinks by exactly one per round, giving `n - 1` rounds.
- With `sticks.length` up to `10^4`, the roughly `10^8` scan steps are too slow in Python, which is what motivates a structure that finds the minimums without rescanning.

### Min-Heap

#### Derivation

The scan version repeats one expensive question every round: which two lengths are smallest now? A [binary min-heap](https://en.wikipedia.org/wiki/Binary_heap) answers it in logarithmic time: after one `heapify`, the shortest stick sits at the root, the next shortest is at one of its two children, and pushing the merged sum back re-sinks it in `O(log n)`:

1. Copy `sticks` into a list and `heapify` it into `heap`, so `heap[0]` is the
   shortest stick.
2. While `heap` holds more than one stick, call `heappop` twice to read
   `shortest` and `second_shortest`.
3. Add `combined_length = shortest + second_shortest` to `total_cost` and
   `heappush` `combined_length` back onto `heap`.
4. When one stick remains, return `total_cost`.

#### Walkthrough

Example 2, `sticks = [1, 8, 3, 5]`, shown by the set of lengths the heap holds; each pop yields the smallest member:

```text
heapify       heap = {1, 3, 5, 8}      total_cost = 0
merge 1       pop 1, pop 3, push 4     total_cost = 4     heap = {4, 5, 8}
merge 2       pop 4, pop 5, push 9     total_cost = 13    heap = {8, 9}
merge 3       pop 8, pop 9, push 17    total_cost = 30    heap = {17}
one stick     return 30
```

The merged sums `4`, `9`, `17` reproduce the Explanation's optimal sequence exactly, and `total_cost` ends at `30`, matching the expected Output.

#### Solution

The code is the walkthrough's pop-pop-push loop wrapped around `heapify`.

```python
import heapq
from typing import List


class Solution:
    def solve(self, sticks: List[int]) -> int:
        heap = list(sticks)
        heapq.heapify(heap)
        total_cost = 0

        while len(heap) > 1:
            shortest = heapq.heappop(heap)
            second_shortest = heapq.heappop(heap)
            combined_length = shortest + second_shortest
            total_cost += combined_length
            heapq.heappush(heap, combined_length)

        return total_cost
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

`heapify` is linear, and each of the `n - 1` merges performs two pops and one push, each `O(log n)`.

##### Space Complexity: `O(n)`

The heap is a copy of the input; the loop itself allocates nothing that grows.

#### Key Insights

- The heap keeps the two smallest lengths reachable at the root at all times, so no round ever rescans the list.
- Merged sums re-enter the heap, so a newly created long stick competes correctly against untouched short originals.
- `heapify` builds the heap in `O(n)`, cheaper than `n` individual pushes; the asymptotic total is still `O(n log n)` because of the merges.

### Two Queues

#### Derivation

The heap pays `O(log n)` per merge to keep the lengths fully ordered, but the merges obey a discipline that makes a total order unnecessary: once the original sticks are sorted, every merged sum is at least as large as the two lengths that formed it, so the merged sums are produced in nondecreasing order too. Two [FIFO queues](https://en.wikipedia.org/wiki/Queue_(abstract_data_type)) exploit that, the same trick Huffman merging uses: one queue holds the sorted original sticks, one holds the merged sums in creation order, and the next shortest stick is always the front of whichever queue holds the smaller head:

1. Sort `sticks` once into `queue_sorted` and start `queue_merged` empty.
2. `pop_shortest` returns the front of `queue_merged` when `queue_merged` is
   non-empty and its head is no larger than the head of `queue_sorted` (or when
   `queue_sorted` is empty), and the front of `queue_sorted` otherwise.
3. While the two queues together hold more than one stick, call `pop_shortest`
   twice, add the sum to `total_cost`, and append the sum to `queue_merged`.
4. Return `total_cost`.

#### Walkthrough

Example 1, `sticks = [2, 4, 3]`:

```text
sort        queue_sorted = [2, 3, 4]   queue_merged = []     total_cost = 0
merge 1     pop_shortest -> 2 (sorted), pop_shortest -> 3 (sorted)
            combined_length = 5, append to merged   total_cost = 5
            queue_sorted = [4], queue_merged = [5]
merge 2     pop_shortest -> 4 (sorted head 4 < merged head 5)
            pop_shortest -> 5 (queue_sorted now empty)
            combined_length = 9, append to merged   total_cost = 14
            queue_sorted = [], queue_merged = [9]
one stick   return 14
```

The second merge reads one stick from each queue, which is the moment the trick earns its keep: the merged sum `5` and the leftover original `4` are both visible as queue heads without any re-sorting. `total_cost` ends at `14`, matching the expected Output.

#### Solution

The code is the walkthrough's two fronts: `pop_shortest` compares heads, and the loop merges whatever it returns.

```python
from collections import deque
from typing import Deque, List


class Solution:
    def solve(self, sticks: List[int]) -> int:
        queue_sorted: Deque[int] = deque(sorted(sticks))
        queue_merged: Deque[int] = deque()
        total_cost = 0

        def pop_shortest() -> int:
            merged_is_shorter = bool(queue_merged) and (
                not queue_sorted or queue_merged[0] <= queue_sorted[0]
            )
            if merged_is_shorter:
                return queue_merged.popleft()
            return queue_sorted.popleft()

        while len(queue_sorted) + len(queue_merged) > 1:
            first_shortest = pop_shortest()
            second_shortest = pop_shortest()
            combined_length = first_shortest + second_shortest
            total_cost += combined_length
            queue_merged.append(combined_length)

        return total_cost
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

The single sort dominates; each of the `n - 1` merges afterwards performs only constant-time queue operations.

##### Space Complexity: `O(n)`

The two queues together hold every original stick and every merged sum not yet re-merged, at most `2n - 1` lengths.

#### Key Insights

- Merged sums are created in nondecreasing order, which is exactly the property that lets plain queues replace the heap: new sums always land at the back of `queue_merged`.
- One concept keeps one name here: `queue_sorted` never changes except by popping, and `queue_merged` only ever appends, so the fronts are always the merge candidates.
- The advantage over the heap is a constant factor, not an asymptotic one: the initial sort already costs `O(n log n)`.

## Comparison of Solutions

### Time Complexity

- **Repeated Scan for the Two Shortest Sticks**: `O(n^2)` - every merge rescans the shrinking list twice for the minimums and twice more to remove them.
- **Min-Heap**: `O(n log n)` - linear `heapify` plus `O(log n)` per pop and push across `n - 1` merges.
- **Two Queues**: `O(n log n)` - one sort up front, then constant-time queue operations per merge.

### Space Complexity

- **Repeated Scan for the Two Shortest Sticks**: `O(n)` - the `lengths` copy of the input.
- **Min-Heap**: `O(n)` - the heap copy of the input.
- **Two Queues**: `O(n)` - both queues together hold at most `2n - 1` lengths (originals plus unmerged sums).

### Trade-offs

- **Repeated Scan for the Two Shortest Sticks**: zero imports and the shortest code, but the quadratic scan count breaks down at the stated constraint sizes.
- **Min-Heap**: the standard answer; a log factor per merge buys simplicity and provable correctness with no ordering argument to make.
- **Two Queues**: the fastest merges in practice, but it depends on the nondecreasing-sums argument, which is easy to state and easy to get wrong without proof.

### When to Use Each

- **Repeated Scan for the Two Shortest Sticks**: as a warm-up or when `n` is tiny and clarity matters more than speed.
- **Min-Heap (Recommended)**: the default interview answer: near-optimal, short, and requires no argument beyond the greedy exchange.
- **Two Queues**: when the interviewer pushes past the heap, asks for constant-time merges, or connects the problem to Huffman merging.

### Optimization Notes

- The cost identity underneath every approach: each original stick contributes its length once per merge it survives, so total cost is minimal when short sticks survive the fewest merges.
- `heapify` beats pushing `n` times (`O(n)` versus `O(n log n)`) and matters at `n = 10^4`, though the merge loop dominates either way.
- A common pitfall is sorting descending by mistake or merging the two longest sticks; both silently produce a valid total that is not minimal.
