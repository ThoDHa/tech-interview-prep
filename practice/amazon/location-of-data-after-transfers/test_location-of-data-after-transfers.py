"""Tests for Location of Data After Transfers — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/location-of-data-after-transfers.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                1,
                7,
                6,
                8,
            ],
            [
                1,
                7,
                2,
            ],
            [
                2,
                9,
                5,
            ],
        ],
        "expected": [
            5,
            6,
            8,
            9,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                1,
                5,
                2,
                6,
            ],
            [
                1,
                4,
                5,
                7,
            ],
            [
                4,
                7,
                1,
                3,
            ],
        ],
        "expected": [
            1,
            2,
            3,
            6,
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                1,
                2,
                3,
            ],
            [
                1,
                2,
            ],
            [
                5,
                6,
            ],
        ],
        "expected": [
            3,
            5,
            6,
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
        _check(solution.Solution().locationOfDataAfterTransfers, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
