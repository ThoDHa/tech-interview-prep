# [Word Search II](https://leetcode.com/problems/word-search-ii/)

**Hard** | **40 minutes** | **Array, String, Backtracking, Trie, Matrix**

**Pattern:** [Trie](../patterns/trie/intuition.md), [Backtracking](../patterns/backtracking_exploration/intuition.md)

**Algorithm:** [Trie](https://en.wikipedia.org/wiki/Trie) · [Backtracking](https://en.wikipedia.org/wiki/Backtracking)

**Practice:** [`practice/word_search_ii/solution.py`](../../practice/word_search_ii/solution.py)

Given a 2-D grid of characters `board` and a list of strings `words`, return all words that are present in the grid.

For a word to be present it must be possible to form the word with a path in the board with horizontally or vertically neighboring cells. The same cell may not be used more than once in a word.

## Examples

### Example 1

**Input:**

```text
board = [
  ["a","b","c","d"],
  ["s","a","a","t"],
  ["a","c","k","e"],
  ["a","c","d","n"]
],
words = ["bat","cat","back","backend","stack"]
```

**Output:**

```text
["cat","back","backend"]
```

### Example 2

**Input:**

```text
board = [
  ["x","o"],
  ["x","o"]
],
words = ["xoxo"]
```

**Output:**

```text
[]
```

## Constraints

- `1 <= board.length, board[i].length <= 12`
- `board[i]` consists only of lowercase English letter.
- `1 <= words.length <= 30,000`
- `1 <= words[i].length <= 10`
- `words[i]` consists only of lowercase English letters.
- All strings within `words` are distinct.

## Deriving the Solution

Each word is a [Word Search](word_search.md) query, so one honest baseline runs that DFS once per word from every cell. The ladder below keeps the per-cell DFS but makes the dictionary itself do the navigating: instead of asking "is the path spelled so far some word's prefix?" by lookup, the search walks a trie and only ever extends paths the dictionary admits.

1. **Start literal.** For each word, DFS from every cell checking that the
   word's characters line up along the path. `O(W * C * 3^L)`: see
   [Per-Word DFS](#per-word-dfs).
2. **Spot the waste.** The same paths are walked once per word sharing
   their prefix; `"back"` and `"backend"` re-walk `b-a-c-k` entirely.
3. **Share the prefixes.** A [trie](https://en.wikipedia.org/wiki/Trie)
   over the words merges every shared prefix, so one DFS walks all words
   simultaneously: extend the path only while the current cell's letter has
   a trie edge, and record a word when its last node is reached: see
   [Trie-Pruned Backtracking](#trie-pruned-backtracking).

## Solutions

### Per-Word DFS

#### Derivation

The most literal reading turns the board into a word-search oracle and queries it once per word. The oracle is the standard word-search DFS: from a start cell, extend the path through unused orthogonal neighbors while the path's characters match the word's, and succeed on consuming the last character:

1. `exists(word)` tries the DFS from every `(row, column)` start.
2. The DFS carries the position `index` in the word and the `used` cell set;
   it fails off-board, on a letter mismatch, or on an already-`used` cell.
3. On a match it marks the cell `used`, recurses to the four neighbors with
   `index + 1`, and unmarks on the way out.
4. `index == len(word)` is success.
5. `findWords` collects every word whose query returns `True`.

#### Walkthrough

Trace `exists("cat")` on Example 1's board. The starts are scanned row-major, so the oracle rejects `(0,0)` and `(0,1)` at their first letter and enters the DFS at `(0,2)`, the first `c`:

```text
start (0,2)=c  index 0 matches, mark (0,2), try down, up, right, left
  down  (1,2)=a  match index 1, mark (1,2)
    down  (2,2)=k  vs t -> no
    up    (0,2)  used
    right (1,3)=t  match index 2, mark (1,3)
      index 3 == len("cat") -> True
```

`cat` is present, matching Example 1's output. The other `c` starts, `(2,1)` and `(3,1)`, would each die hunting a `t` (their only `a` neighbors lead to `k`, `c`, and `d`), but the oracle never reaches them because `any` short-circuits at the first success. The same oracle run for `bat`, `back`, `backend`, and `stack` finds `back` and `backend` but not `bat` (no `t` adjacent to any `ba` path) nor `stack`, giving `["cat", "back", "backend"]`.

#### Solution

The code is the word-search oracle queried once per word.

```python
from typing import List, Set, Tuple


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        rows, columns = len(board), len(board[0])

        def exists(word: str) -> bool:
            def dfs(row: int, column: int, index: int, used: Set[Tuple[int, int]]) -> bool:
                if index == len(word):
                    return True
                if not (0 <= row < rows and 0 <= column < columns):
                    return False
                if (row, column) in used or board[row][column] != word[index]:
                    return False
                used.add((row, column))
                found = any(
                    dfs(row + dr, column + dc, index + 1, used)
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
                )
                used.discard((row, column))
                return found

            return any(
                dfs(row, column, 0, set())
                for row in range(rows)
                for column in range(columns)
            )

        return [word for word in words if exists(word)]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(W * C * 3^L)`

Each of `W` words is searched from each of `C` cells; a DFS path of length `L` branches 4 ways at the first step and at most 3 ways afterwards (the cell it came from is `used`).

##### Space Complexity: `O(L)`

The `used` set and the recursion never exceed the longest word's length; the output adds the found words.

#### Key Insights

- The per-path branching factor is 3, not 4: backtracking the `used` mark
  is what closes the door the path entered through.
- The oracle answers exactly one word at a time; nothing is shared between
  queries, which is the entire cost of this design.
- Correctness is easy to see, which makes this version the reference for
  testing the faster one.

### Trie-Pruned Backtracking

#### Derivation

The oracle repeats its walks for every word, yet the words arrive as one batch: `back` and `backend` differ only after their fourth character, so their searches re-walk the identical `b-a-c-k` prefix. A trie over all the words merges those prefixes, and the DFS walks it instead of a single word. The navigator is now the dictionary itself: at each step the search asks the trie node whether the cell's letter continues any word, and a branch dies the moment no word cares. Reaching a node whose `word` mark is set means the path just spelled a complete word: record it once, then clear the mark so duplicate paths and nested repeats cannot report it twice:

1. Build a trie over `words`; store each word in its last node's `word`
   field.
2. Start a DFS from every board cell at the trie root.
3. In the DFS: `child = node.children.get(board[row][column])`; `None`
   prunes the step.
4. If `child.word` is set, append it to `found` and set `child.word = None`.
5. Mark the cell with a `#` sentinel (removing its letter from future
   matches), recurse over the in-bounds neighbors, and restore the letter.
6. Start the DFS with the parent node, so the start cell itself is matched
   inside the first `dfs` call.

#### Walkthrough

The trie for `["bat", "cat", "back", "backend", "stack"]` holds three root children `b`, `c`, `s`; under `b` the chain `a -> c -> k` carries `back` and continues `e -> n -> d` for `backend`; `cat` hangs off `c`, `stack` off `s`. Trace the search's start at `(0,1)`:

```text
dfs(0,1) letter b  root has child b   no word yet
  dfs(1,1) letter a  b-child has a
    dfs(0,1) letter #  no # child -> prune          (the # guard blocks re-entry)
    dfs(2,1) letter c  a-child has c
      dfs(1,1) letter #  prune
      dfs(3,1) letter c  no c child -> prune
      dfs(2,0) letter a  prune
      dfs(2,2) letter k  c-child has k -> record "back", clear mark
        dfs(2,3) letter e  k-child has e -> n -> d records "backend" here too
    dfs(1,0) letter s, dfs(1,2) letter a, dfs(0,0) letter a  pruned or dead (b-path has no s; the a's lead nowhere)
  dfs(0,2) letter c  the walk sits on the b node, whose only child is a: no c -> prune
```

(The final call runs under the `b` node the path reached through `(1,1)`'s `a`, so `(0,2)`'s `c` finds no edge and the branch closes.)

The `#` in the trace is the guard: when the DFS from `(1,1)` looks back up at `(0,1)`, that cell reads `#`, no trie has a `#` edge, and the re-entry dies in one lookup. `back` is recorded at `(2,2)` and `backend` two steps deeper, exactly Example 1's answer together with `cat` (found from `(0,2)`'s root-`c` start later in the cell loop). The 4 x 4 board yields 16 top-level `dfs` calls, one per cell; on this input the whole search makes 70 cell entries, and on a board whose letters match no word's first letter the trie turns every one of those away at the first lookup.

#### Solution

The code is the trie walk: build once, then one DFS per cell with the sentinel guard and the one-shot word mark.

```python
from typing import List


class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None  # The full word, set only at its last node.


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
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
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(C * 4 * 3^(L-1) + W * L)`

Building the trie is `O(W * L)`. Each of the `C` cells starts one DFS whose first step tries up to 4 neighbors and every later step at most 3 (the `#` guard closes the entry direction), bounded by the longest word's length `L`. The trie-not-words bound is what matters: the same bound per cell covers all `W` words at once, where the per-word DFS paid it `W` times.

##### Space Complexity: `O(W * L)`

The trie holds one node per distinct prefix (at most the total characters), and the DFS depth is bounded by `L`.

#### Key Insights

- The trie inverts control: the dictionary tells the grid search where it
  is still possible to continue, instead of the grid asking the dictionary
  about each finished path.
- The `#` sentinel removes the entry cell from the alphabet, so "don't
  reuse a cell" costs one failed child lookup rather than a set test.
- Clearing `child.word` after recording makes the search duplicate-proof:
  a word with several spellings reports once, and a word that is a prefix
  of another does not re-report when the longer one passes through.

## Comparison of Solutions

### Time Complexity

- **Per-Word DFS**: `O(W * C * 3^L)` - the full grid search repeated per word.
- **Trie-Pruned Backtracking**: `O(C * 4 * 3^(L-1) + W * L)` - one grid search total.

### Space Complexity

- **Per-Word DFS**: `O(L)` - one `used` set and one recursion.
- **Trie-Pruned Backtracking**: `O(W * L)` - the trie, shared by every search.

### Trade-offs

- The per-word DFS needs no auxiliary structure and is trivially correct;
  its cost multiplies by `W` exactly when `W` is large (up to 30,000).
- The trie version pays a build pass and a node class; in exchange the grid
  is searched once, and prefixes shared by many words cost nothing extra.
- On the constraint extremes (30,000 words on a 12 x 12 board) the per-word
  approach is infeasible; the trie approach is the standard.

### When to Use Each

- **Per-Word DFS**: tiny word lists, or as the cross-check oracle when
  testing the trie version.
- **Trie-Pruned Backtracking**: the intended solution whenever more than a
  couple of words share prefixes, which on real word lists is always
  (recommended here).

### Optimization Notes

- Pruning exhausted trie branches back out (deleting a child when its
  subtree has no words left) keeps later searches off dead prefixes once
  every word through them is found.
- Storing `word` strings in the trie nodes costs memory; an index into the
  words list (cleared the same way) trims it if needed.
- The board is mutated during the search and restored on the way out; if
  callers must not observe temporary state, copy the board first, at an
  `O(C)` price.
