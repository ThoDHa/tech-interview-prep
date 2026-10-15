"""Reference-parametrized gauntlet for Linked-List Queue with Delete and
Deduplication.

Expectations in cases_full.json come from an independent definition-model
oracle, not from this reference: the oracle models the queue as a plain
Python list, appending on enqueue, popping the front on dequeue, removing
the first matching element on delete (no change when nothing matches),
and rebuilding the list with first occurrences only on
removeAllDuplicates, which is the statement's definition of each
operation. Every case issues a dequeue only while the queue is nonempty,
so each dequeue yields exactly one expected integer and
`run_operations` compares the whole expected result list per operation.
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
    _check(reference.LinkedQueue, case)
