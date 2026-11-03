"""Tests for Group Anagrams: your attempt (solution.py) against both case sets.

The worked approaches live in ../../../docs/leetcode/group_anagrams.md.

Group order and within-group word order are free, so both sides are
canonicalized to a sorted multiset of sorted groups before comparison; a
solution that duplicates or drops a whole group fails the multiset.
"""

import pytest

from harness import NotSolved, load_cases, load_solution

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _canonical(groups):
    return sorted(sorted(group) for group in groups)


def _check(method, case):
    # Group order and word order within a group are both arbitrary.
    assert _canonical(method(*case["args"])) == _canonical(case["expected"])


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
