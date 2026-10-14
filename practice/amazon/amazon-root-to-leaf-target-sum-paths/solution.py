"""Root-to-Leaf Paths with a Target Sum — https://www.fastprep.io/problems/amazon-root-to-leaf-target-sum-paths

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-root-to-leaf-target-sum-paths.md

Given the root of a binary tree and an integer targetSum, return every root-to-leaf path whose node values add up to targetSum.

  uv run python amazon_oa/amazon-root-to-leaf-target-sum-paths/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-root-to-leaf-target-sum-paths/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def pathSum(self, root, targetSum):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in pathSum above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().pathSum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
