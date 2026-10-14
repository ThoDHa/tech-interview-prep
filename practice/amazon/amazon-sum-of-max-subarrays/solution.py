"""Sum of Max Subarrys — https://www.fastprep.io/problems/amazon-sum-of-max-subarrays

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-sum-of-max-subarrays.md

Find the sum of the maximum of all subarrays multiplied by their length in O(n).

  uv run python amazon_oa/amazon-sum-of-max-subarrays/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-sum-of-max-subarrays/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def sumOfMaxOfSubarrays(self, arr):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in sumOfMaxOfSubarrays above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().sumOfMaxOfSubarrays(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
