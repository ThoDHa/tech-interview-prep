# [Top K Frequent Elements](https://www.fastprep.io/problems/amazon-top-k-frequent-elements)

**Medium** | **NN minutes** | **Array, Hash Table, Heap, Sorting**

Given a nonempty integer array nums and an integer k, return the k distinct values that occur most frequently.

## Examples

### Example 1

**Input:** `nums = [1,1,1,2,2,3]`, `k = 2`

**Output:** `[1,2]`

**Explanation:** Value 1 appears three times and value 2 appears twice.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-top-k-frequent-elements; fill them in. -->

## Solutions

### Count and Sort

#### Derivation

The most direct reading splits the problem into two stages that any solution
must perform: tally how often each value occurs, then choose the `k` highest
tallies. The baseline delegates the second stage entirely to sorting, because
sorting the distinct values by descending frequency lines the winners up at
the front of the list:

1. Build `counts`, a dictionary mapping each value in `nums` to its frequency.
2. Collect the distinct values and sort them by `counts[value]`, descending.
3. Slice the first `k` entries off the sorted list and return them.

#### Walkthrough

Trace both stages on Example 1: `nums = [1,1,1,2,2,3]`, `k = 2`. The counting
pass tallies one value at a time:

```text
value 1   counts = {1: 1}
value 1   counts = {1: 2}
value 1   counts = {1: 3}
value 2   counts = {1: 3, 2: 1}
value 2   counts = {1: 3, 2: 2}
value 3   counts = {1: 3, 2: 2, 3: 1}
```

Sorting the three distinct values by descending frequency orders them
`[1, 2, 3]` (frequencies `3, 2, 1`), and the slice `[:2]` returns `[1, 2]`,
matching the expected Output exactly.

#### Solution

The code is the tally, the frequency sort, and the slice.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int], k: int) -> List[int]:
        counts = {}
        for num in nums:
            counts[num] = counts.get(num, 0) + 1
        distinct = sorted(counts, key=counts.get, reverse=True)
        return distinct[:k]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Counting is `O(n)`. With `m` distinct values (`m <= n`), the sort costs
`O(m log m)`, which is `O(n log n)` at worst.

##### Space Complexity: `O(n)`

The dictionary and the sorted distinct list hold `O(m) <= O(n)` entries.

#### Key Insights

- The two-stage structure, count then select, is shared by every approach on
  this page; they differ only in how the second stage picks the winners.
- Sorting all `m` distinct values does more work than the problem asks for:
  the bottom `m - k` values are ordered with nobody looking.
- Sorting by descending frequency also fixes the output order, which is why
  this baseline reproduces Example 1's `[1, 2]` without any postprocessing.

### Min-Heap of Size K

#### Derivation

