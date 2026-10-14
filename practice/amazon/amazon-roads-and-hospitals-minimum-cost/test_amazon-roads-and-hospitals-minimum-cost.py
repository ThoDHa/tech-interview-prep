"""Tests for Minimum Cost for Roads and Hospitals — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-roads-and-hospitals-minimum-cost.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            3,
            [
                [
                    0,
                    1,
                ],
                [
                    1,
                    2,
                ],
            ],
            3,
            2,
        ],
        "expected": 7,
    },
    {
        "id": 'example_2',
        "args": [
            3,
            [
                [
                    0,
                    1,
                ],
            ],
            2,
            5,
        ],
        "expected": 6,
    },
    {
        "id": 'example_3',
        "args": [
            5,
            [
                [
                    0,
                    1,
                ],
                [
                    2,
                    3,
                ],
            ],
            6,
            1,
        ],
        "expected": 20,
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
        _check(solution.Solution().minimumInfrastructureCost, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
