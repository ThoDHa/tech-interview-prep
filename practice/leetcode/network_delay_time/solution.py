"""Network Delay Time — https://leetcode.com/problems/network-delay-time/

Write-up & approaches: ../../docs/problems/network_delay_time.md

You are given a network of `n` directed nodes, labeled from `1` to `n`. You are also given `times`, a list of directed edges where `times[i] = (ui, vi, ti)`. * `ui` is the source node (an integer from

  uv run python network_delay_time/solution.py   # debug one case (see CASE below)
  uv run pytest network_delay_time/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def networkDelayTime(self, times, n, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in networkDelayTime above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().networkDelayTime(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
