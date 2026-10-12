# [Lowest Common Ancestor Implemented with Stack](https://www.fastprep.io/problems/amazon-lowest-common-ancestor-implemented-with-stack)

**Medium** | **NN minutes** | **Tree, Stack, Hash Table**

This question was reported for Amazon Fall Intern onsite.

Given the root of a binary tree and two distinct nodes p and q in that tree, return their lowest common ancestor.

In this FastPrep version, the binary tree is provided as root, a level-order representation of the tree. Each non-null entry is an integer stored as a string, and "null" marks a missing child. The values p and q identify the two target nodes.

The lowest common ancestor of two nodes is the deepest node in the tree that has both p and q as descendants. A node may be considered a descendant of itself.

You should solve this problem iteratively. In particular, use a stack to traverse the tree and build a parent mapping for each visited node. Then use that parent information to find the first common ancestor of p and q.

A Note From OP

The original OP mentioned that the interviewer specifically required a stack-based solution. The approach they described was to use a stack to traverse the tree and build a parent map for every node. Then, starting from p, move upward to the root and store all ancestors in a set. Finally, starting from q, move upward toward the root; the first node that already appears in p's ancestor set is the lowest common ancestor.

Reference Choice

There are 3 "find lowest common ancestor" questions on LeetCode. 236 was selected as the reference because this source describes the LCA of exactly two existing nodes, p and q, in a normal binary tree.

It does not match 1644, because that variant changes the contract by allowing one or both target nodes to be missing from the tree. It also does not match 1676, because that variant asks for the LCA of multiple nodes, not just p and q.

Additional Practice Note

A super tiny interviewer-pattern prediction:::) if you are interested, you can also try solving the other two Lowest Common Ancestor variants with a stack-based approach. Given that this interviewer seems to be a fan of stacks, they may ask one LCA problem as the main interview question and use the other two LCA variants as follow-ups if time allows 😉

## Examples

### Example 1

**Input:** `root = ["10","5","15","3","7","12","18","null","4","6","8"]`, `p = 3`, `q = 8`

**Output:** `5`

**Explanation:** Node 5 is the lowest node that has both 3 and 8 in its subtree.

### Example 2

**Input:** `root = ["10","5","15","3","7","12","18","null","4","6","8"]`, `p = 5`, `q = 8`

**Output:** `5`

**Explanation:** A node can be an ancestor of itself. Since 5 is an ancestor of 8, the lowest common ancestor is 5.

## Constraints

- `2 <= root.length <= 10^5`
- `Each non-null entry in root is an integer in the range [-10^9, 10^9].`
- `All non-null node values are unique.`
- `p and q are distinct.`
- `Both p and q exist in the tree.`

## Solutions

All three solutions share one piece of bookkeeping: `build_tree`, a queue-based parse of the level-order array into `TreeNode` objects. The interviewer's stack requirement applies to the ancestor search, not to the parse, and every traversal below starts from the parsed tree.

### Find Root-to-Node Paths

#### Derivation

The most literal reading asks two questions: what is the path from the root down to `p`, and what is the path from the root down to `q`? Both paths start at the root and share a prefix exactly up to the lowest common ancestor, because everything below the LCA lives in one child subtree of it and `p` and `q` are distinct. So the LCA is the last entry the two paths share. A [depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) with backtracking collects a root-to-target path in one walk: append each node on the way down, and pop the node when its whole subtree fails to hold the target:

1. Parse the level-order `root` array into `TreeNode` objects with `build_tree`.
2. `find_path(node, target, path)` appends `node.value`, returns `True` when the
   value matches, otherwise tries `node.left` then `node.right`, and pops the
   value from `path` when neither subtree holds the target.
3. Collect `path_to_p` and `path_to_q` with two such searches.
4. Walk both paths from the front while entries agree, remembering the last
   shared value in `lowest_common`; return it.

#### Walkthrough

Example 1: `root = ["10","5","15","3","7","12","18","null","4","6","8"]`, `p = 3`, `q = 8`, the tree

```text
        10
       /  \
      5    15
     / \   / \
    3   7 12  18
     \  / \
      4 6  8
```

The two searches run in sequence; each line is one descent step, and the pop-back fires when a subtree is exhausted without a match:

