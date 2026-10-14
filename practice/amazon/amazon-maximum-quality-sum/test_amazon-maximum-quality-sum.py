"""Tests for Maximum Quality Sum — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-maximum-quality-sum.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                1,
                2,
                3,
                4,
                5,
            ],
            2,
        ],
        "expected": 8,
    },
    {
        "id": 'example_2',
        "args": [
            [
                2,
                2,
                1,
                5,
                3,
            ],
            2,
        ],
        "expected": 7,
    },
    {
        "id": 'example_3',
        "args": [
            [
                89,
                48,
                14,
            ],
            3,
        ],
        "expected": 151,
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
        _check(solution.Solution().maximumQualitySum, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
