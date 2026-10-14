"""Partition Labels — https://leetcode.com/problems/partition-labels/

Write-up & approaches: ../../docs/problems/partition_labels.md
Reference implementation of the write-up's Last-Occurrence Sweep solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python partition_labels/reference.py   # replay the example cases
  uv run pytest partition_labels/               # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        """Return the sizes of the maximum-count partitions of `s`.

        Time:  O(n): one pass fills the last-occurrence map, one pass sweeps.
        Space: O(1): the map holds at most one entry per lowercase letter.
        """
        last = {}
        for ch, letter in enumerate(s):
            last[letter] = ch

        sizes: List[int] = []
        partition_end = 0
        partition_start = 0
        for ch, letter in enumerate(s):
            partition_end = max(partition_end, last[letter])
            if ch == partition_end:
                sizes.append(ch - partition_start + 1)
                partition_start = ch + 1
        return sizes


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().partitionLabels(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
