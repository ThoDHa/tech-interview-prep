"""Find K Level Permutation — https://www.fastprep.io/problems/amazon-find-k-level-permutation

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-k-level-permutation.md

You have an array from 1 to N now you have to find a K-level permutation such that for N-K+1 segments or windows you get the difference between sum of maximum segment sum and minimum segment must be a

  uv run python amazon_oa/amazon-find-k-level-permutation/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-k-level-permutation/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findKLevelPermutation(self, N, K):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findKLevelPermutation above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findKLevelPermutation(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
