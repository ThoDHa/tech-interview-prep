"""Search for an Element in a Stream — https://www.fastprep.io/problems/amazon-search-element-in-stream

Write-up & approaches: ../../../docs/amazon/amazon-search-element-in-stream.md

Reference implementation of the write-up's recommended Value Set
stream, presented as the design class behind the page's judged solve
form. Your own attempt lives in solution.py.

  uv run python amazon/amazon-search-element-in-stream/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-search-element-in-stream/              # run the test sets
"""

from typing import Set

from harness import pick_case


class StreamSearch:
    """Answers membership queries over the values that have already
    arrived, backed by a set, so a repeat arrival is a no-op."""

    def __init__(self) -> None:
        """Start with an empty arrival set.

        Time:  O(1): no records allocated.
        Space: O(1): an empty set.
        """
        self.arrived: Set[int] = set()

    def add(self, value: int) -> None:
        """Record a value's arrival; a repeat arrival changes nothing.

        Time:  O(1) average: one set insert.
        Space: O(1): at most one new record.
        """
        self.arrived.add(value)

    def search(self, value: int) -> bool:
        """Report whether an earlier operation added the value.

        Time:  O(1) average: one set probe.
        Space: O(1).
        """
        return value in self.arrived


if __name__ == "__main__":
    # Debug playground: cases.json is empty (design-operation starter), so
    # Example 1's operation sequence stands in.
    stream = StreamSearch()
    stream.add(5)
    stream.add(3)
    print(stream.search(3))
    print(stream.search(7))
    stream.add(7)
    print(stream.search(7))
