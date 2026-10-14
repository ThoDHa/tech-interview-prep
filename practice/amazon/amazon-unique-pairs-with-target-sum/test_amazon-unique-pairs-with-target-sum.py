"""Tests for Unique Pairs With Target Sum — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-unique-pairs-with-target-sum.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            '8 5\n1 4 2 3 3 2 0 5',
        ],
        "expected": [
            '0,5',
            '1,4',
            '2,3',
        ],
    },
    {
        "id": 'example_2',
        "args": [
            '4 10\n1 2 3 4',
        ],
        "expected": [
            'None',
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
        _check(solution.Solution().solveUniquePairsWithTargetSum, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
