"""Tests for Merge k Sorted Lists: your attempt (solution.py) against both sets.

Each list is stored in the case files as a plain value array; the array of arrays
is marshalled into a list of ListNodes here. The worked approaches live in
../../docs/problems/merge_k_sorted_lists.md.
"""

import pytest

from harness import (
    NotSolved,
    build_linked_list,
    linked_list_to_list,
    load_cases,
    load_solution,
)

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    lists = [build_linked_list(values) for values in case["args"][0]]
    result = method(lists)
    assert linked_list_to_list(result) == case["expected"]


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    try:
        _check(solution.Solution().mergeKLists, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(solution.Solution().mergeKLists, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
