"""Find Minimum Groups — https://www.fastprep.io/problems/amazon-find-minimum-groups

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-minimum-groups.md

A financial services company has requested AWS for a private deployment of its cloud network. Considering the sensitive nature of the company's business, AWS has also advised them to add a specific ty

  uv run python amazon_oa/amazon-find-minimum-groups/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-minimum-groups/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findMinimumGroups(self, security):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMinimumGroups above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMinimumGroups(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
