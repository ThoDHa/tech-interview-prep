# [Find Median from Data Stream](https://www.fastprep.io/problems/amazon-find-median-from-data-stream)

**Hard** | **NN minutes** | **Design, Heap, Sorting**

Process a finite sequence of operations while maintaining every integer added so far. Each row in operations has one of these forms:

["add", value] inserts the integer represented by value.["median"] queries the current median.For an odd number of stored values, the median is the middle value after sorting. For an even number, it is the arithmetic mean of the two middle values. Return a double[] containing the median-query results in encounter order. Add operations produce no output.

## Examples

### Example 1

**Input:** `operations = [["add","5"],["median"],["add","1"],["median"],["add","9"],["median"]]`

**Output:** `[5.0,3.0,5.0]`

**Explanation:** The stored multisets at the three queries are [5], [1,5], and [1,5,9], whose medians are 5, 3, and 5.

### Example 2

**Input:** `operations = [["add","-4"],["add","8"],["median"],["add","8"],["median"],["add","20"],["median"]]`

**Output:** `[2.0,8.0,8.0]`

**Explanation:** The queries observe [-4,8], [-4,8,8], and [-4,8,8,20]. Their medians are 2, 8, and 8.

### Example 3

**Input:** `operations = [["add","1000000000"],["add","999999999"],["median"]]`

**Output:** `[999999999.5]`

**Explanation:** The two middle values are 999999999 and 1000000000, so their arithmetic mean is 999999999.5.

## Constraints

- `1 <= operations.length <= 2000`
- `Every row is either ["add", value] or ["median"].`
- `Each added value is an integer from -1000000000 through 1000000000.`
- `Every median query occurs after at least one add operation.`
- `At least one median query appears.`

## Solutions

### Sorted List with Insertion

#### Derivation

The literal reading of the problem: "median" means the middle of the sorted stored values, so the first approach keeps the stored values in one sorted list at all times. Each add converts the string payload with `int`, slides the value into its sorted slot, and each median query reads the middle index directly. No structure beyond the list is needed:

1. Keep `nums`, a list that is sorted ascending at all times, and `medians` for the query results.
2. On `["add", value]`, convert once with `num = int(value)`, then run a hand-written [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) for the leftmost slot where `num` belongs and call `list.insert` there. The search costs `O(log n)` comparisons, but the insert shifts every stored value after the slot.
3. On `["median"]`, with `count = len(nums)`: an odd count returns `float(nums[middle])` with `middle = count // 2`; an even count appends the mean of `nums[middle - 1]` and `nums[middle]`, computed with `/ 2.0` so the result is a float.
4. Return `medians` after all operations.

The binary search keeps the list sorted without re-sorting, but the physical shift on insert is where the cost concentrates.

#### Walkthrough

Example 1: `operations = [["add","5"],["median"],["add","1"],["median"],["add","9"],["median"]]`. Each line shows the binary search, the list state, and the value a median query reads:

```text
add 5      search on [] -> slot 0        nums = [5]
median     count 1 odd,  middle 0        5.0
add 1      1 belongs before 5, slot 0    nums = [1, 5]
median     count 2 even, middle 1        (1 + 5) / 2 = 3.0
add 9      9 belongs after 5, slot 2     nums = [1, 5, 9]
median     count 3 odd,  middle 1        5.0
```

The collected medians are `[5.0, 3.0, 5.0]`, the expected Output for Example 1. Example 3 exercises the even read on large values: after `add 1000000000` and `add 999999999`, the list is `[999999999, 1000000000]` and the mean of the two middle values is `999999999.5`.

#### Solution

The code is the walkthrough's loop: one branch performs the search-and-insert for an add, the other reads the middle for a median.

```python
from typing import List


class Solution:
    def solve(self, operations: List[List[str]]) -> List[float]:
        nums: List[int] = []
        medians: List[float] = []

        for operation in operations:
            if operation[0] == "add":
                num = int(operation[1])
                low, high = 0, len(nums)
                while low < high:
                    mid = (low + high) // 2
                    if nums[mid] < num:
                        low = mid + 1
                    else:
                        high = mid
                nums.insert(low, num)
            else:
                count = len(nums)
                middle = count // 2
                if count % 2 == 1:
                    medians.append(float(nums[middle]))
                else:
                    medians.append((nums[middle - 1] + nums[middle]) / 2.0)

        return medians
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n` operations either shifts up to `n` stored values (an add) or reads one index (a median), so the adds' shifts dominate with a quadratic total.

##### Space Complexity: `O(n)`

Every added value stays in the single backing list.

#### Key Insights

- Keeping the list sorted at all times pushes all the work into the add, so a median query is two indexes and no search.
- The hand-written binary search locates the slot in `O(log n)`, but it cannot avoid the `O(n)` element shift that `list.insert` performs.
- Values arrive as strings, so converting once with `int` before the search keeps every comparison an integer comparison.
- The even-count read divides by `2.0`, not `2`, because the return type is a float and `999999999.5` must survive intact.

