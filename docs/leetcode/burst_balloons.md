# [Burst Balloons](https://leetcode.com/problems/burst-balloons/)

**Hard** | **40 minutes** | **Array, Dynamic Programming**

**Pattern:** [DP 1D Linear](../patterns/dp_1d_linear/intuition.md)

**Algorithm:** [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization) · [Recurrence relation](https://en.wikipedia.org/wiki/Recurrence_relation)

**Practice:** [`practice/burst_balloons/solution.py`](../../practice/burst_balloons/solution.py)

You are given an array of integers `nums` of size `n`. The `ith` element represents a balloon with an integer value of `nums[i]`. You must burst all of the balloons.

If you burst the `ith` balloon, you will receive `nums[i - 1] * nums[i] * nums[i + 1]` coins. If `i - 1` or `i + 1` goes out of bounds of the array, then assume the out of bounds value is 1.

Return the maximum number of coins you can receive by bursting all of the balloons.

## Examples

### Example 1

**Input:** `nums = [4,2,3,7]`

**Output:** `143`

**Explanation:** nums = [4,2,3,7] --> [4,3,7] --> [4,7] --> [7] --> []
coins =  4*2*3    +   4*3*7   +  1*4*7  + 1*7*1 = 143

## Constraints

- `n == nums.length`
- `1 <= n <= 300`
- `0 <= nums[i] <= 100`

## Deriving the Solution

The coins of one burst depend on the balloon's current neighbors, which are whatever earlier bursts left behind, so a burst order is a sequence of choices whose costs mutate the state every later choice reads. Every solution below searches those orders; they differ in what a "state" is, and only one choice of state lets the search share work.

1. **Start literal.** Simulate the orders: pick a first burst, take its coins,
   and recurse on the shortened array. Every order is explored, so the maximum
   falls out, at `O(n * n!)`: see [Brute Force](#brute-force).
2. **Spot the blocker.** The natural shortcut, "split the array in half, solve
   both halves, add", is false here: bursting a half changes who neighbors whom
   across the split, so the two halves are not independent and their results
   cannot be reused.
3. **Flip which burst the split pins.** Pin not the first balloon an interval
   loses but the last one, and pad both ends with virtual balloons of value `1`.
   The last balloon inside an interval meets the interval's untouched boundary
   walls when it bursts, so its coins are fixed by the walls alone, and the two
   remaining sides become independent subproblems of the same shape: see
   [Top-Down Memoization](#top-down-memoization).
4. **Cache the intervals.** Different burst orders reach the same open interval,
   so a dictionary keyed by the interval's two walls collapses the factorial
   search to one computation per interval: the same move the memoized street
   walk makes, `O(n^3)` states and scans combined.
5. **Tabulate by width.** Every interval's answer reads only narrower
   intervals, so a plain loop over increasing interval width fills the same
   table without recursion: see [Bottom-Up DP](#bottom-up-dp).
6. **Hand the cache to the library.** Only the recurrence is the algorithm; the
   dictionary is bookkeeping that [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache)
   implements: see [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Brute Force

#### Derivation

The most literal reading simulates every burst order: at each step, every surviving balloon is a candidate next burst. Bursting balloon `i` banks `left * nums[i] * right`, where `left` and `right` are the current neighbors (or `1` at an array edge), and shortens the array by removing `nums[i]`. The best total from any position is the maximum over those candidates:

1. If `nums` is empty, no burst remains, so return `0`.
2. For each index `i`, compute `left` and `right` from the current array,
   honoring the out-of-bounds-is-`1` rule.
3. Recurse on `rest = nums[:i] + nums[i + 1:]`.
4. Return the maximum of `left * nums[i] * right + maxCoins(rest)` over all `i`.

Every permutation of bursts corresponds to one path in this recursion, so the result is exact; the cost is that the recursion shares nothing between paths.

#### Walkthrough

Full orders grow fast, so trace a tailored input instead: `nums = [3, 1]`, which has both an interior edge case (bursting `1` puts `3` at the right edge) and a meaningful choice. Each line is a call returning; children print above their parent:

```text
maxCoins: burst 3 first -> 3, recurse on [1]
    maxCoins.0: burst 1 first -> 1, recurse on []
        maxCoins.0.0: empty, -> 0
    maxCoins.0: best over all first bursts = 1
maxCoins: burst 1 first -> 3, recurse on [3]
    maxCoins.1: burst 3 first -> 3, recurse on []
        maxCoins.1.0: empty, -> 0
    maxCoins.1: best over all first bursts = 3
maxCoins: best over all first bursts = 6
-> 6
```

Bursting `3` first banks `1 * 3 * 1 = 3` and leaves `[1]` worth `1`, totaling `4`; bursting `1` first also banks `3 * 1 * 1 = 3` but leaves `[3]` worth `3`, totaling `6`. The root returns `6`, which is indeed the best order (`1` first, then `3`).

#### Solution

The code is the walkthrough's candidate loop: burst each balloon first, recurse on the rest.

```python
from typing import List


class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        if not nums:
            return 0
        best_coins = 0
        for i in range(len(nums)):
            left = nums[i - 1] if i > 0 else 1
            right = nums[i + 1] if i + 1 < len(nums) else 1
            rest = nums[:i] + nums[i + 1:]
            best_coins = max(best_coins, left * nums[i] * right + self.maxCoins(rest))
        return best_coins
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * n!)`

Each call loops over `i` and recurses on an array one element shorter, so the tree has `n * (n - 1) * ... * 1` paths, `n!` leaves, and `O(n)` work per node to slice the array and try every candidate: `n` choices at each of `n` levels makes the bound `O(n * n!)`.

##### Space Complexity: `O(n)`

No table is kept; the recursion stack reaches depth `n`, and each level's `rest` slice is released when the call returns.

#### Key Insights

- The `left`/`right` computation with the out-of-bounds `1` encodes the whole
  boundary rule, which the later solutions must preserve another way.
- Correct and complete: the recursion explores one path per burst order.
- Unusable past tiny inputs: every ordering of the survivors is re-derived once
  per prefix that produced it, and the slicing repeats that cost at each node.

### Top-Down Memoization

#### Derivation

Two repairs turn the brute force into a polynomial search, and they must land in this order.

First, split is impossible but last is not. The tempting "solve the left half and the right half" fails because bursting one half re-writes the other half's boundary neighbors. The fix is to pin the *last* burst of a stretch instead of the first: if balloon `k` is the last one burst among a stretch of balloons whose outside neighbors are fixed, then when `k` finally bursts, every other balloon of the stretch is already gone, so its neighbors are exactly those fixed walls. Its coins `wall_left * nums2[k] * wall_right` do not depend on the order anything inside burst, and everything inside splits into "the balloons strictly left of `k`" and "the balloons strictly right of `k`", two independent stretches with the same contract. Padding both ends of the array with virtual balloons of value `1` gives every original balloon fixed walls and makes the final burst's own `1 * nums2[k] * 1` fit the same formula.

Second, cache what the orders repeat. The state is now just the open interval `(l, r)`: two walls. Different orders burst different subsets in different sequences yet often stand later before the same intact interval, and the interval alone determines everything still to be gained. A dictionary keyed by `(l, r)` keeps the first computation of each interval and answers the rest by lookup:

1. Pad: `nums2 = [1] + nums + [1]`, so balloon `i` of the original sits at
   `nums2[i + 1]` with virtual walls at `0` and `n + 1`.
2. Define `burst(l, r)` as the most coins obtainable by bursting only the
   balloons strictly between the walls `l` and `r`, both walls guaranteed
   intact throughout.
3. Base case: `r - l < 2` means no balloons lie between the walls, return `0`.
4. For each candidate last balloon `k` in `l + 1 .. r - 1`:
   `burst(l, k) + burst(k, r) + nums2[l] * nums2[k] * nums2[r]`; store the
   maximum in `memo[(l, r)]` before returning.
5. The answer is `burst(0, n + 1)`: burst everything, walls included last.

#### Walkthrough

Trace Example 1: `nums = [4, 2, 3, 7]`, padded to `nums2 = [1, 4, 2, 3, 7, 1]`. The answer call is `burst(0, 5)`; each line is a call returning, children print above their parent, and marked lines are memo hits (the per-candidate arithmetic appears in the Bottom-Up walkthrough, so it is omitted here):

```text
  burst(0, 1) -> 0   empty interval, base case
    burst(1, 2) -> 0   empty interval, base case
      burst(2, 3) -> 0   empty interval, base case
        burst(3, 4) -> 0   empty interval, base case
        burst(4, 5) -> 0   empty interval, base case
      burst(3, 5) -> 21   best k = 4, memo[(l, r)] = 21
        burst(2, 3) -> 0   empty interval, base case
        burst(3, 4) -> 0   empty interval, base case
      burst(2, 4) -> 42   best k = 3, memo[(l, r)] = 42
      burst(4, 5) -> 0   empty interval, base case
    burst(2, 5) -> 56   best k = 4, memo[(l, r)] = 56
      burst(1, 2) -> 0   empty interval, base case
      burst(2, 3) -> 0   empty interval, base case
    burst(1, 3) -> 24   best k = 2, memo[(l, r)] = 24
    burst(3, 5) -> 21    ** memo hit **
      burst(1, 2) -> 0   empty interval, base case
      burst(2, 4) -> 42    ** memo hit **
      burst(1, 3) -> 24    ** memo hit **
      burst(3, 4) -> 0   empty interval, base case
    burst(1, 4) -> 108   best k = 3, memo[(l, r)] = 108
    burst(4, 5) -> 0   empty interval, base case
  burst(1, 5) -> 136   best k = 4, memo[(l, r)] = 136
    burst(0, 1) -> 0   empty interval, base case
    burst(1, 2) -> 0   empty interval, base case
  burst(0, 2) -> 8   best k = 1, memo[(l, r)] = 8
  burst(2, 5) -> 56    ** memo hit **
    burst(0, 1) -> 0   empty interval, base case
    burst(1, 3) -> 24    ** memo hit **
    burst(0, 2) -> 8    ** memo hit **
    burst(2, 3) -> 0   empty interval, base case
  burst(0, 3) -> 36   best k = 1, memo[(l, r)] = 36
  burst(3, 5) -> 21    ** memo hit **
    burst(0, 1) -> 0   empty interval, base case
    burst(1, 4) -> 108    ** memo hit **
    burst(0, 2) -> 8    ** memo hit **
    burst(2, 4) -> 42    ** memo hit **
    burst(0, 3) -> 36    ** memo hit **
    burst(3, 4) -> 0   empty interval, base case
  burst(0, 4) -> 136   best k = 1, memo[(l, r)] = 136
  burst(4, 5) -> 0   empty interval, base case
burst(0, 5) -> 143   best k = 4, memo[(l, r)] = 143
-> 143
```

The hits pile up on the right half of the tree: inside `burst(0, 5)`'s scan of last-burst candidates, the `k = 2`, `k = 3`, and `k = 4` branches all need `burst(2, 5)`, `burst(3, 5)`, `burst(0, 3)`, and friends, and every request after the first is a lookup. The root's best last balloon is `k = 4` (value `7`): its walls at that moment are the two `1`s, banking `1 * 7 * 1 = 7`, on top of `burst(0, 4) = 136`. The call returns `143`, matching the expected Output for Example 1.

#### Solution

The code is the padded recursion with the memo check and store wrapped around the candidate scan.

```python
from typing import List


class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        n = len(nums)
        nums2 = [1] + nums + [1]
        memo = {}

        def burst(l: int, r: int) -> int:
            if r - l < 2:
                return 0
            if (l, r) in memo:
                return memo[(l, r)]
            best_coins = 0
            for k in range(l + 1, r):
                coins = burst(l, k) + burst(k, r) + nums2[l] * nums2[k] * nums2[r]
                best_coins = max(best_coins, coins)
            memo[(l, r)] = best_coins
            return best_coins

        return burst(0, n + 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^3)`

There are `O(n^2)` distinct `(l, r)` intervals; each computes its body once and scans up to `n` candidates inside, each candidate an `O(1)` combination of two already-known values.

##### Space Complexity: `O(n^2)`

The memo holds one entry per interval, and the recursion stack reaches depth `n` along the nested chain `(0, n + 1), (0, n), ..., (0, 2)`.

#### Key Insights

- The padding is what makes the walls honest: an unpadded split would force
  "no neighbor yet" conditions into every state, while two virtual `1`s give
  every interval the same fixed-wall contract.
- "Last burst" is the frame that makes the split legal: the pinned balloon's
  neighbors are exactly the walls, whatever the two sides did first.
- The memo key `(l, r)` suffices because the walls are all the future can read:
  which balloons the sides burst and in what order changes nothing outside.

### Bottom-Up DP

#### Derivation

The memoized recursion decides narrow intervals first, because every interval reads only its own sub-intervals: `burst(0, 5)` needs `burst(1, 5)` and `burst(0, 4)`, which need narrower still. [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) with tabulation produces that same table in that same order with a plain loop over interval width and no recursion at all:

1. Let `dp[l][r]` equal `burst(l, r)`: the most coins from bursting everything
   strictly between walls `l` and `r`. Seed every entry at `0`, which is
   exactly the empty-interval base case.
2. Sweep width `w = r - l` from `2` upward; within a width, sweep `l` so that
   `r = l + w` stays inside the padded array.
3. Fill each `dp[l][r]` by the recurrence below; narrower widths are already
   final.
4. Return `dp[0][n + 1]`, the full padded span.

#### Recurrence

Let `nums2` be the padded array and `dp[l][r]` the most coins from bursting only the balloons strictly between walls `l` and `r`:

$$ dp[l][r] = \begin{cases}
0, & r - l < 2 \\[4pt]
\max\limits_{l < k < r} \bigl(dp[l][k] + dp[k][r] + nums2[l] \cdot nums2[k] \cdot nums2[r]\bigr), & r - l \ge 2
\end{cases} $$

```text
dp[l][r] = 0                       when r - l < 2 (no balloon between the walls)
dp[l][r] = max over k in (l, r) of
           dp[l][k] + dp[k][r] + nums2[l] * nums2[k] * nums2[r]
answer   = dp[0][n + 1]
```

The base case covers both empty spans and single-wall spans: with fewer than two indices between the walls there is no balloon to burst. The candidate `k` is the last balloon burst between the walls, so its coins are fixed by the walls, and the two `dp` terms are the independent sides.

#### Walkthrough

Let us fill the table on Example 1: `nums = [4, 2, 3, 7]`, padded to `nums2 = [1, 4, 2, 3, 7, 1]`, `n + 2 = 6` indices. Each row is one interval evaluated over its `k` candidates; width `w` sweeps before anything wider reads it:

```text
w = 2   burst(0, 2): k = 1: 0 + 0 + 1*4*2 = 8   -> dp[0][2] = 8
        burst(1, 3): k = 2: 0 + 0 + 4*2*3 = 24   -> dp[1][3] = 24
        burst(2, 4): k = 3: 0 + 0 + 2*3*7 = 42   -> dp[2][4] = 42
        burst(3, 5): k = 4: 0 + 0 + 3*7*1 = 21   -> dp[3][5] = 21
w = 3   burst(0, 3): k = 1: 0 + 24 + 1*4*3 = 36;  k = 2: 8 + 0 + 1*2*3 = 14   -> dp[0][3] = 36
        burst(1, 4): k = 2: 0 + 42 + 4*2*7 = 98;  k = 3: 24 + 0 + 4*3*7 = 108   -> dp[1][4] = 108
        burst(2, 5): k = 3: 0 + 21 + 2*3*1 = 27;  k = 4: 42 + 0 + 2*7*1 = 56   -> dp[2][5] = 56
w = 4   burst(0, 4): k = 1: 0 + 108 + 1*4*7 = 136;  k = 2: 8 + 42 + 1*2*7 = 64;  k = 3: 36 + 0 + 1*3*7 = 57   -> dp[0][4] = 136
        burst(1, 5): k = 2: 0 + 56 + 4*2*1 = 64;  k = 3: 24 + 21 + 4*3*1 = 57;  k = 4: 108 + 0 + 4*7*1 = 136   -> dp[1][5] = 136
w = 5   burst(0, 5): k = 1: 0 + 136 + 1*4*1 = 140;  k = 2: 8 + 56 + 1*2*1 = 66;  k = 3: 36 + 21 + 1*3*1 = 60;  k = 4: 136 + 0 + 1*7*1 = 143   -> dp[0][5] = 143
-> dp[0][5] = 143
```

The table reproduces the memoized run exactly: `dp[3][5] = 21`, `dp[2][4] = 42`, `dp[1][4] = 108`, and `dp[0][4] = 136` are the same values the recursion stored, and `dp[0][5] = 143` matches the expected Output for Example 1. The root's winning candidate `k = 4` is the same "last balloon is the `7`" split the walkthrough above found.

#### Solution

The code is the walkthrough's width sweep: seed zeros, then fill narrow to wide.

```python
from typing import List


class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        n = len(nums)
        nums2 = [1] + nums + [1]
        # dp[l][r] = most coins from bursting everything strictly between walls
        dp = [[0] * (n + 2) for _ in range(n + 2)]
        for width in range(2, n + 2):
            for l in range(0, n + 2 - width):
                r = l + width
                for k in range(l + 1, r):
                    coins = dp[l][k] + dp[k][r] + nums2[l] * nums2[k] * nums2[r]
                    dp[l][r] = max(dp[l][r], coins)
        return dp[0][n + 1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^3)`

Three nested sweeps: `O(n^2)` intervals, each scanning up to `n` candidates with `O(1)` arithmetic per candidate.

##### Space Complexity: `O(n^2)`

The `dp` table holds one entry per wall pair.

#### Key Insights

- Seeding the whole table at `0` folds the empty-interval base case into the
  array: no width guard remains, because width `0` and `1` cells simply hold
  the base value.
- The width-ascending fill order is the loop form of "children before parent":
  `dp[l][k]` and `dp[k][r]` have widths strictly below `width`, so they are
  final when read.
- Unlike the memoized version, the table keeps every interval's answer, which
  variants asking about sub-spans get for free.

### Top-Down Memoization with functools.cache

#### Derivation

The [Top-Down Memoization](#top-down-memoization) solution stacks two separate things: the last-burst recurrence, and a dictionary that stops the recursion from re-deciding an interval it has already answered. Only the first is the algorithm. The second is pure bookkeeping, and the standard library already implements it. Decorating the function with [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) attaches an unbounded cache keyed by the call's arguments, consulted before the body runs and filled with whatever the body returns, so the recurrence and its base case stay on the page exactly as they were derived:

1. Keep `burst(l, r)` verbatim: return `0` for `r - l < 2`, otherwise the
   candidate scan over `k`.
2. Decorate it with `@cache`, so each distinct interval runs the body at most
   once and every later request is answered from the cache.
3. Delete the three bookkeeping lines the decorator now owns: the
   `memo = {}` declaration, the `if (l, r) in memo` lookup, and the
   `memo[(l, r)] = ...` store.
4. Because `burst` is defined inside `maxCoins`, each call builds a fresh
   function object with a fresh cache, so nothing leaks between inputs.

One behavioural difference follows from where the decorator sits. The hand-rolled version answers `r - l < 2` before it ever consults `memo`, so the empty-interval keys are never stored and their base case re-runs on every visit; `@cache` wraps the entire body, so those keys are cached like any other interval.

#### Walkthrough

The full Example 1 traversal is the one traced above, so run a tailored smaller input instead: `nums = [2, 3]`, padded to `[1, 2, 3, 1]`, small enough to show every empty interval and every hit. The trace indents one level per call and notes whether the decorator ran the body or answered from the cache:

```text
  burst(0, 1) -> 0   base case, now cached under key (0, 1)
    burst(1, 2) -> 0   base case, now cached under key (1, 2)
    burst(2, 3) -> 0   base case, now cached under key (2, 3)
  burst(1, 3) -> 6   max over k, cached under key (1, 3)
    burst(0, 1) -> 0    ** cache hit, the body does not run **
    burst(1, 2) -> 0    ** cache hit, the body does not run **
  burst(0, 2) -> 6   max over k, cached under key (0, 2)
  burst(2, 3) -> 0    ** cache hit, the body does not run **
burst(0, 3) -> 9   max over k, cached under key (0, 3)
-> 9
```

`burst(2, 3)` is the behavioural difference made visible: the hand-rolled memo re-runs that base case on every visit (four times on Example 1), while the decorator answers the second visit from the cache. The root scans `k = 1` and `k = 2`, gets `0 + 6 + 1*2*1 = 8` and `6 + 0 + 1*3*1 = 9`, and returns `9`, the best order for `[2, 3]` (burst `2` for `2 * 3 = 6`, then `3` for `3`).

#### Solution

The padded recursion, unchanged, with one decorator standing in for the memo dictionary.

```python
from typing import List


class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        n = len(nums)
        nums2 = [1] + nums + [1]

        # The cache lives on this inner function object, which is rebuilt on
        # every call, so results never carry over between inputs.
        @cache
        def burst(l: int, r: int) -> int:
            if r - l < 2:
                return 0
            return max(
                burst(l, k) + burst(k, r) + nums2[l] * nums2[k] * nums2[r]
                for k in range(l + 1, r)
            )

        return burst(0, n + 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^3)`

- The cache admits each of the `O(n^2)` intervals into the body exactly once,
  and each admission scans up to `n` candidates with `O(1)` arithmetic each
- Every other call is a tuple-keyed dictionary lookup, constant time on small
  integer pairs

##### Space Complexity: `O(n^2)`

- The decorator's cache holds one entry per distinct `(l, r)` pair, including
  the empty intervals the hand-rolled memo never stored
- The recursion still descends to depth `n` along the nested chain of
  left-leaning intervals, so the stack is a lower-order term next to the cache

#### Key Insights

- `@cache` keys on the argument tuple, so it is a drop-in replacement only when
  the arguments are hashable and the function is genuinely pure; `burst` reads
  nothing but `l`, `r`, and `nums2`, which is what licenses the substitution.
- Caching the base cases is harmless here because they return a constant `0`,
  but the cache grows by `O(n)` extra entries; the same effect in the other
  direction (a cached expensive base case) would be a win.
- The generator expression inside `max` is safe because every interval has at
  least one candidate by the time the body runs (`r - l >= 2` guarantees
  `l + 1 <= r - 1`).

## Comparison of Solutions

The practice harness's `practice/burst_balloons/reference.py` implements the **Top-Down Memoization** solution.

### Time Complexity

- **Brute Force**: `O(n * n!)` - one recursion path per burst order, `O(n)` slicing work per node.
- **Top-Down Memoization**: `O(n^3)` - `O(n^2)` intervals, each scanning up to `n` last-burst candidates once.
- **Bottom-Up DP**: `O(n^3)` - the same interval/candidate loops, run as table sweeps.
- **Top-Down Memoization with functools.cache**: `O(n^3)` - the decorator reproduces the memoized run times.

### Space Complexity

- **Brute Force**: `O(n)` - recursion stack only; each level's slice is transient.
- **Top-Down Memoization**: `O(n^2)` - one memo entry per wall pair plus the stack.
- **Bottom-Up DP**: `O(n^2)` - the full `dp` table.
- **Top-Down Memoization with functools.cache**: `O(n^2)` - the decorator's cache plus the stack.

### Trade-offs

- The Brute Force is the direct transcription of the rules and needs no insight
  to trust, but it is unusable past a handful of balloons.
- The memoized pair all pay `O(n^2)` memory to collapse the factorial search;
  the last-burst frame plus padding is the one non-obvious idea they rest on.
- The Bottom-Up DP removes recursion (and with it the stack-depth consideration)
  and keeps every interval's answer, at the cost of filling cells variants may
  never read.

### When to Use Each

- **Brute Force**: as the derivational baseline and a correctness oracle for
  checking the faster versions on tiny inputs.
- **Top-Down Memoization** (recommended): the default; the last-burst recurrence
  reads directly in its recursive form and the memo collapses the cost to
  `O(n^3)`.
- **Bottom-Up DP**: when recursion depth matters or every sub-span answer will
  be queried later.
- **Top-Down Memoization with functools.cache**: the Pythonic tidy-up when the
  recursive shape is wanted and the memo should not be hand-maintained.

### Optimization Notes

- No local rule replaces the search: bursting the smallest, the largest, or the
  weakest-connected balloon first all fail on crafted inputs, because a cheap
  early burst can isolate neighbors from multipliers they needed. The interval
  frame is what makes the problem tractable at all.
- The `O(n^2)` states are tight: an interval is identified by its two walls and
  every wall pair can be needed. Sub-`O(n^3)` algorithms exist but change the
  problem's constants, not its class, and are interview-irrelevant.
- This is the same `(l, r, k)` triple as Matrix Chain Multiplication and
  Minimum Cost to Cut a Stick: interval DP with a pinned split point. The
  padding trick, adding virtual boundary elements so real edges obey the same
  formula as interior ones, transfers across the family.
- Zeros cost nothing to reason about but must still be burst (`0 <= nums[i]`);
  they never add coins and never help a neighbor, so they simply occupy
  intervals. Removing them up front shrinks constants but changes nothing
  asymptotically.
- The recursion's depth reaches `n`, far under Python's limit at the constraint
  cap of 300 balloons; the bottom-up table is the recursion-free alternative if
  the stack ever matters.
