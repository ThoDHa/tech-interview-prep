"""Tests for Largest Binary-String Subset Within Bit Budgets — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-binary-strings-bounded-subset.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                '100',
                '10',
                '1',
                '11',
                '111',
            ],
            3,
            0,
        ],
        "expected": 2,
    },
    {
        "id": 'example_2',
        "args": [
            [
                '10',
                '0001',
                '111001',
                '1',
                '0',
            ],
            3,
            5,
        ],
        "expected": 4,
    },
    {
        "id": 'example_3',
        "args": [
            [
                '10',
                '0',
                '1',
            ],
            1,
            1,
        ],
        "expected": 2,
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
        _check(solution.Solution().largestBoundedSubset, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
