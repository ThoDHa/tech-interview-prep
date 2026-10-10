# [Evaluate Division](https://www.fastprep.io/problems/amazon-evaluate-division)

**Medium** | **NN minutes** | **Graph, Depth First Search, Breadth First Search**

You are given variable pairs equations and positive real numbers values. For every index i, equations[i] = [a, b] and values[i] mean a / b = values[i].

For each pair in queries, return the requested quotient. Return -1.0 when it cannot be determined. The equations are valid and mutually consistent, and a variable absent from all equations is undefined even when queried against itself.

The query stream can be very large and can repeat the same ordered pairs. Reuse previously resolved relationships or preprocess component weights so repeated calls do not traverse the full graph again.

## Examples

### Example 1

**Input:** `equations = [["a","b"],["b","c"]]`, `values = [2.0,3.0]`, `queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]`

**Output:** `[6.0,0.5,-1.0,1.0,-1.0]`

**Explanation:** Compose or reverse known ratios; undefined variables produce -1.0.

### Example 2

**Input:** `equations = [["a","b"],["b","c"],["bc","cd"]]`, `values = [1.5,2.5,5.0]`, `queries = [["a","c"],["c","b"],["bc","cd"],["cd","bc"]]`

**Output:** `[3.75,0.4,5.0,0.2]`

**Explanation:** Products along graph paths evaluate indirect ratios.

### Example 3

**Input:** `equations = [["a","b"]]`, `values = [0.5]`, `queries = [["a","b"],["b","a"],["a","c"],["x","y"]]`

**Output:** `[0.5,2.0,-1.0,-1.0]`

**Explanation:** The reverse edge uses the reciprocal; unknown variables have no path.

## Constraints

- `1 <= equations.length <= 200000`
- `values.length == equations.length`
- `0.0 < values[i] <= 10^9`
- `1 <= queries.length <= 200000`
- `Variable names contain one to five lowercase letters or digits.`
- `The equations contain no contradictions and no division by zero.`
- `Every quotient implied between two connected variables is between 10^-100 and 10^100, inclusive, so all component weights and requested results are finite.`
- `Results within 10^-5 of the expected value are accepted.`

## Solutions

### BFS over the Ratio Graph

#### Derivation

Treat every equation as a directed, weighted edge: `a / b = values[i]` means an edge from `a` to `b` carrying the multiplier `values[i]`, and the reciprocal edge from `b` to `a` carrying `1.0 / values[i]`. Under that reading, any quotient `x / y` is exactly the product of the edge multipliers along a path from `x` to `y`, and the quotient is determinable precisely when such a path exists. Each query therefore reduces to reachability with a running product, which a breadth-first search answers directly:

1. Build `graph`, mapping each variable to the dict of its outgoing neighbors
   and their multipliers: `graph[numerator][denominator] = ratio` and
   `graph[denominator][numerator] = 1.0 / ratio`.
2. For each query `[query_numerator, query_denominator]`, return -1.0
   immediately when either variable never appeared in an equation.
3. Otherwise search from `query_numerator`: the queue holds
   `(variable, product)` pairs seeded with `(query_numerator, 1.0)`, and
   `visited` keeps the search from cycling.
4. The first time the search reaches `query_denominator`, its `product` is the
   quotient; when the queue empties without reaching it, the two variables sit
   in different components and the quotient is -1.0.

#### Walkthrough

Let us run the five queries of Example 1, `equations = [["a","b"],["b","c"]]`, `values = [2.0,3.0]`, by hand. Building `graph` yields four directed edges:

```text
a -> b (2.0)    b -> a (0.5)    b -> c (3.0)    c -> b (1/3)
```

Each query starts one breadth-first search over `(variable, product)` queue entries:

```text
a/c   queue: (a,1.0) -> (b,2.0) -> (c,6.0)     reached c: quotient 2.0 * 3.0 = 6.0
b/a   queue: (b,1.0) -> (a,0.5)                reached a: quotient 0.5
a/e   e never appeared in an equation          -1.0
a/a   first pop (a,1.0) is already the target  1.0
x/x   x never appeared in an equation          -1.0
```

The `a/c` search composes two edges, `2.0 * 3.0 = 6.0`, and `b/a` rides the reciprocal edge built in step one. The collected quotients are `[6.0, 0.5, -1.0, 1.0, -1.0]`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough: one dict of neighbor dicts, and one queue of `(variable, product)` pairs per query.

