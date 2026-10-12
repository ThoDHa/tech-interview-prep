# [Cheapest Flights Within K Stops](https://www.fastprep.io/problems/amazon-cheapest-flights-within-k-stops)

**Medium** | **NN minutes** | **Graph, Breadth First Search, Shortest Path, Heap**

There are n cities numbered from 0 to n - 1. You are given an array flights where flights[i] = [from_i, to_i, price_i] means there is a directed flight from city from_i to city to_i with cost price_i.

You are also given integers src, dst, and k. Return the cheapest price from src to dst with at most k stops. If no such route exists, return -1.

## Examples

### Example 1

**Input:** `n = 4`, `flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]`, `src = 0`, `dst = 3`, `k = 1`

**Output:** `700`

**Explanation:** The route 0 -> 1 -> 3 costs 700 and uses 1 stop. The cheaper route 0 -> 1 -> 2 -> 3 costs 400 but uses 2 stops, which exceeds k.

### Example 2

**Input:** `n = 3`, `flights = [[0,1,100],[1,2,100],[0,2,500]]`, `src = 0`, `dst = 2`, `k = 1`

**Output:** `200`

**Explanation:** The route 0 -> 1 -> 2 costs 200 with 1 stop, which is cheaper than the direct flight of 500.

## Constraints

- `1 <= n <= 100.`
- `0 <= flights.length <= n * (n - 1).`
- `flights[i].length == 3.`
- `0 <= from_i, to_i < n.`
- `from_i != to_i.`
- `1 <= price_i <= 10^4.`
- `There are no duplicate flights and no self-flights.`
- `0 <= src, dst, k < n.`
- `src != dst.`

## Solutions

### Brute Force Recursion

#### Derivation

The most literal reading enumerates routes: fly any flight out of the current
city, then any flight out of the next, and stop when either `dst` is reached or
flying further would exceed the budget. Every price is at least `1` (the
constraints say `1 <= price_i`), so an optimal route never revisits a city, and
plain recursion over the flight budget explores exactly the meaningful routes.
The stop limit becomes a simple counter of remaining flights, because a route
with at most `k` stops uses at most `k + 1` flights:

1. Build the adjacency list `adjacency` from `flights`, mapping each city to
   its `(neighbor, price)` pairs.
2. Define `dfs(node, flights_left)`: the cheapest cost of completing the route
   to `dst` from `node` when `flights_left` flights may still be taken.
3. Base cases: at `dst` the remaining route costs `0`; with
   `flights_left == 0` no flight may be taken, so an unfinished route is
   impossible (`None`).
4. Otherwise take the `min` of `price + dfs(neighbor, flights_left - 1)` over
   every `(neighbor, price)` outgoing flight whose branch is possible.
5. Run `dfs(src, k + 1)` (a route with `k` stops uses at most `k + 1` flights)
   and map `None` to `-1`.

#### Walkthrough

Example 1: `n = 4`, `flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]`,
`src = 0`, `dst = 3`, `k = 1`, so the budget is `2` flights. The adjacency
lists are `adjacency[0] = [(1, 100)]`, `adjacency[1] = [(2, 100), (3, 600)]`,
`adjacency[2] = [(0, 100), (3, 200)]`, `adjacency[3] = []`, and the trace
indents one level per call:

```text
dfs(0, 2)   try 0 -> 1 (100)
  dfs(1, 1)   try 1 -> 2 (100)
    dfs(2, 0)   not dst, budget spent -> None
  try 1 -> 3 (600)
    dfs(3, 0)   dst reached -> 0
  -> 600            best = 600 + 0
-> 700              best = 100 + 600
```

