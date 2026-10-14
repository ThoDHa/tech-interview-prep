# [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/)

**Medium** | **25 minutes** | **Dynamic Programming, Depth-First Search, Breadth-First Search, Graph Theory, Heap (Priority Queue), Shortest Path**

**Pattern:** [Shortest Path](../patterns/shortest_path/intuition.md)

**Algorithm:** [Bellman-Ford algorithm](https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm) · [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization) · [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search)

**Practice:** [`practice/cheapest_flights_within_k_stops/solution.py`](../../practice/cheapest_flights_within_k_stops/solution.py)

There are `n` airports, labeled from `0` to `n - 1`, which are connected by some flights. You are given an array `flights` where `flights[i] = [from_i, to_i, price_i]` represents a one-way flight from airport `from_i` to airport `to_i` with cost `price_i`. You may assume there are no duplicate flights and no flights from an airport to itself.

You are also given three integers `src`, `dst`, and `k` where:

* `src` is the starting airport
* `dst` is the destination airport
* `src != dst`
* `k` is the maximum number of stops you can make (not including `src` and `dst`)

Return **the cheapest price** from `src` to `dst` with at most `k` stops, or return `-1` if it is impossible.

## Examples

### Example 1

**Input:** `n = 4, flights = [[0,1,200],[1,2,100],[1,3,300],[2,3,100]], src = 0, dst = 3, k = 1`

**Output:** `500`

**Explanation:** The optimal path with at most 1 stop from airport 0 to 3 is shown in red, with total cost `200 + 300 = 500`.
Note that the path `[0 -> 1 -> 2 -> 3]` costs only 400, and thus is cheaper, but it requires 2 stops, which is more than k.

### Example 2

**Input:** `n = 3, flights = [[1,0,100],[1,2,200],[0,2,100]], src = 1, dst = 2, k = 1`

**Output:** `200`

**Explanation:** The optimal path with at most 1 stop from airport 1 to 2 is shown in red and has cost `200`.

## Constraints

- `1 <= n <= 100`
- `fromi != toi`
- `1 <= pricei <= 1000`
- `0 <= src, dst, k < n`

## Deriving the Solution

Splitting a route at any flight leaves a smaller copy of itself: whatever the first leg costs, the rest must be the cheapest completion from the airport it lands on with one fewer flight affordable. The state `(airport, flights still affordable)` therefore determines every optimal continuation, and the solutions below are all searches of that state space; they differ in the order they fill it and the states they refuse to revisit.

