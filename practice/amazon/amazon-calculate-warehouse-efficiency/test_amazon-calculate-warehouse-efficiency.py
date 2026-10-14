"""Tests for Calculate Warehouse Efficiency — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-calculate-warehouse-efficiency.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                4,
                4,
                8,
                5,
                3,
                2,
            ],
        ],
        "expected": 17,
    },
    {
        "id": 'example_2',
        "args": [
            [
                2,
                1,
                8,
                5,
                6,
                2,
                4,
            ],
        ],
        "expected": 23,
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
        _check(solution.Solution().calculateWarehouseEfficiency, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
