# [Count Similar String Groups](https://www.fastprep.io/problems/amazon-count-similar-string-groups)

**unknown difficulty** | **NN minutes** | **unknown categories**

You are given an array of strings strs. All strings are anagrams of each other.

Two strings are considered similar if they are identical, or if you can make them equal by swapping exactly two characters in one of the strings.

Similarity is transitive: if string a is similar to b, and b is similar to c, then all three belong to the same group.

Return the number of groups of similar strings.

## Examples

### Example 1

**Input:** `strs = ["tars", "rats", "arts", "star"]`

**Output:** `2`

**Explanation:** "tars" is similar to "rats", and "rats" is similar to "arts", so they form one group. "star" forms another group.

### Example 2

**Input:** `strs = ["omv", "ovm"]`

**Output:** `1`

**Explanation:** The two strings differ in exactly two positions, so one swap makes them equal.

## Constraints

- `All strings in strs are anagrams of each other.`
- `All strings have the same length.`

## Solutions

### BFS over Pairwise Similarity

#### Derivation

The most literal reading: similarity is transitive, so the strings split into groups exactly the way [connected components](https://en.wikipedia.org/wiki/Component_(graph_theory)) do, over an implicit graph whose nodes are the strings and whose edges join similar pairs. So build the group count by traversal: scan for an unvisited string, flood its whole group, and count the floods.

Everything about the edges sits in one observation. Two anagrams can never differ in exactly one position, because a single changed character would unbalance the letter counts. They can differ in three positions (`"abc"` and `"bca"`), so the count must be tested exactly, not reduced to a parity rule. And when two anagrams differ in exactly two positions, the swapped characters must exchange places: every other position is equal, so the two disagreeing positions hold the same two letters in both strings, just crossed. One swap fixes them. So `is_similar` reduces to counting differing positions and comparing against `0` (identical) or `2` (one swap), with the count abandoned as soon as it reaches `3`:

1. Keep `visited`, a boolean per string, and `groups = 0`.
2. Scan for the first unvisited `start`: increment `groups`, mark it visited,
   and seed a `queue` with it.
3. While the queue is non-empty, `popleft` a `current` string and test every
   unvisited `neighbor` with `is_similar`; each similar neighbor is marked and
   enqueued.
4. Return `groups` after the scan.

#### Walkthrough

Example 1, `strs = ["tars", "rats", "arts", "star"]`. The pairwise difference counts decide every edge:

```text
tars / rats   differ at 0, 2        -> 2  similar
tars / arts   differ at 0, 1, 2     -> 3  not similar
tars / star   differ at 0, 1, 2, 3  -> 4  not similar
rats / arts   differ at 0, 1        -> 2  similar
rats / star   differ at 0, 1, 2, 3  -> 4  not similar
arts / star   differ at 0, 1, 2, 3  -> 4  not similar
```

The scan starts at string `0` (`"tars"`), sets `groups = 1`, and floods its group:

```text
dequeue tars   rats similar -> visit+enqueue
               arts: 3 differences -> skip; star: 4 -> skip
dequeue rats   arts similar -> visit+enqueue; star not similar
dequeue arts   star not similar
queue empty    group {tars, rats, arts} complete
```

The scan then reaches `star` unvisited, so `groups` becomes `2`, the expected Output.

#### Solution

The code is the scan-and-flood from the walkthrough, with `is_similar` as the edge test.

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, strs: List[str]) -> int:
        def is_similar(first: str, second: str) -> bool:
            differences = 0
            for first_char, second_char in zip(first, second):
                if first_char != second_char:
                    differences += 1
                    if differences > 2:
                        return False
            return differences == 0 or differences == 2

        count = len(strs)
        visited = [False] * count
        groups = 0

        for start in range(count):
            if visited[start]:
                continue
            groups += 1
            queue = deque([start])
            visited[start] = True
            while queue:
                current = queue.popleft()
                for neighbor in range(count):
                    if not visited[neighbor] and is_similar(strs[current], strs[neighbor]):
                        visited[neighbor] = True
                        queue.append(neighbor)

        return groups
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2 × L)`

Every unordered pair of strings is tested at most once across the flood fills, and each test scans up to `L` character positions.

##### Space Complexity: `O(n)`

The `visited` array and a queue holding at most one entry per string; the adjacency is tested lazily and never stored.

#### Key Insights

- Anagrams make the edge test exact: distance `1` is impossible and distance `2` is always one swap away, so comparing the difference count against `0` or `2` needs no letter bookkeeping.
- The early exit at three differences bounds the cost of a dissimilar pair by the third mismatch, which is where most pairs stop.
- Transitivity is consumed by the traversal, not by the test: `is_similar` only ever decides a single edge.

### Union-Find with Early Exit

#### Derivation

The BFS materializes each component as it floods, but the answer only needs the number of components, not their members. [Union-Find](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) answers exactly that: start every string in its own component and merge on every similar pair; the surviving component count is the answer. The pair loop then needs no bookkeeping about which components were already flooded, and every adjacency is examined exactly once:

1. Build `UnionFind(n)`; `components` starts at `n`.
2. For every pair `first_index < second_index`, run `is_similar`; on success
   `union(first_index, second_index)`, which decrements `components` only when
   two different roots merge.
3. Return `components`.

#### Walkthrough

Example 1 again, processing the six pairs in row-major order. Roots after path compression shown as `parent`:

```text
pair (0, 1) tars/rats  similar  union -> components 4 -> 3
pair (0, 2) tars/arts  3 diffs  skip
pair (0, 3) tars/star  4 diffs  skip
pair (1, 2) rats/arts  similar  union -> components 3 -> 2
pair (1, 3) rats/star  4 diffs  skip
pair (2, 3) arts/star  4 diffs  skip
```

`components` ends at `2`, the expected Output. Note that the direct pair `tars`/`arts` is not similar at all (three differences): the two strings land in one group only through `"rats"`, which is exactly the transitivity the component count absorbs.

#### Solution

The code is the pair sweep from the walkthrough over a small union-by-rank structure with path compression.

```python
from typing import List


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size
        self.components = size

    def find(self, item: int) -> int:
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, first: int, second: int) -> None:
        first_root, second_root = self.find(first), self.find(second)
        if first_root == second_root:
            return
        if self.rank[first_root] < self.rank[second_root]:
            self.parent[first_root] = second_root
        elif self.rank[first_root] > self.rank[second_root]:
            self.parent[second_root] = first_root
        else:
            self.parent[second_root] = first_root
            self.rank[first_root] += 1
        self.components -= 1


