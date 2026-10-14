"""Maximize Pages Before Suspension — https://www.fastprep.io/problems/amazon-maximize-pages-before-suspension

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximize-pages-before-suspension.md

The engineering team at an Amazon fulfillment center is optimizing n high-performance printers, where each printer i can print pages[i] number of pages.

  uv run python amazon_oa/amazon-maximize-pages-before-suspension/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximize-pages-before-suspension/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMaxPages(self, pages, threshold):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMaxPages above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMaxPages(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
