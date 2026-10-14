"""Good String — https://www.fastprep.io/problems/amazon-convert-to-good-string

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-convert-to-good-string.md

Given A String Containing Integers, A Good String Is One Not Containing A Subsequence With The Patterns "010" Or "101". You Can Perform Operations To Convert 0 To 1 Or 1 To 0. Return The Number Of Ope

  uv run python amazon_oa/amazon-convert-to-good-string/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-convert-to-good-string/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def convertToGoodString(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in convertToGoodString above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().convertToGoodString(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
