"""Tests for Find Median from Data Stream — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-find-median-from-data-stream.md.
"""

import pytest

from harness import load_cases

CASES = load_cases(__file__, "cases.json")


def _ids(cases):
    return [case["id"] for case in cases]


def _assert_design_case_shape(case):
    # A structurally corrupt design gauntlet must fail here rather than skip.
    assert set(case) >= {"id", "operations", "arguments", "expected"}
    assert len(case["operations"]) == len(case["arguments"])


@pytest.mark.parametrize("case", CASES, ids=_ids(CASES))
def test_solution(case):
    _assert_design_case_shape(case)
    pytest.skip("design-operation cases replay against a design class; the starter is not a design class yet")
