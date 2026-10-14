"""Find Min Max Difference — https://www.fastprep.io/problems/amazon-find-min-max-difference

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-min-max-difference.md

Given one unsorted array of size n and integer k.

  uv run python amazon_oa/amazon-find-min-max-difference/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-min-max-difference/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findMinMaxDifference(self, arr, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMinMaxDifference above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMinMaxDifference(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
