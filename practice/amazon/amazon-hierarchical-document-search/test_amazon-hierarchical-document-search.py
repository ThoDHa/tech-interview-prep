"""Tests for Hierarchical Document Search — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-hierarchical-document-search.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                -1,
                0,
                0,
                1,
                1,
                2,
            ],
            [
                0,
                0,
                0,
                1,
                1,
                1,
            ],
            [
                0,
                0,
                0,
                10,
                30,
                40,
            ],
            [
                '',
                '',
                '',
                'pdf',
                'txt',
                'pdf',
            ],
            0,
            20,
            'pdf',
        ],
        "expected": [
            5,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                -1,
                0,
                0,
                1,
                1,
                2,
            ],
            [
                0,
                0,
                0,
                1,
                1,
                1,
            ],
            [
                0,
                0,
                0,
                10,
                30,
                40,
            ],
            [
                '',
                '',
                '',
                'pdf',
                'txt',
                'pdf',
            ],
            1,
            10,
            '',
        ],
        "expected": [
            4,
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
        _check(solution.Solution().searchDocuments, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
