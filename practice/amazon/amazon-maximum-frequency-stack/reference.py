"""Maximum Frequency Stack — https://www.fastprep.io/problems/amazon-maximum-frequency-stack

Write-up & approaches: ../../../docs/amazon/amazon-maximum-frequency-stack.md
Reference implementation of the write-up's recommended Stack of Stacks
solution, kept next to the harness so authored cases stay falsifiable.
Your own attempt lives in solution.py.
"""

from typing import Dict, List


class FreqStack:
    def __init__(self) -> None:
        """Start with no counts, no buckets, and a zeroed max frequency.

        Time:  O(1): two empty maps and a zero.
        Space: O(1): nothing stored yet.
        """
        self.freq_count: Dict[int, int] = {}
        self.freq_buckets: Dict[int, List[int]] = {}
        self.max_freq = 0

    def push(self, value: int) -> None:
        """File `value` under its new frequency; the LIFO order inside
        each bucket encodes the recency tie-break.

        Time:  O(1): one hash increment and one list append.
        Space: O(1) per call: one entry retained in exactly one bucket.
        """
        self.freq_count[value] = self.freq_count.get(value, 0) + 1
        frequency = self.freq_count[value]
        if frequency > self.max_freq:
            self.max_freq = frequency
        self.freq_buckets.setdefault(frequency, []).append(value)

    def pop(self) -> int:
        """Remove and return the value with the highest current frequency,
        breaking ties toward the most recently pushed, and drop
        `max_freq` by one only when the emptied bucket proves no value
        remains at that frequency.

        Time:  O(1): one bucket pop plus constant bookkeeping.
        Space: O(1): no retained state beyond the shrinking buckets.
        """
        value = self.freq_buckets[self.max_freq].pop()
        self.freq_count[value] -= 1
        if not self.freq_buckets[self.max_freq]:
            self.max_freq -= 1
        return value


if __name__ == "__main__":
    # Debug playground: cases.json is empty (design-operation starter), so
    # Example 1's operation sequence stands in.
    stack = FreqStack()
    for value in (5, 7, 5, 7, 4, 5):
        stack.push(value)
    print([stack.pop() for _ in range(4)])
