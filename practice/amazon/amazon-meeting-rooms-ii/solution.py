"""Meeting Rooms II — https://www.fastprep.io/problems/amazon-meeting-rooms-ii

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-meeting-rooms-ii.md

Given an array of meeting time intervals intervals, where intervals[i] = [start_i, end_i], return the minimum number of conference rooms required.

  uv run python amazon_oa/amazon-meeting-rooms-ii/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-meeting-rooms-ii/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minMeetingRooms(self, intervals):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minMeetingRooms above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minMeetingRooms(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
