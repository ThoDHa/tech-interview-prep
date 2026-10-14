"""Get Min Errors — https://www.fastprep.io/problems/amazon-get-min-errors

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-min-errors.md

Amazon's database doesn’t support very large numbers, so numbers are stored as a string of binary characters, '0' and '1'. Accidentally, a '!' was entered at some positions and it is unknown whether t

  uv run python amazon_oa/amazon-get-min-errors/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-min-errors/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMinErrors(self, errorString, x, y):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMinErrors above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMinErrors(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
