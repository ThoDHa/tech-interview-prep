"""0/1 Knapsack — https://www.fastprep.io/problems/amazon-zero-one-knapsack

Write-up & approaches: ../../../docs/amazon/amazon-zero-one-knapsack.md

Reference implementation of the write-up's recommended Bottom-Up
Space-Optimized DP solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-zero-one-knapsack/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-zero-one-knapsack/              # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def maximumKnapsackValue(
        self, weights: List[int], values: List[int], capacity: int
    ) -> int:
        """Return the maximum total value of a subset of the items whose
        total weight is at most `capacity`, each item taken at most once.

        The row of the classic two-dimensional DP table collapses into
        one array: `best_value[c]` holds the best value achievable with
        capacity `c` using only the items processed so far. Each item
        updates the array in descending capacity order, so an item is
        never counted twice in one row.

        Args:
            weights: Item weights, each at least 1.
            values: Item values, each at least 0, aligned with weights.
            capacity: The total weight budget, at least 0.

        Returns:
            The maximum achievable total value; 0 when nothing fits.

        Time:  O(n * capacity): one descending sweep of the array per
            item, n = len(weights).
        Space: O(capacity): the single rolling row regardless of n.
        """
        best_value = [0] * (capacity + 1)
        for weight, value in zip(weights, values):
            for remaining in range(capacity, weight - 1, -1):
                best_value[remaining] = max(
                    best_value[remaining], best_value[remaining - weight] + value
                )
        return best_value[capacity]


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximumKnapsackValue above, then
    # run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().maximumKnapsackValue(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
