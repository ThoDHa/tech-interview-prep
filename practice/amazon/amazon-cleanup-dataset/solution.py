"""Cleanup Dataset — https://www.fastprep.io/problems/amazon-cleanup-dataset

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-cleanup-dataset.md

Data Scientists at Amazon are working on cleansing a machine learning dataset. The dataset is represented as a string dataset consisting of an even number of lowercase English letters. The goal is to 

  uv run python amazon_oa/amazon-cleanup-dataset/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-cleanup-dataset/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def cleanupDataset(self, dataset, x, y):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in cleanupDataset above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().cleanupDataset(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
