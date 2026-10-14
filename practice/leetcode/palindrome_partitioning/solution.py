"""Palindrome Partitioning — https://leetcode.com/problems/palindrome-partitioning/

Write-up & approaches: ../../docs/problems/palindrome_partitioning.md

Given a string `s`, split `s` into substrings where every substring is a palindrome. Return all possible lists of palindromic substrings. You may return the solution in **any order**.

  uv run python palindrome_partitioning/solution.py   # debug one case (see CASE below)
  uv run pytest palindrome_partitioning/              # run the test sets
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
