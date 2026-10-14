"""Implement Trie (Prefix Tree): https://leetcode.com/problems/implement-trie-prefix-tree/

Write-up & approaches: ../../docs/problems/implement_trie_prefix_tree.md

Implement a `Trie` (prefix tree) supporting `insert(word)`, `search(word)`
(exact-match lookup), and `startsWith(prefix)` (does any inserted word begin
with this prefix). Words and prefixes consist of lowercase English letters.

  uv run python implement_trie_prefix_tree/solution.py     # debug one case (see CASE below)
  uv run pytest implement_trie_prefix_tree/                # run the test sets
"""

from harness import NotSolved, pick_case, run_operations


class Trie:
    def __init__(self) -> None:
        # Init empty state here (e.g. an empty root). Build it out as you
        # implement insert/search/startsWith below.
        self.root: dict = {}

    def insert(self, word: str) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def search(self, word: str) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def startsWith(self, prefix: str) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a Trie method above, then run this
    # file. Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    try:
        got = run_operations(Trie, case["operations"], case["arguments"])
    except NotSolved:
        got = "implement Trie (insert/search/startsWith) first"
    print(f"case {case['id']}:")
    print(f"operations: {case['operations']}")
    print(f"arguments:  {case['arguments']}")
    print(f"expected:   {case['expected']}")
    print(f"got:        {got}")
