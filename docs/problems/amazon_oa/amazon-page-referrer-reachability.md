# [Page Referrer Reachability](https://www.fastprep.io/problems/amazon-page-referrer-reachability)

**Medium** | **NN minutes** | **Graph, Breadth First Search, Depth First Search, Hash Table**

You are given a list of web traffic records. Each record is represented as a two-element string array [url, referrer]:

url is the page that a visitor reached.referrer is the page the visitor came from. An empty string represents a direct arrival with no referrer.Every record whose referrer is non-empty creates a directed movement from referrer to url. The reverse movement is not implied.

You are also given query = [start, target]. Return true if target is reachable from start by following zero or more recorded movements. Therefore, return true when start and target are the same page. Otherwise, return false.

Direct-arrival records do not create additional movements.

## Examples

### Example 1

**Input:** `records = [["/catalog","/home"],["/item/7","/catalog"],["/cart","/item/7"]]`, `query = ["/home","/cart"]`

**Output:** `true`

**Explanation:** The records create the directed path /home to /catalog to /item/7 to /cart.

### Example 2

**Input:** `records = [["/pricing","/home"],["/signup","/pricing"]]`, `query = ["/pricing","/home"]`

**Output:** `false`

**Explanation:** The record creates a movement from /home to /pricing, but not the reverse movement requested by the query.

### Example 3

**Input:** `records = [["/landing",""],["/account","/landing"]]`, `query = ["/account","/account"]`

**Output:** `true`

**Explanation:** A page is reachable from itself without following an edge.

## Constraints

- `1 <= records.length <= 2 * 10^5.`
- `Every row in records contains exactly two strings in the order [url, referrer].`
- `Every url, start, and target is non-empty and has length at most 100.`
- `Every referrer is either an empty string or a page URL of length at most 100.`
- `query.length == 2.`
- `Page URLs are compared exactly and are case-sensitive.`
- `The records may contain repeated movements and directed cycles.`

## Solutions

### Adjacency List with Recursive DFS

#### Derivation

