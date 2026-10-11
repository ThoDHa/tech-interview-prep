# [Word Ladder](https://www.fastprep.io/problems/amazon-word-ladder)

**Hard** | **NN minutes** | **Breadth First Search, Graph, String**

You are given beginWord, endWord, and a dictionary wordList. A transformation changes exactly one character, and every transformed word—including endWord—must appear in the dictionary.

Return the number of words in the shortest valid sequence from beginWord through endWord, counting both endpoints. Return 0 when no sequence exists. If the two endpoints are equal, the answer is 1 only when that word appears in the dictionary.

## Examples

### Example 1

**Input:** `beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log","cog"]`

**Output:** `5`

**Explanation:** One shortest sequence is hit -> hot -> dot -> dog -> cog, which contains five words.

### Example 2

**Input:** `beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log"]`

**Output:** `0`

**Explanation:** The endpoint is absent from the dictionary, so no valid ladder exists.

### Example 3

**Input:** `beginWord = "same"`, `endWord = "same"`, `wordList = ["same","came"]`

**Output:** `1`

**Explanation:** The endpoints already match and the endpoint appears in the dictionary.

## Constraints

- `1 <= beginWord.length == endWord.length <= 10.`
- `1 <= wordList.length <= 5000.`
- `Every dictionary word has the same length as beginWord.`
- `Words contain only lowercase English letters.`

## Solutions

### Brute Force Graph BFS

#### Derivation

