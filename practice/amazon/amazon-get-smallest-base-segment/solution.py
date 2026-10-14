"""Get Smallest Base Segment — https://www.fastprep.io/problems/amazon-get-smallest-base-segment

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-smallest-base-segment.md

In Amazon's distributed storage network, some critical data segments are missing. They are represented by a string missingData. The system restores data by choosing a base segment of length segmentSiz

  uv run python amazon_oa/amazon-get-smallest-base-segment/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-smallest-base-segment/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getSmallestBaseSegment(self, segmentSize, missingData):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getSmallestBaseSegment above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getSmallestBaseSegment(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
