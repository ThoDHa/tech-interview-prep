"""Maximum Score With Non-Adjacent Values — https://www.fastprep.io/problems/amazon-maximum-score-with-non-adjacent-values

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximum-score-with-non-adjacent-values.md

You are given a list of integers nums. You may choose any set of values from the list.

  uv run python amazon_oa/amazon-maximum-score-with-non-adjacent-values/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximum-score-with-non-adjacent-values/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximumNonAdjacentValueScore(self, nums):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximumNonAdjacentValueScore above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximumNonAdjacentValueScore(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
