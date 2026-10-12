# [Calculate Beauty Values](https://www.fastprep.io/problems/amazon-calculate-beauty-values)

**Medium** | **NN minutes** | **Array, Sorting, Prefix Sum**

Source note: The judged core task matches the visible source at about 100%. The source images do not show numeric bounds or the original callable signature.

Special thanks: A special thank you to a lovely, amazing fren who shared that this question appeared again on September 14, 2026! 🩷

Amazon's development team is working on a feature for a new product, a smart array processor. In this smart processor, quite simply, given an array of numbers and instructions on which parts of the array to pick and combine into a new array, for each number in the original array, if it's included in the new array, its efficiency is 0; otherwise, the efficiency is the count of smaller numbers in the new array. The goal is to add up the efficiencies for all numbers in the original array.

A user has provided an integer array called arr of size n and a 2-dimensional array called pairs of size m x 2. Each pair in the pairs array represents the starting and ending indices of a subarray within arr.

For each subarray of arr represented by the array pairs, the goal is to merge and concatenate them into a nefficiency callew efficient.

The efficiency of an element at index i in arr is defined as follows: if the index i has not contributed to the formation of the array efficient, the efficiency is the count of integers in efficient that have a value strictly smaller than arr[i]. If the index i has contributed to the formation of the array efficient, its efficiency is 0.

Find the sum of the effiemncy of all the efficients in the array arr.

## Examples

### Example 1

**Input:** `arr = [1, 2, 3, 2, 4, 5]`, `pairs = [[0, 1], [3, 4], [0, 0], [3, 4]]`

**Output:** `12`

**Explanation:** $24

## Constraints

- `arr is an integer array of size n.`
- `pairs is an integer array of size m × 2.`
- `Each pair contains valid inclusive start and end indices for a subarray of arr.`

## Solutions

The statement restated: the array `efficient` is built by appending, in pair
order, the subarray `arr[start:end + 1]` for every pair `[start, end]` in
`pairs`. An index has *contributed* when it falls inside at least one pair's
inclusive range. The efficiency of an index is `0` when it contributed, and
otherwise the count of entries in `efficient` holding a value strictly smaller
than that index's value (duplicates counted). The answer sums that efficiency
over every index.

### Brute Force Concatenation

#### Derivation

The most literal reading executes the statement sentence by sentence: build
`efficient` by extending it with each pair's subarray, mark the indices that
contributed, then price every non-contributing index with a full scan of
`efficient`:

1. Allocate `contributed`, a boolean array of `len(arr)` slots, all `False`.
2. For each `(start, end)` pair, set `contributed[position] = True` for every
   `position` in the inclusive range, and `extend` `efficient` with
   `arr[start:end + 1]`.
3. For every `index` whose `contributed[index]` is still `False`, count the
   entries of `efficient` strictly smaller than `arr[index]` into
   `smaller_count` and add it to `total`.
4. Contributed indices add `0` by being skipped.
5. Return `total`.

#### Walkthrough

Example 1: `arr = [1, 2, 3, 2, 4, 5]`, `pairs = [[0, 1], [3, 4], [0, 0], [3, 4]]`.
The concatenation builds `efficient` chunk by chunk:

```text
[0, 1]  extend arr[0:2] = [1, 2]     efficient = [1, 2]
[3, 4]  extend arr[3:5] = [2, 4]     efficient = [1, 2, 2, 4]
[0, 0]  extend arr[0:1] = [1]        efficient = [1, 2, 2, 4, 1]
[3, 4]  extend arr[3:5] = [2, 4]     efficient = [1, 2, 2, 4, 1, 2, 4]
```

The pairs cover indices `0`, `1`, `3`, and `4`, so only indices `2` and `5`
are priced:

```text
index 2   value 3   scan: 1, 2, 2, 1, 2 are smaller than 3      -> 5
index 5   value 5   scan: all seven entries are smaller than 5  -> 7
total = 5 + 7 = 12
```

The sum `12` matches the expected Output for Example 1.

#### Solution

The code is the walkthrough written down: one extend per pair, one scan per
skipped index.

```python
from typing import List


class Solution:
    def solve(self, arr: List[int], pairs: List[List[int]]) -> int:
        efficient: List[int] = []
        contributed = [False] * len(arr)
        for start, end in pairs:
            for position in range(start, end + 1):
                contributed[position] = True
            efficient.extend(arr[start:end + 1])

        total = 0
        for index, value in enumerate(arr):
            if contributed[index]:
                continue
            smaller_count = 0
            for picked_value in efficient:
                if picked_value < value:
                    smaller_count += 1
            total += smaller_count
        return total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n^2)` worst case

Let `V` be the total number of picked entries, the sum of the pair lengths,
at most `m × n`. Building `efficient` and marking contributions cost `O(V)`;
each of the at most `n` skipped indices then scans all `V` entries, for
`O(n × V)` overall.

