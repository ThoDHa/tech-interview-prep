"""Reference-parametrized gauntlet for Word Dictionary with Wildcard Find.

The generator-emitted test module carries a module-level skip (the
design-operation starter is not a single `==`-assertable call), so the
sanctioned design class lives in reference.py and this module replays
it via run_operations; the generated module stays byte-identical. Every
expectation in cases_full.json is oracle-derived, never hand-computed
and never recorded from this reference: the oracle is a naive
definition-model simulation keeping every inserted word in a plain list
and answering each find by a linear scan for a word of equal length
whose characters match position by position, which shares no mechanism
with the reference's trie DFS. The constructor and mutators expect
None; every find expects one boolean, so run_operations compares the
whole expected list per sequence and no canonicalization applies.

The gauntlet covers the statement's named corners at eye-auditable
sizes: the page's example, a find on an empty dictionary, single-position
wildcards at every slot, the rule that a period matches exactly one
letter (never zero or two), all-dots patterns, dotless exact finds,
duplicate inserts changing nothing, dots at both pattern boundaries,
one dictionary holding several word lengths, a pattern inserted only
after a failed find, single-letter words, prefixes that are not words
alongside their extensions, interleaved inserts and finds, unstored
letters probed directly, one pattern matching many words, and
same-length rejects. One scale corner lives here as a constructed case
per the Testing Strategy rule that length corners are constructible or
synthesized, never serialized bulk; it builds its dictionary in this
module and derives every expected outcome from the construction:

- test_constructed_complete_alphabet_slice_derives_every_find: every
  word over the letter range a..e of length 1 through 4 is inserted
  (5 + 25 + 125 + 625 = 780 inserts), so a pattern's truth value
  follows from its shape alone: it matches exactly when its length is
  at most 4 and every non-period letter lies in a..e. The probes cover
  each length boundary, dotless and all-dots patterns, a letter outside
  the range at the first and last position, and the length-5 rejection
  that no insert can ever satisfy.
"""

import itertools

import pytest

from harness import load_cases, load_solution, run_operations

FULL = load_cases(__file__, "cases_full.json")

reference_module = load_solution(__file__, "reference.py")

ALPHABET_SLICE = "abcde"
ALPHABET_MAX_LENGTH = 4


def _ids(cases):
    return [case["id"] for case in cases]


def _check(design_class, case):
    result = run_operations(design_class, case["operations"], case["arguments"])
    assert result == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference_module.WordDictionary, case)


def test_constructed_complete_alphabet_slice_derives_every_find():
    def matches_by_construction(pattern: str) -> bool:
        return len(pattern) <= ALPHABET_MAX_LENGTH and all(
            letter == "." or letter in ALPHABET_SLICE for letter in pattern
        )

    operations = ["WordDictionary"]
    arguments = [[]]
    expected = [None]
    inserted = 0
    for length in range(1, ALPHABET_MAX_LENGTH + 1):
        for letters in itertools.product(ALPHABET_SLICE, repeat=length):
            word = "".join(letters)
            operations.append("insert")
            arguments.append([word])
            expected.append(None)
            inserted += 1
    assert inserted == 780
    probes = [
        ".", "..", "...", "....", ".....",
        "a", "ab", "abc", "abcd",
        "e..", ".e.", "a.e", "zz", "f..", "..f", "af", "fa",
    ]
    for pattern in probes:
        operations.append("find")
        arguments.append([pattern])
        expected.append(matches_by_construction(pattern))
    assert run_operations(reference_module.WordDictionary, operations, arguments) == expected
