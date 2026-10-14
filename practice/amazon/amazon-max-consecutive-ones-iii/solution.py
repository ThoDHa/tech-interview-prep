"""Max Consecutive Ones III — https://www.fastprep.io/problems/amazon-max-consecutive-ones-iii

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-max-consecutive-ones-iii.md

Given a binary array nums and an integer k, return the maximum number of consecutive ones obtainable by flipping at most k zeros to ones.

  uv run python amazon_oa/amazon-max-consecutive-ones-iii/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-max-consecutive-ones-iii/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def longestOnes(self, nums, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in longestOnes above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().longestOnes(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