##### Space Complexity: `O(V)`

The `efficient` list holds every picked entry, duplicates included.

#### Key Insights

- The efficiency rule never reads `arr` beyond the skipped index's own value:
  everything else comes from the built array, so the problem is really "count
  smaller elements, with a blacklist of indices".
- Repeated pairs contribute repeatedly: Example 1 lists `[3, 4]` twice, and
  both copies of `[2, 4]` land in `efficient`.
- The quadratic scan is the only expensive step; every skipped index re-counts
  the same entries from scratch, which is the waste the next solutions remove.

### Sorted Chunks with Binary Search

#### Derivation

The brute force re-scans all `V` entries for every skipped index. The scan
answers one question, "how many entries are smaller than `value`?", and that
question over a sorted collection is a [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm):
the answer is the insertion point of `value`. Keeping each pair's subarray as
its own sorted chunk preserves the multiset of `efficient` exactly (the
concatenation order never mattered for counting), and a per-value cache stops
two skipped indices holding equal values from paying twice:

1. Mark contributions as before, and append `sorted(arr[start:end + 1])` to
   `sorted_chunks` for each pair.
2. For a skipped index's `value`, sum `bisect_left(chunk, value)` over all
   `sorted_chunks`; each term is the chunk's count of entries strictly smaller
   than `value`.
3. Store that sum in `smaller_cache[value]` so repeated values are answered
   from the cache.
4. Skip contributed indices; add the cached count for the others.

#### Walkthrough

Example 1 again. The four chunks, each sorted independently, are:

```text
[0, 1] -> [1, 2]     [3, 4] -> [2, 4]     [0, 0] -> [1]     [3, 4] -> [2, 4]
```

Only indices `2` (value `3`) and `5` (value `5`) are skipped, and each query
adds one `bisect_left` term per chunk:

```text
value 3   [1, 2] -> 2     [2, 4] -> 1     [1] -> 1     [2, 4] -> 1   sum = 5
value 5   [1, 2] -> 2     [2, 4] -> 2     [1] -> 1     [2, 4] -> 2   sum = 7
total = 5 + 7 = 12
```

The chunk counts reproduce the brute force scan exactly: five entries are
smaller than `3` and seven are smaller than `5`, so the function returns `12`,
matching the expected Output for Example 1.

#### Solution

The code is the chunk sort plus the cached per-chunk binary searches.

```python
from bisect import bisect_left
from typing import Dict, List


class Solution:
    def solve(self, arr: List[int], pairs: List[List[int]]) -> int:
        contributed = [False] * len(arr)
        sorted_chunks: List[List[int]] = []
        for start, end in pairs:
            for position in range(start, end + 1):
                contributed[position] = True
            sorted_chunks.append(sorted(arr[start:end + 1]))

        smaller_cache: Dict[int, int] = {}
        total = 0
        for index, value in enumerate(arr):
            if contributed[index]:
                continue
            if value not in smaller_cache:
                smaller_count = 0
                for chunk in sorted_chunks:
                    smaller_count += bisect_left(chunk, value)
                smaller_cache[value] = smaller_count
            total += smaller_cache[value]
        return total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V log n + q × m × log n)`

Sorting the chunks costs `O(V log n)` with `V` the total picked entries and
`n` the array size. Each of the `q` distinct skipped values (at most `n`) sums
one binary search per chunk, `O(m × log n)`. On inputs where pairs are few the
query term dominates; where pairs are many the tallying of the next solution
wins.

##### Space Complexity: `O(V)`

The sorted chunks hold every picked entry once, duplicates included.

#### Key Insights

- Sorting per chunk instead of one global sort is forced: the insertion-point
  trick on a globally sorted copy loses track of which values came from which
  subarray.
- The multiset view is what makes the chunking legal: counting smaller entries
  is order-blind, so the concatenation can be regrouped freely.
- The cache exploits the gap between skipped indices and distinct skipped
  values; equal values share one answer.

### Frequency Table with Prefix Sums

#### Derivation

The sorted chunks still store all `V` entries, though counting never needed
the entries themselves, only how many hold each value. Collapsing `efficient`
into a value-to-count table removes the materialization: the table is built by
tallying each pair's entries as they are marked, the sorted distinct values
with running totals form a prefix-count array, and each query becomes a single
binary search into the distinct values:

1. For each pair, mark contributions and tally `frequency[arr[position]]` for
   every `position` in the inclusive range.
2. Sort the distinct values into `distinct_values` and build `prefix_counts`,
   where `prefix_counts[iteration_position]` is the number of entries in
   `efficient` holding any of the first `iteration_position` distinct values.
3. For a skipped index's `value`, the count of strictly smaller entries is
   `prefix_counts[bisect_left(distinct_values, value)]`.
4. Skip contributed indices; add the looked-up count for the others. Queries
   are now cheap enough that the per-value cache is unnecessary.

#### Walkthrough

