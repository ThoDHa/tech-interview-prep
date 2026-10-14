"""Last Stone Weight — https://leetcode.com/problems/last-stone-weight/

Write-up & approaches: ../../docs/problems/last_stone_weight.md

You are given an array of integers `stones` where `stones[i]` represents the weight of the `ith` stone. We want to run a simulation on the stones as follows: * At each step we choose the **two heavies

  uv run python last_stone_weight/solution.py   # debug one case (see CASE below)
  uv run pytest last_stone_weight/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def lastStoneWeight(self, stones):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in lastStoneWeight above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().lastStoneWeight(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
