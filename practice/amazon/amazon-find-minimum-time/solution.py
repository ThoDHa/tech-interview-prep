"""Find Minimum Time — https://www.fastprep.io/problems/amazon-find-minimum-time

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-minimum-time.md

In the context of an Amazon gaming product involving a snake and apples on a number line, the product simulates a set of unique coordinates representing the positions of the apples. The array named po

  uv run python amazon_oa/amazon-find-minimum-time/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-minimum-time/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findMinimumTimeForSnake(self, n, k, position):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMinimumTimeForSnake above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMinimumTimeForSnake(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