```text
find_path(10, 3)   append 10   path_to_p = [10]
find_path(5, 3)    append 5    path_to_p = [10, 5]
find_path(3, 3)    append 3    path_to_p = [10, 5, 3]      target found, done

find_path(10, 8)   append 10   path_to_q = [10]
find_path(5, 8)    append 5    path_to_q = [10, 5]
find_path(3, 8)    append 3    path_to_q = [10, 5, 3]      left is null, try right
find_path(4, 8)    append 4    path_to_q = [10, 5, 3, 4]   no 8 below 4 -> pop 4
                   8 not below 3 -> pop 3                  path_to_q = [10, 5]
find_path(7, 8)    append 7    path_to_q = [10, 5, 7]
find_path(6, 8)    append 6    path_to_q = [10, 5, 7, 6]   no 8 below 6 -> pop 6
find_path(8, 8)    append 8    path_to_q = [10, 5, 7, 8]   target found, done
```

Comparing from the front, the entries agree at `10` and `5` and diverge at `3` versus `7`, so `lowest_common = 5`, matching the expected Output.

#### Solution

The code is the walkthrough's two searches and the front-to-back comparison.

```python
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


def build_tree(values: List[str]) -> TreeNode:
    root = TreeNode(int(values[0]))
    queue = deque([root])
    child_slot = 1
    while queue and child_slot < len(values):
        node = queue.popleft()
        left_entry = values[child_slot]
        child_slot += 1
        if left_entry != "null":
            node.left = TreeNode(int(left_entry))
            queue.append(node.left)
        if child_slot < len(values):
            right_entry = values[child_slot]
            child_slot += 1
            if right_entry != "null":
                node.right = TreeNode(int(right_entry))
                queue.append(node.right)
    return root


class Solution:
    def solve(self, root: List[str], p: int, q: int) -> int:
        tree = build_tree(root)

        def find_path(node: Optional[TreeNode], target: int, path: List[int]) -> bool:
            if node is None:
                return False
            path.append(node.value)
            if (node.value == target
                    or find_path(node.left, target, path)
                    or find_path(node.right, target, path)):
                return True
            path.pop()
            return False

        path_to_p: List[int] = []
        path_to_q: List[int] = []
        find_path(tree, p, path_to_p)
        find_path(tree, q, path_to_q)

        lowest_common = tree.value
        for p_entry, q_entry in zip(path_to_p, path_to_q):
            if p_entry != q_entry:
                break
            lowest_common = p_entry
        return lowest_common
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each of the two searches visits any node at most once, and the prefix comparison touches at most `n` entries.

##### Space Complexity: `O(n)`

The two path lists and the recursion stack are each bounded by the tree height, which reaches `n` on a skewed tree.

#### Key Insights

- The LCA is exactly where the root-to-target paths stop sharing entries, so the search reduces to comparing two lists from the front.
- The backtracking `path.pop()` is what keeps `path` a faithful root-to-current-node chain: a failed subtree must not leave entries behind.
- A node counts as its own ancestor, which is why Example 2 returns `5` even though `p` sits on the path to `q`.

### Stack Traversal with Parent Map

#### Derivation

The baseline satisfies the mathematics but not the interviewer's requirement: it recurses, and on a skewed tree of `10^5` nodes the call stack can breach Python's recursion limit. The repair inverts the direction of travel. Tree edges point downward, yet every node needs only its parent to walk upward, and one traversal can record that single pointer for every node. Replace recursion with an explicit [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)): pop a node, write `parent[child] = node` for each child, push the children. Once both targets are mapped, collect every ancestor of `p` into a set and climb from `q` until the first value already in the set appears:

1. Parse the input with `build_tree` as before.
2. Seed `parent = {tree.value: None}` and `stack = [tree]`; the root's `None`
   parent is the termination marker for both upward climbs.
3. While `stack` is non-empty, pop `node`; for each existing child, record its
   parent value and push it.
4. Starting from `p`, follow `parent` links up to the root, adding each value to
   `ancestors`.
5. Starting from `q`, follow `parent` links until the value is in `ancestors`;
   that value is the LCA.

#### Walkthrough

Example 2: `p = 5`, `q = 8` on the same tree, the case where one target is an ancestor of the other. The stack drains root first and deepest nodes last; each line is one pop:

```text
pop 10   parent[5] = 10, parent[15] = 10   stack = [5, 15]
pop 15   parent[12] = 15, parent[18] = 15  stack = [5, 12, 18]
pop 18   leaf                              stack = [5, 12]
pop 12   leaf                              stack = [5]
pop 5    parent[3] = 5, parent[7] = 5      stack = [3, 7]
pop 7    parent[6] = 7, parent[8] = 7      stack = [3, 6, 8]
pop 8    leaf                              stack = [3, 6]
pop 6    leaf                              stack = [3]
pop 3    left is null; parent[4] = 3       stack = [4]
pop 4    leaf                              stack = []
```

The climb from `p` gathers `ancestors = {5, 10}`, and the climb from `q` tests membership at every stop:

```text
climber = 8   8 not in ancestors -> climber = parent[8] = 7
climber = 7   7 not in ancestors -> climber = parent[7] = 5
climber = 5   5 in ancestors     -> return 5
```

The first value on `q`'s upward chain that also lies on `p`'s chain is `5`, and because `p` itself was added to `ancestors`, the ancestor-of-itself case resolves with no special casing. The result matches the expected Output.

#### Solution

The code is the walkthrough's three phases: one stack pass to record parents, one climb to collect `ancestors`, one climb to meet it.

```python
from collections import deque
from typing import Dict, List, Optional, Set


