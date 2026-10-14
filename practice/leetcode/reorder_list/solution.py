"""Reorder List — https://leetcode.com/problems/reorder-list/

Write-up & approaches: ../../docs/problems/reorder_list.md

You are given the head of a singly linked-list. The positions of a linked list of `length = 7` for example, can intially be represented as: `[0, 1, 2, 3, 4, 5, 6]` Reorder the nodes of the linked list

  uv run python reorder_list/solution.py   # debug one case (see CASE below)
  uv run pytest reorder_list/              # run the test sets
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
