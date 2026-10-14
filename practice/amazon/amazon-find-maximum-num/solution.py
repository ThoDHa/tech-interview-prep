"""Find Max Num — https://www.fastprep.io/problems/amazon-find-maximum-num

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-maximum-num.md

Special thanks: whale and spike contributed this problem.

  uv run python amazon_oa/amazon-find-maximum-num/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-maximum-num/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findMaximumNum(self, answered, needed, q):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMaximumNum above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMaximumNum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
