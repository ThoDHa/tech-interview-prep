"""Find All Anagrams in a String: https://leetcode.com/problems/find-all-anagrams-in-a-string/

Write-up & approaches: ../../docs/problems/find_all_anagrams_in_a_string.md

Given two strings `s` and `p`, return an array of all the start indices of `p`'s
anagrams in `s`. You may return the answer in any order.

  uv run python find_all_anagrams_in_a_string/solution.py     # debug one case (see CASE below)
  uv run pytest find_all_anagrams_in_a_string/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findAnagrams above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findAnagrams(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
