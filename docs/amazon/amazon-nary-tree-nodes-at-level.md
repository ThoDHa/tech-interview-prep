# [Nodes at a Given N-ary Tree Level](https://www.fastprep.io/problems/amazon-nary-tree-nodes-at-level)

**Easy** | **NN minutes** | **Tree, Breadth First Search**

An N-ary tree uses node IDs from 0 through children.length - 1, with root ID 0. For each node ID, children[id] lists its child IDs from left to right.

Return the node IDs at zero-based level in left-to-right breadth-first order. Return an empty array when no nodes exist at that level.

## Examples

### Example 1

**Input:** `children = [[1,2,3],[4,5],[],[],[],[]]`, `level = 2`

**Output:** `[4,5]`

**Explanation:** Only nodes 4 and 5 are two edges from the root.

### Example 2

**Input:** `children = [[]]`, `level = 0`

**Output:** `[0]`

**Explanation:** Level zero contains the root.

### Example 3

**Input:** `children = [[1],[2],[3],[]]`, `level = 3`

**Output:** `[3]`

**Explanation:** The skewed tree has one node at level three.

## Constraints

- `1 ≤ children.length ≤ 100000.`
- `The child lists describe one valid rooted tree containing every node exactly once.`
- `0 ≤ level ≤ 100000.`

## Solutions

### Recursive DFS with Depth Pairs

#### Derivation

The most direct plan ignores the "breadth-first" hint in the output and treats grouping as a separate job, the same first step a binary tree level listing takes: walk the whole tree depth-first, remember each node's ID together with its depth, and collect the matching pairs afterward. The tree arrives as a children adjacency list, so the walk needs no node objects: a recursive `visit` receives the node ID and its depth, records the pair, and recurses into `children[node_id]`. Left-to-right child order is whatever the adjacency list order is, which is exactly the output order the problem wants:

1. Start `pairs` empty and call `visit(0, 0)` on the root ID `0`.
2. `visit` appends `(node_id, depth)` and calls itself on each entry of
   `children[node_id]` with `depth + 1`.
3. After the walk, filter `pairs` down to `level_bucket`, the entries whose
   depth equals `level`.
4. Return the node IDs of `level_bucket`, in walk order.

#### Walkthrough

Example 1 asks for level `2` of the tree `children = [[1,2,3],[4,5],[],[],[],[]]`, whose shape is root `0` with children `1`, `2`, `3`, and node `1` holding leaves `4` and `5`. The depth-first walk records one pair per node; each row shows the call and the pair it appends:

| Step | Call | Pair appended | `pairs` so far |
|------|------|---------------|----------------|
| 1 | `visit(0, 0)` | `(0, 0)` | `[(0,0)]` |
| 2 | `visit(1, 1)` | `(1, 1)` | `[(0,0),(1,1)]` |
| 3 | `visit(4, 2)` | `(4, 2)` | `[(0,0),(1,1),(4,2)]` |
| 4 | `visit(5, 2)` | `(5, 2)` | `[(0,0),(1,1),(4,2),(5,2)]` |
| 5 | `visit(2, 1)` | `(2, 1)` | `[(0,0),(1,1),(4,2),(5,2),(2,1)]` |
| 6 | `visit(3, 1)` | `(3, 1)` | `[(0,0),(1,1),(4,2),(5,2),(2,1),(3,1)]` |

The calls for `2` and `3` happen after the whole subtree of `1` because they sit later in `children[0]`, and nodes `4` and `5` keep their relative order because `visit` recurses into `children[1] = [4, 5]` in list order. Filtering the six pairs to depth `2` keeps rows 3 and 4, and returning their node IDs gives `[4,5]`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's walk and filter, with the tree read straight from the adjacency list:

