# [Find K Pairs with Smallest Sums](https://www.fastprep.io/problems/amazon-k-smallest-pair-sums)

**Medium** | **NN minutes** | **Array, Heap, Sorting**

Given two integer arrays nums1 and nums2, both sorted in nondecreasing order, consider every index pair (i, j) and the pair [nums1[i], nums2[j]].

Return the k pairs with the smallest sums. Return them in nondecreasing order of their sums. Different index pairs are distinct, so duplicate value pairs may appear.

## Examples

### Example 1

**Input:** `nums1 = [1,7,11]`, `nums2 = [2,4,6]`, `k = 3`

**Output:** `[[1,2],[1,4],[1,6]]`

**Explanation:** The three smallest pair sums are 3, 5, and 7.

### Example 2

**Input:** `nums1 = [1,1,2]`, `nums2 = [1,2,3]`, `k = 2`

**Output:** `[[1,1],[1,1]]`

**Explanation:** The two occurrences use different indices in nums1.

## Constraints

- `1 <= nums1.length, nums2.length <= 100000.`
- `Both arrays are sorted in nondecreasing order.`
- `Every value is in [-10^9, 10^9].`
- `1 <= k <= nums1.length * nums2.length.`
- `Every pair sum fits in a signed 32-bit integer.`

## Deriving the Solution

Ordering first, before any code. The statement requires the `k` pairs in nondecreasing order of their sums, and it counts duplicate index pairs as distinct pairs, so `[1,1]` from two different `nums1` indices appears twice. Among pairs whose sums tie, the statement leaves the emitted order free; the convention pinned across this page freezes ascending `nums1` index, then ascending `nums2` index, the key `(sum, i, j)`, and every case and code path below follows it. Fix one row per `nums1` index, and each row is itself a sorted sequence: `nums1[i]` is constant while `nums2[j]` ascends, so pair sums rise along every row. The ladder stops rebuilding the grid:

