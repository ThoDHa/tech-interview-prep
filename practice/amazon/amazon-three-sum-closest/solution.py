"""Three Sum Closest — https://www.fastprep.io/problems/amazon-three-sum-closest

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-three-sum-closest.md

Given an integer array nums and an integer target, choose three distinct indices and return the sum of their values that is closest to target.

  uv run python amazon_oa/amazon-three-sum-closest/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-three-sum-closest/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def threeSumClosest(self, nums, target):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in threeSumClosest above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().threeSumClosest(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
