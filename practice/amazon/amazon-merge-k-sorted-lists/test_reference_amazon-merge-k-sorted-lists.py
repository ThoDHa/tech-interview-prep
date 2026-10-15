"""Reference-parametrized gauntlet for Merge k Sorted Lists.

The generator-emitted test module carries a module-level skip (the
starter is not a single `==`-assertable call), so the sanctioned
reference class lives here instead: the generated module stays
byte-identical and cases_full.json stays falsifiable. Every expectation
in cases_full.json is oracle-derived: recorded from the write-up's
Repeated Minimum Scan, an implementation independent of this
reference's divide-and-conquer pairing. Values are asserted in exact
merged order; ties between equal values follow the write-up's stable
convention in both implementations.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    from harness import build_linked_list, linked_list_to_list

    heads = [build_linked_list(values) for values in case["args"][0]]
    got = linked_list_to_list(reference.Solution().mergeKLists(heads))
    assert got == case["expected"]
