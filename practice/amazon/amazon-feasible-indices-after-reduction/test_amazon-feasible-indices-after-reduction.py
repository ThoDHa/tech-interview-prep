"""Tests for Feasible Indices After Reduction — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-feasible-indices-after-reduction.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                1,
                3,
                2,
                5,
                4,
            ],
        ],
        "expected": '10011',
    },
    {
        "id": 'example_2',
        "args": [
            [
                4,
                1,
                3,
                2,
            ],
        ],
        "expected": '1111',
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
        _check(solution.Solution().feasibleIndicesAfterReduction, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
