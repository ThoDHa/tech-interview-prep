"""Location of Data After Transfers — https://www.fastprep.io/problems/location-of-data-after-transfers

Write-up & approaches: ../../../docs/problems/amazon_oa/location-of-data-after-transfers.md

X stores its data on different servers at different locations. From time to time, due to several factors, X needs to move its data from one location to another. This challenge involved keeping track o

  uv run python amazon_oa/location-of-data-after-transfers/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/location-of-data-after-transfers/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def locationOfDataAfterTransfers(self, locations, movedFrom, movedTo):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in locationOfDataAfterTransfers above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().locationOfDataAfterTransfers(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
