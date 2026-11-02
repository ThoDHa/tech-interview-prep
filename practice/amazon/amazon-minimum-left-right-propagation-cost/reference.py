"""Minimum Cost of Left and Right Propagation — https://www.fastprep.io/problems/amazon-minimum-left-right-propagation-cost

Write-up & approaches: ../../../docs/amazon/amazon-minimum-left-right-propagation-cost.md

Reference implementation of the write-up's recommended Kept-Run Greedy
solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-minimum-left-right-propagation-cost/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-minimum-left-right-propagation-cost/              # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def minimumPropagationCost(self, values: List[int]) -> int:
        """Return the minimum total cost of left and right propagations
        that makes every element equal.

        The positions no operation writes form one contiguous stretch,
        and they must already hold the final value, so an optimal plan
        keeps one equal-value run and flattens both outsides with at
        most one propagation per direction. A second propagation in a
        direction either covers a superset (its predecessor was wasted)
        or leaves a hole, and propagating from inside the kept run
        changes nothing. Extending a run strictly lowers the flattened
        width at the same value, so scanning only the maximal runs and
        scoring `(left + n - 1 - right) * value` per run, keeping the
        minimum, is exact. An already-uniform array's single run scores
        0, the statement's zero-operation case.

        Args:
            values: Positive integers, `1 <= n <= 100000`, values up to
                `1e9`; the answer fits a signed 64-bit integer.

        Returns:
            The minimum total propagation cost.

        Time:  O(n): one pass splits the maximal runs; each element is
               touched by the run scan exactly twice.
        Space: O(1): two run pointers and the running minimum.
        """
        count = len(values)
        best = None
        left = 0
        while left < count:
            right = left
            while right + 1 < count and values[right + 1] == values[left]:
                right += 1
            cost = (left + count - 1 - right) * values[left]
            if best is None or cost < best:
                best = cost
            left = right + 1
        return best


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumPropagationCost above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().minimumPropagationCost(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
