"""Add Two Numbers — https://leetcode.com/problems/add-two-numbers/

Write-up & approaches: ../../docs/problems/add_two_numbers.md

You are given two **non-empty** linked lists, `l1` and `l2`, where each represents a non-negative integer. The digits are stored in **reverse order**, e.g. the number 321 is represented as `1 -> 2 -> 

  uv run python add_two_numbers/solution.py   # debug one case (see CASE below)
  uv run pytest add_two_numbers/              # run the test sets
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
