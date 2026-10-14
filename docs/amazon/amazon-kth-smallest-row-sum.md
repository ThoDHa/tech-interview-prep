# [Kth Smallest Sum from Sorted Matrix Rows](https://www.fastprep.io/problems/amazon-kth-smallest-row-sum)

**Hard** | **NN minutes** | **Array, Matrix, Heap**

Given an integer matrix mat whose rows are sorted in nondecreasing order, choose exactly one value from each row and add the chosen values.

Return the kth smallest obtainable sum. Distinct choices occupy distinct ranks even when they produce equal sums.

## Examples

### Example 1

**Input:** `mat = [[1,3,11],[2,4,6]]`, `k = 5`

**Output:** `7`

**Explanation:** The ordered sums begin 3, 5, 5, 7, 7, so the fifth sum is 7.

### Example 2

**Input:** `mat = [[1,3,11],[2,4,6]]`, `k = 9`

**Output:** `17`

**Explanation:** There are nine selections, and the largest and ninth ordered sum is 11 + 6 = 17.

### Example 3

**Input:** `mat = [[1,10,10],[1,4,5],[2,3,6]]`, `k = 7`

**Output:** `9`

**Explanation:** Counting equal sums from different selections separately, the seventh ordered sum is 9.

## Constraints

- `1 <= mat.length, mat[i].length <= 40.`
- `All rows have the same length and are sorted in nondecreasing order.`
- `1 <= mat[i][j] <= 5000.`
- `1 <= k <= min(200, mat[i].length^mat.length).`

## Solutions

### Brute Force Full Expansion

#### Derivation

The most literal reading of "choose exactly one value from each row" is to enumerate every selection, compute its sum, and sort. The number of selections is the product `P` of the row lengths (nine for Example 1: three values from the first row times three from the second), and the constraints keep `P` modest because `k <= 200` only ever asks about the smallest selections. Building the sums row by row keeps the bookkeeping simple: every partial sum of the first `row_count` rows is a partial sum from the first `row_count - 1` rows plus one value of the current row:

1. Start `totals = [0]`, the single empty selection.
2. For each `row`, build `expanded = [partial_sum + value for partial_sum in totals
   for value in row]` and replace `totals` with it.
3. Sort `totals` ascending. Distinct selections occupy distinct slots even when
   their sums are equal, so plain sorting gives every selection its rank.
4. Return `totals[k - 1]`.

#### Walkthrough

Example 1, `mat = [[1,3,11],[2,4,6]]`, `k = 5`:

```text
totals = [0]
row [1, 3, 11]:  expanded = [0+1, 0+3, 0+11]
                 = [1, 3, 11]
row [2, 4, 6]:   expanded = [1+2, 1+4, 1+6, 3+2, 3+4, 3+6, 11+2, 11+4, 11+6]
                 = [3, 5, 7, 5, 7, 9, 13, 15, 17]
sorted:          [3, 5, 5, 7, 7, 9, 13, 15, 17]
```

The sorted list begins `3, 5, 5, 7, 7`, exactly the ordering the example's Explanation quotes, so `totals[5 - 1] = 7` matches the expected Output. The list also holds nine entries, so Example 2's `k = 9` reads the last element `17`, again matching.

#### Solution

The code is the walkthrough's row-by-row expansion and final sort:

```python
from typing import List


class Solution:
    def solve(self, mat: List[List[int]], k: int) -> int:
        """Return the kth smallest sum obtainable by picking one value per row.

        Time:  O(P log P) for sorting P = product of row lengths, plus O(P)
            for the expansion passes that build every selection's sum.
        Space: O(P) for the list of all selection sums.
        """
        totals = [0]
        for row in mat:
            expanded = []
            for partial_sum in totals:
                for value in row:
                    expanded.append(partial_sum + value)
            totals = expanded

        totals.sort()
        return totals[k - 1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(P log P)`

Every one of the `P = mat[i].length^mat.length` selections is built with one addition and the final list is sorted.

##### Space Complexity: `O(P)`

The expansion holds every selection sum of the rows processed so far.

#### Key Insights

