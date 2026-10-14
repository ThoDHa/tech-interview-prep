"""Channel Max Quality — https://www.fastprep.io/problems/amazon-calculate-median-sum

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-calculate-median-sum.md

You are given a list of packets of varying sizes and there are n channels.

  uv run python amazon_oa/amazon-calculate-median-sum/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-calculate-median-sum/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def calculateMedianSum(self, packets, n):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in calculateMedianSum above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().calculateMedianSum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
