"""Get Priorities After Execution — https://www.fastprep.io/problems/get-priorities-after-execution

Write-up & approaches: ../../../docs/problems/amazon_oa/get-priorities-after-execution.md

Several processes are scheduled for execution on an AWS server.

  uv run python amazon_oa/get-priorities-after-execution/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/get-priorities-after-execution/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getPrioritiesAfterExecution(self, priority):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getPrioritiesAfterExecution above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getPrioritiesAfterExecution(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
