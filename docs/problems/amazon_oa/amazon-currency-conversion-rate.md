# [Currency Conversion Rate](https://www.fastprep.io/problems/amazon-currency-conversion-rate)

**Medium** | **NN minutes** | **Graph, Breadth First Search, Hash Table**

You are given currency conversion rates. Each row contains a source currency, a target currency, and the value of one unit of the source currency in the target currency.

A conversion may use multiple rates. A listed rate may also be used in reverse by taking its reciprocal.

Given a query [from, to], return the conversion rate from from to to, rounded and formatted with exactly two digits after the decimal point. Every judged query is connected by the supplied rates.

## Examples

### Example 1

**Input:** `rates = [["USD","JPY","110"],["USD","AUD","1.45"],["JPY","GBP","0.0070"]]`, `query = ["GBP","AUD"]`

**Output:** `"1.88"`

**Explanation:** Use the reverse of JPY -> GBP, then the reverse of USD -> JPY, then USD -> AUD: (1 / 0.0070) * (1 / 110) * 1.45 = 1.883116.... Rounded to two decimal places, the result is 1.88.

### Example 2

**Input:** `rates = [["USD","CAD","1.30"],["CAD","EUR","0.70"]]`, `query = ["USD","EUR"]`

**Output:** `"0.91"`

**Explanation:** One USD is 1.30 CAD, and one CAD is 0.70 EUR, so the rate is 1.30 * 0.70 = 0.91.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-currency-conversion-rate; fill them in. -->

## Solutions

### BFS over the Rate Graph

#### Derivation

Every rate row is a directed, weighted edge between two currencies: `rates[i] = [source, target, value]` means one unit of `source` buys `value` units of `target`, so the edge from `source` to `target` carries the multiplier `value` and the reverse edge carries `1.0 / value`. Under that reading, the conversion rate for `query = [source_currency, target_currency]` is the product of edge multipliers along any path between the two currencies, which is exactly what a breadth-first search with a running product computes. Every judged query is promised connected by the supplied rates, so the search always reaches its target; the -1.0 fallback stays in the code for safety and costs nothing:

1. Build `graph`, mapping each currency to the dict of its outgoing neighbors
   and their multipliers: `graph[source][target] = rate` and
   `graph[target][source] = 1.0 / rate`.
2. Seed `queue` with `(source_currency, 1.0)` and mark `source_currency` in
   `visited`.
3. Pop `(currency, product)`; when `currency == target_currency`, the conversion
   rate is `product`.
4. Otherwise push every unvisited `neighbor` with `product * edge_rate`; an
   emptied queue without a hit means the currencies are disconnected, and the
   result falls back to -1.0.
5. Format the found rate with `f"{converted:.2f}"`, which rounds and renders it
   with exactly two digits after the decimal point.

#### Walkthrough

Let us run Example 1 by hand: `rates = [["USD","JPY","110"],["USD","AUD","1.45"],["JPY","GBP","0.0070"]]`, `query = ["GBP","AUD"]`. Building `graph` yields six directed edges:

```text
USD -> JPY 110        JPY -> USD 1/110
USD -> AUD 1.45       AUD -> USD 1/1.45
JPY -> GBP 0.0070     GBP -> JPY 1/0.0070
```

The search starts at `GBP`, and each line below is one queue event:

```text
pop (GBP, 1.0)          push (JPY, 1 / 0.0070        = 142.8571429)
pop (JPY, 142.8571429)  push (USD, 142.8571429 / 110 = 1.2987013)
pop (USD, 1.2987013)    push (AUD, 1.2987013 * 1.45  = 1.8831169)
pop (AUD, 1.8831169)    target reached: converted = 1.8831169
```

The path rides the reciprocal edge `GBP -> JPY`, then the reciprocal `JPY -> USD`, then the forward edge `USD -> AUD`, composing to `(1 / 0.0070) * (1 / 110) * 1.45 = 1.8831169`, the same product the Example 1 explanation states. Formatted to two decimals the function returns `"1.88"`, matching the expected Output. Example 2 composes two forward edges, `1.30 * 0.70 = 0.91`, and returns `"0.91"`.

#### Solution

The code is the walkthrough: one dict of neighbor dicts, one queue of `(currency, product)` pairs, and one format call at the end.

