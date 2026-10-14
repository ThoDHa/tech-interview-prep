"""Maximum Equal Parts for Prefixes — https://www.fastprep.io/problems/amazon-maximum-equal-parts-for-prefixes

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximum-equal-parts-for-prefixes.md

A team at Amazon is working to ensure all packages are correctly sorted for delivery. Each package has a label represented by an uppercase English letter. The full list of labels is given as the strin

  uv run python amazon_oa/amazon-maximum-equal-parts-for-prefixes/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximum-equal-parts-for-prefixes/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximumEqualParts(self, packages):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximumEqualParts above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximumEqualParts(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
