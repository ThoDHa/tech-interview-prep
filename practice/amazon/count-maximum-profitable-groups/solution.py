"""Count Maximum Profitable Groups — https://www.fastprep.io/problems/count-maximum-profitable-groups

Write-up & approaches: ../../../docs/problems/amazon_oa/count-maximum-profitable-groups.md

Special thanks: 🍓 1000 thanks to spike for spike's incredible help! 🥑

  uv run python amazon_oa/count-maximum-profitable-groups/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/count-maximum-profitable-groups/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countMaximumProfitableGroups(self, stockPrice):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countMaximumProfitableGroups above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countMaximumProfitableGroups(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
