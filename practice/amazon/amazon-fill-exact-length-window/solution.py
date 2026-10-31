"""Fill One Exact-Length Binary Window — https://www.fastprep.io/problems/amazon-fill-exact-length-window

Write-up & approaches: ../../../docs/amazon/amazon-fill-exact-length-window.md

Given a binary string log and an integer k, choose exactly one contiguous substring of length k. Change every 0 inside it to 1. Ones inside the window and all characters outside it stay unchanged.

  uv run python amazon/amazon-fill-exact-length-window/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-fill-exact-length-window/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, log, k):
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
