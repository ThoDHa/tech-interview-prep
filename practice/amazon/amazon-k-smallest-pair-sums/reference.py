"""Find K Pairs with Smallest Sums — https://www.fastprep.io/problems/amazon-k-smallest-pair-sums

Write-up & approaches: ../../../docs/amazon/amazon-k-smallest-pair-sums.md

Reference implementation of the write-up's recommended Min-Heap Row
Merge solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-k-smallest-pair-sums/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-k-smallest-pair-sums/              # run the test sets
"""

import heapq
from typing import List

from harness import pick_case


class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        """Return the k pairs with the smallest sums, in nondecreasing sum order.

        Each row (one per `nums1` index) offers its pairs in ascending sum,
        so the merge keeps a heap of the rows' current heads as
        `(sum, row, column)` tuples; tuple comparison pops equal sums in
        ascending `(row, column)` order, the page's pinned tie rule. Only
        the first `min(len(nums1), k)` rows can ever contribute a pair,
        so the heap is seeded no deeper than that.

        Args:
            nums1: First array, sorted in nondecreasing order; the page
                constraints give 1 <= len(nums1) <= 100000 and values in
                [-10^9, 10^9].
            nums2: Second array, sorted in nondecreasing order, with the
                same bounds.
            k: How many pairs to return; 1 <= k <= len(nums1) * len(nums2).

        Returns:
            The k pairs `[nums1[i], nums2[j]]` with the smallest sums, in
            nondecreasing sum order, ties broken by ascending `i` then
            `j`; duplicate value pairs from different indices are kept.

        Time:  O(k * log(min(n, k))): k pops and at most k pushes over a
               heap of at most min(n, k) tuples, seeded by one heapify.
        Space: O(min(n, k)): the heap, plus the output.
        """
        live_rows = min(len(nums1), k)
        row_heads = [(nums1[row] + nums2[0], row, 0) for row in range(live_rows)]
        heapq.heapify(row_heads)

        smallest_pairs = []
        while len(smallest_pairs) < k and row_heads:
            _, row, column = heapq.heappop(row_heads)
            smallest_pairs.append([nums1[row], nums2[column]])
            next_column = column + 1
            if next_column < len(nums2):
                heapq.heappush(
                    row_heads, (nums1[row] + nums2[next_column], row, next_column)
                )
        return smallest_pairs


if __name__ == "__main__":
    # Debug playground: set a breakpoint in kSmallestPairs above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().kSmallestPairs(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
