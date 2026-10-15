"""Reference-parametrized gauntlet for Reorder List.

Expectations in cases_full.json come from an independent definition oracle,
not from this reference: the reordered sequence is produced by walking the
value list inward from both ends, alternating front and back
(`[0, 1, 2, 3, 4]` becomes `[0, 4, 1, 3, 2]`), which is the problem's
stated interleave order. Values arrive as plain lists in cases_full.json
and are marshalled through the harness `build_linked_list` /
`linked_list_to_list` pair because the reference rewires nodes in place;
the serialized expectation is exact.
"""

import pytest

from harness import build_linked_list, linked_list_to_list, load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


def _check(case):
    head = build_linked_list(case["args"][0])
    assert linked_list_to_list(reference.reorder_list(head)) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(case)
