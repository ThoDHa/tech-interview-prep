"""Tests for Calculate Total Distrance Travelled — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-calculate-total-distance-travelled.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                0,
                2,
                5,
                9,
                12,
                18,
            ],
            [
                [
                    2,
                    5,
                ],
                [
                    1,
                    3,
                ],
            ],
        ],
        "expected": [
            12,
            18,
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
        _check(solution.Solution().calculateTotalDistanceTravelled, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
