# [Minimum Interval to Include Each Query](https://leetcode.com/problems/minimum-interval-to-include-each-query/)

**Medium** | **25 minutes** | **Array, Binary Search, Sweep Line, Sorting, Heap (Priority Queue)**

**Pattern:** [Heap / Priority Queue](../patterns/heap/intuition.md), [Interval](../patterns/interval/intuition.md)

**Algorithm:** [Heap (data structure)](https://en.wikipedia.org/wiki/Heap_(data_structure)) · [Sweep line algorithm](https://en.wikipedia.org/wiki/Sweep_line_algorithm) · [Sorting algorithm](https://en.wikipedia.org/wiki/Sorting_algorithm)

**Practice:** [`practice/minimum_interval_to_include_each_query/solution.py`](../../practice/minimum_interval_to_include_each_query/solution.py)

You are given a 2D integer array `intervals`, where `intervals[i] = [left_i, right_i]` represents the `ith` interval starting at `left_i` and ending at `right_i` **(inclusive)**.

You are also given an integer array of query points `queries`. The result of `query[j]` is the **length of the shortest interval** `i` such that `left_i <= queries[j] <= right_i`. If no such interval exists, the result of this query is `-1`.

Return an array `output` where `output[j]` is the result of `query[j]`.

Note: The length of an interval is calculated as `right_i - left_i + 1`.

## Examples

### Example 1

**Input:** `intervals = [[1,3],[2,3],[3,7],[6,6]], queries = [2,3,1,7,6,8]`

**Output:** `[2,2,3,5,1,-1]`

**Explanation:** - Query = 2: The interval `[2,3]` is the smallest one containing 2, it's length is 2.
- Query = 3: The interval `[2,3]` is the smallest one containing 3, it's length is 2.
- Query = 1: The interval `[1,3]` is the smallest one containing 1, it's length is 3.
- Query = 7: The interval `[3,7]` is the smallest one containing 7, it's length is 5.
- Query = 6: The interval `[6,6]` is the smallest one containing 6, it's length is 1.
- Query = 8: There is no interval containing 8.

## Constraints

- `1 <= intervals.length <= 100000`
- `1 <= queries.length <= 100000`
- `1 <= left_i <= right_i <= 10000000`
- `1 <= queries[j] <= 10000000`

## Deriving the Solution

Each query is an independent question, "which covering interval is shortest?", but answering every query from scratch re-finds the same coverings. The way out is to answer the queries in an order that lets work be shared: process them in point order, and between consecutive queries the set of covering intervals only grows (intervals beginning) or shrinks (intervals ending), which makes a priority structure maintainable incrementally. The solutions below are three stations on that road.

1. **Start literal.** For each query, scan every interval, collect the ones
   covering the point, and take the smallest by length. Correct, and each
   query costs the full interval list: see
   [Per-Query Scan](#per-query-scan).
2. **Sort queries, keep candidates.** Sort the intervals by left endpoint and
   the queries by point; sweep the queries, adding every interval that has
   begun, and keep the candidates in a list pruned of the ones that already
   ended. Correct, but each query may re-scan the whole candidate list: see
   [Sorted Queries with Candidate List](#sorted-queries-with-candidate-list).
3. **Heapify the candidates.** The smallest covering interval is a repeated
   minimum query over a changing set, which is a min-heap keyed by
   `(size, right)`: push new intervals, pop the ones whose right end has
   passed, and the root is the answer: see
   [Min-Heap Sweep](#min-heap-sweep).

## Solutions

### Per-Query Scan

#### Derivation

The most direct reading answers each query on its own: an interval covers the point when `left <= query <= right` (both ends inclusive), and among the coverers the problem wants the smallest `right - left + 1`:

1. For each `query`, walk every interval `[left, right]`.
2. Keep the intervals with `left <= query <= right`.
3. Among them, take the minimum `right - left + 1`.
4. Emit that size, or `-1` when no interval covers the query.

The queries are answered independently, so nothing about one query helps the next.

#### Walkthrough

Trace the scan on Example 1: `intervals = [[1,3],[2,3],[3,7],[6,6]]`, `queries = [2,3,1,7,6,8]`. Each row lists the covering intervals and the winner:

```text
query 2  covering [1,3] (size 3), [2,3] (size 2)                  -> min 2
query 3  covering [1,3] (3), [2,3] (2), [3,7] (5)                 -> min 2
query 1  covering [1,3] (3)                                       -> min 3
query 7  covering [3,7] (5)                                       -> min 5
query 6  covering [3,7] (5), [6,6] (1)                            -> min 1
query 8  covering nothing                                         -> -1
```

The winners assemble into `[2, 2, 3, 5, 1, -1]`, matching the expected Output for Example 1. The inclusive bounds do real work at `query 3`: `[3,7]` covers it because its left endpoint equals the query.

#### Solution

The code is the walkthrough's per-query loop: filter by coverage, then minimize.

```python
from typing import List


class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        output: List[int] = []
        for query in queries:
            best = -1
            for left, right in intervals:
                if left <= query <= right:
                    size = right - left + 1
                    if best == -1 or size < best:
                        best = size
            output.append(best)
        return output
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * q)`

Each of the `q` queries scans all `n` intervals with constant work per interval.

##### Space Complexity: `O(1)`

Beyond the output list, one running best per query.

#### Key Insights

- Inclusive endpoints are the boundary trap: `left <= query <= right` must use two non-strict comparisons, or equal-to-endpoint queries silently lose their coverers.
- The scan is correct but pays full price for every query, even when consecutive queries share most of their covering sets.
- As the smallest correct version, it is the natural oracle for the sweep solutions on small inputs.

### Sorted Queries with Candidate List

#### Derivation

The per-query scan re-tests intervals that have not changed between queries. Sharing that work needs an order: process queries in point order, and maintain the set of intervals covering the current point incrementally. Sorting the intervals by `left` lets a pointer admit every interval that has begun; pruning the ones whose `right` has passed keeps the candidate set honest:

1. Sort `intervals` by `left`; sort the queries with their original indices.
2. Keep `candidates`, the intervals begun but not yet ended.
3. For each query in point order: first add every unstarted interval with
   `left <= query`, then drop every candidate with `right < query`.
4. The answer is the smallest `right - left + 1` among `candidates`, or `-1`
   if it is empty.
5. Write each answer back to its original position.

The order inside step 3 matters: add-then-prune matches the semantics of "covering at this exact point", since an interval that both begins and ends at the query must be added before it could be pruned.

#### Walkthrough

Trace the sweep on Example 1. The intervals sort by left to `[[1,3],[2,3],[3,7],[6,6]]` and the queries sort to points `1, 2, 3, 6, 7, 8`. Each row shows the query's candidates after its add-and-prune; expired intervals leave in the same row that exposes them:

```text
query 1  add [1,3]                      candidates [1,3]               -> answer 3
query 2  add [2,3]                      candidates [1,3], [2,3]        -> answer 2
query 3  add [3,7]                      candidates [1,3], [2,3], [3,7] -> answer 2
query 6  prune [1,3], [2,3] (3 < 6),
         add [6,6]                      candidates [3,7], [6,6]        -> answer 1
query 7  prune [6,6] (6 < 7)            candidates [3,7]               -> answer 5
query 8  prune [3,7] (7 < 8)            candidates empty               -> -1
```

The answers read `3, 2, 2, 1, 5, -1` in point order, and writing each back to its original query position assembles `[2, 2, 3, 5, 1, -1]`, matching the expected Output for Example 1. The prune rows show the bookkeeping the heap will absorb: by query 6, `[1,3]` and `[2,3]` had both expired and were swept, and query 7's only survivor `[3,7]` survives because its right endpoint equals the query.

#### Solution

The code is the sorted sweep with a linear candidate search.

```python
from typing import List


class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        sorted_intervals = sorted(intervals)
        indexed_queries = sorted((query, i) for i, query in enumerate(queries))

        output = [-1] * len(queries)
        ptr = 0
        candidates: List[List[int]] = []
        for query, original_index in indexed_queries:
            while ptr < len(sorted_intervals) and sorted_intervals[ptr][0] <= query:
                candidates.append(sorted_intervals[ptr])
                ptr += 1
            candidates = [
                [left, right]
                for left, right in candidates
                if right >= query
            ]
            if candidates:
                best = min(right - left + 1 for left, right in candidates)
                output[original_index] = best
        return output
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(q log q + n log n + q * c)`

Both sorts cost their logarithms, but each query scans the candidate list, which can hold `c = n` intervals; the quadratic worst case survives inside the sweep.

##### Space Complexity: `O(n + q)`

The candidate list holds begun intervals, and the indexed queries pair every query with its index.

#### Key Insights

- Sorting the queries is the unlock: answers computed out of order are trivially restored by carrying the original indices.
- Add-then-prune is the discipline that keeps "covering at this point" true; swapping the two steps would drop an interval that begins and ends exactly at the query.
- The structure is right and the data structure is wrong: the repeated `min` over a mutable set is exactly what a heap exists to do, which is the last step.

### Min-Heap Sweep

#### Derivation

The candidate list performs three operations per query: admit newly begun intervals, discard expired ones, and find the minimum size. The list does all three linearly; a min-heap keyed by `(size, right)` does the last two in logarithmic time and the first in amortized logarithmic time. Pushing `(size, right)` pairs lets the eviction test read the right endpoint straight off the root, so the heap entry is self-contained:

1. Sort `intervals` by `left`; sort queries with indices.
2. Keep `heap`, a min-heap of `(size, right)` pairs.
3. Per query in point order: push every interval with `left <= query`, pop
   while `heap[0][1] < query`.
4. The answer is `heap[0][0]`, or `-1` if the heap is empty.
5. Write the answer back to the original index.

#### Invariant

The heap holds every interval that has begun and not yet provably ended, and its root is the smallest-size candidate whose expiry is latest among the smallest:

$$ \text{heap} \supseteq \{\, (r - l + 1,\ r) : l \le q,\ r \ge q \,\} \setminus \text{evicted}, \quad \text{heap}[0] \text{ minimizes } (r - l + 1,\ r) $$

```text
heap = (size, right) pairs of all begun, not-yet-evicted intervals
heap[0] = the smallest size among them, ties broken by smallest right
```

Each phase preserves the query's semantics: the push phase guarantees every interval begun by the query is present (nothing begun is ever skipped, because the pointer only advances over admitted intervals); the pop phase removes only intervals with `right < query`, none of which cover the query, so any coverer that exists is still in the heap. At the root, then, the minimum size over covering intervals when the heap is read: the root's size is the answer, unless no coverers exist, in which case the heap empties and the answer is `-1`.

#### Walkthrough

Trace the heap through Example 1: intervals left-sorted as `[[1,3],[2,3],[3,7],[6,6]]`, queries point-sorted to `1, 2, 3, 6, 7, 8`. Heap contents are listed sorted for readability; the root is the pair with the smallest size:

```text
query 1  add [1,3] size 3                    heap = [(3,3)]                  answer 3
query 2  add [2,3] size 2                    heap = [(2,3), (3,3)]           answer 2
query 3  add [3,7] size 5                    heap = [(2,3), (3,3), (5,7)]    answer 2
query 6  add [6,6] size 1                    heap = [(1,6), (2,3), (3,3), (5,7)]  answer 1
query 7  evict size 1 right 6 < 7
         evict size 2 right 3 < 7
         evict size 3 right 3 < 7            heap = [(5,7)]                  answer 5
query 8  evict size 5 right 7 < 8            heap = []                       answer -1
```

Reading the answers in point order gives `3, 2, 2, 1, 5, -1`, and writing each back to its original query position assembles `[2, 2, 3, 5, 1, -1]`, matching the expected Output for Example 1. Query 7's triple eviction is the mechanism on display: every interval except `[3,7]` had ended by 7, and the heap surrendered them root-first, smallest size first.

#### Solution

The code is the sweep: pointer-fed pushes, root-fed evictions, and the root read as the answer.

```python
import heapq
from typing import List


class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        sorted_intervals = sorted(intervals)
        indexed_queries = sorted((query, i) for i, query in enumerate(queries))

        heap: List[tuple] = []
        output = [-1] * len(queries)
        ptr = 0
        for query, original_index in indexed_queries:
            while ptr < len(sorted_intervals) and sorted_intervals[ptr][0] <= query:
                left, right = sorted_intervals[ptr]
                heapq.heappush(heap, (right - left + 1, right))
                ptr += 1
            while heap and heap[0][1] < query:
                heapq.heappop(heap)
            if heap:
                output[original_index] = heap[0][0]
        return output
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n + q log q + (n + q) log n)`

Both sorts, then every interval is pushed once and popped at most once, each operation `O(log n)` against a heap bounded by `n`; the query loop adds one root peek each.

##### Space Complexity: `O(n + q)`

The heap holds at most `n` pairs, and the indexed queries hold one pair per query.

#### Key Insights

- The pointer never moves backwards, so every interval is pushed exactly once and popped at most once: the sweep's total heap work is bounded by `2n` operations, not per-query.
- Eviction is lazy but total: an interval is popped exactly when a query proves it expired, and it can never be needed afterwards because later queries are at larger points.
- The `(size, right)` key makes the heap entry self-contained: the answer reads off `heap[0][0]` and the eviction test reads off `heap[0][1]`, with no auxiliary maps.

## Comparison of Solutions

The practice harness's `practice/minimum_interval_to_include_each_query/reference.py` implements the **Min-Heap Sweep** solution.

### Time Complexity

- **Per-Query Scan**: `O(n * q)` - every query scans every interval.
- **Sorted Queries with Candidate List**: `O(q log q + n log n + q * c)` - the sweep is shared but each query scans the candidates.
- **Min-Heap Sweep**: `O(n log n + q log q + (n + q) log n)` - each interval is pushed and popped at most once.

### Space Complexity

- **Per-Query Scan**: `O(1)` - one running best per query.
- **Sorted Queries with Candidate List**: `O(n + q)` - candidates plus indexed queries.
- **Min-Heap Sweep**: `O(n + q)` - heap pairs plus indexed queries.

### Trade-offs

- The per-query scan is the definition transcribed and the natural oracle; at the constraint caps (`n, q <= 10^5`) its quadratic product is out of budget.
- The candidate list does the algorithmic heavy lifting (shared sweep, offline answers) but leaves a linear minimum search per query, so its worst case stays quadratic.
- The heap completes the design: same sweep, logarithmic minimum maintenance, and `O((n + q) log n)` overall, at the cost of tuple-keyed heap entries that are slightly harder to read.

### When to Use Each

- **Per-Query Scan**: as the correctness oracle on small inputs and the clarity baseline.
- **Sorted Queries with Candidate List**: as the derivation's middle station, or when candidate sets are provably tiny.
- **Min-Heap Sweep** (recommended): the answer at these constraints and the standard offline pattern for point queries over intervals.

### Optimization Notes

- Both sweep versions owe their shape to sorting the queries: offline processing with an index map is the standard trick whenever answers must land back in input order.
- The `right` in the `(size, right)` key is what lets the eviction test read the root directly: the heap entry carries its own expiry, so no auxiliary map from size to endpoints is needed.
- The eviction test is strict (`heap[0][1] < query`) because intervals are inclusive at both ends; using `<=` would wrongly discard an interval ending exactly at the query, the same boundary as `[3,7]` surviving query 7.
- The pointer-fed pushes and the root-fed evictions are each monotone in the query order, which is what makes one pass over both structures sufficient.
