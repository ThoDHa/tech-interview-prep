"""Ways to Group Parcels — https://www.fastprep.io/problems/amazon-find-number-of-ways-to-group-parcels

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-number-of-ways-to-group-parcels.md

In one of the warehouses of Amazon, a pan balance is used to weigh and load the parcels for delivery.

  uv run python amazon_oa/amazon-find-number-of-ways-to-group-parcels/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-number-of-ways-to-group-parcels/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def numberOfWaysToGroupParcels(self, weight, wt):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in numberOfWaysToGroupParcels above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().numberOfWaysToGroupParcels(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
