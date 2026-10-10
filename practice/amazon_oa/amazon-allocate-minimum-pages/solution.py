"""Allocate Minimum Pages — https://www.fastprep.io/problems/amazon-allocate-minimum-pages

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-allocate-minimum-pages.md

You are given an array pages, where pages[i] is the number of pages in the i-th book, and an integer students.

  uv run python amazon_oa/amazon-allocate-minimum-pages/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-allocate-minimum-pages/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def allocateMinimumPages(self, pages, students):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in allocateMinimumPages above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().allocateMinimumPages(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
