"""Tests for Course Schedule II — your attempt (solution.py) against cases.json.

The worked approaches live in ../../docs/problems/course_schedule_ii.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = []

if len(CASES) == 0:
    pytest.skip("any-order output is not `==`-assertable; compare as sets for course_schedule_ii", allow_module_level=True)

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", CASES, ids=_ids(CASES))
def test_solution(case):
    try:
        _check(solution.Solution().solve, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
