"""First Missing Positive — https://www.fastprep.io/problems/amazon-first-missing-positive

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-first-missing-positive.md

Given an unsorted integer array nums, return the smallest positive integer that does not appear in the array.

  uv run python amazon_oa/amazon-first-missing-positive/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-first-missing-positive/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def firstMissingPositive(self, nums):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in firstMissingPositive above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().firstMissingPositive(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
