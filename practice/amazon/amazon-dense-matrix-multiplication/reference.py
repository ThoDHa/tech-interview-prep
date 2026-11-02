"""Dense Matrix Multiplication — https://www.fastprep.io/problems/amazon-dense-matrix-multiplication

Write-up & approaches: ../../../docs/amazon/amazon-dense-matrix-multiplication.md

Reference implementation of the write-up's recommended Row-Wise Loop
Reorder solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-dense-matrix-multiplication/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-dense-matrix-multiplication/              # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def multiplyMatrices(self, left: List[List[int]], right: List[List[int]]) -> List[List[int]]:
        """Return the matrix product of `left` (m by k) and `right` (k by n).

        The loops run in `(i, t, j)` order: for fixed row `i` and inner
        index `t`, the scalar `left[i][t]` is read once and the inner
        loop adds its scaled copy of `right`'s row `t` into the result
        row, walking both rows left to right, the order they occupy in
        memory. Summation order does not affect the integer result, so
        the arithmetic matches the definition exactly while every
        innermost read is contiguous.

        Args:
            left: Rectangular m by k matrix, 1 <= m, k <= 64, elements
                in [-100, 100].
            right: Rectangular k by n matrix sharing `left`'s inner
                dimension, 1 <= n <= 64, elements in [-100, 100].

        Returns:
            The m by n product; entry (i, j) is sum over t of
            left[i][t] * right[t][j].

        Time:  O(m * n * k): every cell accumulates k multiply-adds;
               the reorder changes their order, never the count.
        Space: O(1): beyond the returned matrix, one scalar and two
               row references.
        """
        rows, inner, columns = len(left), len(right), len(right[0])
        result = [[0] * columns for _ in range(rows)]
        for i in range(rows):
            result_row = result[i]
            for t in range(inner):
                left_value = left[i][t]
                right_row = right[t]
                for j in range(columns):
                    result_row[j] += left_value * right_row[j]
        return result


if __name__ == "__main__":
    # Debug playground: set a breakpoint in multiplyMatrices above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().multiplyMatrices(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
