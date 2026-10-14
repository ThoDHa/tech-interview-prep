"""Sort Permutation — https://www.fastprep.io/problems/amazon-can-sort-permutation-in-given-moves

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-can-sort-permutation-in-given-moves.md

Amazon recently conducted interviews where the candidates were asked to sort the permutation p of length n. Then the ith candidate sorted the permutation in moves[i] moves. To verify the result once m

  uv run python amazon_oa/amazon-can-sort-permutation-in-given-moves/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-can-sort-permutation-in-given-moves/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def canSortPermutation(self, p, moves):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in canSortPermutation above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().canSortPermutation(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
