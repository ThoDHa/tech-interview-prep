"""Tests for Combination Sum: your attempt (solution.py) against both case sets.

cases.json (marker `simple`) is the "Run" set; cases_full.json (marker `full`) is
the "Submit" gauntlet. The worked approaches live in ../../docs/problems/combination_sum.md.
"""

import pytest

from harness import NotSolved, load_cases, load_solution

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _canonical(combinations):
    # Order of combinations and order within each combination are both irrelevant.
    return sorted(sorted(combo) for combo in combinations)


def _check(method, case):
    assert _canonical(method(*case["args"])) == _canonical(case["expected"])


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    try:
        _check(solution.Solution().combinationSum, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(solution.Solution().combinationSum, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
