"""Assign Tasks — https://www.fastprep.io/problems/amazon-assign-tasks

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-assign-tasks.md

You have an integer servers, which denote the number of servers, and you have a list called requests which denote the servers that this request is allowed to be scheduled to. You have to schedule each

  uv run python amazon_oa/amazon-assign-tasks/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-assign-tasks/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def assignTasks(self, servers, requests):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in assignTasks above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().assignTasks(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
