# [Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/)

**Easy** | **15 minutes** | **Array, Dynamic Programming**

**Pattern:** [DP 1D Linear](../patterns/dp_1d_linear/intuition.md)

**Algorithm:** [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization) · [Recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science))

**Practice:** [`practice/min_cost_climbing_stairs/solution.py`](../../practice/min_cost_climbing_stairs/solution.py)

Given an array of integers `cost` where `cost[i]` is the cost of taking a step from the `ith` floor of a staircase. After paying the cost, you can step to either the `(i + 1)th` floor or the `(i + 2)th` floor.

You may choose to start at the index `0` or the index `1` floor.

Return the minimum cost to reach the top of the staircase, i.e. just past the last index in `cost`.

## Examples

### Example 1

**Input:** `cost = [1,2,3]`

**Output:** `2`

**Explanation:** We can start at index = `1` and pay the cost of `cost[1] = 2` and take two steps to reach the top. The total cost is `2`.

### Example 2

**Input:** `cost = [1,2,1,2,1,1,1]`

**Output:** `4`

**Explanation:** Start at index = `0`.
* Pay the cost of `cost[0] = 1` and take two steps to reach index = `2`.
* Pay the cost of `cost[2] = 1` and take two steps to reach index = `4`.
* Pay the cost of `cost[4] = 1` and take two steps to reach index = `6`.
* Pay the cost of `cost[6] = 1` and take one step to reach the top.
* The total cost is `4`.

## Constraints

- `2 <= cost.length <= 100`
- `0 <= cost[i] <= 100`

## Deriving the Solution

A climb is fully described by where it starts and how it moves: it may begin free on floor `0` or floor `1`, and from any floor it pays that floor's cost and steps one or two floors up, ending the first time it lands on or past the last index. The total cost is the sum over the floors touched, so "the cheapest way up" is a shortest-path question on a straight line of floors, and every solution below answers it by pricing floors rather than by pricing whole climbs.

