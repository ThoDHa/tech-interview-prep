# [Dynamic Prefix Search Collection](https://www.fastprep.io/problems/amazon-prefix-search-collection)

**Medium** | **NN minutes** | **Trie, String, Design**

Implement a dynamic collection of lowercase words. Process the finite array operations from left to right.

Each operation has one of these forms:

INSERT word: add word to the collection. Inserting a word that is already present does not create a duplicate.SEARCH prefix: return up to three stored words that begin with prefix, ordered lexicographically.The collection starts empty. Return one row for every SEARCH operation, in command order. INSERT operations do not produce output.

## Examples

### Example 1

**Input:** `operations = ["INSERT mouse","INSERT mobile","INSERT moneypot","INSERT monitor","INSERT mousepad","SEARCH mo","SEARCH mou"]`

**Output:** `[["mobile","moneypot","monitor"],["mouse","mousepad"]]`

**Explanation:** The first search keeps the three lexicographically smallest matches for mo. The longer prefix mou has only two matches.

### Example 2

**Input:** `operations = ["INSERT app","INSERT apple","SEARCH ap","INSERT apex","INSERT app","SEARCH ap","SEARCH z"]`

**Output:** `[["app","apple"],["apex","app","apple"],[]]`

**Explanation:** The second insertion of app is idempotent. After apex is added, it is first lexicographically. No stored word begins with z.

## Constraints

- `1 <= operations.length <= 100000.`
- `Every operation is exactly one documented command with one separating space.`
- `Every word and prefix contains 1 to 100 lowercase English letters.`
- `The total number of characters across all operations is at most 1000000.`
- `At least one operation is SEARCH.`

## Solutions

### Linear Scan per Search

#### Derivation

The most literal reading of the design: the collection is "the set of words inserted so far", and a `SEARCH` is one question asked of that set. Keep the words in a set, answer each search by filtering the whole collection through the prefix test, sorting the matches, and slicing off the first three. `INSERT` is a set add, which is idempotent on its own and so carries the statement's no-duplicates rule for free:

1. Parse each operation once with `operation.split(" ", 1)` into `command` and
   `payload`.
2. `INSERT` adds `payload` to `stored_words`; a repeated word lands on the same
   set entry.
3. `SEARCH` builds `matches` from every stored word with
   `word.startswith(payload)`, sorts it, and appends
   `matches[:SUGGESTION_LIMIT]` to `results`.
4. Return `results`, one row per `SEARCH` in command order.

#### Walkthrough

Example 1: the five inserts leave `stored_words = {mouse, mobile, moneypot, monitor, mousepad}`. Each search scans the whole set:

```text
SEARCH mo    prefix test keeps mouse, mobile, moneypot, monitor, mousepad
             sorted: mobile, moneypot, monitor, mouse, mousepad
             first three -> ["mobile", "moneypot", "monitor"]
SEARCH mou   prefix test keeps mouse, mousepad
             sorted -> ["mouse", "mousepad"]
```

The returned rows are `[["mobile", "moneypot", "monitor"], ["mouse", "mousepad"]]`, matching the expected Output. Example 2 exercises the duplicate rule: the second `INSERT app` adds to a set that already holds `app`, so the collection still holds `app` and `apple` once, and the first search returns `["app", "apple"]`.

#### Solution

The code is the parse, the set, and the filter-sort-slice per search.

```python
from typing import List, Set


SUGGESTION_LIMIT = 3


class Solution:
    def solve(self, operations: List[str]) -> List[List[str]]:
        """Return one suggestion row per SEARCH operation.

        Time:  INSERT is O(1) on average; each SEARCH scans all N stored
            words with an O(P) prefix test plus a sort of the matches.
        Space: O(N * L) to store the collection of N words of length L.
        """
        stored_words: Set[str] = set()
        results: List[List[str]] = []

        for operation in operations:
            command, payload = operation.split(" ", 1)
            if command == "INSERT":
                stored_words.add(payload)
            else:
                matches = [word for word in stored_words
                           if word.startswith(payload)]
                matches.sort()
                results.append(matches[:SUGGESTION_LIMIT])

        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N × P)` per search

Each `SEARCH` scans all `N` stored words with an `O(P)` prefix test each, then sorts the `M` matches for `O(M log M)` more; `INSERT` is `O(1)` on average. With `Q` operations the whole run costs `O(Q × N × P)` in the worst case.

