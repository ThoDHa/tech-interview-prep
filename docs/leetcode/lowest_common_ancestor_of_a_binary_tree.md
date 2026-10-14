# [Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/)

**Medium** | **25 minutes** | **Tree, Depth-First Search, Binary Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Algorithm:** [Lowest common ancestor](https://en.wikipedia.org/wiki/Lowest_common_ancestor) · [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) · [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)

**Practice:** [`practice/lowest_common_ancestor_of_a_binary_tree/solution.py`](../../practice/lowest_common_ancestor_of_a_binary_tree/solution.py)

Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.

According to the definition of LCA on Wikipedia: "The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in `T` that has both `p` and `q` as descendants (where we allow a node to be a descendant of itself)."

## Examples

### Example 1

![Lowest Common Ancestor Tree Example](assets/lowest_common_ancestor_of_a_binary_tree_example1.png)

**Input:** `root = [3,5,1,6,2,0,8,null,null,7,4]`, `p = 5`, `q = 1`

**Output:** `3`

**Explanation:** The LCA of nodes `5` and `1` is `3`.

### Example 2

![Lowest Common Ancestor Tree Example](assets/lowest_common_ancestor_of_a_binary_tree_example1.png)

**Input:** `root = [3,5,1,6,2,0,8,null,null,7,4]`, `p = 5`, `q = 4`

**Output:** `5`

**Explanation:** The LCA of nodes `5` and `4` is `5`, since a node can be a descendant of itself according to the LCA definition.

### Example 3

**Input:** `root = [1,2]`, `p = 1`, `q = 2`

**Output:** `1`

## Constraints

- The number of nodes in the tree is in the range `[2, 10^5]`.
- `-10^9 <= Node.val <= 10^9`
- All `Node.val` are unique.
- `p != q`
- `p` and `q` will exist in the tree.

## Deriving the Solution

The lowest common ancestor of `p` and `q` is where their ancestries meet: the root-to-`p` path and the root-to-`q` path share a prefix, and the deepest node of that shared prefix is the LCA. With no value ordering to exploit in a general binary tree, every solution below must search for the two targets; they differ in how the meeting point is detected.

1. **Start literal.** Materialize both root-to-target paths with a
   backtracking DFS, then walk them in lockstep until they diverge. Two passes over the tree and two stored paths: see [Find Root-to-Node Paths](#find-root-to-node-paths).
2. **Spot the waste.** The paths are compared once and discarded, and the
   divergence can be detected during the search itself. One post-order traversal lets each subtree report which target it contains; the first node that hears back from both sides is the LCA. Same `O(n)` time, one pass, no path storage: see [Recursive DFS](#recursive-dfs).
3. **Remove the recursion.** A tree of `10^5` nodes can be deep enough to
   overflow the call stack. Recording each node's parent during a BFS makes ancestry walkable upward without recursion: collect `p`'s ancestors into a set, then climb from `q` until the first member of that set appears: see [Iterative with Parent Pointers](#iterative-with-parent-pointers).

## Solutions

### Find Root-to-Node Paths

#### Derivation

The most direct way to think about a [lowest common ancestor](https://en.wikipedia.org/wiki/Lowest_common_ancestor) is to first find the two paths that lead from the root down to `p` and to `q`. Once both paths are in hand, they share a common prefix that starts at the root and runs until they diverge; the last node before that divergence is the LCA.

1. Write a small recursive search that builds the root-to-target path by hand:
   append the current node, return success if it is the target, otherwise try each subtree, and `pop` the node back off when neither subtree contains the target.
2. Run that search twice, once for `p` and once for `q`, producing two lists of
   nodes ordered from the root downward.
3. Walk the two paths together. While the nodes match, the shared ancestor keeps
   getting deeper; the moment they differ (or one path ends), the last matching node is the answer.

Because a node is allowed to be a descendant of itself, a path that ends at the other target's path naturally yields that target as the LCA: `zip` simply stops at the shorter path.

#### Walkthrough

Trace the first solution on Example 1: `root = [3,5,1,6,2,0,8,null,null,7,4]`, `p = 5`, `q = 1`. That tree looks like this, with `5` and `1` being the two children of the root `3`:

```text
        3
       / \
      5   1
     / \ / \
    6  2 0  8
      / \
     7   4
```

First, `find_path` builds the route from the root down to `p = 5`. It appends each node on the way in and `pop`s any node whose subtrees do not contain the target:

| Call | `path` while inside | Result |
|------|---------------------|--------|
| `find_path(3, 5)` | `[3]` | recurse left |
| `find_path(5, 5)` | `[3, 5]` | `node is target`, returns `True` |

The `True` bubbles straight back up, so nothing is popped: `path_p = [3, 5]`.

Next the same search runs for `q = 1`. The root `3` is appended, its left subtree (rooted at `5`) is searched first and fails, so that exploration unwinds and pops itself back off, then the right subtree finds the target:

| Call | `path` while inside | Result |
|------|---------------------|--------|
| `find_path(3, 1)` | `[3]` | left subtree fails, try right |
| `find_path(1, 1)` | `[3, 1]` | `node is target`, returns `True` |

So `path_q = [3, 1]`.

Finally, walk the two paths in lockstep with `zip` and keep the last node they share:

| Step | `a` (from `path_p`) | `b` (from `path_q`) | `a is b`? | `lca` |
|------|---------------------|---------------------|-----------|-------|
| 1 | `3` | `3` | yes | `3` |
| 2 | `5` | `1` | no, `break` | `3` |

The paths agree on the root and immediately diverge, so the loop breaks with `lca = 3`. The function returns the node `3`, which matches the expected Output of `3`.

#### Solution

The code is the walkthrough written down: the backtracking path builder run twice, then the lockstep comparison.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
from typing import List


class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # Collect the chain of nodes from root down to a target.
        def find_path(node: 'TreeNode', target: 'TreeNode', path: List['TreeNode']) -> bool:
            if not node:
                return False
            path.append(node)
            if node is target:
                return True
            if find_path(node.left, target, path) or find_path(node.right, target, path):
                return True
            # This node leads nowhere useful, so drop it before backtracking.
            path.pop()
            return False

        path_p, path_q = [], []
        find_path(root, p, path_p)
        find_path(root, q, path_q)

        # Walk both paths from the root in lockstep; the last shared node is the LCA.
        lca = root
        for a, b in zip(path_p, path_q):
            if a is b:
                lca = a
            else:
                break
        return lca
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each path search may visit every node once in the worst case, and comparing the two paths is bounded by the tree height. The total work is linear in the number of nodes.

##### Space Complexity: `O(n)`

Both path lists and the recursion stack are each bounded by the tree height, which is `O(n)` for a skewed tree.

#### Key Insights

- Reframing "common ancestor" as "common prefix of two root-to-node paths" makes
  the problem concrete and easy to reason about without any cleverness.
- Building the path by appending on the way down and popping on the way back is
  the standard backtracking pattern for recording a route through a tree.
- It is wasteful compared with the single-pass solutions: it scans the tree twice
  and stores two full paths, but it is the most obvious approach to derive.

### Recursive DFS

#### Derivation

The path-based approach searches the tree twice and stores routes it only compares once. The repair comes from noticing what the comparison actually detects: the LCA is the deepest node from which `p` and `q` are reachable in different directions (or the node that is itself one of them while the other lies below). A single [post-order traversal](https://en.wikipedia.org/wiki/Depth-first_search) answers this: each call reports back the relevant node it found, and the first node that hears back from *both* of its sides is the LCA.

1. Base case: a `None` subtree returns `None`. If the current node *is* `p` or
   `q`, return it immediately. Because the inputs are guaranteed present and a node may be its own ancestor, this correctly handles the case where one target sits above the other.
2. Recurse into the left and right subtrees.
3. If both recursive calls return non-null, `p` and `q` were found on opposite
   sides, so the current node is their lowest common ancestor.
4. If only one side is non-null, both targets live within that side; propagate
   that node upward unchanged.

Correctness follows from the post-order order: a node only declares itself the LCA once both descendants have reported, guaranteeing we return the deepest such node. The Invariant below states the call contract this rests on: each call returns the LCA when both targets lie in its subtree, otherwise whichever single target it contains, otherwise `None`.

#### Invariant

The recursion has no separate "not found" signal: every call returns a node (or `None`), and what that node means is fixed by a contract each call honors. For the subtree rooted at `root`:

$$ f(\textit{root}) = \begin{cases} \mathrm{LCA}(p, q), & \text{both } p \text{ and } q \text{ lie in the subtree} \\[4pt] p \text{ or } q, & \text{exactly one of them lies in the subtree} \\[4pt] \texttt{None}, & \text{neither lies in the subtree} \end{cases} $$

```text
lowestCommonAncestor(root, p, q) =
    LCA(p, q)   if both p and q lie in the subtree rooted at root
    p or q      if exactly one of them lies in the subtree rooted at root
    None        if neither lies in the subtree rooted at root
```

Every branch honors it. An empty subtree contains neither target, so `None` is correct. When `root is p` (or `q`), the subtree holds at least that target and `root` is the highest node in it, which satisfies both of the first two cases at once: if the other target lies below, `root` is their LCA, and if it does not, `root` is the single target contained. Either way the answer is `root`, which is why the early return is sound without ever looking below it.

The composition step reads straight off the contract on the children. If `left` and `right` are both non-`None`, each side holds exactly one target, so `root` is the deepest node with both beneath it. If exactly one is non-`None`, whatever that side reported is already the correct answer for the larger subtree, hence `return left if left else right` rather than any further inspection.

Soundness also leans on the problem's guarantee that both targets exist in the tree. Without it a lone returned node is ambiguous: `p` bubbling all the way to the root would be reported as the LCA of a pair that has none. Given the guarantee, the middle case is only ever a waypoint, and the top-level call falls in the first case, so it returns the LCA.

#### Walkthrough

Let us run the single pass on Example 1: `root = [3,5,1,6,2,0,8,null,null,7,4]`, `p = 5`, `q = 1`, the tree

```text
        3
       / \
      5   1
     / \ / \
    6  2 0  8
      / \
     7   4
```

The indentation shows the recursion; each call either matches a target and returns itself, or waits for both children to report:

```text
lowestCommonAncestor(3)    3 is neither p nor q; recurse into both sides
  lowestCommonAncestor(5)  root is p -> return node 5   (6, 2, 7, 4 never visited)
  lowestCommonAncestor(1)  root is q -> return node 1   (0, 8 never visited)
back at 3: left = 5, right = 1, both non-None -> return 3
```

The left call matches `p` at once and returns node `5` without descending: by the Invariant, `5` is the correct report for its whole subtree whether or not `q` also hides beneath it. The right call likewise returns node `1`. Back at the root, `left` and `right` are both non-`None`: one target was found on each side, so `3` is the split point and is returned. That is the expected Output `3`, found in one traversal with no path lists.

#### Solution

The code is the walkthrough's contract in four lines: match, recurse both sides, return the split point or propagate the single find.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # An empty subtree contains neither target; a node that is p or q
        # reports itself upward
        if not root or root is p or root is q:
            return root

        # Search both subtrees for the targets
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        # Targets found on opposite sides -> this node is their LCA
        if left and right:
            return root

        # Otherwise both lie in (at most) one subtree; bubble up that result
        return left if left else right
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

In the worst case we visit every node once, doing constant work per node.

##### Space Complexity: `O(h)`

The recursion stack is bounded by the tree height `h`, which is `O(n)` for a skewed tree and `O(log n)` for a balanced one.

#### Key Insights

- Returning the found target (or `None`) from each call lets the recursion both
  locate the nodes and identify the split point in one pass.
- The node where the search "splits", with one target on each side, is exactly
  the LCA.
- Identity comparison (`is`) is used because we are matching node references, not
  values.
- Allowing a node to be a descendant of itself is handled for free by returning
  early when `root is p or root is q`.

### Iterative with Parent Pointers

#### Derivation

The recursive solution can overflow the call stack on a deeply skewed tree of `10^5` nodes. Instead of recursing, this approach makes the tree's implicit upward edges explicit by recording each node's parent during a [breadth-first](https://en.wikipedia.org/wiki/Breadth-first_search) walk. Once both `p` and `q` have parents on record, the LCA becomes the first shared node along the two upward paths to the root.

1. Traverse the tree (BFS here), storing `parent[child] = node` for every node
   discovered. Stop as soon as both `p` and `q` appear in the `parent` map, since nothing below them matters.
2. Walk upward from `p` to the root, collecting every node on that path into an
   `ancestors` set.
3. Walk upward from `q`. The first node already present in `ancestors` is the
   lowest node common to both paths, which is exactly the LCA.

The root's parent is set to `None` so the upward walks terminate cleanly. This mirrors the classic technique for finding the intersection of two linked paths, applied to the chains of ancestry running from each target to the root.

#### Walkthrough

Let us run the three phases on Example 2, where the BFS must dig several levels before both targets are mapped: `root = [3,5,1,6,2,0,8,null,null,7,4]`, `p = 5`, `q = 4`, the tree

```text
        3
       / \
      5   1
     / \ / \
    6  2 0  8
      / \
     7   4
```

Phase one builds the `parent` map level by level. The map starts as `{3: None}` and the `queue` as `[3]`; the loop keeps going while either target is missing from the map:

```text
pop 3   map 5 -> 3, 1 -> 3     queue = [5, 1]        5 mapped, 4 missing -> continue
pop 5   map 6 -> 5, 2 -> 5     queue = [1, 6, 2]     4 missing -> continue
pop 1   map 0 -> 1, 8 -> 1     queue = [6, 2, 0, 8]  4 missing -> continue
pop 6   no children            queue = [2, 0, 8]     4 missing -> continue
pop 2   map 7 -> 2, 4 -> 2     queue = [0, 8, 7, 4]  both 5 and 4 mapped -> stop
```

The BFS stops with `0` and `8` still in the queue: once both targets have parents, nothing deeper matters. Phase two climbs from `p = 5` collecting `ancestors`: add `5`, step to `parent[5] = 3`, add `3`, and `parent[3] = None` ends the climb with `ancestors = {5, 3}`. Phase three climbs from `q = 4` testing membership at each stop:

```text
node = 4   4 not in ancestors  -> node = parent[4] = 2
node = 2   2 not in ancestors  -> node = parent[2] = 5
node = 5   5 in ancestors      -> return node 5
```

The first node on `q`'s upward path that also lies on `p`'s path is `5`, so node `5` is returned: `p` is its own ancestor here, matching the expected Output `5`.

#### Solution

The code is the walkthrough's three phases in order: BFS until both targets are mapped, collect `ancestors` of `p`, climb from `q`.

```python
from collections import deque

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # Record each node's parent by walking the tree until both targets seen.
        parent = {root: None}
        queue = deque([root])

        while p not in parent or q not in parent:
            node = queue.popleft()
            if node.left:
                parent[node.left] = node
                queue.append(node.left)
            if node.right:
                parent[node.right] = node
                queue.append(node.right)

        # Collect every ancestor of p (including p itself) into a set.
        ancestors = set()
        node = p
        while node:
            ancestors.add(node)
            node = parent[node]

        # Climb from q until we hit the first node shared with p's ancestry.
        node = q
        while node not in ancestors:
            node = parent[node]
        return node
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Building the parent map visits at most every node once. Each upward walk is bounded by the tree height, which is itself `O(n)`, so the total stays linear.

##### Space Complexity: `O(n)`

The `parent` map stores one entry per visited node, the BFS queue can hold up to a full level, and the `ancestors` set holds one path to the root. All three are bounded by `O(n)`.

#### Key Insights

- Recording parent pointers converts the downward-only tree into a structure
  where each node can climb back toward the root, which is what makes the iterative solution possible.
- Halting the traversal once both targets are mapped avoids scanning the entire
  tree when both nodes appear early.
- Gathering one target's ancestry into a set turns the "first common ancestor"
  question into a simple membership test as the other target climbs.
- Setting the root's parent to `None` gives both upward walks a guaranteed
  termination point.

## Comparison of Solutions

### Time Complexity

- **Find Root-to-Node Paths**: `O(n)` - Two path searches each touch every node once in the worst case.
- **Recursive DFS**: `O(n)` - A single post-order traversal touches each node once.
- **Iterative with Parent Pointers**: `O(n)` - Building the parent map is linear, and the two upward walks are each bounded by the tree height.

### Space Complexity

- **Find Root-to-Node Paths**: `O(n)` - Two path lists and the recursion stack are each bounded by the tree height.
- **Recursive DFS**: `O(h)` - Only the recursion stack is used, bounded by tree height `h`.
- **Iterative with Parent Pointers**: `O(n)` - The parent map, BFS queue, and ancestor set each scale with the node count.

### Trade-offs

- **Find Root-to-Node Paths**: The most intuitive to derive, but it scans the tree twice and stores two full paths instead of answering in a single pass.
- **Recursive DFS**: Compact and elegant with no auxiliary data structures, but it relies on the call stack, which can overflow on a deeply skewed tree of `10^5` nodes.
- **Iterative with Parent Pointers**: Avoids recursion depth limits entirely, but it allocates explicit maps and sets that consume more memory.

### When to Use Each

- **Find Root-to-Node Paths**: As a teaching baseline, or when you also need the actual paths to `p` and `q`, not just their meeting point.
- **Recursive DFS (Recommended)**: Best for interviews and balanced trees - the cleanest expression of the LCA idea in a single pass.
- **Iterative with Parent Pointers**: When the tree may be extremely deep and recursion could exceed Python's stack limit, or when an explicit non-recursive solution is required.

### Optimization Notes

- The Find Root-to-Node Paths approach collapses into the single-pass Recursive DFS once you notice the split point can be detected during the descent itself, without materializing both paths.
- The recursive solution can convert to an explicit stack if recursion depth is the only concern, but the parent-pointer approach reads more naturally.
- Stopping the BFS as soon as both targets are recorded prevents needless traversal of the rest of the tree when `p` and `q` sit near the top.
- For repeated LCA queries on a static tree, precomputing parent pointers (or binary-lifting tables) once amortizes the cost across many queries, which neither single-query solution exploits.
