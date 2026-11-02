# [Are Two People Relatives in a Family Tree?](https://www.fastprep.io/problems/amazon-family-tree-relatives)

**Medium** | **NN minutes** | **Graph, Breadth First Search, Hash Table**

A family tree is given as a list of rows. Each row relations[i] = [parent, child] means that parent is a parent of child. A person can have up to two recorded parents, and some people have no recorded parents at all. Because a child can have two parents, the family is a graph, not a simple tree.

Two people are relatives when they share at least one ancestor. Each person counts as one of their own ancestors. So a person is a relative of every ancestor and every descendant they have, and a person is always a relative of themselves.

## Examples

### Example 1

**Input:** `relations = [["ann","bob"],["ann","cat"],["bob","dan"],["cat","eve"]]`, `first = "dan"`, `second = "eve"`

**Output:** `true`

**Explanation:** dan's ancestors are dan, bob, and ann. eve's ancestors are eve, cat, and ann. Both sets contain ann, so the two cousins are relatives.

## Constraints

- `For this exercise, assume 0 <= relations.length <= 10000 with at most 1000 distinct person names.`
- `Every row is [parent, child]; both entries are person-name strings, and a child never has more than two recorded parents.`
- `The rows never make a person their own ancestor through a chain of relations.`
- `first and second are person names, and they may be the same person.`

## Deriving the Solution

One sentence of the statement carries the whole problem: a person counts as one of their own ancestors. With that settled, "relatives" is a set question: collect one person's ancestors, walk the other's, and ask whether the two ever name the same person. The parent rows point in the only direction the walks need; no forward child index is required.

1. **Start literal.** Compute both people's complete ancestor sets exactly as the statement defines them, then intersect: see [Ancestor-Set Intersection](#ancestor-set-intersection).
2. **Stop at the first hit.** The second set is only ever used for one membership question, so building all of it is waste; walk the second person's ancestors one at a time and return the moment one is already in the first set: see [Early-Exit Ancestor Walk](#early-exit-ancestor-walk).

## Solutions

### Ancestor-Set Intersection

#### Derivation

The statement defines relatives as sharing at least one ancestor and defines ancestors so that every person is their own. Transcribing that definition: each person's ancestor set starts as `{person}` and grows by unioning the ancestor sets of their recorded parents; two people are relatives exactly when their sets intersect. A depth-first fill per person with a cache over finished sets computes both closures without re-walking shared ancestry:

1. Build `parents_of`: each child's row entries appended under the child.
2. Define `ancestors(person)`: start from `{person}`, union `ancestors(parent)` for every recorded parent, and cache the result under `person`.
3. Return whether `ancestors(first) & ancestors(second)` is non-empty.

#### Walkthrough

Example 1, `first = "dan"`, `second = "eve"`. Each closure fills depth-first, parents first:

```text
ancestors(dan)   {dan} + ancestors(bob)
  ancestors(bob)   {bob} + ancestors(ann)
    ancestors(ann)   {ann}                 cached
  = {bob, ann}
= {dan, bob, ann}
ancestors(eve)   {eve} + ancestors(cat)
  ancestors(cat)   {cat, ann}            cache hit on ann
= {eve, cat, ann}

{dan, bob, ann} & {eve, cat, ann} = {ann}   non-empty
```

The intersection holds `ann`, matching the expected Output `true`.

#### Solution

```python
from collections import defaultdict
from typing import DefaultDict, List


class Solution:
    def solve(self, relations: List[List[str]], first: str, second: str) -> bool:
        parents_of: DefaultDict[str, List[str]] = defaultdict(list)
        for parent, child in relations:
            parents_of[child].append(parent)

        ancestors: DefaultDict[str, set] = defaultdict(set)

        def fill(person: str) -> set:
            if not ancestors[person]:
                ancestors[person].add(person)
                for parent in parents_of[person]:
                    ancestors[person] |= fill(parent)
            return ancestors[person]

        return bool(fill(first) & fill(second))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(people + relations)`

Each person's set is filled once (later requests are cache hits) and each parent row is unioned into exactly one fill; the final intersection scans the smaller set.

##### Space Complexity: `O(people^2)`

Every cached closure can hold the whole family in the worst case, and the cache keeps one closure per queried lineage.

#### Key Insights

- Seeding each set with the person themselves is what makes `first == second`, parent-child pairs, and the statement's self-ancestor rule all fall out of the intersection with no special cases.
- The cache is what keeps the recursion honest: a diamond family (two parents with shared ancestors) would otherwise union the same ancestors twice per branch.
- Full closures answer the question but compute more than the question needs, which is exactly the waste the next approach removes.

