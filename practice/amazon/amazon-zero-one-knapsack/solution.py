"""0/1 Knapsack — https://www.fastprep.io/problems/amazon-zero-one-knapsack

Write-up & approaches: ../../../docs/amazon/amazon-zero-one-knapsack.md

You are given two arrays, weights and values, describing n items. Item i has weight weights[i] and value values[i].

  uv run python amazon/amazon-zero-one-knapsack/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-zero-one-knapsack/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximumKnapsackValue(self, weights, values, capacity):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximumKnapsackValue above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximumKnapsackValue(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
