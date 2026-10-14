"""Tests for Optimizing Box Weights — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-minimal-heaviest-set-a.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                5,
                3,
                2,
                4,
                1,
                2,
            ],
        ],
        "expected": [
            4,
            5,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                4,
                2,
                5,
                1,
                6,
            ],
        ],
        "expected": [
            5,
            6,
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                3,
                7,
                5,
                6,
                2,
            ],
        ],
        "expected": [
            6,
            7,
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
        _check(solution.Solution().minimalHeaviestSetA, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
