"""Count Picked Items Less Than Queries — https://www.fastprep.io/problems/amazon-count-picked-items-less-than-queries

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-count-picked-items-less-than-queries.md

A warehouse has items represented by an array items, where items[i] is the value of the i-th item.

  uv run python amazon_oa/amazon-count-picked-items-less-than-queries/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-count-picked-items-less-than-queries/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countPickedItemsLessThan(self, items, startIndex, endIndex, query):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countPickedItemsLessThan above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countPickedItemsLessThan(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
