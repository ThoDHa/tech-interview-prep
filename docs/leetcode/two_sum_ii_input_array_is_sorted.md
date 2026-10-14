# [Two Sum II Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)

**Medium** | **25 minutes** | **Array, Two Pointers, Binary Search**

**Pattern:** [Two Pointers](../patterns/two_pointers/intuition.md), [Binary Search](../patterns/binary_search/intuition.md)

**Algorithm:** [Two-pointer technique](https://usaco.guide/silver/two-pointers) · [Binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm)

**Practice:** [`practice/two_sum_ii_input_array_is_sorted/solution.py`](../../practice/two_sum_ii_input_array_is_sorted/solution.py)

Given an array of integers `numbers` that is sorted in **non-decreasing order**.

Return the indices (**1-indexed**) of two numbers, `[index1, index2]`, such that they add up to a given target number `target` and `index1 < index2`. Note that `index1` and `index2` cannot be equal, therefore you may not use the same element twice.

There will always be **exactly one valid solution**.

Your solution must use $O(1)$ additional space.

## Examples

### Example 1

**Input:** `numbers = [1,2,3,4], target = 3`

**Output:** `[1,2]`

**Explanation:** The sum of 1 and 2 is 3. Since we are assuming a 1-indexed array, `index1` = 1, `index2` = 2. We return `[1, 2]`.

## Constraints

- `2 <= numbers.length <= 30000`
- `-1000 <= numbers[i] <= 1000`
- `-1000 <= target <= 1000`

## Deriving the Solution

The problem hands over two facts at once: the pair is unique, and the array is sorted. Uniqueness means the search can stop the moment a match appears; sortedness means every comparison against a candidate pair tells you which of the two candidates to retire permanently. Every solution below exploits one or both facts, and the space limit rules out remembering what was seen.

1. **Start literal.** Test every pair with two nested loops and return the first match. No extra space, correct, but `O(n²)`: see [Brute Force](#brute-force).
2. **Spend the sortedness.** For each element, its partner is a single known value, `target - numbers[x]`, and finding a known value in a *sorted* array is binary search's home turf. That drops one loop for a `O(log n)` lookup, at `O(n log n)`: see [Binary Search for the Complement](#binary-search-for-the-complement).
3. **Search both ends at once.** The two-pointer sweep compares the sum of the extreme candidates against the target and retires one end per step, visiting each element at most once. Linear time and `O(1)` space: see [Two Pointers](#two-pointers).

## Solutions

### Brute Force

#### Derivation

The most direct reading checks every index pair `x < y` until one sums to the target. The sortedness and the uniqueness guarantee are both left unused; only the "exactly one solution" promise lets the search return as soon as it hits the pair:

1. Loop `x` over `0..n-1`.
2. Loop `y` over `x+1..n-1`.
3. When `numbers[x] + numbers[y] == target`, return `[x + 1, y + 1]`, converting to the problem's 1-indexed answer.

#### Walkthrough

Trace the pair scan on Example 1: `numbers = [1,2,3,4]`, `target = 3`:

```text
x=0 (1)   y=1 (2)   1 + 2 = 3 == target -> return [1, 2]
```

The very first pair matches, and the function returns the 1-indexed `[1, 2]`, matching the expected Output. On a larger input the scan is not usually this lucky: the worst case examines all `n(n-1)/2` pairs.

#### Solution

The code is the double loop over index pairs, with the shift to 1-based indexing at the return.

```python
from typing import List


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        length = len(numbers)
        for x in range(length):
            for y in range(x + 1, length):
                if numbers[x] + numbers[y] == target:
                    return [x + 1, y + 1]
        return []
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

Two nested loops examine every pair of indices in the worst case.

##### Space Complexity: `O(1)`

Only the loop indices are stored, satisfying the problem's space constraint.

#### Key Insights

- Meets the `O(1)` space requirement but not the implied time expectation for `n` up to `30000`.
- Correct on any input, sorted or not, which makes it the reference against which the smarter searches are judged.
- The 1-indexed return is the only place the problem's framing touches the code.

### Binary Search for the Complement

#### Derivation

Fixing one element determines the other completely: the partner of `numbers[x]` must be exactly `target - numbers[x]`. Hunting a known value through an *ordered* array is the textbook use of [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm), so the quadratic inner loop collapses to a logarithmic lookup:

1. For each index `x`, compute `complement = target - numbers[x]`.
2. Binary-search for `complement` in the slice *after* `x`, so an element never pairs with itself.
3. On a hit at index `y`, return `[x + 1, y + 1]`.

The slice restriction is what replaces Two Sum's check-before-store trick: searching only `x + 1..` keeps the partner strictly to the right.

#### Walkthrough

Trace the complement search on a case exercising the slice rule: `numbers = [2,3,4]`, `target = 6`:

```text
x=0   numbers[0]=2   complement=4   search 4 in [3,4] (indices 1..2)
      lo=1 hi=2 mid=1 -> 3 < 4 -> lo=2
      lo=2 hi=2 mid=2 -> 4 == 4 -> found y=2
      return [1, 3]
```

The pair `2 + 4 = 6` is found on the first outer step, and the function returns the 1-indexed `[1, 3]`, the correct answer. Note what the slice rule prevented: searching the whole array for `4` from `x = 0` is harmless here, but for `numbers = [3,3]`, `target = 6`, an unrestricted search from `x = 0` could report the element pairing with itself, which the problem forbids.

#### Solution

The code is the fixed element plus the bounded binary search, hand-rolled to keep the space at `O(1)`.

```python
from typing import List


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        length = len(numbers)
        for x in range(length):
            complement = target - numbers[x]
            lo, hi = x + 1, length - 1
            while lo <= hi:
                mid = (lo + hi) // 2
                if numbers[mid] == complement:
                    return [x + 1, mid + 1]
                if numbers[mid] < complement:
                    lo = mid + 1
                else:
                    hi = mid - 1
        return []
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Each of the `n` outer iterations runs one `O(log n)` binary search over the suffix.

##### Space Complexity: `O(1)`

The search keeps only indices and the computed complement.

#### Key Insights

- Converts wasted scanning into informed search: sortedness makes "where is this value?" cheap.
- The suffix-only search is the subtle correctness point, standing in for Two Sum's check-before-store discipline.
- Still re-asks the search once per element; the two-pointer design answers all those questions in one sweep.

### Two Pointers

#### Derivation

The binary search version re-searches from scratch for every fixed element because it learns nothing from its failures. On a sorted array, a failed comparison at the extremes localizes the answer. Stand at both ends and compute `current_sum = numbers[left] + numbers[right]`. If the sum is too small, no pair using `numbers[left]` and anything smaller than `numbers[right]` can reach the target either, since `numbers[right]` was already the largest available partner; `left` is retired. If the sum is too large, `numbers[right]` has no partner among the remaining (larger-than-before) candidates; `right` is retired. Every step permanently eliminates one element, so the sweep is linear:

1. Set `left = 0` and `right = len(numbers) - 1`.
2. While `left < right`, compute `current_sum`.
3. On equality, return `[left + 1, right + 1]` for the 1-indexed answer.
4. If `current_sum < target`, advance `left`; otherwise retreat `right`.

The uniqueness guarantee is what lets the sweep stop at the first match without checking whether another pair also works.

#### Walkthrough

Trace the converging sweep on Example 1: `numbers = [1,2,3,4]`, `target = 3`:

```text
left=0 (1)   right=3 (4)   current_sum = 5 > 3  -> right = 2
left=0 (1)   right=2 (3)   current_sum = 4 > 3  -> right = 1
left=0 (1)   right=1 (2)   current_sum = 3 == 3 -> return [1, 2]
```

Two retirements bring the ends onto the pair, and the function returns the 1-indexed `[1, 2]`, matching the expected Output. A case showing both directions of movement is `numbers = [1,2,3,4,5,6]`, `target = 11`: the sum `7 < 11` advances `left` through `2, 3, 4, 5`, after which `5 + 6 = 11` returns `[5, 6]`, with only `right` never moving.

#### Solution

The code is the walkthrough's sweep: one comparison per step, one pointer moved per step.

```python
from typing import List


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left, right = 0, len(numbers) - 1
        while left < right:
            current_sum = numbers[left] + numbers[right]
            if current_sum == target:
                return [left + 1, right + 1]
            if current_sum < target:
                left += 1
            else:
                right -= 1
        return []
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every iteration retires one element permanently (`left` grows or `right` shrinks), so the loop runs at most `n - 1` times.

##### Space Complexity: `O(1)`

Two indices and one running sum, meeting the problem's explicit space requirement.

#### Key Insights

- The sorted order is what makes each comparison *informative*: too-small or too-large names exactly which end cannot be part of any remaining answer.
- This is the pattern behind Container With Most Water and 3Sum's inner loop; learning it here pays off across the two-pointer family.
- No hash map: the `O(1)` space constraint from the statement rules out Two Sum's approach, and sortedness supplies a free substitute for memory.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n²)` - every index pair is tested in the worst case.
- **Binary Search for the Complement**: `O(n log n)` - one logarithmic search per element.
- **Two Pointers**: `O(n)` - one element retired per sweep step.

### Space Complexity

- **Brute Force**: `O(1)` - two loop indices.
- **Binary Search for the Complement**: `O(1)` - indices and the running complement.
- **Two Pointers**: `O(1)` - two indices and one sum.

### Trade-offs

- **Brute Force** is assumption-free and trivially correct, and unusable at the stated input sizes.
- **Binary Search for the Complement** uses the sortedness locally, one lookup at a time, and is the natural stepping stone to the sweep.
- **Two Pointers** uses the sortedness globally, learning from every comparison, and is the only approach that is simultaneously linear and constant-space.

### When to Use Each

- **Brute Force**: tiny inputs or as the correctness baseline in tests.
- **Binary Search for the Complement**: when the interviewer asks to improve the quadratic version step by step.
- **Two Pointers**: the answer to this problem as stated (recommended here).

### Optimization Notes

- The 1-indexed return (`left + 1`, `right + 1`) is a pure framing detail, but mixing it up is the most common wrong answer on an otherwise correct solution.
- Binary search may also be written with `bisect_left`, but the hand-rolled loop keeps the `O(1)` space claim airtight and the suffix restriction visible.
- Two pointers never revisits a decision: that "each step retires one candidate" argument is the proof of linearity and is worth stating explicitly in an interview.
