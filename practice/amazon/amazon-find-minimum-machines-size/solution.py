"""Find Minimum Machine Sizes — https://www.fastprep.io/problems/amazon-find-minimum-machines-size

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-minimum-machines-size.md

A sequence of n machines is tasked with stocking or retrieving items. You are given the individual stocking/retrieving capacity values of each machine as an integer array, machineCapacity.

  uv run python amazon_oa/amazon-find-minimum-machines-size/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-minimum-machines-size/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findMinimumMachinesSize(self, machineCapacity):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMinimumMachinesSize above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMinimumMachinesSize(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
