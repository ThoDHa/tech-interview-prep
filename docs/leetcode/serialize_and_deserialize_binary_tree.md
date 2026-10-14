# [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/)

**Hard** | **45 minutes** | **Tree, Design, String, Binary Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Algorithm:** [Tree traversal](https://en.wikipedia.org/wiki/Tree_traversal) · [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) · [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)

**Practice:** [`practice/serialize_and_deserialize_binary_tree/solution.py`](../../practice/serialize_and_deserialize_binary_tree/solution.py)

Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

**Clarification:** The input/output format is the same as how LeetCode serializes a binary tree. You do not necessarily need to follow this format, so please be creative and come up with different approaches yourself.

## Examples

### Example 1

![Serialize and Deserialize Binary Tree Example 1](assets/serialize_and_deserialize_binary_tree_example1.jpg)

**Input:** `root = [1,2,3,null,null,4,5]`

**Output:** `[1,2,3,null,null,4,5]`

### Example 2

**Input:** `root = []`

**Output:** `[]`

## Constraints

- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-1000 <= Node.val <= 1000`

## Deriving the Solution

A codec must record two things: the node values and the tree's shape. A traversal order alone captures only the values, and that is not enough: distinct trees can produce the same value sequence (a chain of `1, 2` leaning left reads exactly like one leaning right). Writing an explicit `"null"` token for every absent child pins down the shape, and every solution below is that one idea executed in a different traversal.

1. **Start with values alone.** Emit the values in some traversal order and try
   to rebuild. The attempt fails: without shape information, deserialization cannot tell where one subtree ends and the next begins, so reconstruction is ambiguous.
2. **Mark the gaps.** Emit `"null"` wherever a child is missing. In preorder
   (root, left, right), each recursive call then consumes exactly one token and knows precisely when its subtree is complete, so the tree rebuilds uniquely: see [Preorder DFS with Null Markers](#preorder-dfs-with-null-markers).
3. **Trade recursion for a queue.** The preorder codec recurses to depth `O(h)`,
   and a skewed tree of `10^4` nodes overruns Python's default recursion limit. The same marker idea works level by level with an explicit queue, which also matches LeetCode's own representation: see [Level-Order BFS](#level-order-bfs).
4. **Flip the traversal.** The markers are traversal-agnostic: postorder (left,
   right, root) works too, with the root landing at the end of the string. The cost of the variety is a twist in deserialization: tokens are consumed from the end, which reverses the order and forces the right subtree to be built before the left: see [Postorder DFS with Null Markers](#postorder-dfs-with-null-markers).

## Solutions

### Preorder DFS with Null Markers

#### Derivation

Ask what the string must contain for the tree to rebuild without guesswork. A plain list of values is ambiguous, because different shapes share the same value sequence. The repair is to record shape explicitly: run a **[preorder traversal](https://en.wikipedia.org/wiki/Depth-first_search) (root → left → right)** and append a `"null"` marker wherever a child is missing. With the markers in place, the token stream is self-delimiting: reading it front to back, every token is either a node (whose two subtrees follow immediately) or a `"null"` (an empty subtree), so a recursive reader that consumes one token per call reconstructs the tree uniquely by following the same preorder pattern.

1. `serialize` runs `preorder(node)`: for a real node, append `str(node.val)` to
   `vals`, then recurse into `node.left` and `node.right`; for a missing node, append `"null"`. Join `vals` with commas.
2. `deserialize` splits the string on commas into the list `vals` and keeps a
   single shared cursor `index`, starting at `0`.
3. `build_tree` consumes one token per call: it reads `vals[index]`, advances
   `index` by one, and returns `None` for a `"null"`; otherwise it creates a `TreeNode`, then fills `node.left` and `node.right` with two recursive calls, in that order.

#### Walkthrough

Let us trace this first solution on Example 1, the tree `[1,2,3,null,null,4,5]`. Drawn out, that tree looks like this: `1` is the root, its children are `2` (left) and `3` (right), `2` is a leaf, and `3` has children `4` (left) and `5` (right).

**Serialization.** `preorder` visits each node root → left → right, appending `str(node.val)` for a real node and `"null"` for a missing child. Because the recursion fully finishes the left subtree before touching the right, the calls unfold like an indented call tree. Each line below shows the call and what it appends to `vals`:

```text
preorder(1)        append "1"        vals = [1]
  preorder(2)      append "2"        vals = [1, 2]
    preorder(None) append "null"     vals = [1, 2, null]          (2's left)
    preorder(None) append "null"     vals = [1, 2, null, null]    (2's right)
  preorder(3)      append "3"        vals = [1, 2, null, null, 3]
    preorder(4)    append "4"        vals = [1, 2, null, null, 3, 4]
      preorder(None) append "null"   vals = [..., 4, null]        (4's left)
      preorder(None) append "null"   vals = [..., 4, null, null]  (4's right)
    preorder(5)    append "5"        vals = [..., 5]
      preorder(None) append "null"   vals = [..., 5, null]        (5's left)
      preorder(None) append "null"   vals = [..., 5, null, null]  (5's right)
```

Joining `vals` with commas gives the serialized string: `1,2,null,null,3,4,null,null,5,null,null`.

**Deserialization.** `build_tree` reads tokens left to right through one shared cursor `index`. Each call consumes exactly one token (reads `vals[index]`, then bumps `index`): a `"null"` returns `None`, otherwise it makes a node and recursively fills its left child, then its right. The same call tree rebuilds, consuming tokens in this order:

| Call | `index` before | Token consumed | Result |
| --- | --- | --- | --- |
| `build_tree()` | 0 | `1` | node `1`, now build its children |
| `build_tree()` | 1 | `2` | node `2`, now build its children |
| `build_tree()` | 2 | `null` | `2.left = None` |
| `build_tree()` | 3 | `null` | `2.right = None`, node `2` complete |
| `build_tree()` | 4 | `3` | node `3`, now build its children |
| `build_tree()` | 5 | `4` | node `4`, now build its children |
| `build_tree()` | 6 | `null` | `4.left = None` |
| `build_tree()` | 7 | `null` | `4.right = None`, node `4` complete |
| `build_tree()` | 8 | `5` | node `5`, now build its children |
| `build_tree()` | 9 | `null` | `5.left = None` |
| `build_tree()` | 10 | `null` | `5.right = None`, node `5` complete |

`index` ends at `11`, the length of `vals`: every token was consumed exactly once.

The returned tree is exactly `[1,2,3,null,null,4,5]`, which matches the expected Output for Example 1.

#### Solution

The code is the two traces written down: `preorder` emits the token stream, and `build_tree` consumes it one token per call.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import Optional


class Codec:
    def serialize(self, root: Optional["TreeNode"]) -> str:
        """Encodes a tree to a single string using preorder traversal"""
        def preorder(node: Optional["TreeNode"]) -> None:
            if not node:
                vals.append("null")
            else:
                vals.append(str(node.val))
                preorder(node.left)
                preorder(node.right)

        vals = []
        preorder(root)
        return ','.join(vals)

    def deserialize(self, data: str) -> Optional["TreeNode"]:
        """Decodes string back to tree using preorder reconstruction"""
        def build_tree() -> Optional["TreeNode"]:
            nonlocal index
            val = vals[index]
            index += 1
            if val == "null":
                return None

            node = TreeNode(int(val))
            node.left = build_tree()
            node.right = build_tree()
            return node

        vals = data.split(',')
        index = 0
        return build_tree()
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)` for both operations

Serialization visits each node once, deserialization processes each serialized value once.

##### Space Complexity: `O(n)` output, `O(h)` auxiliary

The serialized string (and the token list split from it) holds all `n` values plus null markers, so the output is `O(n)` in both directions. Beyond that output, both serialization and deserialization use only a recursion stack proportional to the tree height.

#### Key Insights

- Preorder traversal with explicit null markers captures both the values and the shape of the tree, so the original structure can be reconstructed uniquely without a second traversal.
- Deserialization consumes tokens through a single shared cursor `index`, so each recursive call advances it exactly once and the left subtree is fully built before the right.
- Null markers are mandatory for a general binary tree; without them, distinct trees can produce the same value sequence and become indistinguishable.

### Level-Order BFS

#### Derivation

The preorder codec recurses to a depth equal to the tree height, and with up to `10^4` nodes a skewed tree overruns Python's default recursion limit. The repair is to keep the null-marker idea but drive it with an explicit queue instead of the call stack: **[level-order traversal (BFS)](https://en.wikipedia.org/wiki/Breadth-first_search)** processes nodes level by level from left to right, which is also the way trees are usually drawn and the format LeetCode itself uses. The token stream pairs naturally with a queue in both directions: serialization emits two tokens (its children) for every real node it dequeues, so deserialization can dequeue one built node at a time and hand it the next two tokens as its children.

1. `serialize` seeds `queue` with `root` (returning `""` for an empty tree). It
   repeatedly pops a node: for a real node it appends `str(node.val)` to `result` and enqueues both children, `None` included; for a `None` it appends `"null"`. Join `result` with commas.
2. `deserialize` returns `None` for empty `data`, otherwise splits it into
   `values`, builds `root` from `values[0]`, and seeds `queue` with it. The cursor `index` starts at `1`.
3. Each dequeued `node` takes `values[index]` as its left child and
   `values[index + 1]` as its right, advancing `index` past both. A non-`"null"` token becomes a `TreeNode` that is also enqueued to receive its own children later; a `"null"` leaves the child as `None`.

#### Walkthrough

Let us trace the codec on Example 1, the tree `[1,2,3,null,null,4,5]`:

```text
        1
       / \
      2   3
         / \
        4   5
```

**Serialization.** Each event pops the front of `queue`. A real node emits its value and enqueues both children (including `None`s); a `None` emits `"null"` and enqueues nothing:

```text
pop 1      emit "1"      enqueue 2, 3          queue = [2, 3]
pop 2      emit "2"      enqueue None, None    queue = [3, None, None]
pop 3      emit "3"      enqueue 4, 5          queue = [None, None, 4, 5]
pop None   emit "null"                         queue = [None, 4, 5]
pop None   emit "null"                         queue = [4, 5]
pop 4      emit "4"      enqueue None, None    queue = [5, None, None]
pop 5      emit "5"      enqueue None, None    queue = [None, None, None, None]
pop None   emit "null"   four times            queue empties
```

Joining `result` gives `1,2,3,null,null,4,5,null,null,null,null`: the tree read off level by level, exactly as LeetCode prints it (plus trailing markers).

**Deserialization.** `values` holds the eleven tokens above. `root` is built from `values[0] = "1"` and enqueued; `index` starts at `1`. Each dequeued node claims the next two tokens as its children:

```text
dequeue 1   values[1] = "2"     1.left  = node 2, enqueue    index -> 2
            values[2] = "3"     1.right = node 3, enqueue    index -> 3
dequeue 2   values[3] = "null"  2.left  = None               index -> 4
            values[4] = "null"  2.right = None               index -> 5
dequeue 3   values[5] = "4"     3.left  = node 4, enqueue    index -> 6
            values[6] = "5"     3.right = node 5, enqueue    index -> 7
dequeue 4   values[7], values[8] = "null"   leaf             index -> 9
dequeue 5   values[9], values[10] = "null"  leaf             index -> 11
```

`index` reaches `len(values)`, the loop ends, and `root` heads the rebuilt tree `[1,2,3,null,null,4,5]`, matching the expected Output for Example 1.

#### Solution

The code is the queue discipline from the walkthrough: emit two child tokens per dequeued node going out, claim two child tokens per dequeued node coming back.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from collections import deque
from typing import Optional

class Codec:
    def serialize(self, root: Optional["TreeNode"]) -> str:
        """Encodes tree using level-order traversal (BFS)"""
        if not root:
            return ""

        queue = deque([root])
        result = []

        while queue:
            node = queue.popleft()
            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append("null")

        return ','.join(result)

    def deserialize(self, data: str) -> Optional["TreeNode"]:
        """Decodes string back to tree using level-order reconstruction"""
        if not data:
            return None

        values = data.split(',')
        root = TreeNode(int(values[0]))
        queue = deque([root])
        index = 1

        while queue and index < len(values):
            node = queue.popleft()

            # Process left child
            if values[index] != "null":
                node.left = TreeNode(int(values[index]))
                queue.append(node.left)
            index += 1

            # Process right child
            if index < len(values) and values[index] != "null":
                node.right = TreeNode(int(values[index]))
                queue.append(node.right)
            index += 1

        return root
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)` for both operations

Each node is processed exactly once in both serialization and deserialization.

##### Space Complexity: `O(n)` output, `O(w)` auxiliary

The serialized string and the split token list hold all `n` values plus null markers, the same `O(n)` output the DFS approaches produce. The auxiliary structure is the queue, which holds at most the widest level of the tree (`w` nodes).

#### Key Insights

- A breadth-first ordering matches LeetCode's own level-order representation, making the serialized string easy to read and reason about.
- Reconstruction pairs each dequeued node with the next two tokens as its children, so an explicit queue replaces the recursion used by the DFS approaches.
- Using an iterative queue avoids deep recursion, so very deep or skewed trees will not overflow the call stack.

### Postorder DFS with Null Markers

#### Derivation

The preorder codec writes the root first. Ask whether the null-marker idea depends on that choice: it does not. **[Postorder traversal](https://en.wikipedia.org/wiki/Tree_traversal) (left → right → root)** writes the root last, so the root token sits at the very end of the serialized string. Reading front to back would no longer work, since the reader would not know a subtree's root until after consuming it, but reading from the **end** does: consumed backward, the stream presents root → right → left, a mirror of the preorder discipline. The one twist that reversal forces is that the right subtree must be built before the left. The null markers again tell the recursion exactly where each subtree ends, so any general binary tree reconstructs uniquely.

1. `serialize` runs `postorder(node)`: recurse into `node.left`, then
   `node.right`, then append `str(node.val)` to `vals`; append `"null"` for a missing node. Join `vals` with commas.
2. `deserialize` splits the string into the list `vals` and consumes it from
   the back with `vals.pop()`.
3. `build_tree` pops one token per call: a `"null"` returns `None`; otherwise
   it creates a `TreeNode`, builds `node.right` first, then `node.left`, and returns the node.

#### Walkthrough

Let us trace the codec on Example 1, the tree `[1,2,3,null,null,4,5]`:

```text
        1
       / \
      2   3
         / \
        4   5
```

**Serialization.** `postorder` finishes both subtrees before appending the node itself, so values surface bottom-up. The calls unfold as an indented call tree, each line showing what it appends to `vals`:

```text
postorder(1)
  postorder(2)
    postorder(None)   append "null"   vals = [null]                    (2's left)
    postorder(None)   append "null"   vals = [null, null]              (2's right)
                      append "2"      vals = [null, null, 2]
  postorder(3)
    postorder(4)
      postorder(None) append "null"   vals = [null, null, 2, null]     (4's left)
      postorder(None) append "null"   vals = [null, null, 2, null, null]
                      append "4"      vals = [..., 4]
    postorder(5)
      postorder(None) append "null"   vals = [..., 4, null]            (5's left)
      postorder(None) append "null"   vals = [..., 4, null, null]
                      append "5"      vals = [..., 5]
                      append "3"      vals = [..., 5, 3]
                      append "1"      vals = [..., 5, 3, 1]
```

Joining `vals` gives `null,null,2,null,null,4,null,null,5,3,1`: the root `1` is the last token, exactly as the derivation predicted.

**Deserialization.** `build_tree` pops from the end of `vals`, so tokens arrive in the order `1, 3, 5, null, null, 4, null, null, 2, null, null`: root first, then the right subtree, then the left. Each call pops one token and builds `node.right` before `node.left`:

```text
pop "1"        node 1, build its right subtree first
  pop "3"      node 3, build its right subtree first
    pop "5"    node 5
      pop "null"    5.right = None
      pop "null"    5.left  = None, node 5 complete
    pop "4"    node 4
      pop "null"    4.right = None
      pop "null"    4.left  = None, node 4 complete
  pop "2"      node 2
    pop "null"      2.right = None
    pop "null"      2.left  = None, node 2 complete
```

Node `1` receives `3` as its right child and `2` as its left, and `3` receives `5` on the right and `4` on the left: the rebuilt tree is `[1,2,3,null,null,4,5]`, matching the expected Output for Example 1.

#### Solution

The code is the two traces written down: `postorder` emits bottom-up, and `build_tree` pops from the end, right subtree before left.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import Optional


class Codec:
    def serialize(self, root: Optional["TreeNode"]) -> str:
        """Encodes a tree to a single string using postorder traversal"""
        def postorder(node: Optional["TreeNode"]) -> None:
            if not node:
                vals.append("null")
            else:
                postorder(node.left)
                postorder(node.right)
                vals.append(str(node.val))

        vals = []
        postorder(root)
        return ','.join(vals)

    def deserialize(self, data: str) -> Optional["TreeNode"]:
        """Decodes string back to tree by consuming postorder from the end"""
        def build_tree() -> Optional["TreeNode"]:
            val = vals.pop()
            if val == "null":
                return None

            node = TreeNode(int(val))
            # Postorder is left, right, root; consumed from the end the
            # order reverses, so build the right subtree before the left
            node.right = build_tree()
            node.left = build_tree()
            return node

        vals = data.split(',')
        return build_tree()
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)` for both operations

Serialization visits each node once, deserialization processes each serialized value once.

##### Space Complexity: `O(n)` output, `O(h)` auxiliary

The serialized string and token list hold all `n` values plus null markers, so the output is `O(n)` in both directions. Beyond the output, deserialization uses a recursion stack proportional to tree height.

#### Key Insights

- Writing the root last places its token at the end of the string, so deserialization reads the token list from the back, which reverses the traversal to root then right then left.
- Because the order reverses, the right subtree must be built before the left; swapping them is the most common implementation mistake here.
- The same null-marker technique that works for preorder also works for postorder, demonstrating that the choice of traversal is flexible as long as boundaries are marked.

## Comparison of Solutions

### Time Complexity

- **Preorder DFS with Null Markers**: `O(n)` - Linear time for both operations
- **Level-Order BFS**: `O(n)` - Linear time with queue operations
- **Postorder DFS with Null Markers**: `O(n)` - Linear time for both operations

### Space Complexity

- **Preorder DFS with Null Markers**: `O(n)` serialized output, `O(h)` auxiliary recursion stack
- **Level-Order BFS**: `O(n)` serialized output, `O(w)` auxiliary queue, where w is maximum tree width
- **Postorder DFS with Null Markers**: `O(n)` serialized output, `O(h)` auxiliary recursion stack

### Trade-offs

- **Preorder DFS with Null Markers**: Implementation complexity is medium with good intuitive understanding. The serialized size is larger because it includes null markers, but reconstruction uses simple recursive logic that is stack-based during reconstruction and easy to debug.
- **Level-Order BFS**: Implementation complexity is medium with excellent intuitive understanding, matching how trees are commonly visualized. The serialized size is larger because it includes null markers, reconstruction is queue-based iterative logic, memory during reconstruction is queue-based, and it is easy to debug.
- **Postorder DFS with Null Markers**: Implementation complexity is medium. The serialized size is comparable to the preorder approach since it also stores null markers. The one subtlety is that deserialization consumes tokens from the end of the list and builds the right subtree before the left, which is easy to get wrong but straightforward once understood.

### When to Use Each

- **Preorder DFS with Null Markers**: Best general-purpose solution for interviews and production, with a good balance of simplicity and efficiency
- **Level-Order BFS**: When you want intuitive level-by-level processing or when working with very deep trees (avoids deep recursion)
- **Postorder DFS with Null Markers**: When you want a bottom-up traversal, or to demonstrate that the same null-marker technique works in postorder by reading the token list from the end

### Optimization Notes

- The **Preorder DFS with Null Markers** solution is the recommended choice for interviews and production: preorder traversal with null placeholders provides sufficient information for unique reconstruction without requiring an inorder traversal, and the recursive reconstruction is simple to implement and debug.
- Key implementation detail: serialization and deserialization must follow the same preorder order (root, then left, then right), and the null markers are what allow the recursive `build_tree` to know exactly where each subtree ends.
- The **Level-Order BFS** trades recursion (stack space) for an explicit queue (heap space) and avoids deep recursion, making it the better choice for very deep trees that could otherwise overflow the call stack.
- The **Postorder DFS with Null Markers** solution shows the same null-marker idea applied bottom-up. Because the root is serialized last, deserialization must consume the token list from the end and build the right subtree before the left. A tempting but incorrect shortcut is to drop the null markers and reconstruct using BST-style value bounds (`min < val < max`); that only works for binary search trees and silently misplaces nodes in a general binary tree, so explicit null markers are required for correctness here.
- Common pitfall: forgetting that postorder deserialization reverses direction (right before left) when reading from the end. Corner cases such as empty trees, single nodes, and highly unbalanced trees must be tested for each approach.
