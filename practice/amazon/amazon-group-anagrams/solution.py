"""Group Anagrams — https://www.fastprep.io/problems/amazon-group-anagrams

Write-up & approaches: ../../../docs/amazon/amazon-group-anagrams.md

Group the strings in strs so that two strings appear in the same group exactly when they are anagrams.

  uv run python amazon/amazon-group-anagrams/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-group-anagrams/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def groupAnagrams(self, strs):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in groupAnagrams above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().groupAnagrams(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
