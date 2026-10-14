"""Tests for Closest Version Date — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-closest-version-date.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            '2026-04-01',
            [
                '2023-04-01',
                '2025-04-01',
                '2026-05-03',
            ],
        ],
        "expected": '2026-05-03',
    },
    {
        "id": 'example_2',
        "args": [
            '2024-06-10',
            [
                '2024-06-01',
                '2024-06-20',
                '2024-07-01',
            ],
        ],
        "expected": '2024-06-01',
    },
    {
        "id": 'example_3',
        "args": [
            '2025-01-15',
            [
                '2025-01-10',
                '2025-01-20',
            ],
        ],
        "expected": '2025-01-20',
    },
    {
        "id": 'example_4',
        "args": [
            '2026-04-01',
            [
                '2026-04-01',
                '2026-05-03',
                '2025-12-31',
            ],
        ],
        "expected": '2026-04-01',
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
        _check(solution.Solution().findClosestVersionDate, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
