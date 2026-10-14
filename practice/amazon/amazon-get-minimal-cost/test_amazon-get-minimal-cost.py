"""Tests for Get Minimal Cost — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-get-minimal-cost.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                3,
                7,
                9,
                7,
                8,
            ],
            [
                5,
                2,
                5,
                7,
                5,
            ],
        ],
        "expected": 6,
    },
    {
        "id": 'example_2',
        "args": [
            [
                3,
                3,
                4,
                5,
            ],
            [
                5,
                2,
                2,
                1,
            ],
        ],
        "expected": 5,
    },
    {
        "id": 'example_3',
        "args": [
            [
                2,
                3,
                3,
                2,
            ],
            [
                2,
                4,
                5,
                1,
            ],
        ],
        "expected": 7,
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
        _check(solution.Solution().getMinimalCost, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
