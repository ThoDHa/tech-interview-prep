"""Reference-parametrized gauntlet for Bounded IPv4 Filter.

The generator-emitted test module carries a module-level skip (the
design-operation starter is not a single `==`-assertable call), so the
sanctioned design class lives in reference.py and this module replays
it via run_operations; the generated module stays byte-identical. Every
expectation in cases_full.json is oracle-derived, never hand-computed
and never recorded from this reference: the oracle is a naive
definition-model simulation keeping the pool as a plain list of
canonical address strings with linear-scan membership, add guarded by
the scan and the 128-entry limit, and remove deleting on a hit, which
shares no mechanism with the reference's packed-integer set. Mutators
and the constructor expect None; every check_ip expects one boolean, so
run_operations compares the whole expected list per sequence and no
canonicalization applies. The gauntlet covers the statement's named
corners: the page's three examples, the zero-operations input
(represented by the constructor-only sequence; the truly empty input is
a page-API shape covered by the write-up's fence gate, since
run_operations requires at least the constructor operation), empty-pool
checks, duplicate adds, absent removals, all-octet boundary addresses,
exact-match digit neighbors (10.0.0.1 versus 10.0.0.10 versus
1.0.0.10), the 128-entry limit with an ignored overflow add and its
post-removal retry, and randomized add/remove/check interleavings.
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
    _check(reference.IPv4Pool, case)
