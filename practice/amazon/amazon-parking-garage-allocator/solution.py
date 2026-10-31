"""Parking Garage Allocator — https://www.fastprep.io/problems/amazon-parking-garage-allocator

Write-up & approaches: ../../../docs/amazon/amazon-parking-garage-allocator.md

Manage spaceCount parking spaces. Each operation is "PARK size" or "LEAVE start size". A park request occupies the leftmost available run of the requested size and contributes its starting index, or -

  uv run python amazon/amazon-parking-garage-allocator/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-parking-garage-allocator/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def processParking(self, spaceCount, operations):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in processParking above, then run this file.
    CASE = None
    if CASE is None:
        print("no cases authored yet; add cases to cases.json or cases_full.json, then set CASE to an id")
    else:
        case = pick_case(__file__, CASE)
        result = Solution().processParking(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
