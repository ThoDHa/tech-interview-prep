"""Get Min Time — https://www.fastprep.io/problems/amazon-get-min-time

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-min-time.md

Developers at Amazon have deployed an application with a distributed database. It is stored on total_servers different servers numbered from 1 to total_servers that are connected in a circular fashion

  uv run python amazon_oa/amazon-get-min-time/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-min-time/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMinTime(self, total_servers, servers):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMinTime above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMinTime(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
