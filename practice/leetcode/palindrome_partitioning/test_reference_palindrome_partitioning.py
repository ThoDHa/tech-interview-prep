"""Reference-parametrized gauntlet for Palindrome Partitioning.

Any-order output is compared with full canonicalized-set equality on both
sides (sorted(map(sorted, ...)), the pin for the six set problems): the
oracle-derived expectation is written canonicalized in cases_full.json, and
the returned partition list is canonicalized the same way before the
comparison, so partition order and piece order within a partition are both
free.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


def _canonical(partitions):
    return sorted(sorted(partition) for partition in partitions)


def _check(method, case):
    assert _canonical(method(*case["args"])) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().partition, case)
