"""All Anagram Start Indices — https://www.fastprep.io/problems/amazon-anagram-start-indices

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-anagram-start-indices.md

Given lowercase strings s and p, return every starting index where a substring of s is an anagram of p.

  uv run python amazon_oa/amazon-anagram-start-indices/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-anagram-start-indices/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findAnagrams(self, s, p):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findAnagrams above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findAnagrams(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
