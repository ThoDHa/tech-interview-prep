"""Edit Distance — https://leetcode.com/problems/edit-distance/

Write-up & approaches: ../../docs/problems/edit_distance.md

You are given two strings `word1` and `word2`, each consisting of lowercase English letters. You are allowed to perform three operations on `word1` an unlimited number of times: * Insert a character a

  uv run python edit_distance/solution.py   # debug one case (see CASE below)
  uv run pytest edit_distance/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minDistance(self, word1, word2):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minDistance above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minDistance(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
