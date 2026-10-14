# Data Structures in Pictures

A data structure is a way of organizing data so that certain operations are cheap. Choosing the right one is often most of the solution. This guide introduces the structures used throughout the problems, in plain terms, with a note on what each one is good at and which pattern guide develops it.

## Array (list)

A row of boxes laid side by side, each holding a value, numbered from `0`.

```text
index:   0    1    2    3    4
value: [ 7 ][ 3 ][ 9 ][ 2 ][ 5 ]
```

- **Reading box `i`**: instant, `O(1)`. You jump straight to it by its number.
- **Scanning for a value**: `O(n)`. You may have to look at every box.
- **Inserting or removing in the middle**: `O(n)`, because everything after it
  has to shift over.

A few Python-specific costs worth memorizing:

- `list.append` is amortized `O(1)`, so growing a list at the end is cheap.
- `list.pop(0)` is `O(n)`, because every remaining element shifts left. When
  you need to remove from the front, use `collections.deque` instead.
- Building a string with repeated `+` in a loop is `O(n²)`, because strings
  are immutable and each `+` copies everything built so far. Collect the pieces in a list and finish with `"".join(parts)`.

Arrays are the default container and the backbone of the [two pointers](../patterns/two_pointers/intuition.md), [sliding window](../patterns/sliding_window/intuition.md), and [prefix sum](../patterns/prefix_sum/intuition.md) patterns.

## Hash map (dictionary) and hash set

A hash map stores **key to value** pairs and finds any key almost instantly. A hash set is the same idea but stores only keys, answering "have I seen this?"

```text
"alice" -> 30
"bob"   -> 25
```

- **Look up, insert, or check membership by key**: `O(1)` on average.
- **No order**: you cannot ask for "the third item"; you ask about specific
  keys.

This is the single most useful structure for interviews, because it turns a repeated `O(n)` search into an `O(1)` lookup. The entire [Hashing pattern](../patterns/hashing/intuition.md) is built on it, and [Two Sum](../leetcode/two_sum.md) is the canonical first use.

## Stack

A pile where you only ever touch the top: **last in, first out**. Think of a stack of plates.

```text
push 3, push 7, push 2:
   top -> [ 2 ]
          [ 7 ]
          [ 3 ]
pop returns 2, then 7, then 3
```

- **Push (add to top) and pop (remove from top)**: `O(1)`.
- Useful whenever the most recent thing must be handled first: matching
  brackets, undoing, and evaluating expressions.

See the [Stack pattern](../patterns/stack/intuition.md) and [Monotonic Stack](../patterns/monotonic_stack/intuition.md).

## Queue

A line where you join the back and leave the front: **first in, first out**. Think of a checkout line.

```text
enqueue 3, enqueue 7, enqueue 2:
front -> [ 3 ][ 7 ][ 2 ] <- back
dequeue returns 3, then 7, then 2
```

- **Enqueue (add to back) and dequeue (remove from front)**: `O(1)` when you
  use the right structure (`collections.deque` in Python, not a plain list).
- The engine of breadth-first search, which explores a graph or grid level by
  level. See [Multi-Source BFS](../patterns/grid_bfs_multi_source/intuition.md).

## Linked list

A chain of nodes, where each node holds a value and a pointer to the next node. There is no index; you follow the chain from the head.

```text
head -> [1|*] -> [2|*] -> [3|*] -> None
```

- **Inserting or removing a node** when you already hold it: `O(1)`, just
  re-point the arrows.
- **Finding the `i`-th node**: `O(n)`, you must walk the chain.
- The price of cheap splicing is that you lose instant indexing.

The trick to most linked-list problems is careful pointer rewiring, often with two pointers moving at different speeds. See [Linked List Reversal](../patterns/linked_list_in_place_reversal/intuition.md).

## Tree

Nodes connected top-down with no cycles. One **root** at the top, each node holding pointers to its children. A **binary tree** has at most two children per node (left and right).

```text
        4
       / \
      2   7
     / \
    1   3
```

- Every child is itself the root of a smaller subtree, which is why
  [recursion](recursion.md) fits trees so naturally.
- A **binary search tree** adds an ordering rule (left subtree smaller, right
  subtree larger) that enables `O(log n)` lookup when balanced.

See the [Tree pattern](../patterns/tree/intuition.md).

## Graph

Nodes (also called vertices) connected by edges, with no restriction: cycles are allowed, and a node can have any number of neighbors. A tree is just a graph with no cycles and one path between any two nodes.

```text
A --- B
|   / |
|  /  |
C --- D
```

Graphs are usually stored as an **adjacency list**: a hash map (or array) from each node to the list of its neighbors.

```text
A -> [B, C]
B -> [A, C, D]
C -> [A, B, D]
D -> [B, C]
```

Most graph problems are some flavor of "explore from a starting node", solved with depth-first or breadth-first search. See the [Graph pattern](../patterns/graph/intuition.md) and [Topological Sort](../patterns/topological_sort/intuition.md).

## Heap (priority queue)

A structure that always hands you the smallest (or largest) item instantly, without keeping everything fully sorted.

- **Peek at the minimum**: `O(1)`.
- **Add an item or remove the minimum**: `O(log n)`.
- Useful whenever you repeatedly need "the smallest remaining" or "the `k`
  largest", such as merging sorted lists or finding a running median.

See the [Heap pattern](../patterns/heap/intuition.md).

## Trie (prefix tree)

A tree with one node per character, where each path from the root spells out a prefix. Words that share a prefix share those nodes.

```text
        (root)
        /    \
       c      t
       |      |
       a      o
      / \
     r   t        stores: "car", "cat", "to"
```

- **Inserting or looking up a word of length `L`**: `O(L)`, one step per
  character, no matter how many words are stored.
- Shines when many words share prefixes, and for prefix queries such as
  "every word starting with `ca`".

See the [Trie pattern](../patterns/trie/intuition.md).

## Union-find (disjoint set)

A structure that keeps items grouped into sets and merges groups as new connections appear.

```text
{0, 1, 2}   {3, 4}   {5}        after union(2, 3):
                                {0, 1, 2, 3, 4}   {5}
```

- **`find(x)`** answers "which group is `x` in?", and **`union(x, y)`**
  merges two groups. Both are near-`O(1)` amortized with two standard tricks: path compression and union by rank.
- The tool for dynamic connectivity and grouping: counting connected
  components, detecting cycles, merging accounts as shared items appear.

See the [Union-Find pattern](../patterns/union_find/intuition.md).

## Choosing the right one

A quick decision guide:

| If you need to | Reach for |
|----------------|-----------|
| Look something up by key, or ask "have I seen this?" | Hash map or hash set |
| Handle the most recent item first (nesting, matching) | Stack |
| Handle items in arrival order (level-by-level search) | Queue |
| Repeatedly grab the smallest or largest item | Heap |
| Cheaply splice items in and out of a sequence | Linked list |
| Model hierarchy (parents and children) | Tree |
| Model arbitrary connections (networks, dependencies) | Graph |
| Prefix or whole-word lookups over many words | Trie |
| Merge groups as connections appear | Union-find |

Recognizing which structure a problem wants is a skill that grows with practice. The [pattern guides](../patterns/index.md) connect each structure to the problems that use it.