Example 1 one last time. Tallying the four subarrays `[1, 2]`, `[2, 4]`,
`[1]`, `[2, 4]` counts value `1` twice, value `2` three times, value `4`
twice:

```text
frequency = {1: 2, 2: 3, 4: 2}
distinct_values = [1, 2, 4]
prefix_counts   = [0, 2, 5, 7]
```

The skipped indices query the table with one binary search each:

```text
value 3   bisect_left([1, 2, 4], 3) = 2   prefix_counts[2] = 5
value 5   bisect_left([1, 2, 4], 5) = 3   prefix_counts[3] = 7
total = 5 + 7 = 12
```

The prefix counts read back the same five and seven entries the earlier
solutions counted entry by entry, so the function returns `12`, matching the
expected Output for Example 1.

#### Solution

The code is the tally, the prefix sweep, and one binary search per skipped
index.

```python
from bisect import bisect_left
from itertools import accumulate
from typing import Dict, List


class Solution:
    def solve(self, arr: List[int], pairs: List[List[int]]) -> int:
        size = len(arr)
        contributed = [False] * size
        frequency: Dict[int, int] = {}
        for start, end in pairs:
            for position in range(start, end + 1):
                contributed[position] = True
                frequency[arr[position]] = frequency.get(arr[position], 0) + 1

        distinct_values = sorted(frequency)
        prefix_counts = [0]
        prefix_counts.extend(
            accumulate(frequency[value] for value in distinct_values)
        )

        total = 0
        for index, value in enumerate(arr):
            if contributed[index]:
                continue
            insertion_point = bisect_left(distinct_values, value)
            total += prefix_counts[insertion_point]
        return total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V + n + d log d)`

Tallying touches each of the `V` picked entries once; the final pass visits
each of the `n` indices and answers with one `O(log d)` binary search into the
`d` distinct picked values, whose sorting costs `O(d log d)`. With `d <= V`
this dominates the sorted-chunks cost whenever pairs overlap heavily.

##### Space Complexity: `O(d)`

The frequency table, distinct values, and prefix counts hold one slot per
distinct picked value; nothing stores the `V` entries themselves.

#### Key Insights

- The step from chunks to a tally is the classic "store the multiset as
  counts" compression: counting smaller elements only needs the value
  histogram, never the sequence.
- `prefix_counts[insertion_point]` counts strictly smaller entries in one
  lookup because `bisect_left` lands before the first entry equal to `value`.
- Contributed indices cost a single boolean check: their values never enter
  the frequency table unless some other pair also picked them.

## Comparison of Solutions

### Time Complexity

- **Brute Force Concatenation**: `O(m × n^2)` worst case - builds the picked
  entries once, then scans all of them per skipped index.
- **Sorted Chunks with Binary Search**: `O(V log n + q × m × log n)` - one
  chunk sort per pair plus one binary search per chunk per distinct query.
- **Frequency Table with Prefix Sums**: `O(V + n + d log d)` - one tally per
  picked entry plus a single binary search per skipped index.

### Space Complexity

- **Brute Force Concatenation**: `O(V)` - the materialized concatenation.
- **Sorted Chunks with Binary Search**: `O(V)` - the sorted chunks hold every
  picked entry.
- **Frequency Table with Prefix Sums**: `O(d)` - one slot per distinct picked
  value.

### Trade-offs

- **Brute Force Concatenation**: the statement translated line by line and
  almost impossible to get wrong, but the per-index scans collapse on inputs
  with many skipped indices over many pairs.
- **Sorted Chunks with Binary Search**: turns each scan into logarithmic
  searches while keeping the concatenation's shape, at the cost of sorting
  machinery and a still-materialization-sized memory footprint.
- **Frequency Table with Prefix Sums**: never materializes the concatenation
  and answers queries in one lookup, but needs the two-layer indirection of
  distinct values plus prefix counts to stay correct on duplicates.

### When to Use Each

- **Brute Force Concatenation**: as the spoken baseline and correctness
  reference; fine when the picked volume is tiny.
- **Sorted Chunks with Binary Search** (Recommended): the interview default:
  one clear idea (sort each chunk, bisect per query) with a cache that shows
  awareness of repeated values.
- **Frequency Table with Prefix Sums**: when pairs are many and overlapping,
  so the picked volume dwarfs the distinct-value count, or when memory for the
  concatenation is the binding constraint.

### Optimization Notes

- The counting never depends on concatenation order, only on the multiset of
  picked entries; every speedup here is a different representation of that
  multiset (list, sorted chunks, value counts).
- The per-value cache matters exactly when several skipped indices share a
  value; the frequency table makes it redundant by pricing every query at one
  binary search.
- A tempting shortcut, one global sort with per-range binary searches, is
  subtly wrong: sorting `arr` globally scrambles which values sit inside each
  pair's index window, so range-bounded searches return counts of the wrong
  entries.