- Each pass over a row multiplies the list length by the row length, so the expansion mirrors the definition of `P` directly.
- Sorting keeps equal sums as separate entries, which is exactly the problem's ranking rule: distinct selections occupy distinct ranks.
- The approach is correct but pays for all `P` sums when only the smallest `k <= 200` are ever read.

### Truncation by Prefix

#### Derivation

The brute force sorts `P` sums but only rank `k` is read. The observation that prunes this: if a partial sum cannot make the smallest `k` totals after some prefix of rows, no selection built on it can appear among the smallest `k` full sums, because every remaining row adds values of at least `1`. So after each row it is enough to keep the `k` smallest partial sums and discard the rest; the full expansion is never materialized:

1. Start `smallest = [0]`.
2. For each `row`, sort every `partial_sum + value` candidate and keep the first
   `k` entries in `smallest`.
3. After the last row, `smallest` holds the `k` smallest full sums in order.
4. Return `smallest[k - 1]`.

#### Walkthrough

Example 3, `mat = [[1,10,10],[1,4,5],[2,3,6]]`, `k = 7`:

```text
row [1, 10, 10]:  candidates sorted = [1, 10, 10]
kept = [1, 10, 10]                      (fewer than k, keep all)
row [1, 4, 5]:    candidates sorted = [2, 5, 6, 11, 11, 14, 14, 15, 15]
kept = [2, 5, 6, 11, 11, 14, 14]        (15, 15 dropped)
row [2, 3, 6]:    candidates sorted = [4, 5, 7, 8, 8, 8, 9, ...]
kept = [4, 5, 7, 8, 8, 8, 9]
```

`smallest[7 - 1] = 9` matches the expected Output. The decisive beat is the second truncation: the dropped `15` entries can only grow, so none of them could have entered the smallest seven full sums, and the final kept list still begins with the true global seven.

#### Solution

The code is the walkthrough's build-sort-keep loop:

```python
from typing import List


class Solution:
    def solve(self, mat: List[List[int]], k: int) -> int:
        """Return the kth smallest sum obtainable by picking one value per row.

        Time:  O(m × n × k × log(k × n)) for sorting at most k × n candidates
            after each of the m rows of length n.
        Space: O(k × n) for the candidate list during one row; O(k) retained
            between rows.
        """
        smallest = [0]
        for row in mat:
            candidates = []
            for partial_sum in smallest:
                for value in row:
                    candidates.append(partial_sum + value)
            candidates.sort()
            smallest = candidates[:k]

        return smallest[k - 1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n × k × log(k × n))`

Each of the `m` rows builds at most `k × n` candidates from the kept list and sorts them; the kept list never exceeds `k` entries.

##### Space Complexity: `O(k × n)`

The candidate list holds at most `k × n` sums while one row is merged; the state retained between rows is the `O(k)` kept list.

#### Key Insights

- Monotone growth of sums (row values are at least `1`) makes truncation safe: a discarded partial sum can never re-enter the smallest `k` later.
- The kept list size is `min(k, selections so far)`, so the last row always contains rank `k` whenever `k` is attainable, which the constraints guarantee.
- This is the standard first upgrade over brute force in an interview: same correctness, retained memory bounded by the answer size instead of the input product.

### Heap Pair Merge

#### Derivation

Truncation still sorts every kept-times-row-length candidate. The repair treats each row merge as the classic "k smallest sums of two sorted lists" problem: `smallest` is sorted ascending and `row` is sorted ascending, so their pair sums form a sorted-by-row matrix and the smallest entries can be peeled off with a min-heap instead of materializing and sorting the full candidate set. Two growth rules generate exactly the pairs in order: from a popped pair `(partial_idx, col_idx)`, the next partial of the same column `(partial_idx + 1, col_idx)` is a successor, and, only from the first partial `(0, col_idx)`, the next column `(0, col_idx + 1)` is a successor. The first-partial-only rule prevents the same pair from being seeded twice:

1. Start `smallest = [0]`.
2. For each `row`, seed a `heap` with `(smallest[0] + row[0], 0, 0)` and pop
   `min(k, len(smallest) * len(row))` times, appending each popped `pair_sum`
   to `merged`.
