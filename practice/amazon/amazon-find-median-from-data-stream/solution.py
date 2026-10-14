"""Find Median from Data Stream — https://www.fastprep.io/problems/amazon-find-median-from-data-stream

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-median-from-data-stream.md

Process a finite sequence of operations while maintaining every integer added so far. Each row in operations has one of these forms:

  uv run python amazon_oa/amazon-find-median-from-data-stream/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-median-from-data-stream/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def processMedianOperations(self, operations):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in processMedianOperations above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().processMedianOperations(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
