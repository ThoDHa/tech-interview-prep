"""Valid Anagram: https://leetcode.com/problems/valid-anagram/

Write-up & approaches: ../../docs/problems/valid_anagram.md

Given two strings `s` and `t`, return True if `t` is an anagram of `s`.

  uv run python valid_anagram/solution.py   # debug one case (see CASE below)
  uv run pytest valid_anagram/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in isAnagram above, then run this file.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().isAnagram(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