The branch through city `2` dies at `dfs(2, 0)`: reaching `dst` from there
would need a third flight, and none is affordable, so the return flight
`2 -> 0` (the cycle in the input) is never even tried. The surviving branch
lands on `dst` with the direct hop `1 -> 3`, so the cheapest total is
`100 + 600 = 700`, matching the expected Output for Example 1. The cheaper
route `0 -> 1 -> 2 -> 3` costs `400` but needs `3` flights, one beyond the
budget, and the recursion never extends that branch far enough to price it. On
Example 2 the same enumeration flies `0 -> 1 -> 2` at `100 + 100 = 200` within
the budget of `2` flights and returns `200`.

#### Solution

The code is the route enumeration written down: a base case at `dst`, a budget
guard, and a `min` over outgoing flights.

```python
from typing import List, Optional


class Solution:
    def solve(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        adjacency = [[] for _ in range(n)]
        for departure, arrival, price in flights:
            adjacency[departure].append((arrival, price))

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

The recursion tree branches over the outgoing flights of the current city and
descends `k + 1` levels. Each level branches at most `n - 1` ways on a dense
graph, so the tree reaches `O(n^(k + 1))` leaves, and each level does constant
work per call on top of them.

##### Space Complexity: `O(n + e)`

The adjacency lists store all `e` flights, and the recursion stack descends at
most `k + 1 <= n` frames, which the `O(n)` term covers.

#### Key Insights

- Converting stops to a flight budget (`k + 1` flights) turns the stop rule
  into a single counter, which every later solution reuses.
- Positive prices mean an optimal route never revisits a city, so the recursion
  is finite even though Example 1 contains the cycle `2 -> 0`; the budget
  starves the cycle before it can loop, and no `visited` set is needed.
- The exponential cost is pure repetition: the same `(city, remaining budget)`
  pair is re-solved across countless interleavings of the same flights.

### Top-Down Memoization

#### Derivation

The brute force re-solves subproblems because a route's remaining cost depends
only on where it stands and how many flights it may still take, not on the
route that produced it. When two different prefixes land on the same city with
the same remaining budget, everything below them is computed twice. A memo
table keyed by that pair collapses the repetition while leaving the recursion
itself untouched:

1. Keep `dp(node, flights_left)` exactly as the brute force's `dfs`: return `0`
   at `dst`, `None` with an empty budget, otherwise the `min` of
   `price + dp(neighbor, flights_left - 1)` over the outgoing flights.
2. Declare `memo` and, before computing, return `memo[(node, flights_left)]`
   when the pair is already stored; store each freshly computed result there.
3. Run `dp(src, k + 1)` and map `None` to `-1`.

There are at most `n × (k + 1)` distinct pairs, so the exponential tree
collapses to that many computed cells.

#### Walkthrough

Example 1 succeeds along its single branch without ever revisiting a pair, so
no cache hit occurs there. A tailored input (not an official example) shows
one: `n = 5`, `flights = [[0,1,1],[0,2,2],[1,3,5],[2,3,1],[3,4,10]]`, `src = 0`,
`dst = 4`, `k = 2`, so the budget is `3` flights. Both routes to city `3` leave
the same remaining budget, so the second arrival is served from `memo`:

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

Five calls run the body, one per distinct pair: the entry call at city `0`, the
base case at city `4`, and the three stored results. The second route to city
`3` reused `memo[(3, 1)]` instead of re-flying the tail to `dst`. The answer is
`min(1 + 15, 2 + 11) = 13`, the route `0 -> 2 -> 3 -> 4`. (Example 2 still
returns `200`: the memo only removes recomputation, it never changes an
answer.)

#### Solution

The code is the brute force recursion plus a two-line memo: look up before
computing, store after.

```python
from typing import List, Optional


