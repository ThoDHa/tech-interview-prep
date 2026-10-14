"""Dynamic Kth Largest Queries — https://www.fastprep.io/problems/amazon-dynamic-kth-largest-queries

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-dynamic-kth-largest-queries.md

You are given an initial list of integer values and a stream of operations. The list changes over time as values are inserted.

  uv run python amazon_oa/amazon-dynamic-kth-largest-queries/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-dynamic-kth-largest-queries/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def dynamicKthLargestQueries(self, initialValues, operations, values):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in dynamicKthLargestQueries above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().dynamicKthLargestQueries(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
