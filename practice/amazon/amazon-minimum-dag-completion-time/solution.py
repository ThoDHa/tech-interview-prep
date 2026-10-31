"""Minimum Completion Time for DAG Dependencies — https://www.fastprep.io/problems/amazon-minimum-dag-completion-time

Write-up & approaches: ../../../docs/amazon/amazon-minimum-dag-completion-time.md

Each task has a positive duration. A dependency [before,after] means task after may start only after task before finishes. The dependency graph is acyclic.

  uv run python amazon/amazon-minimum-dag-completion-time/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-minimum-dag-completion-time/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimumCompletionTime(self, durations, dependencies):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumCompletionTime above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimumCompletionTime(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