```python
from collections import deque
from typing import List


class Solution:
    def findConversionRate(self, rates: List[List[str]], query: List[str]) -> str:
        source_currency, target_currency = query
        graph: dict[str, dict[str, float]] = {}
        for source, target, rate_text in rates:
            rate = float(rate_text)
            graph.setdefault(source, {})[target] = rate
            graph.setdefault(target, {})[source] = 1.0 / rate

        converted = -1.0
        visited = {source_currency}
        queue = deque([(source_currency, 1.0)])
        while queue:
            currency, product = queue.popleft()
            if currency == target_currency:
                converted = product
                break
            for neighbor, edge_rate in graph[currency].items():
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, product * edge_rate))
        return f"{converted:.2f}"
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(R + C)`

Let `R` be the number of rate rows and `C` the number of distinct currencies: building the graph touches every row once, and the search visits every currency and directed edge of the component at most once.

##### Space Complexity: `O(C + R)`

The graph stores two directed entries per rate row, and one search holds up to `C` queue entries and visited marks.

#### Key Insights

- Conversion composes multiplicatively along paths, and every listed rate must be stored in both directions, the reverse carrying the reciprocal; that is what lets the search travel `GBP -> JPY -> USD -> AUD` from three rows.
- The `visited` set is not optional: `USD -> JPY` and `JPY -> USD` already form a two-node cycle, and an unmarked search would loop forever.
- Seeding the queue with `(source_currency, 1.0)` makes a same-currency query fall out naturally: the seed pops first and matches the target with rate `1.0`.
- The search stays in floats and the two-decimal formatting happens once at the end; the product `1.8831169` rounds to `"1.88"` with a wide margin, so binary float representation error never comes close to mattering.

### Weighted Union-Find

#### Derivation

Breadth-first search answers one query by walking its component, and it would pay that walk again for every query in a stream. The statement's promise that every judged query is connected means the rate table partitions the currencies into components in which every conversion is already determined, so paying once per row to store each currency's ratio to its component `root` turns any later query into one division of two stored weights. That preprocessing is the algebra of a [union-find](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) whose parent pointers carry weights:

1. Start `parent`, `weight`, and `rank` empty; the first time a currency
   appears, it becomes its own root with `weight` `1.0`.
2. For each row `source / target = rate`, compress both `find` paths, then
   attach the lower-rank root under the higher-rank one with the weight that
   keeps the invariant below true.
3. For the query, return `-1.00` when either currency is unknown or the two
   `find` roots differ; otherwise divide `weight[source_currency]` by
   `weight[target_currency]` and format the quotient to two decimals.

#### Invariant

Let `root(currency)` be the root `find` returns, and let `weight[currency]` record `currency / root(currency)`, the value of one unit of the currency expressed in root units. The structure is correct exactly while this holds for every known currency:

$$ \frac{c}{root(c)} = weight[c] $$

```text
weight[v] = v / root(v)                  for every known currency v
find:      collect the path, then fold products from the root side down, so
           compression leaves every weight root-relative
union:     root_source / root_target = rate * weight[target] / weight[source],
           so attaching root_source under root_target sets
           weight[root_source] = rate * weight[target] / weight[source]
           attaching root_target under root_source sets
           weight[root_target] = weight[source] / (rate * weight[target])
query:     root(x) == root(y)  =>  x / y = weight[x] / weight[y]
```

Reading it back: compression multiplies each node's stored weight by its parent's, because `x/z = (x/y) * (y/z)`. The union lines are where a wrong factor is easy to hide: after compression `weight[source] = source / root_source`, so `root_source = source / weight[source]` and `root_source / root_target = rate * weight[target] / weight[source]`. Both `weight` factors are required; each equals `1.0` only while the endpoint is still a fresh singleton root, which is why small examples pass with the factors dropped while the first merge of two grown components silently corrupts every later cross-boundary query.

#### Walkthrough

Let us build the structure over Example 1's three rows and then answer the query. Every union here attaches a fresh singleton root, so each `weight` factor in the union lines is `1.0`:

```text
union USD/JPY 110     parent[JPY] = USD, weight[JPY] = 1.0 / 110   = 0.0090909
union USD/AUD 1.45    parent[AUD] = USD, weight[AUD] = 1.0 / 1.45  = 0.6896552
union JPY/GBP 0.0070  find(JPY) -> USD, weight[JPY] already root-relative
                      parent[GBP] = USD,
                      weight[GBP] = 0.0090909 / 0.0070             = 1.2987013
                      component {USD, JPY, AUD, GBP}, root USD
query GBP/AUD   same root   weight[GBP] / weight[AUD]
                      = 1.2987013 / 0.6896552 = 1.8831169
```

