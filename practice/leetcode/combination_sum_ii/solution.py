"""Combination Sum II — https://leetcode.com/problems/combination-sum-ii/

Write-up & approaches: ../../docs/problems/combination_sum_ii.md

You are given an array of integers `candidates`, which may contain duplicates, and a target integer `target`. Your task is to return a list of all **unique combinations** of `candidates` where the cho

  uv run python combination_sum_ii/solution.py   # debug one case (see CASE below)
  uv run pytest combination_sum_ii/              # run the test sets
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