1. **Start literal.** Build every index pair, sort them under the pinned key, and slice off `k`: correct, and it materializes all `n * m` pairs: see [Enumerate All Pairs and Sort](#enumerate-all-pairs-and-sort).
2. **Keep only the row heads.** The next pair any row can offer sits at its head, so `k` rounds of scanning the at most `min(n, k)` live heads pick the answer one pair at a time: see [Head Scan k-Way Merge](#head-scan-k-way-merge).
3. **Let a heap watch the heads.** The scan re-finds the same minimum every round; a min-heap over the row heads answers that repeated question in logarithmic time: see [Min-Heap Row Merge](#min-heap-row-merge).

## Solutions

### Enumerate All Pairs and Sort

#### Derivation

The statement's most literal reading: consider every index pair, order them by the pinned key, and keep the first `k`:

1. Build every pair `(nums1[i] + nums2[j], i, j)` for all `i` and `j`.
2. Sort the tuples ascending, which orders by sum, then by `i`, then by `j`, exactly the pinned convention.
3. Return the first `k` pairs as `[nums1[i], nums2[j]]`.

#### Walkthrough

Example 1 (`nums1 = [1,7,11]`, `nums2 = [2,4,6]`, `k = 3`), all nine tuples sorted:

```text
(3, 0, 0)   (5, 0, 1)   (7, 0, 2)   (9, 1, 0)   (11, 1, 1)
(13, 1, 2)  (13, 2, 0)  (15, 2, 1)  (17, 2, 2)
```

The first three tuples unfold to `[[1,2],[1,4],[1,6]]`, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        ranked = [
            (nums1[row] + nums2[column], row, column)
            for row in range(len(nums1))
            for column in range(len(nums2))
        ]
        ranked.sort()
        return [[nums1[row], nums2[column]] for _, row, column in ranked[:k]]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * m * log(n * m))`

`n * m` pairs built and sorted, with `n = len(nums1)` and `m = len(nums2)`.

##### Space Complexity: `O(n * m)`

Every pair is held at once, plus the output.

#### Key Insights

- The enumeration under the pinned key is the definition of the answer, which makes it the oracle every other approach is checked against.
- Sorting everything to keep the smallest `k` pays for pairs it will never emit; the waste is the ladder's next rung.
- Rows are already sorted, so a full sort re-orders information the input structure provides for free.

### Head Scan k-Way Merge

#### Derivation

Along any row, sums ascend, so once a row's head has been emitted, the row's next offer is the pair right behind it: each row behaves like one stream in a `k`-way merge. Only `min(n, k)` rows can ever contribute, because a row's head is its smallest pair and `k` winners cannot leave more than `k - 1` rows unstarted:

1. Seed one cursor per row for rows `0` through `min(n, k) - 1`, all at column `0`.
2. Repeat `k` times: scan the live cursors and take the smallest `(sum, row)` head, where ties on sum break on the smaller row, matching the pinned `(sum, i, j)` key because each candidate is the current head of its row.
3. Emit `[nums1[row], nums2[column]]`, advance that row's cursor, and retire the row when its columns run out.

#### Walkthrough

Example 1 (`nums1 = [1,7,11]`, `nums2 = [2,4,6]`, `k = 3`), the heads before each round:

```text
round 1   heads (3, row 0) (9, row 1) (13, row 2)   -> take (3, row 0)   emit [1, 2]
round 2   heads (5, row 0) (9, row 1) (13, row 2)   -> take (5, row 0)   emit [1, 4]
round 3   heads (7, row 0) (9, row 1) (13, row 2)   -> take (7, row 0)   emit [1, 6]
```

Three rounds emit `[[1,2],[1,4],[1,6]]`, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        live_rows = min(len(nums1), k)
        cursors = {row: 0 for row in range(live_rows)}
        smallest_pairs = []

        for _ in range(k):
            if not cursors:
                break
            best_row = min(cursors, key=lambda row: (nums1[row] + nums2[cursors[row]], row))
            smallest_pairs.append([nums1[best_row], nums2[cursors[best_row]]])
            cursors[best_row] += 1
            if cursors[best_row] == len(nums2):
                del cursors[best_row]

        return smallest_pairs
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(k * min(n, k))`

`k` rounds, each scanning at most `min(n, k)` live heads.

##### Space Complexity: `O(min(n, k))`

One cursor per live row, plus the output.

#### Key Insights

- The row-head observation does all the work: no emitted pair can be followed by a smaller one from its own row, so heads are the only candidates worth comparing.
- Ties break on the row index because equal-sum heads compare on `(sum, row)`; the column never decides here, since each row offers one head at a time.
- The scan is still linear work per emitted pair, and at `n, m <= 100000` that multiplies into the millions; the heap removes exactly that.

### Min-Heap Row Merge

#### Derivation

The scan's repeated question, which live head is smallest, is a minimum priority queue query, and a binary min-heap answers it in `O(log)` while advancing a cursor costs one push. Seeding is a `heapq.heapify` over the `min(n, k)` row heads, built as `(sum, row, column)` tuples so the pinned tie order falls out of tuple comparison:

1. Build `(nums1[row] + nums2[0], row, 0)` for rows `0` through `min(n, k) - 1` and `heapq.heapify` it.
2. Repeat `k` times: pop the smallest tuple, emit `[nums1[row], nums2[column]]`, and push `(sum + nums2[column + 1] - nums2[column], row, column + 1)` when the row has a next column.
3. Stop early if the heap empties, which happens exactly when every pair has been emitted.

#### Walkthrough

Example 1 (`nums1 = [1,7,11]`, `nums2 = [2,4,6]`, `k = 3`), the heap shown in sorted order for reading; the heap itself only guarantees the smallest at the root:

```text
seed            heap = [(3, 0, 0), (9, 1, 0), (13, 2, 0)]
pop (3, 0, 0)   emit [1, 2]   push (5, 0, 1)   heap = [(5, 0, 1), (9, 1, 0), (13, 2, 0)]
pop (5, 0, 1)   emit [1, 4]   push (7, 0, 2)   heap = [(7, 0, 2), (9, 1, 0), (13, 2, 0)]
pop (7, 0, 2)   emit [1, 6]   column 3 is past the row: no push
```

Three pops emit `[[1,2],[1,4],[1,6]]`, matching the expected Output.

#### Solution

```python
import heapq
from typing import List


class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        live_rows = min(len(nums1), k)
        row_heads = [(nums1[row] + nums2[0], row, 0) for row in range(live_rows)]
        heapq.heapify(row_heads)

        smallest_pairs = []
        while len(smallest_pairs) < k and row_heads:
            _, row, column = heapq.heappop(row_heads)
            smallest_pairs.append([nums1[row], nums2[column]])
            next_column = column + 1
            if next_column < len(nums2):
                heapq.heappush(
                    row_heads, (nums1[row] + nums2[next_column], row, next_column)
                )
        return smallest_pairs
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(k * log(min(n, k)))`

The heap holds at most `min(n, k)` tuples, and each of the `k` emissions pops once and pushes at most once; seeding is linear by `heapify`.

##### Space Complexity: `O(min(n, k))`

The heap, plus the output.

#### Key Insights

- Seeding only `min(n, k)` rows is the quiet optimization: row `r`'s head can only matter after `r` pairs have been emitted, so rows beyond `k - 1` never surface.
- The tuple `(sum, row, column)` is the pinned tie rule in data form: Python compares tuples lexicographically, so equal sums pop in ascending `(row, column)` order with no extra code.
- `while len(smallest_pairs) < k and row_heads` guards both ends: `k` can exceed the number of distinct pairs only when duplicates fill the gap, and the heap empties exactly when every pair has been emitted.

## Comparison of Solutions

### Time Complexity

- **Enumerate All Pairs and Sort**: `O(n * m * log(n * m))` - everything built, everything sorted.
- **Head Scan k-Way Merge**: `O(k * min(n, k))` - one full head scan per emitted pair.
- **Min-Heap Row Merge**: `O(k * log(min(n, k)))` - one logarithmic pop and push per emitted pair.

### Space Complexity

- **Enumerate All Pairs and Sort**: `O(n * m)` - the full pair grid materialized.
- **Head Scan k-Way Merge**: `O(min(n, k))` - one cursor per live row.
- **Min-Heap Row Merge**: `O(min(n, k))` - one heap tuple per live row.

### Trade-offs

- **Enumerate All Pairs and Sort**: the definition, usable as the oracle; `100000 * 100000` pairs rule it out at the statement's bounds.
- **Head Scan k-Way Merge**: no library and no heap invariant to trust, at a per-pair cost that grows with the row count.
- **Min-Heap Row Merge**: the same merge with the scan replaced by a log-time query; the statement's `k <= n * m` bound makes `k` the term that matters once `n, m` are large.

### When to Use Each

- **Enumerate All Pairs and Sort**: for tiny inputs, and always as the independent checker for the other two.
- **Head Scan k-Way Merge**: when asked to solve it without a heap; the structure it exposes is the one the heap exploits.
- **Min-Heap Row Merge (Recommended)**: the interview default on this statement: `k` logarithmic steps over a heap bounded by `min(n, k)`, with the tie rule carried by tuple comparison.

### Optimization Notes

- **Min-Heap Row Merge** is the recommended choice: at the statement's bounds (`n, m <= 100000`) the grid can hold `10^10` pairs, while the heap never exceeds `min(n, k)` tuples.
- Every pair sum fits a signed 32-bit integer by the statement's guarantee; Python needs no care here, but in fixed-width languages the sum `nums1[row] + nums2[column]` is the overflow surface to check, at extreme values like `-10^9 + (-10^9) = -2 * 10^9`.
- Equal value pairs from different indices are distinct by the statement, so no dedup pass is wanted anywhere in the pipeline.
- The pinned tie order is a convention, not a statement requirement: a judge accepting any nondecreasing-sum sequence would accept the column-major tie too, which is why the gauntlet freezes the convention on both sides instead of trusting one implementation.
