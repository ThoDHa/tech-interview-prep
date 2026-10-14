# [Kth Largest Element In a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/)

**Easy** | **15 minutes** | **Tree, Design, Binary Search Tree, Heap (Priority Queue), Binary Tree, Data Stream**

**Pattern:** [Heap / Priority Queue](../patterns/heap/intuition.md)

**Algorithm:** [Heap (data structure)](https://en.wikipedia.org/wiki/Heap_(data_structure)) · [Insertion sort](https://en.wikipedia.org/wiki/Insertion_sort) · [Binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm)

**Practice:** [`practice/kth_largest_element_in_a_stream/solution.py`](../../practice/kth_largest_element_in_a_stream/solution.py)

Design a class to find the `kth` largest integer in a stream of values, including duplicates. E.g. the `2nd` largest from [1, 2, 3, 3] is `3`. The stream is not necessarily sorted.

Implement the following methods:
* `constructor(int k, int[] nums)` Initializes the object given an integer `k` and the stream of integers `nums`.
* `int add(int val)` Adds the integer `val` to the stream and returns the `kth` largest integer in the stream.

## Examples

### Example 1

**Input:** `["KthLargest", [3, [1, 2, 3, 3]], "add", [3], "add", [5], "add", [6], "add", [7], "add", [8]]`

**Output:** `[null, 3, 3, 3, 5, 6]`

**Explanation:** KthLargest kthLargest = new KthLargest(3, [1, 2, 3, 3]);
kthLargest.add(3);   // return 3
kthLargest.add(5);   // return 3
kthLargest.add(6);   // return 3
kthLargest.add(7);   // return 5
kthLargest.add(8);   // return 6

## Constraints

- `1 <= k <= 1000`
- `0 <= nums.length <= 1000`
- `-1000 <= nums[i] <= 1000`
- `-1000 <= val <= 1000`
- There will always be at least `k` integers in the stream when you search for the `kth` integer.

## Deriving the Solution

The question only ever asks about one summary of the stream: its top `k` values. Values arrive and never leave, so the `k`th largest of a growing stream never decreases, and once a value falls out of the top `k` it can never return. Every solution below is a choice of how much order to keep between adds, and how much of that order to re-derive each time.

1. **Start literal.** Store every value the stream has delivered; on each `add`,
   append the new value, sort the whole list, and read the `k`th largest off the
   sorted order. Correct, but it re-derives a full order that already existed, at
   `O(n log n)` per add: see [Brute Force](#brute-force).
2. **Sort once, then only insert.** The re-sort repeats work the previous add
   already finished: appending one value disturbs only that value's slot, never the
   order of the rest. Keep the list sorted permanently and pay one insertion-sort
   pass per add, `O(n)`: see
   [Sorted List with Linear Insertion](#sorted-list-with-linear-insertion).
3. **Keep only the top `k`.** The sorted list carefully orders the `n - k` values
   below the cutoff, yet no query ever reads them, and they cannot come back. Keep
   exactly the `k` largest values seen so far in a min-heap, whose root is the
   weakest of them, the current `k`th largest: readable in `O(1)`, replaced by a
   newcomer in `O(log k)`: see [Min-Heap of Size K](#min-heap-of-size-k).
4. **Let the library find the slot.** The sorted-list solution's walk finds `val`'s
   slot one neighbor at a time; [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm)
   finds it in `O(log n)` comparisons, and `bisect.insort` packages the search and
   the insert: see
   [Sorted List with Binary Search Insertion](#sorted-list-with-binary-search-insertion).

## Solutions

### Brute Force

#### Derivation

The most literal reading of the contract: the class owns the stream, so it can simply store all of it, and "the `k`th largest" is a question about the sorted stream. Sorting at construction would go stale the moment the first value arrives, so every `add` re-sorts before answering:

1. `__init__` stores `k` and the stream `nums` as delivered.
2. `add` appends `val` to `nums` and sorts `nums` ascending in place.
3. In a sorted list the `k`th largest sits at index `-k`, so return `nums[-k]`.

#### Walkthrough

Trace Example 1: `k = 3`, `nums = [1, 2, 3, 3]`. Each line is one `add` call; the constructor contributes the leading `null` of the expected Output:

```text
init             nums = [1, 2, 3, 3]
add(3)  sorted   [1, 2, 3, 3, 3]              return nums[-3] = 3
add(5)  sorted   [1, 2, 3, 3, 3, 5]           return nums[-3] = 3
add(6)  sorted   [1, 2, 3, 3, 3, 5, 6]        return nums[-3] = 3
add(7)  sorted   [1, 2, 3, 3, 3, 5, 6, 7]     return nums[-3] = 5
add(8)  sorted   [1, 2, 3, 3, 3, 5, 6, 7, 8]  return nums[-3] = 6
```

The returned sequence `3, 3, 3, 5, 6` matches Example 1's expected Output `[null, 3, 3, 3, 5, 6]`.

#### Solution

The code is the walkthrough's append-sort-read cycle.

```python
from typing import List


class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.nums = nums

    def add(self, val: int) -> int:
        self.nums.append(val)
        self.nums.sort()
        return self.nums[-self.k]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)` per `add`

`add` sorts all `n` stored values, and a comparison sort costs `O(n log n)`. The constructor stores the initial stream untouched, so it is `O(1)`.

##### Space Complexity: `O(n)`

The class keeps every value the stream has delivered.

#### Key Insights

- `nums[-k]` reads the `k`th largest from an ascending list without reversing it:
  negative indexing counts from the end, which is where the largest values live.
- The approach is correct but repeats the maximum possible work per query: the whole
  list is reordered every time, including the values far below the top-`k` cutoff.
- Keeping the stream unsorted between adds is what makes every `add` pay; the next
  solution keeps the sort's result instead of discarding it.

### Sorted List with Linear Insertion

#### Derivation

The brute force re-sorts a list that was already sorted when the previous `add` returned: appending one value can disturb only that value's position, never the order of the rest. One pass of [insertion sort](https://en.wikipedia.org/wiki/Insertion_sort) repairs the order: walk from the end, shifting values larger than `val` one slot right, and drop `val` into the gap that opens. The constructor now pays for the one sort this approach ever needs:

1. `__init__` stores `k` and `sorted(nums)`.
2. `add` appends `val`, then walks `position` from the end toward the front while
   `nums[position - 1] > val`, shifting each displaced value one slot right.
3. Write `val` into `position` and return `nums[-k]`.

#### Walkthrough

Example 1 happens to deliver its values in ascending order, so no shift ever fires; each `add` appends and reads straight off:

```text
init             nums = [1, 2, 3, 3]
add(3)  append   [1, 2, 3, 3, 3]              return nums[-3] = 3
add(5)  append   [1, 2, 3, 3, 3, 5]           return nums[-3] = 3
add(6)  append   [1, 2, 3, 3, 3, 5, 6]        return nums[-3] = 3
add(7)  append   [1, 2, 3, 3, 3, 5, 6, 7]     return nums[-3] = 5
add(8)  append   [1, 2, 3, 3, 3, 5, 6, 7, 8]  return nums[-3] = 6
```

Again the returns are `3, 3, 3, 5, 6`, matching Example 1. To see the walk actually move data, take a tailored delivery: suppose the stream's next value were `2` instead of `8`, arriving while `nums = [1, 2, 3, 3, 3]`:

```text
append 2         nums = [1, 2, 3, 3, 3, 2]    position = 5
nums[4] = 3 > 2  shift right                  [1, 2, 3, 3, 3, 3]   position = 4
nums[3] = 3 > 2  shift right                  [1, 2, 3, 3, 3, 3]   position = 3
nums[2] = 3 > 2  shift right                  [1, 2, 3, 3, 3, 3]   position = 2
nums[1] = 2 > 2  stop: equal values do not shift
nums[2] = 2      nums = [1, 2, 2, 3, 3, 3]
```

The three threes each moved one slot right and `2` settled beside the existing `2`, so the list is sorted again and `nums[-3]` still reads `3`.

#### Solution

The code is the walkthrough's single insertion pass, between the append and the read.

```python
from typing import List


class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.nums = sorted(nums)

    def add(self, val: int) -> int:
        self.nums.append(val)
        # One insertion-sort pass: shift larger values right, drop val in.
        position = len(self.nums) - 1
        while position > 0 and self.nums[position - 1] > val:
            self.nums[position] = self.nums[position - 1]
            position -= 1
        self.nums[position] = val
        return self.nums[-self.k]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)` per `add`

The constructor's sort is the only `O(n log n)` moment. Each `add` walks at most `n` positions, shifting values right one at a time, so an add is linear in the stream length even when `val` itself lands near the top end after a short walk.

##### Space Complexity: `O(n)`

The sorted list holds every delivered value, `n` of them.

#### Key Insights

- The sort is paid exactly once, at construction; every later `add` repairs the
  order locally instead of re-deriving it.
- The shift test uses strict `>`, so a duplicate of `val` does not move and the new
  value inserts after its equals; the answer depends only on the multiset, so the
  tie-break direction is free.
- An array keeps order cheaply but inserts expensively: the `O(n)` shift is the
  floor for a contiguous list, which pushes toward keeping less than the whole
  stream ordered.

### Min-Heap of Size K

#### Derivation

Both sorted-list solutions keep all `n` values ordered although only the top `k` can ever be read, and the values below the cutoff cannot come back: values only arrive, so the `k`th largest of the stream never decreases. That means the cutoff set can be maintained incrementally. A [min-heap](https://en.wikipedia.org/wiki/Heap_(data_structure)) capped at `k` entries maintains it: the root is the smallest of the `k` largest values seen so far, which is exactly the current `k`th largest. A newcomer joins by pushing; when that makes `k + 1` values, the popped root is precisely the one value that fell out of the top `k`. The constructor reaches the same state from the initial stream by heapifying all of it and popping the smallest until `k` remain:

1. `__init__` stores `k`, copies `nums` into `heap`, calls `heapify`, then pops while
   `len(heap) > k`.
2. `add` pushes `val` onto `heap`.
3. If `len(heap) > k`, pop the root: it is the weakest of the `k + 1` values present,
   so the survivors are again the top `k` of the stream.
4. Return `heap[0]`.

#### Invariant

The heap always holds the top `k` of the values seen so far (all of them while fewer than `k` have arrived), and its root is the smallest of those values, the current `k`th largest:

$$ \text{heap} = \text{top } k \text{ of the stream so far} \;\Rightarrow\; \text{heap}[0] = \min(\text{heap}) = k\text{th largest} $$

```text
heap    = the top k values of the stream so far, as a min-heap
heap[0] = smallest of those k values  =  kth largest so far
```

Every branch preserves it. In `__init__`, `heapify` only rearranges, and each trim pop removes the smallest value while more than `k` remain: a value outside the top `k` of a prefix of the stream stays outside the top `k` of the whole stream, because the `k`th largest never decreases as values arrive. In `add`, after the push the heap holds the old top `k` plus `val`; if that makes `k + 1` values, the pop removes the smallest of them, leaving exactly the top `k`. While the heap is at or below `k` entries, no eviction is due and the invariant holds with whatever has arrived. At the return, the invariant says `heap[0]` is the `k`th largest, which is what the code reports.

#### Walkthrough

Trace Example 1: `k = 3`, `nums = [1, 2, 3, 3]`. The interior order of a heap list varies with the sift paths; only the root `heap[0]` is meaningful, and every state below is the list CPython's `heapq` actually maintains:

```text
init     copy [1, 2, 3, 3]     heapify -> [1, 2, 3, 3]
         pop 1 (len 4 > 3)     heap = [2, 3, 3]        root 2 = 3rd largest
add(3)   push -> [2, 3, 3, 3]  pop 2 -> [3, 3, 3]      return heap[0] = 3
add(5)   push -> [3, 3, 3, 5]  pop 3 -> [3, 3, 5]      return heap[0] = 3
add(6)   push -> [3, 3, 5, 6]  pop 3 -> [3, 6, 5]      return heap[0] = 3
add(7)   push -> [3, 6, 5, 7]  pop 3 -> [5, 6, 7]      return heap[0] = 5
add(8)   push -> [5, 6, 7, 8]  pop 5 -> [6, 8, 7]      return heap[0] = 6
```

The constructor trims the four initial values down to the top three, `2, 3, 3`, with the root `2` as the current `k`th largest. Every later `add` pushes, pops the root when the heap overflows, and reads the new root: the returned sequence `3, 3, 3, 5, 6` matches Example 1's expected Output.

#### Solution

The code is the walkthrough's trim in the constructor and push-pop-read in `add`.

```python
import heapq
from typing import List


class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = list(nums)
        heapq.heapify(self.heap)
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + (n - k) log n)` to initialize, `O(log k)` per `add`

`heapify` is `O(n)` over the initial stream, and the trim performs `n - k` pops on a heap of at most `n` entries. Each `add` performs one push and at most one pop on a heap that never exceeds `k + 1` entries, so an add costs `O(log k)` no matter how large the stream grows.

##### Space Complexity: `O(n)` transient, `O(k)` retained

Construction copies the whole initial stream before trimming; from the first query on, the heap holds exactly `min(k, stream size)` entries, `k` at most.

#### Key Insights

- A min-heap, not a max-heap: the answer is the weakest member of the top `k`, and
  the min-heap keeps exactly that value at the root in `O(1)`.
- The eviction pop in `add` discards precisely the value that fell out of the top
  `k`; the never-decreasing property of the `k`th largest is what makes discarding
  safe.
- The constructor trims from the top by popping `n - k` times; pushing the initial
  values one by one into a capped heap reaches the same state by a different trade:
  the capped build costs `O(n log k)` and wins when `k` is small next to `n`, while
  `heapify` plus trimming costs `O(n + (n - k) log n)` and wins as the initial
  stream approaches the cap.

### Sorted List with Binary Search Insertion

#### Derivation

The linear-insertion solution's walk does two jobs: it finds `val`'s slot and it shifts values to open the slot. The finding half can halve instead of step: in a sorted list, [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) locates the insertion point in `O(log n)` comparisons, and `bisect.insort` is that search plus the insert, keeping the list sorted. The shifting half remains `O(n)`, the honest bound of a contiguous array, so the asymptotic complexity does not change; what improves is the comparison count and how much insertion logic the code has to get right by hand:

1. `__init__` stores `k` and `sorted(nums)`.
2. `add` calls `bisect.insort(self.nums, val)`, which slots `val` after any equal
   values.
3. Return `nums[-k]`.

#### Walkthrough

The adds of Example 1 leave the same sorted states the linear version traced; the interesting state is where the search lands. Reuse the tailored delivery from the previous walkthrough, a stream value of `2` arriving while `nums = [1, 2, 3, 3, 3]`:

```text
add(2)   bisect_right([1, 2, 3, 3, 3], 2) = 2   insert after the existing 2
         nums = [1, 2, 2, 3, 3, 3]              return nums[-3] = 3
```

and on Example 1's real `add(5)` into `[1, 2, 3, 3, 3]` the search lands past every equal-or-smaller value, at the end of the list:

```text
add(5)   bisect_right([1, 2, 3, 3, 3], 5) = 5   insert at index 5, the list's end
         nums = [1, 2, 3, 3, 3, 5]              return nums[-3] = 3
```

Both match the results the linear walk produced, without touching a single neighbor by hand.

#### Solution

The code is the sorted-list approach with the hand-written walk replaced by one `bisect.insort` call.

```python
import bisect
from typing import List


class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.nums = sorted(nums)

    def add(self, val: int) -> int:
        bisect.insort(self.nums, val)
        return self.nums[-self.k]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)` per `add`

`bisect.insort` finds the slot in `O(log n)` comparisons but inserts into a Python list, which shifts the tail in `O(n)`. The constructor's sort remains the only `O(n log n)` moment.

##### Space Complexity: `O(n)`

The sorted list holds every delivered value.

#### Key Insights

- `bisect.insort(nums, val)` is `nums.insert(bisect.bisect_right(nums, val), val)`:
  the binary search replaces the comparison walk, the list insert does the shifting.
- The total complexity is unchanged from the linear walk, because the shift
  dominates; the gain is fewer comparisons per insert and less hand-rolled loop code
  to maintain.
- A genuinely sublinear `add` on a fully sorted structure needs a different
  container (a balanced tree or a skip list), or it needs to stop ordering everything
  below the cutoff, which is what the Min-Heap of Size K does.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n log n)` per `add` - the whole stream is re-sorted on every arrival.
- **Sorted List with Linear Insertion**: `O(n)` per `add` - one insertion-sort walk with up to `n` shifts.
- **Min-Heap of Size K**: `O(log k)` per `add` - one push and at most one pop on a heap capped at `k`.
- **Sorted List with Binary Search Insertion**: `O(n)` per `add` - `O(log n)` to find the slot plus an `O(n)` shift.

### Space Complexity

- **Brute Force**: `O(n)` - every delivered value is stored.
- **Sorted List with Linear Insertion**: `O(n)` - every delivered value is stored.
- **Min-Heap of Size K**: `O(k)` - only the top `k` survive construction.
- **Sorted List with Binary Search Insertion**: `O(n)` - every delivered value is stored.

### Trade-offs

- The brute force is the simplest translation of the contract (store, sort, index)
  and needs no auxiliary structure, but it spends the most work per query by a wide
  margin.
- The sorted-list pair keeps the entire stream ordered, which nothing below the top
  `k` ever reads; the linear walk is easy to audit by hand, the bisect call is
  shorter and searches faster, and both still pay an `O(n)` insert.
- The min-heap keeps exactly the entries queries read, gives `O(1)` reads and
  `O(log k)` adds independent of `n`, and gives up random access and any full
  ordering in return.

### When to Use Each

- **Brute Force**: a first pass while the API settles, or streams so small that a
  sort per query is irrelevant.
- **Sorted List with Linear Insertion**: when another consumer needs the whole
  sorted stream anyway and clarity beats constants.
- **Min-Heap of Size K** (recommended): the default for the streaming contract; the
  `k`th largest is read in `O(1)` and every `add` is `O(log k)` no matter how large
  the stream grows.
- **Sorted List with Binary Search Insertion**: the Pythonic tidy-up when the full
  ordered stream is genuinely needed and `bisect` is available.

### Optimization Notes

- Build the initial heap with `heapify` (`O(n)`) and trim by popping, or push the
  initial values one by one into a capped heap: the capped build costs
  `O(n log k)` and wins when `k` is small next to `n`, while `heapify` plus
  trimming costs `O(n + (n - k) log n)` and wins as the initial stream
  approaches the cap.
- `heapreplace(heap, val)` is not a drop-in for the guarded push-pop: it evicts the
  root unconditionally, which corrupts the top `k` whenever `val` is smaller than
  the root (at equality the eviction swaps the value for itself, a harmless no-op).
  Once the heap is full, guard it as `if val > self.heap[0]`.
- The overflow guard fires at most once per `add`, because a single push can raise
  the size past `k` by exactly one.
- The standard library has no sorted-list type with sublinear inserts (`bisect`
  works on plain lists); outside the standard library,
  `sortedcontainers.SortedList` answers this problem with `O(log n)`-amortized
  inserts, a common production variant.
- The two-heap construction, one heap per side of the middle, is the answer to Find
  Median from Data Stream, where both boundaries of the stream matter instead of
  just the top-`k` cutoff.
