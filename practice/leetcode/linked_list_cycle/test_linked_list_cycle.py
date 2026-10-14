"""Tests for Linked List Cycle: your attempt (solution.py) against both sets.

Cases store the list as `[values, pos]` (pos = cycle-entry index, -1 = none) and
are marshalled to a possibly cyclic ListNode here; a cyclic list is never
serialized. The worked approaches live in ../../docs/problems/linked_list_cycle.md.
"""

import pytest

from harness import (
    NotSolved,
    build_linked_list_with_cycle,
    load_cases,
    load_solution,
)

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    values, pos = case["args"]
    head = build_linked_list_with_cycle(values, pos)
    assert method(head) == case["expected"]


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    try:
        _check(solution.Solution().hasCycle, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(solution.Solution().hasCycle, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
