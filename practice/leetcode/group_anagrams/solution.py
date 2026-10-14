"""Group Anagrams — https://leetcode.com/problems/group-anagrams/

Write-up & approaches: ../../docs/problems/group_anagrams.md

Given an array of strings `strs`, group all *anagrams* together into sublists. You may return the output in **any order**. An **anagram** is a string that contains the exact same characters as another

  uv run python group_anagrams/solution.py   # debug one case (see CASE below)
  uv run pytest group_anagrams/              # run the test sets
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
