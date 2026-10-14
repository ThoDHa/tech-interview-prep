"""Add Binary: https://leetcode.com/problems/add-binary/

Write-up & approaches: ../../docs/problems/add_binary.md

Given two binary strings `a` and `b`, return their sum as a binary string.

  uv run python add_binary/solution.py     # debug one case (see CASE below)
  uv run pytest add_binary/                # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def addBinary(self, a: str, b: str) -> str:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in addBinary above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().addBinary(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
