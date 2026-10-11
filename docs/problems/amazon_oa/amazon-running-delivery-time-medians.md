# [Running Delivery Time Medians](https://www.fastprep.io/problems/amazon-running-delivery-time-medians)

**Medium** | **NN minutes** | **Heap, Design**

Given an array deliveryTimes, process the values from left to right. After each new delivery time arrives, output the median of all delivery times seen so far.

When the number of seen values is even, use the lower median, meaning the larger value in the lower half after sorting.

Return an array containing the median after each insertion.

## Examples

### Example 1

**Input:** `deliveryTimes = [5,17,100,11]`

**Output:** `[5,5,17,11]`

**Explanation:** The sorted prefixes are [5], [5,17], [5,17,100], and [5,11,17,100]. Their lower medians are 5, 5, 17, and 11.

## Constraints

- `deliveryTimes are processed from left to right.`
- `After each new value is inserted, record the median of all values seen so far.`
- `When the number of seen values is even, use the lower median: the larger value in the lower half after sorting.`
- `Return one median for each insertion.`

## Solutions

### Sorted List with Insertion

#### Derivation

The statement hands over the most direct reading: the median is a property of the sorted prefix, so the first approach simply keeps the prefix sorted. After each new delivery time arrives, slide it into its sorted position inside one growing list `seen`, then read the lower median straight off an index. No structure beyond the list is needed:

1. Keep `seen`, a list that is sorted ascending at all times, and `medians`, the output.
2. For each incoming `delivery_time`, append it at the end of `seen` and bubble it backward while its left neighbor is larger. The list is sorted again.
3. With `count = len(seen)`, the lower median is `seen[(count - 1) // 2]`: the single middle element for an odd count, and the larger element of the lower half for an even count. Append it to `medians`.
4. Return `medians` after all arrivals.

The backward bubbling is the insertion-sort step. It is simple and obviously correct, but a value arriving at the front of the list shifts every element already stored, which is where the cost concentrates.

#### Walkthrough

Let us run Example 1: `deliveryTimes = [5, 17, 100, 11]`. Each line shows the arrival, the bubbling inside `seen`, and the index the lower median is read from:

```text
arrival 5    seen = [5]                  count 1 -> median seen[0] = 5
arrival 17   seen = [5, 17]              count 2 -> median seen[0] = 5
arrival 100  seen = [5, 17, 100]         count 3 -> median seen[1] = 17
arrival 11   seen = [5, 11, 17, 100]     count 4 -> median seen[1] = 11
```

The third row shows the odd-count read: three values, `(3 - 1) // 2 = 1`, so `seen[1] = 17` is the middle element. The fourth row is the even-count read: `(4 - 1) // 2 = 1`, so `seen[1] = 11` is the larger value of the lower half `[5, 11]`. The collected medians are `[5, 5, 17, 11]`, the expected Output for Example 1.

#### Solution

The code is the walkthrough's arrival loop: bubble the new value back into place, then index the lower median.

```python
from typing import List


class Solution:
    def solve(self, deliveryTimes: List[int]) -> List[int]:
        seen: List[int] = []
        medians: List[int] = []

        for delivery_time in deliveryTimes:
            position = len(seen)
            seen.append(delivery_time)
            while position > 0 and seen[position - 1] > delivery_time:
                seen[position - 1], seen[position] = (
                    seen[position],
                    seen[position - 1],
                )
                position -= 1

            medians.append(seen[(len(seen) - 1) // 2])

        return medians
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n` arrivals can bubble past every element already stored, so one insertion costs up to `O(n)` and the arrivals sum to a quadratic total.

##### Space Complexity: `O(n)`

The sorted list `seen` holds every arrival; the output array is not counted as extra space.

#### Key Insights

- The lower median of a sorted list is always the single index `(count - 1) // 2`, which covers both parities without branching.
- Keeping the whole prefix sorted buys the median in `O(1)`, but the insertion shift makes a long stream quadratic overall.
- The append-then-bubble form of insertion needs no library search helper and shifts the tail in place.

### Two Heaps

#### Derivation

