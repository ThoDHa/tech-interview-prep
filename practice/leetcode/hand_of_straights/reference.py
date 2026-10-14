"""Hand of Straights — https://leetcode.com/problems/hand-of-straights/

Write-up & approaches: ../../docs/problems/hand_of_straights.md
Reference implementation of the write-up's Greedy solution, kept next to the
harness so authored cases stay falsifiable. Your own attempt lives in
solution.py.

  uv run python hand_of_straights/reference.py   # replay the example cases
  uv run pytest hand_of_straights/               # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        """Return whether the hand tiles into consecutive-size groups.

        Time:  O(n log n): counting is O(n), sorting distinct values is
            O(n log n), and the run-opening sweep is linear overall.
        Space: O(n): the frequency map holds one entry per distinct value.
        """
        if len(hand) % groupSize != 0:
            return False
        count = {}
        for card in hand:
            count[card] = count.get(card, 0) + 1
        for card in sorted(count):
            runs = count[card]
            if runs == 0:
                continue
            for value in range(card + 1, card + groupSize):
                if count.get(value, 0) < runs:
                    return False
                count[value] -= runs
            count[card] = 0
        return True


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().isNStraightHand(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
