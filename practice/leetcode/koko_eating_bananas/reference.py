"""Koko Eating Bananas — https://leetcode.com/problems/koko-eating-bananas/

Write-up & approaches: ../../docs/problems/koko_eating_bananas.md
Reference implementation of the write-up's Binary Search on the Answer solution.

You are given an integer array `piles` where `piles[i]` is the number of bananas in the `ith` pile, and an integer `h`, the number of hours you have to eat all the bananas. Each hour you choose a pile and eat `k` bananas from it; you cannot split a pile across hours. Return the minimum integer `k` such that you can eat all the bananas within `h` hours.

  uv run python koko_eating_bananas/reference.py   # debug one case (see CASE below)
  uv run pytest koko_eating_bananas/              # run the test sets
"""

from harness import pick_case


def hours_needed(piles, k):
    """Count the hours eating rate `k` needs for every pile in `piles`.

    A pile of `bananas` takes ceil(bananas / k) hours, the number of
    half-open k-sized chunks that cover it.

    Args:
        piles: Banana counts, each 1 <= piles[i].
        k: Eating rate, 1 <= k.

    Returns:
        The total hours at rate `k`, one chunk minimum per pile.

    Time:  O(n): one pass over the piles.
    Space: O(1).
    """
    return sum((bananas + k - 1) // k for bananas in piles)


class Solution:
    def minEatingSpeed(self, piles, h):
        """Find the minimum rate finishing every pile within `h` hours.

        Binary searches the answer on the monotonic predicate
        "rate k finishes in time": the feasible rates form the suffix
        [some k_min, max(piles)], so halving the interval on the
        hours_needed probe lands on the smallest feasible rate.

        Args:
            piles: Banana counts, 1 <= len(piles), each 1 <= piles[i].
            h: Available hours, len(piles) <= h.

        Returns:
            The smallest integer rate k with hours_needed(piles, k) <= h.

        Time:  O(n log m): log m probes, each an O(n) pass over the piles
            (m = max(piles)).
        Space: O(1): only search-boundary variables.
        """
        left, right = 1, max(piles)
        while left < right:
            mid = (left + right) // 2
            if hours_needed(piles, mid) <= h:
                right = mid
            else:
                left = mid + 1
        return left


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minEatingSpeed above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minEatingSpeed(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
