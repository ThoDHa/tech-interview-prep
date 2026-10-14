# [Single Number](https://leetcode.com/problems/single-number/)

**Easy** | **15 minutes** | **Array, Bit Manipulation**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Algorithm:** [Exclusive or](https://en.wikipedia.org/wiki/Exclusive_or) · [Hash table](https://en.wikipedia.org/wiki/Hash_table) · [Sorting](https://en.wikipedia.org/wiki/Sorting_algorithm)

**Practice:** [`practice/single_number/solution.py`](../../practice/single_number/solution.py)

You are given a **non-empty** array of integers `nums`. Every integer appears twice except for one.

Return the integer that appears only once.

You must implement a solution with $O(n)$ runtime complexity and use only $O(1)$ extra space.

## Examples

### Example 1

**Input:** `nums = [3,2,3]`

**Output:** `2`

### Example 2

**Input:** `nums = [7,6,6,7,8]`

**Output:** `8`

## Constraints

- `1 <= nums.length <= 10000`
- `-10000 <= nums[i] <= 10000`

## Deriving the Solution

The guarantee that exactly one value lacks a partner turns the whole array into a single question: "which value is left over when everything else is paired off?". Every solution below answers that question, differing only in how it detects the unpaired value: by counting it, by ordering it, or by letting arithmetic cancel its partners.

1. **Start literal.** The definition is itself a test: take each value, rescan
   the array to count its occurrences, and return the first one whose count is
   exactly one. Correct, but every candidate pays a full scan, `O(n^2)` in total:
   see [Brute Force](#brute-force).
2. **Count everything at once.** The rescans keep recounting values earlier
   scans already visited. A single pass with a tally dictionary counts every
   value simultaneously; a second pass reads off the key whose count is one.
   That is linear time, but the dictionary costs `O(n)` extra space: see
   [Hash Map](#hash-map).
3. **Spend order instead of memory.** Sorting places every duplicated value's
   two copies in adjacent slots, so one pass of pair comparisons finds the value
   that breaks the pattern without any dictionary. The sort costs
   `O(n log n)`: see [Sorting](#sorting).
4. **Cancel instead of count.** The problem's own demand, linear time and
   `O(1)` extra space, rules out every tally. Exclusive or folds the whole
   array into one accumulator: `x ^ x == 0` erases every pair, `0 ^ v == v`
   keeps the unpaired value, and the fold is order-free. One pass, one integer:
   see [XOR Accumulator](#xor-accumulator).
5. **Or let the library count.** The hash-map tally is exactly what
   [`Counter`](https://docs.python.org/3/library/collections.html#collections.Counter)
   implements; a generator expression over its items picks the count-one value
   in a single expression at the same `O(n)` cost: see [Counter](#counter).

## Solutions

### Brute Force

#### Derivation

The most direct idea follows straight from the definition: the answer is the value appearing once, so ask each value "is it you?" and answer by counting its occurrences by hand. No observation is needed beyond transcribing the problem statement. The steps:

1. For each index `x`, scan the whole array and tally in `count` how many times
   `nums[x]` appears.
2. As soon as a candidate's `count` equals `1`, return `nums[x]`.
3. The trailing `return nums[0]` only satisfies the type signature; the
   guarantee that one value appears once means some candidate always wins first.

#### Walkthrough

Let us run the candidate scan by hand on Example 1: `nums = [3,2,3]`, expected Output `2`.

The outer loop fixes one candidate `nums[x]`, and the inner loop counts its occurrences across the whole array:

```text
x=0  candidate = 3   count over [3,2,3] = 2   count == 1? no   keep scanning
x=1  candidate = 2   count over [3,2,3] = 1   count == 1? yes  -> return 2
```

The first candidate, `3`, appears twice and is skipped. The second candidate, `2`, appears exactly once, so the function returns `2` immediately, matching the expected Output for Example 1. The third position is never reached as a candidate.

#### Solution

The code is the walkthrough's nested scan: an outer candidate loop and an inner counting pass.

```python
from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        n = len(nums)
        for x in range(n):
            count = 0
            for y in range(n):
                if nums[y] == nums[x]:
                    count += 1
            if count == 1:
                return nums[x]
        return nums[0]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

For each of the `n` candidates, an inner pass scans all `n` elements to count matches, giving `n * n` comparisons in the worst case, which hits when the single value sits late in the array.

##### Space Complexity: `O(1)`

Only the scalar `count` and the length `n` are tracked; no structure grows with the input.

#### Key Insights

- Transcribes the problem definition literally: count each value, return the one with a count of one.
- Requires no extra data structures, but pays a quadratic price for it.
- A natural correctness baseline that every later approach exists to speed up.

### Hash Map

#### Derivation

The Brute Force wastes its time recounting: every candidate triggers a fresh scan over values the previous scans already visited. One pass can count every value at the same time by keeping a per-value tally in a [dictionary](https://en.wikipedia.org/wiki/Hash_table); the answer is then whichever key carries the count of exactly one. The steps:

1. Walk the array once, incrementing `counts[num]` for each value.
2. Walk `counts` once and return the first key whose count is `1`.
3. The guarantee that one value appears exactly once means the second walk
   always finds such a key; the trailing return only satisfies the signature.

#### Walkthrough

Let us tally Example 2 by hand: `nums = [7,6,6,7,8]`, expected Output `8`. The first pass grows `counts` one element at a time:

```text
num = 7    counts = {7: 1}
num = 6    counts = {7: 1, 6: 1}
num = 6    counts = {7: 1, 6: 2}
num = 7    counts = {7: 2, 6: 2}
num = 8    counts = {7: 2, 6: 2, 8: 1}
```

The second pass scans the finished tally for the count-one key:

```text
entry (7, 2)   count == 1? no
entry (6, 2)   count == 1? no
entry (8, 1)   count == 1? yes  -> return 8
```

The value `8` is the only key holding a count of `1`, so the function returns `8`, matching the expected Output for Example 2. Both passes are linear and never rescan the array.

#### Solution

The code is the walkthrough's two passes: tally, then select.

```python
from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        counts = {}
        for num in nums:
            counts[num] = counts.get(num, 0) + 1
        for num, count in counts.items():
            if count == 1:
                return num
        return nums[0]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The tally pass visits each of the `n` elements once, and the selection pass visits at most `n` distinct keys. The total is `O(n)`.

##### Space Complexity: `O(n)`

In the worst case the dictionary stores `n / 2 + 1` distinct keys, one per value: linear in the input.

#### Key Insights

- Intuitive and directly self-derivable: count, then pick the count-one value.
- Trades linear extra space for a single linear scan of counting.
- Generalizes unchanged to variants where several values appear odd numbers of times.

### Sorting

#### Derivation

Instead of counting, let position reveal the loner. After [sorting](https://en.wikipedia.org/wiki/Sorting_algorithm), every duplicated value's two copies sit in adjacent slots, so reading the array in pairs `nums[0], nums[1]`, then `nums[2], nums[3]`, and so on, ends exactly when a pair mismatches: the mismatch's left member has no partner and is the answer. If every pair matches, the single value sits at the very end, which the loop's step of two can never absorb into a pair. The steps:

1. Sort `nums` in place.
2. Walk `x` over the pair starts `0, 2, 4, ...` up to `len(nums) - 2`.
3. Return `nums[x]` as soon as `nums[x] != nums[x + 1]`.
4. When the loop finishes without a mismatch, return `nums[-1]`, the unpaired
   survivor at the end.

#### Walkthrough

Let us pair-scan Example 1 by hand: `nums = [3,2,3]` sorts to `[2, 3, 3]`, expected Output `2`:

```text
sorted          [2, 3, 3]
pair x=0        nums[0]=2  vs nums[1]=3   mismatch -> return 2
```

The very first pair mismatches, and its left member `2` is the value without a partner, matching the expected Output for Example 1. The end-fallback matters when the single value sorts last: Example 2's `[7,6,6,7,8]` sorts to `[6, 6, 7, 7, 8]`, the pairs `(6, 6)` and `(7, 7)` both match, the loop exits, and the fallback returns `nums[-1] = 8`, again matching the expected Output.

#### Solution

The code is the walkthrough's pair walk with the end fallback folded in.

```python
from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        nums.sort()
        for x in range(0, len(nums) - 1, 2):
            if nums[x] != nums[x + 1]:
                return nums[x]
        return nums[-1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Dominated by the sort. The pair walk afterward touches each element at most once, `O(n)`.

##### Space Complexity: `O(1)` or `O(n)`

An in-place sort uses `O(1)` auxiliary space; Python's `list.sort` allocates `O(n)` temporary space in the worst case. No additional structure is kept after the sort.

#### Key Insights

- The dictionary disappears: adjacency after sorting answers "is this value paired?" with one comparison.
- The step of two is what pairs the copies; a mismatch at a pair start means the left value is the loner.
- Mutates the input through the in-place sort and pays `O(n log n)`, both avoided by the XOR Accumulator.

### XOR Accumulator

#### Derivation

Both counting approaches pay `O(n)` space and the sorting approach pays `O(n log n)` time, while the problem demands linear time and `O(1)` space. The way out is to stop counting entirely and let [exclusive or](https://en.wikipedia.org/wiki/Exclusive_or) do the pairing. Exclusive or is its own inverse: `x ^ x == 0` for every value, and `0 ^ v == v`, so folding a set of values together erases every value that occurs an even number of times and keeps whatever occurs an odd number of times. Since every value here occurs twice except one, folding the whole array leaves exactly the single value. The fold is also commutative and associative, so the accumulation order never matters: [exclusive or](https://en.wikipedia.org/wiki/Exclusive_or) of the whole array equals the answer no matter how the pairs are interleaved. The steps:

1. Initialize the accumulator `acc` to `0`.
2. For each `num`, fold it in: `acc ^= num`.
3. Return `acc` after the pass.

#### Invariant

The loop maintains one property: after processing `k` elements, `acc` holds the exclusive or of the prefix seen so far:

$$ \textit{acc}_k = \bigoplus_{i=0}^{k-1} \textit{nums}[i] \;\Rightarrow\; \textit{acc}_n = \bigoplus_{i=0}^{n-1} \textit{nums}[i] = \textit{the single value} $$

```text
acc after k steps = XOR of nums[0] .. nums[k-1]
acc after n steps = XOR of the whole array = the single value
    because every paired value cancels:  x ^ x = 0
    and zero keeps the survivor:         0 ^ v = v
```

Each iteration preserves the invariant by definition of the fold: `acc ^= num` extends the prefix by one element. The two identities do the rest: rearranging the whole-array fold into pairs plus the single, every pair collapses to `0`, and the surviving `v` is the value that appears once, which is what the return reports.

#### Walkthrough

Let us fold Example 2 by hand: `nums = [7,6,6,7,8]`, expected Output `8`. Each line shows one fold in binary:

```text
start     acc = 0                 (0000)
num = 7   acc = 0 ^ 7 = 7         (0000 ^ 0111 = 0111)
num = 6   acc = 7 ^ 6 = 1         (0111 ^ 0110 = 0001)
num = 6   acc = 1 ^ 6 = 7         (0001 ^ 0110 = 0111)
num = 7   acc = 7 ^ 7 = 0         (0111 ^ 0111 = 0000)
num = 8   acc = 0 ^ 8 = 8         (0000 ^ 1000 = 1000)
```

Watch the pairs die: the first `7` raises the accumulator to `7`, and the second `7` folds it back to exactly what it held before (`7 ^ 7 = 0` restores the pre-`7` state); the same happens for the two `6`s. After the fourth element the accumulator is back to `0`, carrying nothing from the four paired values, so the final fold leaves `8`, the unpaired value, which matches the expected Output for Example 2.

#### Solution

The code is the walkthrough's fold: one accumulator, one line per element.

```python
from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        acc = 0
        for num in nums:
            acc ^= num
        return acc
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One exclusive-or per element, a single pass with constant work per step.

##### Space Complexity: `O(1)`

One integer accumulator, regardless of input size.

#### Key Insights

- The only approach meeting the problem's own demand: linear time, constant space, no auxiliary structure.
- Correctness rests on two identities, `x ^ x == 0` and `0 ^ v == v`, plus the fold's commutativity and associativity, which make accumulation order irrelevant.
- Negative values need no special handling: exclusive or pairs and cancels any equal integers, whatever their sign, and the single value's sign survives the fold.
- The same fold generalizes: two leftover values appear when exactly two singles exist, and the fold's lowest set bit then splits the array for a second pass.

### Counter

#### Derivation

The Hash Map solution hand-writes machinery the standard library already ships: [`Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) tallies frequencies in one pass, and a generator expression over its items performs the count-one selection. The whole solution collapses to a single expression. The steps:

1. Build `Counter(nums)`, tallying every value in one pass.
2. Run a generator over `.items()` and take the first key whose count is `1`.
3. Return it, wrapped in `next(...)` so the first match stops the scan.

#### Walkthrough

Let us trace what the one-liner does internally on Example 1: `nums = [3,2,3]`, expected Output `2`. `Counter(nums)` builds the same tally the Hash Map builds by hand:

```text
Counter(nums)   {3: 2, 2: 1}        insertion order: 3 first, then 2
next(...)       checks (3, 2) first: count 2, skip
                checks (2, 1) next:  count 1, yield 2
```

The generator scans the tally in insertion order, and `next` stops at the first count-one key, yielding `2`, which matches the expected Output for Example 1.

#### Solution

The code compresses the walkthrough's tally and selection into one expression.

```python
from collections import Counter
from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        return next(num for num, count in Counter(nums).items() if count == 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Building the `Counter` is `O(n)`; the selection scan visits at most `n` distinct keys.

##### Space Complexity: `O(n)`

The `Counter` stores up to `n / 2 + 1` distinct keys, matching the hand-written hash map.

#### Key Insights

- The most concise correct solution, delegating the tally to `collections`.
- Functionally equivalent to the Hash Map approach with the same complexity.
- Like the Hash Map, it keeps `O(n)` space, so it does not meet the problem's `O(1)`-space demand; the XOR Accumulator remains the only approach that does.

## Comparison of Solutions

The practice harness's `practice/single_number/reference.py` implements the **XOR Accumulator** solution.

### Time Complexity

- **Brute Force**: `O(n^2)` - a full array rescan per candidate value.
- **Hash Map**: `O(n)` - one tally pass plus one selection pass.
- **Sorting**: `O(n log n)` - dominated by the sort; the pair walk is linear.
- **XOR Accumulator**: `O(n)` - one exclusive-or per element.
- **Counter**: `O(n)` - one tally pass plus one selection scan.

### Space Complexity

- **Brute Force**: `O(1)` - only the running count.
- **Hash Map**: `O(n)` - the tally dictionary.
- **Sorting**: `O(1)` or `O(n)` - in-place sort auxiliary space; Python's `list.sort` may allocate linearly.
- **XOR Accumulator**: `O(1)` - one integer accumulator.
- **Counter**: `O(n)` - the `Counter` tally.

### Trade-offs

- The Brute Force reads straight off the definition and needs no extra space, but its quadratic time is impractical at the constraint cap.
- The Hash Map is linear and works for any odd-occurrence variant, but keeps a dictionary the problem's space demand forbids.
- The Sorting removes the dictionary by exploiting adjacency, yet still pays `O(n log n)` and reorders the input.
- The XOR Accumulator meets both demands at once, at the cost of the least obvious correctness argument: its proof is two algebraic identities instead of a counting procedure.
- The Counter matches the Hash Map's behavior in a single line, trading explicitness for brevity.

### When to Use Each

- **Brute Force**: a first sketch or tiny inputs where clarity beats everything.
- **Hash Map**: when the tally itself is wanted, or for variants where several values occur an odd number of times.
- **Sorting**: when the input may be reordered freely and no extra structure is allowed but time is not critical.
- **XOR Accumulator** (recommended): the default answer; it is the only approach satisfying the problem's stated linear-time, constant-space contract.
- **Counter**: when a concise, idiomatic one-liner is acceptable and `O(n)` space is fine.

### Optimization Notes

- The XOR fold's order-independence is real parallelism: the array can be partitioned, each chunk folded independently, and the partial results folded together, which matters for arrays too large for one cache pass.
- If the variant allows exactly two unpaired values, fold the whole array into `x ^ y` and split on its lowest set bit: that bit is set in exactly one of the two values, so partitioning elements by it and folding each side again yields the pair.
- Python integers are arbitrary precision, so the accumulator never overflows; in fixed-width languages the accumulator's width must cover the widest value.
- The hash-map family extends unchanged to "every value appears three times except one", where pairs no longer cancel; the XOR fold does not, and that variant needs bit counting by position instead.
