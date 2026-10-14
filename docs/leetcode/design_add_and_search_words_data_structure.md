# [Design Add And Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/)

**Medium** | **25 minutes** | **String, Depth-First Search, Design, Trie**

**Pattern:** [Data-Structure Design](../patterns/design/intuition.md), [Trie](../patterns/trie/intuition.md)

**Algorithm:** [Trie](https://en.wikipedia.org/wiki/Trie)

**Practice:** [`practice/design_add_and_search_words_data_structure/solution.py`](../../practice/design_add_and_search_words_data_structure/solution.py)

Design a data structure that supports adding new words and searching for existing words.

Implement the `WordDictionary` class:

* `void addWord(word)` Adds `word` to the data structure.
* `bool search(word)` Returns `true` if there is any string in the data structure that matches `word` or `false` otherwise. `word` may contain dots `'.'` where dots can be matched with any letter.

## Examples

### Example 1

**Input:**

```text
["WordDictionary","addWord","addWord","addWord","search","search","search","search"]
[[],["day"],["bay"],["may"],["say"],["day"],[".ay"],["b.."]]
```

**Output:**

```text
[null, null, null, null, false, true, true, true]
```

**Explanation:** WordDictionary wordDictionary = new WordDictionary();
wordDictionary.addWord("day");
wordDictionary.addWord("bay");
wordDictionary.addWord("may");
wordDictionary.search("say"); // return false
wordDictionary.search("day"); // return true
wordDictionary.search(".ay"); // return true
wordDictionary.search("b.."); // return true

## Constraints

- `1 <= word.length <= 25`
- `word` in `addWord` consists of lowercase English letters.
- `word` in `search` consist of `'.'` or lowercase English letters.
- There will be at most `2` dots in `word` for `search` queries.
- At most `10,000` calls will be made to `addWord` and `search`.

## Deriving the Solution

The data structure must answer "is any stored word equal to this pattern?" where the pattern is a word with a few positions wildcarded. Storing the words in any searchable container and testing the pattern against every member answers that question; the ladder below tightens which members are tested and how. Every solution shares one structural observation: a `.` can match anything, but the pattern's length is fixed, so only stored words of the same length are ever candidates.

1. **Start literal.** Keep a list; `addWord` appends, `search` tests the
   pattern against every stored word of equal length. `O(n * L)` per search:
   see [Brute Force Scan](#brute-force-scan).
2. **Spot the waste.** The scan visits every word just to learn its length
   fails. Bucketing words by length removes most of the list from
   consideration in `O(1)`: see [Length Buckets](#length-buckets).
3. **Share the prefixes.** Words of the same length still re-scan the same
   early characters. A [trie](https://en.wikipedia.org/wiki/Trie) merges
   those shared prefixes, so a literal character moves down one shared node
   instead of re-comparing every stored word: see
   [Trie with Wildcard DFS](#trie-with-wildcard-dfs).
4. **Handle the wildcard.** In the trie a literal character is one child
   lookup; a `.` is "try every child," which is a tiny DFS forked at each
   dot. Worst case `O(26^d * L)` for `d` dots, but the trie's existing
   children prune it far below that: see
   [Trie with Wildcard DFS](#trie-with-wildcard-dfs).

## Solutions

### Brute Force Scan

#### Derivation

The most literal reading of the contract keeps the words in a list and defines `search` as "does any stored word match?" A stored word matches the pattern exactly when it has the same length and agrees with every non-dot character:

1. `addWord` appends the word to `words`.
2. `search` loops over `words`, skipping any stored word whose length
   differs from the pattern's.
3. For equal-length candidates, compare position by position; a `.` in the
   pattern matches anything, so the pair agrees when
   `stored_char == pattern_char or pattern_char == "."`.
4. Return `True` on the first agreeing word, `False` after the list ends.

#### Walkthrough

Trace Example 1's searches over `words = ["day", "bay", "may"]`:

```text
search("say")  len 3 == 3   "day": s!=d  "bay": s!=b  "may": s!=m   -> False
search("day")  "day": d==d a==a y==y                                     -> True
search(".ay")  "day": .==d a==a y==y -> match on the first candidate     -> True
search("b..")  "day": b!=d  "bay": b==b .==a .==y                        -> True
```

Each result matches the expected Output: `[false, true, true, true]` for the four `search` calls.

#### Solution

The code is the filtered, position-wise comparison loop.

```python
class WordDictionary:
    def __init__(self):
        self.words = []

    def addWord(self, word: str) -> None:
        self.words.append(word)

    def search(self, word: str) -> bool:
        for stored in self.words:
            if len(stored) != len(word):
                continue
            if all(
                stored_char == char or char == "."
                for stored_char, char in zip(stored, word)
            ):
                return True
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * L)` per search

Every one of the `n` stored words is length-checked and, when the lengths match, compared position by position up to `L` characters. `addWord` is `O(1)`.

##### Space Complexity: `O(n * L)`

The list stores every word in full.

#### Key Insights

- The length filter is free correctness insurance: a pattern can only match
  words it spans exactly, dots included.
- Everything that follows is about not visiting all `n` words per search.
- With at most `10,000` calls this is often fast enough; the ladder is
  about scaling, not bare correctness.

### Length Buckets

#### Derivation

The brute force's inner loop is fine; the waste is the outer loop over words the length test could have excluded before ever being visited. Grouping the words once at insert time by their length means `search` only ever walks the one bucket the pattern's length selects, and every candidate there survives the length test:

1. Keep `buckets`, a map from word length to the list of words of that
   length (`defaultdict(list)` creates buckets on demand).
2. `addWord` appends to `buckets[len(word)]`.
3. `search` iterates `buckets[len(word)]` only, running the same
   position-wise dot-aware comparison.

#### Walkthrough

After Example 1's three `addWord` calls, `buckets = {3: ["day", "bay", "may"]}`; every search below lands in that one bucket:

```text
search("say")  bucket 3: "day" s!=d, "bay" s!=b, "may" s!=m        -> False
search(".ay")  bucket 3: "day" .==d a==a y==y -> first candidate   -> True
search("b..")  bucket 3: "day" b!=d, "bay" b==b .==a .==y          -> True
```

A query of a length never inserted (say `search("....")`) would find an empty bucket and return `False` without comparing anything. The results match Example 1's expected outputs.

#### Solution

The code is the brute force with the scan's starting set narrowed to one bucket.

```python
from collections import defaultdict


class WordDictionary:
    def __init__(self):
        self.buckets = defaultdict(list)

    def addWord(self, word: str) -> None:
        self.buckets[len(word)].append(word)

    def search(self, word: str) -> bool:
        for stored in self.buckets[len(word)]:
            if all(
                stored_char == char or char == "."
                for stored_char, char in zip(stored, word)
            ):
                return True
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * L)` per search worst case

All stored words could share the pattern's length, in which case the whole bucket is scanned; when lengths spread out, the scan touches only same-length words. `addWord` stays `O(1)`.

##### Space Complexity: `O(n * L)`

The buckets store every word once; the length keys add `O(1)` overhead per distinct length.

#### Key Insights

- Same total storage, better routing: the length test moved from search
  time to insert time.
- The worst case is unchanged, which is the honest limit of a flat
  container: when every word has the same length this is the brute force.

### Trie with Wildcard DFS

#### Derivation

Buckets fixed the outer loop, but within one bucket each search still re-reads the same leading characters of every candidate: `"day"`, `"bay"`, `"may"` all re-offer their first letter to every query. A trie shares those prefixes: one node per distinct `(prefix, next character)` step, so the words above occupy a single root with children `d`, `b`, `m`. A search walks the pattern down the trie: a literal character follows its one child edge, and a `.` forks over every child edge present, recursing on the rest of the pattern. The recursion is a depth-first search whose depth is the pattern length:

1. `addWord` walks from `root`, creating a child node per character, and
   marks the final node `is_word`.
2. `search` starts a DFS at `root` with position `0`.
3. At each position: a literal `char` requires `char in node.children`
   (else fail); a `.` returns the OR of the DFS over every child.
4. After the last character, the answer is whether the node reached is
   marked `is_word`, which rejects prefixes like `"da"` that are not stored
   words.

#### Walkthrough

After the three `addWord` calls the trie holds a root with children `b`, `d`, `m`, each chain ending at a word-marked `y` node. Trace Example 1's wildcard searches:

```text
search("day")  root -d-> node_d -a-> node_da -y-> node_day  is_word -> True
search("say")  root: 's' not in children {b, d, m}                     -> False
search(".ay")  '.' forks over the root's children in insertion order (d, b, m):
                 d-branch: -a-> node_da -y-> is_word -> True (short-circuits)
search("b..")  b->node_b, '.' forks over {a}:
                 node_ba, '.' forks over {y}: node_bay is_word          -> True
```

All four match Example 1's expected outputs. The `is_word` mark matters for near-misses: `search(".a")` forks over the three first letters, walks each `-a->`, and lands on `node_da`/`node_ba`/`node_ma`, none marked, so it returns `False` even though `"da"` is a prefix of a stored word.

#### Solution

The code is the insert walk plus the forking DFS.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True

    def search(self, word: str) -> bool:
        return self._search_from(self.root, word, 0)

    def _search_from(self, node: TrieNode, word: str, index: int) -> bool:
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
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(L)` for literal searches, `O(26^d * L)` worst case with `d` dots

Each literal character is one child lookup; each dot branches over every child present, so `d` dots multiply the paths by up to the 26-ary branching factor per dot. With the problem's guarantee of at most `2` dots per search the bound is small in practice, and empty branches die at the first missing child.

##### Space Complexity: `O(total characters)` for the trie, `O(d)` DFS depth

The trie holds one node per distinct prefix step, bounded by the total characters inserted and typically far less; the DFS recursion happens only at `.` characters (literal positions are consumed inside the loop of the current frame), so its depth is one frame per dot, `d` at most.

#### Key Insights

- The wildcard turns exact-lookup search into a bounded DFS; the trie is
  what bounds it, since a `.` can only branch over children that actually
  exist.
- `is_word` is what separates "there is a word through here" from "this
  node is a word," which is how prefix-only paths fail cleanly.
- Storing children in a dict keyed by character keeps the literal path at
  one hash lookup per character and makes the dot branch a loop over
  `children.values()`.

## Comparison of Solutions

### Time Complexity

- **Brute Force Scan**: `O(n * L)` per search - every stored word is visited.
- **Length Buckets**: `O(n * L)` per search worst case - only same-length words are visited.
- **Trie with Wildcard DFS**: `O(L)` literal, `O(26^d * L)` with `d` dots - shared prefixes plus branching.

### Space Complexity

- **Brute Force Scan**: `O(n * L)` - the word list.
- **Length Buckets**: `O(n * L)` - the word list plus length keys.
- **Trie with Wildcard DFS**: `O(total characters)` - one node per distinct prefix step.

### Trade-offs

- The scan and buckets are trivial to write and their `addWord` is `O(1)`;
  their searches degrade linearly with stored words.
- The trie pays insert-time allocation and a node class, and wins whenever
  the word set grows or searches repeat prefixes.
- Buckets beat the scan exactly when lengths spread; the trie subsumes that
  benefit (each length's chain lives under its own subtree).

### When to Use Each

- **Brute Force Scan**: prototypes and tiny word sets.
- **Length Buckets**: word sets with naturally varied lengths and no trie
  appetite.
- **Trie with Wildcard DFS**: the intended solution and the default at
  scale; also the pattern to reuse for wildcarded dictionary lookups
  generally (recommended here).

### Optimization Notes

- Tries with array-backed children (index `ord(c) - ord("a")`) beat dict
  lookups by a constant in compiled languages; in Python the dict is
  idiomatic and competitive.
- Words sharing a full path (duplicates or nested words like `"a"` in
  `"an"`) cost no extra nodes; only the `is_word` marks multiply.
- The DFS could also be written with an explicit stack; the recursive form
  is bounded by the pattern length, which the constraints cap at 25.
