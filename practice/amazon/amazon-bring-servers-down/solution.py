"""Bring Servers Down — https://www.fastprep.io/problems/amazon-bring-servers-down

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-bring-servers-down.md

The developers at Amazon want to perform a reliability drill on some servers. There are n servers where the ith server can serve request[i] number of requests and has an initial health of health[i] un

  uv run python amazon_oa/amazon-bring-servers-down/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-bring-servers-down/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimumRequests(self, request, health, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumRequests above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimumRequests(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
