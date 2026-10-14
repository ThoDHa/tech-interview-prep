"""Minimize Variation — https://www.fastprep.io/problems/amazon-minimize-variation

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimize-variation.md

Source note: Examples 3 through 5 were added on 2025-06-25, with relevant source images included in Problem Source. The original poster said Example 5 failed but did not clarify whether the testcase i

  uv run python amazon_oa/amazon-minimize-variation/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimize-variation/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimizeVariation(self, productSize):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimizeVariation above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimizeVariation(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
