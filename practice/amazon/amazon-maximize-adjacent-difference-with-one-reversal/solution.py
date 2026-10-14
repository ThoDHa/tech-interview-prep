"""Maximize Adjacent Difference With One Reversal — https://www.fastprep.io/problems/amazon-maximize-adjacent-difference-with-one-reversal

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximize-adjacent-difference-with-one-reversal.md

Given an integer array values, define its score as the sum of abs(values[i] - values[i + 1]) over every adjacent pair.

  uv run python amazon_oa/amazon-maximize-adjacent-difference-with-one-reversal/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximize-adjacent-difference-with-one-reversal/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximizeArrayScore(self, values):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximizeArrayScore above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximizeArrayScore(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
