"""Dynamic Prefix Search Collection — https://www.fastprep.io/problems/amazon-prefix-search-collection

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-prefix-search-collection.md

Implement a dynamic collection of lowercase words. Process the finite array operations from left to right.

  uv run python amazon_oa/amazon-prefix-search-collection/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-prefix-search-collection/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def processPrefixSearch(self, operations):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in processPrefixSearch above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().processPrefixSearch(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
