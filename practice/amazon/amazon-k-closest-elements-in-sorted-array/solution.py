"""K Closest Elements in a Sorted Array — https://www.fastprep.io/problems/amazon-k-closest-elements-in-sorted-array

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-k-closest-elements-in-sorted-array.md

Given an integer array arr sorted in nondecreasing order, an integer k, and a target x, return the k values closest to x in ascending order.

  uv run python amazon_oa/amazon-k-closest-elements-in-sorted-array/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-k-closest-elements-in-sorted-array/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findClosestElements(self, arr, k, x):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findClosestElements above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findClosestElements(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
