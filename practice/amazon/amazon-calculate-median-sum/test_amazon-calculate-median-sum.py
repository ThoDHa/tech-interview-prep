"""Tests for Channel Max Quality — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-calculate-median-sum.md.
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
                5,
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
        _check(solution.Solution().calculateMedianSum, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