The sorted list pays a linear shift per arrival to maintain far more order than the median ever reads: only the boundary between the lower half and the upper half matters. The repair is to hold each half in its own [heap](https://en.wikipedia.org/wiki/Heap_(data_structure)), so the value straddling the boundary sits at a heap top, reachable in constant time, while each arrival costs only a logarithmic sift:

1. Keep `lower`, a max-heap storing the smaller half as negated values so Python's min-heap behaves as a max-heap, and `upper`, a min-heap storing the larger half.
2. For each `delivery_time`: push it onto `lower`, then immediately pop `lower`'s maximum and push it onto `upper`. This funnel guarantees every value in `lower` is at most every value in `upper`.
3. Rebalance: if `upper` holds more values than `lower`, move `upper`'s minimum back to `lower`. The invariant keeps `lower` holding either the same count as `upper` or exactly one more, so `lower` is always the lower half under the statement's definition.
4. After each arrival, the lower median is `-lower[0]`, the maximum of the smaller half.

Routing every arrival through `lower` before handing its top to `upper` is what keeps the partition correct without comparing the new value against the heap tops.

#### Invariant

The two heaps preserve a partition that pins the lower median to `lower`'s top after every arrival:

```text
max(lower) <= min(upper)                 (partition ordering)
0 <= len(lower) - len(upper) <= 1        (lower holds the lower half)
lower median = max(lower) = -lower[0]
```

The funnel enforces the ordering half: the value that crosses from `lower` to `upper` is `lower`'s maximum, so the boundary value is always the one that moves. The rebalance enforces the size half: whenever the funnel leaves `upper` larger, its minimum returns to `lower`. At loop exit, after the final arrival, the last appended median still equals `max(lower)`, so the output list is correct by the invariant alone.

#### Walkthrough

Let us run Example 1 through the funnel: `deliveryTimes = [5, 17, 100, 11]`. `lower` stores negated values, so `-lower[0]` is the maximum of the smaller half and `upper[0]` the minimum of the larger half. Each line is one arrival; the median line reads the heap tops:

```text
start      lower = []             upper = []
add 5      lower = [-5]           upper = []            median = 5
add 17     lower = [-5]           upper = [17]          median = 5
add 100    lower = [-17, -5]      upper = [100]         median = 17
add 11     lower = [-11, -5]      upper = [17, 100]     median = 11
```

The `add 5` row shows the funnel in full: `5` is pushed onto `lower`, its maximum immediately pops over to `upper`, and the rebalance brings it straight back because `upper` outgrew `lower`. The `add 17` row ends level: `17` funnels into `upper`, the sizes are equal, so no rebalance fires and `lower` keeps `5`. The `add 100` row shows the rebalance: `100` funnels into `upper`, leaving `upper` with two values against one, so `upper`'s minimum `17` moves back and `lower` holds the lower half `[5, 17]` of the odd prefix. The `add 11` row is the even prefix: `17` funnels out and no rebalance fires, leaving `lower` holding `[5, 11]` and `upper` holding `[17, 100]`; the lower median is the max of `[5, 11]`, which is `11`. The medians read `[5, 5, 17, 11]`, the expected Output for Example 1.

#### Solution

The code is the walkthrough's funnel and rebalance, with the median read as `-lower[0]` after each arrival.

```python
import heapq
from typing import List


class Solution:
    def solve(self, deliveryTimes: List[int]) -> List[int]:
        lower: List[int] = []
        upper: List[int] = []
        medians: List[int] = []

        for delivery_time in deliveryTimes:
            heapq.heappush(lower, -delivery_time)
            heapq.heappush(upper, -heapq.heappop(lower))
            if len(upper) > len(lower):
                heapq.heappush(lower, -heapq.heappop(upper))
            medians.append(-lower[0])

        return medians
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Each arrival performs a constant number of heap pushes and pops, each logarithmic in the number of stored values.

##### Space Complexity: `O(n)`

Every arrival is stored in exactly one of the two heaps; the output array is not counted as extra space.

#### Key Insights

- The statement's lower-median rule removes the usual parity branch: `lower` always holds the lower half, so the median is always `-lower[0]`, never an average.
- The push-then-funnel order enforces the partition automatically, so the new value never needs to be compared with the heap tops.
- Negating values lets Python's `heapq`, a min-heap, serve as the max-heap `lower`.

### Sorted List with `bisect.insort`

#### Derivation

This is the same sorted-list strategy as the first solution, with the standard library taking over the bookkeeping: [`bisect.insort`](https://docs.python.org/3/library/bisect.html) finds the leftmost slot where `delivery_time` belongs and inserts it there in one call. The asymptotic cost does not move; only the code shrinks:

1. Keep `seen`, a list that is sorted ascending at all times.
2. For each `delivery_time`, call `bisect.insort(seen, delivery_time)`: an `O(log n)` binary search for the slot followed by the same `O(n)` tail shift as before.
3. Append `seen[(len(seen) - 1) // 2]`, the same lower-median index.

The behavior is identical to the hand-bubbled version; the search and the insertion are simply delegated to `bisect`.

#### Walkthrough

Example 1 again: `deliveryTimes = [5, 17, 100, 11]`. Each `bisect.insort` lands the arrival in exactly the slot the hand-bubbled walkthrough reached:

```text
arrival 5    insort into slot 0    seen = [5]               median seen[0] = 5
arrival 17   insort into slot 1    seen = [5, 17]           median seen[0] = 5
arrival 100  insort into slot 2    seen = [5, 17, 100]      median seen[1] = 17
arrival 11   insort into slot 1    seen = [5, 11, 17, 100]  median seen[1] = 11
```

The arrival `11` shows the search half of the delegation: `bisect` finds slot `1` without touching a single element, then the insert shifts `17` and `100` one step right. The medians are `[5, 5, 17, 11]`, the expected Output for Example 1.

#### Solution

The code is the first solution with its search and bubble collapsed into the single `bisect.insort` call.

```python
import bisect
from typing import List


class Solution:
    def solve(self, deliveryTimes: List[int]) -> List[int]:
        seen: List[int] = []
        medians: List[int] = []

        for delivery_time in deliveryTimes:
            bisect.insort(seen, delivery_time)
            medians.append(seen[(len(seen) - 1) // 2])

        return medians
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

`bisect.insort` locates the slot in `O(log n)` but the underlying list insertion still shifts up to `n` stored values, so the arrivals keep their quadratic total.

##### Space Complexity: `O(n)`

The sorted list `seen` holds every arrival; the output array is not counted as extra space.

#### Key Insights

- `bisect.insort` collapses the binary search and the insertion into one call, making this the most concise sorted-list variant.
- The `O(n)` element shift is untouched: the bottleneck of the first solution is physical, not algorithmic, so no search shortcut removes it.

## Comparison of Solutions

### Time Complexity

- **Sorted List with Insertion**: `O(n^2)` - each arrival can bubble past every stored value, shifting the tail of the list.
- **Two Heaps**: `O(n log n)` - a constant number of logarithmic heap operations per arrival.
- **Sorted List with `bisect.insort`**: `O(n^2)` - the same tail shift behind one library call.

### Space Complexity

- **Sorted List with Insertion**: `O(n)` - the sorted list holds every arrival.
- **Two Heaps**: `O(n)` - every arrival lives in exactly one of the two heaps.
- **Sorted List with `bisect.insort`**: `O(n)` - the sorted list holds every arrival.

### Trade-offs

- **Sorted List with Insertion**: the most self-derivable structure and a constant-time median read, but the insertion shift makes long streams quadratic.
- **Two Heaps**: logarithmic per arrival and the only approach that scales comfortably to the largest streams, at the cost of the funnel-and-rebalance discipline and the negation trick.
- **Sorted List with `bisect.insort`**: the shortest correct implementation of the baseline idea, carrying the baseline's quadratic cost unchanged.

### When to Use Each

- **Two Heaps (Recommended)**: the interview answer and the right call for any realistic stream length, since it keeps every arrival logarithmic.
- **Sorted List with Insertion**: for small inputs, or as the from-scratch stepping stone that motivates the heap split.
- **Sorted List with `bisect.insort`**: when the standard library is available and brevity matters more than the quadratic bound, for example in a quick script over a short feed.

### Optimization Notes

- The statement's lower-median definition simplifies the classic two-heap design: with `lower` holding the lower half, the median is always `max(lower)`, so no parity branch and no averaging are needed.
- The bottleneck of both sorted-list variants is the physical element shift on insertion, not the search; `bisect.insort` inherits exactly the same shift.
- If the stream were read-only afterward, an offline variant could sort once and answer each prefix median by index, but the online setting of this problem requires the incremental structures above.
