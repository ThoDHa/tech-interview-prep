# [Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary/)

**Hard** | **40 minutes** | **Depth-First Search, Graph Theory, Eulerian Circuit**

**Pattern:** [Graph Traversal](../patterns/graph/intuition.md), [Backtracking](../patterns/backtracking_exploration/intuition.md)

**Algorithm:** [Eulerian path](https://en.wikipedia.org/wiki/Eulerian_path) · [Hierholzer's algorithm](https://en.wikipedia.org/wiki/Eulerian_path#Hierholzer%27s_algorithm) · [Backtracking](https://en.wikipedia.org/wiki/Backtracking)

**Practice:** [`practice/reconstruct_itinerary/solution.py`](../../practice/reconstruct_itinerary/solution.py)

You are given a list of flight tickets `tickets` where `tickets[i] = [from_i, to_i]` represent the source airport and the destination airport. 

Each `from_i` and `to_i` consists of three uppercase English letters.

Reconstruct the itinerary in order and return it.

All of the tickets belong to someone who originally departed from `"JFK"`. Your objective is to reconstruct the flight path that this person took, assuming each ticket was used exactly once.

If there are multiple valid flight paths, return the lexicographically smallest one.
* For example, the itinerary `["JFK", "SEA"]` has a smaller lexical order than `["JFK", "SFO"]`.

You may assume all the tickets form at least one valid flight path.

## Examples

### Example 1

**Input:** `tickets = [["BUF","HOU"],["HOU","SEA"],["JFK","BUF"]]`

**Output:** `["JFK","BUF","HOU","SEA"]`

### Example 2

**Input:** `tickets = [["HOU","JFK"],["SEA","JFK"],["JFK","SEA"],["JFK","HOU"]]`

**Output:** `["JFK","HOU","JFK","SEA","JFK"]`

**Explanation:** Another possible reconstruction is `["JFK","SEA","JFK","HOU","JFK"]` but it is lexicographically larger.

## Constraints

- `1 <= tickets.length <= 300`
- `from_i != to_i`

## Deriving the Solution

Using every ticket exactly once is an [Eulerian path](https://en.wikipedia.org/wiki/Eulerian_path): the tickets are edges, the airports are nodes, and the itinerary walks each edge precisely once. The lexicographic tie-break is the complication: among all Eulerian paths from `"JFK"`, the smallest one wins, so a naive greedy walk that always boards the smallest destination can strand tickets behind a dead end. Every solution below builds the adjacency structure first and then finds the path; they differ in how they repair a wrong greedy choice.

1. **Start literal.** Try the tickets in every order: keep the paths that start
   at `"JFK"` and use each ticket legally, and take the lexicographically smallest survivor. Correct but factorial: see [Brute Force Permutation Search](#brute-force-permutation-search).
2. **Spot the structure.** The greedy smallest-destination walk only fails when
   it enters a node whose remaining tickets are all outgoing-none: a dead end reached too early. Letting the walk backtrack and re-choose repairs that, at exponential worst-case cost: see [Backtracking DFS](#backtracking-dfs).
3. **Reverse the failure into the answer.** Hierholzer's Algorithm never
   backtracks: it walks greedily until stuck, records stuck nodes on a stack, and reads the stack backwards. The dead ends pop first and land at the end of the itinerary, which is exactly where a node with no remaining outgoing tickets belongs: see [Hierholzer's Algorithm](#hierholzers-algorithm).

## Solutions

### Brute Force Permutation Search

#### Derivation

The most literal reading of "use each ticket exactly once" enumerates the ways to spend them. Every ordering of the ticket list is a candidate itinerary builder: walk the ordering, extending the route whenever the next ticket departs from the current airport, and keep the full routes. Comparing the survivors lexicographically and keeping the smallest implements the tie-break directly:

1. Build all permutations of `tickets`.
2. For each permutation, grow `route` from `["JFK"]`, appending each ticket's
   destination when its source equals the route's last airport; abandon the
   permutation at the first mismatch.
3. Track `best`, the lexicographically smallest complete route.
4. Return `best`.

#### Walkthrough

Example 1 is small enough to enumerate: `tickets = [["BUF","HOU"],["HOU","SEA"],["JFK","BUF"]]`. Exactly one of the six permutations survives the walk:

```text
JFK->BUF, BUF->HOU, HOU->SEA   route ["JFK","BUF","HOU","SEA"]   complete
...   the other five abandon (no ticket leaves JFK except [JFK,BUF], so any
      ordering not starting with it dies on the first ticket; the one that
      starts [JFK,BUF] but defers [BUF,HOU] dies when HOU->SEA is offered
      while the route still sits in BUF)
```

The only complete route is `["JFK","BUF","HOU","SEA"]`, which is therefore also the lexicographically smallest and matches the expected Output for Example 1.

#### Solution

The code is the permutation walk with the running best.

```python
from itertools import permutations
from typing import List


class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        best = None
        for order in permutations(tickets):
            route = ["JFK"]
            for src, dst in order:
                if route[-1] != src:
                    break
                route.append(dst)
            if len(route) == len(tickets) + 1 and (
                best is None or route < best
            ):
                best = route
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(e! * e)`

All `e!` ticket orderings are built and walked at `O(e)` each.

##### Space Complexity: `O(e)`

The current route and the best route dominate; `permutations` yields lazily.

#### Key Insights

- The tie-break is trivial here: comparing complete routes directly is the definition of "lexicographically smallest".
- Nothing about the graph is exploited, which is why the cost explodes: `(300)!` orderings at the constraint ceiling.
- The structure this solution exposes, that the first ticket must depart `"JFK"` and each later one departs where the last landed, is the constraint the faster methods thread implicitly.

### Backtracking DFS

#### Derivation

The permutation sweep re-derives obvious prefixes billions of times. Backtracking keeps one route and one ticket multiset, extends it greedily toward the smallest destination, and undoes a choice the moment it leads to an incompletable route. The pruning is the whole point: a choice is only wrong when the remaining tickets can no longer all be spent, and the deepest failure (a node with no remaining outgoing tickets while tickets remain) reveals that:

1. Build `adjacency` mapping each source to a sorted list of destinations.
2. Walk recursively from `"JFK"`: for the smallest untried destination, mark
   the ticket used, append the destination to `route`, and recurse.
3. On failure, un-mark the ticket and drop the destination from `route`,
   trying the next-smallest destination.
4. A route of length `len(tickets) + 1` is complete: return it. Because
   destinations are tried smallest-first, the first complete route is the lexicographically smallest.

#### Walkthrough

Let us backtrack by hand on Example 2: `tickets = [["HOU","JFK"],["SEA","JFK"],["JFK","SEA"],["JFK","HOU"]]`, with sorted destinations `JFK: [HOU, SEA]`, `HOU: [JFK]`, `SEA: [JFK]`. The smallest-first walk starts with `HOU`:

```text
route = [JFK]
  try JFK->HOU   route = [JFK, HOU]
    try HOU->JFK  route = [JFK, HOU, JFK]
      try JFK->SEA  route = [JFK, HOU, JFK, SEA]
        try SEA->JFK  route = [JFK, HOU, JFK, SEA, JFK]  complete
```

The first greedy dive happens to complete here: with route `[JFK, HOU, JFK, SEA, JFK]` every one of the four tickets is spent, so the walk returns it without ever backtracking, and being built smallest-first it is the lexicographically smallest, matching the expected Output for Example 2. The pruning earns its keep when a small first choice is a trap: on `[["JFK","KUL"],["JFK","NRT"],["NRT","JFK"]]` the walk into `KUL` strands the `NRT` tickets (node `KUL` has no outgoing ticket), so the walk undoes `KUL`, boards `NRT` instead, and completes `["JFK","NRT","JFK","KUL"]`.

#### Solution

The code is the sorted-destination dive with undo on failure.

```python
from typing import List


class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        adjacency = {}
        for src, dst in tickets:
            adjacency.setdefault(src, []).append(dst)
        for destinations in adjacency.values():
            destinations.sort()

        route = ["JFK"]
        used = [False] * len(tickets)
        ticket_count = len(tickets)

        def backtrack(airport: str) -> bool:
            if len(route) == ticket_count + 1:
                return True
            for dst in adjacency.get(airport, []):
                for index, (src, ticket_dst) in enumerate(tickets):
                    if src == airport and ticket_dst == dst and not used[index]:
                        used[index] = True
                        route.append(dst)
                        if backtrack(dst):
                            return True
                        route.pop()
                        used[index] = False
                        break
            return False

        backtrack("JFK")
        return route
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(e^e)` worst case

The search tree branches over untried destinations per node; the pruning cuts most branches on realistic inputs, but the exponential worst case stands on adversarial dead-end layouts.

##### Space Complexity: `O(e)`

The adjacency map, the route, the used flags, and the recursion stack of depth `e`.

#### Key Insights

- Sorting destinations once makes "try smallest first" free at search time, so the first completed route is the answer without any comparison of alternatives.
- The `used` flags, not destination removal, make duplicate tickets work: two identical tickets are two independent booleans.
- Backtracking is correct but unpredictable; its cost depends on how early dead ends reveal themselves, which is exactly what Hierholzer's stack removes.

### Hierholzer's Algorithm

#### Derivation

The backtracking walk fails only when it enters a node that still has no outgoing untried ticket while tickets remain elsewhere; the correct route must visit such a node last along its detour. [Hierholzer's Algorithm](https://en.wikipedia.org/wiki/Eulerian_path#Hierholzer's_algorithm) turns that failure mode into the construction: walk greedily to the smallest destination, consuming tickets; when stuck, pop the stuck airport onto a `route` stack. Popped nodes are exactly the nodes with nothing left to leave, so the pop order is the itinerary read backwards. No choice is ever undone: a dead end is not a mistake but the next entry from the end:

1. Build `adjacency` mapping each source to a min-heap of destinations, so the
   smallest untried destination pops first.
2. Seed a `stack` with `"JFK"`.
3. While the stack is non-empty: while the top airport still has untried
   tickets, pop its smallest destination and push it on the stack.
4. When the top has none, pop it into `route`.
5. Reverse `route` and return it.

#### Walkthrough

Let us run the stack on Example 2: `tickets = [["HOU","JFK"],["SEA","JFK"],["JFK","SEA"],["JFK","HOU"]]`, adjacency `JFK: [HOU, SEA]`, `HOU: [JFK]`, `SEA: [JFK]`. The greedy dive consumes all four tickets before anyone gets stuck, and the pops unwind the whole route in reverse:

```text
go JFK->HOU  stack = [JFK, HOU]
go HOU->JFK  stack = [JFK, HOU, JFK]
go JFK->SEA  stack = [JFK, HOU, JFK, SEA]
go SEA->JFK  stack = [JFK, HOU, JFK, SEA, JFK]
stuck: pop JFK  route = [JFK]
stuck: pop SEA  route = [JFK, SEA]
stuck: pop JFK  route = [JFK, SEA, JFK]
stuck: pop HOU  route = [JFK, SEA, JFK, HOU]
stuck: pop JFK  route = [JFK, SEA, JFK, HOU, JFK]
reverse -> ["JFK","HOU","JFK","SEA","JFK"]
```

The reversed stack is `["JFK","HOU","JFK","SEA","JFK"]`, matching the expected Output for Example 2. The dead-end case is where the mechanism shows: on `[["JFK","KKK"],["KKK","JFK"],["JFK","MMM"]]` the walk goes `JFK -> KKK -> JFK -> MMM` and pops `MMM` first, parking the airport with no outgoing tickets at the end, then unwinds `JFK`, `KKK`, `JFK` to produce `["JFK","KKK","JFK","MMM"]`.

#### Solution

The code is the greedy dive and the unwind, with the heap keeping destinations sorted.

```python
import heapq
from typing import List


class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        adjacency = {}
        for src, dst in tickets:
            heapq.heappush(adjacency.setdefault(src, []), dst)

        route = []
        stack = ["JFK"]
        while stack:
            while adjacency.get(stack[-1]):
                stack.append(heapq.heappop(adjacency[stack[-1]]))
            route.append(stack.pop())
        route.reverse()
        return route
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(e log e)`

Building the heaps costs one push per ticket, and the walk pops each ticket exactly once from a heap and each airport exactly once from the stack; the logarithmic factor is the heap operations.

##### Space Complexity: `O(e)`

The adjacency heaps, the walk stack, and the route are all bounded by the ticket count.

#### Key Insights

- The reversed pop order is the theorem: nodes pop when they have no untried outgoing tickets, and a node in that state belongs later in the itinerary than anything still on the stack.
- Greedy never needs forgiveness here: taking the smallest destination first is safe because a premature dead end is repaired by placement (it pops early, landing at the end), not by re-choice.
- Consuming tickets by popping the heap is what makes duplicate tickets and the no-reuse rule both automatic.

## Comparison of Solutions

### Time Complexity

- **Brute Force Permutation Search**: `O(e! * e)` - every ticket ordering walked in full.
- **Backtracking DFS**: `O(e^e)` worst case - pruned smallest-first search over destination choices.
- **Hierholzer's Algorithm**: `O(e log e)` - one heapified pass consuming each ticket once.

### Space Complexity

- **Brute Force Permutation Search**: `O(e)` - current and best routes over a lazy permutation stream.
- **Backtracking DFS**: `O(e)` - adjacency, route, used flags, and recursion stack.
- **Hierholzer's Algorithm**: `O(e)` - adjacency heaps, walk stack, and route.

### Trade-offs

- The brute force is correctness made literal: no graph theory, no invariants, unusable past a dozen tickets.
- Backtracking reads naturally and prunes hard on friendly inputs, but its worst case is exponential and input-dependent.
- Hierholzer needs the Eulerian-path insight to trust, and in exchange is linear up to sorting: no search, no undo, no exponential anything.

### When to Use Each

- **Brute Force Permutation Search**: as the executable specification that validates the fast methods on tiny inputs.
- **Backtracking DFS**: when the use-each-edge-once rule is a soft constraint (for example, longest route variants) and no Eulerian guarantee exists.
- **Hierholzer's Algorithm**: the answer whenever the problem says "use every edge exactly once", this problem included (recommended here).

### Optimization Notes

- The min-heap adjacency merges two duties: keeping destinations sorted for the tie-break and consuming tickets so duplicates stay distinguishable.
- The problem guarantees an Eulerian path from `"JFK"`, which is why no validity check appears: the walk provably consumes every ticket.
- Iterative beats recursive here deliberately: the explicit stack survives deep route chains that would pressure Python's recursion limit at `tickets.length = 300`.