1. **Start literal.** Walk every climb: branch over the two moves at each
   floor from each of the two free starts, summing each floor touched.
   Correct, but the branch tree doubles at every level and re-prices the
   same floors in exponentially many branches, costing `O(2^n)`: see
   [Brute Force](#brute-force).
2. **Spot the waste.** The cheapest finish from any one floor is a fixed
   fact about that floor and the array, yet the tree re-derives it
   separately inside every branch that passes through the floor.
3. **Cache it.** Record each floor's cheapest finish the first time it is
   computed and answer every later request from the store: one computation
   per floor, `O(n)`: see [Top-Down Memoization](#top-down-memoization).
4. **Flip the direction.** The cache fills highest-floor-first anyway, so
   a plain loop sweeping from the last floor down to floor `0` produces
   the same table with no recursion and no call overhead: see
   [Bottom-Up DP](#bottom-up-dp).
5. **Shrink the state.** Each update reads only the two entries above it,
   so two rolling registers replace the whole table: `O(1)` space: see
   [Space-Optimized DP](#space-optimized-dp).
6. **Hand the cache to the library.** Step 3 stacked two ideas: the
   pay-then-leap recurrence, and a dictionary keeping it from redoing
   work. Only the recurrence is the algorithm, so decorating the Brute
   Force function with `functools.cache` deletes the three bookkeeping
   lines and leaves the recursion verbatim: see [Top-Down Memoization
   with functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Brute Force

#### Derivation

The most literal reading of the problem enumerates the climb itself: a climb is a sequence of moves, each move steps one or two floors, and every floor stood on collects its `cost[i]` on the way past. Trying every sequence finds the cheapest one:

1. Start a recursion at each of the two free starting floors, floor `0` and
   floor `1`.
2. At each floor, record the floor's own cost and branch into the two legal
   moves: `one = cost[floor] + recurse(floor + 1)` and
   `two = cost[floor] + recurse(floor + 2)`.
3. Stop a branch the moment its floor reaches or passes the last index: the
   top is just past the array, so a step beyond the last floor is free.
4. Return the cheaper of the two branch totals from the cheaper start.

Every path is walked, so the answer is exact, but the same floors are re-priced in exponentially many branches.

#### Walkthrough

Let us branch through Example 1, `cost = [1,2,3]`. The recursion starts at both free floors; the trace indents one level per call and shows each call's two branches and its return:

```text
from(0)                       pays cost[0] = 1, then branches
├── one = 1 + from(1)
│   └── from(1)               pays cost[1] = 2, then branches
│       ├── one = 2 + from(2)
│       │   └── from(2)       pays cost[2] = 3, both leaps land past the top
│       │       one = 3 + 0   two = 3 + 0
│       │       -> 3
│       │   one = 2 + 3 = 5   two = 2 + from(3) = 2 + 0 = 2
│       │   -> 2
│   one = 1 + 2 = 3
└── two = 1 + from(2) = 1 + 3 = 4
from(0) -> min(3, 4) = 3
from(1) -> 2                  recomputed from scratch
answer = min(from(0), from(1)) = min(3, 2) = 2
```

The cheapest route is the free start on floor `1`: pay `cost[1] = 2` and leap two floors straight past the top. The Brute Force still reports it, at the price of walking every route: the branch tree holds every way to compose `1`- and `2`-floor moves into a climb, and the `from(1)` subtree priced under `from(0)` is priced all over again when the recursion restarts there.

#### Solution

The code is the walkthrough's branch tree: pay, branch, stop past the top.

```python
from typing import List


class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        def from_floor(floor: int) -> int:
            # The top sits just past the last index: stepping to or past
            # it collects nothing further.
            if floor >= len(cost):
                return 0

            # Pay this floor, then take whichever leap is cheaper overall.
            one = cost[floor] + from_floor(floor + 1)
            two = cost[floor] + from_floor(floor + 2)
            return min(one, two)

        return min(from_floor(0), from_floor(1))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

Each call spawns two more, so the call tree roughly doubles at every level of floors left to climb; the same subproblem (`from_floor` of one floor) is recomputed in exponentially many branches.

##### Space Complexity: `O(n)`

No table is kept, but the recursion stack reaches depth `n` along the all-single-steps path.

#### Key Insights

- The problem statement translates directly into a recursion over floors, which makes this the natural first formulation
- The top being *just past the last index* is what makes floors `n - 1` and `n - 2` legal launch points: stepping from either one lands on or past the top, and that final step collects no cost
- Every branch re-prices floors the tree has already priced, which is exactly the waste the next solution removes

### Top-Down Memoization

#### Derivation

The Brute Force re-prices the same floor in exponentially many branches, yet the answer for a floor never changes: `from_floor(f)` depends on nothing but `f` and the fixed `cost` array. The branch totals form a tree of calls in which identical floors recur constantly, so cache each floor's answer the first time it is computed and answer every later request from the store. This is [memoization](https://en.wikipedia.org/wiki/Memoization), and it collapses the exponential tree into one computation per floor:

1. Keep the recursion exactly as the Brute Force wrote it: pay `cost[floor]`,
   then branch into `floor + 1` and `floor + 2`.
2. Before branching, check the `memo` dictionary: a floor computed once is
   never branched on again.
3. Store each newly computed total in `memo` before returning it.
4. Return the cheaper of the two starting floors as before; each now costs one
   linear sweep's worth of fresh work.

#### Walkthrough

Let us cache through Example 2, `cost = [1,2,1,2,1,1,1]`, whose overlapping branches make memoization pay. The trace indents one level per call, shows the floors each call branches into, and marks store and reuse events:

```text
from(0)  miss  pays 1, branches into 1 and 2
  from(1)  miss  pays 2, branches into 2 and 3
    from(2)  miss  pays 1, branches into 3 and 4
      from(3)  miss  pays 2, branches into 4 and 5
        from(4)  miss  pays 1, branches into 5 and 6
          from(5)  miss  pays 1, branches into 6 and 7
            from(6)  miss  pays 1, branches into 7 and 8
              from(7) -> 0   past the top
              from(8) -> 0   past the top
            from(6) -> 1 + min(0, 0) = 1   store memo[6] = 1
          from(5) -> 1 + min(1, 0) = 1     store memo[5] = 1
        from(4) -> 1 + min(1, 1) = 2       store memo[4] = 2
      from(3) -> 2 + min(2, 1) = 3         store memo[3] = 3
    from(2) -> 1 + min(3, 2) = 3           store memo[2] = 3
  from(1) -> 2 + min(3, 3) = 5             store memo[1] = 5
from(0)  from(1) = 5 done, then from(2)    ** memo hit: memo[2] = 3, no recursion **
from(0) -> 1 + min(5, 3) = 4               store memo[0] = 4
answer  min(from(0), from(1))              ** memo hit: memo[1] = 5, no recursion **
answer = min(4, 5) = 4
```

The descent prices each floor exactly once on the way down; the two marked hits are the payoff. `from(0)`'s second branch asks for floor `2`, whose whole subtree is already cached, and the second starting floor `from(1)` answers from `memo[1]` without recursing at all. The outer expression returns `min(4, 5) = 4`, matching the expected Output for Example 2.

#### Solution

The code is the Brute Force recursion with the `memo` check and store wrapped around the branch.

```python
from typing import List


class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        memo = {}

        def from_floor(floor: int) -> int:
            if floor >= len(cost):
                return 0
            if floor in memo:
                return memo[floor]

            # Same branch as the Brute Force, now priced once per floor.
            memo[floor] = cost[floor] + min(
                from_floor(floor + 1), from_floor(floor + 2)
            )
            return memo[floor]

        return min(from_floor(0), from_floor(1))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each floor from `0` to `n - 1` runs its body at most once, and each body combines two already-cached values in constant time.

##### Space Complexity: `O(n)`

The cache holds one entry per floor, and the recursion stack reaches depth `n` before the first value returns.

#### Key Insights

- Memoization is an execution strategy, not a new algorithm: the recurrence reads exactly as the Brute Force wrote it
- Each of the two starting floors seeds an independent recursion, but the shared `memo` means the second start repeats almost no work
- The cache trades `O(n)` memory for the exponential blow-up, the standard bargain the two solutions below strike again in different clothes

### Bottom-Up DP

#### Derivation

The memoized recursion still starts at the answer and unwinds downward before producing its first useful value, paying call overhead and stack depth along the way. Watch the order its `memo` actually fills: the highest floors resolve first, then the levels below, down to floors `1` and `0`. Bottom-up [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) produces that same table with a plain loop and no recursion. Let `dp[i]` be the cheapest total collectible when climbing *from* floor `i` to the top; then floor `i` pays `cost[i]` and takes the cheaper of its two leaps:

1. Allocate `dp` with two slots past the last index, both `0`: standing on or
   past the top collects nothing further.
2. Sweep `i` from the last floor down to `0`, setting
   `dp[i] = cost[i] + min(dp[i + 1], dp[i + 2])`.
3. Read the answer from the two free starting floors: `min(dp[0], dp[1])`.

#### Recurrence

Let `dp[i]` be the minimum cost payable from floor `i` onward, where floor `n = len(cost)` (just past the last index) is the top:

$$ dp[i] = \begin{cases} 0, & i \ge n \\[4pt] cost[i] + \min(dp[i+1],\ dp[i+2]), & 0 \le i < n \end{cases} $$

```text
dp[i] = 0,                                  for i >= n
dp[i] = cost[i] + min(dp[i+1], dp[i+2]),    for 0 <= i < n
```

The base case encodes that reaching the top ends the climb for free; the recurrence says a climber on floor `i` always pays `cost[i]` and then chooses the cheaper of the two leaps. The answer is `min(dp[0], dp[1])` because the climb may begin on either floor at no charge.

#### Walkthrough

Let us fill the table on Example 1, `cost = [1,2,3]`, so `n = 3` and the table runs `dp[0]` through `dp[4]` with the two slots at and past the top seeded at `0`:

```text
start    dp = [_, _, _, 0, 0]                     dp[3] = dp[4] = 0
i = 2    dp[2] = 3 + min(dp[3], dp[4]) = 3 + 0    dp = [_, _, 3, 0, 0]
i = 1    dp[1] = 2 + min(dp[2], dp[3]) = 2 + 0    dp = [_, 2, 3, 0, 0]
i = 0    dp[0] = 1 + min(dp[1], dp[2]) = 1 + 2    dp = [3, 2, 3, 0, 0]
```

Two of the three updates leap straight past the top: from floor `2` both moves land on or past index `3`, and from floor `1` the two-floor leap lands on index `3`, so each reads the seeded `0` and pays only its own floor. The method returns `min(dp[0], dp[1]) = min(3, 2) = 2`, matching the expected Output for Example 1: start free on floor `1`, pay `2`, and leap straight past the top.

#### Solution

The code is the corrected table fill from the walkthrough: two free slots past the top, one downward sweep, then the cheaper of the two starts.

```python
from typing import List


class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        length = len(cost)
        # Slots n and n + 1 sit past the top: finishing there is free.
        dp = [0] * (length + 2)

        # The leap from floor i lands on i + 1 or i + 2, so fill downward.
        for i in range(length - 1, -1, -1):
            dp[i] = cost[i] + min(dp[i + 1], dp[i + 2])

        return min(dp[0], dp[1])
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One constant-time update per floor in a single downward sweep.

##### Space Complexity: `O(n)`

The table holds `n + 2` entries, one per floor plus the two free slots past the top.

#### Key Insights

- Defining `dp[i]` as the cost *from* floor `i` (a suffix formulation) puts the free choice of starting floor in the final `min(dp[0], dp[1])` rather than in the recurrence
- The two extra table slots are the whole base case: writing `dp[n] = dp[n + 1] = 0` removes every boundary branch from the loop
- The suffix direction is what makes the free start natural; the prefix formulation used by House Robber needs its answer read from a `dp[n]` slot instead

### Space-Optimized DP

#### Derivation

The Bottom-Up table stores `n + 2` entries, yet the update for floor `i` reads only `dp[i + 1] and dp[i + 2]`: everything older is dead weight once floor `i` is set. The repair keeps just those two values in rolling registers, sweeping the same downward pass with `one_above` playing `dp[i + 1]` and `two_above` playing `dp[i + 2]`:

1. Seed `one_above = two_above = 0`, the two free slots past the top.
2. For each floor `i` from the last down to `0`, compute
   `current = cost[i] + min(one_above, two_above)`, then shift the registers:
   `two_above = one_above`, `one_above = current`.
3. After the floor `0` update, `one_above` holds `dp[0]` and `two_above` holds
   `dp[1]`; return the cheaper, `min(one_above, two_above)`.

#### Walkthrough

Let us roll the registers through Example 1, `cost = [1,2,3]`:

```text
start    one_above = 0, two_above = 0              the two free slots past the top
i = 2    current = 3 + min(0, 0) = 3               (one_above, two_above) = (3, 0)
i = 1    current = 2 + min(3, 0) = 2               (one_above, two_above) = (2, 3)
i = 0    current = 1 + min(2, 3) = 3               (one_above, two_above) = (3, 2)
```

After the floor `0` update, `one_above` holds `dp[0] = 3` and `two_above` holds `dp[1] = 2`. The method returns `min(3, 2) = 2`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's register update: compute, shift, and read the cheaper start at the end.

```python
from typing import List


class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        one_above, two_above = 0, 0
        for i in range(len(cost) - 1, -1, -1):
            current = cost[i] + min(one_above, two_above)
            two_above = one_above
            one_above = current
        return min(one_above, two_above)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The same single downward sweep as the Bottom-Up DP, one constant-time update per floor.

##### Space Complexity: `O(1)`

Two integer registers replace the whole table, regardless of `len(cost)`.

#### Key Insights

- The register names state their meaning directly: `one_above` is the cheapest finish from the next floor up, `two_above` from the floor after that
- After the loop, the registers hold `dp[0]` and `dp[1]`, so the free choice of starting floor is one final `min` with no extra storage
- A register-update this short is also its own correctness risk: the shift order (`two_above` before `one_above`) must follow the assignment that computes `current`, or the registers alias the same floor

### Top-Down Memoization with functools.cache

#### Derivation

The [Top-Down Memoization](#top-down-memoization) solution stacks two separate things: the pay-then-leap recurrence, and a dictionary that stops the recursion from re-pricing a floor it has already answered. Only the first is the algorithm. The second is pure bookkeeping, and the standard library already implements it. Decorating the function with [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) attaches an unbounded cache keyed by the call's arguments, consulted before the body runs and filled with whatever the body returns, so the recurrence and its base case stay on the page exactly as the Brute Force wrote them:

1. Keep `from_floor(floor)` verbatim from the Brute Force: return `0` past the
   top, otherwise return
   `cost[floor] + min(from_floor(floor + 1), from_floor(floor + 2))`.
2. Decorate it with `@cache`, so each distinct floor runs the body at most once
   and every later request for that floor is answered from the cache.
3. Delete the three bookkeeping lines the decorator now owns: the `memo = {}`
   declaration, the `if floor in memo` lookup, and the `memo[floor] = ...`
   store.
4. Because `from_floor` is defined inside `minCostClimbingStairs`, each call
   builds a fresh function object with a fresh cache, so nothing leaks between
   inputs.

#### Walkthrough

Run it on Example 2, `cost = [1,2,1,2,1,1,1]`. The trace indents one level per call and notes whether the decorator ran the body or answered from the cache:

```text
from(0)   miss, run the body
  from(1)   miss, run the body
    from(2)   miss, run the body
      from(3)   miss, run the body
        from(4)   miss, run the body
          from(5)   miss, run the body
            from(6)   miss, run the body
              from(7) -> 0   base case, cached
              from(8) -> 0   base case, cached
            from(6) -> 1 + min(0, 0) = 1   cached
          from(5) -> 1 + min(1, 0) = 1     from(6) hit, from(7) hit; cached
        from(4) -> 1 + min(1, 1) = 2       from(5) hit, from(6) hit; cached
      from(3) -> 2 + min(2, 1) = 3         from(4) hit, from(5) hit; cached
    from(2) -> 1 + min(3, 2) = 3           from(3) hit, from(4) hit; cached
  from(1) -> 2 + min(3, 3) = 5             from(2) hit, from(3) hit; cached
from(0) -> 1 + min(5, 3) = 4               from(1) hit, from(2) hit; cached
answer = min(4, 5) = 4                     second start from(1) is one cache hit
```

Each floor's body runs exactly once. Every branch after the initial descent lands on an already-cached floor, so the deepest work happens once and the second starting floor costs a single dictionary lookup. The outer expression returns `min(4, 5) = 4`, matching the expected Output for Example 2.

#### Solution

The Brute Force recursion, unchanged, with one decorator standing in for the memo dictionary.

```python
from functools import cache
from typing import List


class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        # The cache lives on this inner function object, which is rebuilt on
        # every call, so results never carry over between inputs.
        @cache
        def from_floor(floor: int) -> int:
            if floor >= len(cost):
                return 0
            return cost[floor] + min(from_floor(floor + 1), from_floor(floor + 2))

        return min(from_floor(0), from_floor(1))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The cache admits each floor from `0` to `n` into the body exactly once, and each admission does one `min` of two already-known values; every other call is a dictionary lookup on a small integer key.

##### Space Complexity: `O(n)`

The decorator's cache holds one entry per floor from `0` through `n`, and the recursion stack reaches depth `n` before the first value returns.

#### Key Insights

- The algorithm is untouched: the recurrence and the base case read exactly as the Brute Force wrote them, which makes plain that memoization is an execution strategy rather than a change to the recursion
- Defining the cached function inside the method scopes the cache to a single call, avoiding the stale-results and unbounded-growth hazards of decorating a method or a module-level function
- `@cache` keys on the argument tuple, so it is a drop-in replacement only when the arguments are hashable and the function is genuinely pure; `from_floor` reads nothing but `floor`, which is what licenses the substitution

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(2^n)` - the uncached call tree doubles at each level, re-pricing the same floors exponentially often
- **Top-Down Memoization**: `O(n)` - each floor's total is computed once and cached
- **Bottom-Up DP**: `O(n)` - one downward sweep fills the table
- **Space-Optimized DP**: `O(n)` - the same sweep with two registers replacing the table
- **Top-Down Memoization with functools.cache**: `O(n)` - the same one-computation-per-floor bound, with the decorator's lookup standing in for the hand-written one

### Space Complexity

- **Brute Force**: `O(n)` - no cache, but the recursion stack reaches depth `n`
- **Top-Down Memoization**: `O(n)` - cache holds one entry per floor plus a recursion stack of depth `n`
- **Bottom-Up DP**: `O(n)` - the table holds `n + 2` entries
- **Space-Optimized DP**: `O(1)` - two rolling registers regardless of input length
- **Top-Down Memoization with functools.cache**: `O(n)` - cache plus recursion stack, with one entry per floor including the past-the-top base case

### Trade-offs

- **Brute Force** maps the problem statement onto a recursion most directly, but recomputes shared floors exponentially often, so it is only viable for small `n`
- **Top-Down Memoization** keeps that direct recursive framing and reaches linear time, but pays call overhead and `O(n)` stack depth
- **Bottom-Up DP** removes the recursion entirely and makes the recurrence's direction explicit, at the cost of storing the full table
- **Space-Optimized DP** keeps the sweep and drops the table to two registers, the best balance of efficiency and simplicity in the file
- **Top-Down Memoization with functools.cache** keeps the recursive framing and the linear complexity while cutting three lines of memo plumbing, paying an import and giving up control over what the cache keys on and when it evicts

### When to Use Each

- **Brute Force**: When first deriving the recurrence, or as the baseline that makes memoization's payoff concrete
- **Top-Down Memoization**: When recursive thinking feels most natural, or when an interviewer asks to see the caching mechanism itself
- **Bottom-Up DP**: When teaching DP concepts or when the table itself (for example, the cost from every floor) is worth having
- **Space-Optimized DP** (recommended): The pragmatic winner: linear time, constant space, five lines of loop
- **Top-Down Memoization with functools.cache**: The Pythonic default whenever the recursive framing is the one worth showing; fall back to the explicit dictionary when the cache needs custom keying, eviction, or a lifetime you control

### Optimization Notes

- **Space-Optimized DP is the recommended choice**: it preserves the linear-time clarity of the tabulation while collapsing the table to two rolling registers, giving `O(1)` space without sacrificing readability
- The suffix formulation ("cost from floor `i`") puts the free start in the final `min(dp[0], dp[1])`; a prefix formulation ("cost to reach floor `i`") instead reads the answer from an extra `dp[n]` slot holding `min(dp[n - 1], dp[n - 2])`
- The two past-the-top slots are the entire base case: writing `dp[n] = dp[n + 1] = 0` encodes that a leap from either of the last two floors finishes the climb for free
- In the rolling version, the register shift must happen after `current` is computed; shifting first would alias both registers to the same floor and silently corrupt the recurrence
- The Brute Force is exponential only because of recomputation: adding the one-line `@cache` to it yields the linear functools.cache solution, which is the smallest possible edit that reaches the optimal time bound
