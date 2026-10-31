"""Tests for Connect N Ropes With Minimum Cost — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-connect-ropes-minimum-cost.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                4,
                3,
                2,
                6,
            ],
        ],
        "expected": 29,
    },
    {
        "id": 'example_2',
        "args": [
            [
                4,
                2,
                7,
                6,
                9,
            ],
        ],
        "expected": 62,
    },
    {
        "id": 'example_3',
        "args": [
            [
                10,
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
        _check(solution.Solution().minimumRopeConnectionCost, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
