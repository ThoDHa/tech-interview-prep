"""Tests for Valid Sudoku — your attempt (solution.py) against cases.json.

The worked approaches live in ../../docs/problems/valid_sudoku.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                [
                    '1',
                    '2',
                    '.',
                    '.',
                    '3',
                    '.',
                    '.',
                    '.',
                    '.',
                ],
                [
                    '4',
                    '.',
                    '.',
                    '5',
                    '.',
                    '.',
                    '.',
                    '.',
                    '.',
                ],
                [
                    '.',
                    '9',
                    '8',
                    '.',
                    '.',
                    '.',
                    '.',
                    '.',
                    '3',
                ],
                [
                    '5',
                    '.',
                    '.',
                    '.',
                    '6',
                    '.',
                    '.',
                    '.',
                    '4',
                ],
                [
                    '.',
                    '.',
                    '.',
                    '8',
                    '.',
                    '3',
                    '.',
                    '.',
                    '5',
                ],
                [
                    '7',
                    '.',
                    '.',
                    '.',
                    '2',
                    '.',
                    '.',
                    '.',
                    '6',
                ],
                [
                    '.',
                    '.',
                    '.',
                    '.',
                    '.',
                    '.',
                    '2',
                    '.',
                    '.',
                ],
                [
                    '.',
                    '.',
                    '.',
                    '4',
                    '1',
                    '9',
                    '.',
                    '.',
                    '8',
                ],
                [
                    '.',
                    '.',
                    '.',
                    '.',
                    '8',
                    '.',
                    '.',
                    '7',
                    '9',
                ],
            ],
        ],
        "expected": True,
    },
    {
        "id": 'example_2',
        "args": [
            [
                [
                    '1',
                    '2',
                    '.',
                    '.',
                    '3',
                    '.',
                    '.',
                    '.',
                    '.',
                ],
                [
                    '4',
                    '.',
                    '.',
                    '5',
                    '.',
                    '.',
                    '.',
                    '.',
                    '.',
                ],
                [
                    '.',
                    '9',
                    '1',
                    '.',
                    '.',
                    '.',
                    '.',
                    '.',
                    '3',
                ],
                [
                    '5',
                    '.',
                    '.',
                    '.',
                    '6',
                    '.',
                    '.',
                    '.',
                    '4',
                ],
                [
                    '.',
                    '.',
                    '.',
                    '8',
                    '.',
                    '3',
                    '.',
                    '.',
                    '5',
                ],
                [
                    '7',
                    '.',
                    '.',
                    '.',
                    '2',
                    '.',
                    '.',
                    '.',
                    '6',
                ],
                [
                    '.',
                    '.',
                    '.',
                    '.',
                    '.',
                    '.',
                    '2',
                    '.',
                    '.',
                ],
                [
                    '.',
                    '.',
                    '.',
                    '4',
                    '1',
                    '9',
                    '.',
                    '.',
                    '8',
                ],
                [
                    '.',
                    '.',
                    '.',
                    '.',
                    '8',
                    '.',
                    '.',
                    '7',
                    '9',
                ],
            ],
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
        _check(solution.Solution().isValidSudoku, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