class Solution:
    def solve(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        adjacency = [[] for _ in range(n)]
        for departure, arrival, price in flights:
            adjacency[departure].append((arrival, price))

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

Each of the at most `n × (k + 1)` distinct `(node, flights_left)` pairs runs
its body once, and one body execution relaxes the city's out-degree of edges.
Summed over all pairs the edge relaxations total `O(k × e)`, matching the
sweeps of the next solution without their ordering.

##### Space Complexity: `O(n × k + e)`

The adjacency lists hold all `e` flights, the memo holds one entry per computed
pair, and the recursion stack descends at most `k + 1` frames.

#### Key Insights

- The state `(node, flights_left)` is the whole problem in miniature: the
  cheapest completion from a city with a given budget. Every later solution
  manipulates this same state space with a different execution order.
- The memo never changes an answer, only the number of times it is computed;
  the recursion reads exactly as the brute force with three added lines.
- The pair count `n × (k + 1)` is the bridge from exponential to polynomial:
  the tree is huge, but its distinct nodes are few.

### Bellman-Ford Relaxation Sweeps

#### Derivation

The memoized recursion fills the state space lazily, in whatever order the
calls reach it. Reading the same states as a table admits a chosen order
instead: layer by layer, each sweep extending every city's answer by exactly
one flight, so the layer index is a flight count and sweeping the table is what
enforces the stop budget. A sweep needs nothing but the previous layer: the
recurrence below states the rule, and the solution collapses the table to two
arrays.

#### Recurrence

Let `dp[t][v]` be the cheapest price of any route from `src` to `v` using at
most `t` flights:

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

The previous layer `dp[t - 1]` is read, never written, so every route counted
in layer `t` uses at most one more flight than in layer `t - 1`: the sweep
count is the budget. The answer is read at `dst` after `k + 1` sweeps, with
`-1` wherever the impossible marker survives.

#### Walkthrough

Let us sweep by hand on Example 1: `n = 4`,
`flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]`, `src = 0`,
`dst = 3`, `k = 1`, so two sweeps with `None` playing the impossible marker.
The flights relax in the order the input lists them:

```text
sweep 1   previous = [0, None, None, None]
  0->1: 0 + 100        distances[1] = 100
  1->2: previous[1] impossible -> skip
  2->0: previous[2] impossible -> skip
  1->3: previous[1] impossible -> skip
  2->3: previous[2] impossible -> skip
after sweep 1: [0, 100, None, None]

sweep 2   previous = [0, 100, None, None]
  0->1: 0 + 100 = 100, no improvement
  1->2: 100 + 100      distances[2] = 200
  2->0: previous[2] impossible -> skip
  1->3: 100 + 600      distances[3] = 700
  2->3: previous[2] impossible -> skip
after sweep 2: [0, 100, 200, 700]
```

The final rejection is the whole algorithm: the tempting `400` route
`0 -> 1 -> 2 -> 3` would relax `2 -> 3` from the value `200`, but that value
was written by sweep 2 itself, and the sweep reads the frozen `previous`, where
city `2` is still impossible. The route cannot leak into the two-sweep budget,
and `dp[2][3] = 700` matches the expected Output for Example 1. Letting
`k = 2` on the same input adds a third sweep that relaxes `2 -> 3` from
`200 + 200 = 400` and returns `400`. On Example 2 the sweeps price city `2` at
`200` in sweep 2 (via `0 -> 1 -> 2`) and return `200`.

#### Solution

The code is the recurrence with the previous layer frozen per sweep: sweep
`k + 1` times, then read `dst`.

```python
from typing import List, Optional


class Solution:
    def solve(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        distances: List[Optional[int]] = [None] * n
        distances[src] = 0

        for _ in range(k + 1):
            previous = distances[:]
            for departure, arrival, price in flights:
                if previous[departure] is not None and (
                    distances[arrival] is None
                    or previous[departure] + price < distances[arrival]
                ):
                    distances[arrival] = previous[departure] + price

        return -1 if distances[dst] is None else distances[dst]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(k × e)`

Each of the `k + 1` sweeps reads every flight once and does constant work per
flight, with no adjacency structure to build or sort.

##### Space Complexity: `O(n)`

Two distance arrays of `n` entries; the flight list is swept directly from the
input.

#### Key Insights

- Limiting Bellman-Ford to `k + 1` sweeps is the stop budget: with at most `t`
  sweeps, every recorded distance uses at most `t` flights, so the count itself
  is the constraint.
- The frozen `previous = distances[:]` per sweep is what makes each sweep count
  as exactly one flight; relaxing in place would let a route gain many flights
  within one sweep and return the under-budgeted `400` on Example 1.
- `None` as the impossible marker keeps a genuine `0`-cost state (`src`) from
  being confused with "no route yet", which matters because a route can only be
  extended from cities that are actually reachable.
- No adjacency list is ever built, making this the natural fit when the flight
  list is small or streamed.

### Dijkstra's Algorithm with Stop Budgets

#### Derivation

The sweeps price every city, though only `dst` is wanted, and they reprice a
city as many times as its in-degree even when the improvement is worthless
under the budget. [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
orders the work by price: with all prices positive, the cheapest unsettled
state in the frontier can never be beaten by a detour through another
unsettled state, so its first pop is final. The state grows a third coordinate,
the number of flights taken, because a cheaper price with more flights used and
a dearer price with fewer are genuinely different futures under the budget. A
second array, `fewest_edges`, keeps the frontier from drowning in
budget-discarded states:

1. Build the adjacency lists.
2. Initialize `fewest_edges` to `k + 2` for every city, one past the budget,
   and push `(0, src, 0)` into a min-heap. The source's `0` flights sit below
   the marker, so the first pop expands it without a special case.
3. Pop the smallest `(price, node, edges_used)`. At `dst`, `price` is the
   answer: the heap orders by price, so no later state can be cheaper.
4. Skip the state when `edges_used == k + 1` (budget spent) or
   `edges_used >= fewest_edges[node]` (a cheaper-price state with at most as
   many flights already expanded the city).
5. Otherwise record `fewest_edges[node] = edges_used` and push
   `(price + cost, neighbor, edges_used + 1)` for each outgoing flight.
6. When the heap empties without popping `dst`, return `-1`.

#### Walkthrough

Let us run the heap on Example 1: `n = 4`,
`flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]`, `src = 0`,
`dst = 3`, `k = 1`, so the flight budget is `2` and `fewest_edges` starts as
`[3, 3, 3, 3]`:

```text
push (0, 0, 0)
pop (0, 0, 0)    expand 0->1            push (100, 1, 1)
pop (100, 1, 1)  expand 1->2, 1->3      push (200, 2, 2), (700, 3, 2)
pop (200, 2, 2)  edges_used == 2 = budget spent: skip
pop (700, 3, 2)  dst reached -> return 700
```

The heap's price order settles the question before the budget does:
`(200, 2, 2)` is skipped for having spent the whole budget in a city that is
not even the destination (its outgoing `2 -> 0` and `2 -> 3` would both need a
third flight), and `(700, 3, 2)` pops next because no cheaper state to `dst`
exists anywhere in the frontier. The function returns `700`, matching the
expected Output for Example 1, and never touches the forbidden `400` route,
whose states were pruned before they could win. On Example 2 the first
expansion pushes `(100, 1, 1)` and the direct `(500, 2, 1)`; expanding
`(100, 1, 1)` pushes `(200, 2, 2)`, which pops next and returns `200` without
the dearer direct state ever being expanded.

#### Solution

The code is the priced frontier: pop cheapest, stop at `dst`, prune by budget
and by the `fewest_edges` record.

```python
import heapq
from typing import List


class Solution:
    def solve(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        adjacency = [[] for _ in range(n)]
        for departure, arrival, price in flights:
            adjacency[departure].append((arrival, price))

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

Each of the `n × (k + 1)` states can be expanded at most once (guarded by
`fewest_edges`), expanding a state pushes one entry per outgoing flight, so the
heap holds `O(e × k)` entries across the run and costs logarithmic work per
push or pop.

##### Space Complexity: `O(n + e × k)`

The adjacency lists hold all `e` flights, `fewest_edges` is `O(n)`, and the
heap accumulates at most one pushed entry per edge relaxation, `O(e × k)`.

#### Key Insights

- Shortest paths here are cheapest first, not fewest flights first: the heap
  must order by price, and the budget rides along as a third state coordinate.
- Settling by price needs positive prices, which the constraints guarantee
  (`1 <= price_i`); with free flights the first pop to a state could lose to a
  pricier one that later flies cheaper, and the Bellman-Ford sweeps above
  become the honest tool.
- `fewest_edges` is a dominance filter, not a visited set: it discards a state
  only when an equal-price-or-cheaper state with at most as many flights
  already expanded the city, which keeps the heap from flooding with
  budget-discarded states.
- Pricier-but-shorter states are kept deliberately: dropping them would let the
  budget prune the only routes that survive it, which is exactly the failure
  mode of plain Dijkstra on this problem.

### Top-Down Memoization with functools.cache

#### Derivation

The [Top-Down Memoization](#top-down-memoization) solution is the brute force
recursion plus a dictionary that keeps it from re-solving a
`(city, budget)` pair it has already answered. The recursion is the algorithm;
the dictionary is bookkeeping, and the standard library supplies it. Decorating
the function with [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache)
attaches an unbounded cache keyed by the call's arguments, consulted before the
body runs and filled with whatever the body returns, so the recursion and both
base cases stay exactly as the brute force wrote them:

1. Keep `dp(node, flights_left)` verbatim from the brute force: return `0` at
   `dst`, return `None` when the budget is spent, otherwise take the `min` of
   `price + dp(neighbor, flights_left - 1)` over every outgoing flight whose
   branch is possible.
2. Decorate it with `@cache`, so each distinct `(node, flights_left)` pair runs
   the body at most once and every later request for it is served from the
   cache.
3. Delete the three bookkeeping lines the decorator now owns: the `memo = {}`
   declaration, the `if (node, flights_left) in memo` lookup, and the
   `memo[...] = ...` store.

Because the cache lives on the inner function object, it is rebuilt on every
call, so results never leak between different flight networks.

#### Walkthrough

Run it on the tailored input from the Top-Down Memoization walkthrough:
`n = 5`, `flights = [[0,1,1],[0,2,2],[1,3,5],[2,3,1],[3,4,10]]`, `src = 0`,
`dst = 4`, `k = 2`. The decorator's behavior is identical to the hand-rolled
memo, so the trace reads the same:

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

Five calls reach the body, one per distinct pair, and the second arrival at
city `3` is answered from the cache without running it again. The return value
is `13`, matching the Top-Down Memoization result for the same input.

#### Solution

The brute force recursion, unchanged, with one decorator standing in for the
memo dictionary.

```python
from functools import cache
from typing import List, Optional


class Solution:
    def solve(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        adjacency = [[] for _ in range(n)]
        for departure, arrival, price in flights:
            adjacency[departure].append((arrival, price))

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

The cache admits each distinct `(node, flights_left)` pair into the body
exactly once, and that one admission loops over the city's outgoing flights;
every other call is a dictionary lookup on an integer-pair key, which is
constant time, so the totals match the hand-rolled memo.

##### Space Complexity: `O(n × k + e)`

The cache holds one entry per computed pair and the recursion stack descends at
most `k + 1` frames, matching the hand-rolled version, plus the adjacency
lists.

#### Key Insights

- The decorator is a drop-in replacement only when the arguments are hashable
  and the function is genuinely pure; `dp` reads `node`, `flights_left`, and
  the enclosing `adjacency` and `dst`, which are fixed for the lifetime of the
  cache, so the substitution holds.
- The cache is keyed by the argument tuple `(node, flights_left)` directly, so
  unlike a hand-rolled memo there is no risk of a typo'd key serving a stale
  answer.
- The decorator does nothing about recursion depth: the chain still descends at
  most `k + 1` frames, small under `n <= 100`, so no recursion-limit guard is
  needed here.

## Comparison of Solutions

### Time Complexity

- **Brute Force Recursion**: `O(n^(k + 1))` - re-solves every
  `(city, budget)` pair once per route that reaches it.
- **Top-Down Memoization**: `O(k × e)` - one body run per distinct pair,
  relaxing each state's outgoing flights.
- **Bellman-Ford Relaxation Sweeps**: `O(k × e)` - `k + 1` sweeps over the raw
  flight list.
- **Dijkstra's Algorithm with Stop Budgets**: `O(e × k × log(e × k))` - each
  state expanded at most once, with logarithmic heap costs.
- **Top-Down Memoization with functools.cache**: `O(k × e)` - identical
  totals, dictionary lookups instead of hand-rolled checks.

### Space Complexity

- **Brute Force Recursion**: `O(n + e)` - adjacency lists plus a recursion
  stack no deeper than the budget.
- **Top-Down Memoization**: `O(n × k + e)` - adjacency lists plus one memo
  entry per pair.
- **Bellman-Ford Relaxation Sweeps**: `O(n)` - two distance arrays, no
  adjacency structure.
- **Dijkstra's Algorithm with Stop Budgets**: `O(n + e × k)` - adjacency lists
  plus a heap that accumulates one entry per edge relaxation.
- **Top-Down Memoization with functools.cache**: `O(n × k + e)` - the
  decorator's cache in place of the hand-rolled dictionary.

### Trade-offs

- **Brute Force Recursion**: the route rule translated straight into code, but
  the exponential tree makes it usable only for tiny budgets.
- **Top-Down Memoization**: keeps the brute force's shape while collapsing its
  repetition; the price is memo bookkeeping woven through the recursion.
- **Bellman-Ford Relaxation Sweeps**: the shortest correct code and the only
  one needing no adjacency structure, at the cost of pricing every city when
  only `dst` is wanted.
- **Dijkstra's Algorithm with Stop Budgets**: answers as soon as `dst` pops
  instead of waiting out the sweeps, but carries the three-coordinate state,
  the dominance filter, and heap machinery.
- **Top-Down Memoization with functools.cache**: deletes the memo bookkeeping
  entirely; the recursion-limit risk the decorator cannot remove is absent here
  because the budget bounds the depth by `n <= 100`.

### When to Use Each

- **Brute Force Recursion**: as a first translation of the rules and a
  correctness reference when testing the faster methods.
- **Top-Down Memoization**: when deriving the state `(city, budget)` from the
  brute force and wanting to see exactly what memoization adds.
- **Bellman-Ford Relaxation Sweeps** (Recommended): the interview default: the
  recurrence reads directly off the stop rule, the freeze-per-sweep detail is
  the one subtle line, and the whole solution is a handful of loop lines.
- **Dijkstra's Algorithm with Stop Budgets**: when early exit matters or when
  extending to larger graphs where pricing only what the frontier needs beats
  full sweeps.
- **Top-Down Memoization with functools.cache**: the Pythonic version of the
  memoized recursion, once the hand-rolled mechanism has been seen once.

### Optimization Notes

- Budget and flights differ by one everywhere: a route with at most `k` stops
  uses at most `k + 1` flights. Writing the budget as `k + 1` flights once, at
  the entry call, keeps every later inequality a plain flight count.
- The frozen previous layer is the difference between Bellman-Ford and its
  broken in-place variant here; the classic single-source version tolerates
  in-place sweeps, the budgeted one does not.
- The state count `n × (k + 1)` bounds every efficient solution; any approach
  that fails to notice the budget (plain Dijkstra on `(price, node)`) answers a
  different problem and returns too-cheap, too-many-stop routes.
- A plain visited set is wrong in every solution family: the same city may need
  revisiting under different budgets, and only a dominance rule
  (`fewest_edges`) can discard states safely.
