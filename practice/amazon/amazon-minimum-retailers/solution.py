"""Min Retailers — https://www.fastprep.io/problems/amazon-minimum-retailers

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimum-retailers.md

An online marketplace has onboarded n retailers, each operating within a designated geographical range. Retailer i operates over the interval from regionStart[i] to regionEnd[i] (inclusive on both end

  uv run python amazon_oa/amazon-minimum-retailers/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimum-retailers/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimumRetailers(self, zoneStart, zoneEnd):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumRetailers above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimumRetailers(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
