"""Maximum Frequency Stack — https://www.fastprep.io/problems/amazon-maximum-frequency-stack

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximum-frequency-stack.md

Design a stack-like data structure that supports push and pop.

  uv run python amazon_oa/amazon-maximum-frequency-stack/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximum-frequency-stack/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def processFrequencyStack(self, operations, values):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in processFrequencyStack above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().processFrequencyStack(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
