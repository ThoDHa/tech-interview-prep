"""Tests for Apply a Reversi Move — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-reversi-move-simulation.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                '....',
                '.WB.',
                '....',
            ],
            1,
            3,
            'W',
        ],
        "expected": [
            '....',
            '.WWW',
            '....',
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                '..B..',
                '..W..',
                'BW.WB',
                '..W..',
                '..B..',
            ],
            2,
            2,
            'B',
        ],
        "expected": [
            '..B..',
            '..B..',
            'BBBBB',
            '..B..',
            '..B..',
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                '...',
                '...',
                '...',
            ],
            1,
            1,
            'B',
        ],
        "expected": [
            '...',
            '...',
            '...',
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
        _check(solution.Solution().applyReversiMove, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
