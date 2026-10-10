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

