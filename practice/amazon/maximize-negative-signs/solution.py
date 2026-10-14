"""Maximize Negative Signs — https://www.fastprep.io/problems/maximize-negative-signs

Write-up & approaches: ../../../docs/problems/amazon_oa/maximize-negative-signs.md

Given a sequence of n natural numbers a_1, a_2, ..., a_n, you are to assign a sign (+ or -) to each a_i such that the cumulative sum of the signed a_1 + a_2 + ... + a_i remains positive for each i in 

  uv run python amazon_oa/maximize-negative-signs/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/maximize-negative-signs/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximizeNegativeSigns(self, sequence):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximizeNegativeSigns above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximizeNegativeSigns(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
