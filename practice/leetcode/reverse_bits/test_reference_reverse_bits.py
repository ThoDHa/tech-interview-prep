"""Reference-parametrized gauntlet for Reverse Bits.

reverse_bits's generator-emitted test module carries a module-level skip
(example input is not JSON-representable), so the sanctioned reference
class cannot live there without being skipped alongside it. This file
holds only the reference class: the generator-emitted test module stays
byte-identical, and cases_full.json stays falsifiable.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().reverseBits, case)
