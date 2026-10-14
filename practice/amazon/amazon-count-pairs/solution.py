"""Count Pairs — https://www.fastprep.io/problems/amazon-count-pairs

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-count-pairs.md

You are given an integer array numbers and a nonnegative integer k. Count the number of distinct value pairs (a, b) for which both values occur in numbers and a + k = b.

  uv run python amazon_oa/amazon-count-pairs/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-count-pairs/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countPairs(self, numbers, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countPairs above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countPairs(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
