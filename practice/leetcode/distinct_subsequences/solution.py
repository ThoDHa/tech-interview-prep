"""Distinct Subsequences — https://leetcode.com/problems/distinct-subsequences/

Write-up & approaches: ../../docs/problems/distinct_subsequences.md

You are given two strings `s` and `t`, both consisting of english letters. Return the number of distinct **subsequences** of `s` which are equal to `t`.

  uv run python distinct_subsequences/solution.py   # debug one case (see CASE below)
  uv run pytest distinct_subsequences/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def numDistinct(self, s, t):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in numDistinct above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().numDistinct(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