```python
from typing import List, Tuple


class Solution:
    def solve(self, children: List[List[int]], level: int) -> List[int]:
        pairs: List[Tuple[int, int]] = []

        def visit(node_id: int, depth: int) -> None:
            pairs.append((node_id, depth))
            for child_id in children[node_id]:
                visit(child_id, depth + 1)

        visit(0, 0)

        level_bucket = [pair for pair in pairs if pair[1] == level]
        return [pair[0] for pair in level_bucket]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The walk visits each of the `n` nodes once and each child-list entry once, and the filter is one more pass over the `n` pairs.

##### Space Complexity: `O(n)`

The `pairs` list holds one entry per node, and the recursion stack on a skewed tree reaches `n` frames deep.

#### Key Insights

- A depth-first walk with left-to-right child recursion already emits same-level nodes in the required order, so no sort is ever needed: the filter preserves emission order.
- Storing `(node_id, depth)` pairs defers the level question until after the walk, which keeps the walk dead simple but pays a full `O(n)` record of the traversal.
- On a skewed tree the recursion depth is `n`, so a 100,000-node chain would exceed Python's default recursion limit; the iterative versions below remove that hazard.

### Level-by-Level BFS

#### Derivation

The pairs list exists only because the depth-first walk visits level `2` nodes while its head is elsewhere. But the output is shaped like the traversal it wants: one complete level at a time, left to right. A breadth-first queue already works in exactly that rhythm, and slicing the queue per level removes the depth bookkeeping altogether: each round, whatever sits in the queue is one whole level in left-to-right order. Either that round is the requested `level`, and the queue's contents are the answer, or every node in the round is expanded and its children become the next round:

1. Seed `frontier` with the root ID `0` and set `depth = 0`.
2. While `frontier` is non-empty: when `depth == level`, return `frontier`.
3. Otherwise expand the round: `next_frontier` collects, for each ID in
   `frontier` in order, every entry of `children[ID]`.
4. Replace `frontier` with `next_frontier` and increment `depth`. When the
   queue drains before `depth` reaches `level`, no nodes exist at that level
   and the loop exits with `frontier` empty, so returning `frontier` covers
   the too-deep case without a special branch.

#### Walkthrough

Example 1 again, `children = [[1,2,3],[4,5],[],[],[],[]]` with `level = 2`. Each round below shows the queue at its start and the expansion it performs:

```text
depth 0   frontier = [0]
          expand: children[0] = [1, 2, 3]
depth 1   frontier = [1, 2, 3]
          expand: children[1] = [4, 5], children[2] = [], children[3] = []
depth 2   frontier = [4, 5]
          depth == level -> return [4, 5]
```

Three rounds run, the third finds `depth == level`, and its queue `[4, 5]` is returned as-is, matching the expected Output for Example 1. Example 3, `children = [[1],[2],[3],[]]` with `level = 3`, stretches the same loop into four rounds of one node each and returns `[3]`; had `level` been `5`, the frontier would have drained at depth `3`, and the empty-queue exit would return `[]`.

#### Solution

The code is the round loop from the walkthrough, with the return-inside-the-loop doubling as the empty-result exit:

```python
from typing import List


class Solution:
    def solve(self, children: List[List[int]], level: int) -> List[int]:
        frontier: List[int] = [0]
        depth = 0

        while frontier:
            if depth == level:
                return frontier

            next_frontier: List[int] = []
            for node_id in frontier:
                for child_id in children[node_id]:
                    next_frontier.append(child_id)
            frontier = next_frontier
            depth += 1

        return frontier
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node enters the frontier exactly once and is expanded at most once; the loop stops expanding as soon as the requested level is reached, so it often touches less than the whole tree.

##### Space Complexity: `O(n)`

The frontier holds one level, which on the widest tree is a constant fraction of all `n` nodes; `next_frontier` doubles that peak briefly.

#### Key Insights

- Matching the traversal to the output eliminates the bookkeeping: level rounds make the depth counter the only extra state, and the answer is literally the queue at the right moment.
- Returning `frontier` at the top of the round folds three cases (hit, too deep, exact fit) into one shape: an empty queue means an empty answer.
- Early exit is the quiet win over the DFS pairs approach: nothing past the requested level is ever expanded.

### Iterative DFS with Explicit Stack

#### Derivation

The recursive walk's only weakness is the interpreter's call stack, and the repair is the same substitution the iterative island fill makes: the call stack is just a to-do list, so hold it in an explicit list of `(node_id, depth)` pairs and pop instead of recursing. One consequence is worth naming before the code: a stack is last-in, first-out, so pushing children in list order visits them in reverse. For the count-style question that would not matter, but this output is ordered, and the repair is to push each child list backwards, which restores left-to-right emission. Because the traversal interleaves depths, the result must still be filtered at the end, exactly as in the recursive version:

1. Seed `stack` with `(0, 0)`.
2. Pop `(node_id, depth)`; when `depth == level`, append `node_id` to
   `level_bucket`; otherwise push `(child_id, depth + 1)` for every
   `child_id` in `reversed(children[node_id])`.
3. When the stack empties, return `level_bucket`, whose append order is
   left-to-right.

#### Walkthrough

Example 1, `children = [[1,2,3],[4,5],[],[],[],[]]` with `level = 2`. Each line is one pop; the stack is written bottom-to-top, so the rightmost entry pops next:

