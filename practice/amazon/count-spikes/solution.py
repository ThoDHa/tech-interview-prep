"""Count Spikes — https://www.fastprep.io/problems/count-spikes

Write-up & approaches: ../../../docs/problems/amazon_oa/count-spikes.md

A k-Spike is an element that satisfies both the following conditions: 

  uv run python amazon_oa/count-spikes/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/count-spikes/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countSpikes(self, prices, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countSpikes above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countSpikes(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