The question is a reachability query on a directed graph: is there a path of recorded movements from `start` to `target`? The statement hands over movements in record form, so the first duty is to turn `n` `[url, referrer]` pairs into something traversable, and the second is to search it. A scan-and-restart search would re-walk the same cycles forever (the records may contain cycles), so the search must remember which pages it has already expanded. [DFS](https://en.wikipedia.org/wiki/Depth-first_search) over an adjacency list with a visited set is the direct expression of that plan:

1. Build `movement_from`: a map from page to the list of pages it moves to,
   appending `url` under `referrer` for every record whose `referrer` is not
   the empty string. Direct-arrival records contribute no edge.
2. When `start == target`, return `True` immediately: zero movements suffice.
3. Define `dfs(page)` that marks `page` in `visited` and answers `True` when
   `page == target`; otherwise it recurses into each unvisited successor from
   `movement_from`.
4. Return `dfs(start)`.

#### Walkthrough

Example 1 (`records = [["/catalog","/home"],["/item/7","/catalog"],["/cart","/item/7"]]`, `query = ["/home","/cart"]`). The adjacency list maps `/home` to `["/catalog"]`, `/catalog` to `["/item/7"]`, `/item/7` to `["/cart"]`; the direct-arrival question never arises here because every record has a referrer:

```text
build movement_from:
  /home -> [/catalog]   (record ["/catalog", "/home"])
  /catalog -> [/item/7] (record ["/item/7", "/catalog"])
  /item/7 -> [/cart]    (record ["/cart", "/item/7"])

dfs("/home")    not target; visit; successors: /catalog (unvisited)
  dfs("/catalog")   not target; visit; successors: /item/7 (unvisited)
    dfs("/item/7")  not target; visit; successors: /cart (unvisited)
      dfs("/cart")  == target -> return True
```

The recursion unwinds with `True` at every level and the function returns `True`, matching Example 1's expected output. Example 2 asks the reverse query (`query = ["/pricing","/home"]`): the edges run `/home -> /pricing` and `/pricing -> /signup`, so `dfs("/pricing")` expands its single successor `/signup`, which has no outgoing movements and is not the target, and the recursion returns `False` at both levels without ever reaching `/home`.

#### Solution

The code is the walkthrough's build-then-search: edges into `movement_from`, then a recursive descent guarded by `visited`.

```python
from collections import defaultdict
from typing import DefaultDict, List, Set


class Solution:
    def solve(self, records: List[List[str]], query: List[str]) -> bool:
        movement_from: DefaultDict[str, List[str]] = defaultdict(list)
        for url, referrer in records:
            if referrer != "":
                movement_from[referrer].append(url)

        start, target = query
        visited: Set[str] = set()

        def dfs(page: str) -> bool:
            if page == target:
                return True
            visited.add(page)
            return any(
                dfs(next_page)
                for next_page in movement_from[page]
                if next_page not in visited
            )

        return dfs(start)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(v + e)`

Where `v` is the number of distinct pages and `e` the number of non-direct records: building scans the records once, and the search expands each page at most once over its outgoing edges.

##### Space Complexity: `O(v + e)`

The adjacency list plus the visited set plus a recursion stack that a long path can grow to `v` frames.

#### Key Insights

- The start-equals-target rule is the "zero or more movements" clause: reachability is reflexive, so it is settled before any search.
- The `visited` set is not an optimization but the termination proof: the constraints allow directed cycles, and without it `dfs` would loop forever.
- Recursion depth is this version's weakness: with up to `2 × 10^5` records a long chain can exceed Python's recursion limit, which the iterative versions remove.

### Adjacency List with Iterative DFS

#### Derivation

The recursive descent carries the whole to-do list on the interpreter's call stack, and the record bound (`2 × 10^5`) is far past Python's default recursion limit of 1,000. The fix changes nothing about the search: a call stack is just a [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) of pages waiting to be expanded, so an explicit list of the same pages reproduces the traversal without recursion. Marking pages visited at push time keeps the stack small; checking again at pop time keeps it correct even when duplicates slip in:

1. Build `movement_from` exactly as before.
2. Handle the zero-movement case first: when `start == target`, return `True`.
3. Seed `stack` with `start`; while it is non-empty, pop a page.
4. Return `True` when the popped page equals `target`; otherwise push each
   successor not yet in `visited`, marking each one visited as it is pushed.

#### Walkthrough

Example 1 again, now as stack events. Successors are pushed in adjacency order, so the last-pushed (and first-popped) successor follows the same `/home -> /catalog -> /item/7 -> /cart` path:

```text
stack = ["/home"]
pop /home     not target; push /catalog          stack = ["/catalog"]
pop /catalog  not target; push /item/7           stack = ["/item/7"]
pop /item/7   not target; push /cart             stack = ["/cart"]
pop /cart     == target -> return True
```

The traversal visits the same four pages in the same order as the recursive version here, because each page has one successor. Example 2 (`query = ["/pricing","/home"]`) shows the empty-stack exit: `/pricing` pushes its lone successor `/signup`, `/signup` pushes nothing, and the emptied stack means no path exists, so the function returns `False`, matching the expected output.

```text
stack = ["/pricing"]
pop /pricing   not target; push /signup      stack = ["/signup"]
pop /signup    not target; no successors     stack = []  -> return False
```

#### Solution

The code is the walkthrough's pop-inspect-push loop with the same adjacency build.

```python
from collections import defaultdict
from typing import DefaultDict, List, Set


class Solution:
    def solve(self, records: List[List[str]], query: List[str]) -> bool:
        movement_from: DefaultDict[str, List[str]] = defaultdict(list)
        for url, referrer in records:
            if referrer != "":
                movement_from[referrer].append(url)

        start, target = query
        if start == target:
            return True

        visited: Set[str] = {start}
        stack: List[str] = [start]
        while stack:
            page = stack.pop()
            if page == target:
                return True
            for next_page in movement_from[page]:
                if next_page not in visited:
                    visited.add(next_page)
                    stack.append(next_page)

        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(v + e)`

Each page enters the stack at most once and each edge is inspected at most once from its source.

##### Space Complexity: `O(v + e)`

The adjacency list plus the visited set plus a stack bounded by the number of pages.

#### Key Insights

- An explicit stack is the recursive search with the interpreter removed from the loop; the visit order matches whenever branching is absent.
- Marking visited at push time bounds the stack by the page count; the start page is seeded into `visited` before the loop so a cycle back to `start` cannot re-push it.
- The zero-movement case stays a separate early return: seeding `stack` with `start` and popping it would also work, but the explicit rule mirrors the statement.

### Adjacency List with BFS

#### Derivation

Iterative DFS trades the recursion limit for an exploration order that can wander down a dead end before trying a short path. Reachability does not care about order, but a [queue](https://en.wikipedia.org/wiki/Queue_(abstract_data_type)) explores pages in rings around `start` (nearest first), which costs nothing here and is the structure to reach for when the follow-up asks for the minimum number of movements. The mechanics otherwise match the iterative DFS one-for-one: seed, mark, expand, mark at enqueue time:

1. Build `movement_from` as before and return `True` immediately when
   `start == target`.
2. Seed `queue` with `start` and mark `start` visited.
3. While the queue is non-empty, dequeue a page: return `True` when it equals
   `target`, otherwise enqueue each unvisited successor, marking each as it is
   enqueued.
4. An empty queue means no path exists: return `False`.

#### Walkthrough

A tailored input shows both the ring order and the cycle absorption; suppose `records = [["/b","/a"],["/c","/b"],["/a","/c"],["/help","/contact"]]` and `query = ["/a","/c"]`, so the first three records form the cycle `/a -> /b -> /c -> /a` and the fourth hangs an unreachable edge off `/contact -> /help`. The code checks the target on each edge, so the answer returns during `/b`'s expansion:

```text
seed /a                                        queue = [/a], visited = {/a}
dequeue /a   successor /b: not target -> enqueue   queue = [/b], visited = {/a, /b}
dequeue /b   successor /c == target -> return True
```

`/c` is found at two movements from `/a`, the minimum. The same input with `query = ["/a","/help"]` exercises the cycle and the empty-queue exit:

```text
seed /a                                        queue = [/a], visited = {/a}
dequeue /a   enqueue /b                        queue = [/b], visited = {/a, /b}
dequeue /b   enqueue /c                        queue = [/c], visited = {/a, /b, /c}
dequeue /c   successor /a already visited      queue = []  -> return False
```

The cycle closes harmlessly: `/a` sits in `visited`, so the ring stops expanding, `/help` is never reached because only `/contact` moves to it, and the emptied queue reports `False`.

#### Solution

The code is the iterative DFS with the stack swapped for a deque.

```python
from collections import defaultdict, deque
from typing import DefaultDict, List, Set


class Solution:
    def solve(self, records: List[List[str]], query: List[str]) -> bool:
        movement_from: DefaultDict[str, List[str]] = defaultdict(list)
        for url, referrer in records:
            if referrer != "":
                movement_from[referrer].append(url)

        start, target = query
        if start == target:
            return True

        visited: Set[str] = {start}
        queue = deque([start])
        while queue:
            page = queue.popleft()
            for next_page in movement_from[page]:
                if next_page == target:
                    return True
                if next_page not in visited:
                    visited.add(next_page)
                    queue.append(next_page)

        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(v + e)`

Each page is enqueued at most once and each edge inspected at most once.

##### Space Complexity: `O(v + e)`

The adjacency list plus the visited set plus a queue bounded by the number of pages.

#### Key Insights

- Same search, different frontier: the queue's ring order visits pages by movement count, which turns the same skeleton into a shortest-path answer if the follow-up asks for the number of hops.
- Marking visited at enqueue time (not dequeue time) keeps every page in the queue at most once.
- The target check sits on the edge, not on the dequeue, so the answer returns one expansion earlier; checking at dequeue works too and costs at most one extra ring.

## Comparison of Solutions

### Time Complexity

- **Adjacency List with Recursive DFS**: `O(v + e)` - each page expanded once over its edges.
- **Adjacency List with Iterative DFS**: `O(v + e)` - each page pushed and expanded at most once.
- **Adjacency List with BFS**: `O(v + e)` - each page enqueued at most once.

### Space Complexity

- **Adjacency List with Recursive DFS**: `O(v + e)` - adjacency list, visited set, and a call stack up to `v` frames deep.
- **Adjacency List with Iterative DFS**: `O(v + e)` - adjacency list, visited set, and an explicit stack.
- **Adjacency List with BFS**: `O(v + e)` - adjacency list, visited set, and a queue.

### Trade-offs

- The recursive DFS is the shortest to write and read, but it mortgages memory to the interpreter's call stack.
- The iterative DFS removes the depth limit at the price of manual stack bookkeeping.
- The BFS matches the others in cost and adds ring order, which nothing in this problem requires but a hop-count follow-up would.

### When to Use Each

- **Adjacency List with Recursive DFS**: quick scripts over graphs known to be shallow, or when the page's answer must be derived live on a whiteboard.
- **Adjacency List with Iterative DFS (Recommended)**: the OA answer: the constraint sizes (`2 × 10^5` records) make the recursion limit a real hazard.
- **Adjacency List with BFS**: when the follow-up asks for the minimum number of movements, or when team convention prefers frontier-style traversal.

### Optimization Notes

- Filter the empty referrer at build time: direct arrivals otherwise inject a phantom `""` page into the graph.
- `defaultdict(list)` builds the adjacency in one pass; a plain dict with `setdefault` works identically if the codebase avoids defaultdicts.
- Repeated movements need no deduplication for correctness (the visited set absorbs duplicates), but a `set` adjacency would cap the edge work when the input carries heavy repetition.
