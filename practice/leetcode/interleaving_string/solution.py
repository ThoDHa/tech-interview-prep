"""Interleaving String — https://leetcode.com/problems/interleaving-string/

Write-up & approaches: ../../docs/problems/interleaving_string.md

You are given three strings `s1`, `s2`, and `s3`. Return `true` if `s3` is formed by **interleaving** `s1` and `s2` together or `false` otherwise. **Interleaving** two strings `s` and `t` is done by d

  uv run python interleaving_string/solution.py   # debug one case (see CASE below)
  uv run pytest interleaving_string/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def isInterleave(self, s1, s2, s3):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in isInterleave above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().isInterleave(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
