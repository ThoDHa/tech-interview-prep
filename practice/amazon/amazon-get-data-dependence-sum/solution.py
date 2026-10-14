"""Data Dependence Sum — https://www.fastprep.io/problems/amazon-get-data-dependence-sum

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-data-dependence-sum.md

Data analysts at Amazon are analyzing time-series data. It was concluded that the data of the nth item was dependent on the data of some xth day if there is a positive integer k such that floor(n / k)

  uv run python amazon_oa/amazon-get-data-dependence-sum/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-data-dependence-sum/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getDataDependenceSum(self, n):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getDataDependenceSum above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getDataDependenceSum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
