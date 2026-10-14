"""Valid Palindrome: https://leetcode.com/problems/valid-palindrome/

Write-up & approaches: ../../docs/problems/valid_palindrome.md

Given a string `s`, return `true` if it is a palindrome after lowercasing every
letter and dropping every non-alphanumeric character, or `false` otherwise.

  uv run python valid_palindrome/solution.py     # debug one case (see CASE below)
  uv run pytest valid_palindrome/                # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def isPalindrome(self, s: str) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in isPalindrome above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().isPalindrome(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
