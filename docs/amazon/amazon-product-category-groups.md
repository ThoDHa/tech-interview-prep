# [Product Category Group Sizes](https://www.fastprep.io/problems/amazon-product-category-groups)

**Easy** | **NN minutes** | **Union Find, Sorting**

You are given a list of products and a list of pairs. Each pair means the two products belong to the same category. Category membership is transitive: if product A is in the same category as B, and B is in the same category as C, then A and C are in the same category.

Return the size of every final category group, sorted in increasing order. The number of returned sizes is the number of final categories.

Function Description Complete the function productCategoryGroupSizes in the editor.

productCategoryGroupSizes has the following parameters:

String products[]: all product identifiersString pairs[][]: product pairs that belong to the same categoryReturns int[]: the sorted sizes of the final category groups

## Examples

### Example 1

**Input:** `products = ["A", "B", "C", "D", "E"]`, `pairs = [["A", "B"], ["B", "C"], ["D", "E"]]`

**Output:** `[2, 3]`

**Explanation:** A, B, and C form one category of size 3. D and E form one category of size 2.

### Example 2

**Input:** `products = ["p1", "p2", "p3", "p4"]`, `pairs = [["p1", "p2"]]`

**Output:** `[1, 1, 2]`

**Explanation:** Products p3 and p4 are not paired with any other product, so each is its own category.

## Constraints

- `Product identifiers are unique in products.`
- `Each pair contains two valid product identifiers.`
- `Category membership is transitive.`

## Solutions

Throughout, `P` is the number of products and `E` is the number of pairs. Both solutions read the same implicit graph: products are nodes and each pair is an undirected edge.

### DFS with Adjacency Map

#### Derivation

Transitivity is the language of connected components: two products belong to the same category exactly when a chain of pairs joins them, so the final categories are the components of the implicit graph. The literal plan follows: claim each product's whole component one at a time and count what each claim picks up. A [depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) expresses the claim in the fewest lines, and a `visited` set guarantees no product is counted twice:

1. Build `adjacency`, a map from every product to the set of its paired
   products, adding each pair in both directions.
2. Scan `products` in order, keeping a `visited` set and a `group_sizes` list.
3. When a product is not in `visited`, run a recursive `dfs` that marks the
   product visited and returns `1` plus the sizes of its unvisited neighbors'
   fills.
4. Append each fill's size to `group_sizes` and return
   `sorted(group_sizes)`.

#### Walkthrough

Example 1: `products = ["A", "B", "C", "D", "E"]`, `pairs = [["A", "B"], ["B", "C"], ["D", "E"]]`, so the adjacency map reads `A: {B}`, `B: {A, C}`, `C: {B}`, `D: {E}`, `E: {D}`:

```text
scan A   unvisited -> dfs(A)
  dfs(A)   visited = {A}          neighbor B unvisited -> dfs(B)
  dfs(B)   visited = {A, B}       neighbors A, C -> A visited, dfs(C)
  dfs(C)   visited = {A, B, C}    neighbor B visited -> return 1
  dfs(B) returns 2                (1 + dfs(C))
  dfs(A) returns 3                group_sizes = [3]
scan B, C   visited, skip
scan D   unvisited -> dfs(D)
  dfs(D)   visited = {A, B, C, D}       neighbor E unvisited -> dfs(E)
  dfs(E)   visited = {A, B, C, D, E}    neighbor D visited -> return 1
  dfs(D) returns 2                group_sizes = [3, 2]
scan E   visited, skip
```

The scan ends with `group_sizes = [3, 2]`, and sorting for the required increasing order returns `[2, 3]`, matching the expected Output.

#### Solution

The code is the walkthrough's scan-and-count: the loop seeds each category and `dfs` returns its size.

```python
from typing import Dict, List, Set


class Solution:
    def solve(self, products: List[str], pairs: List[List[str]]) -> List[int]:
        adjacency: Dict[str, Set[str]] = {product: set() for product in products}
        for first_product, second_product in pairs:
            adjacency[first_product].add(second_product)
            adjacency[second_product].add(first_product)

        visited: Set[str] = set()
        group_sizes: List[int] = []

        def dfs(member: str) -> int:
            visited.add(member)
            size = 1
            for neighbor in adjacency[member]:
                if neighbor not in visited:
                    size += dfs(neighbor)
            return size

        for product in products:
            if product not in visited:
                group_sizes.append(dfs(product))
        return sorted(group_sizes)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(P + E)`

Building the adjacency map touches each pair twice, and the fills visit each product once while scanning each edge from both ends; the final sort costs `O(P log P)` on up to `P` category sizes.

##### Space Complexity: `O(P + E)`

The adjacency map stores two endpoints per pair, and the `visited` set plus the recursion stack are bounded by the product count.

#### Key Insights

- Transitivity turns "same category" into plain graph reachability, which is why the whole problem collapses to component sizes.
- A product unvisited at scan time is provably the first member of its category, because every earlier fill marked its whole group.
- Seeding the adjacency sets from `products` (rather than from the pairs) is what makes unpaired products reachable: they enter the map with an empty neighbor set and count as singleton categories.

### Union-Find with Size Tally

#### Derivation

