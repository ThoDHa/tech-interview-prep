"""Tests for Maximum Frequency Stack: your attempt (solution.py) against both case sets.

Each case is a LeetCode design-operation sequence (operations + arguments) that
is replayed against your FreqStack via run_operations. cases.json (marker `simple`)
is the "Run" set; cases_full.json (marker `full`) is the "Submit" gauntlet. The
worked approaches live in ../../docs/problems/maximum_frequency_stack.md.
"""

import pytest

from harness import NotSolved, load_cases, load_solution, run_operations

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(cls, case):
    result = run_operations(cls, case["operations"], case["arguments"])
    assert result == case["expected"]


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    try:
        _check(solution.FreqStack, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(solution.FreqStack, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