Each stored weight is the currency's value in USD: one JPY is `1/110` USD, one AUD is `1/1.45` USD, and one GBP is `(1/0.0070) JPY = 1.2987013` USD. The query divides the two stored weights, `1.8831169`, and the function formats it as `"1.88"`, matching the expected Output for Example 1.

#### Solution

The code is the invariant from the walkthrough: `find` restores it along its path, `union` preserves it while merging, and the query reads it off with one division.

```python
from typing import List


class Solution:
    def findConversionRate(self, rates: List[List[str]], query: List[str]) -> str:
        source_currency, target_currency = query
        parent: dict[str, str] = {}
        weight: dict[str, float] = {}
        rank: dict[str, int] = {}

        def find(currency: str) -> str:
            path: list[str] = []
            walker = currency
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

        def union(source: str, target: str, rate: float) -> None:
            root_source = find(source)
            root_target = find(target)
            if root_source == root_target:
                return
            if rank[root_source] < rank[root_target]:
                parent[root_source] = root_target
                weight[root_source] = rate * weight[target] / weight[source]
            else:
                parent[root_target] = root_source
                weight[root_target] = weight[source] / (rate * weight[target])
                rank[root_source] += 1

        for source, target, rate_text in rates:
            for currency in (source, target):
                if currency not in parent:
                    parent[currency] = currency
                    weight[currency] = 1.0
                    rank[currency] = 0
            union(source, target, float(rate_text))

        if (source_currency not in parent
                or target_currency not in parent
                or find(source_currency) != find(target_currency)):
            converted = -1.0
        else:
            converted = weight[source_currency] / weight[target_currency]
        return f"{converted:.2f}"
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(R × α(C))`

Let `R` be the number of rate rows and `C` the number of distinct currencies: every row performs at most two union operations and the query at most two `find` operations, each amortized to inverse-Ackermann time `α` under path compression and union by rank.

##### Space Complexity: `O(C)`

The three dicts hold one entry per currency, and a `find` path holds at most `C` nodes.

#### Key Insights

- The component partition is where the speedup lives: storing each currency's ratio to its root once answers every future query with two root lookups and a division, which is the right shape when the problem extends to many queries over one rate table.
- Weighted union-find is plain union-find plus the invariant; only the `weight` initialization and the two `weight` assignments in `union` differ from the standard structure.
- Path compression does double duty: it flattens the tree and it converts every weight to be root-relative, exactly the form the query division reads.
- The iterative `find` collects the path first and folds weights from the root side down; folding while walking upward would multiply each node by its parent's still-stale weight.

## Comparison of Solutions

### Time Complexity

- **BFS over the Rate Graph**: `O(R + C)` - one graph build plus one component walk for the query.
- **Weighted Union-Find**: `O(R × α(C))` - one near-constant merge per row and near-constant root lookups for the query.

### Space Complexity

- **BFS over the Rate Graph**: `O(C + R)` - the adjacency dict plus one search's queue and visited set.
- **Weighted Union-Find**: `O(C)` - one parent, weight, and rank entry per currency.

### Trade-offs

- The BFS approach is a single idea (weighted edges and path products) with no algebra to get wrong, but every query re-walks its component from scratch.
- The union-find approach front-loads the work into preprocessing and then answers any number of queries with two root lookups and a division, at the cost of the weight invariant and the two-branch merge algebra.

### When to Use Each

- **BFS over the Rate Graph (Recommended)**: the single judged query of this statement, or rate tables that change between queries, where preprocessing would have to be redone anyway.
- **Weighted Union-Find**: a query stream over a fixed rate table, the common follow-up phrasing ("answer Q queries"); preprocessing once and dividing stored weights wins from the second query onward.

### Optimization Notes

- The two approaches are the same ratio algebra: the search recomputes the path product per query, while the union-find stores it incrementally relative to a root.
- `find` is iterative on purpose: a recursive `find` can exceed Python's recursion limit on deep currency chains, while the collect-then-fold loop cannot.
- The union `weight` lines carry the only real hazard of the second approach: dropping either `weight` factor passes every example built from fresh singletons and breaks the first query that crosses a merged boundary.
- A memo dict over answered query pairs would save the two `find` calls per repeated pair, a constant-factor saving on a structure that is already near-constant per query.
