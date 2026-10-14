"""Subsets II — https://leetcode.com/problems/subsets-ii/

Write-up & approaches: ../../docs/problems/subsets_ii.md

You are given an array `nums` of integers, which may contain duplicates. Return all possible subsets. The solution must **not** contain duplicate subsets. You may return the solution in **any order**.

  uv run python subsets_ii/solution.py   # debug one case (see CASE below)
  uv run pytest subsets_ii/              # run the test sets
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
