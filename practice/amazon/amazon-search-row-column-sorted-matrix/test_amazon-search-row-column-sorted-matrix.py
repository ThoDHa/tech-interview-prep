"""Tests for Search a Row and Column Sorted Matrix — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-search-row-column-sorted-matrix.md.
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
                    4,
                    7,
                ],
                [
                    2,
                    5,
                    9,
                ],
                [
                    3,
                    6,
                    12,
                ],
            ],
            6,
        ],
        "expected": True,
    },
    {
        "id": 'example_2',
        "args": [
            [
                [
                    1,
                    4,
                    7,
                ],
                [
                    2,
                    5,
                    9,
                ],
                [
                    3,
                    6,
                    12,
                ],
            ],
            8,
        ],
        "expected": False,
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
        _check(solution.Solution().searchMatrix, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
