"""String to Integer (atoi): https://leetcode.com/problems/string-to-integer-atoi/

Write-up & approaches: ../../docs/problems/string_to_integer_atoi.md

Convert a string to a 32-bit signed integer (like C's atoi): skip leading
spaces, read an optional sign, read consecutive digits, then clamp the result to
the range [-2^31, 2^31 - 1].

  uv run python string_to_integer_atoi/solution.py     # debug one case (see CASE below)
  uv run pytest string_to_integer_atoi/                # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def myAtoi(self, s: str) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in myAtoi above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().myAtoi(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