The fill never needs to walk the graph at all. Category membership is an equivalence relation, and equivalence classes are exactly what a [disjoint-set](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) structure maintains: begin with every product in its own group, and let each pair merge two groups in near-constant time. After all pairs are processed, two products share a category exactly when they share a root, so the sizes come from one tally pass: count products per root and sort the counts. This also sidesteps the recursion depth the fill risks when the pairs form a long chain:

1. Map each product to a slot with `slot_of_product` (product identifiers are
   unique, so the mapping is unambiguous).
2. Build a `UnionFind` over `P` slots and call `union` for both endpoints of
   every pair.
3. For each product, `find` its root and add one to `size_by_root[root]`.
4. Return `sorted(size_by_root.values())`.

#### Walkthrough

Example 2: `products = ["p1", "p2", "p3", "p4"]`, `pairs = [["p1", "p2"]]`. The slots come out as `p1: 0`, `p2: 1`, `p3: 2`, `p4: 3`, and every slot starts as its own root:

```text
pair p1-p2   find roots 0, 1 -> parent[1] = 0, rank[0] = 1
tally        find(p1) = 0, find(p2) = 0, find(p3) = 2, find(p4) = 3
size_by_root = {0: 2, 2: 1, 3: 1}
sorted sizes = [1, 1, 2]
```

The single pair merges two slots into one group of size `2`, and the untouched slots `2` and `3` survive as singleton categories of size `1`. The sorted result `[1, 1, 2]` matches the expected Output. (On Example 1, three merges chain `A`, `B`, `C` under one root and `D`, `E` under another, so the tally reads `{root: 3, root: 2}` and the return is `[2, 3]`.)

#### Solution

The code is the merge pass plus the tally: one union per pair, one find per product.

```python
from typing import Dict, List


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, member_slot: int) -> int:
        while self.parent[member_slot] != member_slot:
            self.parent[member_slot] = self.parent[self.parent[member_slot]]
            member_slot = self.parent[member_slot]
        return member_slot

    def union(self, first_slot: int, second_slot: int) -> None:
        first_root = self.find(first_slot)
        second_root = self.find(second_slot)
        if first_root == second_root:
            return
        if self.rank[first_root] < self.rank[second_root]:
            first_root, second_root = second_root, first_root
        self.parent[second_root] = first_root
        if self.rank[first_root] == self.rank[second_root]:
            self.rank[first_root] += 1


class Solution:
    def solve(self, products: List[str], pairs: List[List[str]]) -> List[int]:
        slot_of_product: Dict[str, int] = {
            product: slot for slot, product in enumerate(products)
        }
        forest = UnionFind(len(products))
        for first_product, second_product in pairs:
            forest.union(slot_of_product[first_product],
                         slot_of_product[second_product])

        size_by_root: Dict[int, int] = {}
        for product in products:
            root_slot = forest.find(slot_of_product[product])
            size_by_root[root_slot] = size_by_root.get(root_slot, 0) + 1
        return sorted(size_by_root.values())
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(P + E × α(P))`

The slot map and the tally are one pass over the products each, and each of the `E` pairs pays two finds amortized to `α(P)`, the inverse Ackermann function, a constant below `5` for any input that fits in memory.

##### Space Complexity: `O(P)`

The `parent` and `rank` arrays plus the slot map; no adjacency structure is built at all.

#### Key Insights

- Duplicate or self-pairs cost nothing: a union whose roots already match returns immediately, so no deduplication pass is needed.
- The tally pass replaces component enumeration: sizes come from counting products per root, with no traversal of the implicit graph.
- Path halving inside `find` keeps the trees flat iteratively, so chain-shaped pair lists cannot stress the recursion limit the way they stress the fill.

## Comparison of Solutions

### Time Complexity

- **DFS with Adjacency Map**: `O(P + E)` - one adjacency build and one fill visiting every product and pair once, plus a sort of the size list.
- **Union-Find with Size Tally**: `O(P + E × α(P))` - two near-constant finds per pair, one find per product for the tally, plus the same sort.

### Space Complexity

- **DFS with Adjacency Map**: `O(P + E)` - adjacency map with two endpoints per pair, visited set, and a recursion stack.
- **Union-Find with Size Tally**: `O(P)` - parent and rank arrays and the slot map, with no adjacency structure at all.

### Trade-offs

- **DFS with Adjacency Map**: states the definition directly (scan, claim, count) and generalizes to listing each category's members, at the price of building the full adjacency structure and recursing.
- **Union-Find with Size Tally**: never materializes the graph and processes pairs one at a time, which suits streaming pairs and deep chains, but its root-tally bookkeeping is less visual than a fill.

### When to Use Each

- **DFS with Adjacency Map (Recommended)**: the default interview answer when the input is given up front and recursion depth is not a concern; it is the easiest to explain and extends to "print each group" follow-ups.
- **Union-Find with Size Tally**: when pairs arrive as a stream, when chain-shaped inputs make recursion risky, or when the problem is a stepping stone to dynamic connectivity.

### Optimization Notes

- Repeated pairs are free in both solutions: the adjacency `set` absorbs duplicates, and a same-root union returns before touching any structure.
- `union` by rank bounds tree height at `O(log P)` and path halving flattens further on every lookup, which together produce the inverse-Ackermann bound.
- If the sizes themselves must stay grouped (for example, "which products are in the size-3 category"), the DFS variant extends naturally by collecting members instead of counts, while Union-Find would need a root-to-members map on top.
