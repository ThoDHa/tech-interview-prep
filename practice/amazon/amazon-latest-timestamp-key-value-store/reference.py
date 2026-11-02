"""Latest-Timestamp Key-Value Store — https://www.fastprep.io/problems/amazon-latest-timestamp-key-value-store

Write-up & approaches: ../../../docs/amazon/amazon-latest-timestamp-key-value-store.md

Reference implementation of the write-up's recommended Latest-Write
Winner Map solution, presented as the design class behind the page's
judged latestTimestampValues form. Your own attempt lives in solution.py.

  uv run python amazon/amazon-latest-timestamp-key-value-store/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-latest-timestamp-key-value-store/              # run the test sets
"""

from typing import Dict, Tuple


class LatestTimestampStore:
    """A key-value store that answers every get with the greatest-
    timestamp value, the later set winning a timestamp tie.

    There is no eviction, expiration, capacity limit, or historical
    timestamp query, so one winner entry per key is the entire state.
    """

    def __init__(self) -> None:
        """Start with an empty winner map.

        Time:  O(1): no entries allocated.
        Space: O(1): the map grows only as keys arrive.
        """
        self.winners: Dict[str, Tuple[int, str]] = {}

    def set(self, timestamp: int, key: str, value: str) -> None:
        """Record a candidate for the key, replacing the stored winner
        when the candidate's timestamp is greater, or equal: an equal
        timestamp is the later set in the sequence, which the tie rule
        favors.

        Time:  O(1) average: one dict probe.
        Space: O(1) per call: at most one winner entry stored.
        """
        if key not in self.winners or timestamp >= self.winners[key][0]:
            self.winners[key] = (timestamp, value)

    def get(self, key: str) -> str:
        """Return the stored winner's value, or the empty string when the
        key has never been set.

        Time:  O(1) average: one dict probe.
        Space: O(1).
        """
        if key not in self.winners:
            return ""
        return self.winners[key][1]


if __name__ == "__main__":
    # Debug playground: cases.json is empty (design-operation starter), so
    # Example 1's operation sequence stands in.
    store = LatestTimestampStore()
    store.set(10, "a", "newer")
    store.set(3, "a", "older")
    print(store.get("a"))
    store.set(10, "a", "tie")
    print(store.get("a"))
    store.set(12, "a", "newest")
    print(store.get("a"))
