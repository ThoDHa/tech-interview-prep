"""Tests for Course Schedule II: your attempt (solution.py) against both case sets.

The worked approaches live in ../../../docs/leetcode/course_schedule_ii.md.
"""

import pytest

from harness import NotSolved, load_cases, load_solution

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _is_valid_order(order, num_courses, prerequisites):
    if sorted(order) != list(range(num_courses)):
        return False
    place = {course: position for position, course in enumerate(order)}
    return all(place[before] < place[after] for after, before in prerequisites)


def _check(method, case):
    num_courses, prerequisites = case["args"]
    order = method(*case["args"])
    if case["expected"] == []:
        assert order == []
    else:
        assert order != [] and _is_valid_order(order, num_courses, prerequisites)


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
