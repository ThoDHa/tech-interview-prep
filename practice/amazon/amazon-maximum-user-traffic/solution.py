"""Max User Traffic — https://www.fastprep.io/problems/amazon-maximum-user-traffic

Write-up & approaches: ../../../docs/amazon/amazon-maximum-user-traffic.md

In order to ensure a hassle-free user experience during the festive season, Amazon maintains logs of the days when its users use the Amazon Shopping app.

  uv run python amazon/amazon-maximum-user-traffic/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-maximum-user-traffic/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximumUserTraffic(self, login, logout):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximumUserTraffic above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximumUserTraffic(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
