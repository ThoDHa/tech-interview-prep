"""Course Schedule II — https://www.fastprep.io/problems/amazon-course-schedule-ii

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-course-schedule-ii.md

There are numCourses courses labeled from 0 to numCourses - 1. Each pair [course, prerequisite] means the prerequisite must be completed before the course.

  uv run python amazon_oa/amazon-course-schedule-ii/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-course-schedule-ii/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findCourseOrder(self, numCourses, prerequisites):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findCourseOrder above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findCourseOrder(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
