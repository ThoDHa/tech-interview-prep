"""Course Schedule II — https://leetcode.com/problems/course-schedule-ii/

Write-up & approaches: ../../docs/problems/course_schedule_ii.md
Reference implementation of the write-up's Kahn's Algorithm solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python course_schedule_ii/reference.py   # debug one case (see CASE below)
  uv run pytest course_schedule_ii/               # run the test sets
"""

from collections import deque
from typing import List


class Solution:
    def findOrder(
        self, numCourses: int, prerequisites: List[List[int]]
    ) -> List[int]:
        """Return a valid course ordering, or [] when a cycle makes one impossible.

        Builds the prerequisite graph (edge `b -> a` for each `[a, b]`
        pair), counts each course's unmet prerequisites, and repeatedly
        takes courses whose count reaches 0; producing fewer than
        `numCourses` courses means a cycle blocked the rest.

        Args:
            numCourses: Number of courses, labeled `0..numCourses - 1`.
            prerequisites: Pairs `[a, b]` meaning course `b` before `a`.

        Returns:
            A topological order of all courses, or an empty list when the
            graph is cyclic.

        Time:  O(V + E): every course and prerequisite pair is processed
            once.
        Space: O(V + E): the adjacency list, the count array, and the queue.
        """
        adjacency = [[] for _ in range(numCourses)]
        pending = [0] * numCourses
        for course, prerequisite in prerequisites:
            adjacency[prerequisite].append(course)
            pending[course] += 1

        queue = deque(
            course for course in range(numCourses) if pending[course] == 0
        )
        order = []
        while queue:
            course = queue.popleft()
            order.append(course)
            for nxt in adjacency[course]:
                pending[nxt] -= 1
                if pending[nxt] == 0:
                    queue.append(nxt)
        return order if len(order) == numCourses else []


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findOrder above, then run this
    # file. cases.json is empty (any-order output), so a literal example
    # stands in.
    num_courses, prerequisites = 3, [[1, 0]]
    result = Solution().findOrder(num_courses, prerequisites)
    print(f"args = numCourses {num_courses}, prerequisites {prerequisites}")
    print(f"got: {result}")
