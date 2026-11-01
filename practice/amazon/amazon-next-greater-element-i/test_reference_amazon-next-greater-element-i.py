"""Reference-parametrized gauntlet for Next Greater Element I.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Monotonic Stack reference against cases_full.json plus two constructed
full-size corners. Every expectation in cases_full.json is
oracle-derived, never hand-computed and never recorded from this
reference: the oracle locates each query value's position in reference
and scans right for the first strictly greater value, the statement's
literal definition, with no stack and no precompute pass. The gauntlet
covers the statement's named corners: query.length = 1 and
query.length = reference.length, distinct values, every query value
present in reference, scrambled query order, descending reference
(every answer -1), ascending reference (only the last missing), signed
extreme magnitudes, and randomized mixed shapes, all at eye-auditable
sizes. The output is a deterministic list aligned with query order, so
the comparison is plain `==` with no canonicalization.

The two serialized length corners were converted to constructed cases
per the Testing Strategy rule that length corners are constructible or
synthesized, never serialized bulk. No feasible in-test definition-model
oracle exists for this problem at the 10^5 scale (locate-and-scan is
about 10^10 operations), so both corners take the constructible form:
a reference of consecutive ascending integers 0..bound - 1 whose
expectation follows from its construction. In such a reference the
rightward scan from any value's position meets the remaining larger
values in increasing order, so the first strictly greater value is
always the immediate successor: each answer is the queried value
shifted by one, and only a queried maximum has no successor, answering
-1.

- test_constructed_ascending_reference_at_both_length_bounds_answers_value_shift_by_one:
  reference is 0..99999 and query is the same values in descending
  order, so the reference-length and query-length bounds of 10^5 are
  hit at once. The expected list is the per-element shift by one, with
  -1 for the queried maximum 99999; the descending query order proves
  the answers track value positions, not query positions.
- test_constructed_ascending_reference_mid_scale_interleaved_queries_answer_value_shift_by_one:
  converts the stripped 5000x2000 randomized corner: reference is
  0..4999 and query is the 2000 values v with v % 5 < 2 in descending
  order. No queried value is the maximum (4999 % 5 is 4), so every
  answer is v + 1.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference_module = load_solution(__file__, "reference.py")

ASCENDING_BOUND = 100000
MID_SCALE_REFERENCE_BOUND = 5000
MID_SCALE_QUERY_COUNT = 2000


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference_module.Solution().nextGreaterElement, case)


def test_constructed_ascending_reference_at_both_length_bounds_answers_value_shift_by_one():
    reference = list(range(ASCENDING_BOUND))
    query = list(reversed(reference))
    maximum = ASCENDING_BOUND - 1
    expected = [-1 if value == maximum else value + 1 for value in query]
    assert reference_module.Solution().nextGreaterElement(query, reference) == expected


def test_constructed_ascending_reference_mid_scale_interleaved_queries_answer_value_shift_by_one():
    reference = list(range(MID_SCALE_REFERENCE_BOUND))
    query = [value for value in reversed(reference) if value % 5 < 2]
    assert len(query) == MID_SCALE_QUERY_COUNT
    expected = [value + 1 for value in query]
    assert reference_module.Solution().nextGreaterElement(query, reference) == expected
