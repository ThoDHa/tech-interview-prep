"""Count Similar String Groups — https://www.fastprep.io/problems/amazon-count-similar-string-groups

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-count-similar-string-groups.md

You are given an array of strings strs. All strings are anagrams of each other.

  uv run python amazon_oa/amazon-count-similar-string-groups/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-count-similar-string-groups/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countSimilarStringGroups(self, strs):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countSimilarStringGroups above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countSimilarStringGroups(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
