"""Max Transfer Rate — https://www.fastprep.io/problems/amazon-max-transfer-rate

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-max-transfer-rate.md

You are in the Amazon's Cloud Infrastructure Team, and you are working on a project to optimize how data flows through its network of storage servers.

  uv run python amazon_oa/amazon-max-transfer-rate/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-max-transfer-rate/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maxTransferRate(self, throughput, pipelineCount):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxTransferRate above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxTransferRate(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
