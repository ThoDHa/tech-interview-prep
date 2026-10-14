# [Dynamic Kth Largest Queries](https://www.fastprep.io/problems/amazon-dynamic-kth-largest-queries)

**unknown difficulty** | **NN minutes** | **unknown categories**

You are given an initial list of integer values and a stream of operations. The list changes over time as values are inserted.

Each operation is one of the following:

"insert": insert the accompanying value into the list."find": treat the accompanying value as k and return the current k-th largest value in the list.Return the answers to all "find" operations in order.

## Examples

### Example 1

**Input:** `initialValues = [3, 7, 1]`, `operations = ["find", "insert", "insert", "find", "find"]`, `values = [3, 4, 9, 2, 4]`

**Output:** `[1, 7, 3]`

**Explanation:** Initially the sorted values are [1,3,7], so the 3rd largest is 1. After inserting 4 and 9, the values are [1,3,4,7,9]; the 2nd largest is 7 and the 4th largest is 3.

### Example 2

**Input:** `initialValues = [5]`, `operations = ["insert", "find", "insert", "find"]`, `values = [2, 1, 10, 2]`

**Output:** `[5, 5]`

**Explanation:** After inserting 2, the largest value is 5. After inserting 10, the 2nd largest value is still 5.

## Constraints

- `operations.length == values.length`
- `Each operation is either "insert" or "find".`
- `For each "find" operation, 1 <= k <= the current list size.`

## Solutions

Throughout this page `m` is the number of values currently stored, `q` is the number of operations, and `u` is the number of distinct values that ever appear.

### Resort on Every Find

#### Derivation

The most literal reading of the contract: the list is just a bag of values, and "the `k`th largest" is a question about the sorted bag. The `insert` operations arrive far more often than they can be worth pre-sorting for, so the implementation stores values in arrival order and re-sorts only when a `find` asks. In an ascending list the `k`th largest sits at negative index `-k`, counting from the end where the largest values live:

1. Copy `initialValues` into `current` and start `answers` empty.
2. Walk the operation stream paired with `values` through `zip`.
3. On `"insert"`, append the accompanying value to `current`.
4. On `"find"`, sort `current` ascending and append `sorted(current)[-k]` to
   `answers`, where `k` is the accompanying value.
5. Return `answers` after the stream ends.

#### Walkthrough

Example 1: `initialValues = [3, 7, 1]`, `operations = ["find", "insert", "insert", "find", "find"]`, `values = [3, 4, 9, 2, 4]`. Each line is one event; the find rows show the sort they pay for:

```text
start        current = [3, 7, 1]
find k=3     sorted [1, 3, 7]      answers = [1]
insert 4     current = [3, 7, 1, 4]
insert 9     current = [3, 7, 1, 4, 9]
find k=2     sorted [1, 3, 4, 7, 9]    answers = [1, 7]
find k=4     sorted [1, 3, 4, 7, 9]    answers = [1, 7, 3]
```

The returned list `[1, 7, 3]` matches the expected Output. (Example 2 traces the same way: after `insert 2` the sorted list `[2, 5]` gives `1st` largest `5`; after `insert 10` the sorted list `[2, 5, 10]` gives `2nd` largest `5`.)

#### Solution

The code is the walkthrough's event loop: append on insert, sort-and-read on find.

```python
from typing import List


class Solution:
    def solve(self, initialValues: List[int], operations: List[str], values: List[int]) -> List[int]:
        current = list(initialValues)
        answers = []
        for operation, argument in zip(operations, values):
            if operation == "insert":
                current.append(argument)
            else:
                answers.append(sorted(current)[-argument])
        return answers
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(q × m log m)`

Every `find` sorts all `m` stored values, so a find-heavy stream pays the full sort each time; inserts are `O(1)` appends.

##### Space Complexity: `O(m)`

The stored values plus the sorted copy each `find` materializes.

#### Key Insights

- `sorted(current)[-k]` reads the `k`th largest without reversing: negative indexing counts from the largest end.
- Keeping the list unsorted makes every insert cheap and every find expensive, which is the right trade only when finds are rare.
- Each find re-derives an order that is nearly identical to the previous find's order; nothing is remembered, which is the waste the next approach removes.

### Sorted List with Linear Insertion

#### Derivation

The resort-on-every-find approach throws away its own work: after a find, the list is sorted, and appending one value disturbs only that value's slot, never the order of the rest. (The min-heap of size `k` from the fixed-`k` stream problem does not transfer here, because `k` changes from query to query; keeping the full sorted list serves every `k` at once.) Keep the list sorted permanently and pay one insertion-sort pass per insert, shifting larger values one slot right until the new value's home appears:

1. Sort `initialValues` once at the start into `sorted_values`.
2. On `"insert"`, append the value, then walk `position` left from the end,
   shifting every larger value one slot right; drop the value at the vacated
   slot.
3. On `"find"`, the list is already sorted, so append `sorted_values[-k]` to
   `answers` directly, no work at all.
4. Return `answers`.

#### Walkthrough

Example 1 again. The construction sorts once, and the interesting events are the two inserts, each shown as the shifting pass of `position`:

```text
start         sorted_values = [1, 3, 7]
find k=3      read sorted_values[-3] = 1          answers = [1]
insert 4      append at position 3: [1, 3, 7, 4]
              sorted_values[2] = 7 > 4: shift right, position 2
              sorted_values[1] = 3 > 4? no: place 4 at slot 2
              sorted_values = [1, 3, 4, 7]
insert 9      append at position 4: [1, 3, 4, 7, 9]
              sorted_values[3] = 7 > 9? no: place 9, no shifts
              sorted_values = [1, 3, 4, 7, 9]
find k=2      read sorted_values[-2] = 7          answers = [1, 7]
find k=4      read sorted_values[-4] = 3          answers = [1, 7, 3]
```

Every find is now a plain index read, and the inserts performed one and zero shifts; the returned `[1, 7, 3]` matches the expected Output.

#### Solution

The code is the walkthrough's shifting pass: append, shift larger values right, place.

```python
from typing import List


class Solution:
    def solve(self, initialValues: List[int], operations: List[str], values: List[int]) -> List[int]:
        sorted_values = sorted(initialValues)
        answers = []
        for operation, argument in zip(operations, values):
            if operation == "insert":
                position = len(sorted_values)
                sorted_values.append(argument)
                while position > 0 and sorted_values[position - 1] > argument:
                    sorted_values[position] = sorted_values[position - 1]
                    position -= 1
                sorted_values[position] = argument
            else:
                answers.append(sorted_values[-argument])
        return answers
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × q)`

Each insert shifts up to all `m` stored values (a value smaller than everything stored lands at the front), while each find is a constant-time read.

##### Space Complexity: `O(m)`

The sorted list itself; the insertion happens in place.

#### Key Insights

- Sorting once and maintaining the order converts the expensive operation from find to insert, the right trade when finds outnumber inserts.
- The shifting walk is insertion sort's inner loop; on nearly-sorted arrival streams it shifts almost nothing, but adversarial descending inserts degrade it to linear per insert.
- The list stays the single source of truth, so a find never allocates anything.

### Fenwick Tree over Compressed Ranks

#### Derivation

