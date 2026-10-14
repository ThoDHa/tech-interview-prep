# [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/)

**Medium** | **30 minutes** | **Hash Table, String, Design, Trie**

**Pattern:** [Trie](../patterns/trie/intuition.md)

**Algorithm:** [Trie](https://en.wikipedia.org/wiki/Trie)

**Practice:** [`practice/implement_trie_prefix_tree/solution.py`](../../practice/implement_trie_prefix_tree/solution.py)

A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. There are various applications of this data structure, such as autocomplete and spellchecker.

Implement the Trie class:

- `Trie()` Initializes the trie object.
- `void insert(String word)` Inserts the string `word` into the trie.
- `boolean search(String word)` Returns `true` if the string `word` is in the trie (i.e., was inserted before), and `false` otherwise.
- `boolean startsWith(String prefix)` Returns `true` if there is a previously inserted string `word` that has the prefix `prefix`, and `false` otherwise.

## Examples

### Example 1

**Input:**

```text
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
```

**Output:**

```text
[null, null, true, false, true, null, true]
```

**Explanation:**

```text
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple");   // return True
trie.search("app");     // return False
trie.startsWith("app"); // return True
trie.insert("app");
trie.search("app");     // return True
```

## Constraints

- `1 <= word.length, prefix.length <= 2000`
- `word` and `prefix` consist only of lowercase English letters.
- At most `3 * 10^4` calls in total will be made to `insert`, `search`, and `startsWith`.

## Deriving the Solution

Every operation here is a prefix question: `search` asks whether a whole word was stored, `startsWith` whether some stored word begins a certain way. The design question is how to organize the inserted words so that answering costs work proportional to the *query's* length, not to how many words are stored.

1. **Start literal.** Keep every inserted word in a list and scan it on demand,
   comparing strings character by character. Correct, but each query touches all `N` stored words for up to `L` characters each: `O(N × L)` per query: see [Brute Force](#brute-force).
2. **Spot the waste.** The scan re-reads shared prefixes endlessly: checking
   `startsWith("app")` against `"apple"`, `"apply"`, and `"appeal"` compares the same three leading characters three times, and every future query repeats it all again. The words share structure that the flat list ignores.
3. **Share the prefixes.** Store characters along the paths of a tree, so words
   with a common prefix walk the same nodes. A query then follows exactly one node per character of its own input, `O(L)` regardless of `N`, and word ends are flagged on their final node to keep `search` and `startsWith` distinct. The natural node is a dictionary mapping each character to its child: see [Dictionary Children](#dictionary-children).
4. **Fix the alphabet.** The constraints promise lowercase English letters only,
   so each node's dictionary can become a 26-slot array indexed by `ord(ch) - ord("a")`: the same `O(L)` walk with the cheapest possible child lookup, at the price of empty slots: see [Fixed Array Children](#fixed-array-children).

## Solutions

### Brute Force

#### Derivation

Before reaching for any tree structure, ask the simplest question that could possibly work: what if we just remember what was inserted? Store every word in a list and answer each query by [scanning that list](https://en.wikipedia.org/wiki/Linear_search). No shared prefixes, no nodes, just a literal record of the inserts.

One corner needs thought: the empty prefix. In a node-based trie the root node always exists, so `startsWith("")` is `True` even before any word is inserted. The list scan would report `False` on an empty trie, so an explicit early return keeps this baseline consistent with the tree implementations, whose `_find("")` reaches the root and succeeds. The steps:

1. `insert` appends the word to the running `self.words` list.
2. `search` scans `self.words` for an entry equal to `word`, returning `True` on an
   exact match.
3. `startsWith` returns `True` immediately for an empty `prefix`, and otherwise
   scans for any entry whose first `len(prefix)` characters equal `prefix`.

This is correct but slow: every query rescans the entire collection and compares full strings, ignoring the prefix-sharing that makes a trie efficient.

#### Walkthrough

Let us watch the Brute Force solution run on Example 1, replaying its call sequence and tracking the one piece of state it keeps: the `self.words` list. Each query scans that list and compares strings, so the table shows what the scan finds for each call.

| Call | What it does | `self.words` after | Returns |
|------|--------------|--------------------|---------|
| `Trie()` | start with an empty list | `[]` | `null` |
| `insert("apple")` | append `"apple"` | `["apple"]` | `null` |
| `search("apple")` | scan: `"apple" == "apple"`, exact match | `["apple"]` | `true` |
| `search("app")` | scan: `"apple" != "app"`, no exact match | `["apple"]` | `false` |
| `startsWith("app")` | scan: `"apple"[:3] == "app"`, prefix match | `["apple"]` | `true` |
| `insert("app")` | append `"app"` | `["apple", "app"]` | `null` |
| `search("app")` | scan: `"apple" != "app"`, then `"app" == "app"`, exact match | `["apple", "app"]` | `true` |

The crucial pair is the two `search("app")` calls. The first returns `false` because only `"apple"` is stored, and `"apple"` is not equal to `"app"`. The second returns `true` only after `"app"` itself is inserted: a stored word must match exactly for `search`, while `startsWith` is satisfied by any stored word that begins with the prefix, which is why `startsWith("app")` was already `true` when only `"apple"` was present.

Collecting the returned values in order gives `[null, null, true, false, true, null, true]`, which matches the expected Output.

#### Solution

The code is the walkthrough's table written down: one list, two scans.

```python
from typing import List


class Trie:

    def __init__(self):
        # Just remember every inserted word verbatim.
        self.words: List[str] = []

    def insert(self, word: str) -> None:
        self.words.append(word)

    def search(self, word: str) -> bool:
        # A word is present only if it was inserted exactly.
        for stored in self.words:
            if stored == word:
                return True
        return False

    def startsWith(self, prefix: str) -> bool:
        # Every trie contains the empty prefix, even before any insert.
        if not prefix:
            return True
        # Any stored word beginning with prefix satisfies the query.
        for stored in self.words:
            if len(stored) >= len(prefix) and stored[: len(prefix)] == prefix:
                return True
        return False


# Your Trie object will be instantiated and used as follows:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N × L)` per query

`search` and `startsWith` each compare against all `N` stored words, and each comparison touches up to `L` characters, so a single query costs `O(N × L)`. `insert` is `O(1)` amortized.

##### Space Complexity: `O(total characters)`

Every inserted word is kept in full with no prefix sharing, so storage is the sum of all word lengths.

#### Key Insights

- This is the baseline you write before knowing what a trie is: keep the data,
  scan on demand.
- It wastes the structure inherent in the problem; repeated prefixes are stored
  and compared over and over instead of being shared.
- The linear scan per query is exactly what a trie removes by walking one node per
  character regardless of how many words are stored.

### Dictionary Children

#### Derivation

The Brute Force flaw is that every query pays for every stored word, re-comparing shared prefixes each time. The repair is to store those prefixes once: a [trie](https://en.wikipedia.org/wiki/Trie) lays strings out character by character along tree paths, so words with a common prefix walk the same nodes and a query follows one node per character of its own input, never touching the rest of the collection.

Two representation choices remain. For the node, a dictionary mapping a character to its child node is compact and gives constant-time child access. And because a path can be a prefix of a longer word (as `"app"` is of `"apple"`), reaching a node cannot by itself mean "a word ends here": a sentinel key `"$"` on the final node records that. Without it, inserting `"apple"` would make `search("app")` true. The steps:

1. Each node is a `dict`. A child entry maps a character to the next node; a
   special sentinel key `"$"` flags that a complete word ends at this node.
2. `insert` walks the characters of `word`, creating missing child dicts via
   `setdefault`, then sets the sentinel on the final node.
3. `search` walks the word with the `_find` helper; it returns `True` only when
   the path exists and the terminal node carries the `"$"` sentinel.
4. `startsWith` reuses `_find`; reaching any node along the prefix path is enough,
   regardless of whether a word ends there.

#### Walkthrough

Let us run the Dictionary Children solution on Example 1, watching `self.root` grow. Nested braces below are the child dictionaries; `$` marks the sentinel.

```text
Trie()               root = {}
insert("apple")      walk a -> p -> p -> l -> e, setdefault creates each child
                     root = {a: {p: {p: {l: {e: {$}}}}}}
search("apple")      _find follows a,p,p,l,e to node {$}; "$" present -> true
search("app")        _find follows a,p,p to node {l: ...}; no "$" -> false
startsWith("app")    _find follows a,p,p; node reached, that is enough -> true
insert("app")        walk a,p,p; every child already exists, nothing is created;
                     set the sentinel on the node reached
                     root = {a: {p: {p: {$, l: {e: {$}}}}}}
search("app")        _find follows a,p,p to node {$, l: ...}; "$" present -> true
```

The second insert is the trie's whole point in miniature: `insert("app")` allocates no nodes, because the path `a -> p -> p` already exists inside `"apple"`'s path; it only plants the `"$"` sentinel on the shared node. That sentinel is also what separates the two `search("app")` calls: the node existed all along (hence `startsWith("app")` was already `true`), but `search` demanded the sentinel. Collecting the returns gives `[null, null, true, false, true, null, true]`, matching the expected Output.

#### Solution

The code is the walkthrough's descent written down, with the shared walk factored into `_find`.

```python
class Trie:

    def __init__(self):
        # Each node is a dict of child character -> child node.
        # The sentinel key "$" marks the end of a complete word.
        self.root: dict = {}

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and "$" in node

    def startsWith(self, prefix: str) -> bool:
        return self._find(prefix) is not None

    def _find(self, s: str) -> dict | None:
        # Walk down the trie following s; return the node reached or None.
        node = self.root
        for ch in s:
            if ch not in node:
                return None
            node = node[ch]
        return node


# Your Trie object will be instantiated and used as follows:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(L)` per operation

`insert`, `search`, and `startsWith` each traverse one node per character of the input string of length `L`, performing constant-time dictionary work at each step.

##### Space Complexity: `O(total characters)`

In the worst case, with no shared prefixes, each inserted character creates a new node, so storage is proportional to the sum of all inserted word lengths. Shared prefixes reduce this in practice.

#### Key Insights

- A dictionary per node gives `O(1)` child lookup over the 26-letter alphabet
  without preallocating fixed-size arrays.
- The `"$"` sentinel cleanly separates "a word ends here" from "this is only a
  prefix," which is the crux of correct `search` versus `startsWith` behavior.
- `setdefault` collapses the "create child if absent, then descend" pattern into
  a single expression.
- Factoring the shared descent into `_find` removes duplication between `search`
  and `startsWith`.

### Fixed Array Children

#### Derivation

The dictionary node pays a hash lookup per character, and each dict carries per-object overhead. The constraints hand us a repair: inputs are lowercase English letters only, so a node can never have more than 26 distinct children, and the letter itself can *be* the index. Replace each node's dictionary with a fixed-size list of 26 slots, mapping `ch` to slot `ord(ch) - ord("a")`, where `None` means no child along that edge. With a class-based `TrieNode` there is no room for a sentinel key, so a dedicated `is_end` boolean carries the word-end flag instead. Indexing into a contiguous array is the fastest possible child lookup, which is why this layout is common in performance-sensitive [trie implementations](https://en.wikipedia.org/wiki/Trie). The steps:

1. Each `TrieNode` holds a 26-element `children` list initialized to `None` and an
   `is_end` flag that is `False` until a word terminates there.
2. `insert` converts each character to `index = ord(ch) - ord("a")`, creating a
   child node when `children[index]` is `None`, then marks the final node's `is_end`.
3. `search` walks the word via the `_find` helper and checks that the reached node
   has `is_end` set.
4. `startsWith` reuses `_find`; any reachable node along the prefix path suffices.

#### Walkthrough

Let us run the Fixed Array Children solution on Example 1. The structure is the same tree as in the Dictionary Children walkthrough; what changes is how a child is found. The letters involved map to slots `a = 0`, `p = 15`, `l = 11`, `e = 4` (each computed as `ord(ch) - ord("a")`). Nodes are named by the prefix they represent.

```text
Trie()               root: children all None, is_end False
insert("apple")      root.children[0]         is None -> new node (a)
                     (a).children[15]         is None -> new node (ap)
                     (ap).children[15]        is None -> new node (app)
                     (app).children[11]       is None -> new node (appl)
                     (appl).children[4]       is None -> new node (apple)
                     (apple).is_end = True
search("apple")      _find follows slots 0,15,15,11,4 to (apple); is_end -> true
search("app")        _find follows slots 0,15,15 to (app); is_end False -> false
startsWith("app")    _find follows slots 0,15,15; node reached -> true
insert("app")        slots 0,15,15 all occupied, no nodes created;
                     (app).is_end = True
search("app")        _find follows slots 0,15,15 to (app); is_end True -> true
```

As before, the second insert creates nothing: the path for `"app"` already lives inside `"apple"`'s path, and only the `is_end` flag on node `(app)` flips. The flag plays exactly the role the `"$"` sentinel played in the dictionary layout, turning `search("app")` from `false` to `true` while `startsWith("app")` was true throughout. The returns collect to `[null, null, true, false, true, null, true]`, matching the expected Output.

#### Solution

The code is the slot walk from the walkthrough, with the descent again factored into `_find`.

```python
from typing import List, Optional


class TrieNode:

    def __init__(self):
        # One slot per lowercase letter; None means no child along that edge.
        self.children: List[Optional["TrieNode"]] = [None] * 26
        # Marks whether a complete word ends at this node.
        self.is_end: bool = False


class Trie:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            index = ord(ch) - ord("a")
            if node.children[index] is None:
                node.children[index] = TrieNode()
            node = node.children[index]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        return self._find(prefix) is not None

    def _find(self, s: str) -> "TrieNode | None":
        # Walk down the trie following s; return the node reached or None.
        node = self.root
        for ch in s:
            index = ord(ch) - ord("a")
            if node.children[index] is None:
                return None
            node = node.children[index]
        return node


# Your Trie object will be instantiated and used as follows:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(L)` per operation

`insert`, `search`, and `startsWith` each visit one node per character of the input string of length `L`, with constant-time array indexing at each step.

##### Space Complexity: `O(26 × number of nodes)`

Every node allocates a full 26-slot array regardless of how many children it actually has, so memory is proportional to the node count times the alphabet size. This is wasteful for sparse tries but bounded and predictable.

#### Key Insights

- Array indexing by `ord(ch) - ord("a")` gives the tightest constant-factor child
  lookup, avoiding hashing entirely.
- A separate `is_end` flag plays the same role as the dictionary sentinel,
  distinguishing a stored word from a mere prefix.
- The fixed alphabet size is what makes the array layout viable; it relies on the
  constraint that inputs contain only lowercase English letters.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(N × L)` per `search`/`startsWith` query - scans all `N` stored words, comparing up to `L` characters each
- **Dictionary Children**: `O(L)` per operation, with constant-time hashed child lookup at each character
- **Fixed Array Children**: `O(L)` per operation, with constant-time array indexing at each character

### Space Complexity

- **Brute Force**: `O(total characters)` - stores every word in full with no prefix sharing
- **Dictionary Children**: `O(total characters)` - each node stores only the children it actually has
- **Fixed Array Children**: `O(26 × number of nodes)` - each node reserves a full 26-slot array even when mostly empty

### Trade-offs

- **Brute Force** is trivial to write and uses no tree at all, but each query rescans the entire collection, which fails the call-volume constraints at scale
- **Dictionary Children** is memory-efficient for sparse tries and adapts to any character set without changes, at the cost of hashing overhead per lookup
- **Fixed Array Children** offers the fastest possible child access through direct indexing, but wastes memory on empty slots and is tied to a fixed alphabet

### When to Use Each

- **Brute Force**: Only as a conceptual baseline; the per-query scan is too slow for the problem's call volume
- **Dictionary Children**: The default choice when the alphabet is large or unknown, or when tries are sparse and memory matters
- **Fixed Array Children**: When the alphabet is small and fixed (such as lowercase English letters) and raw lookup speed is the priority

### Optimization Notes

- The trie's whole point is replacing the Brute Force per-query scan with a walk of one node per character, making query cost depend on the query length `L` rather than the number of stored words `N`
- Both trie layouts share the same `O(L)` time complexity; the real distinction is the constant factor on lookups versus the memory footprint per node
- The array layout trades memory for speed, which pays off in hot paths over a small fixed alphabet but becomes prohibitive for Unicode-scale character sets
- The dictionary layout generalizes for free to any character set, making it the safer default unless profiling shows child lookup is a bottleneck
