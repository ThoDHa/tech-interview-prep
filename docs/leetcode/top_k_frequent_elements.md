# [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)

**Medium** | **25 minutes** | **Array, Hash Table, Divide and Conquer, Sorting, Heap (Priority Queue), Bucket Sort, Counting, Quickselect**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md), [Heap / Priority Queue](../patterns/heap/intuition.md)

**Algorithm:** [Hash table](https://en.wikipedia.org/wiki/Hash_table) · [Heap (data structure)](https://en.wikipedia.org/wiki/Heap_(data_structure)) · [Bucket sort](https://en.wikipedia.org/wiki/Bucket_sort) · [Sorting](https://en.wikipedia.org/wiki/Sorting_algorithm)

**Practice:** [`practice/leetcode/top_k_frequent_elements/solution.py`](../../practice/leetcode/top_k_frequent_elements/solution.py)

Given an integer array `nums` and an integer `k`, return the `k` most frequent elements within the array.

The test cases are generated such that the answer is always **unique**.

You may return the output in **any order**.

## Examples

### Example 1

**Input:** `nums = [1,2,2,3,3,3], k = 2`

**Output:** `[2,3]`

### Example 2

**Input:** `nums = [7,7], k = 1`

**Output:** `[7]`

## Constraints

- `1 <= nums.length <= 10^4`.
- `-1000 <= nums[i] <= 1000`
- `1 <= k <= number of distinct elements in nums`.

## Deriving the Solution

Selection by frequency decomposes into two stages that can be optimized separately: tally how often each value occurs, then choose the `k` highest tallies. Every solution below counts in one linear pass and differs only in how the second stage selects the winners.

1. **Start literal.** Take the winners one at a time: each of the `k` rounds scans every remaining count for the highest and deletes its value, costing `O(n + k * m)` for `m` distinct values: see [Repeated Maximum Scan](#repeated-maximum-scan).
2. **Order once instead of rescanning.** Re-finding every winner from scratch is the scan's waste; one descending ranking of the `m` distinct values answers all `k` rounds, with the ranking handed to the language's sort at `O(m log m)`: see [Count and Sort](#count-and-sort).
3. **Keep only the winners.** A min-heap of size `k` holds the current top `k` as values stream past: a value beats the heap's minimum or is discarded. Each of the `m` values costs one bounded `O(log k)` push or pop: see [Min-Heap of Size K](#min-heap-of-size-k).
4. **Exploit the frequency bound.** A value's frequency can never exceed `n`, so the distinct values drop into `n + 1` frequency slots and reading the slots from high to low collects the winners in plain linear time, `O(n)`: see [Bucket Sort](#bucket-sort).
5. **Library shortcut last.** `Counter.most_common(k)` performs both stages, tally and top-`k` selection, in one call: see [Counter Most Common](#counter-most-common).

## Solutions

### Repeated Maximum Scan

#### Derivation

The most direct selection takes the winners one at a time. With the counts in hand, the highest-frequency value is found by scanning every entry once; removing it and repeating `k` times peels off the `k` winners in descending frequency order, ties in any order. No ordering of the losers ever happens, because each round only asks for the single best remaining entry:

1. Build `counts`, a dictionary mapping each value in `nums` to its frequency.
2. Repeat `k` times: scan `counts` for the entry with the highest frequency, tracking it in `best_value` and `best_freq`.
3. Append `best_value` to `top` and delete its entry from `counts`, so later rounds cannot take it again.
4. Return `top`.

#### Walkthrough

Trace the rounds on Example 1: `nums = [1,2,2,3,3,3]`, `k = 2`. The counting pass tallies one value at a time:

```text
value 1   counts = {1: 1}
value 2   counts = {1: 1, 2: 1}
value 2   counts = {1: 1, 2: 2}
value 3   counts = {1: 1, 2: 2, 3: 1}
value 3   counts = {1: 1, 2: 2, 3: 2}
value 3   counts = {1: 1, 2: 2, 3: 3}
```

Each selection round scans every surviving entry and removes its winner:

```text
round 1   scan {1: 1, 2: 2, 3: 3}   best_value = 3, best_freq = 3   top = [3]
round 2   scan {1: 1, 2: 2}         best_value = 2, best_freq = 2   top = [3, 2]
```

The rounds return `[3, 2]`, which is the expected Output `[2, 3]` in descending-frequency order, and the any-order contract accepts either. Example 2, `nums = [7,7]`, `k = 1`, finishes in one round: the scan of `{7: 2}` picks `7` and the function returns `[7]`.

#### Solution

The code is the counting pass and the scan-and-remove rounds from the walkthrough.

```python
from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counts = {}
        for num in nums:
            counts[num] = counts.get(num, 0) + 1
        top = []
        for _ in range(k):
            best_value = None
            best_freq = 0
            for value, freq in counts.items():
                if freq > best_freq:
                    best_value = value
                    best_freq = freq
            top.append(best_value)
            del counts[best_value]
        return top
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + k * m)`

Counting is `O(n)`. With `m` distinct values, each of the `k` rounds scans every surviving count once, adding `O(k * m)`. In the worst case, where `k` reaches `m` and `m` reaches `n`, the rounds degrade to `O(n^2)`.

##### Space Complexity: `O(n)`

The dictionary holds `O(m) <= O(n)` entries and the output holds `k`.

#### Key Insights

- The winners can be peeled off one at a time with nothing but scans: selecting the best `k` never requires ordering the losers.
- Deleting each winner as it is taken keeps the later rounds honest at no extra cost.
- The price is repetition: every round pays for a full scan even though the pool shrank by one, which is the flaw the next approach repairs.

### Count and Sort

#### Derivation

The repeated scan re-finds each winner from scratch: `k` rounds cost `k * m` comparisons over the counts, even though a single ordering of the `m` distinct values would settle every round at once. That ordering is mechanical bookkeeping, so this approach hands the ranking to the language's sort. Once every distinct value carries its frequency, sorting the distinct values by that frequency, highest first, lines the winners up at the front of the list:

1. Build `counts`, a dictionary mapping each value in `nums` to its frequency.
2. Collect the distinct values and let `sorted` rank them by `counts[value]`, descending.
3. Slice the first `k` entries off the sorted list and return them.

#### Walkthrough

Trace the ranking on Example 1: `nums = [1,2,2,3,3,3]`, `k = 2`, where the counting pass traced above has left `counts = {1: 1, 2: 2, 3: 3}`. Sorting the distinct values by descending frequency orders them `[3, 2, 1]` (frequencies `3, 2, 1`), and the slice `[3, 2][:2]` returns `[3, 2]`. The expected Output lists `[2, 3]`; the two differ only by the allowed reordering, since any order of the `k` winners is accepted.

#### Solution

The code is the tally, the frequency sort, and the slice.

```python
from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counts = {}
        for num in nums:
            counts[num] = counts.get(num, 0) + 1
        distinct = sorted(counts, key=counts.get, reverse=True)
        return distinct[:k]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Counting is `O(n)`. With `m` distinct values (`m <= n`), the sort costs `O(m log m)`, which is `O(n log n)` at worst.

##### Space Complexity: `O(n)`

The dictionary and the sorted distinct list hold `O(m) <= O(n)` entries.

#### Key Insights

- The two-stage structure, count then select, is shared by every approach in this file.
- Sorting all distinct values does more work than the problem asks for: the bottom `m - k` values are ordered with nobody looking.
- Delegating the ranking to `sorted` makes the selection a one-liner once the counts exist, but it pays the full `O(m log m)` ordering even when `k` is small.

### Min-Heap of Size K

#### Derivation

The sort's waste is that it fully orders all `m` candidates. The selection-only alternative keeps a [heap](https://en.wikipedia.org/wiki/Priority_queue) holding the best `k` values seen so far, ordered so its root is the *weakest* of the current winners. Each candidate then faces exactly one comparison: beat the root and replace it, or leave. Because the heap never grows past `k`, every heap operation costs `O(log k)` regardless of `n`:

1. Build `counts` as before.
2. Seed a min-heap with the first `k` `(frequency, value)` pairs from `counts`.
3. For each remaining `(frequency, value)` pair, push it and pop the minimum, so the heap always holds the `k` strongest.
4. Return the values inside the heap.

Using `(frequency, value)` tuples keeps the comparison on frequency first; the value breaks ties only when frequencies are equal, and per the problem guarantee the top-`k` set is unique, so tie order never changes the answer.

#### Walkthrough

Trace the heap on Example 1: `nums = [1,2,2,3,3,3]`, `k = 2`. After counting, the pairs are `(1, 1)`, `(2, 2)`, `(3, 3)`. The first `k` pairs seed the heap:

```text
seed   heap = [(1, 1), (2, 2)]        root (1, 1) is the weakest winner
(3,3)  push -> [(1,1), (2,2), (3,3)]
       pop minimum (1, 1)
       heap = [(2, 2), (3, 3)]        root (2, 2) is now the weakest
```

The heap ends holding `(3, 3)` and `(2, 2)`, whose values are `[3, 2]`. That is Example 1's winners `[2, 3]` in a different order, which the any-order contract accepts. Example 2, `nums = [7,7]`, `k = 1`, never enters the replacement branch: the single pair `(2, 7)` seeds the heap and its value `[7]` is returned unchanged.

#### Solution

The code is the seeded heap and the replace-the-weakest loop from the walkthrough, using `heapq` for the bounded priority queue.

```python
import heapq
from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counts = {}
        for num in nums:
            counts[num] = counts.get(num, 0) + 1
        pairs = list(counts.items())
        heap = pairs[:k]
        heapq.heapify(heap)
        for freq, value in pairs[k:]:
            heapq.heappush(heap, (freq, value))
            heapq.heappop(heap)
        return [value for _, value in heap]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log k)`

Counting is `O(n)`. Heapifying `k` pairs is `O(k)`, and each of the `m - k` remaining pairs costs one `O(log k)` push-pop, for `O(n log k)` overall.

##### Space Complexity: `O(n)`

The count map holds `O(m)` entries and the heap is capped at `k`, so the count map dominates at `O(n)` worst case.

#### Key Insights

- A bounded heap converts "sort everything" into "keep the best k", dropping the log factor from `log n` to `log k`.
- A min-heap of winners tracks the weakest winner at the root, which is the only member a newcomer must beat.
- When `k` is small relative to `n`, this beats the sort substantially; when `k` approaches `n`, the two converge.

### Bucket Sort

#### Derivation

The sort and the heap both pay a log factor to order candidates against each other, yet the frequencies themselves impose a free order: a frequency is an integer between `1` and `n`, the length of the input. Values can therefore be filed into an array of `n + 1` frequency slots, where slot `f` lists every value occurring exactly `f` times, and scanning the slots from index `n` down collects the winners in descending frequency without a single comparison. This is [bucket sort](https://en.wikipedia.org/wiki/Bucket_sort) with frequency as the bucket index:

1. Build `counts` as before.
2. Create `buckets`, an array of `n + 1` empty lists.
3. For each `(value, frequency)` pair in `counts`, append `value` to `buckets[frequency]`.
4. Scan `buckets` from the last index down to `1`, collecting values into `top` until it holds `k` entries.
5. Return `top`.

#### Walkthrough

Trace the bucketing on Example 1: `nums = [1,2,2,3,3,3]`, `k = 2`. With `n = 6`, `buckets` has indices `0` through `6`, and the counts `{1: 1, 2: 2, 3: 3}` fill three slots:

```text
buckets = [[], [1], [2], [3], [], [], []]
   index:  0   1    2    3
```

The scan walks indices `6, 5, 4, 3, 2, ...` and collects as it goes:

```text
index 6, 5, 4   empty
index 3         take 3      top = [3]
index 2         take 2      top = [3, 2]   len(top) == k -> stop
```

The collected `[3, 2]` holds Example 1's `k = 2` winners, matching the expected Output `[2, 3]` up to reordering.

#### Solution

The code is the fill-and-scan from the walkthrough, with an early return the moment `k` winners are gathered.

```python
from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counts = {}
        for num in nums:
            counts[num] = counts.get(num, 0) + 1
        buckets = [[] for _ in range(len(nums) + 1)]
        for num, freq in counts.items():
            buckets[freq].append(num)
        top = []
        for freq in range(len(buckets) - 1, 0, -1):
            for num in buckets[freq]:
                top.append(num)
                if len(top) == k:
                    return top
        return top
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Counting is `O(n)`, filing the `m` distinct values is `O(m)`, and the scan visits at most `n + 1` slots and `m` values. No pass ever compares two values.

##### Space Complexity: `O(n)`

The count map and the `n + 1` bucket slots are both linear in the input length.

#### Key Insights

- Bounding a value (frequency is in `1..n`) converts a comparison sort into index addressing, and with it `O(n log n)` becomes `O(n)`.
- The early return skips the empty high-frequency slots for free.
- The same trick applies to any problem whose scores are small bounded integers.

### Counter Most Common

#### Derivation

Counting and top-`k` selection are both standard bookkeeping, and Python's standard library performs them together: [`Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) tallies the array in one call, and its `most_common(k)` returns the `k` highest-count entries, ordered by descending count. The two stages of every solution above collapse into a single line whose internals are the tally-plus-selection this file has already derived by hand:

1. Build `Counter(nums)`.
2. Return the values of `most_common(k)`.

#### Walkthrough

Trace the two calls on Example 1: `nums = [1,2,2,3,3,3]`, `k = 2`. Here `Counter` and `most_common` are themselves the technique:

```text
Counter([1,2,2,3,3,3])        -> {3: 3, 2: 2, 1: 1}
.most_common(2)               -> [(3, 3), (2, 2)]
values                        -> [3, 2]
```

The returned `[3, 2]` is Example 1's winner set `[2, 3]` in descending-frequency order, which the any-order contract accepts. Example 2, `nums = [7,7]`, `k = 1`, yields `Counter({7: 2}).most_common(1) = [(7, 2)]`, so the values are `[7]`, matching the expected Output exactly.

#### Solution

```python
from collections import Counter
from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        return [value for value, _ in Counter(nums).most_common(k)]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log k)`

Counting is `O(n)`, and `most_common(k)` maintains a `k`-element heap over the `m` distinct values, costing `O(m log k)`.

##### Space Complexity: `O(n)`

The counter and the returned list hold `O(m)` entries.

#### Key Insights

- The most concise solution: tally, selection, and ordering in one standard library call.
- Internally it is the Min-Heap of Size K approach, so it inherits that approach's `O(n log k)` bound.
- Reaching for `most_common` is idiomatic Python; the hand-rolled Bucket Sort above is what makes its guarantees explainable in an interview.

## Comparison of Solutions

### Time Complexity

- **Repeated Maximum Scan**: `O(n + k * m)` - `k` rounds, each a full scan of the surviving counts.
- **Count and Sort**: `O(n log n)` - sorting all `m` distinct values dominates.
- **Min-Heap of Size K**: `O(n log k)` - one bounded push-pop per distinct value.
- **Bucket Sort**: `O(n)` - counting, filing, and scanning, with no comparisons.
- **Counter Most Common**: `O(n log k)` - the heap approach inside one library call.

### Space Complexity

- **Repeated Maximum Scan**: `O(n)` - the count map plus the `k` winners.
- **Count and Sort**: `O(n)` - count map plus sorted distinct list.
- **Min-Heap of Size K**: `O(n)` - count map plus a heap capped at `k`.
- **Bucket Sort**: `O(n)` - count map plus `n + 1` frequency slots.
- **Counter Most Common**: `O(n)` - the counter plus the returned list.

### Trade-offs

- **Repeated Maximum Scan** needs nothing beyond scans and a dictionary, but every winner costs a full pass over the surviving counts.
- **Count and Sort** is the clearest to write and verify, but pays for ordering values nobody asked about.
- **Min-Heap of Size K** bounds its extra structure at `k`, which shines when `k` is small next to `n`.
- **Bucket Sort** is asymptotically optimal and comparison-free, at the price of an `n + 1` slot array even when only a few frequencies occur.
- **Counter Most Common** is the fewest characters of code and the easiest to maintain in Python.

### When to Use Each

- **Repeated Maximum Scan**: tiny `k` over large distinct sets, or as the hand-rolled warm-up before any ordering machinery.
- **Count and Sort**: quick scripts, small inputs, or when the full descending ranking is wanted anyway and `k` is not far below `m`.
- **Min-Heap of Size K**: streaming or huge inputs where `k` is small and candidates should be inspected once.
- **Bucket Sort**: the optimal answer over in-memory integer arrays (recommended here).
- **Counter Most Common**: idiomatic Python one-offs where clarity beats micro-optimization.

### Optimization Notes

- The frequency bound `1 <= frequency <= n` is the entire idea behind Bucket Sort; missing it makes the linear approach look impossible.
- All approaches share the same counting pass, so interviews usually grade the second stage: know why heap beats sort, and why buckets beat heap, here.
- The scan's `k * m` comparisons beat the sort's `m log m` only while `k < log m`; that crossover is why the ordering approaches take over as `k` grows.
- For the unique-answer guarantee, tie-breaking inside the scan, heap, or library call can never change the selected *set*, only its order, which the any-order contract already forgives.
