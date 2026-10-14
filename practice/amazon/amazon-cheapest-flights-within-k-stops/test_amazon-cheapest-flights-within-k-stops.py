"""Tests for Cheapest Flights Within K Stops — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-cheapest-flights-within-k-stops.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            4,
            [
                [
                    0,
                    1,
                    100,
                ],
                [
                    1,
                    2,
                    100,
                ],
                [
                    2,
                    0,
                    100,
                ],
                [
                    1,
                    3,
                    600,
                ],
                [
                    2,
                    3,
                    200,
                ],
            ],
            0,
            3,
            1,
        ],
        "expected": 700,
    },
    {
        "id": 'example_2',
        "args": [
            3,
            [
                [
                    0,
                    1,
                    100,
                ],
                [
                    1,
                    2,
                    100,
                ],
                [
                    0,
                    2,
                    500,
                ],
            ],
            0,
            2,
            1,
        ],
        "expected": 200,
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
        _check(solution.Solution().findCheapestPrice, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
