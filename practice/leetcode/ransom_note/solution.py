"""Ransom Note: https://leetcode.com/problems/ransom-note/

Write-up & approaches: ../../docs/problems/ransom_note.md

Given two strings `ransomNote` and `magazine`, return `True` if `ransomNote`
can be constructed using the letters of `magazine` (each letter used once).

  uv run python ransom_note/solution.py   # debug one case (see CASE below)
  uv run pytest ransom_note/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in canConstruct above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().canConstruct(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
