"""Find Max Value — https://www.fastprep.io/problems/amazon-find-max-value

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-max-value.md

Amazon’s engineering team is developing a tool designed to minimize the size of an n x n grid named matrix, based on a compression ratio described by the array limit. Their challenge is to compute the

  uv run python amazon_oa/amazon-find-max-value/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-max-value/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findMaxValue(self, limit, matrix, x):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMaxValue above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMaxValue(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
