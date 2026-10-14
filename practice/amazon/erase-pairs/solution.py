"""Erase Pairs — https://www.fastprep.io/problems/erase-pairs

Write-up & approaches: ../../../docs/problems/amazon_oa/erase-pairs.md

You are given a string S. In one move you can erase from S a pair of identical letters. Find the shortest possible string that can be created this way. 

  uv run python amazon_oa/erase-pairs/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/erase-pairs/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def erasePairs(self, S):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in erasePairs above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().erasePairs(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
