"""Unique String Permutations — https://www.fastprep.io/problems/amazon-unique-string-permutations

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-unique-string-permutations.md

Given a lowercase string s, return every distinct permutation of its characters exactly once.

  uv run python amazon_oa/amazon-unique-string-permutations/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-unique-string-permutations/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def uniquePermutations(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in uniquePermutations above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().uniquePermutations(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
