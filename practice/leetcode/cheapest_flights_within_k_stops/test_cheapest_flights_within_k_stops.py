"""Tests for Cheapest Flights Within K Stops — your attempt (solution.py) against cases.json.

The worked approaches live in ../../docs/problems/cheapest_flights_within_k_stops.md.
"""

import pytest

from harness import NotSolved, load_cases, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            4,
            [
                [
                    0,
                    1,
                    200,
                ],
                [
                    1,
                    2,
                    100,
                ],
                [
                    1,
                    3,
                    300,
                ],
                [
                    2,
                    3,
                    100,
                ],
            ],
            0,
            3,
            1,
        ],
        "expected": 500,
    },
    {
        "id": 'example_2',
        "args": [
            3,
            [
                [
                    1,
                    0,
                    100,
                ],
                [
                    1,
                    2,
                    200,
                ],
                [
                    0,
                    2,
                    100,
                ],
            ],
            1,
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

FULL = CASES + load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().findCheapestPrice, case)
