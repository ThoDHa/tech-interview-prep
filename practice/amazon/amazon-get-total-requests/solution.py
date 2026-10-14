"""Get Total Requests — https://www.fastprep.io/problems/amazon-get-total-requests

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-total-requests.md

Developers at Amazon have their applications deployed on n servers. Initially, the ith server has an id server[i] and can handle server[i] requests at a time.

  uv run python amazon_oa/amazon-get-total-requests/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-total-requests/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getTotalRequests(self, server, replaced, newId):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getTotalRequests above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getTotalRequests(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
