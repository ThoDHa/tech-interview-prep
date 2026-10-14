"""Tests for Remove K Digits — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-remove-k-digits.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            '1432219',
            3,
        ],
        "expected": '1219',
    },
    {
        "id": 'example_2',
        "args": [
            '10200',
            1,
        ],
        "expected": '200',
    },
    {
        "id": 'example_3',
        "args": [
            '10',
            2,
        ],
        "expected": '0',
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
        _check(solution.Solution().removeKdigits, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
