"""HTTP Request Redirection — https://www.fastprep.io/problems/amazon-http-request-redirection

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-http-request-redirection.md

Amazon engineers are investigating an HTTP request that is redirected among servers.

  uv run python amazon_oa/amazon-http-request-redirection/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-http-request-redirection/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findFinalServer(self, locations, redirectRecords):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findFinalServer above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findFinalServer(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
