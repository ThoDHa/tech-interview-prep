"""Min Num Unique Distribution Hubs — https://www.fastprep.io/problems/amazon-get-minimum-number-of-unique-distribution-centers

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-minimum-number-of-unique-distribution-centers.md

A well-known consumer brand selling everyday products on Amazon is facing a supply issue due to daily changes in product demand. To manage this, Amazon has set up n distribution hubs, each labeled wit

  uv run python amazon_oa/amazon-get-minimum-number-of-unique-distribution-centers/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-minimum-number-of-unique-distribution-centers/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMinimumNumberOfUniqueDistributionCenters(self, n, dailyTrend):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMinimumNumberOfUniqueDistributionCenters above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMinimumNumberOfUniqueDistributionCenters(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
