"""LFU Cache — https://www.fastprep.io/problems/amazon-lfu-cache

Write-up & approaches: ../../../docs/amazon/amazon-lfu-cache.md

Process commands on an initially empty least-frequently-used cache with positive integer capacity.

  uv run python amazon/amazon-lfu-cache/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-lfu-cache/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def processLfuCache(self, capacity, operations):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in processLfuCache above, then run this file.
    CASE = None
    if CASE is None:
        print("no cases authored yet; add cases to cases.json or cases_full.json, then set CASE to an id")
    else:
        case = pick_case(__file__, CASE)
        result = Solution().processLfuCache(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
