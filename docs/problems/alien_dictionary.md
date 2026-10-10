# [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/)

**Hard** | **40 minutes** | **Array, String, Depth-First Search, Breadth-First Search, Graph Theory, Topological Sort**

> This problem is locked behind [LeetCode Premium](https://leetcode.com/problems/alien-dictionary/); read it free on [NeetCode](https://neetcode.io/problems/foreign-dictionary).

**Pattern:** [Topological Sort](../patterns/topological_sort/intuition.md)

**Algorithm:** [Topological sorting](https://en.wikipedia.org/wiki/Topological_sorting) · [Kahn's algorithm](https://en.wikipedia.org/wiki/Topological_sorting#Kahn%27s_algorithm) · [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search)

**Practice:** [`practice/alien_dictionary/solution.py`](../../practice/alien_dictionary/solution.py)

There is a new alien language that uses the English alphabet, but the order of the letters is unknown.

You are given a list of strings `words` from the alien language's dictionary. It is claimed that the strings in `words` are sorted lexicographically by the rules of this new language.

If this claim is incorrect, and the given arrangement of strings in `words` cannot correspond to any order of letters, return `""`.

Otherwise, return a string of the unique letters in the new alien language sorted in lexicographically increasing order by the new language's rules. If there are multiple solutions, return **any** of them.

A string `a` is lexicographically smaller than a string `b` if either of the following is true:
* The first letter where they differ is smaller in `a` than in `b`.
* `a` is a prefix of `b` *and* `a.length < b.length`.

## Examples

### Example 1

**Input:** `words = ["z","o"]`

**Output:** `"zo"`

**Explanation:** From `"z"` and `"o"`, we know `'z' < 'o'`, so return `"zo"`.

### Example 2

**Input:** `words = ["hrn","hrf","er","enn","rfnn"]`

**Output:** `"hernf"`

**Explanation:** * from `"hrn"` and `"hrf"`, we know `'n' < 'f'`
* from `"hrf"` and `"er"`, we know `'h' < 'e'`
* from `"er"` and `"enn"`, we know `'r' < 'n'`
* from `"enn"` and `"rfnn"` we know `'e' < 'r'`
* so one possible solution is `"hernf"`

### Example 3

**Input:** `words = ["abc","ab"]`

**Output:** `""`

**Explanation:** The second word is a prefix of the first word, but the first word appears before the second. This is impossible in a valid lexicographical ordering, so return `""`.

## Constraints

- `1 <= words.length <= 100`
- `1 <= words[i].length <= 100`
- `words[i]` consists of only lowercase English letters.

## Deriving the Solution

A lexicographic order is a total order on letters, and adjacent word pairs are its only witnesses: in `words[i]` versus `words[i + 1]`, the first position where the two words differ asserts `words[i][p] < words[i + 1][p]`. Collecting those assertions yields a directed graph over letters whose valid orders are exactly its [topological orderings](https://en.wikipedia.org/wiki/Topological_sorting). Every solution below extracts the same edges and then orders the graph; they differ in how the ordering is produced and in which invalid inputs they catch first.

1. **Start literal.** Once the edges exist, find an order by trying every
   permutation of the unique letters and keeping one under which all adjacent pairs sort correctly. Exponential in the letter count, but it states what a valid answer is: see [Brute Force Permutation Check](#brute-force-permutation-check).
2. **Build the order one confirmed letter at a time.** A letter with no
   incoming edge can never be wrong as a next pick: nothing precedes it. Repeatedly taking such a letter and deleting its outgoing edges is [Kahn's algorithm](https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm); letters left untaken at the end reveal a cycle, the signature of a contradictory input: see [Kahn's Algorithm](#kahns-algorithm).
3. **Grow the order backwards instead.** Depth-first search computes the same
   order from the other end: a letter is finished only after everything it precedes is finished, so appending letters in post-order and reversing yields a topological order. A back-edge found during the depth-first walk is the cycle detector: see [DFS Post-Order](#dfs-post-order).

## Solutions

### Brute Force Permutation Check

#### Derivation

The most literal reading of "return the unique letters sorted by the new rules" tries orders directly. Build the precedence edges from adjacent word pairs, enumerate every permutation of the letters that appear, and test each candidate: under a correct order, every word pair must compare `<=` at the first differing position, with the prefix rule for exhausted words. The first passing permutation is a valid answer:

1. Collect the unique letters.
2. Extract the first-difference edges from each adjacent word pair; reject
   immediately if a longer word precedes its own prefix.
3. For each permutation, map letters to positions and verify every adjacent
   word pair compares in nondecreasing order.
4. Return the first surviving permutation as a string, or `""` when none
   survives.

#### Walkthrough

Example 2 has five unique letters, `h, r, n, f, e`, small enough to show the shape of the search. The edges extracted are `h < e`, `r < n`, `n < f`, `e < r`; a candidate order survives only when it places `h` before `e` before `r` before `n` before `f`. Of the `5! = 120` permutations, exactly those extending the chain `h, e, r, n, f` survive, and the chain itself is the smallest survivor:

```text
hernf   respects h<e, e<r, r<n, n<f   survives, lexicographically smallest
hernf + any reordering of {e,r,n,f} breaking the chain   fails its violated edge
```

The search returns `hernf`, matching the expected Output for Example 2. Example 3 (`["abc","ab"]`) never reaches the permutation stage: the extraction step spots the longer word `abc` sitting before its own prefix `ab` and rejects outright.

#### Solution

The code is the edge extraction plus the permutation filter.

```python
from itertools import permutations
from typing import List


class Solution:
    def alienOrder(self, words: List[str]) -> str:
        for first, second in zip(words, words[1:]):
            if len(first) > len(second) and first.startswith(second):
                return ""
        letters = sorted({letter for word in words for letter in word})
        for candidate in permutations(letters):
            position = {letter: index for index, letter in enumerate(candidate)}

            def key(word):
                return tuple(position[letter] for letter in word)

            if all(key(words[i]) <= key(words[i + 1]) for i in range(len(words) - 1)):
                return "".join(candidate)
        return ""
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(k! * total)` for `k` unique letters

Every one of the `k!` permutations is tested against all adjacent word pairs, each test scanning word content; viable only for a handful of letters.

##### Space Complexity: `O(k + total)`

The permutation stream, the position map, and the sort keys.

#### Key Insights

- The sort-key trick (`tuple` of positions per word) reduces the lexicographic comparison to a plain `<=` on tuples, prefix semantics included.
- Nothing is learned between candidates: each permutation re-derives the same verdicts the edges already encode, which is the waste the graph methods remove.
- The prefix violation check is separable from the search: it depends only on adjacent word lengths, never on the candidate order.

### Kahn's Algorithm

#### Derivation

The permutation filter re-tests letters that the edges have already settled. Kahn's algorithm exploits exactly that: a letter with indegree `0` has nothing before it, so taking it first is always safe. Take one, delete its outgoing edges (lowering neighbors' indegrees), and repeat; the taken sequence is a topological order. The loop stalls precisely when every untaken letter sits on a cycle, which is how a contradictory dictionary is detected:

1. Build `adjacency` and `indegree` over the letters that appear, one edge
   per first-difference between adjacent words, skipping duplicate edges.
2. Reject `""` if any longer word precedes its own prefix.
3. Seed a queue with all indegree-`0` letters.
4. Pop a letter, append it to `order`, and decrement each neighbor's
   indegree, enqueueing neighbors that reach `0`.
5. Return `"".join(order)` when every letter was taken, else `""` (a cycle
   exists).

#### Walkthrough

Let us run the queue on Example 2: `words = ["hrn","hrf","er","enn","rfnn"]`. The adjacent-pair comparisons extract `n < f` (from `hrn`/`hrf`), `h < e` (from `hrf`/`er`), `r < n` (from `er`/`enn`), and `e < r` (from `enn`/`rfnn`). Only `h` starts with indegree `0`:

```text
seed h                          queue = [h]
take h   e drops to 0           order = [h]          queue = [e]
take e   r drops to 0           order = [h, e]        queue = [r]
take r   n drops to 0           order = [h, e, r]     queue = [n]
take n   f drops to 0           order = [h, e, r, n]  queue = [f]
take f                          order = [h, e, r, n, f]
```

Each take frees exactly one successor, so the queue never branches and the order is forced: `hernf`, matching the expected Output for Example 2. Five letters were taken out of five known letters, so no cycle exists and the join is returned. On a contradictory input such as `["a","b","a"]` the edges `a < b` and `b < a` leave both letters at indegree `1`, the queue seeds empty, zero letters are taken out of two, and the function returns `""`.

#### Solution

The code is the edge extraction and the indegree-driven queue.

```python
from collections import deque
from typing import List


class Solution:
    def alienOrder(self, words: List[str]) -> str:
        adjacency = {letter: set() for word in words for letter in word}
        indegree = {letter: 0 for letter in adjacency}

        for first, second in zip(words, words[1:]):
            if len(first) > len(second) and first.startswith(second):
                return ""
            for a, b in zip(first, second):
                if a != b:
                    if b not in adjacency[a]:
                        adjacency[a].add(b)
                        indegree[b] += 1
                    break

        queue = deque(letter for letter, degree in indegree.items() if degree == 0)
        order = []
        while queue:
            letter = queue.popleft()
            order.append(letter)
            for next_letter in adjacency[letter]:
                indegree[next_letter] -= 1
                if indegree[next_letter] == 0:
                    queue.append(next_letter)
        return "".join(order) if len(order) == len(adjacency) else ""
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(total)`

Every character of every word is inspected once during extraction; the topological loop then touches each edge and each letter a constant number of times, with `e <= k²` bounded by the alphabet rather than the input.

##### Space Complexity: `O(k)`

The adjacency sets, indegree map, queue, and order hold one entry per letter (at most 26), so the auxiliary space is constant in the input size.

#### Key Insights

- The first-difference scan with an immediate `break` is the whole edge extractor: everything after the first difference asserts nothing.
- Deduplicating edges via the `adjacency` sets is load-bearing: a repeated edge would double-decrement its target's indegree and corrupt the count.
- The untaken-letters test is the cycle detector, and it costs one comparison at the end.

### DFS Post-Order

#### Derivation

Kahn's algorithm grows the order from the front, consuming letters with satisfied predecessors. Depth-first search derives the same order from the back: explore a letter's full downstream chain before finishing it, and append letters at finish time. Because everything a letter precedes finishes first, the finish-time sequence read backwards is a topological order. The walk also detects cycles directly: reaching a letter that is currently on the recursion stack means a back-edge, i.e. the extracted edges are contradictory:

1. Build `adjacency` as before, with the prefix check.
2. Walk `dfs(letter)` from every unvisited letter: mark it on the visit path,
   recurse into unvisited neighbors, then remove it from the path and append
   it to `order`.
3. Recursing into a letter already on the path returns `False` (cycle).
4. Reverse `order` and join, or return `""` on a cycle.

#### Walkthrough

Let us run the walk on Example 2, edges again `n -> f`, `h -> e`, `r -> n`, `e -> r`, iterating sources in the adjacency map's insertion order `h, r, n, f, e` (first appearance in `words`):

```text
dfs(h):  neighbor e
  dfs(e):  neighbor r
    dfs(r):  neighbor n
      dfs(n):  neighbor f
        dfs(f):  no neighbors -> finish f   order = [f]
      finish n                              order = [f, n]
    finish r                                order = [f, n, r]
  finish e                                  order = [f, n, r, e]
finish h                                    order = [f, n, r, e, h]
dfs(r), dfs(n), dfs(f), dfs(e): visited, skip
reverse -> [h, e, r, n, f]
```

The recursion dives to the letter with nothing after it (`f`) first, so the finish order is the itinerary backwards: the deepest chain pops out reversed as `h, e, r, n, f`, matching the expected Output for Example 2. On a contradictory input the path check fires: for `["z","x","z"]` the edges `z -> x` and `x -> z` make `dfs(z)` reach `x` and from `x` reach `z` again while `z` is still on the path, ending the walk with `""`.

#### Solution

The code is the recursive walk with the on-path set as the cycle detector.

```python
from typing import List


class Solution:
    def alienOrder(self, words: List[str]) -> str:
        adjacency = {letter: set() for word in words for letter in word}

        for first, second in zip(words, words[1:]):
            if len(first) > len(second) and first.startswith(second):
                return ""
            for a, b in zip(first, second):
                if a != b:
                    adjacency[a].add(b)
                    break

        order = []
        state = {}  # letter -> "visiting" | "done"

        def dfs(letter: str) -> bool:
            if letter in state:
                return state[letter] == "done"
            state[letter] = "visiting"
            for next_letter in adjacency[letter]:
                if not dfs(next_letter):
                    return False
            state[letter] = "done"
            order.append(letter)
            return True

        for letter in adjacency:
            if not dfs(letter):
                return ""
        return "".join(reversed(order))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(total)`

Extraction scans every character once; the walk visits each letter once and each edge once, with `e <= k²` bounded by the alphabet.

##### Space Complexity: `O(k)`

The adjacency sets, the state map, and the recursion stack of depth up to `k` (at most 26), constant in the input size.

#### Key Insights

- Reversed finish time is the theorem: post-order append plus one reverse replaces Kahn's indegree bookkeeping entirely.
- The two-state marker (`visiting` versus `done`) is what distinguishes a back-edge from a cross-edge: only `visiting` hits signal a cycle.
- The recursion depth is capped by the alphabet, so Python's recursion limit is no practical concern here even though the walk is recursive.

## Comparison of Solutions

### Time Complexity

- **Brute Force Permutation Check**: `O(k! * total)` - every letter permutation tested against every adjacent pair.
- **Kahn's Algorithm**: `O(total)` - one extraction pass plus a linear topological loop.
- **DFS Post-Order**: `O(total)` - the same extraction feeding one linear walk.

### Space Complexity

- **Brute Force Permutation Check**: `O(k + total)` - the position map and comparison keys per candidate.
- **Kahn's Algorithm**: `O(k)` - adjacency sets, indegrees, queue, and order.
- **DFS Post-Order**: `O(k)` - adjacency sets, state map, stack, and order.

### Trade-offs

- The brute force defines validity without graph vocabulary and drowns past a dozen letters.
- Kahn's algorithm reports the cycle only at the end (letters left untaken) and needs indegree bookkeeping; the DFS detects the cycle mid-walk and carries none.
- The DFS is recursive (bounded by the alphabet) and mutates a single order list; Kahn's is iterative and hands the zero-indegree frontier to any extension needing parallel or prioritized takes.

### When to Use Each

- **Brute Force Permutation Check**: as the executable specification for tests on tiny alphabets.
- **Kahn's Algorithm**: the interview default; the queue also generalizes to lexicographically-smallest topological orders by swapping in a heap (recommended here).
- **DFS Post-Order**: when the graph is already built and a cycle check must run anyway; the least bookkeeping of the three.

### Optimization Notes

- Extraction is the shared cost and the shared correctness surface: the first-difference `break` and the prefix check together define every edge, and both faster methods inherit whatever it decides.
- Deduplicating edges (`set` adjacency) matters only to Kahn's algorithm, whose indegrees count; the DFS tolerates duplicate edges but keeps them for symmetry.
- With `k <= 26` letters, all three methods are linear in the input; the real-world differentiator is which failure report the caller needs: Kahn's returns a set of stranded letters, the DFS a specific back-edge.

