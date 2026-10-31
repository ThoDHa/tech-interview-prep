"""Tests for Number of Islands — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-number-of-islands.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                '11110',
                '11010',
                '11000',
                '00000',
            ],
        ],
        "expected": 1,
    },
    {
        "id": 'example_2',
        "args": [
            [
                '11000',
                '11000',
                '00100',
                '00011',
            ],
        ],
        "expected": 3,
    },
    {
        "id": 'example_3',
        "args": [
            [
                '000',
                '000',
            ],
        ],
        "expected": 0,
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
        _check(solution.Solution().numIslands, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
