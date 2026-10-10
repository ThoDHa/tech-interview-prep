"""Tests for Lowest Common Ancestor in an Inserted BST — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-bst-lowest-common-ancestor.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                6,
                2,
                8,
                0,
                4,
                7,
                9,
                3,
                5,
            ],
            2,
            8,
        ],
        "expected": 6,
    },
    {
        "id": 'example_2',
        "args": [
            [
                6,
                2,
                8,
                0,
                4,
                7,
                9,
                3,
                5,
            ],
            2,
            4,
        ],
        "expected": 2,
    },
    {
        "id": 'example_3',
        "args": [
            [
                5,
            ],
            5,
            5,
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
        _check(solution.Solution().bstLowestCommonAncestor, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
