# [0/1 Knapsack](https://www.fastprep.io/problems/amazon-zero-one-knapsack)

**Medium** | **NN minutes** | **Dynamic Programming, Array**

You are given two arrays, weights and values, describing n items. Item i has weight weights[i] and value values[i].

Choose a subset of the items whose total weight is at most capacity. Each item may be chosen at most once. Return the maximum total value achievable.

## Examples

### Example 1

**Input:** `weights = [1,3,4,5]`, `values = [1,4,5,7]`, `capacity = 7`

**Output:** `9`

**Explanation:** Choosing the items with weights 3 and 4 uses the full capacity and yields value 4 + 5 = 9.

### Example 2

**Input:** `weights = [2,2,3]`, `values = [6,10,12]`, `capacity = 5`

**Output:** `22`

**Explanation:** The second and third items fit together and yield value 22.

### Example 3

**Input:** `weights = [4,5]`, `values = [8,9]`, `capacity = 3`

**Output:** `0`

**Explanation:** No item fits, so the empty subset is optimal.

## Constraints

- `0 <= weights.length = values.length <= 200`
- `1 <= weights[i] <= 10000`
- `0 <= values[i] <= 1000000`
- `0 <= capacity <= 10000`
- `The maximum answer fits in a signed 32-bit integer.`

## Deriving the Solution

Every item comes with a binary decision, take it or leave it, and the catch is that the best subset for one budget says nothing about the best subset for a slightly smaller one. What does carry over is the budget itself, which turns the problem into a table over (items so far, remaining capacity). The ladder rebuilds that table three ways:

1. **Start literal.** Enumerate every subset, keep the ones that fit, and take the best value: correct, and exponential in the item count: see [Brute Force Subset Enumeration](#brute-force-subset-enumeration).
2. **Memoize the decisions.** The subsets re-decide the same suffix questions (item `i`, budget `c`) over and over; a recursion over that state with a memo computes each answer once: see [Top-Down Memoization](#top-down-memoization).
3. **Fill the table bottom-up.** The memo is a table in disguise: one row of best values per item processed, and the row only ever looks one item back, so a single array swept in descending capacity order replaces the whole grid: see [Bottom-Up Space-Optimized DP](#bottom-up-space-optimized-dp).
4. **Hand the memo to the library.** `functools.cache` implements the memo dict of the top-down version, leaving the recursion bare: see [Memoized with functools.cache](#memoized-with-functoolscache).

## Solutions

### Brute Force Subset Enumeration

#### Derivation

The statement's most literal reading: try every subset the binary decisions allow, discard the ones that break the budget, and report the best value seen:

1. Generate every subset of the `n` items, grouped by size from 0 to `n`.
2. For each subset, sum the weights; skip it when the sum exceeds `capacity`.
3. Otherwise sum the values and keep the maximum in `best`.
4. Return `best`, which stays 0 when nothing fits.

#### Walkthrough

Example 1 (`weights = [1,3,4,5]`, `values = [1,4,5,7]`, `capacity = 7`) has 16 subsets. The fitting ones with the largest values:

```text
{weights 1,3}       total weight 4 <= 7   value 1 + 4 = 5
{weights 1,4}       total weight 5 <= 7   value 1 + 5 = 6
{weights 1,5}       total weight 6 <= 7   value 1 + 7 = 8
{weights 3,4}       total weight 7 <= 7   value 4 + 5 = 9   <- best
{weights 1,3,4}     total weight 8  > 7   discarded
{weights 3,5}       total weight 8  > 7   discarded
{weights 4,5}       total weight 9  > 7   discarded
{weights 1,3,4,5}   total weight 13 > 7   discarded
```

The best fitting subset is `{weights 3,4}` with value 9, matching the expected Output.

#### Solution

```python
from itertools import combinations
from typing import List


class Solution:
    def maximumKnapsackValue(
        self, weights: List[int], values: List[int], capacity: int
    ) -> int:
        best = 0
        for size in range(len(weights) + 1):
            for chosen in combinations(range(len(weights)), size):
                if sum(weights[index] for index in chosen) <= capacity:
                    best = max(best, sum(values[index] for index in chosen))
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n * n)`

`2^n` subsets, each paying up to `n` to sum its weights and values.

##### Space Complexity: `O(n)`

One combination tuple at a time, plus the output.

#### Key Insights

- The enumeration is the definition of the answer, which makes it the oracle every other approach is checked against.
- Nothing is reusable between subsets: siblings differ by one item, yet each re-sums from scratch, and that waste is the ladder's next rung.
- The empty subset is always feasible, so 0 is a lower bound and the answer never goes negative.

### Top-Down Memoization

#### Derivation

The subsets re-solve the same questions. After deciding items `0..i-1` with `c` capacity left, the best achievable value depends only on the pair `(i, c)`, not on which items produced it: two different partial subsets that left the same budget are identical from here on. Recursion over that state with a memo computes each pair once:

1. Define `best_from(index, remaining)`: the best value using only items `index..n-1` with `remaining` capacity.
2. Base case: `index == n` yields 0.
3. Transition: skip item `index` and take `best_from(index + 1, remaining)`; when `weights[index] <= remaining`, also consider taking it: `values[index] + best_from(index + 1, remaining - weights[index])`; keep the max.
4. Memoize every `(index, remaining)` pair and return `best_from(0, capacity)`.

#### Walkthrough

Example 2 (`weights = [2,2,3]`, `values = [6,10,12]`, `capacity = 5`), the decisive corner of the recursion tree:

```text
best_from(0, 5)   take item 0: 6 + best_from(1, 3)
                  skip item 0: best_from(1, 5)

best_from(1, 3)   take item 1: 10 + best_from(2, 1)
                    -> take item 2? weight 3 > 1: no    = 10
                  skip item 1: best_from(2, 3)
                    -> take item 2: 12                  = 12
                  = max(10, 12) = 12

best_from(0, 5)   take branch: 6 + 12 = 18
                  skip branch: best_from(1, 5)
                    -> take item 1: 10 + best_from(2, 3) = 10 + 12 = 22
                    -> skip item 1: best_from(2, 5) = 12
                  = 22
```

The root returns 22, matching the expected Output: items 1 and 2 together weigh 5 and are worth 22.

#### Solution

```python
from typing import Dict, List, Tuple


class Solution:
    def maximumKnapsackValue(
        self, weights: List[int], values: List[int], capacity: int
    ) -> int:
        item_count = len(weights)
        memo: Dict[Tuple[int, int], int] = {}

        def best_from(index: int, remaining: int) -> int:
            if index == item_count:
                return 0
            state = (index, remaining)
            if state in memo:
                return memo[state]
            best = best_from(index + 1, remaining)
            if weights[index] <= remaining:
                best = max(
                    best,
                    values[index] + best_from(index + 1, remaining - weights[index]),
                )
            memo[state] = best
            return best

        return best_from(0, capacity)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * capacity)`

At most `n * capacity` distinct `(index, remaining)` states, each decided in O(1) from two successors.

##### Space Complexity: `O(n * capacity)`

The memo holds one entry per state, plus `O(n)` recursion depth.

#### Key Insights

- The state `(index, remaining)` is the whole problem: history beyond the remaining budget is irrelevant, which is why memoization works.
- The states reachable from `(0, capacity)` are far fewer than the grid: `remaining` only takes the values `capacity` minus sums of weight prefixes.
- Taking item `index` moves both coordinates (`index + 1`, budget shrunk), so an item can never be taken twice.

### Bottom-Up Space-Optimized DP

#### Derivation

The memo is a table with one row per item and one column per remaining budget, and row `index` reads only row `index + 1`. A single array swept in descending capacity order reproduces exactly that: before item `i`'s sweep, `best_value[c]` holds row `i+1`'s value; sweeping `c` downward updates each cell from a not-yet-touched cell of the previous row. Descending order is the whole trick: it stops the sweep from reading its own row, which would let one item count twice:

1. Keep `best_value[0..capacity]`, all zeros: with no items, nothing is achievable.
2. For each item `(weight, value)`: sweep `c` from `capacity` down to `weight`, setting `best_value[c] = max(best_value[c], best_value[c - weight] + value)`.
3. Return `best_value[capacity]`.

#### Recurrence

Let `best_value[c]` be the best value achievable with capacity `c` using only the items processed so far, and let `(w, v)` be the item being processed:

$$ best\_value[c] = \begin{cases}
0, & \text{no items processed} \\[4pt]
\max(best\_value[c],\ best\_value[c - w] + v), & c \ge w,\ \text{swept in descending } c \\[4pt]
best\_value[c], & c < w
\end{cases} $$

```text
best_value[c] = 0                                  with no items processed
best_value[c] = max(best_value[c],
                    best_value[c - w] + v)         for c >= w, descending sweep
best_value[c] = best_value[c]                      for c < w
```

The base row encodes the empty item set, where every budget achieves 0; the bounds come from the statement (weights are at least 1, so cells below `w` cannot fit the item); and the answer is read from `best_value[capacity]` after the last item's sweep. The descending sweep is what makes the two-coordinate recurrence writable in one array: `best_value[c - w]` still holds the previous item's value when cell `c` is updated.

#### Walkthrough

Example 1 (`weights = [1,3,4,5]`, `values = [1,4,5,7]`, `capacity = 7`), the whole array after each item's descending sweep:

```text
                  c =  0  1  2  3  4  5  6  7
start                [ 0  0  0  0  0  0  0  0 ]
item w1 v1           [ 0  1  1  1  1  1  1  1 ]
item w3 v4           [ 0  1  1  4  5  5  5  5 ]
item w4 v5           [ 0  1  1  4  5  6  6  9 ]
item w5 v7           [ 0  1  1  4  5  7  8  9 ]
```

The last sweep's cell `c = 7` takes `max(9, best_value[2] + 7 = 8) = 9`, and `best_value[7] = 9` matches the expected Output: the winning subset is weights 3 and 4. Cell `c = 6` rose to 8 the same way (`best_value[1] + 7`), showing the sweep reading earlier cells of its own row-freeze.

#### Solution

The code is the recurrence written down: one descending sweep per item over the rolling row.

```python
from typing import List


class Solution:
    def maximumKnapsackValue(
        self, weights: List[int], values: List[int], capacity: int
    ) -> int:
        best_value = [0] * (capacity + 1)
        for weight, value in zip(weights, values):
            for remaining in range(capacity, weight - 1, -1):
                best_value[remaining] = max(
                    best_value[remaining], best_value[remaining - weight] + value
                )
        return best_value[capacity]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * capacity)`

One descending sweep of `capacity + 1 - weight` cells per item, `n` items.

##### Space Complexity: `O(capacity)`

The single rolling row, regardless of the item count.

#### Key Insights

- The descending sweep is the entire correctness argument: it keeps `best_value[c - weight]` one row old, so each item contributes at most once.
- Ascending order would turn the 0/1 knapsack into the unbounded one, where an item may repeat; the direction is the difference between the two problems.
- Cells below the item's weight are untouched by that sweep, which is why weights being at least 1 keeps every row readable.

### Memoized with functools.cache

#### Derivation

The Top-Down Memoization version carries its memo by hand: a dict, an `in` check, and a store-back. `functools.cache` implements exactly that bookkeeping for any function whose arguments are hashable, so the recursion stands alone:

1. Define `best_from(index, remaining)` as in the top-down version.
2. Decorate it with `@cache` and delete the hand-rolled `memo` dict.
3. Return `best_from(0, capacity)`.

#### Walkthrough

Example 2 again; the recursion tree is identical to the Top-Down Memoization trace, with the library storing each `(index, remaining)` result on first computation. The second arrival at `best_from(2, 3)` inside the skip branch is where the hand-rolled dict lookup becomes a cache hit, and both versions return 22.

#### Solution

```python
from functools import cache
from typing import List


class Solution:
    def maximumKnapsackValue(
        self, weights: List[int], values: List[int], capacity: int
    ) -> int:
        item_count = len(weights)

        @cache
        def best_from(index: int, remaining: int) -> int:
            if index == item_count:
                return 0
            best = best_from(index + 1, remaining)
            if weights[index] <= remaining:
                best = max(
                    best,
                    values[index] + best_from(index + 1, remaining - weights[index]),
                )
            return best

        return best_from(0, capacity)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * capacity)`

The same state count as the hand-rolled memo; the decorator adds a hash per call.

##### Space Complexity: `O(n * capacity)`

The cache holds one entry per computed state, plus `O(n)` recursion depth.

#### Key Insights

- `cache` replaces the memo's three bookkeeping lines with one decorator; the recurrence is unchanged and easier to read.
- The closure captures `weights` and `values` by reference, so the cache key stays the small `(index, remaining)` pair.
- The bottom-up row remains the space-optimal form: the cache pays for states the sweep never visits, and the sweep pays for cells the recursion never asks about; on this statement either wins.

## Comparison of Solutions

### Time Complexity

- **Brute Force Subset Enumeration**: `O(2^n * n)` - every subset re-summed.
- **Top-Down Memoization**: `O(n * capacity)` - one O(1) decision per reachable state.
- **Bottom-Up Space-Optimized DP**: `O(n * capacity)` - one descending sweep per item.
- **Memoized with functools.cache**: `O(n * capacity)` - the same states with a hashing constant.

### Space Complexity

- **Brute Force Subset Enumeration**: `O(n)` - one subset at a time.
- **Top-Down Memoization**: `O(n * capacity)` - the memo grid plus recursion depth.
- **Bottom-Up Space-Optimized DP**: `O(capacity)` - the rolling row.
- **Memoized with functools.cache**: `O(n * capacity)` - the decorator's cache plus recursion depth.

### Trade-offs

- **Brute Force Subset Enumeration**: the definition, usable as the oracle; exponential time rules it out at the statement's bounds.
- **Top-Down Memoization**: visits only the states the instance needs, at the cost of recursion depth and hand-rolled memo code.
- **Bottom-Up Space-Optimized DP**: the smallest footprint at the same time bound; it fills cells the recursion might never ask about, which costs nothing here since the table is the size of the budget anyway.
- **Memoized with functools.cache**: the top-down form with the bookkeeping removed; same bounds, least code.

### When to Use Each

- **Brute Force Subset Enumeration**: for tiny `n`, and always as the independent checker for the other three.
- **Top-Down Memoization**: when the reachable state space is sparse or the transition ever becomes instance-dependent.
- **Bottom-Up Space-Optimized DP (Recommended)**: the interview default on this statement: linear in the input size times the budget, one array of memory.
- **Memoized with functools.cache**: when writing the recursion first is the fastest path to a correct answer, before deciding to compress it.

### Optimization Notes

- **Bottom-Up Space-Optimized DP** is the recommended choice: `O(n * capacity)` time against the statement's bounds (`n <= 200`, `capacity <= 10000`) leaves a comfortable margin, in one row of memory.
- The inner loop bound `range(capacity, weight - 1, -1)` encodes both the fit check and the direction; changing the direction to ascending silently converts the problem to the unbounded knapsack.
- The statement guarantees the answer fits a signed 32-bit integer; Python needs no care here, but in fixed-width languages the accumulating row is the overflow surface to check.
- An empty item list returns 0 without entering the loop, and `capacity = 0` leaves the single-cell row at 0 unless an item has weight 0, which the constraints exclude.
