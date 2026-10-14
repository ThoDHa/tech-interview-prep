# [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/)

**Medium** | **25 minutes** | **Array, Math, Divide and Conquer, Geometry, Sorting, Heap (Priority Queue), Quickselect**

**Pattern:** [Heap / Priority Queue](../patterns/heap/intuition.md)

**Algorithm:** [Heap](https://en.wikipedia.org/wiki/Heap_(data_structure)) · [Quickselect](https://en.wikipedia.org/wiki/Quickselect) · [Sorting](https://en.wikipedia.org/wiki/Sorting_algorithm)

**Practice:** [`practice/k_closest_points_to_origin/solution.py`](../../practice/k_closest_points_to_origin/solution.py)

Given an array of points where `points[i] = [xi, yi]` represents a point on the X-Y plane and an integer `k`, return the `k` closest points to the origin `(0, 0)`.

The distance between two points on the X-Y plane is the Euclidean distance (i.e., `√(x1 - x2)² + (y1 - y2)²`).

You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).

## Examples

### Example 1

![K Closest Points to Origin Example](assets/k_closest_points_to_origin_example1.jpg) **Input:** `points = [[1,3],[-2,2]], k = 1`

**Output:** `[[-2,2]]`

**Explanation:** The distance between `(1, 3)` and the origin is `sqrt(10)`. The distance between `(-2, 2)` and the origin is `sqrt(8)`. Since `sqrt(8) < sqrt(10)`, `(-2, 2)` is closer to the origin. We only want the closest `k = 1` points from the origin, so the answer is just `[[-2,2]]`.

### Example 2

**Input:** `points = [[3,3],[5,-1],[-2,4]], k = 2`

**Output:** `[[3,3],[-2,4]]`

**Explanation:** The answer `[[-2,4],[3,3]]` would also be accepted.

## Constraints

- `1 <= k <= points.length <= 10^4`
- `-10^4 <= xi, yi <= 10^4`

## Deriving the Solution

