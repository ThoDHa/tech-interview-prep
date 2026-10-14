"""Alien Dictionary — https://leetcode.com/problems/alien-dictionary/

Write-up & approaches: ../../docs/problems/alien_dictionary.md
Reference implementation of the write-up's Kahn's Algorithm (Topological Sort
via BFS) solution.

There is a new alien language that uses the English alphabet, but the order of the letters is unknown. You are given a list of strings `words` from the alien language's dictionary. It is claimed that the strings in `words` are sorted lexicographically by the rules of this new language. If this claim is incorrect, and the given arrangement of strings in `words` cannot correspond to any order of letters, return `""`. Otherwise, return a string of the unique letters in the new alien language sorted in lexicographically increasing order by the new language's rules. If there are multiple solutions, return **any** of them.

  uv run python alien_dictionary/reference.py   # debug one case (see below)
  uv run pytest alien_dictionary/               # run the test sets
"""

from collections import deque


class Solution:
    def solve(self, *args):
        """Derive the alien letter order from adjacent-word comparisons.

        Extracts one precedence edge per differing letter pair from each
        adjacent word pair, then runs Kahn's algorithm: repeatedly take a
        zero-indegree letter. A prefix violation (`abc` before `ab`) or an
        extracted cycle leaves letters untaken and returns "".

        Args:
            args: One element, `words`: list of lowercase strings claimed to
                be sorted by the alien order.

        Returns:
            One valid ordering of the unique letters as a string, or "" when
            the claim is impossible.

        Time:  O(total): every character is inspected a constant number of
            times, where total is the sum of word lengths.
        Space: O(1): the adjacency map and indegrees hold at most 26 letters.
        """
        (words,) = args
        adjacency = {letter: set() for word in words for letter in word}
        indegree = {letter: 0 for letter in adjacency}

        for first, second in zip(words, words[1:]):
            if len(first) > len(second) and first.startswith(second):
                # A longer word before its own prefix is unsortable.
                return ""
            for a, b in zip(first, second):
                if a != b:
                    if b not in adjacency[a]:
                        adjacency[a].add(b)
                        indegree[b] += 1
                    break

        order = []
        queue = deque(letter for letter in sorted(indegree) if indegree[letter] == 0)
        while queue:
            letter = queue.popleft()
            order.append(letter)
            for nxt in sorted(adjacency[letter]):
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)
        if len(order) != len(adjacency):
            # A cycle among the extracted edges: no valid order exists.
            return ""
        return "".join(order)


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    # cases.json is empty (any-order output), so a literal example stands in.
    words = ["hrn", "hrf", "er", "enn", "rfnn"]
    result = Solution().solve(words)
    print(f"args = {words}")
    print(f"got: {result}")
