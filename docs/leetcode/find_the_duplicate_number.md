# [Find The Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/)

**Medium** | **25 minutes** | **Array, Two Pointers, Binary Search, Bit Manipulation**

**Pattern:** [Two Pointers](../patterns/two_pointers/intuition.md), [Binary Search](../patterns/binary_search/intuition.md)

**Algorithm:** [Floyd's cycle detection](https://en.wikipedia.org/wiki/Cycle_detection) · [Binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) · [Hash table](https://en.wikipedia.org/wiki/Hash_table) · [Sorting](https://en.wikipedia.org/wiki/Sorting_algorithm)

**Practice:** [`practice/find_the_duplicate_number/solution.py`](../../practice/find_the_duplicate_number/solution.py)

You are given an array of integers `nums` containing `n + 1` integers. Each integer in `nums` is in the range `[1, n]` inclusive.

There is exactly **one repeated integer** in `nums`, and every other integer appears at most once.

Return the repeated integer.

## Examples

### Example 1

**Input:** `nums = [1,2,3,2,2]`

**Output:** `2`

### Example 2

**Input:** `nums = [1,2,3,4,4]`

**Output:** `4`

## Constraints

- `1 <= n <= 10,000`
- `nums.length == n + 1`
- `1 <= nums[i] <= n`

## Deriving the Solution

The pigeonhole puts the duplicate beyond doubt: `n + 1` values drawn from `1..n` cannot all be distinct. Because there is exactly one repeated value, the whole problem collapses into one question asked of a candidate value: "do you appear twice?". Every solution below answers that question for the right candidate; they differ in how much memory, time, or input reordering they are willing to spend.

1. **Start literal.** Take each value as a candidate and count its occurrences
   with a full scan of the array. The repeated value is the first candidate
   whose count reaches two. Correct everywhere, but every candidate rescans
   the whole array, costing `O(n^2)`: see [Brute Force](#brute-force).
2. **Spot the waste.** Each pass forgets what earlier passes learned. The
   question "have I seen this value before?" needs only memory of values, not
   counts: a set of seen values answers it per element in `O(1)`, one pass,
   `O(n)` total at the price of linear extra space: see [Hash Set](#hash-set).
3. **Spend order instead of memory.** In a sorted array the repeated value's
   copies sit adjacent, so one pass of neighbor comparisons finds them without
   any auxiliary structure. Sorting costs `O(n log n)` and reorders the input
   (a copy preserves it at `O(n)` space): see [Sorting](#sorting).
4. **Keep the array intact and the space constant.** Count how many entries
   are `<= m`: with one repeated value that count exceeds `m` exactly when
   the duplicate is `<= m`, so the answer space `1..n` can be binary searched,
   each probe paying one `O(n)` counting scan: see
   [Binary Search on Count](#binary-search-on-count).
5. **Read the array as a graph.** The rule "from index `i` step to index
   `nums[i]`" gives every index exactly one outgoing edge, and since values
   are in `1..n` no edge points back at index `0`: the walk from `0` is
   rho-shaped, and its cycle entrance is the value with two incoming edges,
   the duplicate. Floyd's two-pointer technique finds that entrance in one
   array read each, `O(n)` time and `O(1)` space, modifying nothing: see
   [Floyd's Cycle Detection](#floyds-cycle-detection).

## Solutions

### Brute Force

#### Derivation

The most direct reading counts, for each candidate value, how many times it appears. The guarantee "every other integer appears at most once" means the count of the repeated value reaches two:

1. Take `nums[x]` as the candidate for each index `x` in turn.
2. Scan the whole array, incrementing `count` on every equal entry.
3. Return `nums[x]` as soon as `count` reaches `2`; the duplicate is
   guaranteed to be some candidate, so a fallback return is never reached.

#### Walkthrough

Trace the candidate scans on Example 2: `nums = [1,2,3,4,4]`:

```text
x=0  candidate 1   count hits 1                    no return
x=1  candidate 2   count hits 1                    no return
x=2  candidate 3   count hits 1                    no return
x=3  candidate 4   count 2 at j=4 -> return 4
```

Every value before `4` appears exactly once, so their counts never reach two. The candidate `4` finds a second copy at index `4` and the function returns `4`, matching the expected Output for Example 2.

#### Solution

The code is the walkthrough's candidate loop with the early exit at a count of two.

```python
from typing import List


class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        length = len(nums)
        for x in range(length):
            count = 0
            for j in range(length):
                if nums[j] == nums[x]:
                    count += 1
                    if count == 2:
                        return nums[x]
        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n` candidates pays one full `O(n)` scan, and the worst case places the duplicate at the last candidate position.

##### Space Complexity: `O(1)`

Only the candidate index and the running count.

#### Key Insights

- Directly transcribes the guarantee into code: the first count of two is
  the answer.
- Correct for duplicates appearing more than twice, since counting stops at
  two.
- The full rescans per candidate are exactly what the later approaches
  remove.

### Hash Set

#### Derivation

The brute force re-answers one membership question per candidate by scanning. Flip the roles: walk the array once, remembering every value that has passed, and the first value that is already remembered is the duplicate. A [hash set](https://en.wikipedia.org/wiki/Hash_table) keeps that memory with `O(1)` membership tests, and it is the brute force's tally reduced to the one bit that matters, "counted at least once":

1. Start with an empty set `seen`.
2. For each `num`, if `num` is in `seen`, it has appeared before: return it.
3. Otherwise add `num` to `seen` and continue.

The first duplicate in walk order is returned, which is the first position where the second copy sits.

#### Walkthrough

Trace the set on Example 1: `nums = [1,2,3,2,2]`:

```text
num=1   not in seen   seen = {1}
num=2   not in seen   seen = {1, 2}
num=3   not in seen   seen = {1, 2, 3}
num=2   in seen!      return 2
```

The second copy of `2` arrives at index `3`, one step after the set has already absorbed every distinct value. The function returns `2`, matching the expected Output for Example 1. The later copy at index `4` is never visited because the early return has already ended the walk.

#### Solution

The code is the walkthrough's single pass with the membership test before each insert.

```python
from typing import List


class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        seen = set()
        for num in nums:
            if num in seen:
                return num
            seen.add(num)
        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass with an `O(1)` average membership test and insert per element; the walk stops at the second copy, at most the array's end.

##### Space Complexity: `O(n)`

The set holds every distinct value, up to `n` of them when the duplicate is at the very end.

#### Key Insights

- The set is the brute force's counting reduced to presence: a value's first
  appearance is all the memory the question needs.
- Linear time for linear memory is the standard trade; the rest of the file
  buys that memory back.
- Hashing pays no attention to the `1..n` value structure, so this works for
  any hashable values, a generality the later approaches trade away for
  space.

### Sorting

#### Derivation

Equal values are indistinguishable to order, so sorting gathers the duplicate's two copies side by side: the problem becomes finding one adjacent equal pair. That removes the set's memory entirely at the cost of a sort, and it reorders the input. Sorting a copy preserves the caller's array when that matters:

1. Sort a copy `nums_sorted` of the array.
2. Scan once; when `nums_sorted[i] == nums_sorted[i - 1]`, both copies of the
   duplicate are adjacent: return that value.

#### Walkthrough

Trace the adjacent scan on Example 2: `nums = [1,2,3,4,4]`, which sorts to `nums_sorted = [1,2,3,4,4]`:

```text
i=1   2 vs 1   not equal
i=2   3 vs 2   not equal
i=3   4 vs 3   not equal
i=4   4 vs 4   equal -> return 4
```

The only adjacent equal pair is the duplicate's two copies, so the scan returns `4`, matching the expected Output for Example 2. On Example 1 the sort produces `[1,2,2,2,3]` and the pair at indices `1` and `2` returns `2`; the third copy never matters.

#### Solution

The code is the sort followed by the one-pass neighbor comparison.

```python
from typing import List


class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        nums_sorted = sorted(nums)
        for i in range(1, len(nums_sorted)):
            if nums_sorted[i] == nums_sorted[i - 1]:
                return nums_sorted[i]
        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting dominates; the neighbor scan is one linear pass.

##### Space Complexity: `O(n)`

The sorted copy. (Sorting `nums` in place drops this to the sort's internal `O(log n)`, at the price of reordering the caller's data.)

#### Key Insights

- Order is a substitute for memory: adjacency does the work a set was doing.
- The `1..n` value structure is again unused; this works for any orderable
  values.
- The in-place variant is the interview-grade answer only when destroying the
  input is acceptable; the copy keeps correctness at the same asymptotics.

### Binary Search on Count

#### Derivation

Both previous costs come from treating the candidate as a value in the array. Search the value range instead. For any `m` in `1..n`, let `count(m)` be how many entries are `<= m`. If the duplicate were strictly greater than `m`, the `m` values `1..m` would each appear exactly once and `count(m)` would be exactly `m`; the count can only exceed `m` when the duplicate itself is `<= m`. That one comparison splits the range in half, so the answer can be binary searched:

1. Set `low = 1` and `high = n`, where `n = len(nums) - 1`.
2. While `low < high`, set `mid = (low + high) // 2` and count entries `<= mid`.
3. If `count > mid` the duplicate lies in `low..mid`: set `high = mid`.
   Otherwise it lies in `mid + 1..high`: set `low = mid + 1`.
4. `low` and `high` meet on the duplicate.

The invariant across iterations: the duplicate is always inside `low..high`. Each branch preserves it, and loop exit has `low == high`, a one-value range.

#### Walkthrough

Trace the probes on Example 1: `nums = [1,2,3,2,2]`, so `n = 4`, `low = 1`, `high = 4`:

```text
mid=2   entries <= 2: 1, 2, 2, 2   count=4   4 > 2   duplicate in 1..2   high=2
mid=1   entries <= 1: 1           count=1   1 <= 1  duplicate in 2..2   low=2
low == high == 2  -> return 2
```

The first probe already narrows the search to `1..2` because four of five entries are at most `2`. The second clears `1`, and the range collapses onto `2`, matching the expected Output for Example 1. Three `O(n)` counting scans replaced the hash set's linear memory.

#### Solution

The code is the probe loop over the value range, one counting pass per probe.

```python
from typing import List


class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        low, high = 1, len(nums) - 1
        while low < high:
            mid = (low + high) // 2
            count = 0
            for num in nums:
                if num <= mid:
                    count += 1
            if count > mid:
                high = mid
            else:
                low = mid + 1
        return low
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

`O(log n)` probes, each paying one `O(n)` counting scan of the whole array.

##### Space Complexity: `O(1)`

Only the range bounds and the running count; the array is never written.

#### Key Insights

- Binary searching a value range, not the array, is the move to remember:
  the array stays untouched and unsorted.
- The count comparison `count(m) > m` is the pigeonhole principle turned into
  a monotone predicate, which is what makes the range splittable.
- Same asymptotic time as sorting but read-only; it is the bridge from the
  memory-freeing approaches to the fully linear one below.

### Floyd's Cycle Detection

#### Derivation

The value structure `1..n` has not been spent yet. Read the array as a graph: from index `i` there is an edge to index `nums[i]`. Every index has exactly one outgoing edge, so walking is deterministic. Because every value is at least `1`, no edge points at index `0`, so the walk starting at index `0` can never return there: it runs down a tail and then around a cycle forever. Two indices holding the same value are two edges pointing at the same node, and that node is exactly the cycle's entrance: the duplicate.

Finding a cycle entrance without memory is [Floyd's cycle detection](https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare): a `slow` pointer moving one hop and a `fast` pointer moving two hops must meet inside the cycle, and a second meeting between one pointer reset to the start and one continuing from the first meeting point happens precisely at the entrance:

1. Phase one: advance `slow` by one hop (`slow = nums[slow]`) and `fast` by
   two (`fast = nums[nums[fast]]`) until they are equal.
2. Phase two: reset `slow` to index `0`; advance both one hop at a time until
   they are equal again.
3. Return the shared index, which is the duplicate value.

#### Invariant

Let `mu` be the tail length, the number of hops from index `0` to the cycle entrance, and `lam` the cycle's length. When phase one ends, `slow` has traveled `mu + x` hops for some meeting offset `x` inside the cycle, and `fast` has traveled twice as far, with the surplus landing in whole laps:

$$ 2(\mu + x) = \mu + x + k\lambda \;\Rightarrow\; \mu + x = k\lambda $$

```text
slow distance to meeting:   mu + x            (0 <= x < lam)
fast distance to meeting:   mu + x + k·lam    (k >= 1 whole extra laps)
twice as far:               2(mu + x) = mu + x + k·lam
=>                          mu + x = k·lam
=>                          (x + mu) mod lam = 0
```

The last line says the meeting offset `x` plus the tail length `mu` lands back on the cycle start. So in phase two, after exactly `mu` hops the reset pointer stands at the entrance for the first time, and the pointer continuing from the meeting point stands at offset `(x + mu) mod lam = 0`, the same node: the two meetings coincide at the entrance, and neither can pass it without meeting there.

#### Walkthrough

Trace both phases on Example 1: `nums = [1,2,3,2,2]`. The edges are `i -> nums[i]`: indices `3` and `4` hold the value `2`, so both point at index `2`, the node with two incoming edges. The walk from index `0` is `0 -> 1 -> 2 -> 3 -> 2 -> 3 -> ...`: a tail of two hops into a two-node cycle between indices `2` and `3`, so `mu = 2` and the entrance is index `2`:

```text
phase 1
start      slow=0  fast=0
hop 1      slow=1  fast=nums[nums[0]]=2
hop 2      slow=2  fast=nums[nums[2]]=2   slow == fast, meet at 2
phase 2
reset      slow=0  fast=2
hop 1      slow=nums[0]=1   fast=nums[2]=3
hop 2      slow=nums[1]=2   fast=nums[3]=2   meet at 2 -> return 2
```

Phase one spends two hops meeting inside the cycle at index `2`, which happens to be the entrance here. Phase two walks `1` and `3` one hop each, and both land on index `2` together. The shared index is `2`, matching the expected Output for Example 1. On Example 2 (`[1,2,3,4,4]`) the walk is `0 -> 1 -> 2 -> 3 -> 4 -> 4 -> 4 ...`, a self-loop at index `4`: the duplicate `4` is its own cycle entrance, and the same two phases return `4`.

#### Solution

The code is the two phases, each a hop loop, with no array writes anywhere.

```python
from typing import List


class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        slow = fast = 0
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        slow = 0
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
        return slow
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Phase one terminates within `mu + lam <= n` hops for `slow` (at most twice that for `fast`), and phase two walks at most `mu` further hops: linear in the array length.

##### Space Complexity: `O(1)`

Two index variables; the array is only read, never written.

#### Key Insights

- The graph reading is the unlock: `i -> nums[i]` with values in `1..n`
  builds a rho shape whose entrance is the duplicate by construction.
- The array plays the role memory played in the hash set: the deterministic
  walk lets the two pointers rediscover the structure instead of storing it.
- This is the only approach with `O(n)` time, `O(1)` space, and an unmodified
  input, which is why it is the canonical interview answer; the cost is that
  it works only under the problem's exact value guarantees.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - one full scan per candidate value.
- **Hash Set**: `O(n)` - one pass with constant-time set operations.
- **Sorting**: `O(n log n)` - the sort dominates one adjacent-compare pass.
- **Binary Search on Count**: `O(n log n)` - `O(log n)` probes at `O(n)` each.
- **Floyd's Cycle Detection**: `O(n)` - a bounded number of linear walks.

### Space Complexity

- **Brute Force**: `O(1)` - a candidate index and a count.
- **Hash Set**: `O(n)` - every distinct value remembered.
- **Sorting**: `O(n)` - the sorted copy (in-place: the sort's own stack).
- **Binary Search on Count**: `O(1)` - two bounds and a counter.
- **Floyd's Cycle Detection**: `O(1)` - two index variables.

### Trade-offs

- The brute force and the hash set are the readability baseline; the set pays
  linear memory to remove the quadratic rescan.
- Sorting spends a sort and (without a copy) the input's original order for
  the simplest constant-extra-memory code.
- Binary search on the value range keeps the input intact at constant space
  but re-reads the array once per probe.
- Floyd's detection is the only combination of linear time, constant space,
  and a read-only input, at the price of the least obvious reasoning.

### When to Use Each

- **Brute Force**: Tiny inputs, or as the oracle when checking faster
  versions.
- **Hash Set**: The default outside interview constraints; two lines and
  linear time.
- **Sorting**: When the input may be reordered anyway and the hash set's
  memory is unwelcome.
- **Binary Search on Count**: When the array is read-only, memory must stay
  constant, and `O(n log n)` time is acceptable.
- **Floyd's Cycle Detection**: When every constraint bites at once, which is
  the problem's canonical follow-up (recommended here).

### Optimization Notes

- The hash set returns at the second copy's position, so early duplicates
  cost far less than the worst case; the brute force has the same early-exit
  behavior but scans per candidate instead of once.
- The binary search needs `count(m) > m` as a strict comparison; a `>=`
  probe would treat a non-duplicated prefix as containing the duplicate.
- Floyd's phase-one loop has no explicit bound; termination rests on the
  walk from index `0` always being rho-shaped, which the `1..n` value range
  guarantees (no edge points at index `0`).
