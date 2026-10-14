"""Course Schedule: https://leetcode.com/problems/course-schedule/

Write-up & approaches: ../../docs/problems/course_schedule.md

There are `numCourses` courses labeled `0` to `numCourses - 1`. Each pair
`prerequisites[i] = [a, b]` means course `b` must be taken before course `a`.
Return `True` if you can finish every course, otherwise `False`.

  uv run python course_schedule/solution.py     # debug one case (see CASE below)
  uv run pytest course_schedule/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in canFinish above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().canFinish(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
