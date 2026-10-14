"""Split Prefix Suffix — https://www.fastprep.io/problems/amazon-split-prefix-suffix

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-split-prefix-suffix.md

Amazon Prime Day is a day where many items are put on sale for Amazon Prime members. A list of sale items is assembled where each item is assigned a category denoted by a lowercase English letter.

  uv run python amazon_oa/amazon-split-prefix-suffix/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-split-prefix-suffix/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def splitPrefixSuffix(self, categories, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in splitPrefixSuffix above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().splitPrefixSuffix(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
