"""Tests for Path Through an O/X Grid Using Only Right and Down — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-right-down-grid-path.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                'OOO',
                'OXO',
                'OOO',
            ],
            [
                0,
                0,
            ],
            [
                2,
                2,
            ],
        ],
        "expected": True,
    },
    {
        "id": 'example_2',
        "args": [
            [
                'OX',
                'XO',
            ],
            [
                0,
                0,
            ],
            [
                1,
                1,
            ],
        ],
        "expected": False,
    },
    {
        "id": 'example_3',
        "args": [
            [
                'OOO',
            ],
            [
                0,
                2,
            ],
            [
                0,
                0,
            ],
        ],
        "expected": False,
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
        _check(solution.Solution().hasRightDownPath, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
