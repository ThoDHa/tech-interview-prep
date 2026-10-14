"""Max Sum of Non-overlapping Intervals — https://www.fastprep.io/problems/amazon-max-sum-of-non-overlapping-intervals

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-max-sum-of-non-overlapping-intervals.md

AMZ Interval Collection (A group of problems focused on operations involving intervals :) - 

  uv run python amazon_oa/amazon-max-sum-of-non-overlapping-intervals/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-max-sum-of-non-overlapping-intervals/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maxSumNonOverlappingIntervals(self, starts, durations, costs):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxSumNonOverlappingIntervals above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxSumNonOverlappingIntervals(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
