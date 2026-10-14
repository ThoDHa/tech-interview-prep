"""Find Unique Values — https://www.fastprep.io/problems/amazon-find-unique-values

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-unique-values.md

There are n developers working at Amazon where the ith developer has the experience points experience[i]. The company decided to pair the developers by iteratively pairing the developers with the high

  uv run python amazon_oa/amazon-find-unique-values/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-unique-values/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findUniqueValues(self, experience):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findUniqueValues above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findUniqueValues(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
