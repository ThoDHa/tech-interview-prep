# [3Sum](https://leetcode.com/problems/3sum/)

**Medium** | **25 minutes** | **Array, Two Pointers, Sorting**

**Pattern:** [Two Pointers](../patterns/two_pointers/intuition.md)

**Algorithm:** [Two-pointer technique](https://usaco.guide/silver/two-pointers) · [Sorting](https://en.wikipedia.org/wiki/Sorting_algorithm) · [Hash table](https://en.wikipedia.org/wiki/Hash_table)

**Practice:** [`practice/3sum/solution.py`](../../practice/3sum/solution.py)

Given an integer array nums, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.

Notice that the solution set must not contain duplicate triplets.

## Examples

### Example 1

**Input:** `nums = [-1,0,1,2,-1,-4]`

**Output:** `[[-1,-1,2],[-1,0,1]]`

**Explanation:**

- `nums[0] + nums[1] + nums[2]` = (-1) + 0 + 1 = 0.
- `nums[0] + nums[3] + nums[4]` = (-1) + 2 + (-1) = 0.
- `nums[1] + nums[2] + nums[4]` = 0 + 1 + (-1) = 0.
The distinct triplets are `[-1, 0, 1]` and `[-1, -1, 2]`. Notice that the order of the output and the order of the triplets does not matter.

### Example 2

**Input:** `nums = [0,1,1]`

**Output:** `[]`

**Explanation:** The only possible triplet does not sum up to 0.

### Example 3

**Input:** `nums = [0,0,0]`

**Output:** `[[0,0,0]]`

**Explanation:** The only possible triplet sums up to 0.

## Constraints

- `3 <= nums.length <= 3000`
- `-10^5 <= nums[i] <= 10^5`

## Deriving the Solution

Every solution rests on the same reformulation: once the first number `nums[i]` is fixed, the rest of the problem is Two Sum, finding a pair that sums to `-nums[i]`. The approaches differ in how that pair is found and in how duplicate triplets are suppressed.

1. **Start literal.** Enumerate every index triple `i < j < k`, keep the zero
   sums, and collapse repeats through a canonical tuple. Correct, but `C(n, 3)` triples cost `O(n^3)`: see [Brute Force](#brute-force).
2. **Spot the waste.** Once `nums[i]` and `nums[j]` are chosen, the third value is
   fully determined: it must equal `-(nums[i] + nums[j])`. The innermost loop is a linear search for a value already known.
3. **Sort and converge.** Sorting lets the pair search run with two pointers
   walking inward: a sum that is too small moves `left` right, one too large moves `right` left, and sortedness proves no valid pair is ever skipped. Sorting also places equal values side by side, so duplicates are skipped by comparing neighbors. Total cost `O(n^2)` with constant extra space: see [Sorting and Two Pointers](#sorting-and-two-pointers).
4. **Or look the complement up.** The determined third value can instead be found
   in a hash set of values already scanned, the direct Two Sum transplant. Same `O(n^2)` time, at the cost of `O(n)` extra space per fixed element: see [Hash Set](#hash-set).

## Solutions

### Brute Force

#### Derivation

The most direct idea is to try every possible triplet of indices and keep the ones that sum to zero. With three distinct indices `i < j < k`, three nested loops enumerate every combination exactly once. The only wrinkle is deduplication: the same three values can appear at different index combinations, so each found triplet is normalized to a canonical order and tracked in a `seen` set.

1. Loop `i` from the first index to `n - 3`, `j` from `i + 1`, and `k` from `j + 1`, covering every unordered triple of positions.
2. When `nums[i] + nums[j] + nums[k] == 0`, sort the three values by hand (a fixed three-element ordering using swaps) to produce a canonical tuple.
3. Use the `seen` set to record canonical tuples, appending a triplet to the result only the first time its canonical form is encountered.

This is correct because every zero-sum triplet of values is enumerated by some index combination, and the canonical-tuple set guarantees each distinct value-triplet is reported exactly once.

#### Walkthrough

Let us watch the brute force run on Example 1: `nums = [-1, 0, 1, 2, -1, -4]` (indices `0` through `5`). The three loops enumerate every index combination `i < j < k`. Most combinations do not sum to zero and are simply skipped; the table below lists only the index triples where `nums[i] + nums[j] + nums[k] == 0`, since those are the only ones that touch `seen` or `result`.

For each zero-sum hit, the three values are sorted by hand into a canonical tuple, then added to `result` only if that tuple is not already in `seen`.

| Hit | `i, j, k` | values `(nums[i], nums[j], nums[k])` | sum | canonical tuple | in `seen`? | action | `result` after |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `0, 1, 2` | `(-1, 0, 1)` | `0` | `(-1, 0, 1)` | no | add | `[[-1, 0, 1]]` |
| 2 | `0, 3, 4` | `(-1, 2, -1)` | `0` | `(-1, -1, 2)` | no | add | `[[-1, 0, 1], [-1, -1, 2]]` |
| 3 | `1, 2, 4` | `(0, 1, -1)` | `0` | `(-1, 0, 1)` | yes | skip (duplicate) | `[[-1, 0, 1], [-1, -1, 2]]` |

Notice hit 3: the values `(0, 1, -1)` form a genuine zero-sum triple at different indices, but their canonical tuple `(-1, 0, 1)` was already recorded by hit 1, so the `seen` set correctly collapses the duplicate and nothing is appended.

After all index combinations are exhausted, the function returns `[[-1, 0, 1], [-1, -1, 2]]`. This matches the expected Output `[[-1,-1,2],[-1,0,1]]`, since the problem states the order of the triplets does not matter.

#### Solution

The code is the triple loop from the walkthrough, with the hand-rolled three-element sort producing the canonical tuple keyed into `seen`.

```python
from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        seen = set()
        result = []

        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    if nums[i] + nums[j] + nums[k] == 0:
                        # Canonicalize the triplet so duplicates collapse:
                        # order the three values, then key on the tuple
                        a, b, c = nums[i], nums[j], nums[k]
                        if a > b:
                            a, b = b, a
                        if b > c:
                            b, c = c, b
                        if a > b:
                            a, b = b, a
                        triplet = (a, b, c)
                        if triplet not in seen:
                            seen.add(triplet)
                            result.append([a, b, c])

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n³)`

The three nested loops examine every combination of three indices, which is `C(n, 3)` triplets, so the work grows cubically. Each triplet does constant work (a sum, a fixed three-element sort, and one set operation).

##### Space Complexity: `O(n²)`

The `seen` set can hold up to one entry per distinct zero-sum triplet, which is `O(n²)` in the worst case (each pair of earlier values can combine with at most one complement). The output array is not counted toward auxiliary space.

#### Key Insights

- **Exhaustive enumeration needs no sorting**: trying all triplets directly is the most self-evident approach and exposes the raw `O(n³)` cost the smarter methods improve on.
- **Deduplication is the real difficulty**: even brute force must collapse repeated value-triplets, here via a canonical tuple stored in a set.
- **The bound is unsustainable**: at the constraint `n = 3000`, roughly `4.5` billion triplets make this too slow for submission, motivating the sorted two-pointer refinement.

### Sorting and Two Pointers

#### Derivation

The brute force wastes its innermost loop searching for a value that is already fully determined: with `nums[i]` and `nums[j]` fixed, only `-(nums[i] + nums[j])` can complete the triplet. The question this approach asks is how to find pairs summing to a known target without scanning blindly, and the answer is the [two-pointer technique](https://usaco.guide/silver/two-pointers) on a sorted array: fix one number, then converge two pointers toward pairs that sum to the negative of the fixed number.

1. **Sort the array**: this enables the two pointers and makes duplicate handling
   easy, since equal values become adjacent.
2. **Fix the first number**: iterate `i` through the array, using each element as
   the first number of the triplet. Only indices up to `n - 2` need checking, since two more elements must follow. Skip `nums[i]` when it equals `nums[i - 1]` to avoid repeated first numbers.
3. **Two-pointer search**: for each fixed `nums[i]`, set `left = i + 1` and
   `right = n - 1` and seek pairs with `nums[left] + nums[right] = -nums[i]`.
4. **Adjust pointers based on `current_sum`**:
    - If the sum equals 0: record the triplet and move both pointers.
    - If the sum is less than 0: increase it by moving `left` right.
    - If the sum is greater than 0: decrease it by moving `right` left.
5. **Handle duplicates after a hit**: skip repeated second and third numbers. The
   two skip loops leave `left` and `right` sitting on the *last* copy of each repeated value, so the unconditional `left += 1` and `right -= 1` that follow them are what actually advance past the recorded pair; without those two lines a triplet with no adjacent duplicates would be appended forever.

Step 4 is exhaustive rather than merely greedy because the array is sorted: when `nums[i] + nums[left] + nums[right] < 0`, every remaining pair that uses `left` is at most as large as the one just tested, so discarding `left` cannot discard an answer. The Invariant below states both properties formally.

#### Invariant

Two properties carry this solution, and the less obvious one is the duplicate skipping.

The two inner `while` loops do not advance *past* a repeated value; they advance *to the last copy of it*. The condition `left < right and nums[left] == nums[left + 1]` tests the element ahead, so the loop exits with `left` still parked on the final element of that run, holding the same value it started on. That is why the unconditional `left += 1` and `right -= 1` follow the skip loops rather than replace them: the skip loops *position* the pointers, and only the increments *move off* the pair just recorded. Delete the increments and a triplet whose neighbors are all distinct leaves both pointers where they were, so the same triplet is appended forever. Delete the skip loops instead and the code still terminates, but a repeated value can emit its triplet more than once, once for each pass that lands the two pointers back on the same pair of values.

The second property is what makes the sign test exhaustive rather than a heuristic. With `nums[i]` fixed, the pair search seeks

$$ \textit{nums}[\textit{left}] + \textit{nums}[\textit{right}] = -\,\textit{nums}[i] $$

```text
nums[left] + nums[right] == -nums[i]     (nums[i] fixed)
```

and the loop maintains that no valid pair lies outside `[left, right]`. Suppose the current sum falls short. Sortedness gives \(\textit{nums}[j] \le \textit{nums}[\textit{right}]\) for every \(j\) with \(\textit{left} < j < \textit{right}\), so

$$ \textit{nums}[\textit{left}] + \textit{nums}[j] \;\le\; \textit{nums}[\textit{left}] + \textit{nums}[\textit{right}] \;<\; -\,\textit{nums}[i] $$

```text
nums[left] + nums[j] <= nums[left] + nums[right] < -nums[i]
        for every j with left < j < right
```

Every pair still available that uses `left` is at most as large as the one just tested, hence also too small. So `left += 1` discards a whole set of candidates *proven* impossible, not merely unpromising, and the mirrored argument justifies `right -= 1`. At `left == right` the window contains no pair, and the invariant reads: no pair completing `nums[i]` was ever skipped.

#### Walkthrough

Let us trace the pointers on Example 1. After `nums.sort()` the array is `[-4, -1, -1, 0, 1, 2]` (indices `0` through `5`). Each line shows the fixed element, the pointer positions, and the decision `current_sum` forces:

```text
i=0 (-4)  left=1 (-1)  right=5 (2)   current_sum = -3 < 0    left += 1
          left=2 (-1)  right=5 (2)   current_sum = -3 < 0    left += 1
          left=3 (0)   right=5 (2)   current_sum = -2 < 0    left += 1
          left=4 (1)   right=5 (2)   current_sum = -1 < 0    left += 1
          left=5 == right                                    pair search ends
i=1 (-1)  left=2 (-1)  right=5 (2)   current_sum = 0         append [-1, -1, 2]
          skip loops idle, left=3, right=4                   (no adjacent dups)
          left=3 (0)   right=4 (1)   current_sum = 0         append [-1, 0, 1]
          skip loops idle, left=4, right=3                   pair search ends
i=2 (-1)  nums[2] == nums[1]                                 skip duplicate first
i=3 (0)   left=4 (1)   right=5 (2)   current_sum = 3 > 0     right -= 1
          left=4 == right                                    pair search ends
```

The `i=0` block shows the invariant in action: every sum is too small, so `left` marches right until the window closes, and no pair is skipped unproven. At `i=1`, the first hit checks `nums[left] == nums[left + 1]` (`-1` vs `0`) and `nums[right] == nums[right - 1]` (`2` vs `1`); neither fires, so only the unconditional increments move the pointers inward to find the second hit. At `i=2` the duplicate first value `-1` is skipped entirely, preventing a repeat of both triplets.

The function returns `[[-1, -1, 2], [-1, 0, 1]]`, matching the expected Output.

#### Solution

The code is the pointer trace written down: the sign of `current_sum` drives the pointers, and the skip loops fire only after a recorded triplet. Because the array is sorted, a positive `nums[i]` means every remaining number is positive too, so no further triplet can reach zero and the outer loop stops early.

```python
from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []
        n = len(nums)

        for i in range(n - 2):
            # Sorted array: once the fixed number is positive, no triplet can sum to 0
            if nums[i] > 0:
                break
            # Skip duplicate values for the first number
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            left, right = i + 1, n - 1

            while left < right:
                current_sum = nums[i] + nums[left] + nums[right]

                if current_sum == 0:
                    result.append([nums[i], nums[left], nums[right]])

                    # Skip duplicates for the second number
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    # Skip duplicates for the third number
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1

                    left += 1
                    right -= 1

                elif current_sum < 0:
                    left += 1
                else:
                    right -= 1

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

- Sorting takes O(n log n) time
- The outer loop runs O(n) times
- For each iteration of the outer loop, the two-pointer inner loop takes O(n) time in the worst case
- Overall: O(n log n) + O(n²) = O(n²)

##### Space Complexity: `O(1)` or `O(n)`

- If we don't count the output array, the space complexity is O(1) as we only use a constant amount of extra variables
- If we count the output array, the space complexity is O(n) in the worst case when there are many valid triplets
- The sorting operation may use O(log n) additional space depending on the implementation

#### Key Insights

- **Two-pointer technique**: After fixing one element, the problem reduces to finding two numbers that sum to a target (similar to Two Sum II on sorted array)
- **Duplicate handling is crucial**: The problem asks for unique triplets, so we must carefully skip duplicates at all three positions to avoid duplicate results
- **Sorted array enables optimization**: Sorting allows us to use two pointers and also makes it easy to skip duplicates by comparing adjacent elements
- **Early termination**: The `nums[i] > 0` break fires as soon as the fixed number turns positive, since all remaining numbers are then positive too and no triplet can sum to zero. The strict `>` matters: breaking on `>= 0` would miss the all-zero triplet `[0, 0, 0]`

### Hash Set

#### Derivation

The two-pointer scan is one way to answer the inner question "has a value that completes this triplet already appeared?"; a [hash set](https://en.wikipedia.org/wiki/Hash_table) answers it directly, the way Two Sum does. Instead of converging two pointers, walk the remainder of the array once and, for every `nums[j]`, ask whether the complement `-(nums[i] + nums[j])` has already been seen. This trades the two-pointer version's constant auxiliary space for a set, in exchange for the more familiar lookup pattern. The array is still sorted first, because adjacency remains the cleanest way to skip duplicate first and second numbers.

1. **Sort the array**: sorting makes duplicate skipping straightforward because
   identical values become adjacent.
2. **Fix the first number**: iterate `i` through the array, skipping any value
   equal to the previous one to avoid repeated triplets.
3. **Scan with a set**: for each fixed element, maintain a `seen` set of values
   encountered so far in the inner loop. Walking `j` from `i + 1` to the end, compute `complement = -(nums[i] + nums[j])`. If that complement is already in `seen`, the three values sum to zero: record `[nums[i], complement, nums[j]]`.
4. **Skip duplicate triplets**: after recording a triplet, advance `j` past any
   consecutive equal values so the same triplet is not added twice. A `while` loop is used here (rather than a `for` loop) precisely so this manual advance of `j` persists.
5. **Record the current value**: add `nums[j]` to `seen` before moving on, so
   future iterations can pair against it.

#### Walkthrough

Let us trace the set scan on Example 1, again with the sorted array `[-4, -1, -1, 0, 1, 2]`. For each fixed `nums[i]`, `seen` starts empty and every inner step computes `complement = -(nums[i] + nums[j])` before adding `nums[j]`:

```text
i=0 (-4)  j=1 (-1)  complement 5    not in seen {}           add -1
          j=2 (-1)  complement 5    not in seen {-1}         add -1 (no change)
          j=3 (0)   complement 4    not in seen {-1}         add 0
          j=4 (1)   complement 3    not in seen {-1, 0}      add 1
          j=5 (2)   complement 2    not in seen {-1, 0, 1}   add 2
i=1 (-1)  seen reset to {}
          j=2 (-1)  complement 2    not in seen {}           add -1
          j=3 (0)   complement 1    not in seen {-1}         add 0
          j=4 (1)   complement 0    in seen {-1, 0}          append [-1, 0, 1]
          j=5 (2)   complement -1   in seen {-1, 0, 1}       append [-1, -1, 2]
i=2 (-1)  nums[2] == nums[1]                                 skip duplicate first
i=3 (0)   j=4 (1)   complement -1   not in seen {}           add 1
          j=5 (2)   complement -2   not in seen {1}          add 2
```

Both hits land while `i` fixes the first `-1`. At `j=4`, the complement `0` was recorded two steps earlier, so `[nums[i], complement, nums[j]] = [-1, 0, 1]` is appended; the duplicate check `nums[j] == nums[j + 1]` (`1` vs `2`) does not fire. At `j=5`, the complement `-1` has been in `seen` since `j=2`, yielding `[-1, -1, 2]`. The `i=2` pass is skipped entirely, which is what prevents both triplets from being found a second time.

The function returns `[[-1, 0, 1], [-1, -1, 2]]`, matching the expected Output (the order of triplets does not matter).

#### Solution

The code is the scan from the walkthrough: one `seen` set per fixed element, a membership test per `j`, and a duplicate skip after each hit.

```python
from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []
        n = len(nums)

        for i in range(n - 2):
            # Skip duplicate values for the first number
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            # Track values already seen for the current fixed element
            seen = set()
            j = i + 1
            while j < n:
                # We need a third value that completes the triplet to zero
                complement = -(nums[i] + nums[j])
                if complement in seen:
                    result.append([nums[i], complement, nums[j]])
                    # Skip duplicate second numbers to keep triplets unique
                    while j + 1 < n and nums[j] == nums[j + 1]:
                        j += 1
                seen.add(nums[j])
                j += 1

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

- Sorting takes O(n log n) time
- The outer loop runs O(n) times
- For each fixed element, the inner scan visits up to O(n) elements with O(1) average set operations
- Overall: O(n log n) + O(n²) = O(n²)

##### Space Complexity: `O(n)`

- The `seen` set holds up to O(n) values for each fixed element
- This is more than the two-pointer approach, which uses only constant auxiliary space

#### Key Insights

- **Set replaces the inner two pointers**: Instead of converging two pointers, we trade O(1) auxiliary space for an O(n) hash set to find complements directly.
- **Sorting still earns its keep**: Although the set handles the lookup, sorting remains the cleanest way to skip duplicate first and second numbers.
- **Same asymptotic cost, different constants**: Both this and the two-pointer method are O(n²) in time, but the hash set adds linear space and incurs hashing overhead per element.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n³)` - Three nested loops enumerate every triplet of indices
- **Sorting and Two Pointers**: `O(n²)` - Sorting is O(n log n), then an O(n) outer loop each drives an O(n) two-pointer scan
- **Hash Set**: `O(n²)` - Sorting is O(n log n), then an O(n) outer loop each drives an O(n) set-based scan

### Space Complexity

- **Brute Force**: `O(n²)` - The `seen` set can hold up to one entry per distinct zero-sum triplet
- **Sorting and Two Pointers**: `O(1)` excluding the output - Uses only a constant number of pointer variables
- **Hash Set**: `O(n)` - Maintains a set of seen values for each fixed element

### Trade-offs

- The brute force is the most self-evident approach and needs no sorting, but its cubic time makes it unusable at the upper constraint and it still pays for deduplication
- The two-pointer approach uses constant auxiliary space and avoids hashing overhead, making it the leaner of the two quadratic methods
- The hash set approach is arguably easier to reason about for those already comfortable with the Two Sum hash pattern, at the cost of linear extra space
- Both quadratic methods rely on sorting to skip duplicates cleanly, so duplicate handling requires equal care in either version

### When to Use Each

- **Brute Force**: Only as a conceptual starting point or for tiny inputs; too slow to submit at `n = 3000`
- **Sorting and Two Pointers**: Preferred for interviews and production due to constant auxiliary space and predictable performance
- **Hash Set**: Useful when extending the familiar Two Sum hash technique to three numbers, or as a teaching bridge from Two Sum to 3Sum

### Optimization Notes

- The brute force can prune slightly by sorting and skipping repeated first values, but it remains cubic; the real speedup comes from replacing the innermost loop with a two-pointer or set scan
- The two-pointer version can break early once the fixed element becomes positive, since no triplet of sorted nonnegative values can sum to zero unless all are zero
- The hash set version reuses a fresh set per fixed element; clearing and reusing a single set can reduce allocations
- The two quadratic approaches share the same sorting step, so the dominant cost difference between them is the auxiliary space of the inner search
