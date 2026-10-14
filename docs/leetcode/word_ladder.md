# [Word Ladder](https://leetcode.com/problems/word-ladder/)

**Hard** | **45 minutes** | **Hash Table, String, Breadth-First Search**

**Pattern:** [Shortest Path](../patterns/shortest_path/intuition.md)

**Algorithm:** [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) · [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) · [Bidirectional search](https://en.wikipedia.org/wiki/Bidirectional_search)

**Practice:** [`practice/word_ladder/solution.py`](../../practice/word_ladder/solution.py)

A **transformation sequence** from word `beginWord` to word `endWord` using a dictionary `wordList` is a sequence of words `beginWord -> s1 -> s2 -> ... -> sk` such that:

- Every adjacent pair of words differs by a single letter.
- Every `si` for `1 <= i <= k` is in `wordList`. Note that `beginWord` does not need to be in `wordList`.
- `sk == endWord`

Given two words, `beginWord` and `endWord`, and a dictionary `wordList`, return *the **number of words** in the **shortest transformation sequence** from* `beginWord` *to* `endWord`*, or* `0` *if no such sequence exists.*

## Examples

### Example 1

**Input:** `beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log","cog"]`

**Output:** `5`

**Explanation:** One shortest transformation sequence is `"hit" -> "hot" -> "dot" -> "dog" -> "cog"`, which is 5 words long.

### Example 2

**Input:** `beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log"]`

**Output:** `0`

**Explanation:** The endWord `"cog"` is not in wordList, therefore there is no valid transformation sequence.

## Constraints

- `1 <= beginWord.length <= 10`
- `endWord.length == beginWord.length`
- `1 <= wordList.length <= 5000`
- `wordList[i].length == beginWord.length`
- `beginWord`, `endWord`, and `wordList[i]` consist of lowercase English letters.
- `beginWord != endWord`
- All the strings in `wordList` are **unique**.

## Deriving the Solution

Every solution below rests on the same reformulation: words are nodes, two words share an edge when they differ in exactly one letter, and the answer is the number of words on a shortest path from `beginWord` to `endWord` in that unweighted graph. [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) is the natural engine, because it visits words in order of distance; the approaches differ in how the edges are discovered and in how many ends the search grows from.

1. **Start literal.** Materialize the graph: compare every pair of words to find
   the one-letter edges, then BFS from `beginWord`. The all-pairs comparison costs `O(N² × M)`: see [Brute Force Graph BFS](#brute-force-graph-bfs).
2. **Discover neighbors on the fly.** Most pairs are not neighbors, so comparing
   them all is wasted work. Reverse the direction: from the current word, generate its `25 × M` one-letter variants and keep those found in a hash set of the dictionary. The BFS is unchanged and the total drops to `O(M² × N)`: see [BFS with Word-by-Word Comparison](#bfs-with-word-by-word-comparison).
3. **Precompute neighbors by pattern.** Generation still probes mostly gibberish
   strings. Bucketing words under wildcard patterns (`"hot" -> "*ot", "h*t", "ho*"`) turns neighbor lookup into a hash hit that returns only real words, at the price of `O(M² × N)` extra space: see [BFS with Pattern Matching](#bfs-with-pattern-matching).
4. **A wrong turn worth seeing.** Depth-first search also reaches `endWord`, but
   it does not visit words in distance order, must run every path to completion, and admits no sound memoization, degrading toward factorial time: see [Backtracking DFS](#backtracking-dfs).
5. **Halve the depth.** One-ended BFS explores on the order of `b^d` words for
   branching factor `b` and distance `d`. Growing frontiers from both ends and always expanding the smaller one meets in the middle at roughly `2 × b^(d/2)`: see [Bidirectional BFS](#bidirectional-bfs).

## Solutions

### Brute Force Graph BFS

#### Derivation

The reformulation splits the problem into two questions: which words are neighbors, and how to find the shortest path between two nodes. The literal plan answers each with the most direct tool available. For neighbors, two words are adjacent when they differ in exactly one position, which a hand-written character scan (`is_one_diff`) decides for any pair, so compare all pairs. For the path, [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) expands all words reachable in `k` steps before any reachable in `k + 1`, so the first arrival at `endWord` uses the fewest words.

1. Collect every word as a node in `nodes`, including `beginWord`, since the path
   may start from a word that is not in `wordList`.
2. Compare every pair of words with `is_one_diff`, building an `adjacency` list for
   each word from the matches.
3. Run BFS from `(beginWord, 1)`, carrying `length`, the number of words used so
   far, and return `length` the first time `endWord` is dequeued.

#### Walkthrough

Let us trace Example 1: `beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log","cog"]`.

First, `endWord` ("cog") is in `wordList`, so we proceed. The nodes are `beginWord` plus every word: `["hit","hot","dot","dog","lot","log","cog"]`. The all-pairs `is_one_diff` scan builds this adjacency list (each word points to the words that differ from it by exactly one letter):

| Word | Neighbors |
|------|-----------|
| `hit` | `hot` |
| `hot` | `hit`, `dot`, `lot` |
| `dot` | `hot`, `dog`, `lot` |
| `dog` | `dot`, `log`, `cog` |
| `lot` | `hot`, `dot`, `log` |
| `log` | `dog`, `lot`, `cog` |
| `cog` | `dog`, `log` |

Now BFS runs from `("hit", 1)` with `visited = {hit}`. Each row below shows the pair just dequeued, then any unvisited neighbors enqueued (each carries `length + 1`), and the queue that remains:

| Step | Dequeued `(word, length)` | New neighbors enqueued | Queue after step |
|------|---------------------------|------------------------|------------------|
| 1 | `(hit, 1)` | `(hot, 2)` | `[(hot, 2)]` |
| 2 | `(hot, 2)` | `(dot, 3)`, `(lot, 3)` | `[(dot, 3), (lot, 3)]` |
| 3 | `(dot, 3)` | `(dog, 4)` | `[(lot, 3), (dog, 4)]` |
| 4 | `(lot, 3)` | `(log, 4)` | `[(dog, 4), (log, 4)]` |
| 5 | `(dog, 4)` | `(cog, 5)` | `[(log, 4), (cog, 5)]` |
| 6 | `(log, 4)` | none (`dog`, `lot`, `cog` all already visited) | `[(cog, 5)]` |
| 7 | `(cog, 5)` | `current_word == endWord`, so return `5` | - |

At step 7 the dequeued word equals `endWord`, so BFS returns `5`. This matches the expected Output `5`, and the path that produced it is `"hit" -> "hot" -> "dot" -> "dog" -> "cog"`, exactly 5 words long.

#### Solution

The code is the two phases of the walkthrough in order: the all-pairs adjacency build, then the queue loop.

```python
from collections import deque
from typing import List

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0

        # beginWord is a valid start even though it may not be in wordList.
        nodes = [beginWord] + wordList

        def is_one_diff(a: str, b: str) -> bool:
            diff = 0
            for i in range(len(a)):
                if a[i] != b[i]:
                    diff += 1
                    if diff > 1:
                        return False
            return diff == 1

        # Build the graph explicitly by comparing every pair of words.
        adjacency = {word: [] for word in nodes}
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if is_one_diff(nodes[i], nodes[j]):
                    adjacency[nodes[i]].append(nodes[j])
                    adjacency[nodes[j]].append(nodes[i])

        # Plain BFS over the precomputed adjacency lists.
        queue = deque([(beginWord, 1)])
        visited = {beginWord}

        while queue:
            current_word, length = queue.popleft()

            if current_word == endWord:
                return length

            for neighbor in adjacency[current_word]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, length + 1))

        return 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N² × M)`

`M` is the word length and `N` is the number of words. Building the graph compares all `N²` pairs, and each comparison scans up to `M` characters, giving `O(N² × M)`. The BFS that follows visits each node and edge once, which the graph construction already dominates.

##### Space Complexity: `O(N² + M × N)`

The adjacency lists can hold up to `O(N²)` edges in the worst case, and the queue, visited set, and node list together hold up to `N` words of length `M`.

#### Key Insights

- Splitting the work into "build the graph, then BFS it" mirrors how the problem is naturally modeled as a shortest path.
- The all-pairs comparison is the obvious but wasteful step: it costs `O(N²)` even when most words are not neighbors.
- The BFS half is already optimal; only the neighbor discovery needs improving, which the next solutions target.

### BFS with Word-by-Word Comparison

#### Derivation

The brute force spends nearly all its time building edges it never walks: all `N²` pairs are compared even though each word has only a handful of true neighbors. The repair is to flip the neighbor question at search time: instead of asking "which known words is this word adjacent to?", ask "which strings are one letter away, and which of those are known words?". Each word has only `25 × M` one-letter variants, and testing one against a hash set costs `O(1)`, so neighbors can be discovered on demand with no precomputed graph. The [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) shell stays exactly as before:

1. Return `0` immediately when `endWord` is not in `wordList`; otherwise convert
   the list to `word_set` for `O(1)` membership tests.
2. Start the queue at `(beginWord, 1)`: `beginWord` counts as the first word of
   the sequence.
3. For the word at the front of the queue, build every variant `new_word` by
   replacing each position `i` with each of the 26 lowercase letters, skipping the letter already there.
4. If `new_word` equals `endWord`, the sequence closes: return `length + 1`.
   Otherwise enqueue `(new_word, length + 1)` when it is in `word_set` and unvisited, marking it visited at enqueue time so no word enters the queue twice.

#### Walkthrough

Let us trace Example 1: `beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log","cog"]`. `endWord` is present, so the search starts with `queue = [("hit", 1)]` and `visited = {hit}`. Each line dequeues one word and lists the generated variants that survive the filters (in `word_set`, not yet visited):

```text
dequeue (hit, 1)   "hot" (h_t) in word_set              enqueue (hot, 2)
dequeue (hot, 2)   "dot", "lot" (_ot) in word_set       enqueue (dot, 3), (lot, 3)
dequeue (dot, 3)   "hot" visited; "dog" (do_) is new    enqueue (dog, 4)
dequeue (lot, 3)   "hot", "dot" visited; "log" is new   enqueue (log, 4)
dequeue (dog, 4)   variant "cog" == endWord             return 4 + 1 = 5
```

Two details are easy to miss. When `hot` is expanded, the variant `hit` is generated but rejected: `beginWord` was never added to `word_set`, and it is already visited anyway. And the final step never consults `word_set` at all: expanding `dog`, position `0` reaches `"cog"` at letter `c`, the `new_word == endWord` test fires first, and the function returns `length + 1 = 5`. That matches Example 1's Output, along the sequence `hit -> hot -> dot -> dog -> cog`.

#### Solution

The code is the dequeue loop from the trace, with the two nested loops building `new_word` position by position.

```python
from collections import deque
from typing import List

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        # If endWord is absent, no transformation can ever reach it.
        if endWord not in wordList:
            return 0

        # Set membership is O(1); the list scan above is the only linear check.
        word_set = set(wordList)

        # Queue holds (word, words_used_so_far); beginWord counts as the first word.
        queue = deque([(beginWord, 1)])
        visited = {beginWord}

        while queue:
            current_word, length = queue.popleft()

            # Try every one-letter change at every position.
            for i in range(len(current_word)):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    if c == current_word[i]:
                        continue

                    new_word = current_word[:i] + c + current_word[i + 1:]

                    if new_word == endWord:
                        return length + 1

                    if new_word in word_set and new_word not in visited:
                        visited.add(new_word)
                        queue.append((new_word, length + 1))

        return 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(M² × N)`

`M` is the word length and `N` is the number of words. Each of the `N` words is dequeued at most once. For each word we try `M` positions across 26 letters, and building each candidate string with slicing costs `O(M)`. The `26` is a constant, leaving `O(M² × N)`.

##### Space Complexity: `O(M × N)`

The `word_set`, `visited` set, and queue each hold up to `N` words of length `M`, giving `O(M × N)`.

#### Key Insights

- BFS is the natural fit for shortest paths in unweighted graphs because it discovers nodes in order of distance.
- Marking a word visited at enqueue time, not dequeue time, avoids inserting the same word multiple times.
- Generating candidates directly (no preprocessing) keeps the logic simple, at the cost of producing words that may not exist in the dictionary.

### BFS with Pattern Matching

#### Derivation

Generating variants probes `25 × M` strings per dequeued word, and most of them are gibberish that fails the set lookup. Those wasted probes can be precomputed away: two words differ in one letter exactly when masking that position makes them equal, so file every word under its `M` wildcard patterns (`"hot" -> "*ot", "h*t", "ho*"`). Words sharing a bucket are precisely the one-letter neighbors, and the [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) can look neighbors up by bucket instead of generating candidates:

1. For every word in `all_words` (`wordList` plus `beginWord`), build its `M`
   patterns and append the word under each in `pattern_dict`.
2. Run the same BFS from `(beginWord, 1)`.
3. For the dequeued word, form its `M` patterns and visit every `neighbor`
   recorded under them, skipping visited ones.
4. Return `length + 1` the first time a neighbor equals `endWord`.

By precomputing patterns, the search only ever touches words that actually exist in the dictionary, rather than the full 26-letter expansion at every step.

#### Walkthrough

The pattern map is built once up front. On Example 1, `all_words = ["hot","dot","dog","lot","log","cog","hit"]` produces these buckets (every bucket not shown holds a single word):

```text
*ot -> [hot, dot, lot]     h*t -> [hot, hit]     do* -> [dot, dog]
*og -> [dog, log, cog]     lo* -> [lot, log]
```

BFS then walks bucket mates instead of generated strings:

```text
dequeue (hit, 1)   buckets *it, h*t, hi*: new mate "hot"     enqueue (hot, 2)
dequeue (hot, 2)   bucket *ot: "dot", "lot" new              enqueue (dot, 3), (lot, 3)
dequeue (dot, 3)   bucket do*: "dog" new                     enqueue (dog, 4)
dequeue (lot, 3)   bucket lo*: "log" new                     enqueue (log, 4)
dequeue (dog, 4)   bucket *og: mate "cog" == endWord         return 4 + 1 = 5
```

Every word the search touches is a real dictionary word: no gibberish candidate is ever formed. Expanding `dog`, its first pattern `*og` lists `[dog, log, cog]`: `dog` and `log` are already visited, and `cog` trips the `endWord` check, returning `5`. That matches Example 1's Output along `hit -> hot -> dot -> dog -> cog`.

#### Solution

The code builds `pattern_dict` up front; the BFS loop then reads neighbors straight out of the buckets.

```python
from collections import deque, defaultdict
from typing import List

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0

        # Group words by wildcard pattern: "hot" -> "*ot", "h*t", "ho*".
        # Words sharing a pattern are exactly one transformation apart.
        pattern_dict = defaultdict(list)

        all_words = wordList + [beginWord]
        for word in all_words:
            for i in range(len(word)):
                pattern = word[:i] + "*" + word[i + 1:]
                pattern_dict[pattern].append(word)

        queue = deque([(beginWord, 1)])
        visited = {beginWord}

        while queue:
            current_word, length = queue.popleft()

            for i in range(len(current_word)):
                pattern = current_word[:i] + "*" + current_word[i + 1:]

                for neighbor in pattern_dict[pattern]:
                    if neighbor == endWord:
                        return length + 1

                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, length + 1))

        return 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(M² × N)`

Preprocessing builds `M` patterns per word, each costing `O(M)` to slice, so the pattern dictionary is built in `O(M² × N)`. BFS then visits each word and pattern bucket once, bounded by the same order.

##### Space Complexity: `O(M² × N)`

The pattern dictionary stores `M` patterns per word, each of length `M`, giving `O(M² × N)` in addition to the queue and visited set.

#### Key Insights

- Wildcard patterns turn neighbor discovery into a hash lookup, avoiding the generation of words that are not in the dictionary.
- The tradeoff is higher memory: the pattern map is the dominant space cost.
- Including `beginWord` in the pattern map lets the search start from it even though it need not be in `wordList`.

### Backtracking DFS

#### Derivation

BFS owes its shortest-path guarantee to visiting words level by level; it is worth seeing what happens without that order. A [depth-first](https://en.wikipedia.org/wiki/Depth-first_search) search follows one transformation chain as deep as it can, backtracks, and tries the next, taking the minimum length over every complete path it finds:

1. From `current_word`, scan `word_set` for every word that differs by exactly one
   character (`is_one_diff`).
2. Recurse into each such neighbor, adding it to `visited` before the call and
   removing it afterward so `visited` always reflects the current path only.
3. The shortest path through this word is one plus the best result among its
   neighbors; `min_length` collects that minimum.
4. Return `min_length`, leaving it at `float("inf")` when no neighbor reaches the
   target, and translate `inf` to `0` at the top level.

DFS is included for contrast. It returns the correct answer, but because depth-first search does not visit nodes in distance order, it must explore every path to completion rather than stopping at the first arrival the way BFS does.

No memoization is used here. A cache keyed on `(current_word, target_word)` would be unsound: the result of `dfs` depends on which words the active path has already consumed, so a value computed while one path blocks certain words does not hold when a different path reaches the same word with a different `visited` set. Caching such path-dependent values inflates the recorded minimum and yields wrong answers, so the search recomputes each subproblem instead.

#### Walkthrough

Example 1's dictionary spawns a recursion tree far too large to trace by hand, so we use a tailored input that keeps the full tree small while still offering two competing routes: `beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","cog","cot"]`. The direct route is `hit -> hot -> cot -> cog` (4 words); the detour runs through `dot` and `dog` (5 words). The tree below indents one level per call; the iteration order over `word_set` does not matter, because every branch is explored either way:

```text
dfs(hit)   visited {hit}                     neighbor: hot
  dfs(hot)   visited {hit,hot}               neighbors: dot, cot
    dfs(dot)   visited {hit,hot,dot}         neighbors: cot, dog
      dfs(cot)   visited {hit,hot,dot,cot}   neighbor: cog
        dfs(cog) -> 1                        target reached
      cot -> 1 + 1 = 2
      dfs(dog)   visited {hit,hot,dot,dog}   neighbor: cog
        dfs(cog) -> 1                        target reached
      dog -> 1 + 1 = 2
    dot -> 1 + min(2, 2) = 3
    dfs(cot)   visited {hit,hot,cot}         neighbors: dot, cog
      dfs(dot)   visited {hit,hot,cot,dot}   neighbor: dog
        dfs(dog) -> 2                        via cog, as above
      dot -> 1 + 2 = 3
      dfs(cog) -> 1                          target reached
    cot -> 1 + min(3, 1) = 2
  hot -> 1 + min(3, 2) = 3
hit -> 1 + 3 = 4
```

The backtracking is visible in the two visits to `dot`: after the first branch returns, `visited.remove` drops `dot` from the set, which is what lets the later `cot` branch descend into `dot` again, this time with `cot` blocked instead of available. The two visits face different neighbor sets, which is exactly why a cache keyed on the word alone would conflate distinct subproblems. Every complete path is explored, and the minimum, `4`, is returned: `hit -> hot -> cot -> cog`.

#### Solution

The code is the recursion tree above: the loop over `word_set` creates the branches, and the add/remove pair around each call performs the backtracking.

```python
from typing import List, Set

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0

        word_set = set(wordList)

        def is_one_diff(word1: str, word2: str) -> bool:
            diff_count = 0
            for i in range(len(word1)):
                if word1[i] != word2[i]:
                    diff_count += 1
                    if diff_count > 1:
                        return False
            return diff_count == 1

        def dfs(current_word: str, target_word: str, visited: Set[str]) -> float:
            if current_word == target_word:
                return 1

            min_length = float("inf")

            for word in word_set:
                if word not in visited and is_one_diff(current_word, word):
                    visited.add(word)
                    result = dfs(word, target_word, visited)
                    if result != float("inf"):
                        min_length = min(min_length, 1 + result)
                    visited.remove(word)

            return min_length

        result = dfs(beginWord, endWord, {beginWord})
        return result if result != float("inf") else 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N! × M²)` worst case

Without distance-ordered pruning and without a sound cache, DFS can branch into exponentially many partial paths. Each recursive frame scans all `N` words and runs `is_one_diff` at `O(M)` per comparison, and the number of distinct paths explored can grow factorially in `N`.

##### Space Complexity: `O(N × M + recursion depth)`

The `visited` set holds up to `O(N)` words of length `M` along the active path, and the recursion stack can grow as deep as the longest explored path.

#### Key Insights

- DFS reaches the correct answer but is the wrong tool for shortest paths, since it lacks BFS's level-by-level guarantee.
- The `is_one_diff` helper short-circuits once two mismatches are found, so each comparison stops early.
- Memoization is tempting but unsound here: the subproblem result depends on the path-specific `visited` set, so a cache keyed only on the word pair would return wrong (inflated) lengths. Plain backtracking that takes the min over all complete paths stays correct at the cost of recomputation.

### Bidirectional BFS

#### Derivation

Every BFS above grows a single frontier from `beginWord`, and in a dense word graph that frontier can swell like `b^d`, the branching factor to the power of the distance. [Bidirectional BFS](https://en.wikipedia.org/wiki/Bidirectional_search) attacks the exponent instead of the base: grow a `front` set from `beginWord` and a `back` set from `endWord`, and stop the moment a variant generated on one side lands in the other. Each side then covers only about half the depth, roughly `2 × b^(d/2)` work instead of `b^d`:

1. Seed `front = {beginWord}`, `back = {endWord}`, and a shared `visited` holding
   both, with `steps = 1`.
2. Each iteration expands the smaller of the two frontiers (swapping `front` and
   `back` when needed) so the branching factor stays as low as possible.
3. For each word in `front`, generate its one-letter variants. A `neighbor` found
   in `back` means the two searches have met: return `steps + 1`.
4. Otherwise collect valid, unvisited variants into `next_front`, then advance
   `front` and increment `steps`.

Meeting in the middle halves the effective search depth, which is the dominant factor when the branching factor is high.

#### Walkthrough

Let us grow both frontiers on Example 1: `beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log","cog"]`. The state starts at `front = {hit}`, `back = {cog}`, `visited = {hit, cog}`, `steps = 1`. Each line is one pass of the outer loop, labeled with the `steps` value during that pass:

```text
steps 1   front {hit}      back {cog}        expand hit: keep "hot"         front -> {hot}
steps 2   front {hot}      back {cog}        expand hot: keep "dot","lot"   front -> {dot, lot}
steps 3   front {dot,lot} > back {cog}: swap
          front {cog}      back {dot, lot}   expand cog: keep "dog","log"   front -> {dog, log}
steps 4   front {dog,log}  back {dot, lot}   expand dog: variant "dot" is in back
          -> return steps + 1 = 5
```

The third pass shows both refinements at once. The frontiers are unequal, so the sets swap and the singleton `{cog}` is expanded instead of `{dot, lot}`: the search now grows backward from the end. On the fourth pass the two searches sit one edge apart: whichever of `dog` or `log` is expanded first, one of its variants (`dot` or `lot`) is already a member of `back`, so the searches meet and the answer is `steps + 1 = 5` either way. Read across the join, the path is `hit -> hot -> dot` from the begin side stitched to `dog -> cog` from the end side: 5 words, matching Example 1's Output.

#### Solution

The code is the frontier loop from the trace: swap to the smaller side, expand it wholesale, and return the moment a variant lands in `back`.

```python
from typing import List

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        word_set = set(wordList)
        if endWord not in word_set:
            return 0

        # Two frontiers grow toward each other; visited spans both.
        front = {beginWord}
        back = {endWord}
        visited = {beginWord, endWord}
        m = len(beginWord)
        steps = 1

        while front and back:
            # Always expand the smaller frontier to minimize branching.
            if len(front) > len(back):
                front, back = back, front

            next_front = set()

            for word in front:
                for i in range(m):
                    for c in "abcdefghijklmnopqrstuvwxyz":
                        if c == word[i]:
                            continue

                        neighbor = word[:i] + c + word[i + 1:]

                        # The frontiers meet: this neighbor closes the path.
                        if neighbor in back:
                            return steps + 1

                        if neighbor in word_set and neighbor not in visited:
                            visited.add(neighbor)
                            next_front.add(neighbor)

            front = next_front
            steps += 1

        return 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(M² × N)`

The worst-case bound matches plain BFS: each word is expanded once, with `M` positions, 26 letters, and `O(M)` slicing per candidate. In practice the meet-in-the-middle search explores far fewer nodes.

##### Space Complexity: `O(M × N)`

The two frontiers and the `visited` set together hold up to `N` words of length `M`, giving `O(M × N)`.

#### Key Insights

- Searching from both ends shrinks the explored space from roughly `b^d` to `2 × b^(d/2)`, where `b` is the branching factor and `d` the depth.
- Always expanding the smaller frontier keeps each step's work minimal and balances the two searches.
- A path is found the moment a generated neighbor appears in the opposite frontier, so the two halves never need to fully meet on a shared node.

## Comparison of Solutions

### Time Complexity

- **Brute Force Graph BFS**: `O(N² × M)` - building the graph compares all `N²` word pairs, each comparison scanning up to `M` characters; the BFS over the graph is dominated by this.
- **BFS with Word-by-Word Comparison**: `O(M² × N)` - each of `N` words tries `M` positions across 26 letters, and each string build costs `O(M)`.
- **BFS with Pattern Matching**: `O(M² × N)` - preprocessing builds all `M`-length patterns in `O(M² × N)`, and BFS traversal stays within the same order.
- **Backtracking DFS**: `O(N! × M²)` worst case - depth-first search explores exponentially many paths with no sound way to cache subproblems.
- **Bidirectional BFS**: `O(M² × N)` - same worst-case bound, but typically much faster in practice from the reduced search space.

### Space Complexity

- **Brute Force Graph BFS**: `O(N² + M × N)` - the adjacency lists can hold up to `O(N²)` edges, plus the node list, visited set, and queue.
- **BFS with Word-by-Word Comparison**: `O(M × N)` - for the word set, visited set, and BFS queue.
- **BFS with Pattern Matching**: `O(M² × N)` - the pattern dictionary stores `M` patterns per word, each of length `M`.
- **Backtracking DFS**: `O(N × M + recursion depth)` - for the path-specific visited set plus a recursion stack that can grow deep.
- **Bidirectional BFS**: `O(M × N)` - for the two frontiers and the shared visited set; in practice less than unidirectional BFS.

### Trade-offs

- **Brute Force Graph BFS**: Simplest mental model (build the graph, then search it), but the all-pairs neighbor comparison makes it quadratic in the number of words.
- **BFS with Word-by-Word Comparison**: Clear and optimal, but generates candidate words that may not exist in the dictionary.
- **BFS with Pattern Matching**: Avoids invalid candidates, at the cost of higher space usage and a preprocessing pass.
- **Backtracking DFS**: Useful for contrast, but performs poorly and does not visit words in distance order. Memoization cannot be added soundly because subproblem results depend on the active path's visited set.
- **Bidirectional BFS**: Often the fastest in practice, but the dual-frontier bookkeeping is more involved.

### When to Use Each

- **Brute Force Graph BFS**: As a teaching baseline that separates graph construction from the shortest-path search.
- **BFS with Word-by-Word Comparison (Recommended)**: The default interview answer - clear, optimal, and correct on every case.
- **BFS with Pattern Matching**: When the word list is large and avoiding invalid candidates matters more than memory.
- **Backtracking DFS**: For understanding why depth-first search is the wrong tool for shortest paths.
- **Bidirectional BFS**: For very large search spaces where the meet-in-the-middle speedup is worth the extra complexity.

### Optimization Notes

- The brute force's bottleneck is the `O(N²)` all-pairs comparison; generating one-letter variations on the fly (Word-by-Word Comparison) or grouping by wildcard pattern (Pattern Matching) discovers neighbors without comparing every pair.
- Convert `wordList` to a set for `O(1)` membership checks, and return early when `endWord` is absent to skip all further work.
- Mark words visited at the moment they are enqueued (or added to a frontier) so the same word is never processed twice.
- For very large search spaces, Bidirectional BFS is the strongest optimization, expanding from both ends and always growing the smaller frontier.
- Avoid plain DFS for this problem: it does not find the shortest path first, and it admits no sound memoization, so its worst case degrades toward `O(N! × M²)`.
