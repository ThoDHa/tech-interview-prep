# [Word Search II](https://www.fastprep.io/problems/amazon-word-search-ii)

**Hard** | **NN minutes** | **Trie, Backtracking, Matrix, Depth First Search**

Given an m x n board of lowercase English letters and an array of distinct lowercase words, return every word that can be formed on the board.

A word is formed by starting at any cell and repeatedly moving one cell horizontally or vertically. A board cell may be used at most once while forming one word.

Return found words in the same order in which they appear in words.

## Examples

### Example 1

**Input:** `board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]`, `words = ["oath","pea","eat","rain"]`

**Output:** `["oath","eat"]`

**Explanation:** The paths o-a-t-h and e-a-t use horizontal or vertical neighbors without reusing a cell.

### Example 2

**Input:** `board = [["a","b"],["c","d"]]`, `words = ["abcb","abcd","acdb"]`

**Output:** `["acdb"]`

**Explanation:** acdb follows the path down, right, then up. The other words require a reused cell or a diagonal move.

## Constraints

- `1 <= m, n <= 12.`
- `1 <= words.length <= 30000.`
- `1 <= words[i].length <= 10.`
- `The board and every word contain only lowercase English letters.`
- `All words are distinct.`

## Solutions

### Per-Word DFS

#### Derivation

The most literal reading turns the board into a word-search oracle and queries it once per word. The oracle is the standard word-search DFS: from a start cell, extend the path through unused orthogonal neighbors while the path's characters match the word's, and succeed when the path consumes the last character. Querying the oracle in `words` order and keeping the words that answer yes makes the statement's output-order requirement free:

1. For each `word`, run `exists(word)`.
2. The nested `dfs(row, column, index, used)` fails off-board, on a letter
   mismatch, or on a cell already in `used`.
3. On a match it marks `(row, column)` in `used`, recurses to the four
   neighbors with `index + 1`, and unmarks on the way out (backtracking).
4. `index == len(word)` is success, checked at entry so a word succeeds the
   moment its last character lands.
5. `[word for word in words if exists(word)]` returns the survivors in input
   order.

#### Walkthrough

Example 1's board:

```text
row 0   o  a  a  n
row 1   e  t  a  e
row 2   i  h  k  r
row 3   i  f  l  v
```

Trace `exists("oath")`: the start scan is row-major, so the first cell `(0, 0)` already holds the needed `o` and the DFS begins there. Neighbors are tried down, up, right, left:

```text
dfs(0,0) index 0  'o' matches, mark (0,0)
  dfs(1,0) index 1  'e' vs 'a' -> no
  dfs(-1,0)         out of bounds -> no
  dfs(0,1) index 1  'a' matches, mark (0,1)
    dfs(1,1) index 2  't' matches, mark (1,1)
      dfs(2,1) index 3  'h' matches, mark (2,1)
        dfs(3,1) index 4  == len("oath") -> True
```

`"oath"` is present. `"pea"` dies at its first letter: no cell holds `p`, so all 16 starts fail in one comparison each. `exists("eat")` needs a backtrack before it succeeds:

```text
start (1,0)  'e' matches: down 'i', up 'o', right 't' vs 'a', left out -> dead
start (1,3)  'e' matches
  dfs(1,2) index 1  'a' matches, mark (1,2)
    dfs(2,2)  'k' vs 't' -> no
    dfs(0,2)  'a' vs 't' -> no
    dfs(1,3)  used -> no
    dfs(1,1) index 2  't' matches, mark (1,1)
      index 3 == len("eat") -> True
```

`exists("rain")` starts at the only `r`, `(2, 3)`, and finds no neighbor holding `a`. The survivors, queried in `words` order, are `["oath", "eat"]`, matching the expected Output.

#### Solution

The code is the per-word oracle and the order-preserving filter.

