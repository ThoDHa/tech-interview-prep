# [Majority Element](https://leetcode.com/problems/majority-element/)

**Easy** | **15 minutes** | **Array, Hash Table, Divide and Conquer**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Algorithm:** [Boyer-Moore majority vote](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_majority_vote_algorithm) · [Hash table](https://en.wikipedia.org/wiki/Hash_table) · [Sorting algorithm](https://en.wikipedia.org/wiki/Sorting_algorithm)

**Practice:** [`practice/majority_element/solution.py`](../../practice/majority_element/solution.py)

Given an array `nums` of size `n`, return the majority element.

The majority element is the element that appears more than `⌊n / 2⌋` times. You may assume that the majority element always exists in the array.

## Examples

### Example 1

**Input:** `nums = [3,2,3]`

**Output:** `3`

### Example 2

**Input:** `nums = [2,2,1,1,1,2,2]`

**Output:** `2`

## Constraints

- `n == nums.length`
- `1 <= n <= 5 * 10^4`
- `-10^9 <= nums[i] <= 10^9`
- The majority element always exists in the array.

## Follow-up

- Could you solve the problem in linear time and in `O(1)` space?

## Deriving the Solution

The guarantee that one value fills more than `⌊n / 2⌋` positions is stronger than "most frequent", and every solution below leans on it: either by counting until some value crosses the threshold, or by exploiting the fact that more than half the positions belong to a single value.

1. **Start literal.** The definition is itself a test: pick each value as a
   candidate, rescan the array to count its occurrences, and return the first one whose count exceeds `n // 2`. Correct, but every candidate pays a full scan, `O(n^2)` in total: see [Brute Force](#brute-force).
2. **Count everything at once.** The rescans keep recounting the same values.
   A single pass with a per-value counter dictionary tallies every value simultaneously; the majority is then the key carrying the largest count. That is linear time, but the dictionary costs `O(n)` extra space: see [Hash Map](#hash-map).
3. **Let position do the counting.** Sorting clusters equal values into runs,
   and a run longer than half the array must cover the middle index, so `nums[n // 2]` is the answer with no counting at all. The extra structure disappears, but the sort costs `O(n log n)` and mutates the input: see [Sorting](#sorting).
4. **Cancel instead of count.** The follow-up demands linear time and `O(1)`
   space, so full tallies are off the table. Pair each non-majority occurrence against one majority occurrence and discard both: a strict majority can never be fully cancelled, so whatever survives the pairing is the answer. One pass, two variables: see [Boyer-Moore Voting Algorithm](#boyer-moore-voting-algorithm).
5. **Or let the library count.** The hash-map idea is exactly what
   `collections.Counter` implements, collapsing the counting solution to one line at the same `O(n)` time and space: see [Counter](#counter).

## Solutions

### Brute Force

#### Derivation

The most direct idea follows straight from the definition: the majority element is the one appearing more than `⌊n / 2⌋` times, so ask each value "is it you?" and answer by counting its occurrences by hand. No observation is needed beyond transcribing the problem statement. The steps:

1. For each `candidate` value in the array, scan the whole array and tally in
   `count` how many times that value appears.
2. As soon as a candidate's `count` exceeds `n // 2`, return it.
3. The trailing `return nums[0]` only satisfies the type signature; the guarantee
   that a majority exists means one candidate always wins first.

#### Walkthrough

Trace the Brute Force solution on Example 1: `nums = [3,2,3]`. Here `n = 3`, so the winning threshold is `n // 2 = 1`: a candidate must appear strictly more than once.

The outer loop picks each value as the `candidate`, and the inner loop rescans the whole array to tally how many times that candidate appears:

| Outer step | `candidate` | Inner scan over `[3,2,3]` | `count` | `count > 1`? | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | `3` (index `0`) | `3==3` yes, `2==3` no, `3==3` yes | `2` | yes | `return 3` |

The very first candidate, `3`, already appears `2` times, which exceeds the threshold of `1`, so the function returns immediately. The loop never reaches the `2` at index `1` or the trailing `return nums[0]`.

The returned value is `3`, which matches the expected Output of `3`.

#### Solution

The code is the nested tally from the walkthrough: an outer candidate loop and an inner counting pass.

```python
from typing import List


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        n = len(nums)
        for candidate in nums:
            count = 0
            for num in nums:
                if num == candidate:
                    count += 1
            if count > n // 2:
                return candidate
        return nums[0]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

For each of the `n` candidates, an inner pass scans all `n` elements to count matches, giving `n * n` work in the worst case.

##### Space Complexity: `O(1)`

Only the scalar `count` and `n` are tracked; no structure grows with the input.

#### Key Insights

- Transcribes the problem definition literally: count each value, return the one
  over half.
- Requires no extra data structures, but pays a quadratic price for it.
- A natural starting point that every later approach exists to speed up.

### Hash Map

#### Derivation

The Brute Force wastes its time recounting: every candidate triggers a fresh scan over values the previous scans already visited. One pass can count every value at the same time by keeping a per-value tally in a [dictionary](https://en.wikipedia.org/wiki/Hash_table); the majority is then whichever key carries the highest count. Because the majority element appears more than `⌊n / 2⌋` times, its count strictly exceeds every other count, so the maximum-count value is guaranteed to be the answer. The steps:

1. Walk the array once, incrementing `counts[num]` for each value.
2. Walk `counts` once, tracking in `majority` the key whose count is largest.
3. Return `majority`.

#### Walkthrough

Let us count Example 2 by hand: `nums = [2,2,1,1,1,2,2]`. The first pass grows `counts` one element at a time:

```text
num = 2    counts = {2: 1}
num = 2    counts = {2: 2}
num = 1    counts = {2: 2, 1: 1}
num = 1    counts = {2: 2, 1: 2}
num = 1    counts = {2: 2, 1: 3}
num = 2    counts = {2: 3, 1: 3}
num = 2    counts = {2: 4, 1: 3}
```

The second pass selects the maximum. `majority` starts as `nums[0] = 2`, and each entry of `counts` challenges it:

```text
entry (2, 4)   4 > counts[2] = 4 ?  no   majority stays 2
entry (1, 3)   3 > counts[2] = 4 ?  no   majority stays 2
```

The first comparison pits the current majority against itself, which the strict `>` correctly rejects, and `1` cannot beat a count of `4`. The function returns `2`, matching the expected Output of `2`.

#### Solution

The code is the two passes from the walkthrough: tally, then select.

```python
from typing import List


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        counts = {}
        for num in nums:
            counts[num] = counts.get(num, 0) + 1

        majority = nums[0]
        for num, count in counts.items():
            if count > counts[majority]:
                majority = num
        return majority
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The first pass over the array is `O(n)`. The dictionary holds at most `n` distinct keys, so the second pass is also `O(n)`. The total is `O(n)`.

##### Space Complexity: `O(n)`

In the worst case (all values distinct except for the majority), the dictionary stores up to `n` key-value pairs.

#### Key Insights

- Intuitive and directly self-derivable: count, then take the most frequent value.
- Works even without the majority guarantee, in which case it returns the mode.
- Trades extra space for simplicity and a single linear scan of counting.

### Boyer-Moore Voting Algorithm

#### Derivation

The Hash Map is linear in time but not in the sense the follow-up wants: it stores a count for every distinct value, `O(n)` space. The question becomes: can the majority be found without remembering any counts at all? The observation that answers it is cancellation. Discard one occurrence of the majority together with one occurrence of anything else, and the majority is still the majority of what remains; conceptually, [each non-majority value cancels out one majority value](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_majority_vote_algorithm). Since the majority element appears more than `⌊n / 2⌋` times, it cannot be fully cancelled and must survive to the end. Tracking that pairing needs only a single `candidate` and a running `count` of its un-cancelled surplus. The steps:

1. When `count` is zero, adopt the current value as the new `candidate`.
2. Increment `count` when `num` matches the candidate, decrement it otherwise.
3. After the pass, the surviving `candidate` is the majority element.

#### Invariant

The problem guarantees a value occurring more than \(\lfloor n/2 \rfloor\) times:

$$ \exists\, m \ :\ \bigl|\{\, i : \text{nums}[i] = m \,\}\bigr| > \frac{n}{2} $$

```text
there exists m with:  number of i such that nums[i] == m  >  n / 2
```

The algorithm never counts occurrences. It maintains, over the prefix processed so far, the invariant that `count` is the surplus of `candidate` over everything else in the *suffix of that prefix* not yet cancelled away:

$$ \textit{count} = \bigl|\{\, j \in S : \text{nums}[j] = \textit{candidate} \,\}\bigr|
              - \bigl|\{\, j \in S : \text{nums}[j] \ne \textit{candidate} \,\}\bigr|
              \ \ge 0 $$

```text
count = (number of j in S with nums[j] == candidate)
      - (number of j in S with nums[j] != candidate)
      >= 0
      where S = the un-cancelled tail of the prefix processed so far
```

Each mismatch pairs off one candidate occurrence against one non-candidate occurrence and discards both; `count == 0` means the prefix has cancelled out completely and carries no information, so any value may be adopted fresh.

Correctness follows from counting: pairing deletes one majority element at most once per deletion, and since \(m\) occupies strictly more than half the array, no sequence of such pairings can exhaust it. Every pairing removes one \(m\) and one non-\(m\), so the strict majority survives to the end.

The strictness matters. With exactly \(n/2\) occurrences the guarantee fails: `[1,1,2,2]` cancels to `count == 0` and returns whichever value came last, which is why the problem states *more than* \(\lfloor n/2 \rfloor\).

#### Walkthrough

Let us run the vote on Example 2: `nums = [2,2,1,1,1,2,2]`. Each line shows one element's effect on `candidate` and `count`:

```text
start      candidate = None   count = 0
num = 2    count == 0 -> adopt candidate = 2, count = 1
num = 2    match     -> count = 2
num = 1    mismatch  -> count = 1
num = 1    mismatch  -> count = 0     prefix fully cancelled
num = 1    count == 0 -> adopt candidate = 1, count = 1
num = 2    mismatch  -> count = 0     prefix fully cancelled
num = 2    count == 0 -> adopt candidate = 2, count = 1
```

Notice the majority temporarily loses the candidacy: after the run of `1`s the first four elements have cancelled out completely (`count == 0`), so `1` is adopted. That is safe precisely because a zeroed prefix carries no information: the majority of the remaining suffix `[2, 2]` is still `2`, which reclaims the candidacy on the final adoption and ends the pass with `count = 1`.

The surviving `candidate` is `2`, which the function returns, matching the expected Output of `2`.

#### Solution

The code is the adopt-and-vote loop from the walkthrough: one branch to adopt, one line to vote.

```python
from typing import List


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        count = 0
        candidate = None

        for num in nums:
            if count == 0:
                candidate = num
            count += 1 if num == candidate else -1

        return candidate
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

A single pass over the array.

##### Space Complexity: `O(1)`

Only two scalar variables are used, regardless of input size.

#### Key Insights

- Satisfies the follow-up: linear time and constant space.
- The pairwise-cancellation argument depends on the strict "more than half" count.
- No sorting and no auxiliary structure, making it ideal for large inputs.

### Sorting

#### Derivation

Instead of counting occurrences, let position reveal the majority. [Sorting](https://en.wikipedia.org/wiki/Sorting_algorithm) gathers all copies of each value into one contiguous run, and a run holding more than half the positions must cover the center of the array: slide it as far left or as far right as it will go, and it still contains index `len(nums) // 2`. The steps:

1. Sort `nums` in place.
2. Return `nums[len(nums) // 2]`, the element at the middle index.

#### Walkthrough

Let us apply this to Example 2: `nums = [2,2,1,1,1,2,2]`, where `n = 7` and the middle index is `len(nums) // 2 = 3`:

```text
nums (input)    [2, 2, 1, 1, 1, 2, 2]
nums.sort()     [1, 1, 1, 2, 2, 2, 2]
index            0  1  2  3  4  5  6
nums[3] = 2
```

Why the middle index is always safe: the four `2`s form one contiguous run after sorting, and a run of `4 > 7 // 2` elements cannot avoid index `3` no matter where it sits:

```text
run leftmost    [2, 2, 2, 2, 1, 1, 1]   run covers indices 0-3, includes 3
run rightmost   [1, 1, 1, 2, 2, 2, 2]   run covers indices 3-6, includes 3
```

Either extreme placement (and every position in between) straddles the center, so `nums[3]` must be the majority value. The function returns `2`, matching the expected Output of `2`.

#### Solution

The code is the two lines the walkthrough justifies: sort, then read the middle.

```python
from typing import List


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        nums.sort()
        return nums[len(nums) // 2]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Dominated by the sort. The single index lookup afterward is `O(1)`.

##### Space Complexity: `O(1)` or `O(n)`

An in-place sort uses `O(1)` auxiliary space; sorts that allocate a copy use `O(n)`. Python's `list.sort` uses `O(n)` in the worst case.

#### Key Insights

- Extremely concise once the center-index observation is made.
- Correctness rests entirely on the "more than half" guarantee filling the middle.
- Slower than linear approaches because of the sort, and it mutates the input.

### Counter

#### Derivation

The Hash Map solution hand-writes machinery the standard library already ships: [`Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) tallies frequencies in one pass, and its `most_common(1)` method performs the maximum-count selection. The whole solution collapses to a single expression. The steps:

1. Build `Counter(nums)`, tallying every value in one pass.
2. Call `.most_common(1)` to obtain the single highest-frequency
   `(value, count)` pair.
3. Take `[0][0]`, the value from that pair, and return it.

#### Walkthrough

Let us trace what the one-liner does internally on Example 1: `nums = [3,2,3]`. `Counter(nums)` builds the same per-value tally the Hash Map builds by hand:

```text
num = 3    counter holds {3: 1}
num = 2    counter holds {3: 1, 2: 1}
num = 3    counter holds {3: 2, 2: 1}

most_common(1)  -> [(3, 2)]     the largest count is 2, held by 3
[0][0]          -> 3            first pair, first component
```

`most_common(1)` scans the tally once for the largest count rather than sorting all entries, and indexing `[0][0]` unwraps the value from the returned pair. The expression evaluates to `3`, matching the expected Output of `3`.

#### Solution

The code compresses the walkthrough's tally and selection into one expression.

```python
from collections import Counter
from typing import List


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        return Counter(nums).most_common(1)[0][0]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Building the `Counter` is `O(n)`. `most_common(1)` finds the single largest entry in `O(n)` rather than sorting all entries.

##### Space Complexity: `O(n)`

The `Counter` stores up to `n` distinct keys, matching the hand-written hash map.

#### Key Insights

- The most concise correct solution, delegating the core work to `collections`.
- Functionally equivalent to the Hash Map approach with the same complexity.
- Requires `from collections import Counter`; prefer it only when a one-liner is acceptable.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - for each candidate, a full inner pass counts matches.
- **Hash Map**: `O(n)` - two linear passes, counting then selecting the maximum.
- **Boyer-Moore Voting Algorithm**: `O(n)` - a single linear pass.
- **Sorting**: `O(n log n)` - dominated by the sort.
- **Counter**: `O(n)` - one pass to tally, one selection of the largest entry.

### Space Complexity

- **Brute Force**: `O(1)` - only a running count and the length are tracked.
- **Hash Map**: `O(n)` - dictionary of per-value counts.
- **Boyer-Moore Voting Algorithm**: `O(1)` - two scalar variables.
- **Sorting**: `O(1)` in place, otherwise `O(n)`.
- **Counter**: `O(n)` - `Counter` of per-value counts.

### Trade-offs

- The Brute Force approach needs no extra space and reads straight off the definition, but its quadratic time is too slow at the upper constraint.
- The Hash Map approach is intuitive and works without the majority guarantee, but spends `O(n)` extra space.
- The Boyer-Moore approach is the most efficient on both axes, at the cost of a less obvious correctness argument.
- The Sorting approach is short but pays an `O(n log n)` cost and mutates the input.
- The Counter approach matches the Hash Map's behavior in a single line, trading explicitness for brevity.

### When to Use Each

- **Brute Force**: Only as a first sketch or for tiny inputs where clarity beats speed.
- **Hash Map**: When readability matters or the majority guarantee may not hold.
- **Boyer-Moore Voting Algorithm**: When optimal time and space are required, especially for large inputs (Recommended for the follow-up).
- **Sorting**: When implementation simplicity outweighs performance.
- **Counter**: When a concise, idiomatic one-liner is acceptable and `O(n)` space is fine.

### Optimization Notes

- Boyer-Moore is the only approach that meets the follow-up's `O(1)` space target; it leverages the strict "more than `⌊n / 2⌋`" guarantee so the candidate can never be fully cancelled.
- When the majority element is not guaranteed to exist, follow Boyer-Moore with a verification pass that counts the candidate's occurrences, or fall back to the Hash Map or Counter approach.
