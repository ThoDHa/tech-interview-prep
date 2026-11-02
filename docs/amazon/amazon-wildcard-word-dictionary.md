# [Word Dictionary with Wildcard Find](https://www.fastprep.io/problems/amazon-wildcard-word-dictionary)

**Medium** | **NN minutes** | **Trie, String, Depth First Search, Design**

Build a word dictionary that supports inserting words and finding words with wildcards. Process the rows of operations from left to right. The dictionary starts empty, and each row has one of these forms:

["insert", word] adds word to the dictionary. Inserting a word that is already present changes nothing.
["find", pattern] asks whether the dictionary currently holds at least one word that matches pattern.

A pattern matches a word when both have the same length and, at every position, the pattern character is either the same letter or a period .. A period is a wildcard that matches exactly one lowercase letter. It never matches zero letters or more than one letter.

## Examples

### Example 1

**Input:** `operations = [["insert","cat"],["insert","car"],["insert","cart"],["find","ca."],["find","c..t"],["find","ca"],["find","d.."]]`

**Output:** `[true,true,false,false]`

**Explanation:** The pattern ca. matches both cat and car, so the first answer is true. The pattern c..t has length 4 and matches cart. No stored word has length 2, so ca is false. Every stored word starts with c, so d.. is false.

## Constraints

- `N/A (FastPrep lists no constraints)`

## Deriving the Solution

One rule decides everything: a pattern matches only a word of its own exact length, position by position, with a period standing for exactly one letter. So a find is a membership question over a filtered slice of the stored words, and the three approaches differ only in how much of the dictionary that slice touches. The ladder shrinks it:

1. **Start literal.** Keep every word in one list and scan it all, rejecting on length first and matching position by position: see [Brute Force Scan](#brute-force-scan).
2. **Filter by length first.** Length is the cheapest rejection and it never changes after insert, so keep one list per length and scan only the pattern's own bucket: see [Length Buckets](#length-buckets).
3. **Share the prefixes.** Words of one length overlap heavily in their prefixes; a trie stores each prefix once, and a pattern walks it letter by letter, with a period branching over every child: see [Trie with Wildcard DFS](#trie-with-wildcard-dfs).

## Solutions

The approaches mirror the unified-track page [Design Add and Search Words Data Structure](../leetcode/design_add_and_search_words_data_structure.md), which solves the same problem through LeetCode's addWord and search method calls.

### Brute Force Scan

#### Derivation

The statement's most literal reading: the dictionary is the list of words inserted so far, and a find checks the match rule against each of them:

1. Keep `words`, the list of stored words in insert order, skipping a word already present.
2. On `find(pattern)`: scan `words`; a word matches when `len(word) == len(pattern)` and every position holds the pattern's letter or a period.
3. Return whether any word matched.

#### Walkthrough

Example 1, after inserting `cat`, `car`, `cart`. Each find shows the whole scan:

```text
find "ca."    cat: len 3, c-a-. match   -> true
find "c..t"   cart: len 4, c-.-.-t      -> true
find "ca"     all words: len >= 3       -> false
find "d.."    all words start with c    -> false
```

The finds collect into `[true, true, false, false]`, matching the expected Output. `"ca."` matches two words, which the any-scan folds into one true.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, operations: List[List[str]]) -> List[bool]:
        words: List[str] = []
        results: List[bool] = []
        for action, argument in operations:
            if action == "insert":
                if argument not in words:
                    words.append(argument)
            else:
                results.append(self._matches(argument, words))
        return results

    def _matches(self, pattern: str, words: List[str]) -> bool:
        for word in words:
            if len(word) != len(pattern):
                continue
            for word_letter, pattern_letter in zip(word, pattern):
                if pattern_letter != "." and pattern_letter != word_letter:
                    break
            else:
                return True
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * L)` per find

A find scans all `n` stored words at pattern length `L`; an insert is O(n) for the duplicate check and O(1) for the append.

##### Space Complexity: `O(n * L)`

The list holds every distinct inserted word.

#### Key Insights

- The length check is the first rejection and the cheapest; everything else is a position-by-position walk.
- The for-else keeps the match rule flat: the `else` fires only when no position broke, which is exactly the match.
- Duplicate inserts are absorbed by the membership check, though the scan never needs it for finds.

### Length Buckets

#### Derivation

The scan reads every stored word but the match rule kills most of them on the length line alone: a pattern of length `L` can only ever match words of length `L`. Bucketing the words by length moves that rejection from scan time to insert time, so a find opens exactly one bucket:

1. Keep `buckets` mapping length to the list of stored words of that length.
2. On insert: append the word to `buckets[len(word)]` unless already present.
3. On `find(pattern)`: run the position-by-position match over `buckets[len(pattern)]` only.

#### Walkthrough

Example 1 again. Inserting `cat`, `car`, `cart` fills two buckets:

```text
buckets after the inserts:
  3: [cat, car]
  4: [cart]