The sort's waste is that it fully orders all `m` candidates when only `k`
survive. The selection-only alternative keeps a [heap](https://en.wikipedia.org/wiki/Priority_queue)
holding the best `k` values seen so far, ordered so its root is the *weakest*
of the current winners. Each candidate then faces exactly one comparison: beat
the root and replace it, or leave. Because the heap never grows past `k`,
every heap operation costs `O(log k)` regardless of `n`:

1. Build `counts` as before.
2. Seed the min-heap with the first `k` `(frequency, value)` pairs from
   `counts`.
3. For each remaining pair, push it and pop the minimum, so the heap always
   holds the `k` strongest.
4. Pop all `k` winners out (they leave in ascending frequency) and reverse
   them, so the returned list reads in descending-frequency order like
   Example 1's Output.

Storing `(frequency, value)` tuples keeps the comparison on frequency first,
with the value breaking frequency ties deterministically.

#### Walkthrough

Trace the heap on Example 1: `nums = [1,1,1,2,2,3]`, `k = 2`. After counting,
the pairs in insertion order are `(3, 1)`, `(2, 2)`, `(1, 3)`. The first `k`
pairs seed the heap:

```text
seed   heap = [(2, 2), (3, 1)]      root (2, 2) is the weakest winner
(1,3)  push -> heap = [(1, 3), (3, 1), (2, 2)]
       pop minimum (1, 3)
       heap = [(2, 2), (3, 1)]      root (2, 2) is the weakest again
```

The candidate `(1, 3)`, value 3 with the lowest frequency, lost its
comparison against the root and was discarded on the spot. Popping the final
heap yields `(2, 2)` then `(3, 1)`, ascending frequency, and reversing gives
values `[1, 2]`, matching the expected Output exactly.

#### Solution

The code is the seeded heap, the replace-the-weakest loop, and the
pop-and-reverse finish from the walkthrough, using `heapq` for the bounded
priority queue.

```python
import heapq
from typing import List


class Solution:
    def solve(self, nums: List[int], k: int) -> List[int]:
        counts = {}
        for num in nums:
            counts[num] = counts.get(num, 0) + 1
        pairs = list(counts.items())
        heap = pairs[:k]
        heapq.heapify(heap)
        for frequency, value in pairs[k:]:
            heapq.heappush(heap, (frequency, value))
            heapq.heappop(heap)
        winners = [heapq.heappop(heap) for _ in range(k)]
        return [value for _, value in reversed(winners)]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log k)`

Counting is `O(n)`. Heapifying `k` pairs is `O(k)`, each of the `m - k`
remaining pairs costs one `O(log k)` push-pop, and the final `k` pops add
`O(k log k)`, for `O(n log k)` overall.

##### Space Complexity: `O(n)`

The count map holds `O(m)` entries and the heap is capped at `k`, so the
count map dominates at `O(n)` worst case.

#### Key Insights

- A bounded heap converts "sort everything" into "keep the best k", dropping
  the log factor from `log n` to `log k`.
- A min-heap of winners tracks the weakest winner at the root, which is the
  only member a newcomer must beat; losers are discarded in a single
  comparison instead of being sorted.
- When `k` is small relative to `n`, this beats the sort substantially; when
  `k` approaches the number of distinct values, the two converge.

### Bucket Sort

#### Derivation

Both earlier approaches pay a log factor to order candidates against each
other, yet the frequencies themselves impose a free order: a value's
frequency is an integer between `1` and `n`, the length of the input. Values
can therefore be filed into an array of `n + 1` frequency slots, where slot
`f` lists every value occurring exactly `f` times, and scanning the slots
from index `n` down collects the winners in descending frequency without a
single comparison. This is [bucket sort](https://en.wikipedia.org/wiki/Bucket_sort)
with frequency as the bucket index:

1. Build `counts` as before.
2. Create `buckets`, an array of `n + 1` empty lists.
3. For each `(value, frequency)` pair in `counts`, append `value` to
   `buckets[frequency]`.
4. Scan `buckets` from the last index down to `1`, collecting values into
   `winners` until it holds `k` entries.
5. Return `winners`.

#### Walkthrough

Trace the bucketing on Example 1: `nums = [1,1,1,2,2,3]`, `k = 2`. With
`n = 6`, `buckets` has indices `0` through `6`, and the counts
`{1: 3, 2: 2, 3: 1}` fill three slots:

```text
buckets = [[], [3], [2], [1], [], [], []]
   index:  0    1    2    3
```

The scan walks indices `6, 5, 4, 3, 2, ...` and collects as it goes:

```text
index 6, 5, 4   empty
index 3         take 1      winners = [1]
index 2         take 2      winners = [1, 2]   len(winners) == k -> stop
```

The collected `[1, 2]` holds the `k = 2` winners in descending-frequency
order, matching the expected Output exactly.

#### Solution

The code is the fill-and-scan from the walkthrough, with an early return the
moment `k` winners are gathered.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int], k: int) -> List[int]:
        counts = {}
        for num in nums:
            counts[num] = counts.get(num, 0) + 1
        buckets = [[] for _ in range(len(nums) + 1)]
        for num, frequency in counts.items():
            buckets[frequency].append(num)
        winners = []
        for frequency in range(len(buckets) - 1, 0, -1):
            for num in buckets[frequency]:
                winners.append(num)
                if len(winners) == k:
                    return winners
        return winners
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Counting is `O(n)`, filing the `m` distinct values is `O(m)`, and the scan
visits at most `n + 1` slots and `m` values. No pass ever compares two
values.

##### Space Complexity: `O(n)`

The count map and the `n + 1` bucket slots are both linear in the input
length.

#### Key Insights

