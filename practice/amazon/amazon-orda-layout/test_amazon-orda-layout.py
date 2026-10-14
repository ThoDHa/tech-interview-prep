"""Tests for Ordered Confirguration — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-orda-layout.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            '0001LAJ5KBX9H8|0003UKURNK403F|0002MO6K1Z9WFA|0004OWRXZFMS2C',
        ],
        "expected": [
            'LAJ5KBX9H8',
            'MO6K1Z9WFA',
            'UKURNK403F',
            'OWRXZFMS2C',
        ],
    },
    {
        "id": 'example_2',
        "args": [
            '000533B8XLD2EZ|0001DJ2M2JBZZR|0002Y9YK0A7MYO|0004IKDJCAPG5Q|0003IBHMH59SBO',
        ],
        "expected": [
            'DJ2M2JBZZR',
            'Y9YK0A7MYO',
            'IBHMH59SBO',
            'IKDJCAPG5Q',
            '33B8XLD2EZ',
        ],
    },
    {
        "id": 'example_3',
        "args": [
            '0002f7c22e7904|000176a3a4d214|000305d29f4a4b',
        ],
        "expected": [
            '76a3a4d214',
            'f7c22e7904',
            '05d29f4a4b',
        ],
    },
    {
        "id": 'example_4',
        "args": [
            '0002f7c22e7904|000176a3a4d214|000205d29f4a4b',
        ],
        "expected": [
            'Invalid configuration',
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
        _check(solution.Solution().ordaLayout, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