The reformulation every solution shares: words are nodes, two words share an edge when
they differ in exactly one letter, and the answer is the number of words on a shortest
path from `beginWord` to `endWord` in that unweighted graph. The literal plan builds the
graph first and searches it second. [BFS](https://en.wikipedia.org/wiki/Breadth-first_search)
is the search engine because it visits nodes in distance order, so the first arrival at
`endWord` is a shortest arrival. One rule is specific to this variant: when the two
endpoints are equal, the sequence is the single word itself, valid only if it is in the
dictionary, so the equal-endpoints case exits before any graph is built:

1. Copy `wordList` into `word_set`; return `1` when `beginWord == endWord` and the word
   is in `word_set`, `0` when they are equal and it is not.
2. Return `0` when `endWord` is absent from `word_set`: no valid sequence can end there.
3. Collect `nodes = [beginWord] + wordList` (the start need not be a dictionary word)
   and compare every pair with `is_one_diff`, appending each match to both `adjacency`
   lists.
4. BFS from `(beginWord, 1)` carrying `length`, the number of words used so far; return
   `length` the first time `endWord` is dequeued.

#### Walkthrough

Trace both phases on Example 1: `beginWord = "hit"`, `endWord = "cog"`,
`wordList = ["hot","dot","dog","lot","log","cog"]`. The all-pairs `is_one_diff` scan
finds nine edges among the seven nodes:

```text
hit-hot   hot-dot   hot-lot   dot-dog   dot-lot   dog-log   dog-cog   lot-log   log-cog
```

BFS then runs from `("hit", 1)` with `visited = {hit}`. Each line is one dequeue, the
unvisited neighbors it enqueues (each carrying `length + 1`), and the queue that remains:

```text
pop (hit, 1)   hot new                       queue = [(hot, 2)]
pop (hot, 2)   dot, lot new                  queue = [(dot, 3), (lot, 3)]
pop (dot, 3)   hot visited; dog new          queue = [(lot, 3), (dog, 4)]
pop (lot, 3)   hot, dot visited; log new     queue = [(dog, 4), (log, 4)]
pop (dog, 4)   dot, lot visited; cog new     queue = [(log, 4), (cog, 5)]
pop (log, 4)   dog, lot, cog all visited     queue = [(cog, 5)]
pop (cog, 5)   cog == endWord                return 5
```

The dequeued word equals `endWord` at `length = 5`, the length of the sequence
`hit -> hot -> dot -> dog -> cog` that produced the arrival, matching the expected
Output.

#### Solution

The code is the two phases of the walkthrough in order: the equal-endpoints guard, the
all-pairs adjacency build, then the queue loop.

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        word_set = set(wordList)
        if beginWord == endWord:
            return 1 if endWord in word_set else 0
        if endWord not in word_set:
            return 0

        nodes = [beginWord] + wordList

        def is_one_diff(first_word: str, second_word: str) -> bool:
            diff_count = 0
            for position in range(len(first_word)):
                if first_word[position] != second_word[position]:
                    diff_count += 1
                    if diff_count > 1:
                        return False
            return diff_count == 1

        adjacency = {word: [] for word in nodes}
        for first_index in range(len(nodes)):
            for second_index in range(first_index + 1, len(nodes)):
                if is_one_diff(nodes[first_index], nodes[second_index]):
                    adjacency[nodes[first_index]].append(nodes[second_index])
                    adjacency[nodes[second_index]].append(nodes[first_index])

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

`N` is the dictionary size and `M` the word length. Building the graph compares all
`N²` pairs, each comparison scanning up to `M` characters; the BFS that follows visits
each node and edge once, which the construction already dominates.

##### Space Complexity: `O(N² + M × N)`

The adjacency lists can hold up to `O(N²)` edges in a dense word graph, on top of the
node list, visited set, and queue holding `N` words of length `M`.

#### Key Insights

- Separating "build the graph" from "search the graph" makes the shortest-path framing
  explicit, and the search half is already optimal; only neighbor discovery needs work.
- The all-pairs comparison is the waste: at `N = 5000` it runs 12.5 million
  `is_one_diff` scans even though most pairs differ in several letters.
- The equal-endpoints rule is this variant's addition to the classic problem: it must be
  decided before the `endWord` presence check, since the sequence `[beginWord]` uses no
  transformation at all.

### BFS with Word-by-Word Comparison

#### Derivation

The brute force spends nearly all its time building edges it never walks. The repair
flips the neighbor question at search time: instead of asking "which known words is this
word adjacent to?", ask "which strings are one letter away, and which of those are known
words?". Each word has only `25 × M` one-letter variants (the letter already in a
position is skipped), and testing one against `word_set` costs one hash lookup, so
neighbors are discovered on demand with no precomputed graph. The BFS shell stays
exactly as in [Brute Force Graph BFS](#brute-force-graph-bfs):

1. Apply the same two guards: equal endpoints return `1` or `0`, absent `endWord`
   returns `0`; then start `queue` at `(beginWord, 1)` with `visited = {beginWord}`.
2. For the dequeued word, rebuild it position by position: for each `position` and each
   replacement `letter`, form `next_word`.
3. When `next_word == endWord`, the sequence closes: return `length + 1` without
   consulting `word_set`, because the guard already proved `endWord` is in it.
4. Otherwise enqueue `(next_word, length + 1)` when it is in `word_set` and unvisited,
   marking it visited at enqueue time so no word enters the queue twice.

#### Walkthrough

Trace the search on Example 1: `beginWord = "hit"`, `endWord = "cog"`,
`wordList = ["hot","dot","dog","lot","log","cog"]`. Each line dequeues one word and lists
the generated variants that survive the filters (in `word_set`, not yet visited):

```text
dequeue (hit, 1)   position 1 reaches "hot"            enqueue (hot, 2)
dequeue (hot, 2)   position 0 reaches "dot", "lot"     enqueue (dot, 3), (lot, 3)
dequeue (dot, 3)   "hot" visited; position 2 -> "dog"  enqueue (dog, 4)
dequeue (lot, 3)   "hot", "dot" visited; "log" new     enqueue (log, 4)
dequeue (dog, 4)   position 0 reaches "cog" == endWord return 4 + 1 = 5
```

Two details are easy to miss. Expanding `hot`, the variant `hit` is generated but
rejected: `beginWord` was never added to `word_set`, and it is already visited anyway.
And the final step never consults `word_set`: expanding `dog`, position `0` reaches
`"cog"`, the `next_word == endWord` test fires first, and the function returns
`length + 1 = 5`, matching the expected Output along `hit -> hot -> dot -> dog -> cog`.
Example 3 (`beginWord == endWord == "same"`) never reaches the queue: the opening guard
finds the word in `word_set` and returns `1`.

#### Solution

The code is the dequeue loop from the trace, with the two nested loops building
`next_word` position by position.

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        word_set = set(wordList)
        if beginWord == endWord:
            return 1 if endWord in word_set else 0
        if endWord not in word_set:
            return 0

        queue = deque([(beginWord, 1)])
        visited = {beginWord}
        while queue:
            current_word, length = queue.popleft()
            for position in range(len(current_word)):
                for letter in "abcdefghijklmnopqrstuvwxyz":
                    if letter == current_word[position]:
                        continue
                    next_word = current_word[:position] + letter + current_word[position + 1:]
                    if next_word == endWord:
                        return length + 1
                    if next_word in word_set and next_word not in visited:
                        visited.add(next_word)
                        queue.append((next_word, length + 1))
        return 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(M² × N)`

Each of the `N` words is dequeued at most once; each dequeue tries `M` positions across
26 letters, and building each candidate by slicing costs `O(M)`. The 26 is a constant,
leaving `M` positions times `M` slicing work per word. At the constraint sizes
(`M <= 10`, `N <= 5000`) that is a few hundred thousand character operations.

##### Space Complexity: `O(M × N)`

The `word_set`, `visited` set, and queue each hold up to `N` words of length `M`.

#### Key Insights

- BFS is the natural fit for shortest paths in unweighted graphs: it discovers words in
  distance order, so the first closure at `endWord` is a shortest sequence.
- Marking a word visited at enqueue time rather than dequeue time keeps the queue free
  of duplicates.
- Generating candidates directly produces strings that may not exist in the dictionary;
  the wasted probes are the price for holding no precomputed structure, and the next
  solution buys them back.

### BFS with Pattern Matching

#### Derivation

Generating variants probes `25 × M` strings per dequeued word, and most are gibberish
that fails the lookup. Those probes can be precomputed away: two words differ in one
letter exactly when masking that position makes them equal, so file every word under its
`M` wildcard patterns (`"hot"` -> `"*ot"`, `"h*t"`, `"ho*"`). Words sharing a bucket are
precisely the one-letter neighbors, and the BFS looks neighbors up by bucket instead of
generating candidates. This drops the `word_set` entirely, since every bucket member is
a real dictionary word:

1. Apply the same two guards as before; the equal-endpoints rule needs no buckets.
2. Build `patterns`: for every word in `wordList + [beginWord]`, append it under each of
   its `M` masked strings.
3. Run the BFS from `(beginWord, 1)`; for the dequeued word, form its `M` patterns and
   visit every `neighbor` recorded under them.
4. Return `length + 1` the first time a `neighbor` equals `endWord`; skip the visited
   otherwise.

#### Walkthrough

The pattern map is built once up front. On Example 1, the seven words produce these
buckets (every bucket not shown holds a single word):

```text
*ot -> [hot, dot, lot]     h*t -> [hot, hit]     do* -> [dot, dog]
*og -> [dog, log, cog]     lo* -> [lot, log]
```

BFS then walks bucket mates instead of generated strings:

```text
dequeue (hit, 1)   buckets *it, h*t, hi*: new mate "hot"    enqueue (hot, 2)
dequeue (hot, 2)   bucket *ot: "dot", "lot" new             enqueue (dot, 3), (lot, 3)
dequeue (dot, 3)   bucket do*: "dog" new                    enqueue (dog, 4)
dequeue (lot, 3)   bucket lo*: "log" new                    enqueue (log, 4)
dequeue (dog, 4)   bucket *og: mate "cog" == endWord        return 4 + 1 = 5
```

Every word the search touches is a real dictionary word: no gibberish candidate is ever
formed. Expanding `dog`, its pattern `*og` lists `[dog, log, cog]`; `dog` is the word
itself, `log` is already visited, and `cog` trips the `endWord` test, returning `5`,
matching the expected Output along the same five-word sequence as before.

#### Solution

The code builds `patterns` up front; the BFS loop then reads neighbors straight out of
the buckets.

```python
from collections import defaultdict, deque
from typing import DefaultDict, List


class Solution:
    def solve(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        word_set = set(wordList)
        if beginWord == endWord:
            return 1 if endWord in word_set else 0
        if endWord not in word_set:
            return 0

        patterns: DefaultDict[str, List[str]] = defaultdict(list)
        for word in wordList + [beginWord]:
            for position in range(len(word)):
                pattern = word[:position] + "*" + word[position + 1:]
                patterns[pattern].append(word)

        queue = deque([(beginWord, 1)])
        visited = {beginWord}
        while queue:
            current_word, length = queue.popleft()
            for position in range(len(current_word)):
                pattern = current_word[:position] + "*" + current_word[position + 1:]
                for neighbor in patterns[pattern]:
                    if neighbor == endWord:
                        return length + 1
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, length + 1))
        return 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(M² × N)`

Preprocessing builds `M` patterns per word, each costing `O(M)` to slice; the BFS then
visits each word and pattern bucket once, bounded by the same order.

##### Space Complexity: `O(M² × N)`

The pattern dictionary stores `M` patterns per word, each of length `M`, on top of the
queue and visited set.

#### Key Insights

- Wildcard patterns turn neighbor discovery into a hash lookup that returns only real
  words, eliminating the failed probes of variant generation.
- The tradeoff is memory: the pattern map dominates the page's space costs at
  `O(M² × N)`.
- Including `beginWord` in the buckets lets the search start from it even though it need
  not be in `wordList`; `hit` reaches `hot` through the `h*t` bucket, not through any
  dictionary membership.

### Bidirectional BFS

#### Derivation

Every BFS so far grows one frontier from `beginWord`, and a dense word graph makes that
frontier swell like `b^d` for branching factor `b` and distance `d`. [Bidirectional
search](https://en.wikipedia.org/wiki/Bidirectional_search) attacks the exponent: grow a
`front` set from `beginWord` and a `back` set from `endWord`, always expanding the
smaller of the two, and stop the moment a variant generated on one side lands in the
other. Each side then covers only about half the depth, roughly `2 × b^(d/2)` words
instead of `b^d`:

1. Apply the same two guards; then seed `front = {beginWord}`, `back = {endWord}`, and a
   shared `visited` holding both, with `steps = 1`.
2. Each pass expands the smaller frontier, swapping `front` and `back` when needed, so
   the branching factor stays as low as possible.
3. For each word in `front`, generate its one-letter variants: a variant found in `back`
   means the searches have met, so return `steps + 1`.
4. Otherwise collect valid, unvisited variants into `next_front`, then advance `front`
   and increment `steps`; return `0` when either frontier drains, meaning the two sides
   can never meet.

#### Walkthrough

Grow both frontiers on Example 1: `beginWord = "hit"`, `endWord = "cog"`,
`wordList = ["hot","dot","dog","lot","log","cog"]`. The state starts at
`front = {hit}`, `back = {cog}`, `visited = {hit, cog}`, `steps = 1`. Each line is one
pass of the outer loop, labeled with the `steps` value during that pass:

```text
steps 1   front {hit}       back {cog}        expand hit: keep "hot"           front -> {hot}
steps 2   front {hot}       back {cog}        expand hot: keep "dot", "lot"    front -> {dot, lot}
steps 3   front {dot, lot} > back {cog}: swap sides
          front {cog}       back {dot, lot}   expand cog: keep "dog", "log"    front -> {dog, log}
