"""Minimize Effort — https://www.fastprep.io/problems/amazon-minimize-effort

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimize-effort.md

Source note: 2026-07-17 — The EffiBin era is over. Long live Minimum Total Batch Expense. The problem has returned to the Circle of Source Fidelity, with its terminology, function signature, example, 

  uv run python amazon_oa/amazon-minimize-effort/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimize-effort/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def determineMinimalExpense(self, expense):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in determineMinimalExpense above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().determineMinimalExpense(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
