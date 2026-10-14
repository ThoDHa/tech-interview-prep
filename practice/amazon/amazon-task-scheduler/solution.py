"""Task Scheduler — https://www.fastprep.io/problems/amazon-task-scheduler

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-task-scheduler.md

Special thanks: ( ˶ˆᗜˆ˵ ) Many Manyy Manyyy thanks to spike!ᯓᡣ𐭩

  uv run python amazon_oa/amazon-task-scheduler/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-task-scheduler/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def leastInterval(self, tasks, n):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in leastInterval above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().leastInterval(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
