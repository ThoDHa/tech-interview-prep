# [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/)

**Hard** | **30 minutes** | **Heap**

**Pattern:** [Heap / Priority Queue](../patterns/heap/intuition.md)

**Algorithm:** [Heap (data structure)](https://en.wikipedia.org/wiki/Heap_(data_structure))

**Practice:** [`practice/find_median_from_data_stream/solution.py`](../../practice/find_median_from_data_stream/solution.py)

The **median** is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.

- For example, for `arr = [2,3,4]`, the median is `3`.
- For example, for `arr = [2,3]`, the median is `(2 + 3) / 2 = 2.5`.

Implement the MedianFinder class:

- `MedianFinder()` initializes the `MedianFinder` object.
- `void addNum(int num)` adds the integer `num` from the data stream to the data structure.
- `double findMedian()` returns the median of all elements so far. Answers within `10^-5` of the actual answer will be accepted.

## Examples

### Example 1

**Input:**

```text
["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
[[], [1], [2], [], [3], []]
```

**Output:** `[null, null, null, 1.5, null, 2.0]`

**Explanation:**

```text
MedianFinder medianFinder = new MedianFinder();
medianFinder.addNum(1);    // arr = [1]
medianFinder.addNum(2);    // arr = [1, 2]
medianFinder.findMedian(); // return 1.5 (i.e., (1 + 2) / 2)
medianFinder.addNum(3);    // arr = [1, 2, 3]
medianFinder.findMedian(); // return 2.0
```

## Constraints

- `-10^5 <= num <= 10^5`
- There will be at least one element in the data structure before calling `findMedian`.
- At most `5 * 10^4` calls will be made to `addNum` and `findMedian`.

## Follow-up

- If all integer numbers from the stream are in the range `[0, 100]`, how would you optimize your solution?
- If `99%` of all integer numbers from the stream are in the range `[0, 100]`, how would you optimize your solution?

## Deriving the Solution

The median reads only the one or two middle values of the sorted stream, so every solution is a different answer to one question: how much order must be maintained on every `addNum` for `findMedian` to reach the middle instantly?

1. **Start literal.** Keep every number in one list that stays fully sorted: a
   hand-written binary search finds each value's slot, and `findMedian` indexes the middle. The search is `O(log n)`, but `list.insert` shifts the tail, so every `addNum` costs `O(n)`: see [Sorted List with Insertion](#sorted-list-with-insertion).
2. **Spot the waste.** Full sorted order is more than the median ever reads:
   only the boundary between the smaller half and the larger half matters. The linear shift pays to keep an ordering nobody asks about.
3. **Keep only the halves.** Store the smaller half in a max-heap and the
   larger half in a min-heap; the two heap tops straddle the median, and a heap restores itself in `O(log n)` per insert instead of shifting: see [Two Heaps](#two-heaps).
4. **Or lean on the library.** The sorted-list idea also comes prepackaged:
   `bisect.insort` performs the same search and shift in one call, shorter to write but with the same `O(n)` insertion cost: see [Sorted List with `bisect.insort`](#sorted-list-with-bisectinsort).

## Solutions

### Sorted List with Insertion

#### Derivation

The literal reading of `findMedian` is "index the middle of the sorted data", so the first question is how to keep the data sorted as numbers stream in. This brute-force baseline uses no imports at all: the whole stream lives in one Python list that is always kept in sorted order, so the median is just a matter of reading the middle of that list.

1. Maintain a single list `nums` that is invariantly sorted ascending.
2. On `addNum`, run a hand-written [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) to find the leftmost index
   where the new value belongs, then call `list.insert` to place it there. The binary search locates the slot in `O(log n)` comparisons, but the insert itself must shift every element after that slot, making the operation `O(n)`.
3. On `findMedian`, compute the middle index. For an odd count the single middle
   element is the median; for an even count average the two central elements.

The binary search guarantees the list stays sorted without re-sorting the whole collection on every insert, but the physical shift on insertion is what dominates the cost.

#### Walkthrough

Let us trace the first solution (Sorted List with Insertion) on Example 1: the call sequence `addNum(1)`, `addNum(2)`, `findMedian()`, `addNum(3)`, `findMedian()`. We follow `nums` (the sorted backing list) as each call mutates it.

For each `addNum`, the binary search scans with `low` and `high` to find the leftmost slot where `num` belongs, then `list.insert` drops it there:

| Step | Call | Binary search result | `nums` after |
|------|------|----------------------|--------------|
| 1 | `addNum(1)` | list empty, slot `0` | `[1]` |
| 2 | `addNum(2)` | `2` belongs after `1`, slot `1` | `[1, 2]` |
| 3 | `addNum(3)` | `3` belongs after `2`, slot `2` | `[1, 2, 3]` |

Now the two `findMedian` calls read the middle of the sorted list:

- After step 2, `findMedian()` sees `n = 2` (even). `mid = n // 2 = 1`, so it
  averages the two central elements: `(nums[0] + nums[1]) / 2 = (1 + 2) / 2 = 1.5`.
- After step 3, `findMedian()` sees `n = 3` (odd). `mid = n // 2 = 1`, so it
  returns the single middle element: `nums[1] = 2.0`.

The returned values across the call sequence are `1.5` then `2.0`, which matches the example's expected Output `[null, null, null, 1.5, null, 2.0]` (the `null` entries are the constructor and `addNum` calls, which return nothing).

#### Solution

The code is the walkthrough's table: a binary search for the slot in `addNum`, and middle indexing in `findMedian`.

```python
class MedianFinder:

    def __init__(self):
        # Keep all numbers in a single list maintained in sorted order.
        self.nums: list[int] = []

    def addNum(self, num: int) -> None:
        # Hand-written binary search for the leftmost insertion point.
        low, high = 0, len(self.nums)
        while low < high:
            mid = (low + high) // 2
            if self.nums[mid] < num:
                low = mid + 1
            else:
                high = mid
        # Insert keeps the list sorted; list.insert shifts the tail.
        self.nums.insert(low, num)

    def findMedian(self) -> float:
        n = len(self.nums)
        mid = n // 2
        if n % 2 == 1:
            return float(self.nums[mid])
        # Even length: average the two central elements.
        return (self.nums[mid - 1] + self.nums[mid]) / 2.0


# Your MedianFinder object will be instantiated and used as follows:
# obj = MedianFinder()
# obj.addNum(num)
# param_2 = obj.findMedian()
```

#### Time and Space Complexity Analysis

##### Time Complexity

- **addNum**: `O(n)` - the binary search to locate the slot is `O(log n)`, but
  inserting into the middle of a list shifts up to `n` trailing elements, so the linear shift dominates.
- **findMedian**: `O(1)` - it only indexes the one or two middle elements of an
  already sorted list.

##### Space Complexity: `O(n)`

Every number from the stream is retained in the single backing list, so storage grows linearly with the size of the stream.

#### Key Insights

- Keeping the list sorted at all times pushes all the work to `addNum` and lets
  `findMedian` read the median in constant time.
- A hand-written binary search finds the insertion point without any library
  helper, but it cannot avoid the `O(n)` element shift that `list.insert` performs.
- This approach is simple to reason about and correct, but the per-insert linear
  shift makes it slow for large streams.

### Two Heaps

#### Derivation

The sorted list pays `O(n)` per insert to maintain far more order than the median ever reads: only the boundary between the smaller and larger halves of the data matters. The repair is to keep each half in its own [heap](https://en.wikipedia.org/wiki/Heap_(data_structure)), so the two values straddling the median stay at the heap tops, available in constant time, while each insert costs only the heaps' logarithmic sift.

1. Maintain a max-heap `lower` for the smaller half (stored as negated values so
   Python's min-heap behaves as a max-heap) and a min-heap `upper` for the larger half.
2. On `addNum`, push the new value onto `lower`, then immediately pop `lower`'s
   maximum and push it onto `upper`. This guarantees every element in `lower` is `<=` every element in `upper`.
3. Rebalance: if `upper` has grown larger than `lower`, move its minimum back to
   `lower`. The invariant is that `lower` holds either the same count as `upper` or exactly one more.
4. On `findMedian`, if `lower` has the extra element its top is the median;
   otherwise average the two heap tops.

Routing each insert through `lower` before handing the top to `upper` keeps the two halves correctly partitioned without any sorting.

#### Formula

For a sorted sequence \(x_1 \le x_2 \le \dots \le x_n\), the [median](https://en.wikipedia.org/wiki/Median) is defined by cases on parity:

$$ \text{median} = \begin{cases} x_{\frac{n+1}{2}}, & n \text{ odd} \\[6pt] \dfrac{x_{\frac{n}{2}} + x_{\frac{n}{2}+1}}{2}, & n \text{ even} \end{cases} $$

```text
median = x[(n + 1) / 2],                  for n odd
median = (x[n / 2] + x[n / 2 + 1]) / 2,   for n even
         (x sorted ascending, indices 1-based)
```

Only the one or two middle values matter: the rest of the order is irrelevant. That is what the two heaps exploit. They maintain the partition

$$ \max(\textit{lower}) \ \le \ \min(\textit{upper}), \qquad 0 \ \le \ |\textit{lower}| - |\textit{upper}| \ \le \ 1 $$

```text
max(lower) <= min(upper)
0 <= len(lower) - len(upper) <= 1
```

so `lower` holds \(\lceil n/2 \rceil\) elements and `upper` the rest. Under that invariant the two definitions above read directly off the heap tops, with no sorting and no indexing:

$$ \text{median} = \begin{cases} \max(\textit{lower}), & |\textit{lower}| > |\textit{upper}| \\[6pt] \dfrac{\max(\textit{lower}) + \min(\textit{upper})}{2}, & |\textit{lower}| = |\textit{upper}| \end{cases} $$

```text
median = max(lower),                     when len(lower) > len(upper)
median = (max(lower) + min(upper)) / 2,  when len(lower) == len(upper)
```

The push-then-funnel in `addNum` is what enforces the ordering half of the invariant: routing every new number through `lower` before moving its top to `upper` guarantees the element that crosses over is the correct boundary value, whatever its magnitude.

#### Walkthrough

Let us run Example 1's call sequence through the two heaps: `addNum(1)`, `addNum(2)`, `findMedian()`, `addNum(3)`, `findMedian()`. Each snapshot shows the internal heap lists after the call: `lower` stores negated values (so `-lower[0]` is the max of the smaller half) and `upper` stores values as they are (so `upper[0]` is the min of the larger half).

```text
start        lower = []        upper = []
addNum(1)    lower = [-1]      upper = []    1 funnels through upper, rebalances back
addNum(2)    lower = [-1]      upper = [2]   max 2 crosses over; sizes level, no rebalance
findMedian() -> (-lower[0] + upper[0]) / 2 = (1 + 2) / 2 = 1.5
addNum(3)    lower = [-2, -1]  upper = [3]   3 crosses over; upper too big, 2 moves back
findMedian() -> -lower[0] = 2.0              lower holds the extra element
```

`addNum(1)` shows the funnel in full: `-1` is pushed onto `lower`, its top is immediately popped and pushed onto `upper` as `1`, and the rebalance moves it straight back because `upper` outgrew `lower`. `addNum(2)` pushes `-2` onto `lower`, pops the maximum `2` over to `upper`, and the sizes are level, so no rebalance fires. `addNum(3)` funnels the maximum `3` into `upper`, leaving `upper` with two elements against one, so the rebalance returns `upper`'s minimum `2` to `lower` as `-2`, where it sifts to the top.

The two `findMedian` calls read `1.5` (equal sizes, so the average of the tops `1` and `2`) and `2.0` (`lower` one larger, so its top `2`), matching the expected Output `[null, null, null, 1.5, null, 2.0]`.

#### Solution

The code is the walkthrough's funnel and rebalance, with `findMedian` reading the heap tops.

```python
import heapq


class MedianFinder:

    def __init__(self):
        # Max-heap (negated) holds the smaller half of the numbers.
        self.lower: list[int] = []
        # Min-heap holds the larger half of the numbers.
        self.upper: list[int] = []

    def addNum(self, num: int) -> None:
        # Push onto the lower (max) heap, then funnel its top into upper.
        heapq.heappush(self.lower, -num)
        heapq.heappush(self.upper, -heapq.heappop(self.lower))

        # Rebalance so lower holds at most one extra element.
        if len(self.upper) > len(self.lower):
            heapq.heappush(self.lower, -heapq.heappop(self.upper))

    def findMedian(self) -> float:
        if len(self.lower) > len(self.upper):
            return float(-self.lower[0])
        return (-self.lower[0] + self.upper[0]) / 2.0


# Your MedianFinder object will be instantiated and used as follows:
# obj = MedianFinder()
# obj.addNum(num)
# param_2 = obj.findMedian()
```

#### Time and Space Complexity Analysis

##### Time Complexity

- **addNum**: `O(log n)` for a constant number of heap pushes and pops, each
  logarithmic in the number of stored elements.
- **findMedian**: `O(1)` since it only inspects the heap tops.

##### Space Complexity: `O(n)`

Every inserted number is retained in exactly one of the two heaps, so storage grows linearly with the size of the stream.

#### Key Insights

- Splitting the data into a max-heap of the lower half and a min-heap of the
  upper half puts the median element(s) at the heap tops for `O(1)` retrieval.
- Negating values lets Python's `heapq` (a min-heap) serve as a max-heap.
- The push-then-transfer step enforces the ordering invariant automatically, so
  no explicit comparison between the new number and existing tops is needed.
- For the follow-up where values lie in `[0, 100]`, a fixed-size count array of
  101 buckets gives `O(1)` insertion and `O(100)` median lookup; when only 99% fall in range, bucket the common range and keep the rare outliers in separate ordered structures.

### Sorted List with `bisect.insort`

#### Derivation

This is the same sorted-list strategy as the first solution, but it asks what the standard library can take over: [`bisect.insort`](https://docs.python.org/3/library/bisect.html) finds the leftmost slot where `num` belongs and inserts it there, keeping the list sorted at all times. The `O(n)` shift remains; only the code shrinks.

1. Maintain a single list `nums` that is invariantly sorted ascending.
2. On `addNum`, call `bisect.insort(self.nums, num)`. It performs an `O(log n)`
   binary search for the insertion point and then an `O(n)` element shift to place the value.
3. On `findMedian`, index the middle of the sorted list exactly as before: the
   single middle element for an odd count, or the average of the two central elements for an even count.

The behavior is identical to the hand-written version; only the search and insert are delegated to `bisect`.

#### Walkthrough

Let us run Example 1's call sequence once more: `addNum(1)`, `addNum(2)`, `findMedian()`, `addNum(3)`, `findMedian()`. The state is the same sorted list as the hand-written version; here each `addNum` is a single `bisect.insort` call, which lands each value in exactly the slot the hand-written binary search found:

```text
start        nums = []
addNum(1)    insort into slot 0    nums = [1]
addNum(2)    insort into slot 1    nums = [1, 2]
findMedian() -> n = 2 even, (nums[0] + nums[1]) / 2 = 1.5
addNum(3)    insort into slot 2    nums = [1, 2, 3]
findMedian() -> n = 3 odd, nums[1] = 2.0
```

The list after every insert is identical to the hand-written walkthrough, and the two `findMedian` reads return `1.5` then `2.0`, matching the expected Output `[null, null, null, 1.5, null, 2.0]`.

#### Solution

The code is the first solution with its search and insert collapsed into the single `bisect.insort` call.

```python
import bisect


class MedianFinder:

    def __init__(self):
        # Single list kept in sorted order by bisect.insort.
        self.nums: list[int] = []

    def addNum(self, num: int) -> None:
        # bisect.insort does the binary search and the insertion in one call.
        bisect.insort(self.nums, num)

    def findMedian(self) -> float:
        n = len(self.nums)
        mid = n // 2
        if n % 2 == 1:
            return float(self.nums[mid])
        # Even length: average the two central elements.
        return (self.nums[mid - 1] + self.nums[mid]) / 2.0


# Your MedianFinder object will be instantiated and used as follows:
# obj = MedianFinder()
# obj.addNum(num)
# param_2 = obj.findMedian()
```

#### Time and Space Complexity Analysis

##### Time Complexity

- **addNum**: `O(n)` - `bisect.insort` locates the slot in `O(log n)` but the
  underlying list insertion still shifts up to `n` trailing elements.
- **findMedian**: `O(1)` - it only indexes the one or two middle elements.

##### Space Complexity: `O(n)`

Every number from the stream is retained in the single backing list, so storage grows linearly with the size of the stream.

#### Key Insights

- `bisect.insort` collapses the binary search and the insertion into a single
  call, making this the most concise sorted-list variant.
- The asymptotic cost is unchanged from the hand-written binary search: the
  `O(n)` element shift on insertion still dominates.
- Reach for this only when the standard library is available and brevity is
  valued over the explicit, library-free version.

## Comparison of Solutions

### Time Complexity

- **Sorted List with Insertion**: `addNum` is `O(n)` because each insertion must
  shift the trailing portion of the list, even though the binary search that finds the slot is only `O(log n)`. `findMedian` is `O(1)`.
- **Two Heaps**: `addNum` is `O(log n)` from a constant number of heap pushes and
  pops, and `findMedian` is `O(1)`. The heap solution is asymptotically faster on insertion, which is the dominant operation for large streams.
- **Sorted List with `bisect.insort`**: identical asymptotics to the hand-written
  sorted list, `O(n)` `addNum` and `O(1)` `findMedian`; only the search and shift are delegated to the standard library.

### Space Complexity

All three approaches store every number from the stream, so all use `O(n)` space. The sorted-list variants keep them in one contiguous list while the heaps split them across two arrays, but the total storage is the same linear bound.

### Trade-offs

- The sorted list is trivially simple to understand and uses no imports, but its
  linear-time insertion makes a long stream of `addNum` calls quadratic overall.
- The two-heap approach is more intricate to reason about (negation tricks and a
  rebalancing invariant), yet it delivers logarithmic insertion that scales comfortably to the largest inputs.
- The `bisect.insort` variant is the most concise to write but carries the same
  `O(n)` insertion cost as the hand-written sorted list, trading explicitness for brevity without any asymptotic gain.

### When to Use Each

- **Sorted List with Insertion**: Suitable for small streams, teaching the
  median concept, or environments where standard-library imports are unavailable and simplicity matters more than throughput.
- **Two Heaps**: Preferred for any realistic stream size and the expected
  interview answer, since it keeps every insertion logarithmic.
- **Sorted List with `bisect.insort`**: A good pick when the standard library is
  available and you want the shortest correct implementation, accepting the `O(n)` insertion for small or median-heavy workloads.

### Optimization Notes

- The bottleneck in the sorted-list approach is the physical element shift on
  `list.insert`, not the search; no amount of cleverness in the binary search removes that `O(n)` cost, and `bisect.insort` inherits exactly the same shift.
- The two-heap design removes the need to keep the entire collection ordered by
  ordering only enough to expose the median element(s) at the heap tops.
- For the bounded follow-up where values lie in `[0, 100]`, a fixed-size count
  array gives `O(1)` insertion and constant-bucket median lookup, beating both general approaches; when 99% of values fall in range, bucket the common range and track the rare outliers separately.
