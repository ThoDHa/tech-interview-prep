"""Process Queries On Cart — https://www.fastprep.io/problems/amazon-process-queries-on-cart

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-process-queries-on-cart.md

As an aspiring developer at Amazon, you are building a prototype for a cart management service.

  uv run python amazon_oa/amazon-process-queries-on-cart/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-process-queries-on-cart/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def processQueriesOnCart(self, items, query):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in processQueriesOnCart above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().processQueriesOnCart(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
