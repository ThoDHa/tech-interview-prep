"""Tests for Reconstruct Itinerary — your attempt (solution.py) against cases.json.

The worked approaches live in ../../docs/problems/reconstruct_itinerary.md.
"""

import pytest

from harness import NotSolved, load_cases, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                [
                    'BUF',
                    'HOU',
                ],
                [
                    'HOU',
                    'SEA',
                ],
                [
                    'JFK',
                    'BUF',
                ],
            ],
        ],
        "expected": [
            'JFK',
            'BUF',
            'HOU',
            'SEA',
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                [
                    'HOU',
                    'JFK',
                ],
                [
                    'SEA',
                    'JFK',
                ],
                [
                    'JFK',
                    'SEA',
                ],
                [
                    'JFK',
                    'HOU',
                ],
            ],
        ],
        "expected": [
            'JFK',
            'HOU',
            'JFK',
            'SEA',
            'JFK',
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
        _check(solution.Solution().findItinerary, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")

FULL = CASES + load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().findItinerary, case)
