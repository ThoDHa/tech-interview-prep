"""Find Maximum Calories — https://www.fastprep.io/problems/amazon-find-maximum-calories

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-maximum-calories.md

You start on the ground at height 0. There are n stones, and stone i has height height[i].

  uv run python amazon_oa/amazon-find-maximum-calories/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-maximum-calories/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findMaximumCalories(self, height):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMaximumCalories above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMaximumCalories(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
