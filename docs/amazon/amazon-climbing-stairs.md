# [Climbing Stairs](https://www.fastprep.io/problems/amazon-climbing-stairs)

**Easy** | **NN minutes** | **Dynamic Programming, Math**

You are climbing a staircase with n steps.

On each move, you may climb either 1 step or 2 steps. Return the number of distinct sequences of moves that reach exactly the top.

## Examples

### Example 1

**Input:** `n = 2`

**Output:** `2`

**Explanation:** The two valid sequences are 1 + 1 and 2.

### Example 2

**Input:** `n = 5`

**Output:** `8`

**Explanation:** Every valid sequence ends with either a 1-step move from step 4 or a 2-step move from step 3, giving 5 + 3 = 8 sequences.

## Constraints

- `1 <= n <= 45.`

## Deriving the Solution

The last move of any climb lands on step `n` from either step `n - 1` (a 1-step move) or step `n - 2` (a 2-step move), so the number of sequences reaching step `n` is the sum of the two shorter staircases' counts. Every approach below computes that one relation; they differ only in how much of it they recompute.

1. **Start literal.** Enumerate every move sequence with a recursion that tries both moves from the current step. It is correct but recomputes the same sub-staircase exponentially often: see [Brute Force Recursion](#brute-force-recursion).
2. **Cache the recomputed work.** Store each step's count the first time it is resolved, so every sub-staircase is solved once: see [Top-Down Memoization](#top-down-memoization).
3. **Flip the direction.** The memo fills bottom-up anyway, so fill it with a loop and keep only the last two counts, which the recurrence ever reads: see [Space-Optimized Bottom-Up DP](#space-optimized-bottom-up-dp).
4. **Hand the bookkeeping to the standard library.** The memo dictionary is not the algorithm; `functools.cache` is the stock version of it: see [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Brute Force Recursion

#### Derivation

The statement's most literal reading asks for the number of distinct sequences of moves. Read the last move instead of the first: a sequence reaching step `n` either ends with a 1-step move, and its prefix is any sequence reaching step `n - 1`, or ends with a 2-step move, and its prefix is any sequence reaching step `n - 2`. The two prefix families are disjoint and exhaust all sequences, which gives the recursion. Step 0 is the ground with the one empty sequence, and step 1 has the single move 1:

1. Return 1 when `n <= 1` (the empty sequence for the ground, the lone 1-step for step 1).
2. Otherwise return `climbStairs(n - 1) + climbStairs(n - 2)`.

The recursion is the definition, and the cost is the problem: the same sub-staircase is re-enumerated once per path that reaches it.

#### Walkthrough

Example 2, `n = 5`. Each call branches into the two shorter staircases; the indent shows whose subproblem is being re-solved:

```text
ways(5)
├── ways(4)                     1st call of ways(4)
│   ├── ways(3)                 1st call of ways(3)
│   │   ├── ways(2)             1st call of ways(2)
│   │   │   ├── ways(1) -> 1
│   │   │   └── ways(0) -> 1    ways(2) = 2
│   │   └── ways(1) -> 1        ways(3) = 3
│   └── ways(2)                 2nd call, whole subtree repeats
│       ├── ways(1) -> 1
│       └── ways(0) -> 1        ways(2) = 2
│   ways(4) = 3 + 2 = 5
└── ways(3)                     2nd call, recomputed
    ├── ways(2)                 3rd call of ways(2)
    │   ├── ways(1) -> 1
    │   └── ways(0) -> 1        ways(2) = 2
    └── ways(1) -> 1            ways(3) = 3
ways(5) = 5 + 3 = 8
```

The recursion returns 8, matching the expected Output, but it resolved `ways(3)` twice, `ways(2)` three times, and `ways(1)` five times. On larger staircases that overlap grows exponentially.

#### Solution

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 1:
            return 1
        return self.climbStairs(n - 1) + self.climbStairs(n - 2)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

Each call spawns two calls on inputs only one or two smaller, so the call tree doubles in size every level; the exact count is the Fibonacci-like `φ^n`, which is exponential either way. The `n <= 45` constraint caps this at roughly 2^45 nodes, far past usable.

##### Space Complexity: `O(n)`

The recursion descends one level per remaining step before any value returns, so the stack holds at most `n` frames.

#### Key Insights

- Reading the last move instead of the first turns sequence counting into a two-term sum over shorter staircases; this observation survives into every later approach.
- The base cases are step 0 with one sequence (climb nothing) and step 1 with one sequence (a single 1-step); getting step 0 wrong shifts every count.
- The recomputed subtrees are pure function of the argument, which is exactly the property the next approach exploits.

### Top-Down Memoization

#### Derivation

The Brute Force recomputes `ways(k)` once for every distinct path from `n` down to `k`, yet `ways(k)` always returns the same value. A [memoization](https://en.wikipedia.org/wiki/Memoization) dictionary removes the repetition: resolve each step once, store the count under its step number, and answer every later request from the store. The recursion itself is untouched; only its bookkeeping changes:

1. Seed `memo` with the base cases `memo[0] = 1` and `memo[1] = 1`.
2. Define `ways_from(step)`: when `step` is missing from `memo`, fill it with
   `ways_from(step - 1) + ways_from(step - 2)`.
3. Return `memo[step]`, and start the process with `ways_from(n)`.

Every step from 0 to n now enters the recursion body exactly once, so the exponential tree collapses to a chain.

#### Walkthrough

Example 2, `n = 5`. The trace indents one level per call and marks each fill or hit of `memo`:

```text
ways_from(5)  miss, recurse
  ways_from(4)  miss, recurse
    ways_from(3)  miss, recurse
      ways_from(2)  miss, recurse
        ways_from(1)  base        memo[1] = 1
        ways_from(0)  base        memo[0] = 1
        memo[2] = 1 + 1 = 2
      ways_from(1)  hit           1
      memo[3] = 2 + 1 = 3
    ways_from(2)  hit             2
    memo[4] = 3 + 2 = 5
  ways_from(3)  hit               3
  memo[5] = 5 + 3 = 8
```

Each step's count is computed exactly once and every repeated request is a dictionary hit. The outer call returns 8, matching the expected Output.

#### Solution

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        memo = {0: 1, 1: 1}

        def ways_from(step: int) -> int:
            if step not in memo:
                memo[step] = ways_from(step - 1) + ways_from(step - 2)
            return memo[step]

        return ways_from(n)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Steps 0 through n each run the body once and do one addition of known values; every other request is a constant-time dictionary lookup.

##### Space Complexity: `O(n)`

The memo holds one entry per step and the recursion still descends to depth `n` before the first value returns.

#### Key Insights

- Memoization changes no logic: the recurrence reads exactly as in the Brute Force, which shows the overlap was pure waste.
- Seeding both base cases into `memo` lets the `step not in memo` test double as the recursion's stopping condition.
- The recursion fills `memo` deepest-first no matter where it starts, which is the observation the next approach turns into a loop.

### Space-Optimized Bottom-Up DP

#### Derivation

The memoized recursion starts at `n` and unwinds all the way down before producing its first value, paying call overhead and stack depth along the way. Watch the order its memo fills: steps 2, 3, and so on upward, each from its two predecessors. A bottom-up loop fills the same table in the same order with no recursion, and the loop body only ever reads the two most recent entries, so the whole table collapses into two rolling variables:

1. Handle `n <= 1` by returning 1, matching the base cases.
2. Set `previous` and `current` to 1, the counts for steps 0 and 1.
3. For each step from 2 through n, save `current` in `saved_current`, set
   `current = previous + current`, then move `previous = saved_current`.
4. Return `current`, which holds the count for step `n`.

#### Recurrence

Let `dp[i]` be the number of distinct move sequences that reach step `i`:

$$ dp[i] = \begin{cases} 1, & i \le 1 \\[4pt] dp[i-1] + dp[i-2], & i \ge 2 \end{cases} $$

```text
dp[i] = 1,                     for i <= 1
dp[i] = dp[i-1] + dp[i-2],     for i >= 2
```

The base cases encode that step 0 has the one empty sequence and step 1 the lone 1-step move. Each higher step sums the two staircases its last move can come from. In the loop, `current` plays `dp[i]`, `previous` plays `dp[i - 1]`, and `saved_current` carries the outgoing `dp[i - 1]` into the next iteration's `previous`; `dp[n]` is read off `current` when the loop ends.

#### Walkthrough

Example 2, `n = 5`. One row per iteration, with the pair `(previous, current)` standing for `(dp[i - 1], dp[i])`:

```text
start    previous = 1, current = 1                 dp[0] = dp[1] = 1
i = 2    saved_current = 1; current = 2; previous = 1
i = 3    saved_current = 2; current = 3; previous = 2
i = 4    saved_current = 3; current = 5; previous = 3
i = 5    saved_current = 5; current = 8; previous = 5
```

After the loop, `current` holds `dp[5] = 8`, matching the expected Output: the eight sequences are the five that end in a 1-step from step 4 plus the three that end in a 2-step from step 3.

#### Solution

The code is the walkthrough's rolling update: save `current`, sum into `current`, move `previous` forward.

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 1:
            return 1

        previous, current = 1, 1

        for _ in range(2, n + 1):
            saved_current = current
            current = previous + current
            previous = saved_current

        return current
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One addition per step from 2 through n, with no other work per iteration.

##### Space Complexity: `O(1)`

Only `previous`, `current`, and `saved_current` live across iterations, regardless of n.

#### Key Insights

- A recurrence whose state is a fixed-width window of recent entries needs no table: two rolling variables replace the whole array.
- `saved_current` exists because both variables are overwritten per iteration; without it, `previous` would advance to the already-updated value and double-count the newest step.
- The `1 <= n <= 45` bound keeps every intermediate count inside a signed 32-bit integer (the largest, `dp[45]`, is 1,836,311,903), so the arithmetic never leaves the machine word in fixed-width languages.

### Top-Down Memoization with functools.cache

#### Derivation

The [Top-Down Memoization](#top-down-memoization) solution stacks two things: the recurrence, and a dictionary that stops the recursion from recomputing a step. Only the first is the algorithm; the second is bookkeeping the standard library already implements. Decorating the recursion with [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) attaches an unbounded cache keyed by the call's arguments, consulted before the body runs and filled with whatever the body returns, so the recurrence stays on the page exactly as the Brute Force wrote it:

1. Keep the recursion verbatim: return 1 when `climb`'s `step <= 1`, otherwise
   return `climb(step - 1) + climb(step - 2)`.
2. Decorate `climb` with `@cache`, so each distinct step runs the body at most
   once and later requests are answered from the cache.
3. Define `climb` inside `climbStairs`: each call then builds a fresh function
   object with a fresh cache, so nothing leaks between inputs.

One behavioural difference follows from where the decorator sits: the hand-rolled version answers the base cases before consulting `memo` and never stores them, while `@cache` wraps the whole body and caches steps 0 and 1 like any other step.

#### Walkthrough

Example 1, `n = 2`. The trace notes whether the decorator ran the body or answered from the cache:

```text
climb(2)   miss, run the body
  climb(1) -> 1     base case, now cached under key 1
  climb(0) -> 1     base case, now cached under key 0
climb(2) -> 2       1 + 1, cached under key 2
```

The body ran once per distinct argument and the outer call returned 2, matching the expected Output: the two sequences 1 + 1 and 2.

#### Solution

```python
from functools import cache


class Solution:
    def climbStairs(self, n: int) -> int:
        @cache
        def climb(step: int) -> int:
            if step <= 1:
                return 1
            return climb(step - 1) + climb(step - 2)

        return climb(n)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The cache admits each step from 0 to n into the body exactly once, one addition each; every other call is a constant-time dictionary hit.

##### Space Complexity: `O(n)`

The cache holds one entry per step and the recursion descends to depth `n` before the first value returns.

#### Key Insights

- The recurrence and both base cases read exactly as in the Brute Force, which makes plain that memoization is an execution strategy rather than a change to the algorithm.
- `@cache` keys on the argument tuple, so it is a drop-in replacement only when the arguments are hashable and the function is pure; `climb` reads nothing but `step`, which licenses the substitution.
- Defining the cached function inside the method scopes the cache to a single call, avoiding the stale-results hazard of decorating a method, whose cache would live for the whole process.

## Comparison of Solutions

### Time Complexity

- **Brute Force Recursion**: `O(2^n)` - the call tree doubles per level because every sub-staircase is re-enumerated per path.
- **Top-Down Memoization**: `O(n)` - each step's count is computed once; repeats are dictionary hits.
- **Space-Optimized Bottom-Up DP**: `O(n)` - one addition per step in a plain loop.
- **Top-Down Memoization with functools.cache**: `O(n)` - the decorator's cache gives the same once-per-step admission.

### Space Complexity

- **Brute Force Recursion**: `O(n)` - recursion stack depth.
- **Top-Down Memoization**: `O(n)` - memo dictionary plus stack.
- **Space-Optimized Bottom-Up DP**: `O(1)` - two rolling counters plus one temporary.
- **Top-Down Memoization with functools.cache**: `O(n)` - the decorator's cache plus stack.

### Trade-offs

- **Brute Force Recursion**: the shortest honest transcription of the statement; unusable beyond small `n` because of the exponential blowup.
- **Top-Down Memoization**: keeps the top-down reading of the problem and removes the waste; pays for a dictionary and the full recursion stack.
- **Space-Optimized Bottom-Up DP**: the leanest version of the recurrence, constant space and no call overhead; the direction of thinking inverts from "reach n" to "build upward from the ground".
- **Top-Down Memoization with functools.cache**: the recursion with zero bookkeeping code; the cache's lifetime must be managed by nesting the function inside the method.

### When to Use Each

- **Brute Force Recursion**: as the derivation baseline, or when `n` is known to be tiny.
- **Top-Down Memoization**: when the problem is most naturally stated top-down and the reachable state space is sparse.
- **Space-Optimized Bottom-Up DP (Recommended)**: the answer to give in an interview: linear time, constant space, and a loop simple enough to trace by hand.
- **Top-Down Memoization with functools.cache**: in Python, when the memo dict would be pure noise around a recursion the listener already understands.

### Optimization Notes

- **Space-Optimized Bottom-Up DP** is the recommended choice: same linear time as the memoized versions with `O(1)` space and no recursion to overflow.
- The rolling pair is a Fibonacci computation in disguise; `dp[n]` equals `F(n + 1)` under the convention `F(0) = 0, F(1) = 1`, which is a useful cross-check on small inputs.
- In fixed-width languages the 45-step cap keeps every count below 2^31; in Python the integers grow freely, so the constraint matters for the judge's comparisons only.
- The combinatorial closed form `sum(C(n - a, a) for a in range(n // 2 + 1))` also answers the problem in one expression; it counts the arrangements of `a` two-step moves among `n - a` total moves and is the independent model the gauntlet's expectations were frozen from.