Both sorted-list approaches pay a tail shift on insert, because an array must stay contiguous. The values themselves are irrelevant to ordering questions; only their ranks matter. Collect every value that will ever exist (the initial values plus every value in `values`, since inserts only ever introduce those), compress them to ranks `1..u`, and store one count per rank in a [Fenwick tree](https://en.wikipedia.org/wiki/Fenwick_tree). An insert becomes a point update adding `1` at one rank; a find becomes a select: the `k`th largest is the rank whose prefix count reaches `m - k + 1` (the `m - k + 1`th smallest), which the tree answers by descending its powers of two:

1. Build `universe = sorted(set(initialValues) | set(values))` and `rank_of`,
   mapping each value to its `1`-based rank; build the `FenwickTree` over
   `len(universe)` ranks.
2. Insert every initial value: `tree.add(rank_of[value])`; set `values_present`
   to the initial count.
3. On `"insert"`: `tree.add(rank_of[argument])` and increment `values_present`.
4. On `"find"`: compute `smallest_rank = values_present - argument + 1`, then
   `answers.append(universe[tree.select(smallest_rank) - 1])`.
5. Return `answers`.

The select inside the tree: start at rank `0` with the target count and try skipping `step` ranks for `step` at the largest power of two below the size, halving down; when the prefix count of the candidate rank is below the target, keep the skip and subtract it from the target. The rank after the last kept skip is the `target`th smallest.

#### Walkthrough

Example 1: `initialValues = [3, 7, 1]`, `operations = ["find", "insert", "insert", "find", "find"]`, `values = [3, 4, 9, 2, 4]`. The universe and the three initial inserts first:

```text
universe = [1, 2, 3, 4, 7, 9]      ranks 1..6 via rank_of
insert 3 (rank 3)   counts[3] += 1, counts[4] += 1
insert 7 (rank 5)   counts[5] += 1, counts[6] += 1
insert 1 (rank 1)   counts[1] += 1, counts[2] += 1, counts[4] += 1
                    counts = [_, 1, 1, 1, 2, 1, 1]
```

The operation stream, with each find's `select` shown step by step (`step` starts at the largest power of two below 7, which is 4):

```text
find k=3     smallest_rank = 3 - 3 + 1 = 1
             step 4: counts[4] = 2 < 1? no     step 2: counts[2] = 1 < 1? no
             step 1: counts[1] = 1 < 1? no     select returns rank 1 -> value 1
             answers = [1]
insert 4     rank 4: counts[4] += 1        counts = [_, 1, 1, 1, 3, 1, 1]
insert 9     rank 6: counts[6] += 1        counts = [_, 1, 1, 1, 3, 1, 2]
find k=2     smallest_rank = 5 - 2 + 1 = 4
             step 4: counts[4] = 3 < 4? yes: position 4, target 4 - 3 = 1
             step 2: counts[6] = 2 < 1? no     step 1: counts[5] = 1 < 1? no
             select returns rank 5 -> value 7  answers = [1, 7]
find k=4     smallest_rank = 5 - 4 + 1 = 2
             step 4: counts[4] = 3 < 2? no     step 2: counts[2] = 1 < 2? yes: position 2, target 1
             step 1: counts[3] = 1 < 1? no     select returns rank 3 -> value 3
             answers = [1, 7, 3]
```

The three selected ranks `1`, `5`, `3` map to values `1`, `7`, `3`, the expected Output. Note that `counts` holds Fenwick partial sums, not per-rank counts: `counts[4] = 3` covers ranks `1` through `4`.

#### Solution

The code is the rank bookkeeping around the two tree operations, `add` and the binary-lifting `select`:

```python
from typing import List


class FenwickTree:
    def __init__(self, size: int) -> None:
        self.counts = [0] * (size + 1)

    def add(self, rank: int) -> None:
        while rank < len(self.counts):
            self.counts[rank] += 1
            rank += rank & -rank

    def prefix_count(self, rank: int) -> int:
        total = 0
        while rank > 0:
            total += self.counts[rank]
            rank -= rank & -rank
        return total

    def select(self, target: int) -> int:
        step = 1
        while step * 2 < len(self.counts):
            step *= 2
        position = 0
        while step > 0:
            next_position = position + step
            if next_position < len(self.counts) and self.counts[next_position] < target:
                position = next_position
                target -= self.counts[next_position]
            step //= 2
        return position + 1


class Solution:
    def solve(self, initialValues: List[int], operations: List[str], values: List[int]) -> List[int]:
        universe = sorted(set(initialValues) | set(values))
        rank_of = {value: rank for rank, value in enumerate(universe, start=1)}
        tree = FenwickTree(len(universe))
        for value in initialValues:
            tree.add(rank_of[value])

        answers = []
        values_present = len(initialValues)
        for operation, argument in zip(operations, values):
            if operation == "insert":
                tree.add(rank_of[argument])
                values_present += 1
            else:
                smallest_rank = values_present - argument + 1
                answers.append(universe[tree.select(smallest_rank) - 1])
        return answers
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((m + q) × log(m + q))`

Sorting the universe costs `O((m + q) × log(m + q))` once, and every operation afterwards is one tree `add` or one binary-lifting `select`, each `O(log u)` with `u <= m + q`.

##### Space Complexity: `O(u)`

The Fenwick array plus the rank map, one entry per distinct value.

#### Key Insights

- Coordinate compression before the tree is what keeps it small: only ranks, not values, occupy the array, so arbitrary integer values cost nothing extra.
- The conversion `smallest_rank = values_present - k + 1` reuses the same negative-index logic as the list solutions (`[-k]` also means "the `m - k + 1`th smallest") in rank form.
- Both operations shrink from `O(m)` to `O(log u)` because the tree never moves data: order lives in the rank arithmetic, counts live in the partial sums.
- The compression pass needs to see every future value up front, so this design fits a known operation stream but not values that arrive from a truly unbounded source.

### Sorted List with Binary Search Insertion

#### Derivation

The linear insertion finds the new value's home by walking one slot at a time, but the list it walks is sorted, and sorted is exactly what [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) exploits. `bisect.insort` packages that search together with the list splice: the comparisons drop from `O(m)` to `O(log m)`, while the underlying insert still shifts the tail to make room. This is the same algorithm as the linear insertion with only the slot-finding bookkeeping handed to the standard library:

1. Sort `initialValues` once into `sorted_values`.
2. On `"insert"`, call `insort(sorted_values, value)`, which locates the slot
   by binary search and splices the value in.
3. On `"find"`, read `sorted_values[-k]` as before.
4. Return `answers`.

#### Walkthrough

Example 1, with each insert replaced by the slot `bisect` reports and the splice that follows:

```text
start         sorted_values = [1, 3, 7]
find k=3      read sorted_values[-3] = 1          answers = [1]
insert 4      bisect finds slot between 3 and 7:  [1, 3, 4, 7]
insert 9      bisect finds slot at the end:       [1, 3, 4, 7, 9]
find k=2      read sorted_values[-2] = 7          answers = [1, 7]
find k=4      read sorted_values[-4] = 3          answers = [1, 7, 3]
```

Same final list, same `[1, 7, 3]`; only the way the slot was found changed.

#### Solution

The code is the linear insertion with the walk replaced by `insort`:

```python
from bisect import insort
from typing import List


class Solution:
    def solve(self, initialValues: List[int], operations: List[str], values: List[int]) -> List[int]:
        sorted_values = sorted(initialValues)
        answers = []
        for operation, argument in zip(operations, values):
            if operation == "insert":
                insort(sorted_values, argument)
            else:
                answers.append(sorted_values[-argument])
        return answers
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × q)`

Binary search finds each slot in `O(log m)` comparisons, but splicing into a list still shifts up to `m` tail elements, so the worst case per insert stays linear.

##### Space Complexity: `O(m)`

The sorted list; `insort` works in place.

#### Key Insights

- `insort` halves the comparisons but not the shifting: list splicing is the bottleneck, so the worst case per insert stays linear, and a tree-backed container is the door to logarithmic inserts.

## Comparison of Solutions

### Time Complexity

- **Resort on Every Find**: `O(q × m log m)` - every find re-sorts all stored values.
- **Sorted List with Linear Insertion**: `O(m × q)` - each insert shifts up to the whole list; finds are `O(1)` reads.
- **Fenwick Tree over Compressed Ranks**: `O((m + q) × log(m + q))` - one sort up front, then `O(log u)` per operation.
- **Sorted List with Binary Search Insertion**: `O(m × q)` - `O(log m)` comparisons per insert but a linear tail shift remains.

### Space Complexity

- **Resort on Every Find**: `O(m)` - the stored values plus one sorted copy per find.
- **Sorted List with Linear Insertion**: `O(m)` - the sorted list, updated in place.
- **Fenwick Tree over Compressed Ranks**: `O(u)` - one count per distinct rank plus the rank map.
- **Sorted List with Binary Search Insertion**: `O(m)` - the sorted list, updated in place.

### Trade-offs

- **Resort on Every Find**: the least code and the easiest to trust, but a find-heavy stream pays a full sort per query.
- **Sorted List with Linear Insertion**: shifts the cost to inserts, ideal when finds dominate; degrades on adversarial insert orders.
- **Fenwick Tree over Compressed Ranks**: logarithmic per operation with no shifting at all, at the price of coordinate compression and a select routine you must argue correct.
- **Sorted List with Binary Search Insertion**: same algorithm as the linear walk with the slot search handed to the library and a smaller constant, still bounded by list splicing.

### When to Use Each

- **Resort on Every Find**: a warm-up or a checker for tests; almost never the interview answer.
- **Sorted List with Linear Insertion**: when finds vastly outnumber inserts and the value count is modest.
- **Fenwick Tree over Compressed Ranks**: when operation counts grow past what tail shifts tolerate, and in any interview where the follow-up "can you do better than linear per operation?" appears.
- **Sorted List with Binary Search Insertion (Recommended)**: the interview default: `bisect.insort` is two lines, correct, and fast in practice for typical constraint sizes.

### Optimization Notes

- The negative-index read `sorted_values[-k]` is the shared trick of all three list solutions; converting it to `smallest_rank = values_present - k + 1` is what carries the idea into rank space.
- If the stream also deleted values, only the Fenwick design extends cleanly: decrement the count at the rank instead of incrementing, and every list-based approach breaks (splice removal is linear, resorting degenerates).
- `sortedcontainers.SortedList` gives the same `O(log m)` behavior as the Fenwick design with library-grade testing, but it is a third-party dependency; the tree keeps the solution import-free for a reason that matters in a graded OA environment.
- Duplicate values need no special handling anywhere: ranks count occurrences, so two equal values occupy one rank with count two.