```python
from typing import List, Set, Tuple


class Solution:
    def solve(self, board: List[List[str]], words: List[str]) -> List[str]:
        """Return every word formable on the board, in the input word order.

        Time:  O(W * C * 3^L): each of W words is searched from each of C
            cells; a path of length L branches 4 ways once and at most 3
            ways afterwards.
        Space: O(L) for the used set and the recursion of one word search.
        """
        rows, columns = len(board), len(board[0])

        def exists(word: str) -> bool:
            def dfs(row: int, column: int, index: int,
                    used: Set[Tuple[int, int]]) -> bool:
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

##### Time Complexity: `O(W × C × 3^L)`

Each of `W` words is searched from each of `C` cells; a DFS path of length `L` branches 4 ways at the first step and at most 3 ways afterwards (the cell it came from is `used`).

##### Space Complexity: `O(L)`

The `used` set and the recursion never exceed the longest word's length; the output adds the found words.

#### Key Insights

- The per-path branching factor is 3, not 4: unmarking the cell on the way out is what closes the door the path entered through.
- One `used` set serves every start cell of the same word because backtracking removes the marks; a fresh set per start would also be correct but pays more.
- Querying in input order makes the output-order requirement free; the trie version below must restore that order explicitly.
- The cost multiplies by `W` exactly when `W` is largest (up to 30,000 words), which is the flaw the next approach repairs.

### Trie-Pruned Backtracking

#### Derivation

The oracle repeats its walks once per word: any two words sharing a prefix each re-walk the shared steps, and every word pays for its own full search whether or not another word already walked the same cells. With up to 30,000 words that multiplication is fatal. The repair is to build one [trie](https://en.wikipedia.org/wiki/Trie) over all the words and let the DFS walk the trie instead of a single word: the dictionary itself navigates, the search extends a path only while the cell's letter continues some word, and a branch dies the moment no word cares. Reaching a node whose `word` mark is set means the path just spelled a complete word: record it once and clear the mark so a second path spelling the same word cannot report it twice. The board cells are single-character strings in a mutable list of lists, so a `'#'` sentinel removes the entry cell from the alphabet during one search and is restored on the way out. One statement detail the LeetCode twin does not carry: the output must follow `words` order, while the DFS discovers words in board order, so the collected set is filtered through `words` at the end:

1. Build `root`; store each word in its last node's `word` field.
2. Start `dfs(row, column, root)` from every board cell.
3. In `dfs`: `child = node.children.get(board[row][column])`; `None` prunes the
   step.
4. If `child.word` is set, add it to `found_words` and set `child.word = None`.
5. Set `board[row][column] = '#'`, recurse over the in-bounds neighbors, and
   restore the letter.
6. After the cell loop, return
   `[word for word in words if word in found_words]`.

#### Walkthrough

The trie over `["oath", "pea", "eat", "rain"]` has root children `e`, `o`, `p`, `r`; under `o` hangs the chain `a-t-h`, under `e` hangs `a-t`, under `r` hangs `a-i-n`. Most starts die in one lookup because their letter has no root child (every cell except the `o`, the two `e`s, and the `r`). Trace the productive start `(0, 0)`:

```text
dfs(0,0) 'o'  root has child o    no word yet
  dfs(0,1) 'a'  o-child has child a
    dfs(1,1) 't'  oa-child has child t
      dfs(2,1) 'h'  oat-child has child h -> record "oath", clear mark
                    h-child has no children, branch closes
```

The productive path never steps onto a used cell, so the sentinel earns its keep in the reverse direction: when `dfs(0, 1)` looks back at `(0, 0)`, that cell reads `'#'`, no trie holds a `'#'` edge, and the re-entry dies in one lookup. The word `eat` is discovered from its own start `(1, 3)`: the root child `e`, then `a` at `(1, 2)`, then `t` at `(1, 1)` records `"eat"`. `"pea"` is never entered: the `p` child exists in the trie, but no cell holds `p`, so all 16 starts prune at their first lookup. `"rain"` enters from `(2, 3)` through the `r` child, whose next edge needs `a`, but the neighbors of `(2, 3)` hold `e`, `v`, and `k`: pruned. The search ends with `found_words = {"oath", "eat"}`, and filtering `words` against the set returns `["oath", "eat"]` in input order, matching the expected Output.

#### Solution

The code is the trie walk: build once, one DFS per cell with the sentinel guard and the one-shot word mark, then the order-restoring filter.

```python
from typing import Dict, List, Optional, Set


