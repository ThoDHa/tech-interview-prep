"""Get Min Moves — https://www.fastprep.io/problems/amazon-get-min-moves

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-min-moves.md

Developers at Amazon are working on a new algorithm using the Bitwise XOR operation.

  uv run python amazon_oa/amazon-get-min-moves/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-min-moves/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMinMoves(self, arr):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMinMoves above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMinMoves(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
