"""Get Min Num Moves — https://www.fastprep.io/problems/amazon-get-min-num-moves

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-min-num-moves.md

Imagine you are shopping on Amazon.com for some good weight lifting equipment. The equipment you want has blocks of many different weights that you can combine to lift.

  uv run python amazon_oa/amazon-get-min-num-moves/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-min-num-moves/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMinNumMoves(self, blocks):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMinNumMoves above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMinNumMoves(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
