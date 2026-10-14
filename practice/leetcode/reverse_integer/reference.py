"""Reverse Integer — https://leetcode.com/problems/reverse-integer/

Write-up & approaches: ../../docs/problems/reverse_integer.md
Reference implementation of the write-up's Pop-and-Push with Pre-Check
solution, kept next to the harness so authored cases stay falsifiable.
Your own attempt lives in solution.py.

  uv run python reverse_integer/reference.py   # replay the example cases
  uv run pytest reverse_integer/               # run the test sets
"""

from harness import pick_case

INT_MAX_DIGITS = (2**31 - 1) // 10


class Solution:
    def reverse(self, x: int) -> int:
        """Return `x`'s decimal digits reversed, or `0` on 32-bit overflow.

        Peels `x`'s last digit and pushes it onto the result with the
        shift-multiply `rev = rev * 10 + digit`. Before each push, the
        pre-check `rev > INT_MAX_DIGITS` (or equal with an oversized
        digit) proves the push would leave the signed 32-bit range, so
        the function bails with `0` before any out-of-range value exists.

        Args:
            x: A signed 32-bit integer.

        Returns:
            The digit reversal of `x`, or `0` when it overflows.

        Time:  O(log |x|): one constant step per decimal digit.
        Space: O(1): sign flag plus the two working integers.
        """
        sign = -1 if x < 0 else 1
        n = -x if x < 0 else x
        rev = 0
        while n:
            digit = n % 10
            n //= 10
            if rev > INT_MAX_DIGITS or (rev == INT_MAX_DIGITS and digit > 7):
                return 0
            rev = rev * 10 + digit
        return sign * rev


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2", "example_3"):
        case = pick_case(__file__, case_id)
        result = Solution().reverse(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
