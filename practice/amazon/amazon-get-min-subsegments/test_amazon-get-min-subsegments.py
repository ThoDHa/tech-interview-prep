"""Tests for Get Min Subsegments — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-get-min-subsegments.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            '1110011000',
        ],
        "expected": 2,
    },
    {
        "id": 'example_2',
        "args": [
            '110011',
        ],
        "expected": 3,
    },
    {
        "id": 'example_3',
        "args": [
            '100110',
        ],
        "expected": 1,
    },
]

if len(CASES) == 0:
    pytest.skip("no cases parsed", allow_module_level=True)

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", CASES, ids=_ids(CASES))
def test_solution(case):
    try:
        _check(solution.Solution().getminSubsegments, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
