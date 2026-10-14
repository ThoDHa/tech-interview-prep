"""Stack with Constant-Time Middle Queries — https://www.fastprep.io/problems/amazon-middle-stack-operations

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-middle-stack-operations.md

Process a sequence of stack operations. Each operation is ["push", value], ["pop"], ["top"], or ["middle"]. Values are signed decimal integers encoded as strings.

  uv run python amazon_oa/amazon-middle-stack-operations/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-middle-stack-operations/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def processMiddleStack(self, operations):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in processMiddleStack above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().processMiddleStack(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
