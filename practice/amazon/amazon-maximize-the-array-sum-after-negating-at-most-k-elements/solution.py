"""Max Negation — https://www.fastprep.io/problems/amazon-maximize-the-array-sum-after-negating-at-most-k-elements

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximize-the-array-sum-after-negating-at-most-k-elements.md

Given an array A with only positive numbers. We are allowed to negate any entries in the array, 

  uv run python amazon_oa/amazon-maximize-the-array-sum-after-negating-at-most-k-elements/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximize-the-array-sum-after-negating-at-most-k-elements/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maxNegations(self, A):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxNegations above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxNegations(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
