"""Course Schedule II — https://leetcode.com/problems/course-schedule-ii/

Write-up & approaches: ../../docs/problems/course_schedule_ii.md

You are given an array `prerequisites` where `prerequisites[i] = [a, b]` indicates that you **must** take course `b` first if you want to take course `a`. * For example, the pair `[0, 1]`, indicates t

  uv run python course_schedule_ii/solution.py   # debug one case (see CASE below)
  uv run pytest course_schedule_ii/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, *args):
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
