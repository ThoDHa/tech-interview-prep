"""Reference-parametrized gauntlet for Top K Frequent Elements.

Ties in frequency make any specific returned multiset non-obligatory, so
the expectation is the oracle's top-k frequency multiset (the k largest
counts, order-free) written sorted in cases_full.json, and the returned
elements are mapped to their own frequencies and sorted before the
comparison. The gauntlet is therefore tie-aware: every case is checkable
regardless of which value the implementation picks within a tie, and a
wrong frequency ranking or a wrong k still fails.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


def _returned_frequencies(method, case):
    numbers, slot_count = case["args"]
    counts = {}
    for number in numbers:
        counts[number] = counts.get(number, 0) + 1
    returned = method(numbers, slot_count)
    assert len(returned) == slot_count and len(set(returned)) == slot_count
    return sorted(counts[number] for number in returned)


def _check(method, case):
    assert _returned_frequencies(method, case) == sorted(case["expected"])


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().topKFrequent, case)
