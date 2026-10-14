"""Tests for Minimize Variation — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-minimize-variation.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                3,
                1,
                2,
            ],
        ],
        "expected": 3,
    },
    {
        "id": 'example_2',
        "args": [
            [
                6,
                1,
                4,
                2,
            ],
        ],
        "expected": 9,
    },
    {
        "id": 'example_3',
        "args": [
            [
                4,
                5,
                4,
                2,
                6,
                1,
                1,
            ],
        ],
        "expected": 16,
    },
    {
        "id": 'example_4',
        "args": [
            [
                6,
                1,
                4,
                2,
            ],
        ],
        "expected": 9,
    },
    {
        "id": 'example_5',
        "args": [
            [
                3,
                1,
                3,
                3,
                6,
                6,
            ],
        ],
        "expected": 11,
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
        _check(solution.Solution().minimizeVariation, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
