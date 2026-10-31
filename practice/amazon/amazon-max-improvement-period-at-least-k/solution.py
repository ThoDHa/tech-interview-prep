"""Best Improvement Period of at Least K Intervals — https://www.fastprep.io/problems/amazon-max-improvement-period-at-least-k

Write-up & approaches: ../../../docs/amazon/amazon-max-improvement-period-at-least-k.md

A machine learning team tracks how a recommendation model changes over n consecutive time intervals. You are given an integer array changes of length n, where changes[i] is the change in recommendatio

  uv run python amazon/amazon-max-improvement-period-at-least-k/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-max-improvement-period-at-least-k/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, changes, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().solve(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
