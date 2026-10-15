"""Reference-parametrized gauntlet for N Queens.

Correctness-property validation, not membership: each case asserts the
returned board set equals the oracle's complete solution set for that n
(exhaustively enumerated over all n! row permutations), so a board that is
not a solution, a missing solution, or a duplicated board all fail.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert sorted(map(tuple, method(*case["args"]))) == [
        tuple(board) for board in case["expected"]
    ]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().solveNQueens, case)
