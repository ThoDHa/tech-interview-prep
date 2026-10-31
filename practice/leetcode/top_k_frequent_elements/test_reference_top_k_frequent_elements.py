"""Reference-parametrized gauntlet for Top K Frequent Elements.

cases_full.json stores the expected answer as the k elements themselves
in sorted order, matching the solution gauntlet's encoding. Ties in
frequency make any specific element choice non-obligatory, so both the
returned elements and the expected elements are mapped to their own
frequencies and compared as sorted multisets. The gauntlet stays
tie-aware: every case is checkable regardless of which value the
implementation picks within a tie, and a wrong frequency ranking or a
wrong k still fails.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


def _frequencies(numbers):
    counts = {}
    for number in numbers:
        counts[number] = counts.get(number, 0) + 1
    return counts


def _returned_frequencies(method, case):
    numbers, slot_count = case["args"]
    returned = method(numbers, slot_count)
    assert len(returned) == slot_count and len(set(returned)) == slot_count
    return sorted(_frequencies(numbers)[number] for number in returned)


def _check(method, case):
    frequencies = _frequencies(case["args"][0])
    assert _returned_frequencies(method, case) == sorted(
        frequencies[number] for number in case["expected"]
    )


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().topKFrequent, case)
