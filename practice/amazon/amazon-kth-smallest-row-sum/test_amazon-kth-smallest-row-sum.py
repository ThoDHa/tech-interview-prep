"""Tests for Kth Smallest Sum from Sorted Matrix Rows — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-kth-smallest-row-sum.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                [
                    1,
                    3,
                    11,
                ],
                [
                    2,
                    4,
                    6,
                ],
            ],
            5,
        ],
        "expected": 7,
    },
    {
        "id": 'example_2',
        "args": [
            [
                [
                    1,
                    3,
                    11,
                ],
                [
                    2,
                    4,
                    6,
                ],
            ],
            9,
        ],
        "expected": 17,
    },
    {
        "id": 'example_3',
        "args": [
            [
                [
                    1,
                    10,
                    10,
                ],
                [
                    1,
                    4,
                    5,
                ],
                [
                    2,
                    3,
                    6,
                ],
            ],
            7,
        ],
        "expected": 9,
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
        _check(solution.Solution().kthSmallestRowSum, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
