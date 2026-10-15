"""Reference-parametrized gauntlet for Set Matrix Zeroes.

set_matrix_zeroes's generator-emitted test module carries a module-level
skip (in-place mutation return is not `==`-assertable), so the sanctioned
reference class cannot live there without being skipped alongside it. This
file holds only the reference class: the generator-emitted test module
stays byte-identical, and cases_full.json stays falsifiable.

Every expectation in cases_full.json is oracle-derived: it is the
reference's own post-call snapshot of a deep-copied input, never a
hand-computed grid. The comparator re-applies that discipline by mutating
a private copy and comparing the serialize-after-mutate snapshot against
`expected`, so one case file serves any in-place attempt.
"""

import copy

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


def _zeroed_matrix(method, matrix):
    matrix_copy = copy.deepcopy(matrix)
    assert method(matrix_copy) is None
    return matrix_copy


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    assert _zeroed_matrix(reference.Solution().setZeroes, case["args"][0]) == case["expected"]
