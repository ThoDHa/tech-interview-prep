"""Tests for Longest Content Window with Bounded Labels — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-streaming-content-label-window.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                [
                    'toxic',
                    'ok',
                ],
                [
                    'toxic',
                    'ok',
                    'spam',
                ],
            ],
            2,
        ],
        "expected": [
            0,
            0,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                [
                    'toxic',
                    'ok',
                ],
                [
                    'toxic',
                    'ok',
                    'spam',
                ],
            ],
            3,
        ],
        "expected": [
            0,
            1,
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                [
                    'a',
                ],
                [
                    'b',
                    'c',
                ],
                [
                    'a',
                    'b',
                ],
                [
                    'd',
                ],
            ],
            3,
        ],
        "expected": [
            0,
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
        _check(solution.Solution().longestContentWindow, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
