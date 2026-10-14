# [Employee Ratings Management System](https://www.fastprep.io/problems/amazon-employee-ratings-data-structure)

**Hard** | **NN minutes** | **Array, Segment Tree, Binary Search, Design**

Process a sequence of operations on an initially empty ordered list of employee ratings. Operation [1, rating] appends a rating. Operation [2, index] deletes the rating at the current zero-based index, shifting later indices left. Operation [3] queries the maximum rating and its earliest current index.

Return one row [maximumRating, earliestIndex] for every query operation. Every deletion index is valid, and every query occurs while at least one rating exists.

## Examples

### Example 1

**Input:** `operations = [[1,5],[1,7],[1,7],[3],[2,1],[3]]`

**Output:** `[[7,1],[7,1]]`

**Explanation:** The first maximum is at index 1; after deleting it, the remaining 7 shifts to index 1.

### Example 2

**Input:** `operations = [[1,-2],[3],[1,4],[3]]`

**Output:** `[[-2,0],[4,1]]`

**Explanation:** Queries reflect both negative and later positive ratings.

### Example 3

**Input:** `operations = [[1,3],[1,1],[2,0],[3]]`

**Output:** `[[1,0]]`

**Explanation:** Deleting index zero shifts the remaining rating to zero.

## Constraints

- `1 ≤ operations.length ≤ 100000.`
- `Each operation is exactly one of [1, rating], [2, index], or [3].`
- `-10^9 ≤ rating ≤ 10^9.`
- `Deletion indices and non-empty query preconditions are valid.`

## Solutions

### Linear Scan Over a Mutable List

#### Derivation

The most literal reading of the operations: maintain the ratings in a Python list and do exactly what each row says. Append on `[1, rating]`, `pop(index)` on `[2, index]`, and on `[3]` find the maximum with a full scan and its position with a second scan. Nothing else is tracked:

1. Keep `ratings`, the current list, and `results`, one row per query.
2. On `[1, rating]`, call `ratings.append(rating)`.
3. On `[2, index]`, call `ratings.pop(index)`, which shifts the tail left.
4. On `[3]`, compute `max_rating = max(ratings)` and append `[max_rating, ratings.index(max_rating)]`; `index` returns the first match, which is the earliest index by construction.
5. Return `results` after all operations.

Each query is honest and obviously correct, but both the scans and the shift are linear, which the comparison table prices out.

#### Walkthrough

Example 3, which exercises every operation kind: `operations = [[1,3],[1,1],[2,0],[3]]`.

```text
[1, 3]    ratings = [3]
[1, 1]    ratings = [3, 1]
[2, 0]    ratings.pop(0) shifts the tail    ratings = [1]
[3]       max of [1] is 1, index of 1 is 0  results = [[1, 0]]
```

The deletion shows the shift directly: removing the head drags `1` from index 1 to index 0, so the query reads `[1, 0]`, the expected Output for Example 3.

#### Solution

The code is the walkthrough's three branches.

```python
from typing import List


class Solution:
    def solve(self, operations: List[List[int]]) -> List[List[int]]:
        ratings: List[int] = []
        results: List[List[int]] = []

        for operation in operations:
            if operation[0] == 1:
                ratings.append(operation[1])
            elif operation[0] == 2:
                ratings.pop(operation[1])
            else:
                max_rating = max(ratings)
                results.append([max_rating, ratings.index(max_rating)])

        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n` operations pays up to `O(n)`: a deletion shifts the tail, a full append-count list scan runs `max`, and a second scan runs `index`, so the worst case is quadratic overall.

##### Space Complexity: `O(n)`

The current ratings plus one output row per query.

#### Key Insights

- `list.index` returning the first match does half the work for free: the earliest index of the maximum comes with no extra logic.
- The two scans per query and the shift per deletion are invisible at small `n` and fatal at `10^5` operations, which is exactly the constraint this page declares.
- Every later approach answers the same three duties: find the maximum, find how many live ratings precede it, and delete by current position.

