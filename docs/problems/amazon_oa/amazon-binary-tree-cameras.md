# [Binary Tree Cameras](https://www.fastprep.io/problems/amazon-binary-tree-cameras)

**Hard** | **NN minutes** | **Tree, Depth First Search, Dynamic Programming, Greedy**

You are given the root of a binary tree. You may install cameras on its nodes.

A camera installed at a node monitors that node, its parent if one exists, and its immediate children.

Return the minimum number of cameras needed so that every node in the tree is monitored.

## Examples

### Example 1

**Input:** `root = [0,0,null,0,0]`

**Output:** `1`

**Explanation:** Place one camera on the second node in the level-order representation. It monitors its parent, itself, and both of its children, so every node is covered.

### Example 2

**Input:** `root = [0,0,null,0,null,0,null,null,0]`

**Output:** `2`

**Explanation:** No single camera can monitor the entire chain-like tree. Two cameras placed at suitable internal nodes are sufficient.

### Example 3

**Input:** `root = [0]`

**Output:** `1`

**Explanation:** The only node must be monitored, so installing one camera on the root is optimal.

## Constraints

- `The tree contains between 1 and 1000 nodes.`
- `Every node has value 0.`

## Solutions

The solutions below assume the standard node definition and `from typing import Dict, List, Optional, Set, Tuple`:

```python
from typing import Optional


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: "Optional[TreeNode]" = None,
        right: "Optional[TreeNode]" = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right
```

### Brute Force

#### Derivation

The most literal reading of the sentence "return the minimum number of cameras" treats the placement as a search problem: some subset of the nodes carries cameras, every node must end up monitored, and among all subsets that achieve full coverage we want the smallest. With no structural insight yet, enumerate every subset and test each one for full coverage:

1. Walk the tree once to collect `node_list` and fill `parent_of`, the map from
   each node to its parent (the root maps to `None`), so a camera's reach can be
   checked without parent pointers on the nodes.
2. Iterate `mask` over every number from `0` to `2^n - 1`, where bit `position`
   set means the node at `node_list[position]` carries a camera; build
   `camera_set` from the bits.
3. `monitors_all(camera_set)` returns `True` when every node is monitored: a
   node is monitored when it, its parent, or one of its children sits in
   `camera_set`.
4. Track the smallest passing subset size in `best_count` and return it.

A camera on every node trivially works, so the search space always contains at least one passing subset and the loop finds the true minimum.

#### Walkthrough

Example 1, `root = [0,0,null,0,0]`, has four nodes. Naming them `A` (root), `B` (the left child), and `C`, `D` (the two leaves under `B`), the preorder collection builds `node_list = [A, B, C, D]`. The mask scan checks subsets in increasing numeric order:

```text
mask 0   camera_set = {}       no node is monitored              -> reject
mask 1   camera_set = {A}      camera on A covers A, B only;
                               C and D unmonitored               -> reject
mask 2   camera_set = {B}      camera on B covers B itself, its
                               parent A, and its children C, D   -> accept
```

Mask `2` passes with one camera, and no subset of size zero can pass, so `best_count = 1`: the single camera on `B` reaches all four nodes. The same scan on Example 3 (`root = [0]`) rejects the empty set and accepts `{root}` for `1`, matching the expected Output.

#### Solution

The code is the walkthrough's enumeration: collect nodes, test each bit mask's `camera_set` with `monitors_all`, keep the smallest passing size.

```python
from typing import Dict, List, Optional, Set


class Solution:
    def minCameraCover(self, root: Optional[TreeNode]) -> int:
        """Place the fewest cameras so every node is monitored.

        Time:  O(2^n * n): each of the 2^n subsets is checked against n nodes.
        Space: O(n) for the node list, parent map, and camera set.
        """
        node_list: List[TreeNode] = []
        parent_of: Dict[Optional[TreeNode], Optional[TreeNode]] = {}

        def collect(node: Optional[TreeNode], parent: Optional[TreeNode]) -> None:
            if node is None:
                return
            node_list.append(node)
            parent_of[node] = parent
            collect(node.left, node)
            collect(node.right, node)

        collect(root, None)
        total_nodes = len(node_list)

        def monitors_all(camera_set: Set[TreeNode]) -> bool:
            for node in node_list:
                monitored = (
                    node in camera_set
                    or parent_of[node] in camera_set
                    or (node.left is not None and node.left in camera_set)
                    or (node.right is not None and node.right in camera_set)
                )
                if not monitored:
                    return False
            return True

        best_count = total_nodes
        for mask in range(1 << total_nodes):
            camera_set = {
                node_list[position]
                for position in range(total_nodes)
                if mask & (1 << position)
            }
            if monitors_all(camera_set):
                best_count = min(best_count, len(camera_set))
        return best_count
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n × n)`

