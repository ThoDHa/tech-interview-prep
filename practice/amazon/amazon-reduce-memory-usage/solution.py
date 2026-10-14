"""Reduce Memory Usage — https://www.fastprep.io/problems/amazon-reduce-memory-usage

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-reduce-memory-usage.md

You are working on an Amazon Data Center where you are required to reduce the amount of main memory consumption by the processes.

  uv run python amazon_oa/amazon-reduce-memory-usage/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-reduce-memory-usage/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def reduceMemoryUsage(self, processes, m):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in reduceMemoryUsage above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().reduceMemoryUsage(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
