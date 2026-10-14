# [Subsets](https://leetcode.com/problems/subsets/)

**Medium** | **30 minutes** | **Array, Backtracking, Bit Manipulation**

**Pattern:** [Backtracking](../patterns/backtracking_exploration/intuition.md)

**Algorithm:** [Power set](https://en.wikipedia.org/wiki/Power_set) · [Backtracking](https://en.wikipedia.org/wiki/Backtracking)

**Practice:** [`practice/subsets/solution.py`](../../practice/subsets/solution.py)

Given an integer array `nums` of unique elements, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.

## Examples

### Example 1

**Input:** `nums = [1,2,3]`

**Output:** `[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]`

### Example 2

**Input:** `nums = [0]`

**Output:** `[[],[0]]`

## Constraints

- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`
- All the numbers of `nums` are unique.

## Deriving the Solution

A subset is fixed by one binary decision per element: each `nums[i]` is either in or out. With `n` elements those independent choices multiply to `2^n` subsets, so every solution below is a different way of enumerating the same `2^n` decision combinations exactly once.

1. **Grow the answer one element at a time.** Every subset of an enlarged array
   either omits the newest element or contains it, so introducing one more element doubles the collection built so far: copy each existing subset, append the new element to the copy, and keep both. Repeating this for all `n` elements yields the full power set with no recursion: see [Iterative Build-Up](#iterative-build-up).
2. **Walk the decisions as a tree.** The doubling loop is awkward to adapt when
   the enumeration needs constraints (a fixed subset size, skipping duplicates). Explore the same decisions depth-first instead: extend a growing `current_subset` with each later element in turn, recurse, and undo the choice on the way back. Every node of that tree is a valid subset: see [Backtracking](#backtracking).
3. **Make the binary fork explicit.** The backtracking version hides the
   per-element in/out choice inside a for loop over candidates. Restating it as exactly two recursive calls per index (skip it, then choose it) exposes the binary decision tree whose `2^n` leaves are the subsets: see [Recursive Choose or Skip](#recursive-choose-or-skip).
4. **Encode the decisions as bits.** Both recursions spend a call stack on what is
   just `n` independent bits. An integer below `2^n` already holds `n` bits, so counting `mask` from `0` to `2^n - 1` enumerates every subset directly, with no recursion and no duplicate bookkeeping: see [Bit Manipulation](#bit-manipulation).

## Solutions

### Iterative Build-Up

#### Derivation

Ask what happens to the [power set](https://en.wikipedia.org/wiki/Power_set) when one more element arrives. Every subset of the enlarged array either omits the new element, in which case it is already in the collection built so far, or contains it, in which case it is an existing subset with the new element appended. So the power set of `k + 1` elements is the power set of `k` elements plus a copy of that power set with the new element added to every member: it exactly doubles. Starting from the power set of zero elements, which is just the empty subset, and applying this doubling once per element builds the whole answer iteratively:

1. Start with `result = [[]]`: the power set of no elements.
2. For each `num`, build `new_subsets` by appending `num` to a copy of every
   `existing_subset` currently in `result` (`existing_subset + [num]` creates the copy).
3. Extend `result` with `new_subsets`, doubling its size.
4. After all `n` elements, `result` holds all `2^n` subsets.

#### Walkthrough

Let us watch the Iterative Build-Up solution run on Example 1: `nums = [1,2,3]`, expected output `[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]`.

`result` starts as `[[]]`: a list containing just the empty subset. Each iteration of the outer loop takes the current `num`, copies every subset already in `result`, appends `num` to each copy, then extends `result` with those new copies. So `result` doubles in size every pass.

| `num` | new_subsets (each existing subset + `[num]`) | `result` after `extend` |
| --- | --- | --- |
| start | (none) | `[[]]` |
| `1` | `[[1]]` | `[[], [1]]` |
| `2` | `[[2], [1,2]]` | `[[], [1], [2], [1,2]]` |
| `3` | `[[3], [1,3], [2,3], [1,2,3]]` | `[[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]` |

Walking the last pass in detail: when `num` is `3`, the loop visits the four existing subsets `[]`, `[1]`, `[2]`, `[1,2]` and builds `[3]`, `[1,3]`, `[2,3]`, `[1,2,3]`. Note that `new_subsets` is built first from a snapshot of `result`, so the four freshly created subsets are not themselves re-processed in the same pass.

After the loop finishes, `result` is `[[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]`, which matches the expected Output.

#### Solution

The code is the doubling pass from the walkthrough: snapshot, copy, extend.

```python
from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        # Start with empty subset
        result = [[]]

        # For each number in input
        for num in nums:
            # Create new subsets by adding current number to all existing subsets
            new_subsets = []
            for existing_subset in result:
                # Create new subset with current number added
                new_subset = existing_subset + [num]
                new_subsets.append(new_subset)

            # Add all new subsets to result
            result.extend(new_subsets)

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n × n)`

For each element (n iterations), we process all existing subsets (up to 2^(i-1) subsets in iteration i) and create new subsets taking O(n) time each.

##### Space Complexity: `O(2^n × n)`

We store all intermediate and final subsets. The result list grows from 1 to 2^n subsets.

#### Key Insights

- Each new element doubles the number of subsets, which is why the result grows from 1 to `2^n` entries.
- Building `existing_subset + [num]` creates a fresh list, so no two result entries alias the same object.
- The approach needs no recursion and no index bookkeeping, making it the easiest to reason about step by step.

### Backtracking

#### Derivation

The Iterative Build-Up commits to producing subsets wholesale, one doubling pass per element, which leaves no natural place to impose constraints such as a fixed subset size or duplicate skipping. Ask instead: can the subsets be enumerated as paths in a tree, where each step decides which element joins next? That is the classic [backtracking](https://en.wikipedia.org/wiki/Backtracking) "choose, explore, unchoose" pattern. A `start_index` parameter restricts each call to elements at or after that index, so elements are only ever appended in index order, which is what prevents `[1, 2]` and `[2, 1]` from both appearing. Unlike permutations, where only complete arrangements count, every partial path here is itself a valid subset, so the current state is recorded at every node of the tree rather than only at the leaves:

1. Define `backtrack(start_index, current_subset)` and launch it as
   `backtrack(0, [])`.
2. On entry, append a copy of the current state (`current_subset[:]`) to
   `result`: every node of the tree is a subset.
3. For each `i` from `start_index` to the end of `nums`: append `nums[i]` to
   `current_subset` (choose), recurse with `backtrack(i + 1, current_subset)` (explore), then `current_subset.pop()` (unchoose) so the next iteration starts from the same state.
4. When the top-level call returns, `result` holds all `2^n` subsets.

#### Walkthrough

Let us run the tree by hand on Example 1: `nums = [1,2,3]`. Each call records `current_subset` first, then loops over the remaining elements, choosing each one, recursing, and popping it back off. The trace below indents one level per recursive call:

```text
backtrack(0, [])                 record []
  append 1 -> [1]                choose nums[0]
  backtrack(1, [1])              record [1]
    append 2 -> [1, 2]           choose nums[1]
    backtrack(2, [1, 2])         record [1, 2]
      append 3 -> [1, 2, 3]      choose nums[2]
      backtrack(3, [1, 2, 3])    record [1, 2, 3]; range(3, 3) is empty
      pop 3 -> [1, 2]            unchoose
    pop 2 -> [1]                 unchoose
    append 3 -> [1, 3]           choose nums[2]
    backtrack(3, [1, 3])         record [1, 3]
    pop 3 -> [1]                 unchoose
  pop 1 -> []                    unchoose
  append 2 -> [2]                choose nums[1]
  backtrack(2, [2])              record [2]
    append 3 -> [2, 3]           choose nums[2]
    backtrack(3, [2, 3])         record [2, 3]
    pop 3 -> [2]                 unchoose
  pop 2 -> []                    unchoose
  append 3 -> [3]                choose nums[2]
  backtrack(3, [3])              record [3]
  pop 3 -> []                    unchoose
```

Reading off the `record` events in order, `result` ends as `[[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]`: the same eight subsets as the expected Output, in a different order, which the problem explicitly allows.

#### Solution

The code is the choose/explore/unchoose tree from the walkthrough, with the record step first in every call.

```python
from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []

        def backtrack(start_index, current_subset):
            # Add current subset to result (creates a copy)
            result.append(current_subset[:])

            # Try adding each remaining element to current subset
            for i in range(start_index, len(nums)):
                # Choose: add nums[i] to current subset
                current_subset.append(nums[i])

                # Explore: recursively build subsets that include nums[i]
                backtrack(i + 1, current_subset)

                # Unchoose: remove nums[i] for next iteration (backtrack)
                current_subset.pop()

        backtrack(0, [])
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n × n)`

There are 2^n subsets to generate, and each subset takes O(n) time to copy into the result array.

##### Space Complexity: `O(2^n × n + n)`

O(2^n × n) for storing all subsets in the result, plus O(n) for the recursion stack depth and current subset tracking.

#### Key Insights

- The `start_index` parameter enforces a canonical element order, which is what prevents `[1, 2]` and `[2, 1]` from both appearing.
- Recording `current_subset[:]` at every node (not just leaves) captures all `2^n` subsets, since every partial path is itself a valid subset.
- Appending a copy is essential; appending `current_subset` directly would leave every result entry pointing at the same list that later gets mutated.

### Recursive Choose or Skip

#### Derivation

The Backtracking tree works, but its loop over candidates blurs the counting argument: where exactly are the `n` binary decisions that make the answer `2^n`? This formulation makes them explicit. Walk the array one index at a time and [recurse](https://en.wikipedia.org/wiki/Recursion_(computer_science)) exactly twice per index: once skipping `nums[index]` and once choosing it. That builds a binary decision tree of depth `n` whose `2^n` root-to-leaf paths are precisely the subsets, and a subset is collected only at the base case, once every element has been decided:

1. Define `generate_subsets(index, current_subset)` and launch it as
   `generate_subsets(0, [])`.
2. Base case: when `index == len(nums)` every element has been decided, so return
   `[current_subset[:]]`, a list holding one finished subset.
3. Otherwise recurse twice: first skip `nums[index]` (leave `current_subset`
   untouched), then choose it (`current_subset.append(nums[index])`, recurse, and `current_subset.pop()` to backtrack).
4. Collect both branches' lists with `result.extend(...)` and return the combined
   list up the tree.

#### Walkthrough

Let us draw the full decision tree on Example 1: `nums = [1,2,3]`. Each internal node forks into a skip branch (taken first) and a choose branch; each leaf at `index == 3` returns a one-subset list, and every internal node returns the concatenation of its two branches:

```text
generate_subsets(0, [])
  skip 1:   generate_subsets(1, [])
    skip 2:   generate_subsets(2, [])
      skip 3:   generate_subsets(3, [])        -> [[]]
      choose 3: generate_subsets(3, [3])       -> [[3]]
    choose 2: generate_subsets(2, [2])
      skip 3:   generate_subsets(3, [2])       -> [[2]]
      choose 3: generate_subsets(3, [2, 3])    -> [[2, 3]]
  choose 1: generate_subsets(1, [1])
    skip 2:   generate_subsets(2, [1])
      skip 3:   generate_subsets(3, [1])       -> [[1]]
      choose 3: generate_subsets(3, [1, 3])    -> [[1, 3]]
    choose 2: generate_subsets(2, [1, 2])
      skip 3:   generate_subsets(3, [1, 2])    -> [[1, 2]]
      choose 3: generate_subsets(3, [1, 2, 3]) -> [[1, 2, 3]]
```

Concatenating the leaves left to right, the root returns `[[], [3], [2], [2,3], [1], [1,3], [1,2], [1,2,3]]`: the same eight subsets as the expected Output, in a different order, which the problem explicitly allows.

#### Solution

The code is the skip-then-choose fork from the walkthrough, collecting subsets only at the `index == len(nums)` leaves.

```python
from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        def generate_subsets(index, current_subset):
            # Base case: processed all elements
            if index == len(nums):
                return [current_subset[:]]  # Return copy of current subset

            # Recursive case: choose or skip current element
            result = []

            # Skip current element: don't include nums[index]
            result.extend(generate_subsets(index + 1, current_subset))

            # Choose current element: include nums[index]
            current_subset.append(nums[index])
            result.extend(generate_subsets(index + 1, current_subset))
            current_subset.pop()  # Backtrack

            return result

        return generate_subsets(0, [])
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n × n)`

We explore 2^n paths in the decision tree, each requiring O(n) time to copy the subset.

##### Space Complexity: `O(2^n × n + n)`

O(2^n × n) for storing results, plus O(n) for recursion stack depth and current subset tracking.

#### Key Insights

- Each element contributes exactly one binary branch (skip then choose), so the recursion tree has `2^n` leaves, one per subset.
- Subsets are collected only at the base case, which keeps the recursion structurally symmetric with the permutation template.
- The skip branch runs before the choose branch, but ordering of the two branches only affects output order, not correctness.

### Bit Manipulation

#### Derivation

Both recursive solutions spend a call stack simulating `n` binary in/out decisions. A machine already has a data type for `n` binary decisions: the bits of an integer. Let bit `i` of a number mean "`nums[i]` is included"; then every integer from `0` to `2^n - 1` describes exactly one subset, and every subset is described by exactly one integer. Iterating a `mask` over that range therefore enumerates the power set with no recursion and no duplicate bookkeeping, decoding each mask into its subset by testing its bits:

1. Let `n = len(nums)` and iterate `mask` over `range(1 << n)`, since `1 << n`
   is `2^n`.
2. For each `mask`, test every bit position `i` with `mask & (1 << i)`; when the
   bit is set, append `nums[i]` to `subset`.
3. Append each decoded `subset` to `result`; after all `2^n` masks, `result` is
   the power set.

#### Formula

The [power set](https://en.wikipedia.org/wiki/Power_set) of an `n`-element set has \(2^n\) members:

$$
|\mathcal{P}(S)| = 2^{n}
$$

```text
number of subsets of nums = 2^n   where n = len(nums)
```

Each element is independently in or out, so there are \(n\) binary choices, and they multiply to \(2^n\). This solution makes that counting argument literal by building a bijection between subsets and the integers below \(2^n\):

$$ \text{mask} \ \longleftrightarrow \ \bigl\{\, \text{nums}[i] \ :\ \text{bit } i \text{ of mask is } 1 \,\bigr\} $$

```text
mask  <-->  { nums[i] : bit i of mask is 1 }
            for mask = 0 .. 2^n - 1
```

Iterating `mask` from \(0\) to \(2^n - 1\) therefore enumerates every subset exactly once, with no recursion and no bookkeeping to avoid duplicates.

The total output size is also worth stating, because it bounds every solution on this page (each element appears in exactly half of the subsets):

$$ \sum_{k=0}^{n} k\binom{n}{k} = n \cdot 2^{\,n-1} $$

```text
sum over k = 0 .. n of k * (n choose k) = n * 2^(n - 1)
```

So even writing the answer down costs \(\Theta(n 2^n)\), and no approach can be asymptotically faster.

#### Walkthrough

Let us decode every mask on Example 1: `nums = [1,2,3]`, so `n = 3` and `mask` runs from `0` to `7`. Each line shows the mask in binary (bit 0 rightmost), the bits that pass the `mask & (1 << i)` test, and the decoded `subset`:

```text
mask = 0  (000)  no bits set                subset []
mask = 1  (001)  bit 0 -> nums[0] = 1       subset [1]
mask = 2  (010)  bit 1 -> nums[1] = 2       subset [2]
mask = 3  (011)  bits 0, 1 -> 1, 2          subset [1, 2]
mask = 4  (100)  bit 2 -> nums[2] = 3       subset [3]
mask = 5  (101)  bits 0, 2 -> 1, 3          subset [1, 3]
mask = 6  (110)  bits 1, 2 -> 2, 3          subset [2, 3]
mask = 7  (111)  bits 0, 1, 2 -> 1, 2, 3    subset [1, 2, 3]
```

Collecting the decoded subsets in mask order gives `[[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]`, which matches the expected Output exactly.

#### Solution

The code is the mask loop from the walkthrough: count through `2^n` integers and decode each one bit by bit.

```python
from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        result = []

        # Iterate through all possible bitmasks from 0 to 2^n - 1
        for mask in range(1 << n):  # 1 << n is 2^n
            subset = []

            # Check each bit position in the current mask
            for i in range(n):
                # If bit i is set in mask, include nums[i] in subset
                if mask & (1 << i):
                    subset.append(nums[i])

            result.append(subset)

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n × n)`

We iterate through 2^n bitmasks, and for each mask, we check n bits and potentially add n elements.

##### Space Complexity: `O(2^n × n)`

For storing all subsets in the result array. The algorithm itself uses O(1) extra space.

#### Key Insights

- The integers `0` to `2^n - 1` enumerate every subset exactly once, with bit `i` deciding whether `nums[i]` is included.
- No recursion stack is needed, so the only extra space beyond the output is a single integer mask.
- This mapping is clean only while `n` is small enough to fit in one machine integer, which the constraint `n ≤ 10` guarantees.

## Comparison of Solutions

### Time Complexity

- **Iterative Build-Up**: `O(2^n × n)` - For each of n elements we process all existing subsets, creating new ones in O(n).
- **Backtracking**: `O(2^n × n)` - There are 2^n subsets to generate, and copying each into the result takes O(n).
- **Recursive Choose or Skip**: `O(2^n × n)` - We explore 2^n paths in the decision tree, each requiring O(n) to copy the subset.
- **Bit Manipulation**: `O(2^n × n)` - We iterate through 2^n bitmasks, checking n bits per mask.

### Space Complexity

- **Iterative Build-Up**: `O(2^n × n)` - Stores all intermediate and final subsets, with higher intermediate space usage.
- **Backtracking**: `O(2^n × n + n)` - O(2^n × n) to store all subsets, plus O(n) for the recursion stack and current subset.
- **Recursive Choose or Skip**: `O(2^n × n + n)` - O(2^n × n) for results, plus O(n) for recursion stack and current subset.
- **Bit Manipulation**: `O(2^n × n)` - For storing all subsets; the algorithm itself uses O(1) extra space.

### Trade-offs

- **Iterative Build-Up**: Non-recursive and easy to follow step-by-step, but uses more intermediate space as subsets are duplicated.
- **Backtracking**: Clear logic that is educational and easily extensible to handle duplicates or constraints, at the cost of recursion overhead.
- **Recursive Choose or Skip**: Makes the binary include or skip choice explicit, but has a more complex recursion structure.
- **Bit Manipulation**: Elegant with a direct integer-to-subset mapping and no recursion, but less intuitive and harder to extend.

### When to Use Each

- **Iterative Build-Up**: For those who prefer iterative solutions or need to understand incremental construction.
- **Backtracking (Recommended)**: Best for interviews: clear, extensible to handle duplicates or constraints.
- **Recursive Choose or Skip**: For educational purposes to understand the binary decision tree structure.
- **Bit Manipulation**: When you want to demonstrate mathematical insight or avoid recursion.

### Optimization Notes

- All four solutions share the same `O(2^n × n)` time complexity because the power set inherently contains 2^n subsets, so none is asymptotically faster than another.
- Backtracking is the recommended approach for interviews: it reads clearly and extends naturally to variations such as subsets with duplicates (sort then skip equal elements) or fixed-size k-combinations.
- Bit manipulation avoids recursion entirely and offers the lowest constant overhead, but only works cleanly when n is small enough for a single integer mask (here n ≤ 10).
- A common pitfall in backtracking is appending `current_subset` directly instead of a copy (`current_subset[:]`); without the copy, all result entries reference the same mutated list.
