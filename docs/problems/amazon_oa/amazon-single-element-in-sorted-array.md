# [Single Element in a Sorted Array](https://www.fastprep.io/problems/amazon-single-element-in-sorted-array)

**Medium** | **NN minutes** | **Array, Binary Search**

Given a sorted integer array nums, every value appears exactly twice except for one value that appears exactly once.

Return the value that appears once. Your solution must run in O(log n) time and use O(1) extra space.

## Examples

### Example 1

**Input:** `nums = [1,1,2,3,3,4,4]`

**Output:** `2`

**Explanation:** Every value except 2 belongs to an adjacent pair.

### Example 2

**Input:** `nums = [0]`

**Output:** `0`

**Explanation:** The only element is the unique value.

## Constraints

- `1 <= nums.length <= 100000`
- `nums.length is odd.`
- `-2147483648 <= nums[i] <= 2147483647`
- `nums is sorted in nondecreasing order.`
- `Exactly one value appears once; every other value appears exactly twice.`

## Solutions

### Linear Scan of Aligned Pairs

#### Derivation

The most literal reading uses the one structural fact the sort guarantees: equal values sit next to each other, so the pairs tile the array as `(0, 1), (2, 3), ...` as long as no single element has disturbed the alignment. That makes pairing an index arithmetic question: positions `pair_start` and `pair_start + 1` hold a genuine pair exactly while `pair_start` is even and undisturbed. The first aligned position where the two values differ is where the single element broke the tiling, and it must be the element at `pair_start` itself:

1. Walk `pair_start` over the even positions `0, 2, 4, ...`, stopping before the
   last index.
2. Return `nums[pair_start]` the first time
   `nums[pair_start] != nums[pair_start + 1]`: the tiling broke here, so the
   single is the element that starts this misaligned group.
3. If the walk finishes with no break, every aligned pair is intact and the
   single is the last element, `nums[-1]`.

#### Walkthrough

Example 1, `nums = [1,1,2,3,3,4,4]`, breaks at the first pair after the single:

```text
pair_start 0   nums[0]=1, nums[1]=1 -> intact, keep walking
pair_start 2   nums[2]=2, nums[3]=3 -> broken
               return nums[2] = 2
```

The comparison at `pair_start = 2` is the decisive beat: `2` failed to find its twin next door because the single element sits exactly there, and everything after it shifted by one. The return is `2`, matching the expected Output. On Example 2, `nums = [0]`, the walk range is empty and step 3 returns `nums[-1] = 0`.

#### Solution

The code is the walkthrough's walk: check each aligned pair, return at the first break, fall through to the last element.

```python
from typing import List


class Solution:
    def singleNonDuplicate(self, nums: List[int]) -> int:
        for pair_start in range(0, len(nums) - 1, 2):
            if nums[pair_start] != nums[pair_start + 1]:
                return nums[pair_start]
        return nums[-1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The walk reads two array entries per aligned pair and stops at the break; a single hiding in the last position forces a scan of the whole array.

##### Space Complexity: `O(1)`

One loop index.

#### Key Insights

- Sorted order turns "every value appears twice" into "adjacent aligned pairs", which needs no hashing and no counting.
- If every aligned pair up to `pair_start` is intact, the single cannot sit before `pair_start`: intact pairs consume elements two at a time from the left.
- The linear bound is exactly what the statement's `O(log n)` requirement rules out, so this solution is the baseline an interview answer must state and then beat.

### XOR Fold

#### Derivation

The scan leans on the sort for its pairing. A different question never inspects order at all: if every value could cancel against its twin, which value survives? Exclusive or has exactly that algebra. `value ^ value = 0`, `value ^ 0 = value`, and the operation is commutative and associative, so folding the whole array cancels every paired value regardless of position and leaves only the single element. Where the scan's running time depends on where the break happens, the fold has no data-dependent exit: it always does one uniform pass, and it needs no sortedness at all:

1. Initialize `folded = 0`.
2. Fold every value in: `folded ^= value`.
3. Return `folded`, the one value no twin cancelled.

#### Walkthrough

Example 1 again, `nums = [1,1,2,3,3,4,4]`, folded left to right. Pairs cancel even when adjacent singles sit between them:

```text
value 1   folded 0 -> 1
value 1   folded 1 -> 0    the pair (1, 1) cancelled
value 2   folded 0 -> 2
value 3   folded 2 -> 1
value 3   folded 1 -> 2    the pair (3, 3) cancelled back to 2
value 4   folded 2 -> 6
value 4   folded 6 -> 2    the pair (4, 4) cancelled back to 2
```

The running value is not meaningful mid-fold (association makes any order legal), but the end state is: every paired value appeared an even number of times and vanished, leaving `folded = 2`, the single element and the expected Output. On Example 2, `nums = [0]`, the fold is the single step `folded = 0 ^ 0 = 0`, matching the expected Output.

#### Solution

The code is the walkthrough's three-line fold.

```python
from typing import List


class Solution:
    def singleNonDuplicate(self, nums: List[int]) -> int:
        folded = 0
        for value in nums:
            folded ^= value
        return folded
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass folds every value exactly once, with no early exit to exploit.

##### Space Complexity: `O(1)`

One integer accumulator regardless of input size.

#### Key Insights

- `value ^ value = 0` plus associativity is the whole algorithm: even occurrences cancel, odd occurrences survive.
- The fold ignores the sorted guarantee entirely, so it also answers the unsorted variant of the problem where aligned pairs do not exist.
- Uniform work is a feature and a cost: no data-dependent branch behaves badly, but no input lets it stop early the way the scan's break does.