### Lazy Heap + Fenwick Index Mapping

#### Derivation

Two duties are separable, and separating them is the whole trick. Finding the maximum needs only a [priority queue](https://en.wikipedia.org/wiki/Priority_queue), not a sorted structure. Mapping a current index to the underlying slot needs only live counts. The obstacle to combining them is that a plain heap cannot delete arbitrary elements, so deletions leave stale entries. The repair is [lazy deletion](https://en.wikipedia.org/wiki/Lazy_deletion): never remove from the heap on delete; mark the slot dead, and let a query discard stale entries only when they surface at the top:

1. Give every append a permanent sequence number `sequence`; slots are never reused, so a heap entry `(-rating, sequence)` identifies its rating for life.
2. Track liveness in `alive` and fold it into a [Fenwick tree](https://en.wikipedia.org/wiki/Fenwick_tree) `live_prefix`, where `count_live_through(sequence)` returns how many live slots precede or equal it: the current index of the live slot `sequence` is `count_live_through(sequence) - 1`.
3. Deletion `[2, index]` asks the inverse question: which live slot is the `index + 1`-th live one? `find_rank_live` walks the Fenwick tree's binary lifting and returns the slot, which is then marked dead.
4. A query `[3]` pops heap entries whose slot is dead, reads the top's rating, and maps it to its current index with `count_live_through`.
5. Ties need no handling: the tuple ordering pops the smaller sequence first among equal ratings, which is the earliest current index.

#### Formula

The Fenwick tree stores live counts over slot numbers so that both directions of the index mapping are logarithmic. For a live slot `sequence`, its current zero-based index is

$$ \text{currentIndex}(\textit{sequence}) = \left(\sum_{k=1}^{\textit{sequence}} \textit{live}_k\right) - 1 $$

```text
currentIndex(sequence) = live[1] + ... + live[sequence] - 1
```

and the deletion `[2, index]` inverts the relation, asking for the slot whose rank among live slots is `index + 1`. The Fenwick lift answers it by descending the implicit binary tree of the `live_prefix` array, accumulating one bit of the position at a time:

```text
find_rank_live(rank):
  position = 0, remaining = rank
  for step in powers of two, high to low:
    if live_prefix[position + step] < remaining:
      remaining -= live_prefix[position + step]
      position += step
  return position + 1
```

A slot is dead when it sits behind its own stale `live_prefix` contribution, which is exactly what the accumulated sum keeps out; the returned `position + 1` is the `rank`-th live slot number.

#### Walkthrough

Example 1: `operations = [[1,5],[1,7],[1,7],[3],[2,1],[3]]`. The heap entries are written `(rating, sequence)` here (negated in the code); `alive` lists slots 1 through 3:

```text
[1, 5]   push (5,1)    heap {(5,1)}            alive {1}        no output
[1, 7]   push (7,2)    heap {(7,2),(5,1)}      alive {1,2}
[1, 7]   push (7,3)    heap {(7,2),(7,3),(5,1)} alive {1,2,3}
[3]      top (7,2) is alive: count_live_through(2) = 2, index 2-1 = 1   -> [7, 1]
[2, 1]   find_rank_live(2): the second live slot is 2; mark 2 dead
         heap {(7,2),(7,3),(5,1)} keeps the now-stale (7,2), alive {1,3}
[3]      top (7,2) is dead: discard it; next top (7,3) is alive
         count_live_through(3) = 2, index 2-1 = 1                       -> [7, 1]
```

The first query needs no peeling: among the two ratings 7, the tuple order surfaces `(7, 2)` before `(7, 3)`, and slot 2 is the earliest index. After the deletion of slot 2, the second query pays exactly one lazy pop to discard the stranded `(7, 2)` and reports `[7, 1]` again, now pointing at slot 3, the expected Output for Example 1.

#### Solution

The code is the walkthrough's three parts: the Fenwick helpers over `live_prefix`, the rank walk for deletions, and the lazy-top query.

```python
import heapq
from typing import List, Tuple


class Solution:
    def solve(self, operations: List[List[int]]) -> List[List[int]]:
        append_count = sum(1 for operation in operations if operation[0] == 1)
        alive = [False] * (append_count + 1)
        live_prefix = [0] * (append_count + 1)
        highest_step = 1 << (append_count.bit_length() - 1)
        heap: List[Tuple[int, int]] = []
        results: List[List[int]] = []
        sequence = 0

        def add_live_prefix(sequence_number: int, delta: int) -> None:
            while sequence_number <= append_count:
                live_prefix[sequence_number] += delta
                sequence_number += sequence_number & -sequence_number

        def count_live_through(sequence_number: int) -> int:
            live_total = 0
            while sequence_number > 0:
                live_total += live_prefix[sequence_number]
                sequence_number -= sequence_number & -sequence_number
            return live_total

        def find_rank_live(rank: int) -> int:
            position = 0
            remaining = rank
            step = highest_step
            while step > 0:
                next_position = position + step
                if (next_position <= append_count
                        and live_prefix[next_position] < remaining):
                    position = next_position
                    remaining -= live_prefix[next_position]
                step //= 2
            return position + 1

        for operation in operations:
            if operation[0] == 1:
                sequence += 1
                alive[sequence] = True
                add_live_prefix(sequence, 1)
                heapq.heappush(heap, (-operation[1], sequence))
            elif operation[0] == 2:
                target_sequence = find_rank_live(operation[1] + 1)
                alive[target_sequence] = False
                add_live_prefix(target_sequence, -1)
            else:
                while not alive[heap[0][1]]:
                    heapq.heappop(heap)
                negated_rating, max_sequence = heap[0]
                results.append(
                    [-negated_rating, count_live_through(max_sequence) - 1])

        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Every operation touches the Fenwick tree in `O(log n)` and the heap in `O(log n)` amortized: each append pushes once, so the total number of lazy pops across the whole run is bounded by the number of pushes.

##### Space Complexity: `O(n)`

The slot arrays and the heap, which holds one entry per append plus whatever stale entries deletion has stranded.

#### Key Insights

- Never-reused sequence numbers turn "which slot is this?" from a linear search into an array lookup, which is what lets lazy deletion work at all.
- Lazy deletion moves the cost of a deletion onto the first query that surfaces the dead entry, and each entry can be discarded only once, so the amortized bound stays logarithmic.
- Encoding the slot number as the heap tuple's tie-break resolves equal ratings toward the earliest current index for free.
- `highest_step = 1 << (append_count.bit_length() - 1)` is the largest power of two not exceeding `append_count`, the standard starting step of the Fenwick lift.

### Segment Tree Over Append Slots

#### Derivation

The lazy heap delegates liveness to a side array and lets stale entries linger. The segment tree version refuses stale state altogether: it maintains one [segment tree](https://en.wikipedia.org/wiki/Segment_tree) over the `append_count` slots where every node stores three aggregates over its slot range: `live_count`, `best_rating`, and `best_slot`, the slot achieving that maximum among live ratings. Then all three duties run inside one structure, and the maximum's slot comes out of the root with its earliest-index guarantee enforced by an explicit tie-break in `refresh`:

1. Precount `append_count` and build the tree over slots `1` through `append_count`, every leaf starting dead with rating `empty_rating` (a value below any legal rating, so dead leaves never win a `refresh` comparison).
2. `[1, rating]` assigns the next sequence number to the leaf and updates the path to the root, leaf set live with that rating.
3. `[2, index]` walks the tree by live counts (`find_rank_live`: descend left when the left child holds at least `index + 1` live slots) and marks the found leaf dead.
4. `[3]` reads `best_rating[1]` and `best_slot[1]` from the root and converts the slot to its current index with `count_live_before`, a live-count query over the prefix of slots before `best_slot[1]`.
5. In `refresh`, the left child wins ties (`>=`), so equal maxima resolve to the leftmost slot, which is the earliest current index.

#### Invariant and Bound

Every internal node satisfies, after any `set_live` path update:

```text
live_count[node] = live_count[left] + live_count[right]
best_rating[node] = max over live leaves in the node's range
best_slot[node]   = leftmost slot achieving best_rating[node]
```

`refresh` restores the relation on both ancestors of the one changed leaf, and no other node's aggregates change, so every operation repairs `O(log n)` nodes. The left-wins tie in the parent comparison is what preserves the leftmost claim at every level, so by induction the root's `best_slot` is the leftmost live maximum. With every leaf initialized dead and `empty_rating` strictly below all legal ratings, a `refresh` over an all-dead range yields a dead sentinel rather than a stale rating, so a query during a live rating can never read one.

#### Walkthrough

Example 3: `operations = [[1,3],[1,1],[2,0],[3]]`, capacity 4. Only nodes on changed paths are shown:

```text
build      every leaf dead, empty_rating = -10^18
[1, 3]     set_live slot 1, rating 3
           n4[1,1]=(3), n2[1,2]: live 1, best (3, slot 1), n1: best (3, slot 1)
[1, 1]     set_live slot 2, rating 1
           n5[2,2]=(1), n2[1,2]: live 2, best (3, slot 1)  (3 beats 1)
           n1 unchanged: best (3, slot 1)
[2, 0]     find_rank_live(1): n2 holds 2 live >= 1 -> left;
           n4 holds 1 live >= 1 -> slot 1; set_live slot 1 dead
           n4 dead, n2[1,2]: live 1, best (1, slot 2), n1: live 1, best (1, slot 2)
[3]        count_live_before(slot 2) = 0 live slots before it
           result [best_rating 1, index 0]                 -> [1, 0]
```

The second append's rating 1 never reaches the root because the tie-break and the max both favor the still-live slot 1; the deletion then propagates the new state up one path, and the query reads `[1, 0]` straight off the root, the expected Output for Example 3.

#### Solution

The code is the four tree routines over one array-based segment tree: `refresh`, `set_live`, the live-count prefix query, and the rank walk, with the operation loop on top.

```python
from typing import List


class Solution:
    def solve(self, operations: List[List[int]]) -> List[List[int]]:
        append_count = sum(1 for operation in operations if operation[0] == 1)
        empty_rating = -(10 ** 18)
        tree_capacity = 4 * append_count
        live_count = [0] * tree_capacity
        best_rating = [empty_rating] * tree_capacity
        best_slot = [0] * tree_capacity
        results: List[List[int]] = []
        sequence = 0

        def refresh(node: int) -> None:
            left_node, right_node = 2 * node, 2 * node + 1
            live_count[node] = live_count[left_node] + live_count[right_node]
            if best_rating[left_node] >= best_rating[right_node]:
                best_rating[node] = best_rating[left_node]
                best_slot[node] = best_slot[left_node]
            else:
                best_rating[node] = best_rating[right_node]
                best_slot[node] = best_slot[right_node]

        def build(node: int, low: int, high: int) -> None:
            if low == high:
                best_slot[node] = low
                return
            middle = (low + high) // 2
            build(2 * node, low, middle)
            build(2 * node + 1, middle + 1, high)
            refresh(node)

        def set_live(node: int, low: int, high: int, slot: int,
                     is_live: bool, rating: int) -> None:
            if low == high:
                live_count[node] = 1 if is_live else 0
                best_rating[node] = rating if is_live else empty_rating
                best_slot[node] = slot
                return
            middle = (low + high) // 2
            if slot <= middle:
                set_live(2 * node, low, middle, slot, is_live, rating)
            else:
                set_live(2 * node + 1, middle + 1, high, slot, is_live, rating)
            refresh(node)

        def count_live_before(node: int, low: int, high: int, bound: int) -> int:
            if low >= bound:
                return 0
            if high < bound:
                return live_count[node]
            middle = (low + high) // 2
            return (count_live_before(2 * node, low, middle, bound)
                    + count_live_before(2 * node + 1, middle + 1, high, bound))

        def find_rank_live(node: int, low: int, high: int, rank: int) -> int:
            if low == high:
                return low
            middle = (low + high) // 2
            if rank <= live_count[2 * node]:
                return find_rank_live(2 * node, low, middle, rank)
            return find_rank_live(2 * node + 1, middle + 1, high,
                                  rank - live_count[2 * node])

        build(1, 1, append_count)
        for operation in operations:
            if operation[0] == 1:
                sequence += 1
                set_live(1, 1, append_count, sequence, True, operation[1])
            elif operation[0] == 2:
                slot = find_rank_live(1, 1, append_count, operation[1] + 1)
                set_live(1, 1, append_count, slot, False, 0)
            else:
                results.append([
                    best_rating[1],
                    count_live_before(1, 1, append_count, best_slot[1]),
                ])

        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Every operation updates or queries one root-to-leaf path, and each tree routine visits `O(log n)` nodes.

##### Space Complexity: `O(n)`

The three tree arrays over `4 * append_count` nodes.

#### Key Insights

- Precounting the appends sizes the tree once, so slots are fixed from the start and no dynamic resizing ever occurs.
- Storing the winner's slot, not just its rating, removes the "find which slot holds the maximum" search the heap approach pays at every query.
- The left-wins tie in `refresh` is the entire earliest-index guarantee; switching it to `>` would silently return a later duplicate's index.
- The dead sentinel `empty_rating` must stay below every legal rating, so all-dead ranges never surface a stale maximum to a live query.

## Comparison of Solutions

### Time Complexity

- **Linear Scan Over a Mutable List**: `O(n^2)` - each operation scans or shifts up to the full list.
- **Lazy Heap + Fenwick Index Mapping**: `O(n log n)` - logarithmic heap and Fenwick work per operation, with lazy pops amortized against pushes.
- **Segment Tree Over Append Slots**: `O(n log n)` - every operation updates or queries one root-to-leaf path.

### Space Complexity

- **Linear Scan Over a Mutable List**: `O(n)` - the current list plus output rows.
- **Lazy Heap + Fenwick Index Mapping**: `O(n)` - slot arrays and the heap, including stranded stale entries.
- **Segment Tree Over Append Slots**: `O(n)` - three aggregates per tree node over `4 * append_count` nodes.

### Trade-offs

- The linear scan is three lines per operation and impossible to get wrong, but it cannot survive the declared `10^5` operations in the worst case.
- The lazy heap carries the fewest moving parts among the fast options: a heap, a liveness flag, and a Fenwick tree; the cost is that stale entries linger and queries do the cleanup.
- The segment tree keeps no stale state at all and answers every duty in one structure, but it carries the most code and the tie-break lives in one comparison operator.

### When to Use Each

- **Linear Scan Over a Mutable List**: prototyping, cross-checking the fast versions on small inputs, or operations counts in the hundreds.
- **Lazy Heap + Fenwick Index Mapping (Recommended)**: the interview target: it reaches `O(n log n)` with structures small enough to write under time pressure.
- **Segment Tree Over Append Slots**: when the operation set grows beyond this page (range aggregates, more query kinds) or when guaranteed worst-case per-operation cost matters more than code volume.

### Optimization Notes

- Precounting appends is what both fast solutions hinge on: a fixed slot per append turns shifting-index deletion into mark-one-slot-dead.
- In the heap approach, total lazy pops are bounded by total pushes, so the amortized `O(log n)` holds no matter how many deletions strand entries; the same trick is worth reusing wherever a heap needs arbitrary deletion.
- In the segment tree, `refresh`'s `>=` is load-bearing: it implements the leftmost tie-break, and changing it to `>` changes observable output on duplicate maxima.
- A production variant could replace `count_live_before` with a stored order-statistic per node, trading one extra array for a constant-factor faster index conversion.
