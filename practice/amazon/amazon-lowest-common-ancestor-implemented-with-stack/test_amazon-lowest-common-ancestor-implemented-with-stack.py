"""Tests for Lowest Common Ancestor Implemented with Stack — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-lowest-common-ancestor-implemented-with-stack.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                '10',
                '5',
                '15',
                '3',
                '7',
                '12',
                '18',
                'null',
                '4',
                '6',
                '8',
            ],
            3,
            8,
        ],
        "expected": 5,
    },
    {
        "id": 'example_2',
        "args": [
            [
                '10',
                '5',
                '15',
                '3',
                '7',
                '12',
                '18',
                'null',
                '4',
                '6',
                '8',
            ],
            5,
            8,
        ],
        "expected": 5,
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
        _check(solution.Solution().lowestCommonAncestor, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
