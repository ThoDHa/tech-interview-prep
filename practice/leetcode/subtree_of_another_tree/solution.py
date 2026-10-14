"""Subtree of Another Tree — https://leetcode.com/problems/subtree-of-another-tree/

Write-up & approaches: ../../docs/problems/subtree_of_another_tree.md

Given the roots of two binary trees `root` and `subRoot`, return `true` if there is a subtree of `root` with the same structure and node values of `subRoot` and `false` otherwise. A subtree of a binar

  uv run python subtree_of_another_tree/solution.py   # debug one case (see CASE below)
  uv run pytest subtree_of_another_tree/              # run the test sets
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
