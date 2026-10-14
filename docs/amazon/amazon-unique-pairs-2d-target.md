# [Unique Pairs in a 2D Matrix Summing to Target](https://www.fastprep.io/problems/amazon-unique-pairs-2d-target)

**Easy** | **NN minutes** | **Array, Matrix, Hash Table, Two Pointers**

Given a rectangular integer matrix matrix whose values are globally unique and an integer target, return the number of unordered pairs of values whose sum is target.

Each pair must use two different cells. Count a value pair once regardless of order.

## Examples

### Example 1

**Input:** `matrix = [[1,5],[7,-1]]`, `target = 6`

**Output:** `2`

**Explanation:** The unordered pairs are (1, 5) and (-1, 7).

### Example 2

**Input:** `matrix = [[1,2],[3,4]]`, `target = 5`

**Output:** `2`

**Explanation:** The pairs are (1, 4) and (2, 3).

### Example 3

**Input:** `matrix = [[4]]`, `target = 8`

**Output:** `0`

**Explanation:** The one value cannot be paired with its own cell.

## Constraints

- `1 <= matrix.length, matrix[i].length.`
- `The matrix is rectangular and contains at most 100000 cells.`
- `-10^9 <= matrix[i][j], target <= 10^9.`
- `All matrix values are distinct.`

## Solutions

### Brute Force Pair Scan

#### Derivation

The most literal reading counts pairs: take every unordered pair of distinct cells and count the ones whose values sum to `target`. The grid shape is incidental; what matters is that each value occupies exactly one cell, so "two different cells" is the only restriction. Flattening the cells into a list and scanning every pair of positions with the second position after the first counts each unordered pair exactly once:

1. Collect all values into `values`, in any order, with a double loop over `matrix`.
2. Scan every index pair `first_position < second_position`.
3. When `values[first_position] + values[second_position] == target`, increment `pairs`.
4. Return `pairs`.

#### Walkthrough

Example 1, `matrix = [[1,5],[7,-1]]`, `target = 6`. Flattened, `values = [1, 5, 7, -1]`:

```text
positions (0, 1)   1 + 5  = 6   match,  pairs = 1
positions (0, 2)   1 + 7  = 8   no
positions (0, 3)   1 + -1 = 0   no
positions (1, 2)   5 + 7  = 12  no
positions (1, 3)   5 + -1 = 4   no
positions (2, 3)   7 + -1 = 6   match,  pairs = 2
```

The scan counts the pairs `(1, 5)` and `(7, -1)`, so it returns `2`, matching the expected Output for Example 1.

#### Solution

The code is the flatten plus the half-matrix pair scan from the walkthrough:

```python
from typing import List


class Solution:
    def countPairs(self, matrix: List[List[int]], target: int) -> int:
        """Count unordered pairs of values in different cells that sum to target.

        Time:  O(c^2): every pair of the c cells is summed once.
        Space: O(c): the flattened list of all values.
        """
        values = [value for row in matrix for value in row]
        total_cells = len(values)
        pairs = 0
        for first_position in range(total_cells):
            for second_position in range(first_position + 1, total_cells):
                if values[first_position] + values[second_position] == target:
                    pairs += 1
        return pairs
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(c²)`

With `c` the number of cells, the double loop sums every unordered pair once: `c × (c - 1) / 2` sums. For the stated limit of `100000` cells that is about `5 × 10^9` additions, far beyond an OA time budget.

##### Space Complexity: `O(c)`

The flattened `values` list holds every cell value; the loop indices and `pairs` are constant.

#### Key Insights

- Scanning with `second_position` starting at `first_position + 1` is what counts each unordered pair once and never pairs a cell with itself.
- The values being distinct does not help this approach at all: it never looks values up, it only adds them.
- The approach is correct but quadratic; the constraint `at most 100000 cells` is the signal that a linear pass is expected.

### Hash Set Complement Pass

#### Derivation

