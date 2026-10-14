"""Maximum Saw Height for At Least M Cut Length — https://www.fastprep.io/problems/amazon-woodcut-saw-height

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-woodcut-saw-height.md

You have vertical wooden poles with integer heights heights. Set a saw to a non-negative integer height h; every pole taller than h contributes height - h units of wood, and shorter poles contribute n

  uv run python amazon_oa/amazon-woodcut-saw-height/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-woodcut-saw-height/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maxSawHeight(self, heights, requiredWood):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxSawHeight above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxSawHeight(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