class TrieNode:
    def __init__(self) -> None:
        self.children: Dict[str, "TrieNode"] = {}
        self.word: Optional[str] = None


class Solution:
    def solve(self, board: List[List[str]], words: List[str]) -> List[str]:
        """Return every word formable on the board, in the input word order.

        Time:  O(C * 4 * 3^(L-1) + W * L): building the trie is O(W * L) and
            each of C cells starts one bounded DFS over the shared trie.
        Space: O(W * L) for the trie; the recursion depth is bounded by L.
        """
        root = TrieNode()
        for word in words:
            node = root
            for letter in word:
                node = node.children.setdefault(letter, TrieNode())
            node.word = word

        rows, columns = len(board), len(board[0])
        found_words: Set[str] = set()

        def dfs(row: int, column: int, node: TrieNode) -> None:
            letter = board[row][column]
            child = node.children.get(letter)
            if child is None:
                return
            if child.word is not None:
                found_words.add(child.word)
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
            board[row][column] = letter

        for row in range(rows):
            for column in range(columns):
                dfs(row, column, root)

        return [word for word in words if word in found_words]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(C × 4 × 3^(L-1) + W × L)`

Building the trie is `O(W × L)`. Each of the `C` cells starts one DFS whose first step tries up to 4 neighbors and every later step at most 3 (the `'#'` guard closes the entry direction), bounded by the longest word's length `L`. The trie-not-words bound is what matters: one bound per cell covers all `W` words at once, where the per-word DFS paid it `W` times. The final filter adds `O(W)`.

##### Space Complexity: `O(W × L)`

The trie holds one node per distinct prefix, and the DFS depth is bounded by `L`.

#### Key Insights

- The trie inverts control: the dictionary tells the grid search where it is still possible to continue, instead of the grid asking the dictionary about each finished path.
- The `'#'` sentinel removes the entry cell from the alphabet, so "do not reuse a cell" costs one failed child lookup rather than a set test.
- Clearing `child.word` after recording makes the search duplicate-proof: a word spellable along several paths is added once, and a word that is a prefix of another is not re-reported when the longer one passes through its node.
- The output order is a property of the statement, not of the search: the set collects in board order and the final filter restores the `words` order.

## Comparison of Solutions

### Time Complexity

- **Per-Word DFS**: `O(W × C × 3^L)` - the full grid search repeated once per word.
- **Trie-Pruned Backtracking**: `O(C × 4 × 3^(L-1) + W × L)` - one grid search total over the shared trie, plus the build.

### Space Complexity

- **Per-Word DFS**: `O(L)` - one `used` set and one recursion.
- **Trie-Pruned Backtracking**: `O(W × L)` - the trie, shared by every search.

### Trade-offs

- The per-word DFS needs no auxiliary structure and is trivially correct; its cost multiplies by `W` exactly when `W` is large (up to 30,000).
- The trie version pays a build pass and a node class; in exchange the grid is searched once, and prefixes shared by many words cost nothing extra.
- On the constraint extremes (30,000 words on a 12 × 12 board) the per-word approach is infeasible; the trie approach is the standard.

### When to Use Each

- **Per-Word DFS**: tiny word lists, or as the cross-check oracle when testing the trie version.
- **Trie-Pruned Backtracking (Recommended)**: the intended solution whenever more than a couple of words share prefixes, which on real word lists is always.

### Optimization Notes

- Pruning exhausted trie branches back out (deleting a child once its subtree holds no unrecorded words) keeps later cell starts off dead prefixes.
- Storing `word` strings in the trie nodes costs memory; an index into the `words` list, cleared the same way, trims it if needed.
- The board is mutated during the search and restored on the way out; if callers must not observe temporary state, copy the board first at an `O(C)` price.
- The final `words`-order filter is the statement's ordering requirement made explicit; dropping it would return words in board-discovery order and fail ordered checkers.
