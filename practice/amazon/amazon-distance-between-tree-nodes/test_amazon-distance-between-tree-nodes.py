"""Tests for Distance Between Two Tree Nodes — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-distance-between-tree-nodes.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            7,
            [
                1,
                1,
                2,
                2,
                3,
                3,
            ],
            [
                2,
                3,
                4,
                5,
                6,
                7,
            ],
            1,
            4,
            7,
        ],
        "expected": 4,
    },
    {
        "id": 'example_2',
        "args": [
            5,
            [
                1,
                1,
                3,
                3,
            ],
            [
                2,
                3,
                4,
                5,
            ],
            1,
            3,
            5,
        ],
        "expected": 1,
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
        _check(solution.Solution().distanceBetweenNodes, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
