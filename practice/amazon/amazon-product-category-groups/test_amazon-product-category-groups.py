"""Tests for Product Category Group Sizes — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-product-category-groups.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                'A',
                'B',
                'C',
                'D',
                'E',
            ],
            [
                [
                    'A',
                    'B',
                ],
                [
                    'B',
                    'C',
                ],
                [
                    'D',
                    'E',
                ],
            ],
        ],
        "expected": [
            2,
            3,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                'p1',
                'p2',
                'p3',
                'p4',
            ],
            [
                [
                    'p1',
                    'p2',
                ],
            ],
        ],
        "expected": [
            1,
            1,
            2,
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
        _check(solution.Solution().productCategoryGroupSizes, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