There are `2^n` subsets and each one is tested against every node with a constant number of membership checks, so the enumeration dominates everything else.

##### Space Complexity: `O(n)`

The node list, the parent map, and the largest `camera_set` each hold at most `n` entries.

#### Key Insights

- The coverage test is local: whether a node is monitored depends only on cameras at itself, its parent, and its children, which is what makes each subset check cheap.
- The parent map exists only because the brute force must test a camera's upward reach; the tree nodes themselves carry no parent pointer.
- Correct and complete, but `2^n` subsets cannot run on the allowed 1,000 nodes: the gap between "checks every placement" and "places them greedily" is what the next solutions close.

### Bottom-Up Status DP

#### Derivation

The brute force re-decides every placement combination from scratch because it never asks what a subtree contributes on its own. The bottom-up repair asks each subtree for a small report instead: how many cameras its coverage requires, broken down by the state of its root. Three states matter, because a parent's decision depends on exactly one fact per child: can this child's subtree already be trusted to cover its own root, or does the root still need help?

- `with_camera`: the subtree is fully monitored and this node carries a camera.
- `covered`: the subtree is fully monitored and this node has no camera, being
  watched by one of its children.
- `uncovered`: every node below is monitored, but this node itself is not yet
  watched and must be covered by its parent.

An absent child contributes `(inf, 0, 0)`: it cannot host a camera, and it imposes no coverage duty. Combining two child reports then follows the coverage rule:

1. `with_camera = 1 + left_cheapest + right_cheapest`: paying for this camera
   leaves each child free to take its cheapest of all three states.
2. `covered = min(left_with + right_stable, left_stable + right_with)`: exactly
   one child must carry a camera that watches this node, where `stable` is the
   cheapest of that child's two fully monitored states.
3. `uncovered = left_stable + right_stable`: both children must be fully
   monitored on their own, while this node waits for its parent.
4. The root has no parent, so the answer is `min(root_with, root_covered)`.

#### Walkthrough

Trace the reports on Example 1, `root = [0,0,null,0,0]`, with nodes `A` (root), `B` (left child), `C`, `D` (leaves under `B`). The recursion descends to the leaves first, and each line shows the `(with_camera, covered, uncovered)` triple the node returns:

```text
C (leaf)   children absent -> (1, inf, 0)   covered by a child impossible
D (leaf)   children absent -> (1, inf, 0)
B          left (1, inf, 0), right (1, inf, 0)
           with_camera = 1 + 0 + 0           = 1
           covered     = min(1+1, 1+1)       = 2
           uncovered   = 1 + 1               = 2
           -> (1, 2, 2)
A          left (1, 2, 2), right absent (inf, 0, 0)
           with_camera = 1 + 1 + 0           = 2
           covered     = min(1+0, 1+inf)     = 1
           uncovered   = 1 + 0               = 1
           -> (2, 1, 1)
```

The decisive line is `A`: a camera on the root would cost `2` in total, because under that placement `B` still has to cover its own subtree with its camera, while the `covered = 1` branch gets the root watched for free by `B`'s camera (`left_with + right_stable = 1 + 0`). The root has no parent to catch an `uncovered` report, so the answer reads `min(root_with, root_covered) = min(2, 1) = 1`, matching the expected Output. Example 3 (`root = [0]`) returns the leaf pattern `(1, inf, 0)` at the root, and `min(1, inf) = 1`.

#### Solution