### Two Heaps

#### Derivation

The sorted list maintains far more order than a median query ever reads: only the boundary between the lower half and the upper half of the stored values matters, and the linear insert shift pays to keep the rest ordered. The repair is to store each half in its own [heap](https://en.wikipedia.org/wiki/Heap_(data_structure)), so the two values straddling the median sit at the heap tops in constant time while each add costs only the logarithmic sift:

1. Keep `lower`, a max-heap of the smaller half (values negated so Python's min-heap behaves as a max-heap), and `upper`, a min-heap of the larger half.
2. On add, convert the payload with `int`, push `-num` onto `lower`, then immediately pop `lower`'s top and push it onto `upper`.
3. Rebalance: when `upper` holds more values than `lower`, move `upper`'s top back. The invariant is that `lower` holds either the same count as `upper` or exactly one more.
4. On median: if `lower` holds the extra value, its top is the median; otherwise average the two tops.

Routing every add through `lower` before handing its top to `upper` is what places the correct boundary value on the crossing, whatever the new value's magnitude.

#### Formula

For the sorted stored values \(x_1 \le x_2 \le \dots \le x_n\), the [median](https://en.wikipedia.org/wiki/Median) is defined by cases on parity:

$$ \text{median} = \begin{cases} x_{\frac{n+1}{2}}, & n \text{ odd} \\[6pt] \dfrac{x_{\frac{n}{2}} + x_{\frac{n}{2}+1}}{2}, & n \text{ even} \end{cases} $$

```text
median = x[(n + 1) / 2],                  for n odd
median = (x[n / 2] + x[n / 2 + 1]) / 2,   for n even
          (x sorted ascending, indices 1-based)
```

Only the one or two middle values matter, which is what the two heaps exploit. They maintain the partition

$$ \max(\textit{lower}) \ \le \ \min(\textit{upper}), \qquad 0 \ \le \ |\textit{upper}| - |\textit{lower}| \ \le \ 1 $$

```text
max(lower) <= min(upper)
0 <= len(upper) - len(lower) <= 1
```

with `lower` holding \(\lceil n/2 \rceil\) values and `upper` the rest. Under that invariant the definition reads straight off the heap tops:

$$ \text{median} = \begin{cases} \max(\textit{lower}), & |\textit{lower}| > |\textit{upper}| \\[6pt] \dfrac{\max(\textit{lower}) + \min(\textit{upper})}{2}, & |\textit{lower}| = |\textit{upper}| \end{cases} $$

```text
median = max(lower),                     when len(lower) > len(upper)
median = (max(lower) + min(upper)) / 2,  when len(lower) == len(upper)
```

#### Walkthrough

Example 1 again. Each line shows the heap contents after the call: `lower` stores negated values (so `-lower[0]` is the max of the smaller half) and `upper` stores values as they are (so `upper[0]` is the min of the larger half):

```text
start       lower = []         upper = []
add 5       lower = [-5]       upper = []     5 crosses to upper, rebalance returns it
median      lower holds the extra -> -lower[0] = 5.0
add 1       lower = [-1]       upper = [5]    top 5 crosses over; sizes level
median      equal sizes -> (-lower[0] + upper[0]) / 2 = (1 + 5) / 2 = 3.0
add 9       lower = [-5, -1]   upper = [9]    top 9 crosses, rebalance returns 5
median      lower holds the extra -> -lower[0] = 5.0
```

`add 1` shows the funnel in full: `-1` joins `lower`, the top `5` immediately crosses to `upper`, and the sizes stay level so no rebalance fires. `add 9` funnels `9` into `upper`, leaving `upper` one larger, so the rebalance returns `upper`'s minimum `5` to `lower`. The three medians read `5.0`, `3.0`, and `5.0`, the expected Output for Example 1. Example 3 shows the even read at the extreme: after the two adds, `lower = [-999999999]` and `upper = [1000000000]`, so the median is `(999999999 + 1000000000) / 2 = 999999999.5`.

#### Solution

The code is the walkthrough's funnel and rebalance, with the median read off the heap tops.

```python
import heapq
from typing import List


class Solution:
    def solve(self, operations: List[List[str]]) -> List[float]:
        lower: List[int] = []
        upper: List[int] = []
        medians: List[float] = []

        for operation in operations:
            if operation[0] == "add":
                num = int(operation[1])
                heapq.heappush(lower, -num)
                heapq.heappush(upper, -heapq.heappop(lower))
                if len(upper) > len(lower):
                    heapq.heappush(lower, -heapq.heappop(upper))
            else:
                if len(lower) > len(upper):
                    medians.append(float(-lower[0]))
                else:
                    medians.append((-lower[0] + upper[0]) / 2.0)

        return medians
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Each add performs a constant number of heap pushes and pops, each logarithmic in the number of stored values, and each median read is `O(1)`.

##### Space Complexity: `O(n)`

Every added value is retained in exactly one of the two heaps.

#### Key Insights

- Splitting the values into a max-heap of the lower half and a min-heap of the upper half puts the median element or elements at the heap tops for constant-time reads.
- Negating values lets Python's `heapq`, a min-heap, serve as the max-heap of the lower half.
- The push-then-funnel step enforces the ordering invariant automatically, so no explicit comparison between the new value and the two tops is needed.
- The even read divides the sum of two tops by `2.0`; with values up to `10^9`, `999999999.5` is still exactly representable, so no precision is lost.

### Sorted List with `bisect.insort`

#### Derivation

This is the same sorted-list strategy as the first solution, but it asks what the standard library can take over: [`bisect.insort`](https://docs.python.org/3/library/bisect.html) finds the leftmost slot where a value belongs and inserts it there, keeping the list sorted at all times. The `O(n)` shift remains; only the code shrinks:

1. Keep `nums` sorted ascending, exactly as before.
2. On add, call `bisect.insort(nums, int(value))`, which performs the `O(log n)` search and the `O(n)` shift in one call.
3. On median, read the middle of the list exactly as in the first solution, and return `medians` at the end.

The behavior is identical to the hand-written version; only the search and insert are delegated to `bisect`.

#### Walkthrough

Example 1 once more. Each add is a single `bisect.insort` call that lands the value in exactly the slot the hand-written binary search found, so the list states match the first walkthrough event for event:

```text
add 5      insort into slot 0    nums = [5]
median     count 1 odd,  middle 0 -> 5.0
add 1      insort into slot 0    nums = [1, 5]
median     count 2 even, middle 1 -> (1 + 5) / 2 = 3.0
add 9      insort into slot 2    nums = [1, 5, 9]
median     count 3 odd,  middle 1 -> 5.0
```

The medians are `[5.0, 3.0, 5.0]`, the expected Output for Example 1.

#### Solution

The code is the first solution with its search and insert collapsed into the single `bisect.insort` call.

```python
import bisect
from typing import List


class Solution:
    def solve(self, operations: List[List[str]]) -> List[float]:
        nums: List[int] = []
        medians: List[float] = []

        for operation in operations:
            if operation[0] == "add":
                bisect.insort(nums, int(operation[1]))
            else:
                count = len(nums)
                middle = count // 2
                if count % 2 == 1:
                    medians.append(float(nums[middle]))
                else:
                    medians.append((nums[middle - 1] + nums[middle]) / 2.0)

        return medians
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

`bisect.insort` locates the slot in `O(log n)` but the underlying list insertion still shifts up to `n` stored values, so the adds keep their quadratic total.

##### Space Complexity: `O(n)`

Every added value stays in the single backing list.

#### Key Insights

- `bisect.insort` collapses the binary search and the insertion into one call, making this the most concise sorted-list variant.
- The asymptotic cost is unchanged from the hand-written version: the `O(n)` element shift on insertion still dominates.
- The leftmost-slot semantics of `insort` match the hand-written search exactly, so equal values keep their arrival order.

## Comparison of Solutions

### Time Complexity

- **Sorted List with Insertion**: `O(n^2)` - the binary search finds each slot in `O(log n)`, but `list.insert` shifts up to `n` stored values per add; median reads are `O(1)`.
- **Two Heaps**: `O(n log n)` - a constant number of logarithmic heap sifts per add and constant-time median reads.
- **Sorted List with `bisect.insort`**: `O(n^2)` - identical asymptotics to the hand-written sorted list; only the search and shift are delegated to the standard library.

### Space Complexity

- **Sorted List with Insertion**: `O(n)` - one contiguous list of every added value.
- **Two Heaps**: `O(n)` - every value retained in exactly one of the two heaps.
- **Sorted List with `bisect.insort`**: `O(n)` - the same single list as the hand-written version.

### Trade-offs

- The sorted list variants are easy to reason about and make the median read trivial, but a long stream of adds degrades to quadratic work.
- The two-heap approach is more intricate (negation trick, funnel, rebalancing invariant), yet it keeps every add logarithmic, which is what the `10^9`-wide value range and a 2000-operation stream both tolerate comfortably.
- The `bisect.insort` variant trades explicitness for brevity without any asymptotic gain over the hand-written list.

### When to Use Each

- **Sorted List with Insertion**: teaching the median concept, or tiny streams where clarity beats throughput.
- **Two Heaps (Recommended)**: the expected interview answer for any realistic stream: logarithmic adds and constant reads.
- **Sorted List with `bisect.insort`**: the shortest correct implementation when the standard library is available and the stream is small.

### Optimization Notes

- The bottleneck in both sorted-list variants is the physical element shift on insert, not the search; no binary search refinement removes it, and `bisect.insort` inherits the same shift.
- The two-heap design orders only what the median reads: the funnel step guarantees the value crossing between the halves is always the correct boundary value.
- If every median query arrived before any add, sorting once per query would suffice, but interleaved queries make the incremental structures the right shape.