```python
from collections import deque
from typing import List


class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float],
                     queries: List[List[str]]) -> List[float]:
        graph: dict[str, dict[str, float]] = {}
        for (numerator, denominator), ratio in zip(equations, values):
            graph.setdefault(numerator, {})[denominator] = ratio
            graph.setdefault(denominator, {})[numerator] = 1.0 / ratio

        quotients = []
        for query_numerator, query_denominator in queries:
            if query_numerator not in graph or query_denominator not in graph:
                quotients.append(-1.0)
                continue
            visited = {query_numerator}
            queue = deque([(query_numerator, 1.0)])
            quotient = -1.0
            while queue:
                variable, product = queue.popleft()
                if variable == query_denominator:
                    quotient = product
                    break
                for neighbor, edge_ratio in graph[variable].items():
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, product * edge_ratio))
            quotients.append(quotient)
        return quotients
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(E + Q × (V + E))`

Let `E` be the number of equations, `V` the number of distinct variables, and `Q` the number of queries: building the graph touches every equation once, and each query runs one search that visits every variable and edge of its component at most once.

##### Space Complexity: `O(V + E)`

The graph stores two directed edges per equation, and a single search holds up to `V` queue entries and `V` visited marks.

#### Key Insights

- Division composes along paths: `a/b` times `b/c` is `a/c`, so the quotient of any two connected variables is the product of edge ratios along their path.
- Every edge must be stored in both directions, the reverse carrying the reciprocal; that is what makes `b/a` queries as cheap as `a/b`.
- The `visited` set is not optional: ratio graphs routinely contain cycles (`a/b` and `b/a` are already a two-node cycle), and an unmarked search would loop forever.
- `a/a` costs no special case: the seed `(a, 1.0)` is popped first and matches the target, yielding `1.0`.

### Weighted Union-Find

#### Derivation

Breadth-first search answers each query correctly, but the statement warns that the query stream can be very large and can repeat the same ordered pairs: every repeated pair re-walks the same edges. The observation that removes that cost is that the equations are valid and mutually consistent, so they partition the variables into components in which every quotient is already determined. Hang every variable below its component's `root` with a stored `weight` recording `variable / root`, and any quotient between connected variables becomes one division of stored weights, so a query costs two root lookups instead of a traversal. Merging components is the algebra of a [union-find](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) whose parent pointers carry weights:

1. Start `parent`, `weight`, and `rank` empty; the first time a variable
   appears, it becomes its own root with `weight` `1.0`.
2. For each equation `numerator / denominator = ratio`, compress both `find`
   paths, then attach the lower-rank root under the higher-rank one with the
   weight that keeps the invariant below true.
3. For each query, return -1.0 when either variable is unknown or the two
   `find` roots differ; otherwise return `weight[query_numerator] /
   weight[query_denominator]`.

#### Invariant

Let `root(variable)` be the root `find` returns, and let `weight[variable]` record `variable / root(variable)`. The structure is correct exactly while this holds for every known variable:

$$ \frac{x}{root(x)} = weight[x] $$

```text
weight[v] = v / root(v)                for every known variable v
find:      fold products into each node along the path to the root, so
           compression keeps every weight root-relative
union:     attaching root_numerator under root_denominator sets
           weight[root_numerator] = ratio * weight[denominator]
           attaching root_denominator under root_numerator sets
           weight[root_denominator] = weight[numerator] / ratio
query:     root(x) == root(y)  =>  x / y = weight[x] / weight[y]
```

Reading it back: compression multiplies each node's stored weight by its parent's, because `x/z = (x/y) * (y/z)`. The union assignment is the one line that looks arbitrary: with `weight[numerator]` already equal to `numerator / root_a` after compression, `weight[numerator] / ratio` equals `(numerator / root_a) / (numerator / denominator)`, which is `denominator / root_a`, exactly the new `root_b / root_a` the invariant demands.

#### Walkthrough

Let us build the structure over Example 1's two equations and then answer its five queries. Union `a/b = 2.0` first: both variables are fresh roots of weight `1.0` with tied ranks, so `b` hangs under `a`:

```text
union a/b 2.0   parent[b] = a, weight[b] = 1.0 / 2.0 = 0.5
union b/c 3.0   find(b) keeps root a, weight[b] = 0.5 already root-relative
                parent[c] = a, weight[c] = weight[b] / 3.0 = 1/6
                component {a, b, c}, root a, every weight relative to a
query a/c   same root   weight[a] / weight[c] = 1.0 / (1/6) = 6.0
query b/a   same root   weight[b] / weight[a] = 0.5 / 1.0   = 0.5
query a/e   e unknown                                         -1.0
query a/a   same root   weight[a] / weight[a] = 1.0
query x/x   x unknown                                         -1.0
```

