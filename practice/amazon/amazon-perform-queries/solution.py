"""Perform Queries — https://www.fastprep.io/problems/amazon-perform-queries

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-perform-queries.md

Amazon ships millions of packages every day. A large percentage of them are fulfilled by Amazon, so it is important to minimize shipping costs. It has been found that moving a group of 3 packages to t

  uv run python amazon_oa/amazon-perform-queries/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-perform-queries/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def performQueries(self, queries):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in performQueries above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().performQueries(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