steps 4   front {dog, log}  back {dot, lot}   expand dog: variant "dot" in back
          -> return steps + 1 = 5
```

The third pass shows both refinements at once. The frontiers are unequal, so the sets
swap and the singleton `{cog}` is expanded instead of `{dot, lot}`: the search grows
backward from the end. On the fourth pass the two searches sit one edge apart: expanding
`dog`, the variant `dot` is already a member of `back`, so the searches meet and the
answer is `steps + 1 = 5`. Read across the join, the path is `hit -> hot -> dot` from
the begin side stitched to `dog -> cog` from the end side: 5 words, matching the
expected Output.

#### Solution

The code is the frontier loop from the trace: swap to the smaller side, expand it
wholesale, and return the moment a variant lands in `back`.

```python
from typing import List, Set


class Solution:
    def solve(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        word_set = set(wordList)
        if beginWord == endWord:
            return 1 if endWord in word_set else 0
        if endWord not in word_set:
            return 0

        front: Set[str] = {beginWord}
        back: Set[str] = {endWord}
        visited: Set[str] = {beginWord, endWord}
        steps = 1

        while front and back:
            if len(front) > len(back):
                front, back = back, front

            next_front: Set[str] = set()
            for word in front:
                for position in range(len(word)):
                    for letter in "abcdefghijklmnopqrstuvwxyz":
                        if letter == word[position]:
                            continue
                        next_word = word[:position] + letter + word[position + 1:]
                        if next_word in back:
                            return steps + 1
                        if next_word in word_set and next_word not in visited:
                            visited.add(next_word)
                            next_front.add(next_word)

            front = next_front
            steps += 1
        return 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(M² × N)`

The worst-case bound matches plain BFS, since each word is expanded once with `M`
positions, 26 letters, and `O(M)` slicing per candidate; in practice the
meet-in-the-middle order explores far fewer words than `b^d`.

##### Space Complexity: `O(M × N)`

The two frontiers and the shared `visited` set together hold up to `N` words of length
`M`; in practice less than unidirectional BFS, whose frontier at the widest level is
larger than either half-frontier here.

#### Key Insights

- Searching from both ends shrinks the explored space from roughly `b^d` to
  `2 × b^(d/2)`, which matters once the word graph is dense enough for frontiers to
  double every level.
- Always expanding the smaller frontier keeps each pass's work minimal and balances the
  two searches.
- A path is found the moment a generated variant appears in the opposite frontier, so
  the halves never need to share a fully expanded node.
- The shared `visited` set is what makes the meeting test sound: a word claimed by one
  side is never re-expanded by the other.

## Comparison of Solutions

### Time Complexity

- **Brute Force Graph BFS**: `O(N² × M)` - building the graph compares all `N²` word
  pairs, each comparison scanning up to `M` characters; the BFS over the graph is
  dominated by this.
- **BFS with Word-by-Word Comparison**: `O(M² × N)` - each of `N` words tries `M`
  positions across 26 letters, and each candidate build costs `O(M)`.
- **BFS with Pattern Matching**: `O(M² × N)` - preprocessing slices `M` patterns per
  word in `O(M² × N)`, and the BFS traversal stays within the same order.
- **Bidirectional BFS**: `O(M² × N)` - the same worst-case bound, typically much faster
  in practice from the halved search depth.

### Space Complexity

- **Brute Force Graph BFS**: `O(N² + M × N)` - the adjacency lists can hold up to `N²`
  edges, plus the node list, visited set, and queue.
- **BFS with Word-by-Word Comparison**: `O(M × N)` - for the word set, visited set, and
  queue.
- **BFS with Pattern Matching**: `O(M² × N)` - the pattern dictionary stores `M`
  patterns per word, each of length `M`.
- **Bidirectional BFS**: `O(M × N)` - for the two frontiers and the shared visited set.

### Trade-offs

- **Brute Force Graph BFS**: the clearest mental model (build the graph, then search
  it), but the all-pairs comparison makes it quadratic in the dictionary size.
- **BFS with Word-by-Word Comparison**: no preprocessing and optimal time, at the cost
  of generating candidate words that mostly are not in the dictionary.
- **BFS with Pattern Matching**: never forms an invalid candidate, at the price of the
  largest memory footprint on the page.
- **Bidirectional BFS**: the fastest in practice on dense word graphs, but the
  dual-frontier bookkeeping and the meeting test are the most involved.

### When to Use Each

- **Brute Force Graph BFS**: as a teaching baseline that separates graph construction
  from the shortest-path search, or when the dictionary is tiny.
- **BFS with Word-by-Word Comparison (Recommended)**: the default interview answer:
  clear, optimal, and correct on every case including the equal-endpoints one.
- **BFS with Pattern Matching**: when the dictionary is large and repeated runs against
  it make the preprocessing worth amortizing.
- **Bidirectional BFS**: when the word graph is dense and the frontier growth is the
  observable bottleneck.

### Optimization Notes

- The brute force's bottleneck is the `O(N²)` all-pairs scan; both variant generation
  and pattern bucketing discover neighbors without comparing every pair.
- The `next_word == endWord` early return skips a set lookup on the final step, which
  the `endWord in word_set` guard has already made unnecessary.
- Marking words visited at enqueue (or frontier-insert) time is what bounds the queue
  and frontier sizes by `N`; marking at dequeue time can stack duplicate words.
- For the FastPrep constraint sizes (`M <= 10`, `N <= 5000`) all three optimal
  solutions run in well under a million character operations, so the choice between
  them is about clarity and memory, not speed.
