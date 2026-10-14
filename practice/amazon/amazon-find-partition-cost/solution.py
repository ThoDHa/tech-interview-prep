"""Get Largest Number — https://www.fastprep.io/problems/amazon-find-partition-cost

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-partition-cost.md

The database specialists at Amazon are engaged in segmenting their sequence of interconnected servers. There exists a consecutive sequence of m servers, labeled from 1 to m, where the expense metric l

  uv run python amazon_oa/amazon-find-partition-cost/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-partition-cost/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getLargestNumber(self, expense, p):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getLargestNumber above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getLargestNumber(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
