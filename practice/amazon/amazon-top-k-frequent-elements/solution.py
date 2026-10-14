"""Top K Frequent Elements — https://www.fastprep.io/problems/amazon-top-k-frequent-elements

Write-up & approaches: ../../../docs/amazon/amazon-top-k-frequent-elements.md

Given a nonempty integer array nums and an integer k, return the k distinct values that occur most frequently.

  uv run python amazon_oa/amazon-top-k-frequent-elements/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-top-k-frequent-elements/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, nums, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().solve(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
