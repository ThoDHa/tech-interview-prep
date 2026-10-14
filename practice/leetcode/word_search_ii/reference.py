"""Word Search II — https://leetcode.com/problems/word-search-ii/

Write-up & approaches: ../../docs/problems/word_search_ii.md
Reference implementation of the write-up's Trie-Pruned Backtracking solution,
kept next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python word_search_ii/reference.py   # debug one case (see below)
  uv run pytest word_search_ii/               # run the test sets
"""

from typing import List


class TrieNode:
    """One prefix position in the word trie."""

    def __init__(self) -> None:
        self.children = {}
        self.word = None  # Full word, set only at a word's last node.


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        """Return every word spellable by a non-reusing path in the board.

        Builds a trie over the words once, then runs a DFS from every board
        cell, walking the trie alongside the grid: a cell is consumed only
        when its letter follows the current trie node's edge. A reached node
        holding a word records it and clears the mark, so each word is
        reported once even if several paths spell it, and dead prefixes
        abandon the branch immediately.

        Args:
            board: Grid of lowercase letters.
            words: Distinct lowercase words to search for.

        Returns:
            The found words (any order; this implementation follows
            board-cell order and per-node child order).

        Time:  O(C · 4 · 3^(L-1)) for C cells and longest word length L:
            each cell starts a DFS whose first step has 4 neighbors and
            every later step at most 3 (no stepping back).
        Space: O(W · L) for the trie over W words of length up to L, plus
            O(L) recursion depth.
        """
        root = TrieNode()
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.word = word

        rows, columns = len(board), len(board[0])
        found: List[str] = []

        def dfs(row: int, column: int, node: TrieNode) -> None:
            char = board[row][column]
            child = node.children.get(char)
            if child is None:
                return
            if child.word is not None:
                found.append(child.word)
                child.word = None
            board[row][column] = "#"
            if row > 0:
                dfs(row - 1, column, child)
            if row + 1 < rows:
                dfs(row + 1, column, child)
            if column > 0:
                dfs(row, column - 1, child)
            if column + 1 < columns:
                dfs(row, column + 1, child)
            board[row][column] = char

        for row in range(rows):
            for column in range(columns):
                dfs(row, column, root)

        return found


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findWords above, then run this
    # file. cases.json is empty (any-order output), so a literal example
    # stands in.
    board = [
        ["a", "b", "c", "d"],
        ["s", "a", "a", "t"],
        ["a", "c", "k", "e"],
        ["a", "c", "d", "n"],
    ]
    words = ["bat", "cat", "back", "backend", "stack"]
    result = Solution().findWords(board, words)
    print(f"args = words {words}")
    print(f"got: {sorted(result)}")