The code is the walkthrough's report: one recursive function returning the three-state tuple, with the answer read from the root's two covered states.

```python
from typing import Optional, Tuple


class Solution:
    def minCameraCover(self, root: Optional[TreeNode]) -> int:
        """Place the fewest cameras so every node is monitored.

        Time:  O(n): each node is visited once and combines its children's
            triples with a constant number of sums and minimums.
        Space: O(h) recursion stack, h the tree height.
        """
        def cover_report(node: Optional[TreeNode]) -> Tuple[float, int, int]:
            if node is None:
                return (float("inf"), 0, 0)
            left_with, left_covered, left_uncovered = cover_report(node.left)
            right_with, right_covered, right_uncovered = cover_report(node.right)
            left_cheapest = min(left_with, left_covered, left_uncovered)
            right_cheapest = min(right_with, right_covered, right_uncovered)
            left_stable = min(left_with, left_covered)
            right_stable = min(right_with, right_covered)
            with_camera = 1 + left_cheapest + right_cheapest
            covered = min(left_with + right_stable, left_stable + right_with)
            uncovered = left_stable + right_stable
            return (with_camera, covered, uncovered)

        root_with, root_covered, _ = cover_report(root)
        return min(root_with, root_covered)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node is visited exactly once, and each visit merges its two child triples with a constant number of additions and minimums.

##### Space Complexity: `O(h)`

Only the recursion stack grows with the input, one frame per level, `h` the tree height; the reports themselves are returned, not stored.

#### Key Insights

- The three-state split encodes the whole camera rule: a parent must know whether a child's root is already watched, and `uncovered` is the state that says "place the camera here or above".
- The `inf` for an absent child does double duty: it forbids counting a camera on a node that does not exist (in `covered`) while contributing zero duty (in `with_camera` and `uncovered`).
- This DP is the systematic form of the greedy below: the greedy's local rule is what the DP proves sufficient, and the DP generalizes to coverage variants where the greedy rule breaks.

### Greedy Postorder Placement

#### Derivation

The DP proves a three-state summary suffices; the greedy compresses that insight into a placement rule that needs no minimums at all. Process the tree bottom-up and let each node look only at its two children's statuses: a leaf starts life needing coverage, a node whose child still needs coverage must carry the camera itself (there is nobody below left to do it), and otherwise a node with a camera among its children is already watched. Cameras land on the lowest possible parents, and each camera watches as many still-needy nodes as it can:

1. `place_from_bottom(node)` recurses postorder and returns one of the module
   constants `HAS_CAMERA`, `COVERED`, `NEEDS_COVER`; a `None` child returns
   `COVERED` because it neither needs help nor provides any.
2. When either child returns `NEEDS_COVER`, increment `camera_count` and return
   `HAS_CAMERA`: this node's camera watches that child, itself, and its parent.
3. Otherwise, when either child returns `HAS_CAMERA`, return `COVERED`.
4. Otherwise return `NEEDS_COVER`: only the parent can watch this node now.
5. After the recursion, the root has no parent, so a root that returned
   `NEEDS_COVER` gets one final camera.

#### Walkthrough

Example 2, `root = [0,0,null,0,null,0,null,null,0]`, is a leftward chain with one rightward tail: root `A` has left child `B`, `B` has left child `C`, `C` has left child `D`, and `D` has right child `E`:

```text
        A
       /
      B
     /
    C
   /
  D
   \
    E
```

The postorder visits `E`, `D`, `C`, `B`, `A`; each line shows the children's statuses and the decision:

```text
place(E)   leaf, no children            -> NEEDS_COVER
place(D)   right E NEEDS_COVER          -> camera_count = 1, return HAS_CAMERA
place(C)   left D HAS_CAMERA            -> COVERED
place(B)   left C COVERED, right absent -> NEEDS_COVER
place(A)   left B NEEDS_COVER           -> camera_count = 2, return HAS_CAMERA
root       A HAS_CAMERA                 -> no final camera needed
```

The camera on `D` covers `E`, `D`, and `C`; the camera on the root covers `A` and `B`. Every node ends monitored and the function returns `2`, matching the expected Output. Example 1 collapses to the shorter version of the same trace: both leaves under `B` need cover, so `B` takes the single camera and the already-covered root adds nothing, returning `1`; Example 3's lone node is a leaf whose `NEEDS_COVER` report triggers the final camera for `1`.

#### Solution

The code is the walkthrough's decision table, run postorder with the root fix as the last step.

```python
from typing import Optional

