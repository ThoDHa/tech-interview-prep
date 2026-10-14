"""Number Of Well Performing Groups — https://www.fastprep.io/problems/amazon-number-of-well-performing-groups

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-number-of-well-performing-groups.md

Amazon aims to review its network of m servers deployed across different regions globally. The workloads on these servers are stored in the array workloads. A collection of servers is labeled as perfo

  uv run python amazon_oa/amazon-number-of-well-performing-groups/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-number-of-well-performing-groups/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def numberOfWellPerformingGroups(self, load, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in numberOfWellPerformingGroups above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().numberOfWellPerformingGroups(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
