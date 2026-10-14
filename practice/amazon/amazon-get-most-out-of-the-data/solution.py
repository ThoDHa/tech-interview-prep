"""Get The Most Out Of The Data — https://www.fastprep.io/problems/amazon-get-most-out-of-the-data

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-most-out-of-the-data.md

DAs at TomTom Global are deeply engaged in the analysis of the info gained when the company's re-inforcement learning AI model named Supa Helo is trained with different arrangements of exact the same 

  uv run python amazon_oa/amazon-get-most-out-of-the-data/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-most-out-of-the-data/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMostOutOfData(self, data):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMostOutOfData above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMostOutOfData(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
