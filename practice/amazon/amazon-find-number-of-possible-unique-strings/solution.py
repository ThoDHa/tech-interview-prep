"""Num of Possible Unique Strings — https://www.fastprep.io/problems/amazon-find-number-of-possible-unique-strings

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-number-of-possible-unique-strings.md

Given a string of lowercase characters, pick substring of any length in it and reverse them. Find the number of possible unique strings.

  uv run python amazon_oa/amazon-find-number-of-possible-unique-strings/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-number-of-possible-unique-strings/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findNumberOfPossibleUniqueStrings(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findNumberOfPossibleUniqueStrings above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findNumberOfPossibleUniqueStrings(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
