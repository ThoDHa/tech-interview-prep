"""Maximum Quality Sum — https://www.fastprep.io/problems/amazon-maximum-quality-sum

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximum-quality-sum.md

Amazon's AWS provides fast and efficient server solutions. The developers want to stress-test the quality of the servers' channels. They must ensure the following:

  uv run python amazon_oa/amazon-maximum-quality-sum/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximum-quality-sum/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximumQualitySum(self, packets, channels):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximumQualitySum above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximumQualitySum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