find "ca."    bucket 3: cat matches, car matches       -> true
find "c..t"   bucket 4: cart matches                   -> true
find "ca"     bucket 2: empty                          -> false
find "d.."    bucket 3: cat no (d), car no (d)         -> false
```

The finds collect into `[true, true, false, false]`, matching the expected Output. The empty bucket answers `"ca"` without reading a single word.

#### Solution

```python
from typing import Dict, List


class Solution:
    def solve(self, operations: List[List[str]]) -> List[bool]:
        buckets: Dict[int, List[str]] = {}
        results: List[bool] = []
        for action, argument in operations:
            if action == "insert":
                bucket = buckets.setdefault(len(argument), [])
                if argument not in bucket:
                    bucket.append(argument)
            else:
                results.append(self._matches(argument, buckets.get(len(argument), [])))
        return results

    def _matches(self, pattern: str, words: List[str]) -> bool:
        for word in words:
            for word_letter, pattern_letter in zip(word, pattern):
                if pattern_letter != "." and pattern_letter != word_letter:
                    break
            else:
                return True
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(b * L)` per find

`b` is the number of stored words of the pattern's length; an insert stays O(b) for the duplicate check against its own bucket.

##### Space Complexity: `O(n * L)`

The buckets partition the same `n` words the scan list held.

#### Key Insights

- Length is a property of the key, not of the query: bucketing by it is free at insert and decisive at find.
- The worst case is unchanged, a bucket holding every word of one length, but the average find shrinks by the length distribution.
- The match helper lost its length check: the bucket lookup performs it.

### Trie with Wildcard DFS

#### Derivation

Even within one bucket the words repeat each other: `cat` and `cart` share their first two letters, and every word starting with `c` re-stores that fact. A [trie](https://en.wikipedia.org/wiki/Trie) stores each prefix once as a root-to-node path, with a word-end flag marking complete words. An insert walks and builds the path; a find walks the pattern, and a period stops pinning one child: it branches over every child the node has. The exact-length rule becomes the walk's termination: the pattern must be consumed exactly at a word-end node:

1. Keep `root`, a trie node holding a letter-keyed child map and an `is_word` flag.
2. On insert: walk the letters, creating missing children, and set `is_word` on the final node.
3. On `find(pattern)`: depth-first search from the root over `pattern` positions; a letter descends into its one child, a period tries every child.
4. Return whether any walk consumes the pattern at a node whose `is_word` is set.

#### Walkthrough

Example 1's trie after the three inserts, with word-end nodes starred:

```text
root
└── c
    └── a
        ├── t*   (cat)
        └── r*   (car)
            └── t*   (cart)

find "ca.":   root -c-> a, "." branches over {t*, r*}: both are
              word ends and the pattern is consumed     -> true
find "c..t":  root -c-> a, "." branches: from t* the last
              "." finds no child (t is a leaf); from r,
              "." -> t* with the pattern consumed       -> true
