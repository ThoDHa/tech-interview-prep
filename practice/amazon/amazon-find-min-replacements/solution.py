"""Find Replacement — https://www.fastprep.io/problems/amazon-find-min-replacements

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-min-replacements.md

In Amazon's distribution network, there are several drones with varying capacities, ranging from 1 to 10^9. Each j-th drone has a carrying capacity of j. The company needs to dispatch n packages, wher

  uv run python amazon_oa/amazon-find-min-replacements/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-min-replacements/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findMinReplacements(self, parcels):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMinReplacements above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMinReplacements(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
