"""Tallest Billboard — https://www.fastprep.io/problems/amazon-tallest-billboard

Write-up & approaches: ../../../docs/amazon/amazon-tallest-billboard.md

Reference implementation of the write-up's recommended Bottom-Up
Difference DP solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-tallest-billboard/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-tallest-billboard/              # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def tallestBillboard(self, rods: List[int]) -> int:
        """Return the greatest common height of two disjoint rod groups.

        `best_shorter[d]` tracks, over assignments of the rods processed
        so far, the tallest shorter support among the assignments whose
        two supports differ by exactly `d`; `-1` marks a difference no
        assignment builds. Each rod rolls the row forward once: copied
        states are the rod unused, `difference + rod` puts it on the
        taller side (the shorter support is unchanged), and
        `abs(difference - rod)` puts it on the shorter side, where it
        grows that support by `min(difference, rod)` before the sides
        possibly swap. Difference zero at the end is a level ending.

        Args:
            rods: Rod lengths; the page constraints give
                1 <= len(rods) <= 20, 1 <= rods[i] <= 1000, and a total
                length of at most 5000.

        Returns:
            The greatest common sum of two disjoint rod groups, 0 when
            no positive split exists (the empty groups always level).

        Time:  O(n * S): one sweep of at most `total + 1` differences
               per rod, with S = sum(rods) <= 5000.
        Space: O(S): the rolling row and its updated copy.
        """
        total = sum(rods)
        best_shorter = [-1] * (total + 1)
        best_shorter[0] = 0

        for rod in rods:
            updated = best_shorter[:]
            for difference in range(total - rod + 1):
                shorter = best_shorter[difference]
                if shorter < 0:
                    continue
                if shorter > updated[difference + rod]:
                    updated[difference + rod] = shorter
                split = abs(difference - rod)
                grown = shorter + min(difference, rod)
                if grown > updated[split]:
                    updated[split] = grown
            best_shorter = updated

        return best_shorter[0]


if __name__ == "__main__":
    # Debug playground: set a breakpoint in tallestBillboard above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().tallestBillboard(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
