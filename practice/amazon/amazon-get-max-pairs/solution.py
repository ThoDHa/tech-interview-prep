"""Get Max Pairs — https://www.fastprep.io/problems/amazon-get-max-pairs

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-max-pairs.md

An AWS client wants to deploy multiple applications and needs two servers, one for their frontend and another for their backend. They have a list of integers representing the quality of servers in ter

  uv run python amazon_oa/amazon-get-max-pairs/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-max-pairs/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMaxPairs(self, frontend, backend):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMaxPairs above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMaxPairs(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
