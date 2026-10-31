"""Dense Matrix Multiplication — https://www.fastprep.io/problems/amazon-dense-matrix-multiplication

Write-up & approaches: ../../../docs/amazon/amazon-dense-matrix-multiplication.md

You are given two rectangular integer matrices: left has m rows and k columns, and right has k rows and n columns. Return their matrix product, which has m rows and n columns.

  uv run python amazon/amazon-dense-matrix-multiplication/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-dense-matrix-multiplication/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def multiplyMatrices(self, left, right):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in multiplyMatrices above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().multiplyMatrices(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
