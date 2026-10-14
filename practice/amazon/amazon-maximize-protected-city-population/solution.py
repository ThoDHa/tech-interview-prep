"""Maximize Protected City Population — https://www.fastprep.io/problems/amazon-maximize-protected-city-population

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximize-protected-city-population.md

You are given n cities arranged in a line. City i has population population[i] and may contain a security unit described by unit[i], where unit[i] = '1' means a unit is initially stationed in city i.

  uv run python amazon_oa/amazon-maximize-protected-city-population/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximize-protected-city-population/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximizeProtectedPopulation(self, population, unit):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximizeProtectedPopulation above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximizeProtectedPopulation(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
