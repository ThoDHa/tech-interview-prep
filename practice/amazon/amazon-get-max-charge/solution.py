"""Get Max Charge — https://www.fastprep.io/problems/amazon-get-max-charge

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-max-charge.md

A team of engineers at Amazon, using advanced simulation tools, are analyzing a series of interconnected systems, where each system has a charge value represented by charge[i] (which can be positive, 

  uv run python amazon_oa/amazon-get-max-charge/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-max-charge/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMaxCharge(self, charge):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMaxCharge above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMaxCharge(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
