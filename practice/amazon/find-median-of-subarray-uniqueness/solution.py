"""Find Median Of Subarray Uniqueness — https://www.fastprep.io/problems/find-median-of-subarray-uniqueness

Write-up & approaches: ../../../docs/problems/amazon_oa/find-median-of-subarray-uniqueness.md

In an Amazon coding marathon, the following challenge was given.

  uv run python amazon_oa/find-median-of-subarray-uniqueness/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/find-median-of-subarray-uniqueness/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findMedianOfSubarrayUniqueness(self, arr):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMedianOfSubarrayUniqueness above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMedianOfSubarrayUniqueness(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
