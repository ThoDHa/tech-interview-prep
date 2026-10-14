"""Count Islands from Streaming Rows — https://www.fastprep.io/problems/amazon-streaming-island-count

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-streaming-island-count.md

A binary matrix arrives one row at a time from top to bottom. Given those rows as the finite ordered batch rows, return an array where result i is the number of islands present after rows 0 through i 

  uv run python amazon_oa/amazon-streaming-island-count/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-streaming-island-count/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, rows):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().solve(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
