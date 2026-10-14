"""Get Active Requests Count — https://www.fastprep.io/problems/amazon-get-active-requests-count

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-active-requests-count.md

You are given an integer, requests which denotes the number of requests, and a list wait_time, where wait_time[i] denote the maximum wait time of the i'th request. The requests in the list are served 

  uv run python amazon_oa/amazon-get-active-requests-count/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-active-requests-count/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getActiveRequestsCount(self, requests, wait_time):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getActiveRequestsCount above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getActiveRequestsCount(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
