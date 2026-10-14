"""Environment Variable Store and Substitution — https://www.fastprep.io/problems/amazon-environment-variable-substitution

Write-up & approaches: ../../../docs/amazon/amazon-environment-variable-substitution.md

Process a sequence of environment-variable operations:

  uv run python amazon_oa/amazon-environment-variable-substitution/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-environment-variable-substitution/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def processEnvironment(self, operations):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in processEnvironment above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().processEnvironment(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
