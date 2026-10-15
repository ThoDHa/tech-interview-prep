"""Reference-parametrized gauntlet for Root-to-Leaf Paths with a Target Sum.

The generator-emitted test module carries a module-level skip (the
starter is not a single `==`-assertable call), so the sanctioned
reference class lives here instead: the generated module stays
byte-identical and cases_full.json stays falsifiable. Every expectation
in cases_full.json is oracle-derived: recorded from the write-up's
Copy-per-Node Recursion, an implementation independent of this
reference's shared-path backtracking. Output order is asserted exactly:
left-to-right depth-first, root-first within each path.
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

    got = reference.Solution().pathSum(build_tree(case["args"][0]), case["args"][1])
    assert got == case["expected"]
