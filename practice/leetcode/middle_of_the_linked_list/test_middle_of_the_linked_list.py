"""Tests for Middle of the Linked List: your attempt (solution.py) against both sets.

Linked lists are stored in the case files as plain value arrays and marshalled to
ListNode here. The result node is serialized back to a list (middle node to end)
for comparison. The worked approaches live in ../../docs/problems/middle_of_the_linked_list.md.
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
    head = build_linked_list(case["args"][0])
    result = method(head)
    assert linked_list_to_list(result) == case["expected"]


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    try:
        _check(solution.Solution().middleNode, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(solution.Solution().middleNode, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