1. **Start literal.** Enumerate routes exactly as the rules state them: fly any
   flight out of the current airport, recurse with one fewer flight affordable, and keep the cheapest branch that reaches `dst`. Correct, but the same airport is re-solved under the same budget across countless interleavings of the same flights, costing `O(n^(k + 1))`: see [Brute Force Recursion](#brute-force-recursion).
2. **Cache the repeats.** The future depends only on the pair
   `(node, flights_left)`, never on the route that produced it, so storing each pair's answer the first time it is computed collapses the exponential tree to at most `n × (k + 1)` cells: see [Top-Down Memoization](#top-down-memoization).
3. **Flip the direction.** The cached recursion still explores lazily, in call
   order. Reframed as a recurrence over layers, `dp[t][v]` is the cheapest price using at most `t` flights, and each layer reads only the frozen previous one, so `k + 1` sweeps over the raw flight list finish the table: see [Bellman-Ford Relaxation Sweeps](#bellman-ford-relaxation-sweeps).
4. **Pay only for what the answer needs.** The sweeps price every airport,
   including ones no answer needs, and with positive prices the cheapest unsettled state can never be beaten later: expanding states in price order with the flight count riding along as a third coordinate lets the search stop the moment `dst` pops: see [Dijkstra's Algorithm with Stop Budgets](#dijkstras-algorithm-with-stop-budgets).
5. **Hand the cache to the library.** Step 2's memo is not part of the
   recursion, only a dictionary bolted onto it. Decorating the brute-force function with `functools.cache` deletes the lookup and the store while leaving the recursion and both base cases untouched: see [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Brute Force Recursion

#### Derivation

The most literal reading of the problem enumerates routes: fly any flight out of `src`, then any flight out of that airport, and stop when either `dst` is reached or flying further would exceed the budget. Since every price is at least `1`, an optimal route never revisits an airport, so plain recursion over the flight budget explores exactly the meaningful routes, and the stop limit becomes a simple counter of remaining flights:

1. Build the adjacency list `adjacency` from `flights`, mapping each airport to
   its `(neighbor, price)` pairs.
2. Define `dfs(node, flights_left)`: the cheapest cost of completing the route
   to `dst` from `node` when `flights_left` flights may still be taken.
3. Base cases: at `dst` the remaining route costs `0`; with
   `flights_left == 0` no flight may be taken, so an unfinished route is impossible (`None`).
4. Otherwise take the `min` of `price + dfs(neighbor, flights_left - 1)` over
   every `(neighbor, price)` outgoing flight whose branch is possible.
5. Run `dfs(src, k + 1)` (a route with `k` stops uses at most `k + 1` flights)
   and map `None` to `-1`.

#### Walkthrough

Let us enumerate the routes by hand on Example 1: `n = 4`, `flights = [[0,1,200],[1,2,100],[1,3,300],[2,3,100]]`, `src = 0`, `dst = 3`, `k = 1`, so the budget is `2` flights. The adjacency lists are `adjacency[0] = [(1, 200)]`, `adjacency[1] = [(2, 100), (3, 300)]`, `adjacency[2] = [(3, 100)]`, `adjacency[3] = []`, and the trace indents one level per call:

```text
dfs(0, 2)   try 0 -> 1 (200)
  dfs(1, 1)   try 1 -> 2 (100)
    dfs(2, 0)   not dst, budget spent -> None
  try 1 -> 3 (300)
    dfs(3, 0)   dst reached -> 0
  -> 300            best = 300 + 0
-> 500              best = 200 + 300
```

The branch through airport `2` dies at `dfs(2, 0)`: reaching `dst` from there would need a third flight, and none is affordable. The surviving branch lands on `dst` with the direct hop `1 -> 3`, so the cheapest total is `200 + 300 = 500`, matching the expected Output for Example 1. The cheaper `0 -> 1 -> 2 -> 3` route exists in the graph but needs `3` flights, one beyond the budget, and the recursion never extends that branch far enough to price it.

#### Solution

The code is the route enumeration written down: a base case at `dst`, a budget guard, and a `min` over outgoing flights.

```python
from typing import List, Optional


class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        adjacency = [[] for _ in range(n)]
        for u, v, price in flights:
            adjacency[u].append((v, price))

        def dfs(node: int, flights_left: int) -> Optional[int]:
            if node == dst:
                return 0
            if flights_left == 0:
                return None
            best = None
            for neighbor, price in adjacency[node]:
                rest = dfs(neighbor, flights_left - 1)
                if rest is not None and (best is None or price + rest < best):
                    best = price + rest
            return best

        best = dfs(src, k + 1)
        return -1 if best is None else best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^(k + 1))`

The recursion tree branches over the outgoing flights of the current airport and descends `k + 1` levels. Each level branches at most `n - 1` ways on a dense graph, so the tree reaches `O(n^(k + 1))` leaves, and each level does constant work per call on top of them.

##### Space Complexity: `O(n + e)`

The adjacency lists store all `e` flights, and the recursion stack descends at most `k + 1 <= n` frames, which the `O(n)` term covers.

#### Key Insights

- Converting stops to a flight budget (`k + 1` flights) turns the stop rule into
  a single counter, which every later solution reuses.
- Positive prices mean an optimal route never revisits an airport, so the
  recursion is finite even though the graph may contain cycles; no `visited` set is needed.
- The exponential cost is pure repetition: the same `(airport, remaining
  budget)` pair is re-solved across countless interleavings of the same flights.

### Top-Down Memoization

#### Derivation

The brute force re-solves subproblems because a route's remaining cost depends only on where it stands and how many flights it may still take, not on the order that led there. When two different prefixes land on the same airport with the same remaining budget, everything below them is computed twice. A memo table keyed by that pair collapses the repetition while leaving the recursion itself untouched:

1. Keep `dp(node, flights_left)` exactly as the brute force's `dfs`: return `0`
   at `dst`, `None` with an empty budget, otherwise the `min` of
   `price + dp(neighbor, flights_left - 1)` over the outgoing flights.
2. Declare `memo` and, before computing, return
   `memo[(node, flights_left)]` when the pair is already stored; store each
   freshly computed result there.
3. Run `dp(src, k + 1)` and map `None` to `-1`.

There are at most `n × (k + 1)` distinct pairs, so the exponential tree collapses to that many computed cells.

#### Walkthrough

Example 1 exercises the machinery, but a tailored input shows a cache hit, which no official example produces. Consider `n = 5`, `flights = [[0,1,1],[0,2,2],[1,3,5],[2,3,1],[3,4,10]]`, `src = 0`, `dst = 4`, `k = 2`. Both routes to airport `3` leave the same remaining budget, so the second arrival is served from `memo`:

```text
dp(0, 3)                      try 0 -> 1 (1)
  dp(1, 2)                    try 1 -> 3 (5)
    dp(3, 1)                  try 3 -> 4 (10)
      dp(4, 0)  -> 0          dst reached
    -> 10                     memo[(3, 1)] = 10
  -> 15                       memo[(1, 2)] = 15
  try 0 -> 2 (2)
  dp(2, 2)                    try 2 -> 3 (1)
    dp(3, 1)  -> 10           ** cache hit **
  -> 11                       memo[(2, 2)] = 11
-> 13                         min(1 + 15, 2 + 11) = 13
```

Five calls run the body, one per distinct pair: the entry call at airport `0`, the base case at airport `4`, and the three stored results. The second route to airport `3` reused `memo[(3, 1)]` instead of re-flying the tail to `dst`. The answer is `min(1 + 15, 2 + 11) = 13`, the route `0 -> 2 -> 3 -> 4`.

#### Solution

The code is the brute force recursion plus a two-line memo: look up before computing, store after.

```python
from typing import List, Optional


class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        adjacency = [[] for _ in range(n)]
        for u, v, price in flights:
            adjacency[u].append((v, price))

        memo = {}

        def dp(node: int, flights_left: int) -> Optional[int]:
            if node == dst:
                return 0
            if flights_left == 0:
                return None
            if (node, flights_left) in memo:
                return memo[(node, flights_left)]
            best = None
            for neighbor, price in adjacency[node]:
                rest = dp(neighbor, flights_left - 1)
                if rest is not None and (best is None or price + rest < best):
                    best = price + rest
            memo[(node, flights_left)] = best
            return best

        best = dp(src, k + 1)
        return -1 if best is None else best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(k × e)`

Each of the at most `n × (k + 1)` distinct `(node, flights_left)` pairs runs its body once, and one body execution relaxes the airport's out-degree of edges. Summed over all pairs the edge relaxations total `O(k × e)`, matching the sweeps of the next solution without their ordering.

##### Space Complexity: `O(n × k + e)`

The adjacency lists hold all `e` flights, the memo holds one entry per computed pair, and the recursion stack descends at most `k + 1` frames.

#### Key Insights

- The state `(node, flights_left)` is the whole problem in miniature: the
  cheapest completion from an airport with a given budget. Every later solution
  manipulates this same state space with a different execution order.
- The memo never changes an answer, only the number of times it is computed;
  the recursion reads exactly as the brute force with three added lines.
- The pair count `n × (k + 1)` is the bridge from exponential to polynomial:
  the tree is huge, but its distinct nodes are few.

### Bellman-Ford Relaxation Sweeps

#### Derivation

The memoized recursion fills the state space lazily, in whatever order the calls reach it. Reading the same states as a table admits a chosen order instead: layer by layer, each sweep extending every airport's answer by exactly one flight, so the layer index is a flight count and sweeping the table is what enforces the stop budget. A sweep needs nothing but the previous layer: the recurrence below states the rule, and the solution collapses the table to two arrays.

#### Recurrence

Let `dp[t][v]` be the cheapest price of any route from `src` to `v` using at most `t` flights:

$$ dp[t][v] = \begin{cases}
0, & v = \textit{src},\ t \ge 0 \\[4pt]
\min\bigl(dp[t-1][v],\ \min_{(u \to v) \in E} dp[t-1][u] + \textit{price}_{uv}\bigr), & t > 0
\end{cases} $$

```text
dp[0][src] = 0                        dp[0][v] = impossible for v != src
dp[t][v] = min(dp[t-1][v],            stay: still at most t-1 flights used
               min over flights u -> v of dp[t-1][u] + price)
answer = dp[k + 1][dst]               k stops = k + 1 flights
```

The previous layer `dp[t - 1]` is read, never written, so every route counted in layer `t` uses at most one more flight than in layer `t - 1`: the sweep count is the budget. The answer is read at `dst` after `k + 1` sweeps, with `-1` wherever the impossible marker survives.

#### Walkthrough

Let us sweep by hand on Example 1: `n = 4`, `flights = [[0,1,200],[1,2,100],[1,3,300],[2,3,100]]`, `src = 0`, `dst = 3`, `k = 1`, so three layers with `None` playing the impossible marker:

```text
layer 0     [0, None, None, None]
layer 1     0->1: 0+200      [0, 200, None, None]
layer 2     1->2: 200+100    [0, 200, 300, None]
            1->3: 200+300    [0, 200, 300, 500]
            2->3: 300+100    frozen layer-1[2] is None -> rejected
```

The rejection in layer 2 is the whole algorithm: airport `3` may inherit from `layer 1[1] = 200` (the route `0 -> 1 -> 3`), but the tempting `300 + 100 = 400` through airport `2` would build on the value `layer 2[2] = 300`, which already spent the entire budget. Because the sweep reads only the frozen previous layer, that route cannot leak in, and `dp[2][3] = 500` matches the expected Output for Example 1. A run without the freeze writes `400` into layer 2 and returns the under-budgeted answer; letting `k = 2` on the same input admits `400` through the same relaxation.

#### Solution

The code is the recurrence with the previous layer frozen per sweep: sweep `k + 1` times, then read `dst`.

```python
from typing import List


class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        distances = [None] * n
        distances[src] = 0

        # One sweep per additional flight the budget allows: k stops = k + 1 flights.
        for _ in range(k + 1):
            previous = distances[:]
            for u, v, price in flights:
                if previous[u] is not None and (
                    distances[v] is None or previous[u] + price < distances[v]
                ):
                    distances[v] = previous[u] + price

        return -1 if distances[dst] is None else distances[dst]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(k × e)`

Each of the `k + 1` sweeps reads every flight once and does constant work per flight, with no adjacency structure to build or sort.

##### Space Complexity: `O(n)`

Two distance arrays of `n` entries; the flight list is swept directly from the input.

#### Key Insights

- Limiting Bellman-Ford to `k + 1` sweeps is the stop budget: with at most `t`
  sweeps, every recorded distance uses at most `t` flights, so the count itself is the constraint.
- The frozen `previous = distances[:]` per sweep is what makes each sweep count
  as exactly one flight; relaxing in place would let a route gain many flights within one sweep and exceed the budget (it returns `400` on Example 1).
- `None` as the impossible marker keeps a genuine `0`-cost state (`src`) from
  being confused with "no route yet", which matters because a route can only be extended from airports that are actually reachable.
- No adjacency list is ever built, making this the natural fit when the edge
  list is small or streamed.

### Dijkstra's Algorithm with Stop Budgets

#### Derivation

The sweeps price every airport, though only `dst` is wanted, and they reprice an airport as many times as its in-degree even when the improvement is worthless under the budget. [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) orders the work by price: with all prices positive, the cheapest unsettled state in the frontier can never be beaten by a detour through another unsettled state, so its first pop is final. The state grows a third coordinate, the number of flights taken, because a cheaper price with more flights used and a dearer price with fewer are genuinely different futures under the budget. A second array, `fewest_edges`, keeps the frontier from drowning in budget-discarded states:

1. Build the adjacency lists.
2. Initialize `fewest_edges` to `k + 2` for every airport, one past the budget,
   and push `(0, src, 0)` into a min-heap. The source's `0` flights sit below
   the marker, so the first pop expands it without a special case.
3. Pop the smallest `(price, node, edges_used)`. At `dst`, `price` is the
   answer: the heap orders by price, so no later state can be cheaper.
4. Skip the state when `edges_used == k + 1` (budget spent) or
   `edges_used >= fewest_edges[node]` (a cheaper-price state with at most as
   many flights already expanded `node`).
5. Otherwise record `fewest_edges[node] = edges_used` and push
   `(price + cost, neighbor, edges_used + 1)` for each outgoing flight.
6. When the heap empties without popping `dst`, return `-1`.

#### Walkthrough

Let us run the heap on Example 1: `n = 4`, `flights = [[0,1,200],[1,2,100],[1,3,300],[2,3,100]]`, `src = 0`, `dst = 3`, `k = 1`, so the flight budget is `2`:

```text
push (0, 0, 0)
pop (0, 0, 0)    expand 0->1            push (200, 1, 1)
pop (200, 1, 1)  expand 1->2, 1->3      push (300, 2, 2), (500, 3, 2)
pop (300, 2, 2)  edges_used == 2 = budget spent: skip
pop (500, 3, 2)  dst reached -> return 500
```

The heap's price order settles the question before the budget does: `(300, 2, 2)` is skipped for having spent the whole budget on a state that is not even the destination, and `(500, 3, 2)` pops next because no cheaper state to `dst` exists anywhere in the frontier. The function returns `500`, matching the expected Output for Example 1, and never touches the forbidden `400` route, whose states were pruned before they could win.

#### Solution

The code is the priced frontier: pop cheapest, stop at `dst`, prune by budget and by the `fewest_edges` record.

```python
import heapq
from typing import List


class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        adjacency = [[] for _ in range(n)]
        for u, v, price in flights:
            adjacency[u].append((v, price))

        fewest_edges = [k + 2] * n
        heap = [(0, src, 0)]

        while heap:
            price, node, edges_used = heapq.heappop(heap)
            if node == dst:
                return price
            if edges_used == k + 1:
                continue
            if edges_used >= fewest_edges[node]:
                continue
            fewest_edges[node] = edges_used
            for neighbor, cost in adjacency[node]:
                heapq.heappush(heap, (price + cost, neighbor, edges_used + 1))
        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(e × k × log(e × k))`

Each of the `n × (k + 1)` states can be expanded at most once (guarded by `fewest_edges`), expanding a state pushes one entry per outgoing flight, so the heap holds `O(e × k)` entries across the run and costs logarithmic work per push or pop.

##### Space Complexity: `O(n + e × k)`

The adjacency lists hold all `e` flights, `fewest_edges` is `O(n)`, and the heap accumulates at most one pushed entry per edge relaxation, `O(e × k)`.

#### Key Insights

- Shortest paths here are cheapest first, not fewest flights first: the heap
  must order by price, and the budget rides along as a third state coordinate.
- Settling by price needs positive prices, which the constraints guarantee
  (`1 <= price_i`); with free flights the first pop to a state could lose to a pricier one that later flies cheaper, and the Bellman-Ford sweeps above become the honest tool.
- `fewest_edges` is a dominance filter, not a visited set: it discards a state
  only when an equal-price-or-cheaper state with at most as many flights already expanded the airport, which keeps the heap linear-sized in spirit.
- Pricier-but-shorter states are kept deliberately: dropping them would let the
  budget prune the only routes that survive it, which is exactly the failure mode of plain Dijkstra on this problem.

### Top-Down Memoization with functools.cache

#### Derivation

The [Top-Down Memoization](#top-down-memoization) solution is the brute force recursion plus a dictionary that keeps it from re-solving an `(airport, budget)` pair it has already answered. The recursion is the algorithm; the dictionary is bookkeeping, and the standard library supplies it. Decorating the function with [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) attaches an unbounded cache keyed by the call's arguments, consulted before the body runs and filled with whatever the body returns, so the recursion and both base cases stay exactly as the brute force wrote them:

1. Keep `dp(node, flights_left)` verbatim from the brute force: return `0` at
   `dst`, return `None` when the budget is spent, otherwise take the `min` of
   `price + dp(neighbor, flights_left - 1)` over every outgoing flight whose branch is possible.
2. Decorate it with `@cache`, so each distinct `(node, flights_left)` pair runs
   the body at most once and every later request for it is served from the cache.
3. Delete the three bookkeeping lines the decorator now owns: the `memo = {}`
   declaration, the `if (node, flights_left) in memo` lookup, and the `memo[...] = ...` store.

Because the cache lives on the inner function object, it is rebuilt on every call, so results never leak between different flight networks.

#### Walkthrough

Run it on the tailored input from the Top-Down Memoization walkthrough: `n = 5`, `flights = [[0,1,1],[0,2,2],[1,3,5],[2,3,1],[3,4,10]]`, `src = 0`, `dst = 4`, `k = 2`. The decorator's behavior is identical to the hand-rolled memo, so the trace reads the same:

```text
dp(0, 3)                      try 0 -> 1 (1)
  dp(1, 2)                    try 1 -> 3 (5)
    dp(3, 1)                  try 3 -> 4 (10)
      dp(4, 0)  -> 0          dst reached
    -> 10                     cached
  -> 15                       cached
  try 0 -> 2 (2)
  dp(2, 2)                    try 2 -> 3 (1)
    dp(3, 1)  -> 10           ** cache hit **
  -> 11                       cached
-> 13                         min(1 + 15, 2 + 11) = 13
```

Five calls reach the body, one per distinct pair, and the second arrival at airport `3` is answered from the cache without running it again. The return value is `13`, matching the Top-Down Memoization result for the same input.

#### Solution

The brute force recursion, unchanged, with one decorator standing in for the memo dictionary.

```python
from functools import cache
from typing import List, Optional


class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        adjacency = [[] for _ in range(n)]
        for u, v, price in flights:
            adjacency[u].append((v, price))

        # The cache lives on this inner function object, which is rebuilt on
        # every call, so results never carry over between flight networks.
        @cache
        def dp(node: int, flights_left: int) -> Optional[int]:
            if node == dst:
                return 0
            if flights_left == 0:
                return None
            best = None
            for neighbor, price in adjacency[node]:
                rest = dp(neighbor, flights_left - 1)
                if rest is not None and (best is None or price + rest < best):
                    best = price + rest
            return best

        best = dp(src, k + 1)
        return -1 if best is None else best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(k × e)`

The cache admits each distinct `(node, flights_left)` pair into the body exactly once, and that one admission loops over the airport's outgoing flights; every other call is a dictionary lookup on an integer-pair key, which is constant time, so the totals match the hand-rolled memo.

##### Space Complexity: `O(n × k + e)`

The cache holds one entry per computed pair and the recursion stack descends at most `k + 1` frames, matching the hand-rolled version, plus the adjacency lists.

#### Key Insights

- The decorator is a drop-in replacement only when the arguments are hashable
  and the function is genuinely pure; `dp` reads `node`, `flights_left`, and the enclosing `adjacency` and `dst`, which are fixed for the lifetime of the cache, so the substitution holds.
- The cache is keyed by the argument tuple `(node, flights_left)` directly, so
  unlike a hand-rolled memo there is no risk of a typo'd key serving a stale answer.
- The decorator does nothing about recursion depth: the chain still descends at
  most `k + 1` frames, small under `n <= 100`, so no recursion-limit guard is needed here.

## Comparison of Solutions

### Time Complexity

- **Brute Force Recursion**: `O(n^(k + 1))` - re-solves every `(airport, budget)` pair once per route that reaches it.
- **Top-Down Memoization**: `O(k × e)` - one body run per distinct pair, relaxing each state's outgoing flights.
- **Bellman-Ford Relaxation Sweeps**: `O(k × e)` - `k + 1` sweeps over the raw flight list.
- **Dijkstra's Algorithm with Stop Budgets**: `O(e × k × log(e × k))` - each state expanded at most once, with logarithmic heap costs.
- **Top-Down Memoization with functools.cache**: `O(k × e)` - identical totals, dictionary lookups instead of hand-rolled checks.

### Space Complexity

- **Brute Force Recursion**: `O(n + e)` - adjacency lists plus a recursion stack no deeper than the budget.
- **Top-Down Memoization**: `O(n × k + e)` - adjacency lists plus one memo entry per pair.
- **Bellman-Ford Relaxation Sweeps**: `O(n)` - two distance arrays, no adjacency structure.
- **Dijkstra's Algorithm with Stop Budgets**: `O(n + e × k)` - adjacency lists plus a heap that accumulates one entry per edge relaxation.
- **Top-Down Memoization with functools.cache**: `O(n × k + e)` - the decorator's cache in place of the hand-rolled dictionary.

### Trade-offs

- **Brute Force Recursion**: The route rule translated straight into code, but the exponential tree makes it usable only for tiny budgets.
- **Top-Down Memoization**: Keeps the brute force's shape while collapsing its repetition; the price is memo bookkeeping woven through the recursion.
- **Bellman-Ford Relaxation Sweeps**: The shortest correct code and the only one needing no adjacency structure, at the cost of pricing every airport when only `dst` is wanted.
- **Dijkstra's Algorithm with Stop Budgets**: Answers as soon as `dst` pops instead of waiting out the sweeps, but carries the three-coordinate state, the dominance filter, and heap machinery.
- **Top-Down Memoization with functools.cache**: Deletes the memo bookkeeping entirely; the recursion-limit risk the decorator cannot remove is absent here because the budget bounds the depth by `n <= 100`.

### When to Use Each

- **Brute Force Recursion**: As a first translation of the rules and a correctness reference when testing the faster methods.
- **Top-Down Memoization**: When deriving the state `(airport, budget)` from the brute force and wanting to see exactly what memoization adds.
- **Bellman-Ford Relaxation Sweeps** (recommended): The recurrence reads directly off the stop rule, the freeze-per-sweep detail is the one subtle line, and the whole solution is a handful of loop lines.
- **Dijkstra's Algorithm with Stop Budgets**: When early exit matters or when extending to larger graphs where pricing only what the frontier needs beats full sweeps.
- **Top-Down Memoization with functools.cache**: The Pythonic version of the memoized recursion, once the hand-rolled mechanism has been seen once.

### Optimization Notes

- Budget and flights differ by one everywhere: a route with at most `k` stops
  uses at most `k + 1` flights. Writing the budget as `k + 1` flights once, at the entry call, keeps every later inequality a plain flight count.
- The frozen previous layer is the difference between Bellman-Ford and its
  broken in-place variant here; the classic single-source version tolerates in-place sweeps, the budgeted one does not.
- The state count `n × (k + 1)` bounds every efficient solution; any approach
  that fails to notice the budget (plain Dijkstra on `(price, node)`) answers a different problem and returns too-cheap, too-many-stop routes.
- A plain visited set is wrong in every solution family: the same airport may
  need revisiting under different budgets, and only a dominance rule (`fewest_edges`) can discard states safely.

