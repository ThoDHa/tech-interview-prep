"""Minimum Completion Time for DAG Dependencies — https://www.fastprep.io/problems/amazon-minimum-dag-completion-time

Write-up & approaches: ../../../docs/amazon/amazon-minimum-dag-completion-time.md

Reference implementation of the write-up's recommended Topological
Longest-Path Dynamic Programming solution. Your own attempt lives in
solution.py.

  uv run python amazon/amazon-minimum-dag-completion-time/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-minimum-dag-completion-time/              # run the test sets
"""

from collections import deque
from typing import List

from harness import pick_case


class Solution:
    def minimumCompletionTime(self, durations: List[int], dependencies: List[List[int]]) -> int:
        """Return the minimum time to finish every task when any number of
        ready tasks may run in parallel.

        A task starts the instant its last dependency finishes, so its
        finish time is forced: its own duration stacked on the largest
        finish among its predecessors (zero with none). The dependency
        graph is a DAG, so Kahn's topological order visits every task
        only after all predecessors have fixed that stacked value; one
        queue pass propagates each finish into its successors and the
        answer is the largest finish over all tasks, 0 for an empty
        list. Durations reach 1e9 and chains reach 1e5 tasks, so the
        totals reach 1e14 in a plain integer accumulator.

        Args:
            durations: Per-task positive durations, length `n >= 0`.
            dependencies: `[before, after]` pairs; the graph is a DAG.

        Returns:
            The minimum completion time over all tasks.

        Time:  O(n + m): each task is dequeued once and each edge
               relaxes its successor exactly once.
        Space: O(n + m): successor lists, indegrees, finish times,
               and the queue.
        """
        count = len(durations)
        graph = [[] for _ in range(count)]
        indegree = [0] * count
        for before, after in dependencies:
            graph[before].append(after)
            indegree[after] += 1

        finish = [0] * count
        queue = deque(task for task in range(count) if indegree[task] == 0)
        while queue:
            task = queue.popleft()
            finish[task] += durations[task]
            for next_task in graph[task]:
                finish[next_task] = max(finish[next_task], finish[task])
                indegree[next_task] -= 1
                if indegree[next_task] == 0:
                    queue.append(next_task)
        return max(finish, default=0)


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumCompletionTime above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().minimumCompletionTime(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