The `b/c` union never recomputes `a`: `find(b)` has already left `weight[b]` carrying `b / a = 0.5`, and dividing by `3.0` turns it into `c / a = 1/6` for `c`. The collected quotients are `[6.0, 0.5, -1.0, 1.0, -1.0]`, matching the expected Output for Example 1, and every later query over this component is a single division of two stored weights.

#### Solution

The code is the invariant from the walkthrough: `find` restores it along its path, `union` preserves it while merging, and each query reads it off.

```python
from typing import List


class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float],
                     queries: List[List[str]]) -> List[float]:
        parent: dict[str, str] = {}
        weight: dict[str, float] = {}
        rank: dict[str, int] = {}

        def find(variable: str) -> str:
            path: list[str] = []
            walker = variable
            while parent[walker] != walker:
                path.append(walker)
                walker = parent[walker]
            root = walker
            accumulated = 1.0
            for node in reversed(path):
                accumulated *= weight[node]
                weight[node] = accumulated
                parent[node] = root
            return root

        def union(numerator: str, denominator: str, ratio: float) -> None:
            root_numerator = find(numerator)
            root_denominator = find(denominator)
            if root_numerator == root_denominator:
                return
            if rank[root_numerator] < rank[root_denominator]:
                parent[root_numerator] = root_denominator
                weight[root_numerator] = ratio * weight[denominator]
            else:
                parent[root_denominator] = root_numerator
                weight[root_denominator] = weight[numerator] / ratio
                rank[root_numerator] += 1

        for (numerator, denominator), ratio in zip(equations, values):
            for variable in (numerator, denominator):
                if variable not in parent:
                    parent[variable] = variable
                    weight[variable] = 1.0
                    rank[variable] = 0
            union(numerator, denominator, ratio)

        quotients = []
        for query_numerator, query_denominator in queries:
            if (query_numerator not in parent
                    or query_denominator not in parent
                    or find(query_numerator) != find(query_denominator)):
                quotients.append(-1.0)
            else:
                quotients.append(
                    weight[query_numerator] / weight[query_denominator])
        return quotients
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((E + Q) × α(V))`

Let `E` be the number of equations, `Q` the number of queries, and `V` the number of distinct variables: every equation performs at most two union operations and every query at most two `find` operations, each amortized to inverse-Ackermann time `a` under path compression and union by rank.

##### Space Complexity: `O(V)`

The three dicts hold one entry per variable, and a `find` path holds at most `V` nodes.

#### Key Insights

- The component partition is where the speedup lives: the ratio structure is shared by every pair in a component, so paying once per equation to embed each variable's ratio to its root answers all future queries in constant time.
- Weighted union-find is plain union-find plus the invariant; only two lines differ from the standard structure, the `weight` initialization and the `weight` assignment in `union`.
- Path compression does double duty: it flattens the tree and it converts every node's weight to be root-relative, which is exactly the form queries read.
- The iterative `find` collects the path first and folds weights from the root side down; folding while walking upward would multiply each node by its parent's still-stale weight.

## Comparison of Solutions

### Time Complexity

- **BFS over the Ratio Graph**: `O(E + Q × (V + E))` - each query traverses its component independently.
- **Weighted Union-Find**: `O((E + Q) × α(V))` - equations and queries alike resolve through near-constant root lookups.

### Space Complexity

- **BFS over the Ratio Graph**: `O(V + E)` - the adjacency dict plus one search's queue and visited set.
- **Weighted Union-Find**: `O(V)` - one parent, weight, and rank entry per variable.

### Trade-offs

- The BFS approach is a single idea (weighted edges and path products) with no algebra to get wrong, but it re-pays the traversal for every query, which the statement's large repeated query stream punishes directly.
- The union-find approach front-loads the work into preprocessing and then answers any number of queries in near-constant time, at the cost of the weight invariant and the two-branch union algebra.

### When to Use Each

- **BFS over the Ratio Graph**: small query counts, or when equations and queries interleave dynamically so the graph keeps growing between searches.
- **Weighted Union-Find (Recommended)**: the interview answer under this problem's own constraints, where up to 200000 queries hit at most 200000 equations and reuse dominates.

### Optimization Notes

- The union-find version is the direct answer to the statement's reuse warning: preprocessing component weights once turns each query into a dictionary division.
- `find` is iterative on purpose: with up to 200000 equations a recursive `find` can exceed Python's recursion limit, while the collect-then-fold loop cannot.
- Union by rank keeps the trees shallow even before compression; compression alone would already be fast in practice but carries an `O(log V)` worst case instead of `α(V)`.
- A memo dict over seen query pairs would save the two `find` calls per repeat, a constant-factor saving on a structure that is already near-constant per query.
