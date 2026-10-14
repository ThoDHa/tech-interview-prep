"""Select K Paired Indices for Maximum Score — https://www.fastprep.io/problems/amazon-select-k-paired-array-score

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-select-k-paired-array-score.md

Select exactly k shared indices from two equal-length arrays. The score is the sum of selected values from first multiplied by the minimum selected value from second.

  uv run python amazon_oa/amazon-select-k-paired-array-score/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-select-k-paired-array-score/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximumPairedScore(self, first, second, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximumPairedScore above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximumPairedScore(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
