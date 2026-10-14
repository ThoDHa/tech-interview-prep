"""Number of Suitable Locations — https://www.fastprep.io/problems/amazon-num-of-suitable-places

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-num-of-suitable-places.md

Amazon has multiple delivery centers across the world, represented by a number line from -10^9 to 10^9. There are n delivery centers, the ith one located at position center[i].

  uv run python amazon_oa/amazon-num-of-suitable-places/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-num-of-suitable-places/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def numberOfSuitablePlaces(self, center, d):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in numberOfSuitablePlaces above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().numberOfSuitablePlaces(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
