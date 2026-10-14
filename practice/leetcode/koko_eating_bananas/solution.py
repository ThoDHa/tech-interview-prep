"""Koko Eating Bananas — https://leetcode.com/problems/koko-eating-bananas/

Write-up & approaches: ../../docs/problems/koko_eating_bananas.md

You are given an integer array `piles` where `piles[i]` is the number of bananas in the `ith` pile. You are also given an integer `h`, which represents the number of hours you have to eat all the bana

  uv run python koko_eating_bananas/solution.py   # debug one case (see CASE below)
  uv run pytest koko_eating_bananas/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minEatingSpeed(self, piles, h):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minEatingSpeed above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minEatingSpeed(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
