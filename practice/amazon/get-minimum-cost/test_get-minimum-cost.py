"""Tests for Get Minimum Costs — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/get-minimum-cost.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                2,
                1,
                1,
            ],
            [
                1,
                2,
                3,
            ],
            4,
        ],
        "expected": 7,
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
        _check(solution.Solution().getMinimumCost, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