The pair scan re-answers, for every cell, a question it could have remembered the answer to: does the complement `target - value` exist among the other cells? A [hash set](https://en.wikipedia.org/wiki/Hash_table) answers that in `O(1)` average time. One pass over the cells, asking about the complement before inserting the current value, gives the correct count of unordered pairs: values already in the set are exactly the earlier cells, and because all matrix values are globally distinct, each complementary pair is discovered exactly once, at its later member. The distinctness guarantee removes the two classic hazards of this pattern: no value can pair with itself across two equal copies, and no pair can be counted twice:

1. Start with an empty `seen` set and `pairs = 0`.
2. Flatten-scan every `value` of `matrix`.
3. Compute `complement = target - value`; when `complement` is in `seen`, increment `pairs`.
4. Add `value` to `seen` and continue; return `pairs` after the scan.

#### Walkthrough

Example 1, `matrix = [[1,5],[7,-1]]`, `target = 6`. Each line is one scan step, with `seen` shown before the lookup:

```text
value 1     seen = {}          complement 5   not present   insert, seen = {1}
value 5     seen = {1}         complement 1   present, pairs = 1
            insert, seen = {1, 5}
value 7     seen = {1, 5}      complement -1  not present   insert
            seen = {1, 5, 7}
value -1    seen = {1, 5, 7}   complement 7   present, pairs = 2
            insert, seen = {1, 5, 7, -1}
```

The lookups hit at values `5` and `-1`, the later members of the pairs `(1, 5)` and `(7, -1)`, so the function returns `2`, matching the expected Output for Example 1. Example 3 (`matrix = [[4]]`, `target = 8`) never hits: the lone cell's complement `4` is looked up in an empty set, and the cell is only inserted afterwards, which is exactly the rule that forbids pairing a value with its own cell.

#### Solution

The code is the walkthrough's per-value lookup-then-insert:

```python
from typing import List


class Solution:
    def countPairs(self, matrix: List[List[int]], target: int) -> int:
        """Count unordered pairs of values in different cells that sum to target.

        Time:  O(c): one pass over the c cells with O(1) average set operations.
        Space: O(c): the set holds every value in the worst case.
        """
        seen: set[int] = set()
        pairs = 0
        for row in matrix:
            for value in row:
                if target - value in seen:
                    pairs += 1
                seen.add(value)
        return pairs
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(c)`

Each of the `c` cells triggers one membership test and one insertion, both `O(1)` on average for a hash set; the flattening is folded into the same scan.

##### Space Complexity: `O(c)`

In the worst case (few or no pairs) `seen` holds every value in the matrix.

#### Key Insights

- Lookup before insert is the invariant: `seen` only ever holds earlier cells, so each unordered pair is counted once, at its later member, and no value ever meets itself.
- Globally distinct values are what make this one-pass form safe: with duplicates, a `target` of twice a value would need count bookkeeping instead of bare membership.
- The two-dimensional layout never matters; the matrix is just a container of unique numbers, and the solution treats it as a stream.

### Sort and Two Pointers

#### Derivation

The hash set buys linear time with linear extra memory. The same count can be found with ordered data and two moving ends: in a sorted sequence, if the extreme values sum to less than `target` the small end must grow, if they sum to more the large end must shrink, and every other pairing is eliminated by the same argument at each step. The matrix is flattened once and sorted, which costs the `O(c log c)` that hashing avoids, and the two-pointer sweep then uses `O(1)` working memory beyond the sorted copy. This is the flattening of [Two Sum's](../leetcode/two_sum.md) sort-based variant, with counting instead of index reporting:

1. Flatten the matrix into `values` and sort it ascending.
2. Point `low` at the start and `high` at the end of `values`.
3. While `low < high`: on a sum equal to `target` count the pair, advance `low`, and retreat `high`; on a smaller sum advance `low`; on a larger sum retreat `high`.
4. Return the count when the pointers meet.

#### Invariant

Every counted pair comes from `values[low] + values[high] == target`, and no pair outside the window `[low, high]` sums to `target` uncounted. The sweep preserves this: when the sum is too small, `values[low]` paired with anything in the window is also too small (the window's maximum partner `values[high]` already failed), so discarding `low` loses nothing; the symmetric argument discards `high` on a too-large sum; on a match, both elements are counted together and the window closes over them. At `low == high` the window holds one element, which cannot pair with itself, so the count is complete.

#### Walkthrough

Example 2, `matrix = [[1,2],[3,4]]`, `target = 5`. Sorted, `values = [1, 2, 3, 4]`:

```text
low=0 (1)   high=3 (4)   1 + 4 = 5   match, pairs = 1   low=1, high=2
low=1 (2)   high=2 (3)   2 + 3 = 5   match, pairs = 2   low=2, high=1
low=2       high=1       low < high fails -> return 2
```

Both matches are found before the pointers cross, so the function returns `2`, matching the expected Output for Example 2.

#### Solution

The code is the sorted window and the advance-or-retreat loop from the walkthrough:

```python
from typing import List


class Solution:
    def countPairs(self, matrix: List[List[int]], target: int) -> int:
        """Count unordered pairs of values in different cells that sum to target.

        Time:  O(c log c): sorting the c flattened values dominates the sweep.
        Space: O(c): the sorted copy of the values.
        """
        values = sorted(value for row in matrix for value in row)
        pairs = 0
        low, high = 0, len(values) - 1
        while low < high:
            current_sum = values[low] + values[high]
            if current_sum == target:
                pairs += 1
                low += 1
                high -= 1
            elif current_sum < target:
                low += 1
            else:
                high -= 1
        return pairs
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(c log c)`

Sorting the `c` flattened values dominates; the two-pointer sweep itself is `O(c)` because every step moves an endpoint inward.

##### Space Complexity: `O(c)`

The sorted `values` list holds all cell values. (Sorting in place after flattening does not change this: the flattened list is itself `O(c)`.)

#### Key Insights

- Each step of the sweep permanently discards one element, which is why the loop cannot miss a pair or count one twice.
- Counting pairs that all share one sum lets the match branch advance both pointers; with duplicates allowed, equal-value runs would need careful run-length arithmetic instead.
- The approach trades the hash set's average-case constant for a guaranteed comparison-based bound and no hashing at all, at the price of `O(c log c)` time.

## Comparison of Solutions

### Time Complexity

- **Brute Force Pair Scan**: `O(c²)` - sums every unordered pair of the `c` cells.
- **Hash Set Complement Pass**: `O(c)` - one pass with average constant-time set operations.
- **Sort and Two Pointers**: `O(c log c)` - sorting dominates the linear sweep.

### Space Complexity

- **Brute Force Pair Scan**: `O(c)` - the flattened value list.
- **Hash Set Complement Pass**: `O(c)` - the seen set in the worst case.
- **Sort and Two Pointers**: `O(c)` - the sorted copy of the values.

### Trade-offs

- **Brute Force Pair Scan**: impossible to get wrong, but quadratic time is unusable at the stated scale of `100000` cells.
- **Hash Set Complement Pass**: linear time and a single pass, spending linear memory on the set and relying on hash average-case behavior.
- **Sort and Two Pointers**: deterministic comparison-based time and no hashing, paying `O(c log c)` and a sorted copy for it.

### When to Use Each

- **Hash Set Complement Pass (Recommended)**: the interview default: fastest, one pass, and the lookup-before-insert discipline is worth stating aloud.
- **Sort and Two Pointers**: when hash worst cases matter, when the data is nearly sorted already, or when memory for the set is better spent on the sorted copy.
- **Brute Force Pair Scan**: only for tiny inputs or as the spoken baseline before improving it.

### Optimization Notes

- The matrix structure is a red herring: all three approaches flatten first, because the pair condition is order-free.
- Lookup before insert is the load-bearing detail of the hash set version; inserting first would let Example 3's single `4` pair with itself and wrongly return `1` for `target = 8`.
- Globally distinct values are what let the hash set store bare membership; with duplicates the set would need value counts, and a `2 × value == target` hit would add `count × (count - 1) / 2` pairs.
- If only the existence of a pair were needed rather than the count, the two-pointer version could sort in place on a mutable input and reach `O(1)` auxiliary space beyond the input.
