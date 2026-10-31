"""Course Order and Cycle — https://www.fastprep.io/problems/amazon-course-order-and-cycle

Write-up & approaches: ../../../docs/amazon/amazon-course-order-and-cycle.md

Source note: Reports describe prerequisite execution order, cycle identification, and a changed-task rerun follow-up. Canonical sorted traversal, filtered full ordering, global cycle scope, and runner

  uv run python amazon/amazon-course-order-and-cycle/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-course-order-and-cycle/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def analyzeCourses(self, numCourses, prerequisites, changedCourses):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in analyzeCourses above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().analyzeCourses(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