3. After each pop, push `(smallest[partial_idx + 1] + row[col_idx],
   partial_idx + 1, col_idx)` when that partial exists, and push
   `(smallest[0] + row[col_idx + 1], 0, col_idx + 1)` when the pop came from
   the first partial and that column exists.
4. Replace `smallest` with `merged`; after the last row return `smallest[k - 1]`.

#### Walkthrough

Example 1, `mat = [[1,3,11],[2,4,6]]`, `k = 5`. The first row merges `[0]` with `[1,3,11]` and leaves `smallest = [1, 3, 11]`. The final row merges that with `[2, 4, 6]`, popping five pairs (each line shows the pushes after the pop):

```text
pop 3  from (0,0)  merged [3]       push (3+2, (1,0)), (1+4, (0,1))
pop 5  from (0,1)  merged [3,5]     push (3+4, (1,1)), (1+6, (0,2))
pop 5  from (1,0)  merged [3,5,5]   push (11+2, (2,0))
pop 7  from (0,2)  merged [3,5,5,7] push (3+6, (1,2))
pop 7  from (1,1)  merged [3,5,5,7,7]
```

`smallest = [3, 5, 5, 7, 7]` and rank five reads `7`, matching the expected Output. The equal `5` and `7` pops are the ranking rule in action: they come from different partials (selections `1+4` and `3+2`, `1+6` and `3+4`), so they occupy separate ranks. For Example 3 the same merge keeps `smallest = [2, 5, 6, 11, 11, 14, 14]` after the second row and `[4, 5, 7, 8, 8, 8, 9]` after the third, whose seventh entry is `9`.

#### Solution

The code is the walkthrough's seeded heap, pop-push loop, and per-row replacement of `smallest`:

```python
import heapq
from typing import List


class Solution:
    def solve(self, mat: List[List[int]], k: int) -> int:
        """Return the kth smallest sum obtainable by picking one value per row.

        Time:  O(m × k × log k): each of the m rows pops at most k pairs from
            a heap that never holds more than 2k entries.
        Space: O(k) for the merged list and the heap.
        """
        smallest = [0]
        for row in mat:
            heap = [(smallest[0] + row[0], 0, 0)]
            merged = []
            for _ in range(min(k, len(smallest) * len(row))):
                pair_sum, partial_idx, col_idx = heapq.heappop(heap)
                merged.append(pair_sum)
                if partial_idx + 1 < len(smallest):
                    heapq.heappush(heap, (smallest[partial_idx + 1] + row[col_idx],
                                          partial_idx + 1, col_idx))
                if partial_idx == 0 and col_idx + 1 < len(row):
                    heapq.heappush(heap, (smallest[0] + row[col_idx + 1],
                                          0, col_idx + 1))
            smallest = merged

        return smallest[k - 1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × k × log k)`

Each of the `m` rows pops at most `min(k, len(smallest) × len(row))` pairs; every pop and its at most two pushes cost `O(log k)` on a heap capped at `2k` entries.

##### Space Complexity: `O(k)`

The heap holds at most two entries per already-popped rank and `merged` holds at most `k` sums.

#### Key Insights

- Merging against one sorted row at a time turns the whole matrix into a chain of two-list merges, each solved by the classic seeded-heap technique.
- Seeding column successors only from the first partial (`partial_idx == 0`) is what keeps every pair discoverable exactly once; the partial successor rule covers downward movement.
- The heap peels only the pairs the answer can use, so the row length never multiplies into the sort the way it does in truncation.

### One-Liner with itertools.product

#### Derivation

After the brute force's expansion exists, the enumeration itself is exactly what [itertools.product](https://docs.python.org/3/library/itertools.html#itertools.product) expresses: one selection per row, every combination, in library form. The algorithm is the brute force verbatim; the row loop collapses into one generator over the product:

1. Enumerate `itertools.product(*mat)`, yielding every selection tuple.
2. Sum each selection in a generator, sort, and take index `k - 1`.

#### Walkthrough

