"""Get Max Stability — https://www.fastprep.io/problems/amazon-get-max-stability

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-max-stability.md

AWS provides a range of servers to meet the deployment needs of its clients. A client wants to choose a set of servers to deploy their application. Each server is

  uv run python amazon_oa/amazon-get-max-stability/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-max-stability/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMaxStability(self, reliability, availability):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMaxStability above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMaxStability(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