class TreeNode:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


def build_tree(values: List[str]) -> TreeNode:
    root = TreeNode(int(values[0]))
    queue = deque([root])
    child_slot = 1
    while queue and child_slot < len(values):
        node = queue.popleft()
        left_entry = values[child_slot]
        child_slot += 1
        if left_entry != "null":
            node.left = TreeNode(int(left_entry))
            queue.append(node.left)
        if child_slot < len(values):
            right_entry = values[child_slot]
            child_slot += 1
            if right_entry != "null":
                node.right = TreeNode(int(right_entry))
                queue.append(node.right)
    return root


class Solution:
    def solve(self, root: List[str], p: int, q: int) -> int:
        tree = build_tree(root)

        parent: Dict[int, Optional[int]] = {tree.value: None}
        stack: List[TreeNode] = [tree]
        while stack:
            node = stack.pop()
            if node.left:
                parent[node.left.value] = node.value
                stack.append(node.left)
            if node.right:
                parent[node.right.value] = node.value
                stack.append(node.right)

        ancestors: Set[int] = set()
        walker: Optional[int] = p
        while walker is not None:
            ancestors.add(walker)
            walker = parent[walker]

        climber = q
        while climber not in ancestors:
            climber = parent[climber]
        return climber
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The stack traversal records one parent per node, and each upward walk touches one root path, so every node participates in constant work.

##### Space Complexity: `O(n)`

The `parent` map holds one entry per node, the `stack` can hold a level's worth of nodes, and `ancestors` holds one root path.

#### Key Insights

- Writing `parent[child]` at discovery time converts a downward-only tree into an upward-walkable structure for the price of one map.
- The explicit stack removes the recursion-depth hazard the recursive baseline carries; the pop order does not matter, only the parent relation does.
- Adding `p` itself to `ancestors` before climbing is what makes "a node is its own ancestor" hold without a special case.

### Stack Traversal with Depth Alignment

#### Derivation