```text
seed                stack = [(0,0)]
pop (0,0)  d=0      push reversed [1,2,3]     stack = [(1,1), (2,1), (3,1)]
pop (3,1)  d=1      children[3] = []          stack = [(1,1), (2,1)]
pop (2,1)  d=1      children[2] = []          stack = [(1,1)]
pop (1,1)  d=1      push reversed [4,5]       stack = [(4,2), (5,2)]
pop (5,2)  d=2      depth == level            level_bucket = [5]
pop (4,2)  d=2      depth == level            level_bucket = [5, 4]
```

There it is: `5` pops before `4`, and the function would return `[5,4]`, reversed against the expected Output `[4,5]`. The reversal is mechanical, not logical: the stack flipped the two subtrees' visit order. Feeding children in backwards (`reversed`) fixes the emission order without touching the algorithm, and the fixed walk collects `level_bucket = [4, 5]` at the same two pops. The filtered result matches the expected Output for Example 1.

#### Solution

The code is the pop loop with the backwards push; the filter matches the recursive version's:

```python
from typing import List, Tuple


class Solution:
    def solve(self, children: List[List[int]], level: int) -> List[int]:
        stack: List[Tuple[int, int]] = [(0, 0)]
        level_bucket: List[int] = []

        while stack:
            node_id, depth = stack.pop()
            if depth == level:
                level_bucket.append(node_id)
                continue
            for child_id in reversed(children[node_id]):
                stack.append((child_id, depth + 1))

        return level_bucket
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is pushed and popped at most once, and the per-pop work is proportional to its child count, so the total is one pass over the tree.

##### Space Complexity: `O(n)`

The explicit stack holds at most `n` entries on a skewed tree, and `level_bucket` holds the answer level.

#### Key Insights

- An explicit stack reproduces the recursion with no depth limit, which matters here more than usual: the constraints allow 100,000 nodes on one chain.
- LIFO order reverses child-list traversal, and pushing `reversed(children[node_id])` is the minimal correction; forgetting it produces silently reversed per-level output.
- Popping at the requested level and continuing (instead of expanding) is what keeps the stack from growing into the subtree below the answer.

## Comparison of Solutions

### Time Complexity

- **Recursive DFS with Depth Pairs**: `O(n)` - one walk over all nodes plus one filter pass, always touching the whole tree.
- **Level-by-Level BFS**: `O(n)` - each node enqueued at most once, with the loop stopping at the requested level.
- **Iterative DFS with Explicit Stack**: `O(n)` - one push and pop per node with a proportional amount of child-list scanning.

### Space Complexity

- **Recursive DFS with Depth Pairs**: `O(n)` - the pairs list plus a recursion stack that reaches `n` frames on a skewed tree.
- **Level-by-Level BFS**: `O(n)` - the frontier holds the widest level, briefly doubled by `next_frontier`.
- **Iterative DFS with Explicit Stack**: `O(n)` - the explicit stack on a skewed tree plus the answer bucket.

### Trade-offs

- **Recursive DFS with Depth Pairs**: the clearest expression of "walk then group" and immune to queue-slicing subtleties, but it always traverses the entire tree and its pairs list is pure overhead.
- **Level-by-Level BFS**: the traversal that mirrors the output shape, with early exit at the requested level and no per-node depth records, at the cost of building one throwaway frontier per round.
- **Iterative DFS with Explicit Stack**: recursion-free like the BFS form but shape-agnostic, so it walks the whole tree and must carry the reversed-push subtlety to keep the order right.

### When to Use Each

- **Level-by-Level BFS (Recommended)**: the interview default for "nodes at level L": the round structure states the answer, terminates early, and needs no depth-pair filtering.
- **Recursive DFS with Depth Pairs**: when the tree is known shallow or the same walk must serve several level queries at once, since one pairs list answers any `level` with a different filter.
- **Iterative DFS with Explicit Stack**: when recursion depth is the concern but level slicing is not wanted, and in trees where per-node expansion order must follow the input's child list exactly once.

### Optimization Notes

- The BFS form never expands nodes below the requested level, so its best case touches far fewer than `n` nodes; the two DFS forms have no such exit and always pay the full walk.
- Both iterative versions avoid Python's recursion limit, which the constraints make a real hazard: a 100,000-node chain overflows the default limit of 1,000 frames.
- The reversed-push fix is the kind of bug tests catch only when a level holds two or more nodes with siblings ordered non-symmetrically; Example 1's `[4, 5]` is precisely such a case, which is why the walkthrough deliberately shows the broken order first.
