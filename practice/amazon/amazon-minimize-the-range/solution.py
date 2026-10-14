"""Fortune Telling — https://www.fastprep.io/problems/amazon-minimize-the-range

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimize-the-range.md

Given a collection of n cards. The i-th card (1 ≤ i ≤ n) has a number Ai on its front and a number Bi on its back. At the start, all the cards are facing upwards. He wants to minimize the range of num

  uv run python amazon_oa/amazon-minimize-the-range/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimize-the-range/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimizeTheRange(self, n, m, A, B):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimizeTheRange above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimizeTheRange(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
