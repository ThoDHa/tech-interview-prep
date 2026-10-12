# [First Missing Positive](https://www.fastprep.io/problems/amazon-first-missing-positive)

**Hard** | **NN minutes** | **Array, Hash Table**

Given an unsorted integer array nums, return the smallest positive integer that does not appear in the array.

Your algorithm must run in O(n) time and use O(1) extra space, excluding the input array.

## Examples

### Example 1

**Input:** `nums = [1,2,0]`

**Output:** `3`

**Explanation:** The positive values 1 and 2 are present, so 3 is the first missing positive.

### Example 2

**Input:** `nums = [3,4,-1,1]`

**Output:** `2`

**Explanation:** The value 1 is present but 2 is absent.

### Example 3

**Input:** `nums = [7,8,9,11,12]`

**Output:** `1`

**Explanation:** No value 1 appears.

## Constraints

- `1 <= nums.length <= 100000.`
- `-2^31 <= nums[i] <= 2^31 - 1.`

## Solutions

### Set Membership Scan

#### Derivation

The most literal reading of the problem is a candidate sweep: the answer is `1` unless `1` is present, then `2` unless `2` is present, and so on. A [set](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset) makes each presence test constant time, so the literal version is one pass to build the set plus one candidate loop. The candidate loop can never run away: an array of `n` entries cannot contain all of `1..n+1`, so some candidate in `1..n+1` must be missing:

1. Build `seen` as the set of `nums`.
2. Try `candidate = 1, 2, 3, ...`; return the first candidate not in `seen`.

#### Walkthrough

Example 2, `nums = [3, 4, -1, 1]`:

```text
seen = {3, 4, -1, 1}
candidate 1   in seen -> continue
candidate 2   not in seen -> return 2
```

The return is `2`, matching the expected Output. Example 3, `nums = [7, 8, 9, 11, 12]`, returns at `candidate 1`, also matching.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        """Return the smallest positive integer absent from nums.

        Time:  O(n): one pass builds the set and the candidate loop
            stops within n + 1 tries.
        Space: O(n): the set holds up to n values.
        """
        seen = set(nums)
        candidate = 1
        while candidate in seen:
            candidate += 1
        return candidate
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass builds the set; the candidate loop advances at most `n + 1` times before it must find a gap, each test constant time.

##### Space Complexity: `O(n)`

The set stores up to `n` values.

#### Key Insights

- The candidate loop's bound is a counting argument: if every value `1..n` were present, the answer would be `n + 1`, so the loop exits within `n + 1` tries.
- This version already meets the time bound; only the space fails the problem's `O(1)` requirement, which is what the remaining approaches repair.
- Negative values, zero, and values above `n` are noise: none of them can be a missing candidate below `n + 1`, so any approach may ignore them.

### Sorting Scan

#### Derivation

The set answers membership queries, but the problem only asks one question in order: what is the first gap in the positive values? Sorting lays the values out so that gap becomes a linear walk with a running `expected` counter. The trade is time for space: `O(n log n)` comparisons instead of a hash set, in exchange for in-place sorting. The walk skips non-positive entries and duplicates, advancing `expected` on a match:

1. Sort `nums` in place.
2. Set `expected = 1`; walk `value` over `nums`.
3. Skip `value <= 0` or `value < expected` (duplicates and stale values).
4. When `value == expected`, increment `expected`; when `value > expected`,
   the gap is found.
5. Return `expected` after the walk.

#### Walkthrough

Example 2, `nums = [3, 4, -1, 1]`, sorted to `[-1, 1, 3, 4]`:

```text
expected = 1
value -1   <= 0, skip
value  1   == expected -> expected = 2
value  3   > expected -> gap found, return 2
```

The return is `2`, matching the expected Output.

#### Solution

The code is the sorted walk with the `expected` counter:

```python
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        """Return the smallest positive integer absent from nums.

        Time:  O(n log n): the sort dominates; the scan is linear.
        Space: O(1) auxiliary beyond the sort's internal needs: sorting
            happens in place and two scalars carry the state.
        """
        nums.sort()
        expected = 1
        for value in nums:
            if value < expected:
                continue
            if value == expected:
                expected += 1
            else:
                break
        return expected
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

The in-place sort dominates; the single scan that follows is linear.

##### Space Complexity: `O(1)` auxiliary

Two scalars carry the state, with the sort's internal workspace the only caveat; Python's `list.sort` is not guaranteed constant-space.

#### Key Insights

- Sorting converts "find the missing value" into "walk until a gap", removing the hash set the first approach needed.
- The `value < expected` skip absorbs duplicates and non-positive values in one test.
- The approach misses the problem's `O(n)` time bound, so it is a stepping stone: the remaining approaches recover linear time while keeping space constant.

### Cyclic Sort Placement

#### Derivation

Both earlier approaches spend memory remembering values. The array itself can serve as the memory: value `value`, when it lies in `1..n`, has a natural home at zero-based position `value - 1`. Swapping each value into its home makes the array a permutation table, and after the sweep, the first position whose value disagrees with its index names the missing positive. A value may arrive at a position already holding its correct occupant (a duplicate), so a swap there would loop forever; the guard is to advance whenever `nums[value - 1] == value` already holds:

1. Walk `position` over `nums`.
2. While `1 <= nums[position] <= n` and
   `nums[nums[position] - 1] != nums[position]`, swap `nums[position]` with
   its home slot `nums[nums[position] - 1]`.
3. Scan again: the first `position` with `nums[position] != position + 1`
   returns `position + 1`.
4. When every position agrees, return `n + 1`.

#### Invariant

Every swap places at least one value into its home slot and never removes a placed value: the swapped-in value either is the home occupant now placed, or it was already out of place. The quantity "number of values not at their home position" therefore drops by at least one per swap, and it never rises, since swaps only move values toward their homes. That bounds the total swap work across the whole walk at `n`, which is what makes the nested-looking loop linear:

```text
placed(position) = nums[position] == position + 1
each swap strictly increases the number of placed values
total swaps over the whole walk <= n
```

The loop exits when the current slot holds a home-occupied value, a duplicate, or an out-of-range value; in every case the remaining work belongs to later positions.

#### Walkthrough

Example 2, `nums = [3, 4, -1, 1]`, `n = 4`, values homes at `value - 1`:

```text
position 0   value 3   home slot 2 holds -1 -> swap -> [ -1, 4, 3, 1 ]
             value -1  out of range -> move on
position 1   value 4   home slot 3 holds  1 -> swap -> [ -1, 1, 3, 4 ]
             value 1   home slot 0 holds -1 -> swap -> [  1, -1, 3, 4 ]
             value -1  out of range -> move on
position 2   value 3   home slot 2 holds  3 -> already home, move on
position 3   value 4   home slot 3 holds  4 -> already home, move on
final scan   position 0 holds 1 == 1, position 1 holds -1 != 2 -> return 2
```

The return is `2`, matching the expected Output: value `1` found its home, value `2` is the one positive below `n + 1` with no home occupant.

#### Solution

The code is the placement loop, the final scan, and the `n + 1` fallback:

```python
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        """Return the smallest positive integer absent from nums.

        Time:  O(n): each swap places one value in its home slot for
            good, so total swaps are bounded by n.
        Space: O(1): the input array is rearranged in place.
        """
        length = len(nums)
        for position in range(length):
            while (1 <= nums[position] <= length
                   and nums[nums[position] - 1] != nums[position]):
                home_slot = nums[position] - 1
                nums[position], nums[home_slot] = nums[home_slot], nums[position]

        for position in range(length):
            if nums[position] != position + 1:
                return position + 1
        return length + 1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each swap permanently places one value, so the while body runs at most `n` times across the entire walk; the two passes are linear.

##### Space Complexity: `O(1)`

The input array is rearranged in place; only scalars are allocated, meeting the problem's exclusion of the input array from the space budget.

#### Key Insights

- The array doubles as its own hash table: value `value` lives at index `value - 1`, so membership becomes an index read.
- The duplicate guard `nums[nums[position] - 1] != nums[position]` is the correctness linchpin: without it, two equal values swap places forever.
- Each swap is terminal progress, which converts the apparent `O(n^2)` nesting into `O(n)` total work.
- The input is destroyed; restore it or copy it first when the caller needs the original order.

### Sign-Mark Placement

#### Derivation

The cyclic sort moves values around, but the answer only needs one bit of information per slot: is value `position + 1` present? A value's presence can be recorded in its home slot without displacing anything, by flipping that slot's sign, the classic sign-marking trick. Values are first normalized out of the way (non-positives parked as a sentinel), a marking pass flips home slots negative, and the first slot that stayed positive names the missing value. Because magnitude must survive sign flips, every read goes through `abs`:

1. First pass: replace every `nums[position] <= 0` or `> length` with
   `length + 1`, a value whose presence is irrelevant and whose slot will
   read positive.
2. Second pass: for every `position`, compute `value = abs(nums[position])`;
   when `1 <= value <= length`, set `nums[value - 1] = -abs(nums[value - 1])`.
3. Third pass: return `position + 1` for the first `position` where
   `nums[position] > 0`.
4. When every slot is negative, return `length + 1`.

#### Invariant

After the marking pass, slot `value - 1` is non-positive exactly when some slot held value `value` at marking time: each flip is caused by an occurrence, and `abs` on every read keeps later flips from erasing earlier marks. Negativity is the permanent record; the magnitude underneath it stays readable, which is what lets one array hold both the data and the answer:

```text
marked(value) = nums[value - 1] <= 0 after the marking pass
marking is monotone: a slot only moves from positive to non-positive
answer = smallest value in 1..length with marked(value) false, else length + 1
```

#### Walkthrough

Example 2, `nums = [3, 4, -1, 1]`, `length = 4`:

```text
normalize   -1 out of range -> [ 3, 4, 5, 1 ]
mark position 0   value 3 -> slot 2 negative   [ 3, 4, -5, 1 ]
mark position 1   value 4 -> slot 3 negative   [ 3, 4, -5, -1 ]
mark position 2   abs(-5) = 5, out of range -> no mark
mark position 3   value 1 -> slot 0 negative   [ -3, 4, -5, -1 ]
final scan   slot 1 still positive -> value 2 missing -> return 2
```

The return is `2`, matching the expected Output: values `1`, `3`, and `4` each marked their home slots, and slot `1`, home of value `2`, stayed positive.

#### Solution

The code is the three passes: normalize, mark through `abs`, and scan:

```python
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        """Return the smallest positive integer absent from nums.

        Time:  O(n): three linear passes with constant work each.
        Space: O(1): signs inside the input array carry the marks.
        """
        length = len(nums)

        for position in range(length):
            if nums[position] <= 0 or nums[position] > length:
                nums[position] = length + 1

        for position in range(length):
            value = abs(nums[position])
            if 1 <= value <= length:
                nums[value - 1] = -abs(nums[value - 1])

        for position in range(length):
            if nums[position] > 0:
                return position + 1
        return length + 1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Three linear passes, each doing constant work per element.

##### Space Complexity: `O(1)`

Signs inside the input array carry every mark; only scalars are allocated, meeting the problem's space requirement.

#### Key Insights

- Encoding a boolean in a sign bit is the canonical way to get `O(1)`-space presence tracking over a bounded value range.
- `abs` on every read is what keeps the encoding intact: a marked slot can be marked again by a duplicate without losing its magnitude.
- The sentinel `length + 1` parks out-of-range values where they can neither be marked nor be mistaken for marks, and its own slot reads positive so the final scan never lands on it.
- Compared with cyclic sort, no values move: the array's order is destroyed only in sign, which some would count as gentler, though both leave the caller's data transformed.

## Comparison of Solutions

### Time Complexity

- **Set Membership Scan**: `O(n)` - one set-building pass plus a candidate loop bounded by `n + 1` tries.
- **Sorting Scan**: `O(n log n)` - the in-place sort dominates the linear gap walk.
- **Cyclic Sort Placement**: `O(n)` - each swap places one value permanently, bounding total swaps by `n`.
- **Sign-Mark Placement**: `O(n)` - three linear passes with constant work per element.

### Space Complexity

- **Set Membership Scan**: `O(n)` - the set holds up to `n` values.
- **Sorting Scan**: `O(1)` auxiliary beyond the sort's internal needs - two scalars plus whatever `list.sort` uses.
- **Cyclic Sort Placement**: `O(1)` - the input array is rearranged in place.
- **Sign-Mark Placement**: `O(1)` - signs inside the input array carry the marks.

### Trade-offs

- **Set Membership Scan**: simplest to write and already linear in time, but the `O(n)` set breaks the problem's space requirement.
- **Sorting Scan**: no auxiliary structure, but `O(n log n)` misses the problem's time requirement and Python's sort is not constant-space.
- **Cyclic Sort Placement**: meets both bounds and keeps a strong mental model (every value in its home), at the cost of in-place mutation and the duplicate-swap subtlety.
- **Sign-Mark Placement**: meets both bounds with no data movement, at the cost of the `abs`-read discipline and a three-pass structure that is easier to get subtly wrong.

### When to Use Each

- **Cyclic Sort Placement (Recommended)**: the interview target for this problem: both bounds met, and the home-slot story is easy to narrate while coding.
- **Sign-Mark Placement**: an equally valid `O(n)`/`O(1)` answer when the sign-bit trick comes to mind first; state the `abs` discipline explicitly while writing it.
- **Set Membership Scan**: the spoken baseline that establishes the `n + 1` candidate bound before repairing the space.
- **Sorting Scan**: when the strict bounds are not actually enforced and simplicity outweighs asymptotics.

### Optimization Notes

- Both `O(n)`/`O(1)` approaches hinge on the same observation: only values `1..n` can matter, so an array of `n` slots is exactly the right size for the answer's bookkeeping.
- The cyclic sort's while-loop guard must test the home slot's content (`nums[nums[position] - 1] != nums[position]`), not the current value's presence; testing presence instead of home-occupancy causes infinite swaps on duplicate input.
- The sign-mark approach must read every value through `abs` after normalization, or a later pass misreads a mark as data; this is the most common bug in this family.
- Both approaches destroy the input; if the caller needs `nums` intact, copy it first, and say so in an interview.