[Stack Traversal with Parent Map](#stack-traversal-with-parent-map) spends a set on `p`'s entire ancestry even when the answer would be found after a few steps. Recording one more attribute during the same stack pass, the depth of every node, supports a different meeting rule borrowed from the classic technique for finding where two paths intersect: lift the deeper target up to the shallower target's depth, then advance both climbers in lockstep until they hold the same value. Equal-depth climbers that step together stay at equal depth, so the first value they share is the shallowest node on both root paths, which is the LCA:

1. Run the same stack pass as before, additionally recording
   `depth[child] = depth[node] + 1` at each discovery.
2. Name the deeper target's value `deeper_value` and the other
   `shallower_value`.
3. While `depth[deeper_value] > depth[shallower_value]`, step `deeper_value` to
   its parent.
4. While the two values differ, step both to their parents.
5. Return the shared value.

#### Walkthrough

Example 1: `p = 3`, `q = 8`. The stack pass leaves one depth entry per node:

```text
value   10  5   15  3   7   12  18  4   6   8
depth    0  1   1   2   2   2   2   3   3   3
```

`q = 8` sits one level below `p = 3`, so the lift runs first and the lockstep climb follows:

```text
lift      deeper_value = parent[8] = 7    depth 3 -> 2, depths now equal
lockstep  7 != 3 -> deeper_value = parent[7] = 5, shallower_value = parent[3] = 5
lockstep  5 == 5 -> return 5
```

Both climbers step into `5` on the same beat: `3` and `7` are children of `5`, the deepest node that is an ancestor of both targets. The result matches the expected Output.

#### Solution

The code is the same stack pass extended with `depth`, then the lift-and-lockstep climb.

```python
from collections import deque
from typing import Dict, List, Optional


class TreeNode:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


def build_tree(values: List[str]) -> TreeNode:
    root = TreeNode(int(values[0]))
    queue = deque([root])
    child_slot = 1
    while queue and child_slot < len(values):
        node = queue.popleft()
        left_entry = values[child_slot]
        child_slot += 1
        if left_entry != "null":
            node.left = TreeNode(int(left_entry))
            queue.append(node.left)
        if child_slot < len(values):
            right_entry = values[child_slot]
            child_slot += 1
            if right_entry != "null":
                node.right = TreeNode(int(right_entry))
                queue.append(node.right)
    return root


class Solution:
    def solve(self, root: List[str], p: int, q: int) -> int:
        tree = build_tree(root)

        parent: Dict[int, Optional[int]] = {tree.value: None}
        depth: Dict[int, int] = {tree.value: 0}
        stack: List[TreeNode] = [tree]
        while stack:
            node = stack.pop()
            if node.left:
                parent[node.left.value] = node.value
                depth[node.left.value] = depth[node.value] + 1
                stack.append(node.left)
            if node.right:
                parent[node.right.value] = node.value
                depth[node.right.value] = depth[node.value] + 1
                stack.append(node.right)

        deeper_value, shallower_value = (p, q) if depth[p] >= depth[q] else (q, p)
        while depth[deeper_value] > depth[shallower_value]:
            deeper_value = parent[deeper_value]
        while deeper_value != shallower_value:
            deeper_value = parent[deeper_value]
            shallower_value = parent[shallower_value]
        return deeper_value
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One stack pass builds both maps, and each climb step advances a value one level toward the root, so the total work stays linear.

##### Space Complexity: `O(n)`

The `parent` and `depth` maps hold one entry per node; the ancestor set of the previous approach is gone, replaced by the second map built during the same pass.

#### Key Insights

- Depth equalization before the lockstep climb is the whole trick: climbers at equal depth that step together can only meet at their LCA.
- The climb touches only the two node-to-root paths, so the memory moves from a full ancestor set to a second map recorded during the discovery pass.
- The same alignment pattern extends past this problem: the number of climb steps is the distance between the two nodes, and the pattern generalizes to k targets by repeated alignment.

## Comparison of Solutions

### Time Complexity

- **Find Root-to-Node Paths**: `O(n)` - two root-to-target searches plus a linear prefix comparison.
- **Stack Traversal with Parent Map**: `O(n)` - one stack pass records parents and two root-path climbs finish the job.
- **Stack Traversal with Depth Alignment**: `O(n)` - the same single pass with one extra attribute per node and two bounded climbs.

### Space Complexity

- **Find Root-to-Node Paths**: `O(n)` - two path lists plus a recursion stack that can reach depth `n` on a skewed tree.
- **Stack Traversal with Parent Map**: `O(n)` - the parent map, the explicit stack, and `p`'s ancestor set.
- **Stack Traversal with Depth Alignment**: `O(n)` - parent and depth maps plus the explicit stack, with no ancestor set.

### Trade-offs

- **Find Root-to-Node Paths**: the most direct expression of the definition, but it recurses (a recursion-limit risk at `10^5` nodes) and fails the interviewer's stack requirement.
- **Stack Traversal with Parent Map**: iterative and single-pass, and the ancestor-set climb narrates cleanly; the set stores `p`'s whole chain even when the answer sits near `p`.
- **Stack Traversal with Depth Alignment**: same asymptotics with the set traded for a depth map, and its lockstep climb is the pattern that carries over to distance queries and multi-target variants.

### When to Use Each

- **Stack Traversal with Parent Map (Recommended)**: the answer this interviewer asked for: iterative, one pass, and easy to explain aloud.
- **Find Root-to-Node Paths**: as the first spoken idea that sets up the parent-map refinement, or when recursion is allowed and clarity is the only goal.
- **Stack Traversal with Depth Alignment**: when a follow-up asks for the distance between the two nodes or pushes for a version without the ancestor set.

### Optimization Notes

- Stop the stack pass once both `p` and `q` have entries in the map: nothing below the deeper of the two targets can change the answer.
- In a real interview the tree arrives as `TreeNode` objects, so `build_tree` disappears and the stack pass starts directly at the given root.
- Node values are unique (`[-10^9, 10^9]`), which is why both maps key on values; with duplicates you would key on object identity instead.