HAS_CAMERA, COVERED, NEEDS_COVER = 0, 1, 2


class Solution:
    def minCameraCover(self, root: Optional[TreeNode]) -> int:
        """Place the fewest cameras so every node is monitored.

        Time:  O(n): one postorder visit per node with constant work each.
        Space: O(h) recursion stack, h the tree height.
        """
        camera_count = 0

        def place_from_bottom(node: Optional[TreeNode]) -> int:
            nonlocal camera_count
            if node is None:
                return COVERED
            left_status = place_from_bottom(node.left)
            right_status = place_from_bottom(node.right)
            if left_status == NEEDS_COVER or right_status == NEEDS_COVER:
                camera_count += 1
                return HAS_CAMERA
            if left_status == HAS_CAMERA or right_status == HAS_CAMERA:
                return COVERED
            return NEEDS_COVER

        if place_from_bottom(root) == NEEDS_COVER:
            camera_count += 1
        return camera_count
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The postorder visit touches each node once, and every visit compares at most two child statuses before deciding.

##### Space Complexity: `O(h)`

The recursion stack holds one frame per level, `h` the tree height; no auxiliary structure grows with the node count.

#### Key Insights

- Placing each camera at the parent of a needy child is optimal because that camera covers three useful nodes at once: the child, itself, and its own parent; placing it on the leaf instead would cover two.
- Treating a `None` child as `COVERED` removes every presence check from the decision: leaves fall out of the same three-way rule as interior nodes.
- The greedy and the Bottom-Up Status DP agree on every input, but the greedy is where to start in an interview: five lines of decision, with the DP as the fallback when the coverage rule is stranger than "node, parent, children".

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(2^n × n)` - every subset of nodes is checked against every node for coverage.
- **Bottom-Up Status DP**: `O(n)` - one visit per node combining two child triples.
- **Greedy Postorder Placement**: `O(n)` - one postorder visit per node with constant decision work.

### Space Complexity

- **Brute Force**: `O(n)` - the node list, parent map, and camera set.
- **Bottom-Up Status DP**: `O(h)` - the recursion stack only; triples are returned, never stored.
- **Greedy Postorder Placement**: `O(h)` - the recursion stack only.

### Trade-offs

- **Brute Force**: answers any variant of the coverage question without structural insight, but exponential time confines it to toy trees.
- **Bottom-Up Status DP**: optimal and systematic, with the state definition making correctness arguable in an interview, at the cost of juggling three numbers per node.
- **Greedy Postorder Placement**: optimal with the smallest code and smallest constants, but its correctness is a claim about the coverage geometry rather than something the code itself exhibits.

### When to Use Each

- **Brute Force**: as the spoken baseline that pins down what "monitored" means, or when validating the fast solutions on tiny random trees.
- **Bottom-Up Status DP**: when the coverage rule is more complex than the standard one, or when the interviewer asks you to prove optimality from first principles.
- **Greedy Postorder Placement** (Recommended): the interview default: optimal, shortest to write, and easy to narrate leaf by leaf.

### Optimization Notes

- Both fast solutions are already linear; the remaining lever is recursion depth. A degenerate 1,000-node chain is 1,000 frames deep, at Python's default recursion limit, so an iterative postorder (explicit stack) is the production hardening for unbalanced inputs.
- The greedy's status constants double as the DP's states: `NEEDS_COVER` is `uncovered`, `HAS_CAMERA` is `with_camera`, and `COVERED` is `covered`; recognizing that mapping is what lets you derive the greedy from the DP instead of memorizing two algorithms.
- A common pitfall is forgetting the root fix: a root that reports `NEEDS_COVER` has no parent to catch it, so the final `camera_count += 1` is what keeps single-node and chain-shaped trees correct.
