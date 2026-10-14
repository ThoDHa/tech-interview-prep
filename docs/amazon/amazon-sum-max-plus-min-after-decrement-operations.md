# [Sum Max Plus Min After Decrement Operations](https://www.fastprep.io/problems/amazon-sum-max-plus-min-after-decrement-operations)

**Medium** | **NN minutes** | **Heap, Greedy**

You are given an integer array arr and an integer requests.

Repeat the following operation exactly requests times:

Find the current maximum value and the current minimum value in arr.Add their sum to the answer.Choose one occurrence of the maximum value and decrease it by 1.Return the final accumulated answer.

Function Description Complete the function sumMaxPlusMinAfterOperations in the editor below.

sumMaxPlusMinAfterOperations has the following parameters:

int[] arr: the initial valuesint requests: the number of operationsReturns long: the accumulated sum

## Examples

### Example 1

**Input:** `arr = [1, 2]`, `requests = 2`

**Output:** `5`

**Explanation:** First add 1 + 2 = 3 and decrement the 2 to 1. Then add 1 + 1 = 2. The total is 5.

### Example 2

**Input:** `arr = [3, 3, 3]`, `requests = 1`

**Output:** `6`

**Explanation:** The current maximum and minimum are both 3, so the answer increases by 6.

## Constraints

- `1 <= arr.length <= 105`
- `1 <= arr[i] <= 109`
- `0 <= requests <= 109`
- `Each operation decreases one occurrence of the current maximum value by exactly 1.`
- `Use a wide enough integer type (e.g., long) for the accumulated total.`

## Solutions

### Simulate Every Request

#### Derivation

The operation is fully specified: read the current maximum and minimum, add their sum, then decrement one occurrence of the maximum. The baseline maintains a plain list and rescans for both extremes every request:

1. Per request, find the maximum and minimum by scanning.
2. Add their sum; decrement the maximum in place.
3. Repeat exactly `requests` times.

#### Walkthrough

Example 1, `arr = [1, 2]`, `requests = 2`: the first request reads max 2 and min 1, adds 3, and decrements the 2 to 1; the second reads 1 and 1, adds 2. The total is 5. Example 2, `[3, 3, 3]`, one request adds `3 + 3 = 6`.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, arr: List[int], requests: int) -> int:
        """Return the accumulated max-plus-min sum after all requests.

        Time:  O(requests * n): two full scans per request.
        Space: O(n).
        """
        values = list(arr)
        total = 0
        for _ in range(requests):
            total += max(values) + min(values)
            values[values.index(max(values))] -= 1
        return total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(requests * n)`

At the constraint ceiling (`10^9` requests), hopeless; the rung is the definition and the oracle.

##### Space Complexity: `O(n)`

One copy of the array.

#### Key Insights

- The minimum never changes: every decrement lowers a maximum toward but never below the current minimum floor until they meet.
- Repeated maxima collapse into counts: how many values sit at each level.

### Two Heaps With Level Counts

#### Derivation

Track the frontier values with a max-heap and a min-heap over the same multiset. Each request pops the maximum (paying the sum with the current minimum read off the min-heap), then reinserts `maximum - 1`. Stale min-heap entries never lie about the minimum (values only decrease, so a stale larger entry is simply never the minimum once a smaller one exists). The heaps answer both extremes in `O(log n)` per request. Beyond the heaps, a closed form exists for long runs: while the maximum and minimum differ, each request lowers the maximum by 1, so the sum declines linearly until the two meet; after they meet, every request pays `2 * minimum` and decrements a value that immediately returns to the pool, so the tail is a constant. The heap rung below stays mechanical; the closed form is left as the optimization note's derivation.

1. Maintain both heaps over the live multiset.
2. Per request: `total += max + min`; replace the max with `max - 1`.
3. Stop after `requests` iterations.

#### Walkthrough

Example 1, `[1, 2]`, 2 requests: the heaps hold `{1, 2}`. Request 1: max 2, min 1, total 3; the multiset becomes `{1, 1}`. Request 2: max 1, min 1, total 5. Example 2, `[3, 3, 3]`, 1 request: max 3, min 3, total 6.

#### Solution

```python
import heapq
from typing import List


class Solution:
    def solve(self, arr: List[int], requests: int) -> int:
        """Return the accumulated max-plus-min sum after all requests.

        Time:  O((n + requests) * log n): heap setup plus one
            push-pop cycle per request.
        Space: O(n).
        """
        low_heap = list(arr)
        high_heap = [-value for value in arr]
        heapq.heapify(low_heap)
        heapq.heapify(high_heap)
        total = 0
        for _ in range(requests):
            maximum = -high_heap[0]
            minimum = low_heap[0]
            total += maximum + minimum
            heapq.heapreplace(high_heap, -(maximum - 1))
            heapq.heappush(low_heap, maximum - 1)
        return total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((n + requests) * log n)`

Linear setup, logarithmic work per request; at `requests = 10^9` the closed form in the optimization notes takes over.

##### Space Complexity: `O(n + requests)` in the worst case

The min-heap accumulates one entry per decrement; the max-heap stays size `n`. (An indexable multiset removes the growth; see the notes.)

#### Key Insights

- The maximum frontier moves only downward, so `heapreplace` on the max side never invalidates anything.
- The minimum is nondecreasing only until the maxes sink to it; from then on both extremes read the same level.
- The accumulated total needs a 64-bit accumulator at these constraints.

## Comparison of Solutions

### Time Complexity

- **Simulate Every Request**: `O(requests * n)` - the definition.
- **Two Heaps With Level Counts**: `O((n + requests) * log n)`.

### Space Complexity

- **Simulate Every Request**: `O(n)`.
- **Two Heaps With Level Counts**: up to `O(n + requests)` without a multiset prune.

### Trade-offs

- The rescan needs no data structure and no invariant argument.
- The heaps pay with bookkeeping but answer each request logarithmically.

### When to Use Each

- **Simulate Every Request**: small arrays, small request counts, and as the test oracle.
- **Two Heaps With Level Counts**: the practical rung for moderate request counts.

### Optimization Notes

- Closed form: let `minimum` be the array minimum. While any value exceeds `minimum`, the max declines by exactly 1 per request and the sum per request is `current_max + minimum`; summing that run is an arithmetic series. Once all values equal `minimum`, each remaining request contributes `2 * minimum` exactly. Splitting `requests` at the meeting point answers `10^9` requests in constant time after an `O(n log n)` sort.
- A `Counter` over levels (value to count) replaces both heaps: the max is the largest occupied level, and decrementing either empties the level or drops its count, moving to the level below.
