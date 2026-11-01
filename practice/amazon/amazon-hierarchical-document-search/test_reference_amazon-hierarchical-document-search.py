"""Reference-parametrized gauntlet for Hierarchical Document Search.

The statement's tree serialization, matching conventions, and output
ordering are practice assumptions (the page's source note records
this), and the gauntlet tests exactly the contract the write-up
states: aligned node arrays forming one rooted tree where each folder's
children are homogeneous (all documents or all folders), strict size
comparison against `minSize`, case-sensitive type equality, an empty
`wantedType` disabling the type condition, folder metadata ignored, and
increasing output order. The comparison is plain `==` because the
statement fixes that order.

This is one of the outlier problems whose oracle stays alive instead of
being scratched after freezing, so every run cross-checks the
reference against an independent definition model. Every expectation
in cases_full.json was frozen from that oracle, never hand-computed
and never recorded from the reference: the oracle is a memoized
upward walk (a node is in the search root's subtree iff following
parent links reaches the root), which shares no mechanism with the
reference's children-map DFS; the gauntlet re-runs it against the
reference on every JSON case. The oracle is O(n), so it also covers
the statement's length corner, which is constructed here rather than
serialized and whose expectation additionally follows from arithmetic
on the construction:

- test_constructed_document_fan_of_100000_nodes_matches_the_derived_band:
  50000 folders in a chain (labels 0..49999) carrying all 50000
  documents (labels 50000 + index) as children of the last folder, so
  every folder's children stay homogeneous, document sizes cycling
  0..9 by construction and every type "pdf". Searching from the tree
  root with `minSize = 5` and an empty type must return exactly the
  documents whose `(label - 50000) % 10 > 5`, in increasing order:
  20000 IDs derived arithmetically, then confirmed by both
  implementations.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")

FAN_FOLDER_COUNT = 50_000


def _ids(cases):
    return [case["id"] for case in cases]


class SubtreeOracle:
    """Definition-model oracle: subtree membership by upward parent walks.

    `in_subtree(node)` follows parent links until it hits a node with a
    known verdict, then fills every node on that chain. The search root
    starts known-true and every chain ends at the tree root or at -1,
    so each node is resolved once: O(n) over all queries.
    """

    def __init__(self, parents, root):
        self.parents = parents
        self.verdicts = {root: True}

    def in_subtree(self, node):
        chain = []
        while node != -1 and node not in self.verdicts:
            chain.append(node)
            node = self.parents[node]
        known = node != -1 and self.verdicts[node]
        for member in chain:
            self.verdicts[member] = known
        return known

    def search(self, document_flags, sizes, document_types, min_size, wanted_type):
        matches = []
        for node in range(len(self.parents)):
            if (
                document_flags[node] == 1
                and self.in_subtree(node)
                and sizes[node] > min_size
                and (wanted_type == "" or document_types[node] == wanted_type)
            ):
                matches.append(node)
        return sorted(matches)


def _oracle_from_case(case):
    parents, document_flags, sizes, document_types, root, min_size, wanted_type = case["args"]
    return SubtreeOracle(parents, root).search(document_flags, sizes, document_types, min_size, wanted_type)


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    got = reference.Solution().searchDocuments(*case["args"])
    assert got == case["expected"]
    assert _oracle_from_case(case) == case["expected"]


def test_constructed_document_fan_of_100000_nodes_matches_the_derived_band():
    folder_count = FAN_FOLDER_COUNT
    parents = [-1] + list(range(folder_count - 1))
    parents += [folder_count - 1] * folder_count
    document_flags = [0] * folder_count + [1] * folder_count
    document = FAN_FOLDER_COUNT
    sizes = [0] * folder_count + [index % 10 for index in range(folder_count)]
    document_types = [""] * folder_count + ["pdf"] * folder_count

    got = reference.Solution().searchDocuments(parents, document_flags, sizes, document_types, 0, 5, "")
    expected = [document + index for index in range(folder_count) if index % 10 > 5]
    oracle = SubtreeOracle(parents, 0).search(document_flags, sizes, document_types, 5, "")
    assert got == expected
    assert oracle == expected
