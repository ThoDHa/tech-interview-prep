"""Get Maximum Sum — https://www.fastprep.io/problems/amazon-get-maximum-sum

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-maximum-sum.md

Note 📝 - might be a sister problem of  🦥 Get Max Sum

  uv run python amazon_oa/amazon-get-maximum-sum/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-maximum-sum/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMaximumSum(self, health, serverType, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMaximumSum above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMaximumSum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
