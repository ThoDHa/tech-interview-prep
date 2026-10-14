"""Tests for Vertical Order Traversal of a Binary Tree — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-vertical-order-traversal-of-binary-tree.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                '3',
                '9',
                '20',
                'null',
                'null',
                '15',
                '7',
            ],
        ],
        "expected": [
            [
                9,
            ],
            [
                3,
                15,
            ],
            [
                20,
            ],
            [
                7,
            ],
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                '1',
                '2',
                '3',
                '4',
                '6',
                '5',
                '7',
            ],
        ],
        "expected": [
            [
                4,
            ],
            [
                2,
            ],
            [
                1,
                6,
                5,
            ],
            [
                3,
            ],
            [
                7,
            ],
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [],
        ],
        "expected": [],
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
        _check(solution.Solution().verticalOrder, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