### Early-Exit Ancestor Walk

#### Derivation

The intersection approach builds both closures although it only ever asks one question about the second one: does it contain anything from the first? A frontier walk over the second person's ancestors answers that question online. Walk `second`'s ancestry breadth-first, one person at a time, and return `true` the instant a person already sits in `first`'s ancestor set. The first hit is the deepest shared ancestor the walk can produce, because every person the frontier visits later is a strictly higher ancestor, and if the frontier drains with no hit there is no shared ancestor at all:

1. Build `parents_of` as before.
2. Fill `ancestors_of_first` with a frontier walk seeded at `first`, including `first` itself.
3. Walk from `second` (seeded with `second`): return `true` at the first person in `ancestors_of_first`, `false` when the frontier drains.

#### Walkthrough

Example 1, `first = "dan"`, `second = "eve"`. The first walk completes; the second stops at its first hit:

```text
walk dan    frontier [dan]     ancestors_of_first = {dan}
            frontier [bob]     ancestors_of_first = {dan, bob}
            frontier [ann]     ancestors_of_first = {dan, bob, ann}
            frontier []        done
walk eve    visit eve          not in set
            visit cat          not in set
            visit ann          in set -> return true
```

The second walk returns `true` at `ann` without ever building a set of its own, matching the expected Output.

#### Solution

The code is the two frontier walks: one fills `ancestors_of_first`, the other stops at the first member it touches.

```python
from collections import deque
from typing import DefaultDict, List


class Solution:
    def solve(self, relations: List[List[str]], first: str, second: str) -> bool:
        parents_of: DefaultDict[str, List[str]] = DefaultDict(list)
        for parent, child in relations:
            parents_of[child].append(parent)

        ancestors_of_first = {first}
        frontier = deque([first])
        while frontier:
            person = frontier.popleft()
            for parent in parents_of[person]:
                if parent not in ancestors_of_first:
                    ancestors_of_first.add(parent)
                    frontier.append(parent)

        visited = {second}
        frontier = deque([second])
        while frontier:
            person = frontier.popleft()
            if person in ancestors_of_first:
                return True
            for parent in parents_of[person]:
                if parent not in visited:
                    visited.add(parent)
                    frontier.append(parent)
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(people + relations)`

Each walk admits every person at most once, and each parent row is read at most twice across both walks.

##### Space Complexity: `O(people + relations)`

The parent map plus one ancestor set; the second walk's `visited` guards its frontier only.

#### Key Insights

- The early exit preserves the answer exactly: the frontier visits ancestors in non-decreasing depth, so the first membership hit is a genuine shared ancestor and no later one could be deeper.
- Seeding the second walk with `second` itself keeps the statement's self-ancestor rule working: equal queries return `true` before either frontier moves.
- The second walk's `visited` set is not the answer's memory, only loop hygiene; families merge through two-parent rows, so a person can be reached twice.

## Comparison of Solutions

### Time Complexity

- **Ancestor-Set Intersection**: `O(people + relations)` - two cached closure fills and one intersection.
- **Early-Exit Ancestor Walk**: `O(people + relations)` - two frontier walks, the second possibly truncated at its first hit.

### Space Complexity

- **Ancestor-Set Intersection**: `O(people^2)` - the cache holds a closure per filled person.
- **Early-Exit Ancestor Walk**: `O(people + relations)` - one ancestor set plus loop guards.

### Trade-offs

- **Ancestor-Set Intersection**: a direct transcription of the statement's definition that also hands you both full closures (useful if more queries follow), at the price of quadratic cache memory in the worst case.
- **Early-Exit Ancestor Walk**: one set and a truncated second walk; the price is two hand-rolled frontiers instead of one recursive fill.

### When to Use Each

- **Ancestor-Set Intersection**: when both closures are themselves wanted, or as the reference reading to check the optimized version against.
- **Early-Exit Ancestor Walk (Recommended)**: the answer to give in an interview: one membership question, one set, and an answer that arrives as early as it possibly can.

### Optimization Notes

- If one family faces many relative queries, precompute the union-find style merge over all rows once; each later query then costs two root finds.
- The two-parent cap bounds each frontier's branching factor but not its size; merged royal-family graphs stay linear precisely because both walks admit each person once.
- Both approaches are already linear; the only asymptotic trap is re-walking ancestry per person without a cache, which turns diamonds into exponential work.
