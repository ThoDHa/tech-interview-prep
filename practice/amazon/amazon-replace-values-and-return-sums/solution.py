"""Replace Values and Return Sums — https://www.fastprep.io/problems/amazon-replace-values-and-return-sums

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-replace-values-and-return-sums.md

You are given an integer array entries and a 2D integer array transactions. Each transaction is a pair [oldValue, newValue].

  uv run python amazon_oa/amazon-replace-values-and-return-sums/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-replace-values-and-return-sums/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def replaceValuesAndReturnSums(self, entries, transactions):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in replaceValuesAndReturnSums above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().replaceValuesAndReturnSums(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
