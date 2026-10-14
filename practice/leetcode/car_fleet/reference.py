"""Car Fleet — https://leetcode.com/problems/car-fleet/

Write-up & approaches: ../../docs/problems/car_fleet.md
Reference implementation of the write-up's Single-Pass Counter solution.

There are `n` cars traveling to the same destination on a one-lane highway. You are given two arrays of integers `position` and `speed`, both of length `n`, and the `target` position. A car can not pass another car ahead of it; a car fleet is a non-empty set of cars driving at the same position and same speed. Return the number of different car fleets that will arrive at the destination.

  uv run python car_fleet/reference.py   # debug one case (see CASE below)
  uv run pytest car_fleet/              # run the test sets
"""

from harness import pick_case


class Solution:
    def carFleet(self, target, position, speed):
        """Count the fleets that reach `target`, scanning positions once.

        Sorts the cars by position, closest to the target first, and walks
        them in that order computing each car's arrival time. A car slower
        to arrive than every fleet ahead of it starts a new fleet; arriving
        no later means it merges into the fleet directly ahead.

        Args:
            target: Destination position, 0 < target.
            position: Unique start positions, each 0 <= position[i] < target.
            speed: Speeds in the same order, each 1 <= speed[i].

        Returns:
            The number of car fleets that arrive at the destination.

        Time:  O(n log n): the position sort dominates the linear scan.
        Space: O(n): the sorted (position, speed) pairs.
        """
        cars = sorted(zip(position, speed), reverse=True)
        fleets = 0
        fleet_time = 0.0
        for pos, spd in cars:
            time = (target - pos) / spd
            if time > fleet_time:
                fleets += 1
                fleet_time = time
        return fleets


if __name__ == "__main__":
    # Debug playground: set a breakpoint in carFleet above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().carFleet(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
