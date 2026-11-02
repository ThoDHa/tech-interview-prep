"""Reference-parametrized gauntlet for Search for an Element in a Stream.

The generator-emitted test module carries a module-level skip (the
design-operation starter is not a single `==`-assertable call), so the
sanctioned design class lives in reference.py and this module replays
it via run_operations; the generated module stays byte-identical. Every
expectation in cases_full.json is oracle-derived, never hand-computed
and never recorded from this reference: the oracle is a naive
definition-model simulation keeping every arrival in a plain log list
(duplicates included) and answering each search with a linear scan of
the log, the statement's "arrived at an earlier index" read literally,
which shares no mechanism with the reference's set. Adds and the
constructor expect None; every search expects one boolean, so
run_operations compares the whole expected list per sequence and no
canonicalization applies. The no-searches case is the statement's
granted empty contract in this representation: an adds-only stream
returns an empty result array, which the aligned replay records as
every entry None. The gauntlet covers the statement's named
rules as corners: the page's example, a search before any arrival, the
no-searches input (adds only), repeat arrivals changing nothing,
repeated searches across an arrival, a search immediately after its
add, never-added values, the negative/zero/large value domain, and
randomized add/search interleavings.
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
    _check(reference.StreamSearch, case)
