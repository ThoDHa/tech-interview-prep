"""Reference-parametrized gauntlet for Encode and Decode Strings.

Expectations in cases_full.json come from an independent oracle, not from
this reference: the encoded form is produced by a literal append loop
writing `str(len(word))`, `#`, then the word itself, and each decode case
expects the original list back from that exact wire string, so a decoder
that misreads digits, hashes, or payload boundaries fails on the adversarial
payloads (hashes, digit-looking prefixes, empty strings). Both directions
are exact string/list comparisons driven by `run_operations`.
"""

import pytest

from harness import load_cases, load_solution, run_operations

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


def _check(design_class, case):
    result = run_operations(design_class, case["operations"], case["arguments"])
    assert result == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution, case)
