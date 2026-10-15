"""Reference-parametrized gauntlet for Environment Variable Store and
Substitution.

Expectations in cases_full.json come from an independent definition-model
oracle, not from this reference: the oracle keeps a plain dict and
answers each operation by definition: set stores or overwrites, get
returns the value or None (the harness form of the statement's NULL),
and parse rewrites the text by substituting every complete %KEY%
placeholder whose key exists and leaving every missing placeholder
untouched. The substitution is one pass: values enter the output and are
never re-scanned, so a value containing %OTHER% stays unexpanded. Every
case yields exactly one expected string per non-set operation, and
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
    _check(reference.EnvironmentStore, case)