##### Space Complexity: `O(N × L)`

The set holds every distinct inserted word in full; the matches list holds at most `N` words during one search.

#### Key Insights

- The set is the whole design: it buys idempotent inserts without a single extra line, because adding a duplicate is a no-op.
- Sorting the full match list wastes work when more than three words match: the sort orders matches the slice will throw away.
- Nothing is shared between searches: every `SEARCH` re-reads the entire collection, which is the cost both later approaches attack.

### Sorted List with Binary Search

#### Derivation

The linear scan pays `O(N × P)` per search to find words that, in sorted order, sit together in one contiguous block: every word beginning with `prefix` is at least `prefix` itself, and the first stored word that sorts at or after `prefix` starts the block. Keeping the collection sorted at all times turns the search into a location problem: `bisect_left` finds the block's start in `O(log N)` comparisons, and the suggestions are the next words that still pass the prefix test, stopping at the first word that diverges or at three, whichever comes first. The price moves to `INSERT`, which must splice the word into its sorted position:

1. Keep `sorted_words`, a list maintained in ascending order.
2. `INSERT` computes `word_index = bisect_left(sorted_words, payload)`; when
   `sorted_words[word_index]` already equals `payload`, the insert is a
   duplicate and is skipped, which is the idempotence rule.
3. Otherwise `sorted_words.insert(word_index, payload)` splices the word in.
4. `SEARCH` starts at `word_index = bisect_left(sorted_words, payload)` and
   collects forward while `sorted_words[word_index].startswith(payload)`,
   stopping after `SUGGESTION_LIMIT` words.
5. Return the collected rows in command order.

#### Walkthrough

Example 2, where the duplicate insert and the `apex`-before-`app` ordering both matter. `apex` sorts before `app` because they diverge at the third letter (`e` < `p`), and `app` sorts before `apple` because it is a prefix of it:

```text
INSERT app     sorted_words = ["app"]
INSERT apple   spliced after app        sorted_words = ["app", "apple"]
SEARCH ap      bisect_left -> 0; "app" matches (1), "apple" matches (2)
               end of list -> ["app", "apple"]
INSERT apex    bisect_left -> 0 (apex < app); insert at front
               sorted_words = ["apex", "app", "apple"]
INSERT app     bisect_left -> 1, sorted_words[1] == "app" -> duplicate, skip
SEARCH ap      bisect_left -> 0; "apex" (1), "app" (2), "apple" (3) -> limit
               -> ["apex", "app", "apple"]
SEARCH z       bisect_left -> 3 == len, no word at or after "z" -> []
```

The rows collect to `[["app", "apple"], ["apex", "app", "apple"], []]`, matching the expected Output.

#### Solution

The code is the maintained sorted list: bisect to insert and to locate, then a forward scan that stops at three.

```python
from bisect import bisect_left
from typing import List


SUGGESTION_LIMIT = 3


class Solution:
    def solve(self, operations: List[str]) -> List[List[str]]:
        """Return one suggestion row per SEARCH operation.

        Time:  INSERT is O(N) worst case (the splice shifts the tail) with
            O(log N * L) comparisons to find it; SEARCH is O(log N * L) to
            locate the block plus the scan of its first few entries.
        Space: O(N * L) for the sorted word list.
        """
        sorted_words: List[str] = []
        results: List[List[str]] = []

        for operation in operations:
            command, payload = operation.split(" ", 1)
            if command == "INSERT":
                word_index = bisect_left(sorted_words, payload)
                if (word_index == len(sorted_words)
                        or sorted_words[word_index] != payload):
                    sorted_words.insert(word_index, payload)
            else:
                word_index = bisect_left(sorted_words, payload)
                matches: List[str] = []
                while (word_index < len(sorted_words)
                       and sorted_words[word_index].startswith(payload)):
                    matches.append(sorted_words[word_index])
                    if len(matches) == SUGGESTION_LIMIT:
                        break
                    word_index += 1
                results.append(matches)

        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log N × L)` per search

`bisect_left` performs `O(log N)` string comparisons of up to `L` characters, and the forward scan touches at most `SUGGESTION_LIMIT + 1` entries (one extra to see the block end). `INSERT` pays the same lookup plus an `O(N)` splice that shifts the list tail.