class Solution:
    def solve(self, strs: List[str]) -> int:
        def is_similar(first: str, second: str) -> bool:
            differences = 0
            for first_char, second_char in zip(first, second):
                if first_char != second_char:
                    differences += 1
                    if differences > 2:
                        return False
            return differences == 0 or differences == 2

        union_find = UnionFind(len(strs))
        for first_index in range(len(strs)):
            for second_index in range(first_index + 1, len(strs)):
                if is_similar(strs[first_index], strs[second_index]):
                    union_find.union(first_index, second_index)

        return union_find.components
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2 × L)`

The pair sweep performs `n(n-1)/2` similarity tests of `O(L)` each; the unions add only inverse-Ackermann terms.

##### Space Complexity: `O(n)`

The `parent` and `rank` arrays.

#### Key Insights

- Counting components needs no traversal order: merging every similar pair into a disjoint-set forest leaves `components` holding the answer.
- Redundant unions are harmless and cheap: a pair whose endpoints already share a root is detected and skipped before any rank work.
- The early-exit similarity test is unchanged from the BFS version, which shows where the problem's real content lives: the edge predicate, not the component machinery.

### Union-Find with Duplicate Collapse

#### Derivation

Both solutions so far pay `O(L)` to compare even two identical strings, and the early exit never fires for them. But identical strings are similar by the statement's first clause, so duplicates can never join two different groups: every copy of a string belongs to the group of that string. A hash map can therefore collapse all copies onto one representative before any character comparison happens, and the pair sweep then runs over distinct strings only. The group count among representatives equals the group count among all strings, because collapsed copies always sit in their representative's group:

1. Walk `strs` once, mapping each string to the index of its first occurrence
   in `first_seen`; the survivors are the representatives.
2. Build `UnionFind(len(first_seen))` over the representatives.
3. Sweep all pairs of representatives, union on `is_similar`.
4. Return `components`.

#### Walkthrough

A tailored input with a duplicate (Example 2 has none): `strs = ["omv", "ovm", "omv"]`:

```text
first_seen pass     "omv" -> 0, "ovm" -> 1, "omv" already mapped
representatives     [0, 1]  ("omv", "ovm")
pair (0, 1)         omv/ovm differ at 1, 2 -> 2  union -> components 2 -> 1
```

The third string never reaches a character comparison; it is absorbed by the map. `components` is `1`, which is the expected Output of Example 2, and the duplicate copy did not change it.

#### Solution

The code is the map pass plus the representative sweep from the walkthrough.

```python
from typing import List


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size
        self.components = size

    def find(self, item: int) -> int:
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, first: int, second: int) -> None:
        first_root, second_root = self.find(first), self.find(second)
        if first_root == second_root:
            return
        if self.rank[first_root] < self.rank[second_root]:
            self.parent[first_root] = second_root
        elif self.rank[first_root] > self.rank[second_root]:
            self.parent[second_root] = first_root
        else:
            self.parent[second_root] = first_root
            self.rank[first_root] += 1
        self.components -= 1


