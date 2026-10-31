"""Find K Pairs with Smallest Sums — https://www.fastprep.io/problems/amazon-k-smallest-pair-sums

Write-up & approaches: ../../../docs/amazon/amazon-k-smallest-pair-sums.md

Given two integer arrays nums1 and nums2, both sorted in nondecreasing order, consider every index pair (i, j) and the pair [nums1[i], nums2[j]].

  uv run python amazon/amazon-k-smallest-pair-sums/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-k-smallest-pair-sums/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def kSmallestPairs(self, nums1, nums2, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in kSmallestPairs above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().kSmallestPairs(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