### Binary Search on Even Midpoints

#### Derivation

Both linear approaches read every element, but the array's structure lets one comparison discard half of it. The single element splits the array into two regions with different parity structure: before the single, every aligned pair is intact, so the element pattern is `(x, x)` at positions `(even, odd)`; from the single onward, the shift breaks every pair, and the pattern becomes `(y, y)` at positions `(odd, even)`. A probe at the midpoint therefore tests which side of the single it landed on, and halving is legal because the predicate is monotone: intact pairs cannot sit after broken ones.

One normalization makes the test single-branched. A midpoint `middle` may land on either parity; nudging an odd `middle` down by one re-aligns it to the even position of its pair. At an aligned `middle`, exactly two things can happen:

- `nums[middle] == nums[middle + 1]`: the pair starting at `middle` is intact,
  so the single is strictly right of the pair: search `[middle + 2, high]`.
- otherwise the pair is broken, and the single is at `middle` or left of it:
  search `[low, middle]`.

Both branches shrink the window, so the loop terminates with `low == high` pinned on the single:

1. Set `low = 0`, `high = len(nums) - 1`.
2. While `low < high`: set `middle = (low + high) // 2`, then `middle -= 1` when
   `middle` is odd.
3. Advance `low = middle + 2` when `nums[middle] == nums[middle + 1]`, otherwise
   lower `high = middle`.
4. Return `nums[low]`.

#### Walkthrough

Example 1, `nums = [1,1,2,3,3,4,4]`, has the single at index `2`; each probe halves the window:

```text
low 0, high 6   middle 3 -> odd, align to 2
                nums[2]=2, nums[3]=3 differ -> pair 2 broken   high = 2
low 0, high 2   middle 1 -> odd, align to 0
                nums[0]=1, nums[1]=1 match -> pair 0 intact    low  = 2
low == high == 2 -> return nums[2] = 2
```

The first probe is the parity beat: raw `middle = 3` sits on the odd side of the broken pair `(2, 3)`, and the alignment nudge to `2` makes the mismatch visible in one comparison. The second probe proves the left half clean, `low` climbs to `2`, and the window closes on the single. On Example 2, `nums = [0]`, the loop body never runs and the return is `nums[0] = 0`.

#### Solution

The code is the walkthrough's probe loop: align the midpoint, compare the pair, halve the window.

```python
from typing import List


class Solution:
    def singleNonDuplicate(self, nums: List[int]) -> int:
        low, high = 0, len(nums) - 1
        while low < high:
            middle = (low + high) // 2
            if middle % 2 == 1:
                middle -= 1
            if nums[middle] == nums[middle + 1]:
                low = middle + 2
            else:
                high = middle
        return nums[low]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

Each iteration performs one comparison and shrinks the window to at most half its size.

##### Space Complexity: `O(1)`

Two boundary indices and one midpoint.

#### Key Insights

- The single element imposes a global parity pattern: intact `(even, odd)` pairs before it, broken `(odd, even)` pairs after it, so any mid-array probe sorts itself to one side.
- Nudging an odd `middle` down to its pair's even position replaces two symmetric probe cases with one, which is where most hand-written versions of this search go wrong.
- Halving is justified by monotonicity, not just by structure: intact pairs never follow broken ones, so the predicate "pair at `middle` intact" is a step function the search can bisect.
- The window always ends on the single: intact-pair probes jump `low` past a whole verified pair, and broken-pair probes keep the break inside `[low, high]`.

## Comparison of Solutions

### Time Complexity

- **Linear Scan of Aligned Pairs**: `O(n)` worst case - reads aligned pairs until the break, which may be the last index.
- **XOR Fold**: `O(n)` - one uniform pass over every value with no early exit.
- **Binary Search on Even Midpoints**: `O(log n)` - one pair comparison per halving step.

### Space Complexity

- **Linear Scan of Aligned Pairs**: `O(1)` - a loop index.
- **XOR Fold**: `O(1)` - one integer accumulator.
- **Binary Search on Even Midpoints**: `O(1)` - two boundaries and a midpoint.

### Trade-offs

- The scan is the shortest to reason about and exits early when the single sits early, but its worst case touches every element and it silently violates the stated `O(log n)` requirement.
- The fold trades early exit for uniformity and independence from the sort: same linear bound, but it also solves the unsorted variant and streams in constant memory.
- The binary search meets the requirement by spending the most care per line: alignment parity is easy to nudge wrong, and its correctness argument is the subtlest of the three.

### When to Use Each

- **Linear Scan of Aligned Pairs**: as the interview opener to establish the pairing structure before beating it, or for tiny inputs where log-time machinery is overhead.
- **XOR Fold**: when the sorted guarantee is absent, when the data streams, or when uniform branch-free behavior matters more than the log factor.
- **Binary Search on Even Midpoints (Recommended)**: the answer the problem asks for: `O(log n)` time and `O(1)` space, satisfying the statement's requirement outright.

### Optimization Notes

- The alignment nudge `middle -= 1` on odd midpoints is the compact form of the alternative (comparing `nums[middle]` against both neighbors with parity-dependent logic); it removes the branch and its boundary bugs.
- `low = middle + 2` rather than `middle + 1` matters: the probe proved a whole pair intact, so both of its elements are discarded at once and `low` always stays on an even index.
- The binary search finds the position of the single; the fold can only report the value. If a follow-up asks where the odd element lives, only the search extends naturally.

