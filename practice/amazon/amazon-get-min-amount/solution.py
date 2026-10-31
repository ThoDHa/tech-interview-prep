"""Get Minimum Amount — https://www.fastprep.io/problems/amazon-get-min-amount

Write-up & approaches: ../../../docs/amazon/amazon-get-min-amount.md

The manager of the Amazon warehouse has decided to make changes to the inventory. Currently, the inventory has n products, where the quality of the ith product after quality checks is represented by t

  uv run python amazon/amazon-get-min-amount/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-get-min-amount/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMinAmount(self, quality):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMinAmount above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMinAmount(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