- Bounding a value (a frequency lies in `1..n`) converts a comparison sort
  into index addressing, and with it `O(n log n)` becomes `O(n)`.
- The early return skips the empty high-frequency slots for free.
- The same trick applies to any selection problem whose scores are small
  bounded integers.

### Counter Most Common

#### Derivation

Counting and top-`k` selection are both standard bookkeeping, and Python's
standard library performs them together: [`Counter`](https://docs.python.org/3/library/collections.html#collections.Counter)
tallies the array in one call, and its `most_common(k)` returns the `k`
highest-count entries ordered by descending count. The two stages of every
solution above collapse into a single line whose internals are the
tally-plus-selection this page has already derived by hand:

1. Build `Counter(nums)`.
2. Return the values of `most_common(k)`.

#### Walkthrough

Trace the two calls on Example 1: `nums = [1,1,1,2,2,3]`, `k = 2`. Here
`Counter` and `most_common` are themselves the technique:

```text
Counter([1,1,1,2,2,3])        -> {1: 3, 2: 2, 3: 1}
.most_common(2)               -> [(1, 3), (2, 2)]
values                        -> [1, 2]
```

The returned `[1, 2]` matches the expected Output exactly, because
`most_common` already orders by descending count.

#### Solution

```python
from collections import Counter
from typing import List


class Solution:
    def solve(self, nums: List[int], k: int) -> List[int]:
        return [value for value, _ in Counter(nums).most_common(k)]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log k)`

Counting is `O(n)`, and `most_common(k)` maintains a `k`-element heap over
the `m` distinct values, costing `O(m log k)`.

##### Space Complexity: `O(n)`

The counter and the returned list hold `O(m)` entries.

#### Key Insights

- The most concise solution: tally, selection, and ordering in one standard
  library call.
- Internally it is the Min-Heap of Size K approach, so it inherits that
  approach's `O(n log k)` bound.
- Reaching for `most_common` is idiomatic Python; the hand-rolled Bucket Sort
  above is what makes its guarantees explainable in an interview.

## Comparison of Solutions

### Time Complexity

- **Count and Sort**: `O(n log n)` - sorting all `m` distinct values
  dominates.
- **Min-Heap of Size K**: `O(n log k)` - one bounded push-pop per distinct
  value.
- **Bucket Sort**: `O(n)` - counting, filing, and scanning, with no
  comparisons.
- **Counter Most Common**: `O(n log k)` - the heap approach inside one
  library call.

### Space Complexity

- **Count and Sort**: `O(n)` - count map plus sorted distinct list.
- **Min-Heap of Size K**: `O(n)` - count map plus a heap capped at `k`.
- **Bucket Sort**: `O(n)` - count map plus `n + 1` frequency slots.
- **Counter Most Common**: `O(n)` - the counter plus the returned list.

### Trade-offs

- **Count and Sort** is the clearest to write and verify, but pays for
  ordering values nobody asked about.
- **Min-Heap of Size K** bounds its extra structure at `k`, which shines when
  `k` is small next to `n`.
- **Bucket Sort** is asymptotically optimal and comparison-free, at the price
  of an `n + 1` slot array even when only a few frequencies occur.
- **Counter Most Common** is the fewest characters of code and the easiest to
  maintain in Python.

### When to Use Each

- **Count and Sort**: the interview warm-up before tightening, or quick
  scripts where input sizes are small.
- **Min-Heap of Size K**: streaming or huge inputs where `k` is small and
  candidates should be inspected once.
- **Bucket Sort** (recommended here): the optimal answer over in-memory
  integer arrays.
- **Counter Most Common**: idiomatic Python one-offs where clarity beats
  micro-optimization.

### Optimization Notes

- The frequency bound `1 <= frequency <= n` is the entire idea behind Bucket
  Sort; missing it makes the linear approach look impossible.
- All approaches share the same counting pass, so interviews usually grade
  the second stage: know why a heap beats a sort, and why buckets beat a
  heap, here.
- The Min-Heap solution pops and reverses at the end to hand back the
  winners in descending-frequency order; the order itself costs only
  `O(k log k)`.
- When frequencies tie at the cut boundary, several winner sets are valid;
  the heap tuples break such ties by value, so the code is deterministic.
