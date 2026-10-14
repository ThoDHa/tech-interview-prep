"""Tests for K Closest Points to Origin: your attempt (solution.py) against both sets.

cases.json (marker `simple`) is the "Run" set; cases_full.json (marker `full`) is
the "Submit" gauntlet. The worked approaches live in
../../docs/problems/k_closest_points_to_origin.md.
"""

import pytest

from harness import NotSolved, load_cases, load_solution

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _canonical(points):
    # Answer order is not fixed, but each point [x, y] must stay intact.
    return sorted(map(list, points))


def _check(method, case):
    result = method(*case["args"])
    assert _canonical(result) == _canonical(case["expected"])


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    try:
        _check(solution.Solution().kClosest, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(solution.Solution().kClosest, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
