"""Tests for Min Retailers — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-minimum-retailers.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                1,
                3,
                4,
                6,
                9,
            ],
            [
                2,
                8,
                5,
                7,
                10,
            ],
        ],
        "expected": 2,
    },
    {
        "id": 'example_2',
        "args": [
            [
                1,
                2,
                3,
                4,
            ],
            [
                2,
                3,
                5,
                5,
            ],
        ],
        "expected": 1,
    },
    {
        "id": 'example_3',
        "args": [
            [
                1,
                2,
                4,
            ],
            [
                7,
                5,
                6,
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
        _check(solution.Solution().minimumRetailers, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
