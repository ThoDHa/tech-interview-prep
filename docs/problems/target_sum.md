# [Target Sum](https://leetcode.com/problems/target-sum/)

**Medium** | **25 minutes** | **Array, Dynamic Programming, Backtracking**

**Pattern:** [DP Knapsack/Subset](../patterns/dp_knapsack_subset/intuition.md)

**Algorithm:** [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization) · [Backtracking](https://en.wikipedia.org/wiki/Backtracking)

**Practice:** [`practice/target_sum/solution.py`](../../practice/target_sum/solution.py)

You are given an array of integers `nums` and an integer `target`.

For each number in the array, you can choose to either add or subtract it to a total sum.

* For example, if `nums = [1, 2]`, one possible sum would be `"+1-2=-1"`.

If `nums=[1,1]`, there are **two different ways** to sum the input numbers to get a sum of `0`: `"+1-1"` and `"-1+1"`.

Return the number of **different ways** that you can build the expression such that the total sum equals `target`.

## Examples

### Example 1

**Input:** `nums = [2,2,2], target = 2`

**Output:** `3`

**Explanation:** There are 3 different ways to sum the input numbers to get a sum of 2.
`+2 +2 -2 = 2`
`+2 -2 +2 = 2`
`-2 +2 +2 = 2`

## Constraints

- `1 <= nums.length <= 20`
- `0 <= nums[i] <= 1000`
- `-1000 <= target <= 1000`

## Deriving the Solution

Every expression assigns each number a sign, so there are `2^n` candidate expressions and the task is to count the ones that evaluate to `target`. The sign assignment has two equivalent readings: a left-to-right accumulation of `+nums[i]` and `-nums[i]` choices, or a split of the numbers into a positive set `P` and a negative set `N`. The second reading hides an algebraic shortcut that the accumulation cannot see.

1. **Start literal.** Walk the array choosing a sign per number and count the
   paths whose total equals `target`. That enumerates all `2^n` expressions:
   see [Brute Force Enumeration](#brute-force-enumeration).
2. **Cache the states.** A branch's future depends only on `(index, current
   total)`, not on which signs produced the total, so the same states recur
   across sign histories. Memoizing them collapses the tree to one solve per
   state: see [Top-Down Memoization](#top-down-memoization).
3. **Reframe algebraically.** With `P` the sum of positively signed numbers
   and `N` the sum of negatively signed ones, `P - N = target` and
   `P + N = total`, so `P = (total + target) / 2`: counting expressions is
   counting subsets with one fixed sum. Tabulate the subsets: see
   [Bottom-Up 2-D DP](#bottom-up-2-d-dp).
4. **Keep one row.** Each subset-count cell reads only the row above, so one
   row swept right to left per number carries the whole table:
   see [Space-Optimized 1-D DP](#space-optimized-1-d-dp).
5. **Hand the cache to the library.** Step 2's memo dict is bookkeeping, not
   logic. Decorating the recursion with `functools.cache` deletes the lookup
   and the store while the sign fork and the base case stay exactly as
   written: see
   [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Brute Force Enumeration

#### Derivation

The most literal reading builds each expression one number at a time. Walking left to right, number `i` either joins the running total as `+nums[i]` or as `-nums[i]`; the expression is complete when every number has a sign, and it counts when the total hits `target`:

1. Define `dfs(i, current)` as the number of sign choices for `nums[i:]` that
   turn the running total `current` into `target`.
2. When `i == len(nums)`, the expression is complete: return `1` when
   `current == target`, else `0`.
3. Otherwise return `dfs(i + 1, current + nums[i]) + dfs(i + 1, current - nums[i])`.
4. Return `dfs(0, 0)`.

#### Walkthrough

The tree is small enough on Example 1 to list whole: `nums = [2,2,2]`, `target = 2`:

```text
dfs(0, +0)   +2 | -2
  dfs(1, +2)
    dfs(2, +4)
      dfs(3, +6) -> 0   != target
      dfs(3, +2) -> 1   == target     +2 +2 -2
    dfs(2, +4) -> 1
    dfs(2, +0)
      dfs(3, +2) -> 1   == target     +2 -2 +2
      dfs(3, -2) -> 0   != target
    dfs(2, +0) -> 1
  dfs(1, +2) -> 2
  dfs(1, -2)
    dfs(2, +0)
      dfs(3, +2) -> 1   == target     -2 +2 +2
      dfs(3, -2) -> 0   != target
    dfs(2, +0) -> 1
    dfs(2, -4) -> 0     (both children miss)
  dfs(1, -2) -> 1
dfs(0, +0) -> 3
```

Exactly three leaves land on `+2` (`+2 +2 -2`, `+2 -2 +2`, `-2 +2 +2`), so the root returns `3`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's sign tree.

```python
from typing import List


class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        def dfs(i: int, current: int) -> int:
            if i == len(nums):
                return 1 if current == target else 0
            # Assign + or - to nums[i] and recurse
            return dfs(i + 1, current + nums[i]) + dfs(i + 1, current - nums[i])

        return dfs(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

Each of the `n` numbers forks into two sign choices, so the tree has `2^n` leaves.

##### Space Complexity: `O(n)`

The recursion stack, one frame per number along the current branch.

#### Key Insights

- Transcribes the problem statement directly: one fork per number, one test
  at the end.
- Correct on every input the constraints allow, including zeros and negative
  targets, with no special cases.
- The number of distinct states is far below the number of paths: different
  sign prefixes often reach the same `(i, current)`, which is the redundancy the
  next solution removes.

### Top-Down Memoization

#### Derivation

The enumeration re-solves futures it has already seen: on `[2, 2, 2]`, the state `(index 2, current 0)` is reached both by `+2, -2` and by `-2, +2`, yet the subtree below it is walked twice. A branch's future depends only on `(i, current)`, never on the signs that produced `current`, so each pair is a [memoizable](https://en.wikipedia.org/wiki/Memoization) state. The running total stays within `±total`, so there are at most `n × (2 × total + 1)` of them:

1. Keep the enumeration's recursion unchanged.
2. Add a `memo` keyed by `(i, current)`; check it on entry and store before
   every return.

#### Walkthrough

Trace the recursion with hits marked on Example 1: `nums = [2,2,2]`, `target = 2`. The `+` child is taken first, then the `-` child:

```text
dfs(0, +0)
  dfs(1, +2)
    dfs(2, +4)
      dfs(3, +6) -> 0   != target
      dfs(3, +2) -> 1   == target
    dfs(2, +4) -> 1  stored
    dfs(2, +0)
      dfs(3, +2) -> 1   == target
      dfs(3, -2) -> 0   != target
    dfs(2, +0) -> 1  stored
  dfs(1, +2) -> 2  stored
  dfs(1, -2)
    dfs(2, +0) -> 1  ** memo hit **
    dfs(2, -4)
      dfs(3, -2) -> 0   != target
      dfs(3, -6) -> 0   != target
    dfs(2, -4) -> 0  stored
  dfs(1, -2) -> 1  stored
dfs(0, +0) -> 3  stored
```

The second arrival at `dfs(2, +0)` (via `-2, +2` after the first visit via `+2, -2`) is answered from the memo. Six states are stored against the brute tree's fifteen nodes, and the root returns `3`, matching the expected Output for Example 1.

#### Solution

The code is the enumeration with a dict in front of it.

```python
from typing import List


class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        memo = {}

        def dfs(i: int, current: int) -> int:
            if i == len(nums):
                return 1 if current == target else 0
            if (i, current) in memo:
                return memo[(i, current)]
            memo[(i, current)] = dfs(i + 1, current + nums[i]) + dfs(
                i + 1, current - nums[i]
            )
            return memo[(i, current)]

        return dfs(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × total)`

At most `n × (2 × total + 1)` distinct states, one constant-work solve each.

##### Space Complexity: `O(n × total)`

The memo's entries plus the recursion stack of `n` frames.

#### Key Insights

- The state `(i, current)` is a complete summary of the sign history: many
  prefixes collapse onto one entry.
- The memo does not care that `current` can be negative: dict keys handle it,
  which is why this formulation survives negative targets with no shifts or
  offsets.
- The polynomial state count hints the problem has knapsack structure; the
  algebra of the next solution makes it explicit.

### Bottom-Up 2-D DP

#### Derivation

Memoization still enumerates expressions. Name the sums: `P` is the total of the positively signed numbers, `N` of the negatively signed ones. Every expression obeys `P - N = target` and, since together the two sets partition the array, `P + N = total`. Adding the equations eliminates `N`: `P = (total + target) / 2`. So counting expressions equals counting subsets that sum to one specific value, and the two base conditions fall out of the algebra: the expression count is `0` when `total + target` is odd (no integer `P`) and when `|target| > total` (`P` would exceed the sum of all numbers). The subset count tabulates without recursion: `dp[i][s]` is the number of subsets of the first `i` numbers summing to `s`:

1. Compute `total`; return `0` when `|target| > total` or
   `(total + target)` is odd.
2. Set `positive_sum = (total + target) // 2`; allocate `dp` of size
   `(len(nums) + 1) x (positive_sum + 1)` with `dp[0][0] = 1`.
3. For each index `i` in `1..len(nums)` with `num = nums[i - 1]`, and each
   `s` in `0..positive_sum`:
   - `dp[i][s] = dp[i - 1][s]` (leave the number out),
   - plus `dp[i - 1][s - num]` when `s >= num` (put it in).
4. Return `dp[len(nums)][positive_sum]`.

The `- 1` offsets exist because the table counts number prefixes while the list is position-indexed: row `i` decides with `nums[i - 1]`.

#### Walkthrough

Trace the fill on Example 1: `nums = [2,2,2]`, so `total = 6`, `target = 2`, `positive_sum = 4`. Rows are number prefixes, columns are sums `0..4`:

```text
            ''   s=0  s=1  s=2  s=3  s=4
  (none)         1    0    0    0    0
  num 2          1    0    1    0    0
  num 2          1    0    2    0    1
  num 2          1    0    3    0    3
```

Each row copies the row above and adds the shifted counts: row `num 2` (the second) gets `dp[2][2] = dp[1][2] + dp[1][0] = 1 + 1 = 2` (subsets `{2a}` and `{2a, 2b}`... reading exactly: the first number alone, and the first two together) and `dp[2][4] = dp[1][4] + dp[1][2] = 0 + 1 = 1`. The final row reads `dp[3][4] = dp[2][4] + dp[2][2] = 1 + 2 = 3`, matching the expected Output for Example 1: the three subsets of size two, one per number left positive. Odd sums stay `0` throughout, and any input whose `total + target` is odd, like `nums = [1, 1]` with target `0` from the statement, returns `0` at that gate.

#### Solution

The code is the row-by-row fill of the walkthrough's table, with the algebra's two gates in front.

```python
from typing import List


class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        total = sum(nums)
        if abs(target) > total or (total + target) % 2 != 0:
            return 0
        positive_sum = (total + target) // 2
        dp = [[0] * (positive_sum + 1) for _ in range(len(nums) + 1)]
        dp[0][0] = 1
        for i in range(1, len(nums) + 1):
            num = nums[i - 1]
            for s in range(positive_sum + 1):
                dp[i][s] = dp[i - 1][s]
                if s >= num:
                    dp[i][s] += dp[i - 1][s - num]
        return dp[len(nums)][positive_sum]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × total)`

One copy plus one conditional add per table cell.

##### Space Complexity: `O(n × total)`

The full table.

#### Key Insights

- The transformation `P = (total + target) / 2` converts a two-sided sign
  problem into a one-sided subset count, halving the state space.
- The gates are the algebra speaking: odd `total + target` and
  `|target| > total` are exactly the conditions under which no integer `P`
  exists.
- A zero number enters every subset sum "twice" (in or out, same sum), which
  the table expresses as `dp[i][s] += dp[i - 1][s - 0]`, doubling each count;
  the count stays correct with no special case.

### Space-Optimized 1-D DP

#### Derivation

Cell `(i, s)` reads only row `i - 1`: the cell above and the cell above-left. Older rows are dead weight, so the whole table collapses to one row `dp` where `dp[s]` counts the subsets of the numbers processed so far that sum to `s`. Sweeping `s` right to left keeps `dp[s - num]` at its previous-row value when the update reads it, which is the put-the-number-in branch; `dp[s]`'s old value is the leave-it-out branch:

1. Compute `total`; return `0` when `|target| > total` or
   `(total + target)` is odd.
2. Initialize `dp` of size `positive_sum + 1` with `dp[0] = 1`.
3. For each `num`, sweep `s` from `positive_sum` down to `num`, updating
   `dp[s] += dp[s - num]`.
4. Return `dp[positive_sum]`.

#### Recurrence

Let \(dp_k[s]\) be the number of subsets of the first `k` numbers summing to `s`, after the transformation fixes the target sum:

$$ |P| = \frac{\text{total} + \text{target}}{2}, \qquad dp_0[s] = [\,s = 0\,] $$

$$ dp_k[s] = dp_{k-1}[s] + dp_{k-1}[s - \text{nums}[k-1]] $$

```text
positive_sum = (total + target) / 2     (gate: total + target even,
                                         |target| <= total)
dp_0[s] = (s == 0)
dp_k[s] = dp_(k-1)[s] + dp_(k-1)[s - nums[k - 1]]
          (second term only when s >= nums[k - 1])
```

Both terms read row `k - 1`: each number is used at most once, which is the 0/1 knapsack constraint. Sweeping `s` downward inside the single row makes every read of \(dp[s - \text{num}]\) land on the previous row's value; sweeping upward would read row `k` and count number reuse, the unbounded knapsack (Coin Change II's ascending sweep). The answer is \(dp_n[\text{positive\_sum}]\).

#### Walkthrough

Trace the single row on Example 1: `positive_sum = 4`, `nums = [2,2,2]`, one line per number:

```text
start          dp = [1, 0, 0, 0, 0]
num 2          dp = [1, 0, 1, 0, 0]
num 2          dp = [1, 0, 2, 0, 1]
num 2          dp = [1, 0, 3, 0, 3]
```

Each line equals the corresponding table row of the Bottom-Up 2-D DP. In the last sweep, `dp[4]` reads `dp[2] = 2` (still the previous row's value because the sweep is descending) and becomes `1 + 2 = 3`. The final `dp[positive_sum]` is `3`, matching the expected Output for Example 1; the corner case of a zero in the array (`[1, 0]`, target `1`) returns `2` because the zero doubles the one way to form the sum `1`.

#### Solution

The code is the walkthrough's sweeps: one right-to-left pass per number, behind the algebra's gates.

```python
from typing import List


class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        total = sum(nums)
        if abs(target) > total or (total + target) % 2 != 0:
            return 0
        positive_sum = (total + target) // 2
        dp = [0] * (positive_sum + 1)
        dp[0] = 1
        for num in nums:
            for s in range(positive_sum, num - 1, -1):
                dp[s] += dp[s - num]
        return dp[positive_sum]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × total)`

One add per (number, sum) pair; the gate exits are `O(n)` for the `sum` call.

##### Space Complexity: `O(total)`

The single row of `positive_sum + 1` entries.

#### Key Insights

- The descending sweep is the whole trick: it freezes `dp[s - num]` at the
  previous row's value so each number is used once.
- The inner sweep starts at `num`, not `0`: sums below the number cannot
  include it, and their counts carry over unchanged.
- This is the same 0/1 knapsack row as Partition Equal Subset Sum, pointed
  at `(total + target) / 2` instead of `total / 2`, counting ways instead of
  answering reachability.

### Top-Down Memoization with functools.cache

#### Derivation

Step 2's memo is not part of the recurrence. The dict, the membership test, and the store all exist to remember what `dfs(i, current)` returned, which is precisely what [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) does around any pure function. Decorating the recursion deletes all three pieces of bookkeeping and leaves the sign fork and the base case untouched:

1. Keep the memoized recursion's structure: the same base case, the same
   two-branch sum.
2. Replace the `memo` dict with `@cache` on `dfs`, keyed automatically by the
   arguments `(i, current)`.
3. Return `dfs(0, 0)`.

The one behavioral cost: `@cache` also stores the `n + 1` leaf results and keeps every state alive for the life of the process.

#### Walkthrough

Trace the decorated recursion on Example 1: `nums = [2,2,2]`, `target = 2`. The call sequence is identical to the Top-Down Memoization walkthrough; the only difference is where a repeat lookup lands:

```text
dfs(0, +0) -> dfs(1, +2) + dfs(1, -2)
  ... identical descent ...
dfs(2, +0) -> 1                       ** cached: no recompute **
dfs(0, +0) -> 3
```

10 distinct `(i, current)` calls are cached (6 interior states plus the 4 leaves the dict version never stored), the one repeat arrival is a hit, and the answer is `3`, matching the expected Output for Example 1.

#### Solution

The code is the memoized recursion with the dict replaced by the decorator.

```python
from functools import cache
from typing import List


class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        @cache
        def dfs(i: int, current: int) -> int:
            if i == len(nums):
                return 1 if current == target else 0
            return dfs(i + 1, current + nums[i]) + dfs(i + 1, current - nums[i])

        return dfs(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × total)`

The cache admits each `(i, current)` state once; the body is constant work.

##### Space Complexity: `O(n × total)`

The decorator's cache plus the recursion stack.

#### Key Insights

- `functools.cache` is the dict-based memo with the ceremony removed: same
  asymptotics, three fewer lines, no key-tuple mistakes.
- Caching leaves and interior states alike is harmless: there are only two
  distinct leaf results.
- The recursion body is the problem statement in its purest form; the
  algebraic transformation of the DP sections is the performance story, this
  section is the readability story.

## Comparison of Solutions

### Time Complexity

- **Brute Force Enumeration**: `O(2^n)` - every sign assignment enumerated.
- **Top-Down Memoization**: `O(n × total)` - one solve per `(i, current)` state.
- **Bottom-Up 2-D DP**: `O(n × total)` - one update per table cell.
- **Space-Optimized 1-D DP**: `O(n × total)` - the same cells, one row at a time.
- **Top-Down Memoization with functools.cache**: `O(n × total)` - the dict memo with library bookkeeping.

### Space Complexity

- **Brute Force Enumeration**: `O(n)` - the recursion stack.
- **Top-Down Memoization**: `O(n × total)` - the memo plus the stack.
- **Bottom-Up 2-D DP**: `O(n × total)` - the full table.
- **Space-Optimized 1-D DP**: `O(total)` - the single row.
- **Top-Down Memoization with functools.cache**: `O(n × total)` - the decorator's cache plus the stack.

### Trade-offs

- Enumeration is the definitional baseline; exponential time makes it a
  correctness oracle rather than a solution.
- The memoized recursion needs no algebraic insight and tolerates negative
  totals naturally, at the price of a stack and a dict.
- The transformed row is the fastest constant factor and the least memory,
  but it only exists after the `P = (total + target) / 2` derivation.

### When to Use Each

- **Brute Force Enumeration**: tiny inputs, or as the brute-force oracle when
  checking the faster versions.
- **Top-Down Memoization**: when deriving live and the subset-sum
  transformation is not yet visible; the states are cacheable immediately.
- **Bottom-Up 2-D DP**: when the full table matters, for example to
  reconstruct which numbers went positive by walking it backward.
- **Space-Optimized 1-D DP**: the answer to the problem as stated
  (recommended here).
- **Top-Down Memoization with functools.cache**: Python code that wants the
  memoized recursion without the dict ceremony.

### Optimization Notes

- The parity and range gates are free early exits: they reject impossible
  targets in `O(n)` before any table or recursion is built.
- The state space of the memoized recursion is symmetric in `±current`, so
  states beyond `±(total - remaining)` are unreachable; neither the memo nor
  the table exploits this, and exploiting it complicates the code for a
  constant factor.
- A target of `0` with all-zero numbers is the count `2^n`: the gates pass
  (`positive_sum = 0`) and the table's `dp[0]` doubles per zero, which the
  row handles without special cases.
