"""Find Requests In Queue — https://www.fastprep.io/problems/amazon-find-requests-in-queue

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-requests-in-queue.md

Amazon Web Services (AWS) is a cloud computing platform with multiple servers. One of the servers is assigned to serve customer requests. There are n customer requests placed sequentially in a queue, 

  uv run python amazon_oa/amazon-find-requests-in-queue/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-requests-in-queue/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findRequestsInQueue(self, wait):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findRequestsInQueue above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findRequestsInQueue(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
