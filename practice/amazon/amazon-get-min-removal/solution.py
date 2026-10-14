"""Get Min Removal — https://www.fastprep.io/problems/amazon-get-min-removal

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-min-removal.md

There are n products in an Amazon catalogue, where the category of the i^th product is represented by the array catalogue.

  uv run python amazon_oa/amazon-get-min-removal/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-min-removal/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getminRemoval(self, catalogue, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getminRemoval above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getminRemoval(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
