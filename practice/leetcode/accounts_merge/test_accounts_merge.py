"""Tests for Accounts Merge: your attempt (solution.py) against both case sets.

cases.json (marker `simple`) is the "Run" set; cases_full.json (marker `full`) is
the "Submit" gauntlet. Answer order is not fixed, so both sides are canonicalized
(emails sorted within each account, then accounts sorted) before comparing. The
worked approaches live in ../../docs/problems/accounts_merge.md.
"""

import pytest

from harness import NotSolved, load_cases, load_solution

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _canon(accounts):
    # Sort emails within each account, then sort the accounts themselves.
    return sorted([acc[0]] + sorted(acc[1:]) for acc in accounts)


def _check(method, case):
    result = method(*case["args"])
    assert _canon(result) == _canon(case["expected"])


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    try:
        _check(solution.Solution().accountsMerge, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(solution.Solution().accountsMerge, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
