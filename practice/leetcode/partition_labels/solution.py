"""Partition Labels — https://leetcode.com/problems/partition-labels/

Write-up & approaches: ../../docs/problems/partition_labels.md

You are given a string `s` consisting of lowercase english letters. We want to split the string into as many substrings as possible, while ensuring that each letter appears in at most one substring. R

  uv run python partition_labels/solution.py   # debug one case (see CASE below)
  uv run pytest partition_labels/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def partitionLabels(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in partitionLabels above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().partitionLabels(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
