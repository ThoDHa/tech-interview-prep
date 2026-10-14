"""Min Dock Bays — https://www.fastprep.io/problems/amazon-get-minimum-dock-bays

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-minimum-dock-bays.md

You are managing operations at a large Amazon warehouse. Loaded trucks arrive at the warehouse sequentially and must be unloaded within a specific timeframe to ensure timely delivery. Your task is to 

  uv run python amazon_oa/amazon-get-minimum-dock-bays/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-minimum-dock-bays/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMinimumDockBays(self, truckCargoSize, maxTurnaroundTime):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMinimumDockBays above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMinimumDockBays(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
