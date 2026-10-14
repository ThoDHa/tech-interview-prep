"""Tests for Product of Array Except Self — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-product-array-except-self.md.
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
            ],
        ],
        "expected": [
            24,
            12,
            8,
            6,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                -1,
                1,
                0,
                -3,
                3,
            ],
        ],
        "expected": [
            0,
            0,
            9,
            0,
            0,
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                2,
                3,
            ],
        ],
        "expected": [
            3,
            2,
        ],
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
        _check(solution.Solution().productExceptSelf, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
