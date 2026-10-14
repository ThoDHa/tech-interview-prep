"""Multiply Strings — https://leetcode.com/problems/multiply-strings/

Write-up & approaches: ../../docs/problems/multiply_strings.md
Canonical reference implementation: the write-up's Position Accumulator
solution (schoolbook grid into one bucket array). Your own attempt lives in
solution.py.

You are given two strings `num1` and `num2` that represent non-negative
integers. Return the product of `num1` and `num2` in the form of a string.
Neither input contains any leading zero, unless it is the number `0` itself,
and built-in big-integer conversion is off limits.

  uv run python multiply_strings/reference.py   # replay the example cases
  uv run pytest multiply_strings/               # run the test sets
"""

from harness import pick_case


class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        """Multiply two digit strings without big-integer conversion.

        Uses the schoolbook grid index law: digit `i` of `num1` times digit
        `j` of `num2` contributes to result positions `i + j` (carry) and
        `i + j + 1` (digit). Every pairwise product is folded into a single
        `m + n` bucket array with carries settled in-loop, then leading
        zeros are skipped on the way to the output string.

        Args:
            num1: First factor as decimal digits, no leading zero unless
                the number is "0".
            num2: Second factor, same format.

        Returns:
            The exact product as a decimal string; "0" when either factor
            is "0".

        Time:  O(m * n): one constant-time bucket update per digit pair,
            plus an O(m + n) final read-out.
        Space: O(m + n): the bucket array, exactly the largest product's
            digit count; every bucket holds a single digit throughout.
        """
        if num1 == "0" or num2 == "0":
            return "0"
        m, n = len(num1), len(num2)
        pos = [0] * (m + n)
        for i in range(m - 1, -1, -1):
            d1 = ord(num1[i]) - ord("0")
            for j in range(n - 1, -1, -1):
                d2 = ord(num2[j]) - ord("0")
                total = pos[i + j + 1] + d1 * d2
                pos[i + j + 1] = total % 10
                pos[i + j] += total // 10
        start = 0
        while start < len(pos) - 1 and pos[start] == 0:
            start += 1
        return "".join(chr(p + ord("0")) for p in pos[start:])


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().multiply(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
