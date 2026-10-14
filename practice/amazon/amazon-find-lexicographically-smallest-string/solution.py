"""Find Lexicographically Smallest String — https://www.fastprep.io/problems/amazon-find-lexicographically-smallest-string

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-lexicographically-smallest-string.md

Given a lowercase string s, find the lexicographically smallest lowercase string t that has the same length as s, is strictly greater than s, and has no two equal adjacent characters.

  uv run python amazon_oa/amazon-find-lexicographically-smallest-string/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-lexicographically-smallest-string/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findLexicographicallySmallestString(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findLexicographicallySmallestString above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findLexicographicallySmallestString(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
