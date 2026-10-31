"""Tallest Billboard — https://www.fastprep.io/problems/amazon-tallest-billboard

Write-up & approaches: ../../../docs/amazon/amazon-tallest-billboard.md

Partition any subset of rods into two groups with equal sums. Return the greatest possible common sum. A rod may be unused.

  uv run python amazon/amazon-tallest-billboard/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-tallest-billboard/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def tallestBillboard(self, rods):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in tallestBillboard above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().tallestBillboard(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