Every approach ranks points by the same key: the squared distance `x*x + y*y`, which orders points exactly as the true Euclidean distance does (the [Formula](#formula) below makes that precise). The approaches differ only in how much ordering work they spend to isolate the `k` smallest keys.

1. **Start literal.** "The `k` closest points" invites finding the single
   closest point, removing it, and repeating `k` times. Correct, but every round rescans the whole remaining list, costing `O(n * k)`: see [Brute Force](#brute-force).
2. **Sort once instead.** The repeated scans keep re-deriving order information
   that one pass could settle. Sorting the whole array by the key makes the `k` closest the first `k` slots in `O(n log n)`, but fully orders all `n` points when only `k` of them matter: see [Sort by Distance](#sort-by-distance).
3. **Keep only `k` candidates.** The far points never need any order among
   themselves. A max-heap capped at `k` entries holds the best candidates seen so far and evicts the farthest in `O(log k)` whenever something closer arrives, for `O(n log k)` total: see [Max-Heap of Size K](#max-heap-of-size-k).
4. **Order nothing but the boundary.** Even the `k` kept points need no internal
   order; only the boundary between the `k` closest and everything else matters. Quicksort's partition step fixes exactly that boundary in `O(n)` average time: see [Quickselect](#quickselect).
5. **Let the library run the bounded heap.** The capped heap of step 3 is a
   standard shape, and `heapq.nsmallest` implements it given the same key, absorbing the negation trick, the eviction test, and the `heapreplace` call into one line: see [Library One-Liner with `heapq.nsmallest`](#library-one-liner-with-heapqnsmallest).

## Solutions

### Brute Force

#### Derivation

The most direct reading, with no sort or heap: to collect the `k` closest points, find the single nearest point, remove it, and repeat `k` times. The only subtlety is the ranking key: comparing squared distances `x*x + y*y` is enough, because taking the square root never changes which of two distances is smaller (the [Formula](#formula) below states this precisely), so `sqrt` would add cost without changing any comparison.

1. Copy `points` into a working list `remaining` so the input is left intact.
2. Repeat `k` times: scan every remaining point, track in `best` the index of
   the smallest squared distance `dist`, then pop that point and append it to `closest`.
3. After `k` rounds `closest` holds exactly the `k` closest points.

#### Formula

The ranking key is the [Euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance) from the origin:

$$ d(x, y) = \sqrt{(x - 0)^2 + (y - 0)^2} = \sqrt{x^2 + y^2} $$

```text
d(x, y) = sqrt((x - 0)^2 + (y - 0)^2) = sqrt(x^2 + y^2)
```

Every solution on this page compares \(d^2 = x^2 + y^2\) and never calls `sqrt`. That is safe because \(t \mapsto \sqrt{t}\) is strictly increasing on \(t \ge 0\), so for non-negative \(a, b\):

$$ \sqrt{a} < \sqrt{b} \iff a < b $$

```text
sqrt(a) < sqrt(b)  if and only if  a < b,  for a >= 0 and b >= 0
```

Ordering by \(d^2\) therefore produces exactly the same ordering as \(d\). Dropping the square root also keeps the arithmetic in exact integers rather than floats, so ties between equidistant points are decided without rounding error.

#### Walkthrough

Trace the Brute Force on Example 1: `points = [[1,3],[-2,2]]`, `k = 1`.

First, set up the working state: `remaining = [[1,3],[-2,2]]` (a copy of the input) and `closest = []`. We then run the outer loop `k = 1` time, so just one selection round.

In that round, `best` starts at `0` (pointing at `[1,3]`), and the inner loop scans the rest of `remaining` to find the smallest squared distance. The keys are `dist([1,3]) = 1*1 + 3*3 = 10` and `dist([-2,2]) = (-2)*(-2) + 2*2 = 8`:

| inner `i` | `remaining[i]` | `dist(remaining[i])` | `dist(remaining[best])` | smaller? | `best` after |
| --------- | -------------- | -------------------- | ----------------------- | -------- | ------------ |
| start     | -              | -                    | `10` (`best = 0`)       | -        | `0`          |
| `1`       | `[-2,2]`       | `8`                  | `10`                    | yes      | `1`          |

The scan ends with `best = 1`, so `remaining.pop(1)` removes `[-2,2]` and appends it: `closest = [[-2,2]]`, leaving `remaining = [[1,3]]`. With `k = 1` the loop is done.

The function returns `closest = [[-2,2]]`, which matches the example's expected Output `[[-2,2]]`.

#### Solution

The code is the walkthrough's selection round repeated `k` times: an inner scan for `best`, then a pop into `closest`.

```python
from typing import List


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        def dist(p: List[int]) -> int:
            # Squared distance preserves ordering and avoids a costly sqrt.
            return p[0] * p[0] + p[1] * p[1]

        remaining = list(points)
        closest = []
        # Pick the single closest remaining point k times by hand.
        for _ in range(k):
            best = 0
            for i in range(1, len(remaining)):
                if dist(remaining[i]) < dist(remaining[best]):
                    best = i
            closest.append(remaining.pop(best))
        return closest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * k)`

Each of the `k` selection rounds scans up to `n` remaining points, so the total work is `O(n * k)`. When `k` approaches `n` this degrades toward `O(n^2)`.

##### Space Complexity: `O(n)`

The working copy of the points holds up to `n` entries; the result aside, no other storage grows with the input.

#### Key Insights

- This is the most self-evident correct solution: find the nearest, remove it,
  repeat. It selects by hand rather than delegating to a sort or heap.
- It wastes work by rescanning the entire remaining list on every round, which
  motivates the heap and selection approaches that follow.
- Always key on squared distance; computing `sqrt` adds floating-point cost and
  rounding risk for no benefit to the ordering.

### Max-Heap of Size K

#### Derivation

The Brute Force pays for its rounds: each of the `k` selections rescans every remaining point, including the far ones that will never be part of the answer. What the scan really maintains is a running set of "best candidates so far", and a [max-heap](https://en.wikipedia.org/wiki/Heap_(data_structure)) maintains exactly that without rescanning: keep at most `k` points, arranged so the farthest current candidate sits on top and can be evicted the moment something closer arrives. Python's `heapq` is a min-heap, so storing the negated squared distance `-dist` puts the largest distance at `heap[0]`.

1. Iterate over the points, computing each squared distance `dist = x*x + y*y`.
2. While the heap holds fewer than `k` points, push the point with key
   `-dist` (negation turns Python's min-heap into a max-heap).
3. Once the heap is full, if a new point is closer than the heap's farthest
   (`-dist > heap[0][0]`), replace the top with `heapreplace`.
4. After processing all points, the heap holds exactly the `k` closest; return
   their coordinates.

#### Walkthrough

Trace the heap on Example 2: `points = [[3,3],[5,-1],[-2,4]]`, `k = 2`. The squared distances are `18`, `26`, and `20`. Each line shows the decision for one point and the heap contents (as the list `heapq` maintains) afterward:

```text
[3,3]   dist=18   heap not full -> push (-18, [3,3])     heap = [(-18, [3,3])]
[5,-1]  dist=26   heap not full -> push (-26, [5,-1])    heap = [(-26, [5,-1]), (-18, [3,3])]
[-2,4]  dist=20   -20 > heap[0][0] = -26 -> heapreplace  heap = [(-20, [-2,4]), (-18, [3,3])]
```

The first two points fill the heap to its cap of `k = 2`. Because the keys are negated, the smallest tuple sits at `heap[0]`, and the smallest negated key belongs to the largest distance: after two pushes the top is `(-26, [5,-1])`, the farthest candidate. The third point has `-dist = -20 > -26`, which says `20 < 26`: it is closer than the current farthest, so `heapreplace` evicts `[5,-1]` and inserts `[-2,4]` in one balanced operation.

The final comprehension strips the keys and returns `[[-2,4], [3,3]]`. Example 2 accepts any order, and this matches its explicitly accepted answer `[[-2,4],[3,3]]`.

#### Solution

The code is the walkthrough's push-or-replace decision applied to every point.

```python
import heapq
from typing import List


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        # Max-heap keyed by negative squared distance, capped at k entries.
        heap: list[tuple[int, List[int]]] = []
        for x, y in points:
            dist = x * x + y * y
            if len(heap) < k:
                heapq.heappush(heap, (-dist, [x, y]))
            elif -dist > heap[0][0]:
                # Closer than the current farthest in the heap: swap it in.
                heapq.heapreplace(heap, (-dist, [x, y]))
        return [point for _, point in heap]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log k)`

Each of the `n` points triggers at most one heap push or replace, and every heap operation costs `O(log k)` because the heap never exceeds `k` elements.

##### Space Complexity: `O(k)`

The heap stores at most `k` points; output aside, no other storage grows with the input.

#### Key Insights

- Keeping the heap bounded at `k` makes this superior to sorting when `k` is much
  smaller than `n`.
- Negating the squared distance turns `heapq` into a max-heap so the farthest
  candidate is always evictable in `O(1)` time at the top.
- `heapreplace` performs the pop-then-push in one balanced operation rather than
  two.

### Quickselect

#### Derivation

The heap still spends `O(log k)` per point maintaining order inside the candidate set, order the problem never asks for: the output may come back in any order. All that actually matters is a boundary: after rearranging, the first `k` slots must hold smaller keys than everything after them, with no order required on either side. [Quickselect](https://en.wikipedia.org/wiki/Quickselect) fixes exactly that boundary. It reuses the partition step of quicksort: pick a pivot, move every point with a smaller squared distance to its left, and the pivot lands at its final sorted index `mid`. Then, instead of recursing into both sides as quicksort would, it narrows toward the one side containing index `k`.

1. Pick a random pivot and `partition` the points so everything with a smaller
   squared distance sits to its left.
2. Let `mid` be the pivot's final index. If `mid == k`, the first `k` elements
   are exactly the answer.
3. If `mid < k`, the boundary lies to the right, so continue with `left = mid+1`;
   if `mid > k`, continue with `right = mid-1`.
4. When the loop ends, the first `k` points are the closest (in arbitrary order),
   which the problem permits.

#### Walkthrough

Trace Quickselect on Example 2: `points = [[3,3],[5,-1],[-2,4]]`, `k = 2`, with squared distances `18`, `26`, `20`. The pivot index is drawn at random, so a hand-trace must fix the draws: suppose the first draw is `pivot_idx = 2`, which resolves the search in a single partition (any other draw reaches the same first-two-points set after more rounds).

```text
setup      left=0, right=2      points = [[3,3], [5,-1], [-2,4]]   dists 18, 26, 20
partition  pivot_idx=2, pivot_dist = dist([-2,4]) = 20
           swap points[2], points[2]: pivot already at the end; store = 0
  i=0      dist([3,3]) = 18 < 20      -> swap points[0], points[0]; store = 1
  i=1      dist([5,-1]) = 26 < 20 fails -> store stays 1
           swap points[2], points[1]  -> points = [[3,3], [-2,4], [5,-1]]
           return store = 1
select     mid = 1, and mid < k = 2   -> left = mid + 1 = 2
loop       left == right              -> loop exits
```

The partition placed `[-2,4]` (key `20`) at its final sorted index `1`, with the smaller key `18` on its left and the larger key `26` on its right. Since `mid = 1 < k`, the boundary at index `k = 2` lies further right, and narrowing to `left = 2` ends the loop immediately. The function returns `points[:2] = [[3,3],[-2,4]]`, which is Example 2's expected Output.

#### Solution

The code is the walkthrough's partition-and-narrow loop; only the random pivot draws vary from run to run.

```python
import random
from typing import List


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        def dist(p: List[int]) -> int:
            return p[0] * p[0] + p[1] * p[1]

        def partition(left: int, right: int, pivot_idx: int) -> int:
            pivot_dist = dist(points[pivot_idx])
            # Move pivot to the end, then gather smaller elements on the left.
            points[pivot_idx], points[right] = points[right], points[pivot_idx]
            store = left
            for i in range(left, right):
                if dist(points[i]) < pivot_dist:
                    points[store], points[i] = points[i], points[store]
                    store += 1
            points[right], points[store] = points[store], points[right]
            return store

        left, right = 0, len(points) - 1
        # Target the boundary so the first k slots are the k smallest distances.
        while left < right:
            pivot_idx = random.randint(left, right)
            mid = partition(left, right, pivot_idx)
            if mid == k:
                break
            elif mid < k:
                left = mid + 1
            else:
                right = mid - 1
        return points[:k]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)` average, `O(n^2)` worst case

Each partition is linear, and random pivots shrink the search range by a constant fraction on average, yielding `O(n)` expected work. A pathological pivot sequence degrades to `O(n^2)`, made unlikely by randomization.

##### Space Complexity: `O(1)`

Partitioning happens in place; only a constant number of indices are tracked, so no extra storage scales with the input.

#### Key Insights

- Quickselect beats sorting because it only orders enough of the array to fix the
  `k`-th boundary, never fully sorting either side.
- Randomizing the pivot guards against adversarial inputs that would otherwise
  trigger the quadratic worst case.
- Mutating `points` in place keeps auxiliary space constant, at the cost of
  reordering the caller's list.

### Sort by Distance

#### Derivation

Every approach so far works to avoid ordering all `n` points. When `n` is modest, the shortest correct program accepts that cost and lets the language do the work: [sort](https://en.wikipedia.org/wiki/Sorting_algorithm) every point by its squared distance from the origin, then slice off the first `k`. The full sort does more than the problem asks, ordering the far points too, which is exactly the waste the heap and Quickselect exist to remove; the trade is that the code shrinks to two lines. The key is the same squared distance `x*x + y*y` used everywhere on this page, which sorts identically to the true distance.

1. Sort `points` in place using the squared distance as the key.
2. Slice off the first `k` entries, which are now the closest.

#### Walkthrough

Sorting is the entire technique here, so the trace shows what the sort receives and what it must produce. On Example 2: `points = [[3,3],[5,-1],[-2,4]]`, `k = 2`:

```text
keys     [3,3] -> 9 + 9 = 18    [5,-1] -> 25 + 1 = 26    [-2,4] -> 4 + 16 = 20
before   points = [[3,3], [5,-1], [-2,4]]    keys 18, 26, 20
after    points = [[3,3], [-2,4], [5,-1]]    keys 18, 20, 26
slice    points[:2] = [[3,3], [-2,4]]
```

The sort rearranges the points into ascending key order `18, 20, 26`, and the slice keeps the first `k = 2` of them. The function returns `[[3,3],[-2,4]]`, Example 2's expected Output.

#### Solution

The code is the two steps of the walkthrough: sort by key, then slice.

```python
from typing import List


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        # Squared distance preserves ordering and avoids a costly sqrt.
        points.sort(key=lambda p: p[0] * p[0] + p[1] * p[1])
        return points[:k]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

The sort dominates: every one of the `n` points is compared during an `O(n log n)` comparison sort.

##### Space Complexity: `O(n)`

Python's `list.sort` is in place only in the sense that no second list of points is built: CPython's Timsort still allocates a temporary merge buffer of up to `n/2` elements, so the auxiliary space is `O(n)` in the worst case.

#### Key Insights

- The shortest solution to write, leaning on the built-in sort, and perfectly
  acceptable given the constraint `n <= 10^4`.
- Sorting the entire array does more work than necessary when `k` is much smaller
  than `n`, which the heap and Quickselect approaches avoid.
- Always key on squared distance; computing `sqrt` adds floating-point cost and
  rounding risk for no benefit to the ordering.

### Library One-Liner with `heapq.nsmallest`

#### Derivation

The Max-Heap of Size K solution is a bounded-heap sweep: hold at most `k` candidates, keep the farthest of them reachable in constant time, and evict it the moment a closer point arrives. [`heapq.nsmallest`](https://docs.python.org/3/library/heapq.html#heapq.nsmallest) is that sweep, packaged. Handing it the same squared-distance key moves the entire mechanism into the library: the `-dist` negation that fakes a max-heap out of `heapq`, the "is the heap full yet" branch, the `-dist > heap[0][0]` comparison against the current farthest, the `heapreplace` call, and the comprehension that strips keys back off the survivors. What stays is the single decision the problem actually poses: rank points by `x*x + y*y`.

1. Express the ranking as a `key` function, the same squared distance every
   solution on this page uses.
2. Call `heapq.nsmallest(k, points, key=...)`, which sweeps the points once
   while maintaining a heap capped at `k` entries.
3. Return the resulting list directly. `nsmallest` yields the original points
   rather than key-decorated tuples, so there is nothing to unwrap.

The result comes back in ascending distance order, which is more than the problem asks for (any order is accepted) and more than the raw bounded heap provided.

#### Walkthrough

Trace it on Example 2: `points = [[3,3],[5,-1],[-2,4]]`, `k = 2`, whose squared distances are `18`, `26`, and `20`. This is the same case the Max-Heap walkthrough traced, and `nsmallest` makes the same decisions in the same order, seeding the heap with the first `k` points and then testing each remaining point against the current farthest:

```text
seed     first k=2 points   heap holds keys 18 and 26, farthest 26 on top
[-2,4]   key 20 < 26        replace the farthest: heap holds keys 18 and 20
sort     survivors ordered  keys 18, 20 -> [[3,3], [-2,4]]
```

The seeding step fills the heap to its cap of `k = 2` with `[3,3]` (key `18`) and `[5,-1]` (key `26`), arranged so the largest key sits on top. The third point has key `20`, which is smaller than the top key `26`, so it displaces `[5,-1]` in one balanced operation, exactly the `heapreplace` the Max-Heap section performs by hand. CPython then sorts the two survivors by key before returning them, which is why the output is ordered while the hand-written heap's was not.

The call returns `[[3,3],[-2,4]]`, matching Example 2's expected Output `[[3,3],[-2,4]]`.

#### Solution

The bounded-heap sweep, expressed as the key it ranks by.

```python
import heapq
from typing import List


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        # Squared distance preserves ordering and avoids a costly sqrt.
        return heapq.nsmallest(
            k, points, key=lambda p: p[0] * p[0] + p[1] * p[1]
        )
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log k)`

Each of the `n` points has its key computed once and is compared against the heap's largest key; only a point that wins that comparison pays for an `O(log k)` replacement, and the final sort of the `k` survivors adds `O(k log k)`. That is the bound while `k` is well below `n`. CPython does not hold to it at the extremes: it delegates to `min` when `k == 1`, and when `k` reaches `len(points)` it sorts the whole input instead, making the call `O(n log n)` exactly where a bounded heap would have stopped paying off anyway.

##### Space Complexity: `O(k)`

The heap holds `k` decorated triples of key, insertion order, and point, and the final sort runs over those same `k` entries. Nothing else scales with `n`, and the input list is never mutated, unlike Quickselect and Sort by Distance.

#### Key Insights

- This hides the bounded-heap mechanics that the Max-Heap of Size K section
  teaches: the negated key that turns `heapq` into a max-heap, the full-heap test, and the `heapreplace` eviction. Asked how `nsmallest` works, the earlier section is the answer you should be able to write from scratch.
- The one-liner is honest about cost only if you know the fallbacks: it is
  `O(n log k)` for small `k`, but degrades to a full sort once `k` approaches `n`, so it does not beat Sort by Distance in that regime.
- `nsmallest` sorts its survivors before returning, so the output is in
  ascending distance order rather than the arbitrary heap order of the manual version. The problem accepts either, but tests that compare against an ordered expectation will pass here and fail on the raw heap.
- The `key` callable is evaluated exactly once per point, so there is no hidden
  recomputation of the distance during heap comparisons, which is what keeps the lambda cheap enough to leave inline.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n * k)` - `k` selection rounds, each scanning up to `n` points.
- **Max-Heap of Size K**: `O(n log k)` - one bounded heap operation per point.
- **Quickselect**: `O(n)` average, `O(n^2)` worst case - partial
  in-place selection.
- **Sort by Distance**: `O(n log n)` - one comparison sort over all points.
- **Library One-Liner with `heapq.nsmallest`**: `O(n log k)` - the same bounded-heap sweep, falling back to an `O(n log n)` sort when `k` reaches `len(points)`.

### Space Complexity

- **Brute Force**: `O(n)` - a working copy of the points to remove from.
- **Max-Heap of Size K**: `O(k)` - the heap holds at most `k` points.
- **Quickselect**: `O(1)` - partitions the input in place.
- **Sort by Distance**: `O(n)` - Timsort's merge buffer can hold up to `n/2` elements; "in place" only means no second list of points.
- **Library One-Liner with `heapq.nsmallest`**: `O(k)` - `k` decorated triples of key, insertion order, and point, sorted in place at the end.

### Trade-offs

- Brute Force is the most self-evident to derive (find nearest, remove, repeat)
  but rescans the entire remaining list every round, wasting work when `k` is large.
- The heap gives a stable, predictable bound and never mutates the input, but
  carries a `log k` factor and `O(k)` extra space.
- Quickselect achieves linear average time and constant space but has a quadratic
  worst case and reorders the original array.
- Sorting is the shortest to write, but does full `O(n log n)` work even when `k`
  is tiny relative to `n`, and leans on the built-in sort to do the core selection.
- `heapq.nsmallest` gets the heap's `O(n log k)` bound and its non-mutating
  behaviour in one line, but pushes the selection mechanism out of sight, so it demonstrates nothing about how the bounded heap works.

### When to Use Each

- **Brute Force**: When `k` is tiny and clarity of derivation matters more than
  speed, or as a teaching baseline that selects by hand.
- **Max-Heap of Size K**: Streaming or very large `n` with small `k`, or when
  the input must not be modified and worst-case stability matters.
- **Quickselect**: When the whole array is in memory, average-case
  speed is the priority, and mutating the input is acceptable.
- **Sort by Distance**: When `n` is modest (as here, `n <= 10^4`) and the
  shortest correct code matters more than shaving the `log` factor.
- **Library One-Liner with `heapq.nsmallest`**: The Pythonic default for
  production code, where `k` is much smaller than `n` and the input must not be reordered. In an interview, write it after the Max-Heap version, not instead of it.

### Optimization Notes

- Always compare squared distances; computing `sqrt` adds floating-point cost and
  rounding risk for no benefit to the ordering.
- Brute Force is the intuitive baseline; the heap improves to `O(n log k)` when
  `k` is small, Quickselect reaches `O(n)` average by ordering only enough of the array to fix the `k`-th boundary, and Sort by Distance trades the extra `log` factor for the brevity of a built-in sort.
- `heapq.nsmallest` reaches the heap's `O(n log k)` bound with a smaller constant
  than the hand-written loop, because its comparison and eviction run in C rather than in Python bytecode.
- The one-liner's shortcuts matter when sizing it up: `k == 1` becomes a `min`
  scan, and `k >= len(points)` becomes a full sort, so its advantage over Sort by Distance exists only in the range where `k` is genuinely small.
