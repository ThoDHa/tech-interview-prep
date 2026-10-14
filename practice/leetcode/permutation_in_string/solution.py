"""Permutation In String — https://leetcode.com/problems/permutation-in-string/

Write-up & approaches: ../../docs/problems/permutation_in_string.md

You are given two strings `s1` and `s2`. Return `true` if `s2` contains a permutation of `s1`, or `false` otherwise. That means if a permutation of `s1` exists as a substring of `s2`, then return `tru

  uv run python permutation_in_string/solution.py   # debug one case (see CASE below)
  uv run pytest permutation_in_string/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def checkInclusion(self, s1, s2):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in checkInclusion above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().checkInclusion(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
