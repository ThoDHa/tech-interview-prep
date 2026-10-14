"""Tests for Permutations: your attempt (solution.py) against both case sets.

cases.json (marker `simple`) is the "Run" set; cases_full.json (marker `full`) is
the "Submit" gauntlet. The worked approaches live in ../../docs/problems/permutations.md.
"""

import pytest

from harness import NotSolved, load_cases, load_solution

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _canonical(perms):
    # The set of permutations may be returned in any order, but each
    # permutation's internal order is significant, so sort the outer list only.
    return sorted(map(tuple, perms))


def _check(method, case):
    assert _canonical(method(*case["args"])) == _canonical(case["expected"])


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    try:
        _check(solution.Solution().permute, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(solution.Solution().permute, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