find "ca":    root -c-> a, pattern consumed at a,
              which is not a word end                   -> false
find "d..":   root has no d child                       -> false
```

The finds collect into `[true, true, false, false]`, matching the expected Output. The `"ca"` miss is the subtle one: the path exists, but the walk ends one letter short of any word-end node, which is exactly the prefix-is-not-a-word rule.

#### Solution

The code is the walk from the trace: one child per letter, every child per period, and the word-end flag as the only acceptance.

```python
from typing import List


class TrieNode:
    def __init__(self) -> None:
        self.children: dict = {}
        self.is_word = False


class Solution:
    def solve(self, operations: List[List[str]]) -> List[bool]:
        root = TrieNode()
        results: List[bool] = []
        for action, argument in operations:
            if action == "insert":
                node = root
                for letter in argument:
                    node = node.children.setdefault(letter, TrieNode())
                node.is_word = True
            else:
                results.append(self._search_from(root, argument, 0))
        return results

    def _search_from(self, node: TrieNode, pattern: str, index: int) -> bool:
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
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(L)` per find without periods

A dotless pattern walks one root-to-node path in `O(L)`. Every period opens all children at its node, so a pattern with `d` periods explores at most `26^d` paths, bounded by the stored words of the pattern's length: the worst case is `O(m * L)` for `m` same-length words, one visited path per word.

An insert is `O(L)`: one child lookup or creation per letter.

##### Space Complexity: `O(total letters)`

Every inserted word contributes at most `L` new nodes, shared prefixes stored once; the search holds one frame per pattern position, `O(L)`.

#### Key Insights

- The trie compiles the dictionary once so a find explores only paths that exist; the scan reads words that mostly cannot match.
- The word-end flag carries the exact-length rule: a walk that runs out of pattern mid-path, like `"ca"` against `cat`, is a miss no matter how alive the path is.
- A period is a branch, not a gap: it tries every child exactly one level down, so it can never match zero letters or span two positions.

## Comparison of Solutions

### Time Complexity

- **Brute Force Scan**: `O(n * L)` per find - every stored word is read.
- **Length Buckets**: `O(b * L)` per find - only the pattern's length bucket is read.
- **Trie with Wildcard DFS**: `O(L)` per find without periods, `O(m * L)` worst case with them - only existing paths are walked.

### Space Complexity

- **Brute Force Scan**: `O(n * L)` - one list of all words.
- **Length Buckets**: `O(n * L)` - the same words, partitioned.
- **Trie with Wildcard DFS**: `O(total letters)` - shared prefixes stored once, which is never worse and often far smaller.

### Trade-offs

- **Brute Force Scan**: the definition written down and the easiest to trust; it pays for every stored word on every find.
- **Length Buckets**: one observation, one lookup, and the scan shrinks; the length distribution decides how much.
- **Trie with Wildcard DFS**: the only structure whose work tracks the pattern's own path; dotless finds are linear in the pattern alone, at the price of node plumbing and a recursive walk.

### When to Use Each

- **Brute Force Scan**: as the baseline to state first, or for a tiny dictionary queried rarely.
- **Length Buckets**: when lengths spread widely and finds dominate: cheap to build, no recursion, big average win.
- **Trie with Wildcard DFS (Recommended)**: the interview answer for wildcard lookups: the structure every follow-up (prefix queries, deletion, counted wildcards) builds on.

### Optimization Notes

- **Trie with Wildcard DFS** is the recommended choice: dotless patterns resolve in `O(L)`, and periods only pay for branches that actually exist.
- The search returns on the first matching branch, so an early hit prunes the remaining period branches; the order of `children` never changes correctness, only which hit is found first.
- The word-end flag is what separates this problem from a prefix search: dropping it would answer `"ca"` with true once `cart` is stored, the classic trie miss.
- In a language without dict-ordered guarantees the node's child map is still fine here: find is order-insensitive because it accepts any matching branch.
