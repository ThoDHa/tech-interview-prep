"""Predict Answer — https://www.fastprep.io/problems/amazon-predict-answer

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-predict-answer.md

In this stock price prediction game, Player 1 provides Player 2 with stock market data for n consecutive days, representing the stock prices on each day, represented by stockData[].

  uv run python amazon_oa/amazon-predict-answer/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-predict-answer/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def predictAnswer(self, stockData, queries):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in predictAnswer above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().predictAnswer(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
