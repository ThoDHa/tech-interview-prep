"""Reference-parametrized gauntlet for Same Tree.

The generator-emitted test module carries a module-level skip (the
starter is not a single `==`-assertable call), so the sanctioned
reference class lives here instead: the generated module stays
byte-identical and cases_full.json stays falsifiable. Every expectation
in cases_full.json is oracle-derived: it is this reference's own output
on the marshalled input, recorded once by the gauntlet authoring pass,
never hand-computed.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    from harness import build_tree

    got = reference.Solution().isSameTree(build_tree(case["args"][0]), build_tree(case["args"][1]))
    assert got == case["expected"]
