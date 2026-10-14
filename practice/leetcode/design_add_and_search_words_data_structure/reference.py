"""Design Add And Search Words Data Structure — https://leetcode.com/problems/design-add-and-search-words-data-structure/

Write-up & approaches: ../../docs/problems/design_add_and_search_words_data_structure.md
Reference implementation of the write-up's Trie with Wildcard DFS solution,
kept next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python design_add_and_search_words_data_structure/reference.py   # debug one case (see below)
  uv run pytest design_add_and_search_words_data_structure/               # run the test sets
"""

from typing import List


class TrieNode:
    """One character position in the prefix tree."""

    def __init__(self) -> None:
        self.children = {}
        self.is_word = False


class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        """Insert `word` one character at a time, creating missing nodes.

        Time:  O(L) for a word of length L: one node visit per character.
        Space: O(L): at most L new nodes when the word shares no prefix.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True

    def search(self, word: str) -> bool:
        """Return whether any stored word matches `word`, `.` matching any letter.

        Walks literal characters down the trie; at a `.` it forks a DFS over
        every child, so the search follows all branches the wildcards open.

        Time:  O(L) with no dots; O(26^d · L) worst case with d dots, in
            practice far less because the trie prunes to existing children.
        Space: O(L): the DFS depth is at most one node per character.
        """
        return self._search_from(self.root, word, 0)

    def _search_from(self, node: TrieNode, word: str, index: int) -> bool:
        """Match `word[index:]` starting from `node`."""
        for position in range(index, len(word)):
            char = word[position]
            if char == ".":
                return any(
                    self._search_from(child, word, position + 1)
                    for child in node.children.values()
                )
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word


if __name__ == "__main__":
    # Debug playground: set a breakpoint in search above, then run this file.
    # cases.json is empty (multi-method starter), so a literal example stands in.
    dictionary = WordDictionary()
    operations = [
        ("addWord", "day"),
        ("addWord", "bay"),
        ("addWord", "may"),
        ("search", "say"),
        ("search", "day"),
        ("search", ".ay"),
        ("search", "b.."),
    ]
    print(f"operations = {operations}")
    for op, arg in operations:
        result = getattr(dictionary, op)(arg)
        print(f"{op}({arg!r}) -> {result}")
