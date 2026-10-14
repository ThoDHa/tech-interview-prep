"""Pow(x, n) — https://leetcode.com/problems/powx-n/

Write-up & approaches: ../../docs/problems/powx_n.md
Canonical reference implementation: the write-up's Iterative Binary
Exponentiation solution (exponentiation by squaring). Your own attempt
lives in solution.py.

`Pow(x, n)` is a mathematical function to calculate the value of `x` raised
to the power of `n` (i.e., `x^n`). Given a floating-point value `x` and an
integer value `n`, implement the `myPow(x, n)` function, which calculates
`x` raised to the power `n`.

  uv run python powx_n/reference.py   # replay the example cases
  uv run pytest powx_n/               # run the test sets
"""

from harness import pick_case


class Solution:
    def myPow(self, x: float, n: int) -> float:
        """Compute x raised to the integer power n by binary exponentiation.

        Consumes n's binary digits from the low end: a running `base` holds
        `x^(2^k)` at bit position k, and `result` accumulates a factor of
        `base` exactly where n's bit is 1. Negative exponents return the
        reciprocal of the positive power.

        Args:
            x: The base, -100.0 < x < 100.0 (and not 0 when n <= 0).
            n: The exponent, -2^31 <= n <= 2^31 - 1.

        Returns:
            x^n as a float; x^0 is 1.0.

        Time:  O(log n): one loop iteration per bit of n, at most 31
            iterations at the constraint cap, constant work per bit.
        Space: O(1): two running variables and no call stack.
        """
        if n == 0:
            return 1.0
        if n < 0:
            return 1.0 / self.myPow(x, -n)

        result = 1.0
        base = x
        while n > 0:
            if n & 1:
                result *= base
            base *= base
            n >>= 1
        return result


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2", "example_3"):
        case = pick_case(__file__, case_id)
        result = Solution().myPow(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
