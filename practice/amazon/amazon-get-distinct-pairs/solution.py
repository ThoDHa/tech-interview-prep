"""Get Distinct Pairs — https://www.fastprep.io/problems/amazon-get-distinct-pairs

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-distinct-pairs.md

A financial strategist at Amazon Web Services (AWS) is analyzing a collection of profitable investments, each represented by an integer array. Every value in the array indicates the annual gain of a p

  uv run python amazon_oa/amazon-get-distinct-pairs/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-distinct-pairs/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getDistinctPairs(self, stocksProfit, target):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getDistinctPairs above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getDistinctPairs(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
