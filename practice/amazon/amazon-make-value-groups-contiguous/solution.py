"""Make Value Groups Contiguous — https://www.fastprep.io/problems/amazon-make-value-groups-contiguous

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-make-value-groups-contiguous.md

You are given an integer array arr. In one operation, choose two values x and y (where y may be any value, including an existing value in the array), and replace every occurrence of x in the array wit

  uv run python amazon_oa/amazon-make-value-groups-contiguous/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-make-value-groups-contiguous/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minOperationsToMakeValuesContiguous(self, arr):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minOperationsToMakeValuesContiguous above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minOperationsToMakeValuesContiguous(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
