"""Get Smaller Items — https://www.fastprep.io/problems/amazon-get-smaller-items

Write-up & approaches: ../../../docs/amazon/amazon-get-smaller-items.md

An Amazon fulfillment center receives a large number of orders each day. Each order is associated with a range of prices of items that need to be picked from the warehouse and packed into a box. There

  uv run python amazon/amazon-get-smaller-items/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-get-smaller-items/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getSmallerItems(self, items, start, end, query):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getSmallerItems above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getSmallerItems(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