##### Space Complexity: `O(N × L)`

The sorted list holds every distinct word; the matches list holds at most three.

#### Key Insights

- Sorted order makes all words sharing a prefix contiguous, so a search becomes one binary lookup plus a scan of the block's head.
- The duplicate check before `insert` is the idempotence rule: `bisect_left` landing on an equal word proves the insert was already applied.
- `INSERT` inherits the search's `O(N)` weakness in a different costume: the binary lookup is cheap, but splicing into a Python list shifts every later word.
- The block-scan early exit matters: without the `SUGGESTION_LIMIT` break, a popular prefix would walk its whole block, which is exactly the linear cost this design was meant to avoid.

### Trie with Sorted-Child DFS

#### Derivation

Both earlier designs process a search by asking every stored word (or a slice of sorted storage) about a prefix it may not share. The trie removes the mismatch: words share their prefix paths in the tree, so `INSERT` walks one node per character and a `SEARCH` walks the prefix once and then explores only the subtree that actually hangs below it. Two details finish the design. Lexicographic order must come out of the exploration itself, and it does: visiting a node's word mark before its children, and its children in sorted letter order, emits words exactly in dictionary order, including the prefix-word beat (`app` before `apple`, because the word end sits on the node above its children). And the three-suggestion cap turns the walk into a bounded one: once three words are collected, the exploration stops, so a search touches the prefix path plus at most the characters of three reported words:

1. Each `TrieNode` holds `children`, a dictionary mapping a letter to its
   child, and `word`, set to the complete word when one ends at the node.
2. `INSERT` walks `payload` letter by letter with
   `children.setdefault(letter, TrieNode())`, then sets `node.word = payload`;
   re-inserting a stored word re-walks the same nodes and re-sets the same
   mark, which is the idempotence rule.
3. `SEARCH` walks the prefix; falling off the trie yields an empty row.
4. From the node reached, `collect_matches` appends `node.word` when set, then
   recurses into `sorted(node.children)`, stopping for good once
   `len(matches)` reaches `SUGGESTION_LIMIT`.
5. Return the collected rows in command order.

#### Walkthrough

Example 1: the five inserts grow the trie below the `m-o` node into three subtrees, `b` (mobile), `n` (moneypot, monitor), and `u` (mouse, mousepad). The two searches walk it:

```text
SEARCH mo    walk m -> o; sorted children of mo: b, n, u
             b: i -> l -> e records "mobile"                    (1 of 3)
             n: children e, i; e: y -> p -> o -> t records "moneypot"  (2 of 3)
                i: t -> o -> r records "monitor"                (3 of 3) -> stop
             -> ["mobile", "moneypot", "monitor"]
SEARCH mou   walk m -> o -> u; child s
             s -> e: node holds word "mouse", recorded before
             its children (1 of 2)
             e's child p -> a -> d records "mousepad"           (2 of 2)
             -> ["mouse", "mousepad"]
```

The `mouse`-before-`mousepad` order is the word-mark-before-children rule at work: the word end and the longer word's continuation share one node, and the shorter word is reported first. The rows match the expected Output. Example 2 adds the two design beats: the second `INSERT app` re-walks the existing `a-p-p` path and re-sets the same mark, creating nothing; and `SEARCH ap` finds the reached node with sorted children `e`, `l`:

```text
SEARCH ap    walk a -> p; sorted children: e, l
             e -> x records "apex"        (1 of 3)
             node word "app" recorded     (2 of 3)
             l -> e records "apple"       (3 of 3) -> stop
             -> ["apex", "app", "apple"]
SEARCH z     root has no z child -> []
```

`apex` is visited first because `e` sorts before `l`, exactly the lexicographic requirement. All three rows match the expected Output.

#### Solution

The code is the trie walk: parse, insert by walking, search by walking the prefix and then the bounded sorted-child DFS.

