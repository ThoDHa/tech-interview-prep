"""Maximize Similarity — https://www.fastprep.io/problems/amazon-maximize-similarity

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximize-similarity.md

In the world of Amazon's vast inventory management, you face a challenge of optimizing two inventories, inv1 and inv2, each containing n elements.

  uv run python amazon_oa/amazon-maximize-similarity/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximize-similarity/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximizeSimilarity(self, inv1, inv2):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximizeSimilarity above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximizeSimilarity(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
