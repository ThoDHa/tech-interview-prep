"""Combination Sum II — https://leetcode.com/problems/combination-sum-ii/

Write-up & approaches: ../../docs/problems/combination_sum_ii.md
Canonical reference implementation of the write-up's Sorted Backtracking with
Duplicate Skipping solution, kept next to the harness so authored cases stay
falsifiable. Your own attempt lives in solution.py.

  uv run python combination_sum_ii/reference.py   # debug one case (see below)
  uv run pytest combination_sum_ii/               # run the test sets
"""

from typing import List


class Solution:
    def solve(self, candidates: List[int], target: int) -> List[List[int]]:
        """Return every unique combination of `candidates` summing to `target`.

        Sorts `candidates` so equal values sit adjacent, then backtracks over
        a `start` index, recursing on `i + 1` so each element is used at most
        once. Within one loop level (same `start`) any value equal to its left
        sibling is skipped, so duplicates never arise instead of being
        filtered afterward; the second twin stays reachable one level deeper,
        where `start` has moved past the first. Sorting also upgrades the
        overshoot test to a `break`: the first candidate exceeding
        `remaining` ends the whole level, since every later one is at least
        as large.

        Args:
            candidates: Available values, may contain duplicates,
                1 <= len(candidates) <= 100, each in [1, 50]; sorted in
                place.
            target: Sum to reach, 1 <= target <= 30.

        Returns:
            All unique combinations, each a non-decreasing list summing to
            `target`, in no particular order.

        Time:  O(2^N * k): each of the N candidates is included or excluded,
            and each recorded combination of length k is copied; the skip
            rule and the `break` prune cut whole levels and subtrees in
            practice.
        Space: O(N): the recursion depth and `current` are bounded by the
            candidate count, since each element is used at most once
            (excluding the output).
        """

        def backtrack(start: int, remaining: int, current: List[int]) -> None:
            if remaining == 0:
                result.append(current[:])
                return
            for i in range(start, len(candidates)):
                if i > start and candidates[i] == candidates[i - 1]:
                    continue
                candidate = candidates[i]
                if candidate > remaining:
                    break
                current.append(candidate)
                backtrack(i + 1, remaining - candidate, current)
                current.pop()

        candidates.sort()
        result: List[List[int]] = []
        backtrack(0, target, [])
        return result


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    # cases.json is empty (any-order output), so a literal example stands in.
    candidates = [9, 2, 2, 4, 6, 1, 5]
    target = 8
    combinations = Solution().solve(list(candidates), target)
    print(f"args = candidates={candidates}, target={target}")
    print(f"got: {combinations}")
