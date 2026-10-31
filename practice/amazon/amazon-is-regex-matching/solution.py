"""Is Regex Matching — https://www.fastprep.io/problems/amazon-is-regex-matching

Write-up & approaches: ../../../docs/amazon/amazon-is-regex-matching.md

The developers at Amazon are developing a regex matching library for their NLP use cases. A prototype regex matching has the following requirements:

  uv run python amazon/amazon-is-regex-matching/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-is-regex-matching/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def isRegexMatching(self, regex, arr):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in isRegexMatching above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().isRegexMatching(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
