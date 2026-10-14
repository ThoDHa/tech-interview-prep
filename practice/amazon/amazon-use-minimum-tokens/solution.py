"""Use Minimum Tokens — https://www.fastprep.io/problems/amazon-use-minimum-tokens

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-use-minimum-tokens.md

Amazon operates a system of n warehouses, each represented by warehouse[i], where warehouse[i] indicates the maximum number of items that particular warehouse can hold. Additionally, there are q shipm

  uv run python amazon_oa/amazon-use-minimum-tokens/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-use-minimum-tokens/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def useMinimumTokens(self, warehouse, catalog):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in useMinimumTokens above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().useMinimumTokens(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
