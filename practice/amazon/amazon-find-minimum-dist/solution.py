"""Get Min Distance (AMZ CN) — https://www.fastprep.io/problems/amazon-find-minimum-dist

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-minimum-dist.md

note - See the Problem Source at the vely bottom of the page for the original problem description~

  uv run python amazon_oa/amazon-find-minimum-dist/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-minimum-dist/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findMinimumDist(self, center, destination):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMinimumDist above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMinimumDist(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
