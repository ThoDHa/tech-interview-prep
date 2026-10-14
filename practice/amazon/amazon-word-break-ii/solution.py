"""Word Break II — https://www.fastprep.io/problems/amazon-word-break-ii

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-word-break-ii.md

Given a string s and an array of unique dictionary words wordDict, insert spaces into s so that every resulting token is a dictionary word.

  uv run python amazon_oa/amazon-word-break-ii/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-word-break-ii/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def wordBreak(self, s, wordDict):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in wordBreak above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().wordBreak(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
