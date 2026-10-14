"""Alien Dictionary — https://leetcode.com/problems/alien-dictionary/

Write-up & approaches: ../../docs/problems/alien_dictionary.md

There is a new alien language that uses the English alphabet, but the order of the letters is unknown. You are given a list of strings `words` from the alien language's dictionary. It is claimed that 

  uv run python alien_dictionary/solution.py   # debug one case (see CASE below)
  uv run pytest alien_dictionary/              # run the test sets
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
