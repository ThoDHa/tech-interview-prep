"""Reference-parametrized gauntlet for Course Schedule II.

Correctness-property validation, not membership: the validator accepts a
returned ordering exactly when it is a permutation of all numCourses
courses in which every prerequisite pair points forward, and it pins []
verbatim for the cyclic cases.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


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


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().findOrder, case)
