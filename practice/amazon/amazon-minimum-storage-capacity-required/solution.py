"""Minimize Storage Required — https://www.fastprep.io/problems/amazon-minimum-storage-capacity-required

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimum-storage-capacity-required.md

Need to efficiently distribute a collection of computer games among k different children. Each game is characterized by its size, denoted by gameSize[i] for 1 ≤ i ≤ n.

  uv run python amazon_oa/amazon-minimum-storage-capacity-required/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimum-storage-capacity-required/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findMinimumPenDriveCapacity(self, gameSize, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMinimumPenDriveCapacity above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMinimumPenDriveCapacity(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
