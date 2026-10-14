"""Maximum Non-Adjacent House Value — https://www.fastprep.io/problems/amazon-maximum-non-adjacent-house-value

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximum-non-adjacent-house-value.md

You are given an array values where values[i] is the amount available in the ith house arranged in a line.

  uv run python amazon_oa/amazon-maximum-non-adjacent-house-value/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximum-non-adjacent-house-value/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maxNonAdjacentHouseValue(self, values):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxNonAdjacentHouseValue above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxNonAdjacentHouseValue(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
