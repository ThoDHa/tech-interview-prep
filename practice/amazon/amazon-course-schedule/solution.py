"""Course Schedule — https://www.fastprep.io/problems/amazon-course-schedule

Write-up & approaches: ../../../docs/amazon/amazon-course-schedule.md

There are numCourses courses labeled from 0 to numCourses - 1. Each pair [course, prerequisite] means the prerequisite must be completed before the course.

  uv run python amazon/amazon-course-schedule/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-course-schedule/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, numCourses, prerequisites):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().solve(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
