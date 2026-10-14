# [Kth Largest Element In An Array](https://leetcode.com/problems/kth-largest-element-in-an-array/)

**Medium** | **25 minutes** | **Array, Divide and Conquer, Sorting, Heap (Priority Queue), Quickselect**

**Pattern:** [Heap / Priority Queue](../patterns/heap/intuition.md)

**Algorithm:** [Quickselect](https://en.wikipedia.org/wiki/Quickselect) · [Heap (data structure)](https://en.wikipedia.org/wiki/Heap_(data_structure)) · [Sorting](https://en.wikipedia.org/wiki/Sorting_algorithm)

**Practice:** [`practice/kth_largest_element_in_an_array/solution.py`](../../practice/kth_largest_element_in_an_array/solution.py)

Given an unsorted array of integers `nums` and an integer `k`, return the `kth` largest element in the array.

By `kth` largest element, we mean the `kth` largest element in the sorted order, not the `kth` distinct element.

Follow-up: Can you solve it without sorting?

## Examples

### Example 1

**Input:** `nums = [2,3,1,5,4]`, `k = 2`

**Output:** `4`

**Explanation:** The elements sorted in descending order are `[5,4,3,2,1]`; the element at rank `k = 2` is `4`.

### Example 2

**Input:** `nums = [2,3,1,1,5,5,4]`, `k = 3`

**Output:** `4`

**Explanation:** The elements sorted in descending order are `[5,5,4,3,2,1,1]`; the two `5`s occupy ranks `1` and `2`, and because duplicates count toward the rank rather than being skipped, rank `k = 3` falls to `4`.

## Constraints

- `1 <= k <= nums.length <= 10000`
- `-1000 <= nums[i] <= 1000`

## Deriving the Solution

Every solution must answer one question: which value would sit at index `target = n - k` if `nums` were sorted ascending, where `n = len(nums)`? Rank `k` counting from the top and index `target` counting from the bottom are the same element, and `target` never depends on the values, only on `n` and `k`. The solutions differ only in how much ordering they build to read that one slot.

1. **Start literal.** "The `kth` largest" invites extracting the maximum,
   removing it, and repeating `k - 1` more times. Correct, but every round rescans the whole array, costing `O(n * k)`: see [Brute Force](#brute-force).
2. **Settle every rank at once.** The repeated scans keep re-deriving rank
   information that one pass could store. Sorting buys every rank in `O(n log n)`, the answer sitting at index `n - k`: see [Sorting](#sorting). The values here live in a band of only `r = 2001` possible values (`-1000 <= nums[i] <= 1000`), so a tally of one counter per value holds every rank without comparing anything, in `O(n + r)`: see [Counting Tally](#counting-tally).
3. **Heapify the repeated maximum.** The brute force rescans because a plain
   array cannot yield its maximum cheaply twice in a row. A min-heap of the `k` largest candidates keeps the answer on top and admits each newcomer in `O(log k)`, for `O(n log k)` total: see [Min-Heap of Size K](#min-heap-of-size-k).
4. **Order nothing but the boundary.** Even the heap spends `log k` per element
   maintaining order inside the candidate set, order the answer never needs: rank `k` is a single position. Quicksort's partition places one element at its final sorted index, so aiming it at `target` narrows only the side containing the answer, reaching `O(n)` average time: see [Quickselect](#quickselect).
5. **Let the library run the bounded heap.** The capped heap of step 3 is a
   standard shape, and `heapq.nlargest` implements it with the same orientation, absorbing the size test, the gatekeeper comparison, and the `heapreplace` call into one line that hands back the candidates ordered: see [Library One-Liner with `heapq.nlargest`](#library-one-liner-with-heapqnlargest).

## Solutions

### Brute Force

#### Derivation

The most literal reading of "kth largest" is to extract it by hand: the largest element is the `1st` largest, so removing the maximum `k - 1` times leaves the `kth` largest on top of what remains. No sort, no heap, no bookkeeping beyond a removal per round; the question this approach asks is only "where is the current maximum?":

1. Repeat `k - 1` times: scan `nums` for the largest value, then remove one
   occurrence of it.
2. Scan `nums` once more; the largest value left in the array is the `kth`
   largest overall.
3. Return that value. Each round shrinks the array by one, so exactly `k`
   scans run in total.

#### Walkthrough

Trace the repeated-maximum extraction on Example 1: `nums = [2,3,1,5,4]`, `k = 2`. One removal round runs first, then the final scan reads the answer:

```text
round 1   scan [2,3,1,5,4] -> max 5   remove one 5 -> [2,3,1,4]
round 2   scan [2,3,1,4]   -> max 4   that is the kth largest
```

Round 1 pulls the maximum `5` out of the array. The second scan runs over the four survivors, finds `4` on top, and there is nothing left to remove: the answer is `4`, matching the expected Output for Example 1. With `k = 2` only two scans were needed; the cost is the full rescan per removed element.

#### Solution

The code is the walkthrough written down: `k - 1` scan-and-remove rounds, then one final scan through `largest` for the survivor.

```python
from typing import List


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        remaining = list(nums)
        # Remove the maximum k - 1 times; the kth max is then on top.
        for _ in range(k - 1):
            largest = max(remaining)
            remaining.remove(largest)
        return max(remaining)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * k)`

Each of the `k` rounds scans all `n` remaining elements (`max` walks the whole list, and so does `remove`), so the total work is `O(n * k)`. When `k` approaches `n` this degrades to `O(n^2)`.

##### Space Complexity: `O(n)`

The working copy `remaining` duplicates the input so the caller's list is left intact; the loop indices add nothing.

#### Key Insights

- The approach never orders anything: it answers rank queries by destroying
   lower ranks one at a time, which is the most direct expression of the definition.
- The waste is the rescan: each round re-examines every survivor to re-learn
   information (the running maximum) that a better structure could maintain incrementally.
- `k = 1` degenerates to a single maximum scan, the cheapest case; the approach
   is only painful when `k` grows toward `n`.

### Counting Tally

#### Derivation

The brute force keeps re-deriving rank information because it never records anything between rounds. The values themselves invite a record: the constraint `-1000 <= nums[i] <= 1000` confines every value to a band of `2001` integers, so one counter per possible value fits in a flat array. Counting sorts answer rank queries without any comparison at all: the number of values greater than `v` is exactly the tally of counters above `v`'s slot, so walking the counters from highest value down and subtracting counts from `k` reaches the counter where the cumulative count first reaches `k`, and that counter's value is the answer:

1. Build `count` with one slot per value in `[-1000, 1000]`; increment
   `count[num + 1000]` for every `num` in `nums`.
2. Walk `value` from `1000` down to `-1000`. Maintain `remaining = k`, and
   subtract each nonzero counter from it as its slot passes.
3. The first `value` whose counter drops `remaining` to `0` or below is the
   `kth` largest: return it.

Duplicates are handled by arithmetic rather than logic: a counter of `3` consumes three ranks at once, which is exactly the "duplicates count toward the rank" rule.

#### Invariant

The downward walk preserves a rank-budget invariant:

```text
before examining slot `value`:  remaining == k - (number of elements > value)
```

Each branch preserves it: skipping a zero counter removes nothing from the array, so the count of greater elements is unchanged; subtracting a nonzero `count[value]` removes exactly those elements from the "greater" side as `value` becomes the candidate itself. At loop exit, when `remaining <= 0` first holds, the elements greater than `value` number fewer than `k`, and the elements `>= value` number at least `k`: exactly the defining property of the `kth` largest, so `value` is the answer.

#### Walkthrough

Trace the downward walk on Example 2: `nums = [2,3,1,1,5,5,4]`, `k = 3`. The nonzero counters, drawn at their values, are:

```text
value    5  4  3  2  1
count    2  1  1  1  2     remaining = k = 3
```

The walk starts at the top of the band and stops at the first slot that exhausts the budget:

```text
value=5  count=2  remaining: 3 - 2 = 1    not <= 0 -> keep walking
value=4  count=1  remaining: 1 - 1 = 0    <= 0 -> answer is 4
```

Subtracting the two `5`s leaves `remaining = 1`: one rank is still owed, and the next counter holds exactly one `4`, which pays it off. The walk returns `4`, matching the expected Output for Example 2. The same trace shows why duplicates need no special case: had `k = 1`, the very first counter (`2` fives) would drop `remaining` to `-1` and still return `5`.

#### Solution

The code is the tally plus the budgeted downward walk: increment one slot per element, then spend `remaining` from the top of the band.

```python
from typing import List


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        MIN_VALUE, MAX_VALUE = -1000, 1000
        # Slot value - MIN_VALUE counts occurrences of that value.
        count = [0] * (MAX_VALUE - MIN_VALUE + 1)
        for num in nums:
            count[num - MIN_VALUE] += 1

        remaining = k
        for value in range(MAX_VALUE, MIN_VALUE - 1, -1):
            if count[value - MIN_VALUE] == 0:
                continue
            remaining -= count[value - MIN_VALUE]
            if remaining <= 0:
                return value
        raise ValueError("unreachable: k <= len(nums) guarantees a slot answers")
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + r)`

Counting is one pass over `n` elements, and the walk visits `r = 2001` slots regardless of `n`. With the constraint's fixed band this is linear time; the `r` term is why the approach is unusable when the value range is wide or unbounded.

##### Space Complexity: `O(r)`

The tally holds one integer per value in the band, `2001` counters, independent of `n`.

#### Key Insights

- A narrow value range turns a selection problem into a counting problem:
   the tally stores every rank simultaneously, so no per-round recomputation is possible.
- Duplicates cost nothing: a counter of `c` consumes `c` ranks in one
   subtraction, encoding the "not distinct" rule arithmetically.
- The trade is the band: `O(r)` time and space are constants here, but the
   same code breaks if the values span `10^9`, which is when heap and Quickselect take over.

### Min-Heap of Size K

#### Derivation

The brute force rescans because a plain array gives up its maximum only to a full search. A [heap](https://en.wikipedia.org/wiki/Heap_(data_structure)) is the structure that maintains "the extreme of a changing set" permanently: keep the `k` largest candidates seen so far in a min-heap, and the `kth` largest of everything seen is always the smallest of the candidates, sitting at `heap[0]`. Each new element either loses to the current gatekeeper or evicts it. Python's `heapq` is a min-heap, which is exactly the orientation needed when keeping the largest:

1. Push the first `k` elements of `nums` onto `heap` unchanged.
2. For each remaining element `num`: if `num > heap[0]`, the newcomer beats
   the weakest current candidate, so `heapreplace` swaps it in; otherwise skip it.
3. After the sweep, `heap[0]` is the smallest of the `k` largest elements,
   which is the `kth` largest overall: return it.

The heap is capped at `k`, so every heap operation costs `O(log k)` no matter how large `n` grows.

#### Walkthrough

Trace the bounded sweep on Example 2: `nums = [2,3,1,1,5,5,4]`, `k = 3`. The first three elements seed the heap; every later element tests itself against `heap[0]`, the weakest candidate:

```text
seed [2,3,1]        heap = [1, 3, 2]        (min-heap: 1 on top)
num=1   1 > 1? no   heap unchanged = [1, 3, 2]
num=5   5 > 1? yes  heapreplace -> heap = [2, 3, 5]
num=5   5 > 2? yes  heapreplace -> heap = [3, 5, 5]
num=4   4 > 3? yes  heapreplace -> heap = [4, 5, 5]
```

Each `heapreplace` evicts the root (the weakest of the top-`k` candidates) and sifts the newcomer down to its place, exactly the list states shown above. After the last element the heap holds `{4, 5, 5}`, the three largest values of the array, and its root `heap[0] = 4` is the smallest of them: the `3rd` largest, matching the expected Output for Example 2. Note that the final `4` replaced the root `3`: only the gatekeeper ever needs to be consulted, never the rest of the heap.

#### Solution

The code is the walkthrough's seed-then-gate sweep: `k` pushes, then one comparison and possible `heapreplace` per remaining element.

```python
import heapq
from typing import List


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap: List[int] = []
        for num in nums:
            if len(heap) < k:
                heapq.heappush(heap, num)
            elif num > heap[0]:
                # Newcomer beats the weakest of the k largest so far.
                heapq.heapreplace(heap, num)
        return heap[0]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log k)`

Each of the `n` elements triggers at most one heap push or replace, and every heap operation costs `O(log k)` because the heap never exceeds `k` entries. When `k` is small relative to `n` this approaches linear; at `k = n` it is `O(n log n)`, the same as sorting.

##### Space Complexity: `O(k)`

The heap holds at most `k` elements; nothing else grows with the input.

#### Key Insights

- The min-heap orientation is what makes the cap work: the answer (the `kth`
   largest) is precisely the minimum of the top-`k` set, so the root can be compared against each newcomer in `O(1)` and evicted in `O(log k)`.
- The heap never holds more than `k` elements, so the bound is `O(n log k)`
   rather than `O(n log n)`: the structure remembers the pruning, unlike a full sort.
- This is the approach to reach for when the data streams or `k` is small;
   the same bounded sweep underlies the Kth Largest Element In a Stream problem, where the sweep simply continues forever.

### Quickselect

#### Derivation

The heap pays `O(log k)` per element to keep the candidates internally ordered, yet the answer needs no order at all: rank `k` is one position, `target = n - k` in ascending terms, and the question that matters is only "which value lands at that position?". [Quickselect](https://en.wikipedia.org/wiki/Quickselect) answers exactly that. It reuses quicksort's partition: pick a pivot, sweep the current range gathering every smaller element to its left, and the pivot lands at its final sorted index. Quicksort would then recurse into both sides; Quickselect instead compares the landing index `mid` with `target` and narrows into the single side that contains `target`, discarding the other side entirely. With random pivots, each round expects to shrink the range by a constant fraction, so the expected total work telescopes to `O(n)`:

1. Set `target = len(nums) - k` and search the full range
   `left = 0` to `right = len(nums) - 1`.
2. Draw `pivot_idx` at random in the range, and `partition`: move the pivot to
   the right end, sweep `i` from `left` to `right - 1` gathering smaller values at `store`, then swap the pivot into `store`.
3. The pivot is now sorted-final at `mid = store`. If `mid == target`, the
   search is done; if `mid < target`, continue with `left = mid + 1`; otherwise with `right = mid - 1`.
4. The loop exits when the range collapses onto `target`; return
   `nums[target]`.

Because every partition places one more element at its final index and the range halves in expectation, the loop cannot chase the target forever; the random draw keeps adversarial orderings from forcing the quadratic worst case.

#### Invariant

Each partition round preserves a shrinking-range invariant:

```text
target in [left, right]   and   every index outside [left, right]
                                 already holds its final sorted value
```

Each branch preserves it: the partition proves `nums[mid]` is sorted-final, so if `mid < target` everything at indices `<= mid` is `<= nums[mid]` and `target` must lie in `[mid + 1, right]`; symmetrically for `mid > target`; and `mid == target` exits with `nums[target]` final. At loop exit (`left == right`), the range has collapsed onto the one index `target`, which must therefore hold the `target`-th smallest value: the `kth` largest.

#### Walkthrough

Trace Quickselect on Example 1: `nums = [2,3,1,5,4]`, `k = 2`, so `target = 5 - 2 = 3`. The pivot index is drawn at random, so a hand-trace must fix the draws: suppose the first draw is `pivot_idx = 1` (pivot value `3`; any other draw reaches the same answer, possibly after more rounds).

```text
setup       left=0, right=4, target=3    nums = [2,3,1,5,4]
partition   pivot_idx=1, pivot = 3
            swap nums[1], nums[4] -> [2,4,1,5,3]; store = 0
  i=0       2 < 3 -> swap nums[0], nums[0]; store = 1
  i=1       4 < 3 fails
  i=2       1 < 3 -> swap nums[1], nums[2] -> [2,1,4,5,3]; store = 2
  i=3       5 < 3 fails
            swap nums[4], nums[2] -> [2,1,3,5,4]
            return mid = 2
narrow      mid=2 < target=3 -> left = 3
partition   left=3, right=4, pivot_idx=4, pivot = 4
            swap nums[4], nums[4] (no-op); store = 3
  i=3       5 < 4 fails
            swap nums[4], nums[3] -> [2,1,3,4,5]
            return mid = 3
done        mid=3 == target=3 -> return nums[3] = 4
```

The first partition landed the pivot `3` at its final sorted index `2` with `2, 1` gathered on its left and `5, 4` on its right; since `target = 3` lies to the right, the left half was discarded outright. The second partition proved `4` belongs at index `3`: `mid == target`, so `nums[target] = 4` is the `2nd` largest, matching the expected Output for Example 1. (The final array `[2,1,3,4,5]` is partially sorted as a side effect; only index `3` is guaranteed.)

#### Solution

The code is the walkthrough's partition-and-narrow loop; only the random pivot draws vary from run to run.

```python
import random
from typing import List


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        def partition(left: int, right: int, pivot_idx: int) -> int:
            pivot = nums[pivot_idx]
            # Move the pivot to the end, then gather smaller elements left.
            nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
            store = left
            for i in range(left, right):
                if nums[i] < pivot:
                    nums[store], nums[i] = nums[i], nums[store]
                    store += 1
            nums[right], nums[store] = nums[store], nums[right]
            return store

        left, right = 0, len(nums) - 1
        target = len(nums) - k
        while left < right:
            pivot_idx = random.randint(left, right)
            mid = partition(left, right, pivot_idx)
            if mid == target:
                break
            elif mid < target:
                left = mid + 1
            else:
                right = mid - 1
        return nums[target]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)` average, `O(n^2)` worst case

Each partition is linear over its range, and random pivots shrink the range by a constant fraction in expectation, so the expected work is `n + n/2 + n/4 + ... = O(n)`. A pathological pivot sequence (consistently extreme pivots) degrades to `O(n^2)`, which randomization makes vanishingly unlikely on any fixed input.

##### Space Complexity: `O(1)`

Partitioning happens in place; only a constant number of indices are tracked, and the iterative narrowing avoids recursion. The cost is that `nums` is reordered, so the caller's array does not survive.

#### Key Insights

- The reformulation `target = n - k` converts "kth largest" into "index `n - k`
   ascending", which lets the untouched quicksort machinery aim at the answer directly.
- Quickselect is quicksort with the recursion thrown away: one side of each
   partition is provably irrelevant to the answer and is discarded, which is exactly the saving over `O(n log n)`.
- The random pivot is not decoration: a fixed rule (say, always the rightmost)
   turns an already-sorted array into the quadratic worst case, while the draw makes every input equally cheap in expectation.
- Duplicates are safe here: values equal to the pivot are neither gathered by
   `store` nor lost, they simply flank it, and the target index still resolves because the pivot always lands at one valid final position.

### Sorting

#### Derivation

The brute force keeps paying for re-deriving one rank per scan, yet a single scan that compared every pair of elements would settle every rank at once. That scan is [sorting](https://en.wikipedia.org/wiki/Sorting_algorithm): one `O(n log n)` pass orders the whole array, and the answer is the element `k - 1` steps from the descending end, or equivalently index `n - k` of the ascending result. The full sort does more work than the problem asks, ordering every element when only one position matters, which is exactly the waste Counting Tally and Quickselect exist to remove; the trade is that the code is two lines and impossible to get wrong. The follow-up "can you solve it without sorting?" is answered by every other solution on this page.

1. Sort a copy of `nums` ascending.
2. Return the element at index `len(nums) - k`.

#### Walkthrough

Sorting is the entire technique here, so the trace shows what the sort receives and what the slice reads. On Example 1: `nums = [2,3,1,5,4]`, `k = 2`:

```text
before   nums = [2,3,1,5,4]
sorted   [1,2,3,4,5]          ascending
index    target = 5 - 2 = 3   sorted[3] = 4
```

The sort orders the values `1,2,3,4,5`, and index `n - k = 3` counts `k = 2` steps back from the top: `4`, the expected Output for Example 1. On Example 2 the same arithmetic gives `target = 7 - 3 = 4` into `[1,1,2,3,4,5,5]`, again `4`.

#### Solution

The code is the two steps of the walkthrough: sort, then index from the top.

```python
from typing import List


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        ascending = sorted(nums)
        return ascending[len(nums) - k]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

The comparison sort dominates: every one of the `n` elements participates in `O(n log n)` comparisons, and the final indexing is constant time.

##### Space Complexity: `O(n)`

`sorted` builds a full ordered copy of the input, leaving the caller's list untouched; CPython's Timsort additionally uses a merge buffer of up to `n/2` elements for that copy.

#### Key Insights

- The shortest, least error-prone solution, and the baseline every other
   approach on this page is measured against: with `n <= 10^4` it is fast enough.
- It answers the problem's follow-up in the negative by design: this is the
   "with sorting" option, kept honest next to the approaches that avoid it.
- Indexing `target = n - k` from the ascending end is the whole trick; sorting
   descending and taking `nums[k - 1]` is equivalent.

### Library One-Liner with `heapq.nlargest`

#### Derivation

The Min-Heap of Size K solution is a bounded-heap sweep: hold at most `k` candidates, keep the weakest of them reachable at the root, and evict it whenever a bigger value arrives. [`heapq.nlargest`](https://docs.python.org/3/library/heapq.html#heapq.nlargest) is that sweep, packaged. Handing it the plain values moves the entire mechanism into the library: the `len(heap) < k` seeding branch, the `num > heap[0]` comparison against the weakest candidate, the `heapreplace` call, and the final read of the answer off `heap[0]`. What stays is the single query the problem poses: "give me the `k` largest, ordered descending", whose last element is the answer. (Its mirror `heapq.nsmallest` keeps the `k` smallest; pointing it at this problem, e.g. via `nsmallest(k, nums)[-1]`, silently returns the `kth` smallest instead. The orientation is the bug to avoid.) It also falls back to sorting the whole input when `k` reaches `len(nums)`:

1. Call `heapq.nlargest(k, nums)`, which sweeps `nums` once keeping the `k`
   largest candidates, returned in descending order.
2. Return the last element of that list: the smallest of the `k` largest,
   which is the `kth` largest overall.

The result is deterministic and the input is never mutated.

#### Walkthrough

Trace it on Example 2: `nums = [2,3,1,1,5,5,4]`, `k = 3`. This is the same case the Min-Heap walkthrough traced, and `nlargest` makes the same decisions in the same order, seeding the heap with the first `k` values and then testing each remaining value against the weakest candidate, `heap[0]`:

```text
seed     first k=3 values 2,3,1   heap of candidates = [1, 3, 2]
num=1    1 > heap[0]=1? no        candidates unchanged
num=5    5 > 1? yes               evict 1 -> candidates {2, 3, 5}
num=5    5 > 2? yes               evict 2 -> candidates {3, 5, 5}
num=4    4 > 3? yes               evict 3 -> candidates {4, 5, 5}
sort     survivors ordered        [5, 5, 4]
```

The seeding step fills the candidate set to its cap of `k = 3`, and each later value that beats `heap[0]` evicts it in one balanced operation, exactly the `heapreplace` the Min-Heap section performs by hand. CPython then sorts the three survivors descending before returning them, which is why the output is ordered `[5, 5, 4]`. The call returns `[5, 5, 4][-1] = 4`: the weakest of the three survivors is exactly the `3rd` largest, matching the expected Output for Example 2.

#### Solution

The bounded-candidate sweep, expressed as one library call plus a last-element read.

```python
import heapq
from typing import List


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        return heapq.nlargest(k, nums)[-1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log k)`

Each of the `n` elements has its key compared against the heap's extreme and at worst costs one `O(log k)` replacement, with a final `O(k log k)` sort of the survivors. CPython does not hold to it at the extremes: `k == 1` delegates to a `max` scan (`O(n)`), and `k >= len(nums)` sorts the whole input, making the call `O(n log n)` exactly where the bounded heap would stop paying off anyway.

##### Space Complexity: `O(k)`

The heap holds `k` decorated tuples (key, order, value), and the final sort runs over those same `k` entries; nothing scales with `n` and the input is never mutated.

#### Key Insights

- One line replaces the machinery: `nlargest` absorbs the seed, the
   gatekeeper comparison, and the eviction that the Min-Heap of Size K section performs by hand. Asked how `nlargest` works, that section is the answer you should be able to write from scratch.
- Orientation is the trap: the sibling `heapq.nsmallest` keeps the `k`
   smallest, so `nsmallest(k, nums)[-1]` computes the `kth` smallest, a wrong answer this problem will not flag at runtime. Getting `nlargest` right is the entire exercise.
- Know the fallbacks before claiming the bound: `k == 1` degrades to a `max`
   scan and `k >= n` to a full sort, so the `O(n log k)` advantage exists only while `k` is genuinely small.
- Unlike Quickselect, the input is left unmodified and the result is
   deterministic, which matters when the caller's array must survive.

## Comparison of Solutions

The practice harness's `practice/kth_largest_element_in_an_array/reference.py` implements the **Quickselect** solution.

### Time Complexity

- **Brute Force**: `O(n * k)` - `k` maximum-extraction rounds, each scanning
  all `n` remaining elements.
- **Counting Tally**: `O(n + r)` - one counting pass plus a walk of the
  `r = 2001` value-band slots.
- **Min-Heap of Size K**: `O(n log k)` - one bounded heap operation per element.
- **Quickselect**: `O(n)` average, `O(n^2)` worst case - partition narrows
  toward one index, discarding the other side each round.
- **Sorting**: `O(n log n)` - one comparison sort over all elements.
- **Library One-Liner with `heapq.nlargest`**: `O(n log k)` - the same
  bounded-candidate sweep, falling back to an `O(n log n)` sort when `k` reaches `len(nums)`.

### Space Complexity

- **Brute Force**: `O(n)` - a working copy of the array to remove maxima from.
- **Counting Tally**: `O(r)` - 2001 counters, one per possible value in the
  band.
- **Min-Heap of Size K**: `O(k)` - the heap holds at most `k` candidates.
- **Quickselect**: `O(1)` - partitions the input in place.
- **Sorting**: `O(n)` - `sorted` builds a full ordered copy.
- **Library One-Liner with `heapq.nlargest`**: `O(k)` - `k` decorated tuples
  of key, order, and value, sorted in place at the end.

### Trade-offs

- Brute Force is the most direct translation of the definition (remove the
  maximum `k - 1` times) but rescans the entire array every round.
- Counting Tally is comparison-free and effectively constant-space here, but
  it is chained to the narrow value band: widen the values and the tally stops fitting.
- The Min-Heap of Size K keeps the input untouched and streams gracefully, but
  carries a `log k` factor and `O(k)` extra space to maintain order the answer never reads.
- Quickselect reaches linear average time in constant space but mutates the
  caller's array and carries a (randomization-defused) quadratic worst case.
- Sorting orders every element when only one rank matters, paying for clarity
  with the full `O(n log n)`.
- The `heapq.nlargest` one-liner gets the heap's bound and non-mutating
  behaviour in one line, at the cost of hiding the selection mechanism entirely.

### When to Use Each

- **Brute Force**: As a first intuition or a teaching baseline for tiny `k`;
  too slow to defend at the constraints.
- **Counting Tally**: When the value range is known to be narrow (as the
  constraint here guarantees) and the simplest possible correct pass beats shaving log factors.
- **Min-Heap of Size K** (recommended): The interview default: bounded work,
  no input mutation, no value-range assumptions, and it extends directly to the streaming variant.
- **Quickselect**: When average-case speed is the priority, `O(1)` space
  matters, and mutating the input is acceptable; the follow-up's "without sorting" answer in its strongest form.
- **Sorting**: When `n` is modest and the shortest correct code matters more
  than the log factor.
- **Library One-Liner with `heapq.nlargest`**: The production default for
  small `k` with an intact input; write the Min-Heap version first in an interview, then offer this.

### Optimization Notes

- The rank mirror `target = n - k` is the load-bearing observation: Sorting and
  Quickselect both use it, converting a "largest" question into an ascending-order index.
- The three regimes worth naming: counting wins when values are bounded, the
  heap wins when `k` is small or data streams, Quickselect wins on average when one-shot selection may reorder the input.
- `heapq.nlargest` reaches the hand-written heap's bound with a smaller
  constant, because its comparisons and evictions run in C rather than Python bytecode; but check its fallbacks (`k == 1` becomes `max`, `k >= n` becomes a sort) before quoting `O(n log k)`.
- Quickselect's random pivot is the difference between expected `O(n)` and an
  adversary-sorted `O(n^2)`; deterministic pivoting (first or last element) is the classic trap on this problem.
- For the strict `O(n)` worst case, median-of-medians pivot selection exists,
  but its constants make it a theory answer rather than a practical one.
