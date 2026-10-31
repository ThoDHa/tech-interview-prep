"""Tests for Available Recipes from Initial Supplies — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-available-recipes-from-supplies.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                'bread',
                'sandwich',
            ],
            [
                [
                    'flour',
                    'water',
                ],
                [
                    'bread',
                    'ham',
                ],
            ],
            [
                'flour',
                'water',
                'ham',
            ],
        ],
        "expected": [
            'bread',
            'sandwich',
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                'cake',
                'icing',
                'tea',
            ],
            [
                [
                    'flour',
                    'icing',
                ],
                [
                    'sugar',
                ],
                [
                    'water',
                ],
            ],
            [
                'sugar',
                'water',
            ],
        ],
        "expected": [
            'icing',
            'tea',
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                'meal',
                'base',
            ],
            [
                [
                    'base',
                ],
                [],
            ],
            [],
        ],
        "expected": [
            'meal',
            'base',
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
        _check(solution.Solution().findAvailableRecipes, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
