"""Tests for Perform Queries — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-perform-queries.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                [
                    'INSERT',
                    'GT23513413',
                ],
                [
                    'INSERT',
                    'TQC2451340',
                ],
                [
                    'SHIP',
                    '-',
                ],
                [
                    'INSERT',
                    'VYP8561991',
                ],
                [
                    'SHIP',
                    '-',
                ],
            ],
        ],
        "expected": [
            [
                'N/ A',
            ],
            [
                'GT23513413',
                'TQC2451340',
                'VYP8561991',
            ],
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
        _check(solution.Solution().performQueries, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
