"""Connect N Ropes With Minimum Cost — https://www.fastprep.io/problems/amazon-connect-ropes-minimum-cost

Write-up & approaches: ../../../docs/amazon/amazon-connect-ropes-minimum-cost.md

Reference implementation of the write-up's recommended Min-Heap with
heapq solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-connect-ropes-minimum-cost/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-connect-ropes-minimum-cost/              # run the test sets
"""

import heapq
from typing import List

from harness import pick_case


class Solution:
    def minimumRopeConnectionCost(self, ropes: List[int]) -> int:
        """Return the minimum total cost of merging all ropes into one.

        Always connecting the two shortest ropes is optimal: each rope
        contributes its length once per merge above it, so keeping long
        ropes shallow minimizes the sum of depth-weighted lengths. A
        min-heap serves "the two shortest ropes so far" in O(log n):
        pop two, pay their sum, and feed the combined rope back.

        Args:
            ropes: Rope lengths, 1 <= ropes[i] <= 10^4 with
                1 <= len(ropes) <= 10^5 per the page constraints.

        Returns:
            The minimum total connection cost; 0 when fewer than two
            ropes need no operation at all.

        Time:  O(n + k log n): heapify is linear, and each of the k = n - 1
            merges does two pops and one push on a heap of size O(n).
        Space: O(n): the heap holds every rope not yet merged.
        """
        if len(ropes) <= 1:
            return 0

        total_cost = 0
        min_heap = list(ropes)
        heapq.heapify(min_heap)

        while len(min_heap) > 1:
            first_rope = heapq.heappop(min_heap)
            second_rope = heapq.heappop(min_heap)
            combined = first_rope + second_rope
            total_cost += combined
            heapq.heappush(min_heap, combined)

        return total_cost


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumRopeConnectionCost above,
    # then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().minimumRopeConnectionCost(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
