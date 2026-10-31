"""Are Two People Relatives in a Family Tree? — https://www.fastprep.io/problems/amazon-family-tree-relatives

Write-up & approaches: ../../../docs/amazon/amazon-family-tree-relatives.md

A family tree is given as a list of rows. Each row relations[i] = [parent, child] means that parent is a parent of child. A person can have up to two recorded parents, and some people have no recorded

  uv run python amazon/amazon-family-tree-relatives/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-family-tree-relatives/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, relations, first, second):
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
