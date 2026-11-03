"""Tests for N Queens: your attempt (solution.py) against both case sets.

The worked approaches live in ../../../docs/leetcode/n_queens.md.

Boards may be returned in any order, so both sides are compared as a
sorted multiset of row tuples; a solution that duplicates or drops a
board fails the multiset, while row order inside a board stays exact.
"""

import pytest

from harness import NotSolved, load_cases, load_solution

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    # Solution boards may be returned in any order; each board's rows are significant.
    assert sorted(map(tuple, method(*case["args"]))) == sorted(
        map(tuple, case["expected"])
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
