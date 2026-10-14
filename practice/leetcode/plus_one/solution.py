"""Plus One — https://leetcode.com/problems/plus-one/

Write-up & approaches: ../../docs/problems/plus_one.md

You are given an integer array `digits`, where each `digits[i]` is the `ith` digit of a large integer. It is ordered from most significant to least significant digit, and it will not contain any leadi

  uv run python plus_one/solution.py   # debug one case (see CASE below)
  uv run pytest plus_one/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def plusOne(self, digits):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in plusOne above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().plusOne(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
