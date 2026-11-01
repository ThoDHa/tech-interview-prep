"""Bounded IPv4 Filter — https://www.fastprep.io/problems/amazon-bounded-ipv4-filter

Write-up & approaches: ../../../docs/amazon/amazon-bounded-ipv4-filter.md

Reference implementation of the write-up's recommended Packed Octet
Integer Set pool, presented as the design class behind the page's
judged processIpOperations form. Your own attempt lives in solution.py.

  uv run python amazon/amazon-bounded-ipv4-filter/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-bounded-ipv4-filter/              # run the test sets
"""

from typing import Set

from harness import pick_case

POOL_LIMIT = 128


class IPv4Pool:
    """A pool of at most 128 distinct IPv4 addresses, backed by a set of
    packed 32-bit integers, one machine word per stored record."""

    def __init__(self) -> None:
        """Start with an empty pool.

        Time:  O(1): no records allocated.
        Space: O(1): an empty set.
        """
        self.stored: Set[int] = set()

    @staticmethod
    def _pack(address: str) -> int:
        """Pack a canonical dotted-decimal address into one 32-bit integer.

        Args:
            address: Four canonical octets 0-255 joined by dots, with no
                leading zeros, so the packing is injective.

        Returns:
            The address as `(o1 << 24) | (o2 << 16) | (o3 << 8) | o4`.

        Time:  O(1): four octet parses and three shifts.
        Space: O(1): one integer.
        """
        first_octet, second_octet, third_octet, fourth_octet = (
            int(part) for part in address.split(".")
        )
        return (
            (first_octet << 24)
            | (second_octet << 16)
            | (third_octet << 8)
            | fourth_octet
        )

    def add_ip(self, address: str) -> None:
        """Add the address unless the pool is full; a repeat add is a no-op.

        The single capacity guard implements both statement rules: when
        the pool holds fewer than 128 addresses the set-add either
        inserts a new record or leaves a present one unchanged, and a
        full pool ignores the request without evicting anything.

        Time:  O(1) average: one pack plus one set probe.
        Space: O(1): at most one new record.
        """
        if len(self.stored) < POOL_LIMIT:
            self.stored.add(self._pack(address))

    def remove_ip(self, address: str) -> None:
        """Remove the address if present; removing an absent address
        changes nothing.

        Time:  O(1) average: one pack plus one set probe.
        Space: O(1): one record released on a hit.
        """
        self.stored.discard(self._pack(address))

    def check_ip(self, address: str) -> bool:
        """Report whether the exact address is currently present.

        Time:  O(1) average: one pack plus one set probe.
        Space: O(1).
        """
        return self._pack(address) in self.stored


if __name__ == "__main__":
    # Debug playground: cases.json is empty (design-operation starter), so
    # Example 1's operation sequence stands in.
    pool = IPv4Pool()
    print(pool.check_ip("10.0.0.1"))
    pool.add_ip("10.0.0.1")
    print(pool.check_ip("10.0.0.1"))
    pool.add_ip("10.0.0.1")
    pool.remove_ip("10.0.0.1")
    print(pool.check_ip("10.0.0.1"))
