"""Task Scheduler: https://leetcode.com/problems/task-scheduler/

Write-up & approaches: ../../docs/problems/task_scheduler.md

Given a list of CPU `tasks` (uppercase letters) and a cooldown `n`, return the
least number of time units needed so that any two identical tasks are separated
by at least `n` units, idling when no task is available.

  uv run python task_scheduler/solution.py   # debug one case (see CASE below)
  uv run pytest task_scheduler/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in leastInterval above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().leastInterval(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
