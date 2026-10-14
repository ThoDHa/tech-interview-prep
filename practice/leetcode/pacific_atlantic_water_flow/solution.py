"""Pacific Atlantic Water Flow — https://leetcode.com/problems/pacific-atlantic-water-flow/

Write-up & approaches: ../../docs/problems/pacific_atlantic_water_flow.md

You are given a rectangular island `heights` where `heights[r][c]` represents the **height above sea level** of the cell at coordinate `(r, c)`. The islands borders the **Pacific Ocean** from the top 

  uv run python pacific_atlantic_water_flow/solution.py   # debug one case (see CASE below)
  uv run pytest pacific_atlantic_water_flow/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, *args):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().solve(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