class Solution:
    def solve(self, strs: List[str]) -> int:
        def is_similar(first: str, second: str) -> bool:
            differences = 0
            for first_char, second_char in zip(first, second):
                if first_char != second_char:
                    differences += 1
                    if differences > 2:
                        return False
            return differences == 0 or differences == 2

        first_seen = {}
        for position, string in enumerate(strs):
            first_seen.setdefault(string, position)
        representatives = list(first_seen.values())

        union_find = UnionFind(len(representatives))
        for first_index in range(len(representatives)):
            for second_index in range(first_index + 1, len(representatives)):
                first_string = strs[representatives[first_index]]
                second_string = strs[representatives[second_index]]
                if is_similar(first_string, second_string):
                    union_find.union(first_index, second_index)

        return union_find.components
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × L + d^2 × L)`

One hash pass over `n` strings plus a pair sweep over `d`, the number of distinct strings; `d` ranges from `1` (all copies of one string) to `n`.

##### Space Complexity: `O(d)`

The `first_seen` map plus the union-find arrays over representatives.

#### Key Insights

- Identity is transitive closure for free: copies of one string are similar to each other and to everything their representative is similar to, so collapsing them before the sweep preserves the group count exactly.
- The win is data-dependent, not asymptotic in the worst case (`d = n` degenerates to the previous solution), but real test data with repeated strings shrinks the quadratic term.
- The dict keeps the first occurrence as representative so the union-find indices remain valid positions into `strs`.

## Comparison of Solutions

### Time Complexity

- **BFS over Pairwise Similarity**: `O(n^2 × L)` - every unordered pair tested at most once across the flood fills, each test scanning up to `L` positions.
- **Union-Find with Early Exit**: `O(n^2 × L)` - `n(n-1)/2` similarity tests plus near-constant union-find work.
- **Union-Find with Duplicate Collapse**: `O(n × L + d^2 × L)` - a hash pass over all strings, then pairs over the `d` distinct ones only.

### Space Complexity

- **BFS over Pairwise Similarity**: `O(n)` - visited array plus queue.
- **Union-Find with Early Exit**: `O(n)` - parent and rank arrays.
- **Union-Find with Duplicate Collapse**: `O(d)` - the representative map plus union-find arrays.

### Trade-offs

- **BFS over Pairwise Similarity**: the most direct expression of the connected-components idea and it exposes group membership during the flood, but it stores traversal state and re-derives structure the answer never uses.
- **Union-Find with Early Exit**: the shortest correct core (one pair sweep, one counter), with no traversal bookkeeping; it never names the groups, only counts them.
- **Union-Find with Duplicate Collapse**: adds a hash pass to buy immunity to duplicate-heavy inputs; on all-distinct inputs it is the previous solution plus overhead.

### When to Use Each

- **BFS over Pairwise Similarity**: when the groups themselves matter (membership queries after counting), or when explaining the problem to yourself first.
- **Union-Find with Early Exit (Recommended)**: the interview default: minimal state, exact count, and the same `is_similar` predicate carries the whole correctness argument.
- **Union-Find with Duplicate Collapse**: when duplicates are plausible at scale (logs, catalog data) or the interviewer pushes on optimizing beyond the pairwise sweep.

### Optimization Notes

- The early exit at three differences is what keeps the constant in `O(n^2 × L)` honest: a dissimilar anagram pair is rejected at its third mismatched position, not at the end of the strings.
- Deduplication first is the only optimization here that changes the quadratic term; sorting or bucketing tricks do not, because similarity is defined by position-wise comparison, not by signature equality.
- All strings being anagrams is what makes the distance rule exact (`0` or `2`); on arbitrary strings the predicate would need to verify that the two differing positions actually exchange letters, since differing twice elsewhere would not be fixable by one swap.