Example 1, `mat = [[1,3,11],[2,4,6]]`, `k = 5`: the product yields the nine selections in row-major order, `(1,2), (1,4), (1,6), (3,2), (3,4), (3,6), (11,2), (11,4), (11,6)`, whose sums sort to `3, 5, 5, 7, 7, 9, 13, 15, 17`; index `4` reads `7`, matching the expected Output.

#### Solution

```python
import itertools
from typing import List


class Solution:
    def solve(self, mat: List[List[int]], k: int) -> int:
        """Return the kth smallest sum obtainable by picking one value per row.

        Time:  O(P log P): the product materializes all P selections and the
            sort dominates.
        Space: O(P) for the sorted list of selection sums.
        """
        return sorted(sum(selection) for selection in itertools.product(*mat))[k - 1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(P log P)`

Identical work to the brute force: all `P` selection sums are built and sorted.

##### Space Complexity: `O(P)`

The sorted list holds every selection sum; the product itself streams one selection at a time.

#### Key Insights

- `itertools.product` replaces the two nested expansion loops with the library's own enumeration, leaving the sum-sort-index pipeline visible in one line.
- The generator feeds the sort lazily, but the sort still materializes every sum, so the asymptotics never improve over the brute force.
- It ranks last for the same reason the brute force does: correct and compact, but it pays for all `P` selections when only `k` are needed.

## Comparison of Solutions

### Time Complexity

- **Brute Force Full Expansion**: `O(P log P)` - builds all `P = product of row lengths` sums and sorts them.
- **Truncation by Prefix**: `O(m × n × k × log(k × n))` - sorts at most `k × n` candidates per row over `m` rows.
- **Heap Pair Merge**: `O(m × k × log k)` - at most `k` heap pops per row on a heap capped at `2k` entries.
- **One-Liner with itertools.product**: `O(P log P)` - same enumeration and sort as the brute force.

### Space Complexity

- **Brute Force Full Expansion**: `O(P)` - the expansion holds every selection sum.
- **Truncation by Prefix**: `O(k × n)` - the kept list is capped at rank `k`, with one row's candidates transiently reaching `k × n`.
- **Heap Pair Merge**: `O(k)` - the heap and merged list never exceed `2k` and `k` entries.
- **One-Liner with itertools.product**: `O(P)` - the sorted list materializes all sums.

### Trade-offs

- **Brute Force Full Expansion**: the shortest from-scratch expression of the problem and trivially correct, but its cost grows with the full selection product rather than with `k`.
- **Truncation by Prefix**: bounds retained memory by the answer size with a two-line change to the brute force, but still sorts every kept-times-row candidate pair.
- **Heap Pair Merge**: removes the row length from the sorting work and only ever touches pairs a rank can use, at the cost of heap bookkeeping and the seed-once successor rule.
- **One-Liner with itertools.product**: maximally compact, but it inherits the brute force's full product cost and hides the enumeration behind a library call.

### When to Use Each

- **Truncation by Prefix (Recommended)**: the interview default: easy to derive from the brute force, memory bounded by `k`, and simple to prove correct.
- **Heap Pair Merge**: when the interviewer pushes past `O(k × n)` per row or the row lengths make truncation's candidate sort the bottleneck.
- **Brute Force Full Expansion**: as the spoken baseline that motivates the other two; also fine when every row is short and `P` is tiny.
- **One-Liner with itertools.product**: for quick scripts and cross-checking the other approaches on small inputs.

### Optimization Notes

- An `O(m × n × log(...))` alternative exists for much larger `k`: binary search the answer value `s` and count selections with sum at most `s` in `O(m × n)` per count by walking each row with a shrinking pointer; with `k <= 200` here, the heap ladder is simpler and already linear in `k`.
- The heap variant relies on row values being at least `1`, so pair sums strictly increase along successors; with non-positive values allowed, the seeded-heap growth order would need a full re-derivation.
- A common pitfall in the heap variant is seeding `(partial_idx + 1, col_idx)` pairs eagerly for every column at row start; that re-introduces the `k × n` candidate set the heap exists to avoid.
- Ranks, not values, are sorted here: equal sums from distinct selections occupy distinct ranks, which is why the sorted lists in the walkthroughs keep their duplicate entries.
