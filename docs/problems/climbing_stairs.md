# [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/)

**Easy** | **15 minutes** | **Dynamic Programming**

**Pattern:** [DP 1D Linear](../patterns/dp_1d_linear/intuition.md)

**Algorithm:** [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization) · [Fibonacci sequence](https://en.wikipedia.org/wiki/Fibonacci_sequence) · [Exponentiation by squaring](https://en.wikipedia.org/wiki/Exponentiation_by_squaring) · [Binet's formula](https://en.wikipedia.org/wiki/Fibonacci_sequence#Closed-form_expression)

**Practice:** [`practice/climbing_stairs/solution.py`](../../practice/climbing_stairs/solution.py)

You are climbing a staircase. It takes `n` steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

## Examples

### Example 1

**Input:** `n = 2`

**Output:** `2`

**Explanation:** There are two ways to climb to the top.

1. 1 step + 1 step
2. 2 steps

### Example 2

**Input:** `n = 3`

**Output:** `3`

**Explanation:** There are three ways to climb to the top.

1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step

## Constraints

- `1 <= n <= 45`

## Deriving the Solution

The last move onto step `n` was either a single step from `n - 1` or a double step from `n - 2`, and no climb can end both ways, so `ways(n) = ways(n - 1) + ways(n - 2)`: the Fibonacci recurrence. Every solution below evaluates that recurrence; they differ only in how much work the evaluation costs.

1. **Start literal.** Recurse on the recurrence exactly as written. Every call forks in two and the same steps are recomputed exponentially often, costing `O(2^n)`: see [Brute Force](#brute-force).
2. **Cache it.** `climb(step)` depends only on `step`, so store each answer the first time it is computed and reuse it afterward, collapsing the tree to one computation per step: `O(n)`: see [Top-Down Memoization](#top-down-memoization).
3. **Flip the direction.** The memo fills from the bottom anyway, so skip the recursion and fill a `dp` table upward from the base cases with a plain loop: see [Bottom-Up DP](#bottom-up-dp).
4. **Shrink the state.** Each `dp[i]` reads only the two entries below it, so two rolling variables replace the whole array: `O(1)` space: see [Space-Optimized DP](#space-optimized-dp).
5. **Jump instead of walk.** The recurrence is linear with constant coefficients, so one step is a fixed matrix product and `n` steps are a matrix power, computable by repeated squaring in `O(log n)`: see [Matrix Exponentiation](#matrix-exponentiation).
6. **Solve it outright.** The recurrence also admits a closed-form solution, Binet's formula, evaluated in `O(1)` floating-point arithmetic at the cost of precision: see [Closed-Form Formula](#closed-form-formula).
7. **Hand the cache to the library.** Step 2 stacked two ideas: the recurrence, and a dictionary keeping it from redoing work. Only the recurrence is the algorithm, so decorating the Brute Force function with `functools.cache` deletes the three bookkeeping lines and leaves the recursion and its base cases untouched: see [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Brute Force

#### Derivation

The most direct idea restates the problem as a recurrence and counts every path by hand. The question it asks is simply "how could the climb have ended?": to stand on step `n`, the final move was either a single step from `n - 1` or a double step from `n - 2`, so the count for `n` is the sum of the counts for those two predecessors. [Recursing](https://en.wikipedia.org/wiki/Recursion_(computer_science)) without any caching explores the full tree of choices:

1. If `step` is 0 or 1, return 1, since each of those positions is reached exactly one way (an empty climb for 0, a single move for 1)
2. Otherwise return `climb(step - 1) + climb(step - 2)`, summing the ways the two legal final moves could have arrived
3. Let the recursion fan out into a binary tree of calls, recomputing shared subproblems independently

#### Walkthrough

Trace the Brute Force on Example 1, `n = 2`. The call begins with `climb(2)`, and each call that is above 1 splits into two child calls, `climb(step - 1)` and `climb(step - 2)`, whose returned counts are summed on the way back up.

The call tree, with each call's return value shown as it unwinds:

```text
climb(2)                          step 2 > 1, so it splits
├── climb(1)  -> 1                step <= 1: base case, returns 1
└── climb(0)  -> 1                step <= 1: base case, returns 1
climb(2)      -> 1 + 1 = 2        sums the two children
```

Reading it as state changing step by step:

| Step | Call | What happens | Returns |
|------|------|--------------|---------|
| 1 | `climb(2)` | `2 > 1`, so recurse into `climb(1) + climb(0)` | pending |
| 2 | `climb(1)` | `step <= 1`: base case | `1` |
| 3 | `climb(0)` | `step <= 1`: base case | `1` |
| 4 | `climb(2)` resumes | combines children: `1 + 1` | `2` |

The outer call `climb(2)` returns `2`, which matches the expected Output `2` for Example 1. With a larger `n` the tree would fan out much wider, and the same subproblems (such as `climb(0)` and `climb(1)`) would be recomputed many times: that repeated work is exactly what the later memoized solutions eliminate.

#### Solution

The code is the recurrence from the walkthrough written down: the base cases, then the two-way split.

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        def climb(step: int) -> int:
            # One empty path reaches step 0, and exactly one way reaches step 1
            if step <= 1:
                return 1

            # The last move was either a single step from step - 1
            # or a double step from step - 2
            return climb(step - 1) + climb(step - 2)

        return climb(n)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

- Each call spawns two more, so the call tree roughly doubles at every level
- The number of nodes grows like the Fibonacci numbers, which is exponential in `n`

##### Space Complexity: `O(n)`

- No auxiliary table is allocated, but the recursion stack reaches depth `n` along the deepest path

#### Key Insights

- Writing the recurrence directly from the problem statement is the simplest, most discoverable formulation
- The same step is recomputed exponentially often, which is exactly the waste the later solutions remove
- This baseline is correct but only practical for small `n`; it makes the case for memoization concrete

### Top-Down Memoization

#### Derivation

The Brute Force call tree recomputes the same values relentlessly, yet `climb(step)` depends on nothing but `step`: every one of the exponentially many calls with the same argument returns the same number. The repair is to [cache each step's result](https://en.wikipedia.org/wiki/Memoization) in a hand-rolled dictionary so no subproblem is solved twice:

1. The number of ways to reach step `n` equals the ways to reach `n - 1` (then take a single step) plus the ways to reach `n - 2` (then take a double step)
2. Base cases return 1 for steps 0 and 1, since each has exactly one way to be reached
3. Before recursing, check the `memo` dictionary; the first time a step is computed, store it so later calls return instantly
4. This collapses the exponential call tree into one computation per distinct step

#### Walkthrough

Example 1 (`n = 2`) and Example 2 (`n = 3`) finish before any cached step is needed a second time: their only repeated calls are the base cases `0` and `1`, which return before ever touching the memo. To see a cache hit we use the tailored input `n = 4`, the smallest climb whose recursion revisits a memoized step.

The trace indents one level per recursive call; the marked line is the revisit:

```text
climb(4)                 4 not in memo -> recurse
  climb(3)               3 not in memo -> recurse
    climb(2)             2 not in memo -> recurse
      climb(1) -> 1      base case
      climb(0) -> 1      base case
    climb(2) -> 2        memo[2] = 1 + 1 = 2
    climb(1) -> 1        base case
  climb(3) -> 3          memo[3] = 2 + 1 = 3
  climb(2) -> 2          ** memo hit, no recursion **
climb(4) -> 5            memo[4] = 3 + 2 = 5
```

The step `2` is needed twice: once inside `climb(3)` and once directly by `climb(4)`. The first visit computes and stores `memo[2] = 2`; the second answers straight from the dictionary without re-spawning the `climb(1)`/`climb(0)` subtree. The call returns `5`, which is indeed the count for `n = 4`: `1+1+1+1`, `1+1+2`, `1+2+1`, `2+1+1`, and `2+2`.

#### Solution

The code is the Brute Force recursion with the memo check and store wrapped around the split.

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        memo = {}

        def climb(step: int) -> int:
            # Base cases: a single empty path reaches step 0,
            # and exactly one way reaches step 1
            if step <= 1:
                return 1
            if step in memo:
                return memo[step]

            # The last move was either a single step from step - 1
            # or a double step from step - 2
            memo[step] = climb(step - 1) + climb(step - 2)
            return memo[step]

        return climb(n)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- Memoization ensures each step from 2 to n is computed exactly once
- Each computation combines two cached values in constant time

##### Space Complexity: `O(n)`

- The cache stores one entry per step, and the recursion stack reaches depth n

#### Key Insights

- This problem follows the Fibonacci sequence pattern, so the recurrence is the Fibonacci recurrence
- Writing the dictionary out by hand shows the mechanism (check, compute, store) that a decorator would otherwise hide, which is worth seeing once; `functools.cache` collapses those same three lines and is the version to reach for afterwards, see [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache)
- Memoization converts the exponential naive recursion into a linear-time solution
- Top-down recursion expresses the relationship most directly, which makes it a natural step before deriving the iterative versions

### Bottom-Up DP

#### Derivation

The memoized recursion still starts at `n` and unwinds all the way down before producing its first useful value, paying call overhead and stack depth `n` along the way. But watch the order in which its memo actually fills: the deepest calls resolve first, so entries appear for step 2, then 3, and so on upward. Bottom-up [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) with tabulation produces the same table in the same order with a plain loop and no recursion at all:

1. We create a DP array where `dp[i]` represents the number of ways to climb to the ith step
2. Base cases: `dp[0] = dp[1] = 1` (there's only one way to reach steps 0 and 1)
3. For steps 2 through n, we apply the recurrence relation: `dp[i] = dp[i-1] + dp[i-2]`
4. This relation captures that to reach step i, we can either:
    - Take a single step from step i-1
    - Take a double step from step i-2

#### Recurrence

Let `dp[i]` be the number of distinct ways to reach step `i`:

$$ dp[i] = \begin{cases} 1, & i \le 1 \\[4pt] dp[i-1] + dp[i-2], & i \ge 2 \end{cases} $$

```text
dp[i] = 1,                     for i <= 1
dp[i] = dp[i-1] + dp[i-2],     for i >= 2
```

This is the Fibonacci recurrence with the index shifted by one, so \(dp[n] = F(n+1)\) under the usual convention \(F(0)=0,\ F(1)=1\). That shift is why the two solutions further down, which compute Fibonacci numbers directly, read the answer off `F(n+1)` rather than `F(n)`.

#### Walkthrough

Let us fill the table on Example 2, `n = 3`. The array starts with the base cases in place, and each iteration sums the two entries just below it:

```text
start    dp = [1, 1, 0, 0]              dp[0] = dp[1] = 1
i = 2    dp[2] = dp[1] + dp[0] = 2      dp = [1, 1, 2, 0]
i = 3    dp[3] = dp[2] + dp[1] = 3      dp = [1, 1, 2, 3]
```

The method returns `dp[3] = 3`, matching the expected Output for Example 2: the three climbs `1+1+1`, `1+2`, and `2+1`.

#### Solution

The code is the table fill from the walkthrough: seed the base cases, then loop the recurrence upward.

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 1:
            return 1

        # Create array to store number of ways to reach each step
        dp = [0] * (n + 1)
        dp[0] = dp[1] = 1

        # Fill dp array using recurrence relation
        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]

        return dp[n]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- We iterate through the array once from 2 to n
- Each iteration involves constant time operations

##### Space Complexity: `O(n)`

- We use an array of size n+1 to store the intermediate results

#### Key Insights

- This problem follows the Fibonacci sequence pattern
- The dynamic programming approach breaks down the problem into simpler subproblems
- By storing results of subproblems, we avoid redundant calculations

### Space-Optimized DP

#### Derivation

The Bottom-Up table stores all `n + 1` entries, yet the loop body only ever reads `dp[i - 1]` and `dp[i - 2]`: everything older is dead weight. The repair keeps just those two values in rolling variables:

1. We observe that at any step, we only need the previous two values in the sequence
2. Instead of using an array to store all intermediate results, we use the two variables `previous` and `current`
3. We iteratively update these variables as we move up the staircase, saving the old `current` in `saved_current` before overwriting it so `previous` can advance correctly
4. This maintains the same logic as the Bottom-Up DP approach but uses O(1) space

#### Walkthrough

Let us run the rolling pair on Example 2, `n = 3`. At the top of each iteration, `previous` and `current` play the roles of `dp[i - 2]` and `dp[i - 1]`:

```text
start    previous = 1, current = 1                                ways to reach steps 0 and 1
i = 2    saved_current = 1; current = 1 + 1 = 2; previous = 1     (previous, current) = (1, 2)
i = 3    saved_current = 2; current = 1 + 2 = 3; previous = 2     (previous, current) = (2, 3)
```

After the loop, `current` holds the count for step `3`. The method returns `3`, matching the expected Output for Example 2.

#### Solution

The code is the walkthrough's update loop: save `current` in `saved_current`, roll both variables forward.

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 1:
            return 1

        # Initialize first two numbers in the sequence
        previous, current = 1, 1

        # Calculate subsequent numbers using only two variables
        for i in range(2, n + 1):
            saved_current = current
            current = previous + current
            previous = saved_current

        return current
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- We still need to iterate through each step from 2 to n once

##### Space Complexity: `O(1)`

- We use only a constant amount of extra space regardless of input size

#### Key Insights

- When a DP solution only depends on a fixed number of previous states, we can optimize space usage
- This approach is particularly useful for large inputs where memory might be a concern
- The solution maintains the elegance of the DP approach while being more efficient

### Matrix Exponentiation

#### Derivation

Every approach so far advances the recurrence one step per iteration, so none can beat `O(n)`. The recurrence is linear with constant coefficients, though, and such recurrences can be advanced in jumps: one step is a fixed matrix product, so `n` steps are the `n`th power of that matrix, and powers can be computed with [repeated squaring](https://en.wikipedia.org/wiki/Exponentiation_by_squaring) rather than one multiplication at a time, dropping the time below linear:

1. The recurrence `F(n+1) = F(n) + F(n-1)` can be packaged as a matrix equation: multiplying the state vector `[F(n), F(n-1)]` by the matrix `[[1, 1], [1, 0]]` advances it one step to `[F(n+1), F(n)]`
2. Advancing `n` steps therefore means raising that matrix to the nth power: `[[1, 1], [1, 0]]^n = [[F(n+1), F(n)], [F(n), F(n-1)]]`, and since the ways to climb `n` stairs equal `F(n+1)`, the answer sits in the top-left entry
3. Instead of multiplying the matrix in one at a time (which would just be the linear DP in disguise), we use binary exponentiation: square the base matrix to jump from `M^k` to `M^2k`, and multiply the accumulator `result` by the current `base` whenever the corresponding bit of `n` is set, halving the remaining `power` each iteration
4. Both the `multiply` helper and the squaring loop are written from scratch on plain lists, so the whole computation stays in exact integer arithmetic

Compared to its neighbors on the ladder, this trades their `O(n)` scans for `O(log n)` doublings, so for huge exponents it overtakes every linear approach; and unlike the Closed-Form Formula that follows, it never touches floating point, so the answer is exact at any size.

#### Closed Form (Matrix Power)

One step of the recurrence is a single matrix-vector product, which stacks into a matrix power:

$$ \begin{pmatrix} F(n+1) \\ F(n) \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} F(n) \\ F(n-1) \end{pmatrix} \qquad\Longrightarrow\qquad \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^{n} = \begin{pmatrix} F(n+1) & F(n) \\ F(n) & F(n-1) \end{pmatrix} $$

```text
[[1, 1], [1, 0]] * [F(n), F(n-1)] = [F(n+1), F(n)]     (column vectors)
    implies  [[1, 1], [1, 0]]^n = [[F(n+1), F(n)], [F(n), F(n-1)]]
             with F(0) = 0, F(1) = 1
```

Here \(F\) is the Fibonacci sequence under the usual convention \(F(0) = 0,\ F(1) = 1\), which also supplies the base of the identity: at \(n = 1\) it reads \(\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix} = \begin{pmatrix} F(2) & F(1) \\ F(1) & F(0) \end{pmatrix}\), true because \(F(2) = 1\). The answer `ways(n)` is \(F(n+1)\), the top-left entry. Binary exponentiation then evaluates the power in \(O(\log n)\) multiplications by squaring rather than multiplying the matrix in one copy at a time.

#### Walkthrough

Trace the binary exponentiation on Example 2, `n = 3`. In binary, `3 = 11`, so the loop runs twice and multiplies the accumulator on both passes. Writing `M = [[1, 1], [1, 0]]`:

| Pass | `power` | Bit set? | `result` after | `base` after |
|------|---------|----------|----------------|--------------|
| start | 3 | - | `[[1, 0], [0, 1]]` (identity) | `M` |
| 1 | 3 | yes, so `result = result x M` | `[[1, 1], [1, 0]]` = `M` | `M^2 = [[2, 1], [1, 1]]` |
| 2 | 1 | yes, so `result = result x M^2` | `M^3 = [[3, 2], [2, 1]]` | `M^4` (unused) |
| end | 0 | - | loop exits | - |

The accumulator now holds `M^3 = [[3, 2], [2, 1]]`, whose top-left entry is `F(4) = 3`. That matches the expected Output `3` for Example 2: two squarings and two multiplications instead of a step-by-step walk, and for `n = 45` the loop would take only 6 passes instead of 44 iterations.

#### Solution

The code is the squaring loop from the walkthrough, with the `multiply` helper written out entry by entry.

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        def multiply(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
            # Hand-rolled 2x2 matrix product, all four entries written out
            return [
                [
                    a[0][0] * b[0][0] + a[0][1] * b[1][0],
                    a[0][0] * b[0][1] + a[0][1] * b[1][1],
                ],
                [
                    a[1][0] * b[0][0] + a[1][1] * b[1][0],
                    a[1][0] * b[0][1] + a[1][1] * b[1][1],
                ],
            ]

        # Start from the 2x2 identity matrix; base is the Fibonacci matrix
        result = [[1, 0], [0, 1]]
        base = [[1, 1], [1, 0]]

        # Binary exponentiation: square the base, halve the exponent
        power = n
        while power > 0:
            if power % 2 == 1:
                result = multiply(result, base)
            base = multiply(base, base)
            power //= 2

        # [[1, 1], [1, 0]]^n = [[F(n+1), F(n)], [F(n), F(n-1)]],
        # and ways(n) = F(n+1), which sits in the top-left entry
        return result[0][0]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

- The exponent is halved on every pass, so the loop runs about `log2(n)` times
- Each pass performs at most two 2x2 matrix multiplications, and each of those is a fixed bundle of 8 multiplications and 4 additions, so the per-iteration cost is constant (for the word-sized integers here; astronomically large `n` would grow the integers themselves)

##### Space Complexity: `O(1)`

- The iterative loop keeps only two 2x2 matrices (`result` and `base`) plus a scalar, regardless of `n`
- A recursive formulation of the squaring would cost `O(log n)` stack; the iterative loop avoids it

#### Key Insights

- Any linear recurrence with constant coefficients can be encoded as a fixed transition matrix, and computing the nth term becomes computing a matrix power; this generalizes far beyond Fibonacci (tribonacci, tiling counts, counting walks in graphs)
- Binary exponentiation is the engine: it works for matrices exactly as it does for numbers because matrix multiplication is associative, which is all repeated squaring requires
- Unlike Binet's formula, every operation here is integer addition and multiplication, so the result is exact for arbitrarily large `n`; Python's big integers never overflow, whereas the float closed form drifts off by one once `n` grows
- With the constraint capping `n` at 45, the `O(log n)` advantage is invisible in practice and the constant factor of matrix multiplies makes it slower than the two-variable loop; the technique earns its keep when `n` reaches into the millions or when the recurrence's answer is needed modulo some number

### Closed-Form Formula

#### Derivation

Even the matrix power still iterates, if only `O(log n)` times. The last refinement removes iteration altogether: the Fibonacci recurrence can be solved outright, and evaluating the resulting closed form is a constant amount of floating-point arithmetic:

1. Since the climbing stairs problem follows the Fibonacci sequence with `ways(n) = F(n+1)`, computing the answer means evaluating a single Fibonacci number
2. We can use the mathematical closed-form solution ([Binet's formula](https://en.wikipedia.org/wiki/Fibonacci_sequence#Closed-form_expression)): `F(n) = (φ^n - ψ^n)/√5`, which the code evaluates at `n + 1`
3. Where φ is the golden ratio `(1 + √5)/2` and ψ is its conjugate `(1 - √5)/2`

#### Closed Form

[Binet's formula](https://en.wikipedia.org/wiki/Fibonacci_sequence#Closed-form_expression) gives the nth Fibonacci number with no iteration at all:

$$ F(n) = \frac{\varphi^{\,n} - \psi^{\,n}}{\sqrt{5}}, \qquad \varphi = \frac{1 + \sqrt{5}}{2}, \qquad \psi = \frac{1 - \sqrt{5}}{2} $$

```text
F(n) = (phi**n - psi**n) / sqrt(5)
       phi = (1 + sqrt(5)) / 2
       psi = (1 - sqrt(5)) / 2
```

Since \(dp[n] = F(n+1)\), the code evaluates the expression at `n + 1`. The two roots \(\varphi\) and \(\psi\) are exactly the solutions of \(x^2 = x + 1\), the characteristic equation of the recurrence, which is why a sum of their powers satisfies it. Because \(|\psi| < 1\), the second term shrinks toward zero and \(F(n)\) is simply \(\varphi^{\,n}/\sqrt{5}\) rounded to the nearest integer.

#### Walkthrough

Let us evaluate the formula on Example 2, `n = 3`. Because `ways(3) = F(4)`, the code raises both roots to the power `n + 1 = 4`:

```text
sqrt5    = 2.23606797749979
phi      = (1 + sqrt5) / 2 =  1.618033988749895
psi      = (1 - sqrt5) / 2 = -0.6180339887498949
phi**4   = 6.854101966249686           the dominant term
psi**4   = 0.14589803375031551         the vanishing correction
fibn     = 6.854101966249686 - 0.14589803375031551 = 6.70820393249937
fibn / sqrt5 = 3.0000000000000004
round(3.0000000000000004) = 3
```

The quotient lands a hair above the exact value `3` this time, but floating-point error can just as easily land a hair *below* it, where truncation would return one too few. Rounding to the nearest integer absorbs the error in both directions, which is why the code uses `round` rather than `int`. The method returns `3`, matching the expected Output for Example 2.

#### Solution

The code is the evaluation from the walkthrough: two powers, one subtraction, one division, one rounding.

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        import math

        # Fibonacci closed form formula (Binet's formula)
        sqrt5 = math.sqrt(5)
        fibn = ((1 + sqrt5) / 2) ** (n + 1) - ((1 - sqrt5) / 2) ** (n + 1)
        return round(fibn / sqrt5)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)`

- The calculation is done in constant time regardless of n
- However, for very large n, there might be precision issues

##### Space Complexity: `O(1)`

- Only a constant amount of variables are used

#### Key Insights

- Recognizing the problem follows the Fibonacci sequence unlocks a mathematical solution
- This approach is theoretically the most efficient but may face floating-point precision issues
- It's more of a mathematical curiosity than a practical solution for very large n

### Top-Down Memoization with functools.cache

#### Derivation

The [Top-Down Memoization](#top-down-memoization) solution stacks two separate things: the Fibonacci recurrence, and a dictionary that stops the recursion from recomputing a step it has already answered. Only the first is the algorithm. The second is pure bookkeeping, and the standard library already implements it. Decorating the function with [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) attaches an unbounded cache keyed by the call's arguments, consulted before the body runs and filled with whatever the body returns, so the recurrence and its base cases stay on the page exactly as the Brute Force wrote them:

1. Keep `climb(step)` verbatim from the Brute Force: return 1 when `step <= 1`,
   otherwise return `climb(step - 1) + climb(step - 2)`
2. Decorate it with `@cache`, so each distinct `step` runs the body at most once
   and every later request for that step is answered from the cache
3. Delete the three bookkeeping lines the decorator now owns: the `memo = {}`
   declaration, the `if step in memo` lookup, and the `memo[step] = ...` store
4. Because `climb` is defined inside `climbStairs`, each call builds a fresh
   function object with a fresh cache, so nothing leaks between inputs; a `@cache` on a method or a module-level function would instead live for the whole process

One behavioural difference follows from where the decorator sits. The hand-rolled version answers `step <= 1` before it ever consults `memo`, so the base cases are never stored; `@cache` wraps the entire body, so steps `0` and `1` are cached like any other step.

#### Walkthrough

Run it on Example 2, `n = 3`. The trace indents one level per call and notes whether the decorator ran the body or answered from the cache:

```text
climb(3)   miss, run the body
  climb(2)   miss, run the body
    climb(1) -> 1     base case, now cached under key 1
    climb(0) -> 1     base case, now cached under key 0
  climb(2) -> 2       1 + 1, cached under key 2
  climb(1) -> 1       ** cache hit, the body does not run **
climb(3) -> 3         2 + 1, cached under key 3
```

`climb(3)` needs both `climb(2)` and `climb(1)`. Resolving `climb(2)` first computes and caches `climb(1)`, so when `climb(3)` asks for `climb(1)` in its own right the decorator returns `1` immediately. The hand-rolled memo would have re-entered the function there, cheaply (it is a base case) but visibly, which is why that version needed `n = 4` before a hit appeared. The outer call returns `3`, matching the expected Output `3` for Example 2.

#### Solution

The Brute Force recursion, unchanged, with one decorator standing in for the memo dictionary.

```python
from functools import cache


class Solution:
    def climbStairs(self, n: int) -> int:
        # The cache lives on this inner function object, which is rebuilt on
        # every call, so results never carry over between inputs.
        @cache
        def climb(step: int) -> int:
            # One empty path reaches step 0, and exactly one way reaches step 1
            if step <= 1:
                return 1

            # The last move was either a single step from step - 1
            # or a double step from step - 2
            return climb(step - 1) + climb(step - 2)

        return climb(n)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- The cache admits each step from `0` to `n` into the body exactly once, and
  each admission does one addition of two already-known values
- Every other call is a dictionary lookup on a small integer key, which is
  constant time, so the total is linear in `n`

##### Space Complexity: `O(n)`

- The decorator's cache holds one entry per distinct step, `n + 1` entries once
  the base cases are counted, which the hand-rolled memo excluded
- The recursion still descends to depth `n` before the first value returns, so
  the stack matches the cache in order of growth

#### Key Insights

- The algorithm is untouched: the recurrence and both base cases read exactly as
  they do in the Brute Force, which makes plain that memoization is an execution strategy rather than a change to the recursion
- `@cache` keys on the argument tuple, so it is a drop-in replacement only when
  the arguments are hashable and the function is genuinely pure; `climb` reads nothing but `step`, which is what licenses the substitution
- Defining the cached function inside the method scopes the cache to a single
  call, avoiding the stale-results and unbounded-growth hazards of decorating a method or a module-level function
- Use `functools.lru_cache(maxsize=...)` instead when the key space is unbounded
  and eviction matters; `cache` is `lru_cache(maxsize=None)`, which never evicts

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(2^n)` - The uncached call tree doubles at each level, growing exponentially
- **Top-Down Memoization**: `O(n)` - Each step is computed once and cached
- **Bottom-Up DP**: `O(n)` - Linear time to build the DP table
- **Space-Optimized DP**: `O(n)` - Same linear time requirement
- **Matrix Exponentiation**: `O(log n)` - Repeated squaring halves the exponent each iteration
- **Closed-Form Formula**: `O(1)` - Constant time calculation
- **Top-Down Memoization with functools.cache**: `O(n)`: the same
  one-computation-per-step bound, with the decorator's lookup standing in for the hand-written one

### Space Complexity

- **Brute Force**: `O(n)` - No cache, but the recursion stack reaches depth n
- **Top-Down Memoization**: `O(n)` - Cache holds one entry per step plus a recursion stack of depth n
- **Bottom-Up DP**: `O(n)` - Requires an array of size n+1
- **Space-Optimized DP**: `O(1)` - Uses only a constant amount of extra space
- **Matrix Exponentiation**: `O(1)` - Holds two fixed-size 2x2 matrices; the iterative loop avoids recursion stack
- **Closed-Form Formula**: `O(1)` - Uses only a constant amount of extra space
- **Top-Down Memoization with functools.cache**: `O(n)`: cache plus recursion
  stack, as above, with `n + 1` cache entries because the decorator stores the base cases the hand-rolled memo skipped

### Trade-offs

- **Brute Force** maps the recurrence onto the problem statement most directly, but recomputes shared subproblems exponentially often, so it is only viable for small n
- **Top-Down Memoization** mirrors the recurrence most directly and computes only the steps it needs, but carries recursion overhead and stack depth proportional to n
- **Bottom-Up DP** is intuitive and good for educational purposes, but uses more space
- **Space-Optimized DP** provides the best balance of simplicity and efficiency for most cases
- **Matrix Exponentiation** beats every linear approach asymptotically and stays exact in integer arithmetic, but its per-step constant (a bundle of 2x2 multiplies) and extra code make it overkill at this problem's scale
- **Closed-Form Formula** is theoretically most efficient but can have numerical precision issues
- **Top-Down Memoization with functools.cache** keeps the recurrence and the
  linear complexity of the hand-rolled version while cutting three lines of memo plumbing, paying an import and giving up direct control over what the cache keys on, how long it lives, and when it evicts

### When to Use Each

- **Brute Force**: When first deriving the recurrence, or as a teaching baseline that motivates memoization
- **Top-Down Memoization**: When recursive thinking feels most natural or as the first step before deriving an iterative solution
- **Bottom-Up DP**: When teaching DP concepts or when space is not a concern
- **Space-Optimized DP**: In most practical scenarios, efficient and easy to understand
- **Matrix Exponentiation**: When n is huge (millions or more) or an exact answer is required beyond floating-point range, such as computing the count modulo a large prime
- **Closed-Form Formula**: When absolute performance is critical and n is within the range of floating-point precision
- **Top-Down Memoization with functools.cache**: The Pythonic default whenever
  the recursive framing is the one worth showing. Prefer it over the hand-rolled memo for readability, and fall back to the explicit dictionary when an interviewer asks to see the caching mechanism itself or when the cache needs custom keying, eviction, or a lifetime you control

### Optimization Notes

- **Space-Optimized DP is the recommended choice**: it preserves the linear-time clarity of the tabulation approach while collapsing the DP array down to two rolling variables, giving `O(1)` space without sacrificing readability
- The Brute Force is the from-scratch starting point; adding a cache to it is exactly what turns its `O(2^n)` time into the memoized `O(n)`
- Top-Down Memoization reaches the same linear complexity, so prefer it when the recursive framing is clearer, but be mindful of Python's recursion limit for large n (the constraint here caps n at 45, well within bounds)
- When the recursive framing is the one you want, write it as `@cache` on the Brute Force function rather than as a hand-rolled dictionary: the two have identical complexity, and the decorator removes the three lines where an off-by-one in the check-or-store logic could hide
- A key implementation detail is the use of a `saved_current` variable when updating `previous` and `current`: the old `current` must be saved before it is overwritten, otherwise `previous` would advance incorrectly and break the Fibonacci recurrence
- Avoid reaching for the Closed-Form Formula (Binet's formula) in production: although it is `O(1)`, raising the golden ratio to a power relies on floating-point arithmetic that accumulates rounding error and can return an off-by-one result for larger `n`
- Matrix Exponentiation is the exact-arithmetic answer to that precision problem: it reaches `O(log n)` without ever leaving integers, so prefer it over Binet's formula whenever sub-linear time is genuinely needed; within this problem's `n <= 45` cap, though, the two-variable loop remains the pragmatic winner
- Remember the base-case guard `if n <= 1: return 1` in all approaches; without it the loop never runs and the rolling-variable initialization silently returns the wrong count for `n = 0`
