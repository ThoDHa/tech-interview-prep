"""Maximum Sum of Heights — https://www.fastprep.io/problems/amazon-maximum-sum-of-heights

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximum-sum-of-heights.md

Given positive maximum heights maxHeights, choose a positive height for every index so that height[i] <= maxHeights[i]. The resulting array must be mountain-shaped: for some peak index, heights do not

  uv run python amazon_oa/amazon-maximum-sum-of-heights/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximum-sum-of-heights/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximumSumOfHeights(self, maxHeights):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximumSumOfHeights above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximumSumOfHeights(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
