# [Two Sum](https://leetcode.com/problems/two-sum/)

**Easy** | **15 minutes** | **Array, Hash Table**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Algorithm:** [Hash table](https://en.wikipedia.org/wiki/Hash_table) · [Two-pointer technique](https://usaco.guide/silver/two-pointers) · [Sorting](https://en.wikipedia.org/wiki/Sorting_algorithm)

**Practice:** [`practice/two_sum/solution.py`](../../practice/two_sum/solution.py)

Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

## Examples

### Example 1

**Input:** `nums = [2,7,11,15]`, `target = 9`

**Output:** `[0,1]`

**Explanation:** Because `nums[0] + nums[1] == 9`, we return `[0, 1]`.

### Example 2

**Input:** `nums = [3,2,4]`, `target = 6`

**Output:** `[1,2]`

### Example 3

**Input:** `nums = [3,3]`, `target = 6`

**Output:** `[0,1]`

## Constraints

- `2 <= nums.length <= 10^4`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`
- Only one valid answer exists.

## Follow-up

Can you come up with an algorithm that is less than O(n²) time complexity?

## Deriving the Solution

Once one number of the pair is fixed, the other is fully determined: if `nums[x]` is in the answer, its partner must equal `target - nums[x]`. Every solution below asks the same question, "have I seen the complement?", and differs only in how that lookup is performed.

1. **Start literal.** Fix each element in turn and scan the rest of the array
   for its complement. Correct, but the scan repeats for every element and costs `O(n^2)`: see [Brute Force](#brute-force).
2. **Spot the waste.** The inner scan is a search for one known value, yet it
   walks blindly through an unordered suffix every time. Searching is only expensive because the data has no structure to exploit.
3. **Add structure by ordering.** In a sorted sequence the search dissolves
   into a single converging sweep: too small a sum advances the left end, too large retreats the right end. Sorting costs `O(n log n)` and the original indices must be carried along: see [Sort and Two Pointers](#sort-and-two-pointers).
4. **Add structure by memory instead.** A hash map answers "have I seen the
   complement?" in `O(1)` without any ordering: record each value's index as it passes and test each new element against the map. One pass, `O(n)`: see [Hash Map](#hash-map).

## Solutions

### Brute Force

#### Derivation

The most direct reading of the problem examines every possible pair of numbers in the array. For each element, calculate the complement (`target - current number`) and check all remaining elements for this complement; the pair is found the moment the complement appears.

1. Iterate over each index `x` in the array.
2. Compute the complement `target - nums[x]` that would complete the pair.
3. Scan every later index `y` and return `[x, y]` as soon as `nums[y]` equals the complement.

#### Walkthrough

Let us run the pair scan by hand on Example 1: `nums = [2,7,11,15]`, target = `9`.

The outer loop fixes one index `x`, computes `complement = target - nums[x]`, and the inner loop scans every later index `y` looking for a value equal to that complement.

| Step | `x` | `nums[x]` | `complement` | `y` | `nums[y]` | `nums[y] == complement`? |
|------|-----|-----------|--------------|-----|-----------|--------------------------|
| 1    | `0` | `2`       | `9 - 2 = 7`  | `1` | `7`       | yes, `7 == 7`            |

On the very first inner step the complement is found: `nums[0] = 2` and `nums[1] = 7` sum to `9`. The scan stops and reports `[x, y]`, which is `[0, 1]`.

The returned value is `[0, 1]`, which matches the expected Output for Example 1.

#### Solution

The code is the walkthrough's double scan written down: an outer loop fixing `x`, an inner loop hunting the complement.

```python
from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        length = len(nums)
        # Try every pair (x, y) and check whether it sums to the target
        for x in range(length):
            complement = target - nums[x]
            # Only look at later elements so a pair is never counted twice
            for y in range(x + 1, length):
                if nums[y] == complement:
                    return [x, y]
        return []
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

The solution uses nested loops - for each of the `n` elements, we potentially check `n-1` other elements, resulting in `O(n²)` time complexity.

##### Space Complexity: `O(1)`

Only a constant amount of extra space is used regardless of input size.

#### Key Insights

- Simple and intuitive approach that works for all valid inputs
- Inefficient for large arrays due to quadratic time complexity
- No additional data structures required

### Sort and Two Pointers

#### Derivation

The brute force pays because its inner scan searches an unordered suffix by walking all of it. Give the values an order and the search collapses: in a sorted sequence, the smallest and largest remaining candidates sit at the two ends, and their sum can only be corrected in one direction. That is the [two pointers](https://usaco.guide/silver/two-pointers) technique: if the pointed values sum to less than the target, the left pointer moves right to increase the sum; if they sum to more, the right pointer moves left to decrease it. When the sum matches, the pair is found.

Because the problem asks for the original indices, we cannot sort `nums` directly without losing that information. We instead pair each value with its original index before sorting, sort by value, and return the stored original indices when the matching pair is found:

1. Build `indexed = sorted(enumerate(nums), key=lambda pair: pair[1])`, pairing
   each original index with its value and ordering by value.
2. Start `left` at `0` and `right` at the last position of `indexed`.
3. Compare `current_sum = indexed[left][1] + indexed[right][1]` with `target`:
   on a match return the stored original indices `[indexed[left][0], indexed[right][0]]`; if too small, advance `left`; if too large, retreat `right`.

#### Walkthrough

Let us converge the pointers by hand on Example 1: `nums = [2,7,11,15]`, target = `9`. Sorting by value happens to keep this input's order, so `indexed = [(0,2), (1,7), (2,11), (3,15)]`, with each entry holding `(original index, value)`:

```text
left=0 (value 2)   right=3 (value 15)   current_sum = 17 > 9   -> right = 2
left=0 (value 2)   right=2 (value 11)   current_sum = 13 > 9   -> right = 1
left=0 (value 2)   right=1 (value 7)    current_sum = 9 == 9   -> match
```

Every overshoot retreats `right` to shrink the sum, and the ends meet exactly on the pair `2 + 7`. The match reports the stored original indices `[indexed[0][0], indexed[1][0]] = [0, 1]`, matching the expected Output for Example 1. The index bookkeeping earns its keep on inputs the sort actually reorders: Example 2's `[3,2,4]` sorts to values `[2,3,4]`, yet the same procedure still reports the original positions `[1, 2]`.

#### Solution

The code is the converging sweep from the walkthrough, run over the index-carrying `indexed` list.

```python
from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Pair each value with its original index before sorting
        indexed = sorted(enumerate(nums), key=lambda pair: pair[1])
        left, right = 0, len(indexed) - 1
        while left < right:
            current_sum = indexed[left][1] + indexed[right][1]
            if current_sum == target:
                # Return the original indices, not the sorted positions
                return [indexed[left][0], indexed[right][0]]
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        return []
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting dominates the cost at `O(n log n)`, and the two-pointer scan that follows is a single `O(n)` pass.

##### Space Complexity: `O(n)`

Pairing each value with its original index produces a new list of `n` elements, requiring linear additional space.

#### Key Insights

- The two-pointer technique requires a sorted sequence, so sorting is a prerequisite rather than an optimization
- Tracking original indices is essential because the answer is expressed in terms of the unsorted input positions
- Faster than brute force yet slower than the hash map, this approach shines when a sorted order is needed anyway or when extra space for a hash map is undesirable

### Hash Map

#### Derivation

Sorting bought a faster search by rearranging the data, but the question "have I seen the complement?" does not need order at all: it needs memory. A [hash map](https://en.wikipedia.org/wiki/Hash_table) provides exactly that, answering membership questions in `O(1)` on average. Walk the array once, and for each element ask whether its complement has already passed by; if not, record the current value and its index and move on:

1. Iterate over each index `x`, computing `complement = target - nums[x]`.
2. If `complement` is already a key in `nums_dict`, the earlier element and this
   one form the pair: return `[nums_dict[complement], x]`.
3. Otherwise store `nums_dict[nums[x]] = x` and continue.

Checking before storing is what keeps an element from pairing with itself: the map only ever holds strictly earlier elements.

#### Walkthrough

Let us fill the map by hand on Example 2: `nums = [3,2,4]`, target = `6`, which exercises both a miss and a hit:

```text
x=0  nums[0]=3  complement=3  not in {}            store -> nums_dict = {3: 0}
x=1  nums[1]=2  complement=4  not in {3: 0}        store -> nums_dict = {3: 0, 2: 1}
x=2  nums[2]=4  complement=2  in nums_dict! -> return [nums_dict[2], 2] = [1, 2]
```

The complement of `4` is `2`, which was recorded at index `1`, so the function returns `[1, 2]`, matching the expected Output for Example 2. The check-then-store order also handles Example 3's duplicates: on `nums = [3,3]`, index `0` stores `{3: 0}` (its complement `3` is not yet in the empty map), and index `1` finds that stored `3` and returns `[0, 1]` without ever pairing an element with itself.

#### Solution

The code is the walkthrough's single pass: one complement lookup and one store per element.

```python
from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        length = len(nums)
        nums_dict = {}
        for x in range(length):
            complement = target - nums[x]
            # Check if the complement exists in dictionary
            if complement in nums_dict:
                return [nums_dict[complement], x]
            # Store current number and its index
            nums_dict[nums[x]] = x
        return []
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

We traverse the array only once, and hash map operations (lookups and insertions) are `O(1)` on average.

##### Space Complexity: `O(n)`

In worst case, we might need to store nearly all elements in the hash map before finding a solution.

#### Key Insights

- Trades space for time efficiency by using a hash map
- Single-pass algorithm with linear time complexity
- Demonstrates how auxiliary data structures can optimize solutions

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n²)` - Requires nested loops to check all possible pairs
- **Sort and Two Pointers**: `O(n log n)` - Sorting dominates, followed by a single linear two-pointer pass
- **Hash Map**: `O(n)` - Single-pass approach with constant-time lookups

### Space Complexity

- **Brute Force**: `O(1)` - Uses only a constant amount of extra space
- **Sort and Two Pointers**: `O(n)` - Stores value-index pairs to preserve original positions through sorting
- **Hash Map**: `O(n)` - Requires additional storage proportional to input size

### Trade-offs

- The brute force solution is simple to implement and uses minimal memory, but becomes impractically slow for large inputs
- The sort and two pointers solution beats brute force and avoids hashing, but the sort makes it slower than the hash map and the index bookkeeping adds complexity
- The hash map solution is significantly faster for large inputs but requires additional memory

### When to Use Each

- **Brute Force**: Suitable for very small inputs or memory-constrained environments where simplicity is valued over performance
- **Sort and Two Pointers**: Appropriate when the data is already sorted, when a sorted order is needed for other reasons, or when the two-pointer pattern is preferred
- **Hash Map**: Preferred for most practical applications, especially with larger datasets

### Optimization Notes

- The hash map approach demonstrates the classic space-time tradeoff in algorithm design
- By using a hash map to store previously seen values, we eliminate the need for the inner loop in the brute force approach
- The sort and two pointers approach removes the inner loop differently, by exploiting sorted order rather than a lookup table, but pays an `O(n log n)` sorting cost
- This is a common pattern in solving array problems: using additional data structures to achieve linear time complexity
