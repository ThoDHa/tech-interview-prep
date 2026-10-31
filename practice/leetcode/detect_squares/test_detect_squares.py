"""Tests for Detect Squares — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/leetcode/detect_squares.md.
"""

import pytest

from harness import load_cases

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")


def _ids(cases):
    return [case["id"] for case in cases]


def _assert_design_case_shape(case):
    # A structurally corrupt design gauntlet must fail here rather than skip.
    assert set(case) >= {"id", "operations", "arguments", "expected"}
    assert len(case["operations"]) == len(case["arguments"])


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    _assert_design_case_shape(case)
    pytest.skip("design-operation cases replay against a design class; the starter is not a design class yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    _assert_design_case_shape(case)
    pytest.skip("design-operation cases replay against a design class; the starter is not a design class yet")
