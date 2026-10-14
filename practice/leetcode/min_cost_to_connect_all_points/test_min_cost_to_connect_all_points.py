"""Tests for Min Cost to Connect All Points — your attempt (solution.py) against cases.json.

The worked approaches live in ../../docs/problems/min_cost_to_connect_all_points.md.
"""

import pytest

from harness import NotSolved, load_cases, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                [
                    0,
                    0,
                ],
                [
                    2,
                    2,
                ],
                [
                    3,
                    3,
                ],
                [
                    2,
                    4,
                ],
                [
                    4,
                    2,
                ],
            ],
        ],
        "expected": 10,
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
        _check(solution.Solution().minCostConnectPoints, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")

FULL = CASES + load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().minCostConnectPoints, case)
