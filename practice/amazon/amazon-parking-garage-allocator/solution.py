"""Parking Garage Allocator — https://www.fastprep.io/problems/amazon-parking-garage-allocator

Write-up & approaches: ../../../docs/amazon/amazon-parking-garage-allocator.md

Manage spaceCount parking spaces. Each operation is "PARK size" or "LEAVE start size". A park request occupies the leftmost available run of the requested size and contributes its starting index, or -

  uv run python amazon/amazon-parking-garage-allocator/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-parking-garage-allocator/              # run the test sets
"""
from harness import NotSolved, pick_case, run_operations


class ParkingGarage:
    def __init__(self, space_count: int) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def park(self, size: int) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def leave(self, freed_start: int, freed_size: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a ParkingGarage method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(ParkingGarage, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement ParkingGarage's methods first")
