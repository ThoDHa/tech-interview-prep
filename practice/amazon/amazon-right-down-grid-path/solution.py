"""Path Through an O/X Grid Using Only Right and Down — https://www.fastprep.io/problems/amazon-right-down-grid-path

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-right-down-grid-path.md

Given a rectangular array of strings grid, a zero-based coordinate source = [row, col], and a zero-based coordinate destination = [row, col], return whether the destination is reachable.

  uv run python amazon_oa/amazon-right-down-grid-path/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-right-down-grid-path/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def hasRightDownPath(self, grid, source, destination):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in hasRightDownPath above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().hasRightDownPath(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
