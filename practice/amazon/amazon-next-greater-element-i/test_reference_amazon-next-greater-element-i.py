"""Reference-parametrized gauntlet for Next Greater Element I.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Monotonic Stack reference against cases_full.json. Every expectation in
cases_full.json is oracle-derived, never hand-computed and never
recorded from this reference: the oracle locates each query value's
position in reference and scans right for the first strictly greater
value, the statement's literal definition, with no stack and no
precompute pass. The gauntlet covers the statement's named corners:
query.length = 1 and query.length = reference.length (both length
bounds), distinct values, every query value present in reference, plus
scrambled query order, descending reference (every answer -1),
ascending reference (only the last missing), signed extreme magnitudes,
randomized mixed shapes, and two randomized cases at the statement's
reference-length upper bound of 100000 (one with 2000 queries, one with
100000, the query-length bound). The output is a deterministic list aligned with query order,
so the comparison is plain `==` with no canonicalization.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().nextGreaterElement, case)
