"""Minimize Binary Subsequence Cost — https://www.fastprep.io/problems/amazon-minimize-binary-subsequence-cost

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimize-binary-subsequence-cost.md

You are given a string binaryString consisting only of '0', '1', and '!', and two integers x and y.

  uv run python amazon_oa/amazon-minimize-binary-subsequence-cost/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimize-binary-subsequence-cost/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimizeBinarySubsequenceCost(self, binaryString, x, y):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimizeBinarySubsequenceCost above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimizeBinarySubsequenceCost(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
