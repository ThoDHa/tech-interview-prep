"""Remove Duplicate Letters for the Largest Result — https://www.fastprep.io/problems/amazon-largest-lexicographic-unique-letters

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-largest-lexicographic-unique-letters.md

Given a lowercase string s, remove characters so that every distinct letter appears exactly once. The remaining characters must preserve their original relative order.

  uv run python amazon_oa/amazon-largest-lexicographic-unique-letters/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-largest-lexicographic-unique-letters/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def largestUniqueLetters(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in largestUniqueLetters above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().largestUniqueLetters(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
