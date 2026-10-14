"""Get Min Change — https://www.fastprep.io/problems/amazon-get-minimum-changes

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-minimum-changes.md

Amazon's software developers are working on enhancing their inventory management system with a new pricing adjustment operation on an array of products, where the price of the i^th product is given by

  uv run python amazon_oa/amazon-get-minimum-changes/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-minimum-changes/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMinimumChanges(self, prod_price, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMinimumChanges above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMinimumChanges(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
