"""Word Dictionary with Wildcard Find — https://www.fastprep.io/problems/amazon-wildcard-word-dictionary

Write-up & approaches: ../../../docs/amazon/amazon-wildcard-word-dictionary.md

Reference implementation of the write-up's recommended Trie with
Wildcard DFS solution, presented as the design class behind the page's
judged find-word operations form. Your own attempt lives in solution.py.

  uv run python amazon/amazon-wildcard-word-dictionary/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-wildcard-word-dictionary/              # run the test sets
"""

from typing import Dict


class TrieNode:
    """One prefix position: children keyed by letter, plus whether a
    stored word ends exactly here."""

    def __init__(self) -> None:
        """Start with no children and no word ending.

        Time:  O(1): one empty dict and one flag.
        Space: O(1): the children grow only as words demand.
        """
        self.children: Dict[str, "TrieNode"] = {}
        self.is_word = False


class WordDictionary:
    """A word dictionary answering wildcard finds over a trie: an
    inserted word is a root-to-node path whose end node carries the
    word-end flag, and a pattern walks all branches its periods open."""

    def __init__(self) -> None:
        """Start with the bare root node.

        Time:  O(1): one node allocated.
        Space: O(1): one node.
        """
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Add the word, creating any missing prefix nodes; a word already
        present re-walks existing nodes and changes nothing.

        Time:  O(L) for a word of length L: one node lookup or creation
            per letter.
        Space: O(L): at most one new node per letter, only for prefixes
            not stored yet.
        """
        node = self.root
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()
            node = node.children[letter]
        node.is_word = True

    def find(self, pattern: str) -> bool:
        """Report whether at least one stored word matches the pattern:
        equal length, and every position either equal or a period, where
        a period matches exactly one letter.

        Time:  O(L) when the pattern holds no periods; each period opens
            all children at its node, so the worst case visits one path
            per same-length stored word, O(M * L) for M matching-length
            words.
        Space: O(L): one node pointer per recursion level.
        """
        return self._search_from(self.root, pattern, 0)

    def _search_from(self, node: TrieNode, pattern: str, index: int) -> bool:
        """Match pattern[index:] onward from the given node, branching
        over every child at a period and requiring a word-end node when
        the pattern is consumed.

        Time:  O(L) per explored path; see find.
        Space: O(L): one frame per remaining pattern position.
        """
        if index == len(pattern):
            return node.is_word
        letter = pattern[index]
        if letter != ".":
            child = node.children.get(letter)
            return child is not None and self._search_from(child, pattern, index + 1)
        for child in node.children.values():
            if self._search_from(child, pattern, index + 1):
                return True
        return False


if __name__ == "__main__":
    # Debug playground: cases.json is empty (design-operation starter), so
    # Example 1's operation sequence stands in.
    dictionary = WordDictionary()
    dictionary.insert("cat")
    dictionary.insert("car")
    dictionary.insert("cart")
    print(dictionary.find("ca."))
    print(dictionary.find("c..t"))
    print(dictionary.find("ca"))
    print(dictionary.find("d.."))
