"""Combination Sum: https://leetcode.com/problems/combination-sum/

Write-up & approaches: ../../../docs/leetcode/combination_sum.md

Given an array of distinct integers `candidates` and a target integer `target`,
return all unique combinations of `candidates` whose numbers sum to `target`. The
same number may be reused an unlimited number of times. Combinations may be
returned in any order.

  uv run python combination_sum/solution.py     # debug one case (see CASE below)
  uv run pytest combination_sum/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        result: List[List[int]] = []
        candidates.sort()

        def backtrack(index: int, remaining: int, current: List[int]):
            if remaining == 0:
                result.append(current[:])
                return
            if remaining < 0 or index >= len(candidates):
                return

            current.append(candidates[index])
            backtrack(index, remaining - candidates[index], current)
            current.pop()

            backtrack(index + 1, remaining, current)

        def dynamic():
            dp: List[List[List[int]]] = [[] for _ in range(target + 1)]
            dp[0] = [[]]

            for candidate in candidates:
                for x in range(candidate, target + 1):
                    for combo in dp[x - candidate]:
                        dp[x].append(combo + [candidate])
            return dp[target]

        return dynamic()


if __name__ == "__main__":
    # Debug playground: set a breakpoint in combinationSum above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().combinationSum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
