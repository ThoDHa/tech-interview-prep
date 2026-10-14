# [Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/)

**Easy** | **15 minutes** | **Tree, Depth-First Search, String Matching, Binary Tree, Hash Function**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Algorithm:** [Tree traversal](https://en.wikipedia.org/wiki/Tree_traversal) · [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) · [Hash function](https://en.wikipedia.org/wiki/Hash_function) · [String-searching algorithm](https://en.wikipedia.org/wiki/String-searching_algorithm)

**Practice:** [`practice/subtree_of_another_tree/solution.py`](../../practice/subtree_of_another_tree/solution.py)

Given the roots of two binary trees `root` and `subRoot`, return `true` if there is a subtree of `root` with the same structure and node values of `subRoot` and `false` otherwise.

A subtree of a binary tree `tree` is a tree that consists of a node in `tree` and all of this node's descendants. The tree `tree` could also be considered as a subtree of itself.

## Examples

### Example 1

**Input:** `root = [1,2,3,4,5], subRoot = [2,4,5]`

**Output:** `true`

### Example 2

**Input:** `root = [1,2,3,4,5,null,null,6], subRoot = [2,4,5]`

**Output:** `false`

## Constraints

- The number of nodes in the `root` tree is in the range `[1, 2000]`.
- The number of nodes in the `subRoot` tree is in the range `[1, 1000]`.
- `-10^4 <= root.val <= 10^4`
- `-10^4 <= subRoot.val <= 10^4`

## Deriving the Solution

A subtree is fully determined by the node it hangs from, so the question "is `subRoot` hiding anywhere inside `root`?" decomposes into one same-tree question per anchor node of `root`. Every solution answers those per-anchor questions; the family differs in how much of that work is redone.

1. **Start literal.** Walk `root` and run a full two-tree equality check at
   every node, stopping at the first match. Correct, but each anchor redoes
   an `O(m)` comparison: see
   [Same-Tree Check at Every Node](#same-tree-check-at-every-node).
2. **Fingerprint instead of re-comparing.** Record every root subtree's
   serialization in a set exactly once, and the anchor question collapses
   into a set membership test. The serialization must encode structure with
   null markers and keep tokens separated, or a `12` masquerades as a `2`:
   see [Subtree Serialization Set](#subtree-serialization-set).
3. **Linearize and let text search finish.** A lossless serialization makes
   subtree containment a substring containment question, which the standard
   library answers with an optimized scan: see
   [Serialization and Substring Search](#serialization-and-substring-search).

## Solutions

### Same-Tree Check at Every Node

#### Derivation

The most direct reading pairs the two problems: [Same Tree](same_tree.md) already answers "are these two trees identical?", and this problem only adds a scan for the right place to ask. Each node of `root` is an anchor candidate; at each one, run the same-tree check between the anchor's subtree and `subRoot`:

1. Reuse the same-tree check as a helper: both `None` is a match, exactly
   one `None` or differing values is not, otherwise recurse on both child
   pairs.
2. Walk the anchors with an explicit stack seeded on `root`.
3. Pop an anchor and run the helper; on a match return `True` immediately.
4. Push the children of any surviving anchor and continue.
5. An emptied stack means no anchor matched: return `False`.

#### Walkthrough

Trace the anchor scan on Example 1: `root = [1,2,3,4,5]`, `subRoot = [2,4,5]`:

```text
root:          subRoot:
      1              2
     / \            / \
    2   3          4   5
   / \
  4   5

stack: [1]
pop 1:  is_same(node 1, subRoot): 1 != 2 -> False
        push 2, push 3                 stack: [2, 3]
pop 3:  is_same(node 3, subRoot): 3 != 2 -> False
        no children to push            stack: [2]
pop 2:  is_same(node 2, subRoot): 2 == 2 -> recurse
        left pair  (4, 4): equal, both leaves -> True
        right pair (5, 5): equal, both leaves -> True
        -> True, return True
```

The first two anchors fail on the value check alone, and the third matches all the way down, returning `True`, matching the expected Output for Example 1. A failing anchor that is worth noticing lives in Example 2: the anchor at node `2` has children `4` and `5` like `subRoot`, but the left pair is `(4, 6-laden 4)`, and the check's one-sided `None` guard fires when `subRoot`'s `4` has no left child, so that anchor correctly fails.

#### Solution

The code is the same-tree helper plus the anchor stack.

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


class Solution:
    def isSubtree(self, root: TreeNode, subRoot: TreeNode) -> bool:
        def is_same(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
            if a is None and b is None:
                return True
            if a is None or b is None or a.val != b.val:
                return False
            return is_same(a.left, b.left) and is_same(a.right, b.right)

        stack = [root]
        while stack:
            node = stack.pop()
            if is_same(node, subRoot):
                return True
            if node.left is not None:
                stack.append(node.left)
            if node.right is not None:
                stack.append(node.right)
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * m)`

Each of the `n` anchors runs a check that costs `O(m)` in the worst case, where `m` is `subRoot`'s size; early mismatches usually cost less.

##### Space Complexity: `O(h)`

The anchor stack holds one root-to-leaf frontier of `root` (`O(h_root)`), and the equality check's recursion adds at most `subRoot`'s height on top.

#### Key Insights

- The problem is two familiar problems glued together: a linear anchor scan
  plus an unchanged same-tree check at each anchor.
- The one-sided `None` guard is what rejects structural near-misses such as
  Example 2's node `2`, where every value of `subRoot` appears but the
  shapes differ.
- The anchor scan never backtracks: once an anchor fails, its subtree
  contributes nothing further, which is exactly the wasted work the later
  solutions attack.

### Subtree Serialization Set

#### Derivation

The anchor scan re-derives each subtree's shape at every anchor, even though each node's subtree is fixed. A fingerprint computed once per node removes the recomputation: serialize each subtree into a string that encodes both values and structure, collect the strings in a set while composing them bottom-up, and finish with a single set membership test for `subRoot`'s serialization:

1. Serialize a `None` as the null marker `,#`.
2. Serialize a node as its value with a leading comma, followed by the left
   serialization, then the right.
3. Walk `root` bottom-up, recording every subtree's serialization in `serials`.
4. Serialize `subRoot` the same way and test membership in `serials`.

Two details make the encoding lossless. The null marker is what separates "leaf" from "node with missing children", so equal values in different shapes serialize differently. And every token carries its own leading comma, because a bare `12` contains the text `2`: the delimiters, not the values, are where one token ends and the next begins.

#### Walkthrough

Trace the set build on Example 2: `root = [1,2,3,4,5,null,null,6]`, `subRoot = [2,4,5]`:

```text
root:                 subRoot:
        1                   2
       / \                 / \
      2   3               4   5
     / \
    4   5
   /
  6

node 6 -> ",6,#,#"
node 4 -> ",4,6,#,#,#"            (6 hangs left)
node 5 -> ",5,#,#"
node 2 -> ",2,4,6,#,#,#,5,#,#"    (the candidate anchor)
node 3 -> ",3,#,#"
node 1 -> ",1,2,4,6,#,#,#,5,#,#,3,#,#"

subRoot  -> ",2,4,#,#,5,#,#"
membership: not in serials -> False
```

Every subtree serial is recorded exactly once as it is composed. `subRoot`'s serial differs from the node-`2` record at the third token: `subRoot` expects `#` there (its `4` is a leaf's parent with no grandchild), while the record holds `6`, so the membership test fails, matching the expected Output for Example 2. On Example 1 the node-`2` record is exactly `,2,4,#,#,5,#,#`, which the set contains, matching the expected Output for Example 1.

#### Solution

The code is the serializer, the bottom-up collector, and the one membership test.

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


class Solution:
    def isSubtree(self, root: TreeNode, subRoot: TreeNode) -> bool:
        def serialize(node: Optional[TreeNode]) -> str:
            if node is None:
                return ",#"
            return f",{node.val}" + serialize(node.left) + serialize(node.right)

        serials = set()

        def collect(node: Optional[TreeNode]) -> str:
            if node is None:
                return ",#"
            serial = f",{node.val}" + collect(node.left) + collect(node.right)
            serials.add(serial)
            return serial

        collect(root)
        return serialize(subRoot) in serials
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * h_root + m * h_sub)`

Each node's serialization string costs its own subtree's length to compose, so building every root serial costs the sum of all subtree sizes, `O(n * h_root)` in a worst-case skewed tree, plus `O(m * h_sub)` for `subRoot`'s; the membership test compares one string against the set.

##### Space Complexity: `O(n * h_root)`

The set stores every subtree's serialization, and those lengths sum to the same bound as the build cost. The recursion depth is the tree's height: with `n` up to `2000`, a skewed chain exceeds Python's default recursion limit, so raise the limit or drive the serialization with an explicit stack on degenerate inputs.

#### Key Insights

- A serialization with null markers is a lossless fingerprint: two subtrees
  serialize equally exactly when they are the same tree.
- Leading commas per token are not decoration: without them, a `12` node's
  serialization contains the `2` node's serialization, and the set would
  report matches that do not exist.
- Composing hash signatures instead of strings (a node's signature hashes
  its value and its children's signatures) cuts the cost to `O(n)` total,
  trading the string bookkeeping for a theoretical hash-collision risk.

### Serialization and Substring Search

#### Derivation

The set version fingerprints every root subtree separately, but a preorder serialization has a stronger property: each subtree's serialization is a contiguous slice of the whole tree's serialization, and because every subtree serial is self-delimiting (its null markers say where it ends), `subRoot` matches some subtree of `root` exactly when `subRoot`'s serialization appears as a substring of `root`'s. The whole problem becomes text search over two strings, and text search is what the standard library does best:

1. Serialize `root` to `root_serial` and `subRoot` to `sub_serial`, with the
   leading-comma token format that keeps token boundaries visible.
2. Return whether `sub_serial` is a substring of `root_serial`, delegating
   the scan to `in`.

The same leading-comma discipline matters even more here: the substring scan will start a match anywhere the bytes allow, so a delimiter-free encoding produces false positives (a `12` substring matching a `2` query) while the delimited encoding cannot.

#### Walkthrough

Trace the two serializations on Example 2: `root = [1,2,3,4,5,null,null,6]`, `subRoot = [2,4,5]`:

```text
root_serial = ",1,2,4,6,#,#,#,5,#,#,3,#,#"
sub_serial  = ",2,4,#,#,5,#,#"

scan: no position of root_serial starts a match for sub_serial
      (the only ",2," occurrence is followed by ",4,6", not ",4,#")
-> False
```

The candidate position fails at the token after `,4`: `root_serial` holds `6` where `sub_serial` demands `#`, so no substring match exists, matching the expected Output for Example 2. On Example 1 the root serializes to `,1,2,4,#,#,5,#,#,3,#,#`, which contains `,2,4,#,#,5,#,#` starting at its second token, matching the expected Output for Example 1.

#### Solution

The code is the two serializations and one `in`.

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


class Solution:
    def isSubtree(self, root: TreeNode, subRoot: TreeNode) -> bool:
        def serialize(node: Optional[TreeNode]) -> str:
            if node is None:
                return ",#"
            return f",{node.val}" + serialize(node.left) + serialize(node.right)

        return serialize(subRoot) in serialize(root)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * h_root + m * h_sub)` to serialize, plus the delegated scan

The serialization cost matches the set version's analysis. The containment scan is handed to the standard library, whose implementation is heavily optimized; the same scan written by hand (an anchor at every position of `root_serial`, comparing forward) is the classic `O(n * m)` worst case, and this delegation is the entire difference from writing that loop out.

##### Space Complexity: `O(n + m)`

Two serializations: one token per node plus one per missing child. The serializer recurses one frame per level, so the same skewed-chain caveat applies: a 2000-node `root` exceeds Python's default recursion limit.

#### Key Insights

- Self-delimiting serializations turn tree containment into substring
  containment: a match can only start at a genuine node token and can only
  end at a genuine subtree boundary.
- The stdlib `in` is the tidied form of the hand-rolled anchor loop; the
  insight it relies on (the lossless linear form) is derived above it.
- Memory drops from the set version's stored collection to just the two
  serializations, because the whole tree is linearized once instead of once
  per node.

## Comparison of Solutions

The practice harness's `practice/subtree_of_another_tree/reference.py` implements the **Subtree Serialization Set** solution.

### Time Complexity

- **Same-Tree Check at Every Node**: `O(n * m)` - an `O(m)` comparison at each of `n` anchors.
- **Subtree Serialization Set**: `O(n * h_root + m * h_sub)` - one serialization per subtree, composed bottom-up.
- **Serialization and Substring Search**: `O(n * h_root + m * h_sub)` plus the delegated scan - two serializations and a stdlib text search.

### Space Complexity

- **Same-Tree Check at Every Node**: `O(h)` - anchor stack plus the check's recursion.
- **Subtree Serialization Set**: `O(n * h_root)` - every subtree's serialization stored.
- **Serialization and Substring Search**: `O(n + m)` - the two serialized strings.

### Trade-offs

- The anchor scan spends no extra memory and is the easiest to argue, but
  re-compares overlapping subtrees at every anchor.
- The set version computes each subtree's fingerprint once and answers by
  hashing, paying memory proportional to the total serialization length.
- The substring version linearizes once and lets optimized library code
  finish, the least code and the least memory above the serializations, at
  the cost of trusting the encoding discipline.

### When to Use Each

- **Same-Tree Check at Every Node**: The interview default: it composes two
  problems you already know and needs no encoding tricks (recommended here).
- **Subtree Serialization Set**: When `root` is queried against many
  different `subRoot`s, the set amortizes across queries.
- **Serialization and Substring Search**: When the shortest correct code
  wins and the serialization format is under your control.

### Optimization Notes

- All three depend on the anchor or token boundaries being explicit: the
  one-sided `None` guard in the check, the null markers and leading commas
  in the serializations.
- The set version's cost concentrates in string composition; replacing
  strings with hash signatures (Merkle style) is the standard route to a
  true `O(n)`, with collision risk as the price.
- The constraints are small (`n <= 2000`), so even the `O(n * m)` anchor
  scan is comfortably fast; the serializations matter for the idea and for
  scaled-up inputs.
