"""Min Chars to Append — https://www.fastprep.io/problems/amazon-determine-minimum-characters-to-append

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-determine-minimum-characters-to-append.md

You are given two strings, searchWord and resultWord. You may append characters only to the end of searchWord. Return the minimum number of characters that must be appended so that resultWord is a sub

  uv run python amazon_oa/amazon-determine-minimum-characters-to-append/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-determine-minimum-characters-to-append/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minCharactersToAppend(self, searchWord, resultWord):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minCharactersToAppend above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minCharactersToAppend(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
