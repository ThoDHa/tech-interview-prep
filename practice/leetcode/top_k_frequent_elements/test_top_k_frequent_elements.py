"""Tests for Top K Frequent Elements: your attempt (solution.py) against both case sets.

The worked approaches live in ../../../docs/leetcode/top_k_frequent_elements.md.

Ties in frequency make any specific element choice non-obligatory, so
both the returned elements and the expected elements are mapped to their
own frequencies and compared as sorted multisets, after pinning the slot
count and distinctness; a wrong frequency ranking or a wrong k still
fails. Ported from test_reference_top_k_frequent_elements.py.
"""

import pytest

from harness import NotSolved, load_cases, load_solution

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


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
    # Elements tied in frequency may be returned in any order.
    frequencies = _frequencies(case["args"][0])
    assert _returned_frequencies(method, case) == sorted(
        frequencies[number] for number in case["expected"]
    )


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    try:
        _check(solution.Solution().solve, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(solution.Solution().solve, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
