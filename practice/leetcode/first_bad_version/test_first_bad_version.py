"""Tests for First Bad Version: your attempt (solution.py) against both sets.

This is an api-callback problem: Solution.firstBadVersion(n) calls the module-level
isBadVersion(version). Each case is {args: [n, bad], expected: first_bad}; before
calling the solution we point solution.bad at the case's bad version so that
isBadVersion(v) returns v >= bad. The worked approaches live in
../../docs/problems/first_bad_version.md.
"""

import pytest

from harness import NotSolved, load_cases, load_solution

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(case):
    n, bad = case["args"]
    solution.bad = bad
    assert solution.Solution().firstBadVersion(n) == case["expected"]


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    try:
        _check(case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
