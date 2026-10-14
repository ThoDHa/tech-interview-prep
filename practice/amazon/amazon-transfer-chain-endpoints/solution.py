"""Initial and Final Accounts in a Transfer Chain — https://www.fastprep.io/problems/amazon-transfer-chain-endpoints

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-transfer-chain-endpoints.md

You are given directed account-transfer pairs [from, to] in arbitrary order. Together they form one non-branching chain containing every pair exactly once.

  uv run python amazon_oa/amazon-transfer-chain-endpoints/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-transfer-chain-endpoints/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def transferEndpoints(self, transfers):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in transferEndpoints above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().transferEndpoints(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
