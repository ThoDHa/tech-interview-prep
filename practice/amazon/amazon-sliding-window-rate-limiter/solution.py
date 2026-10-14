"""Sliding-Window Rate Limiter — https://www.fastprep.io/problems/amazon-sliding-window-rate-limiter

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-sliding-window-rate-limiter.md

You receive requests in nondecreasing timestamp order. Each request has a user ID and an integer timestamp in seconds.

  uv run python amazon_oa/amazon-sliding-window-rate-limiter/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-sliding-window-rate-limiter/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def applySlidingWindowRateLimit(self, userIds, timestamps):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in applySlidingWindowRateLimit above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().applySlidingWindowRateLimit(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
