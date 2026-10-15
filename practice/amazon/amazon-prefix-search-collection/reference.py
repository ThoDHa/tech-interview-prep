"""Dynamic Prefix Search Collection — https://www.fastprep.io/problems/amazon-prefix-search-collection

Write-up & approaches: ../../../docs/amazon/amazon-prefix-search-collection.md
Reference implementation of the write-up's recommended Trie with
Sorted-Child DFS solution, kept next to the harness so authored cases stay
falsifiable. Your own attempt lives in solution.py.
"""

from typing import Dict, List, Optional

SUGGESTION_LIMIT = 3


class TrieNode:
    def __init__(self) -> None:
        self.children: Dict[str, "TrieNode"] = {}
        self.word: Optional[str] = None


class PrefixSearchCollection:
    def __init__(self) -> None:
        """Start an empty collection with a bare trie root.

        Time:  O(1): one node.
        Space: O(1): no words stored yet.
        """
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Walk one node per character and mark the terminal node with the
        complete word; re-inserting a stored word re-walks the same path
        and re-sets the same mark, so inserts are idempotent.

        Time:  O(L) for a word of length L: one dictionary lookup per
            character.
        Space: O(L) worst case for the new nodes a novel word creates.
        """
        node = self.root
        for letter in word:
            node = node.children.setdefault(letter, TrieNode())
        node.word = word

    def search(self, prefix: str) -> List[str]:
        """Return up to `SUGGESTION_LIMIT` stored words beginning with
        `prefix`, in lexicographic order.

        Time:  O(P + 3 × L): the prefix walk touches P characters and the
            bounded DFS stops at the third reported word.
        Space: O(1) beyond the returned row of at most three words.
        """
        node = self.root
        for letter in prefix:
            node = node.children.get(letter)
            if node is None:
                return []
        matches: List[str] = []
        self._collect_matches(node, matches)
        return matches

    def _collect_matches(self, node: TrieNode, matches: List[str]) -> None:
        """Emit the node's own word before its children in sorted letter
        order, stopping for good once the limit lands.

        Time:  O(1) amortized per reported word against the limit; the
            recursion touches only nodes that prefix stored words.
        Space: O(depth) recursion, bounded by the 100-character word
            limit the constraints declare.
        """
        if node.word is not None:
            matches.append(node.word)
            if len(matches) == SUGGESTION_LIMIT:
                return
        for letter in sorted(node.children):
            self._collect_matches(node.children[letter], matches)
            if len(matches) == SUGGESTION_LIMIT:
                return


if __name__ == "__main__":
    # Debug playground: cases.json is empty (design-operation starter), so
    # Example 1's operation sequence stands in.
    collection = PrefixSearchCollection()
    for word in ("mouse", "mobile", "moneypot", "monitor", "mousepad"):
        collection.insert(word)
    print(collection.search("mo"))
    print(collection.search("mou"))
