"""Gas Station — https://leetcode.com/problems/gas-station/

Write-up & approaches: ../../docs/problems/gas_station.md
Reference implementation of the write-up's Greedy solution, kept next to the
harness so authored cases stay falsifiable. Your own attempt lives in
solution.py.

  uv run python gas_station/reference.py   # replay the example cases
  uv run pytest gas_station/               # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        """Return the start index of a completable circuit, or -1.

        Time:  O(n): one pass, constant work per station.
        Space: O(1): three integers.
        """
        n = len(gas)
        total = 0
        tank = 0
        start = 0
        for i in range(n):
            gain = gas[i] - cost[i]
            total += gain
            tank += gain
            if tank < 0:
                start = i + 1
                tank = 0
        return start if total >= 0 else -1


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().canCompleteCircuit(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