```python
from typing import Dict, List, Optional


SUGGESTION_LIMIT = 3


class TrieNode:
    def __init__(self) -> None:
        self.children: Dict[str, "TrieNode"] = {}
        self.word: Optional[str] = None


class Solution:
    def solve(self, operations: List[str]) -> List[List[str]]:
        """Return one suggestion row per SEARCH operation.

        Time:  O(total characters): INSERT walks one node per character;
            SEARCH walks the prefix plus at most the characters of three
            reported words.
        Space: O(total characters) for the trie nodes.
        """
        root = TrieNode()
        results: List[List[str]] = []

        def collect_matches(node: TrieNode, matches: List[str]) -> None:
            if node.word is not None:
                matches.append(node.word)
                if len(matches) == SUGGESTION_LIMIT:
                    return
            for letter in sorted(node.children):
                collect_matches(node.children[letter], matches)
                if len(matches) == SUGGESTION_LIMIT:
                    return

        for operation in operations:
            command, payload = operation.split(" ", 1)
            if command == "INSERT":
                node = root
                for letter in payload:
                    node = node.children.setdefault(letter, TrieNode())
                node.word = payload
            else:
                node = root
                for letter in payload:
                    node = node.children.get(letter)
                    if node is None:
                        break
                matches: List[str] = []
                if node is not None:
                    collect_matches(node, matches)
                results.append(matches)

        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(total characters)`

`INSERT` walks one node per character of its word. A `SEARCH` walks its `P` prefix characters, and the bounded DFS visits only nodes that are prefixes of stored words, stopping at the third report, so it touches at most the characters of the three reported words (each of length up to `L`): `O(P + 3 × L)` per search.

##### Space Complexity: `O(total characters)`

The trie holds one node per distinct prefix across all inserted words, which is bounded by the total characters constraint.

#### Key Insights

- The word mark sitting before the sorted children is what produces lexicographic order, including the prefix beat: a word that is a prefix of another is reported when its node is reached, before that node's subtree is explored.
- The `SUGGESTION_LIMIT` check after each append and after each child return stops the recursion mid-subtree the moment the third word lands; a check only after a full exploration would over-walk.
- Idempotent inserts need no test at all: re-walking an existing path and re-setting the same `word` mark changes nothing, so the duplicate rule is free.
- Sorting `node.children` on each visit costs `O(26 log 26)` per node, a constant; keeping children in a sorted structure would trade insert time for that constant and is not worth it at this alphabet size.

## Comparison of Solutions

### Time Complexity

- **Linear Scan per Search**: `O(N × P)` per search - every stored word takes one prefix test, plus a sort of the matches.
- **Sorted List with Binary Search**: `O(log N × L)` per search - one bisect plus a bounded scan; inserts pay an `O(N)` splice.
- **Trie with Sorted-Child DFS**: `O(P + 3 × L)` per search and `O(L)` per insert - one walk per operation, no scan of unrelated words.

### Space Complexity

- **Linear Scan per Search**: `O(N × L)` - the set of stored words.
- **Sorted List with Binary Search**: `O(N × L)` - the sorted word list.
- **Trie with Sorted-Child DFS**: `O(total characters)` - one node per distinct prefix, bounded by the constraint.

### Trade-offs

- **Linear Scan per Search**: the shortest code and an obvious correctness argument, but every search pays for every stored word, which collapses at `10^5` operations.
- **Sorted List with Binary Search**: fast searches through sorted contiguity, but the splice makes inserts quadratic in the worst case, so write-heavy workloads suffer.
- **Trie with Sorted-Child DFS**: both operations cost work proportional to their own input, at the price of the node machinery and the sorted-child discipline.

### When to Use Each

- **Linear Scan per Search**: prototypes and tiny collections, or as the cross-check oracle when testing the faster designs.
- **Sorted List with Binary Search (Recommended for read-heavy work)**: collections that change rarely and get searched often, where the amortized splice cost is acceptable.
- **Trie with Sorted-Child DFS**: the constraint-scale design, and the natural choice whenever inserts and searches interleave freely.

### Optimization Notes

- The trie's bounded search relies on every visited node being a prefix of some stored word; a trie over arbitrary keys would need an additional word-count per node to keep the same guarantee.
- Storing the complete word string in each terminal node duplicates characters; storing an index into an inserted-words array trims memory if needed.
- The `matches[:SUGGESTION_LIMIT]` slice in the linear scan sorts more words than it keeps; `heapq.nsmallest(SUGGESTION_LIMIT, matches)` would bound that pass, though the scan itself remains the real cost.
- Recursion depth in the trie DFS is bounded by the 100-character word limit, so Python's recursion limit is never a concern here.
