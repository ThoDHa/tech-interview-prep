"""Get Min Subsegments — https://www.fastprep.io/problems/amazon-get-min-subsegments

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-min-subsegments.md

Amazon Prime Video is developing a new feature called "Segmentify." This feature applies to a video with n (even) visual frames, where each frame is represented by a binary character in the array fram

  uv run python amazon_oa/amazon-get-min-subsegments/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-min-subsegments/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getminSubsegments(self, frames):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getminSubsegments above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getminSubsegments(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
