"""Count the Number of Complete Components — https://www.fastprep.io/problems/amazon-count-complete-components

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-count-complete-components.md

You are given an integer n and an undirected graph whose vertices are numbered from 0 through n - 1. The array edges contains each undirected edge [u, v].

  uv run python amazon_oa/amazon-count-complete-components/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-count-complete-components/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countCompleteComponents(self, n, edges):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countCompleteComponents above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countCompleteComponents(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
