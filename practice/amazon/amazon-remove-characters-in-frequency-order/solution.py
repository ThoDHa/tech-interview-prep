"""Remove Characters in Frequency Order — https://www.fastprep.io/problems/amazon-remove-characters-in-frequency-order

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-remove-characters-in-frequency-order.md

(Look into LC 664. Strange Printer may help :)

  uv run python amazon_oa/amazon-remove-characters-in-frequency-order/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-remove-characters-in-frequency-order/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimumOperationsToRemove(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumOperationsToRemove above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimumOperationsToRemove(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
