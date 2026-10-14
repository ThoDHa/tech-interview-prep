"""Tests for Cousins in Binary Tree II — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-cousins-in-binary-tree-ii.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                '5',
                '4',
                '9',
                '1',
                '10',
                'null',
                '7',
            ],
        ],
        "expected": [
            '0',
            '0',
            '0',
            '7',
            '7',
            'null',
            '11',
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                '3',
                '1',
                '2',
            ],
        ],
        "expected": [
            '0',
            '0',
            '0',
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                '1',
                '2',
                '3',
                '4',
                'null',
                '5',
                '6',
            ],
        ],
        "expected": [
            '0',
            '0',
            '0',
            '11',
            'null',
            '4',
            '4',
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
        _check(solution.Solution().replaceValueInTree, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
