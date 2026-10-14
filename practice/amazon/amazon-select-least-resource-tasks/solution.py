"""Select Least Resource Tasks — https://www.fastprep.io/problems/amazon-select-least-resource-tasks

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-select-least-resource-tasks.md

Amazon's Elastic Container Service schedules tasks dynamically. You are given an integer array resourceConsumption, where resourceConsumption[i] is the resource consumption of one task.

  uv run python amazon_oa/amazon-select-least-resource-tasks/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-select-least-resource-tasks/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def selectLeastResourceTasks(self, resourceConsumption):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in selectLeastResourceTasks above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().selectLeastResourceTasks(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
