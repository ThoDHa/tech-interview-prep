# [Shortest Distance on a Circular Bus Route](https://www.fastprep.io/problems/amazon-shortest-distance-circular-bus-route)

**Easy** | **NN minutes** | **Array, Prefix Sum**

For this exercise, assume a bus route has n stops arranged in a circle. The array distance contains the distance from stop i to stop (i + 1) mod n.

Given two distinct stops, start and destination, return the shorter travel distance between them. A bus may travel clockwise or counterclockwise around the circle.

## Examples

### Example 1

**Input:** `distance = [1,2,3,4]`, `start = 0`, `destination = 2`

**Output:** `3`

**Explanation:** Clockwise travel from stop 0 to stop 2 costs 1 + 2 = 3. The other direction costs 4 + 3 = 7, so the answer is 3.

### Example 2

**Input:** `distance = [7,10,1,12]`, `start = 1`, `destination = 3`

**Output:** `11`

**Explanation:** Travel through stops 1 -> 2 -> 3 costs 10 + 1 = 11. The opposite direction costs 12 + 7 = 19.

## Constraints

- `2 <= distance.length <= 100000`
- `1 <= distance[i] <= 10000`
- `0 <= start, destination < distance.length`
- `start != destination`

## Solutions

### Two Directional Walks

#### Derivation

The most literal reading asks the bus to actually travel: walk the edge list clockwise from `start` until `destination` is reached, then walk counterclockwise the same way, and keep the cheaper total. Counterclockwise needs care because `distance` stores only clockwise edges, but the circle is symmetric: reversing direction from `start` is the same as walking clockwise from `destination` back around to `start`, so the reverse trip reuses the same forward stepping with the endpoints exchanged:

1. Define `walk_distance(source, target)` that sums `distance[position]` from
   `source` up to (but not including) `target`, stepping `position` forward
   with the modulo wrap `(position + 1) % n`.
2. Compute `clockwise = walk_distance(start, destination)`.
3. Compute `counterclockwise = walk_distance(destination, start)`.
4. Return the smaller of the two.

#### Walkthrough

Example 1, `distance = [1,2,3,4]`, `start = 0`, `destination = 2`, so `n = 4`:

```text
clockwise      walk 0 -> 1 -> 2     1 + 2            = 3
counterclockwise  walk 2 -> 3 -> 0     3 + 4            = 7
return         min(3, 7) = 3
```

Each walk adds `distance[position]` before advancing `position = (position + 1) % n`, so the wrap from stop 3 back to stop 0 contributes `distance[3] = 4` to the reverse trip. The minimum is `3`, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, distance: List[int], start: int, destination: int) -> int:
        stop_count = len(distance)

        def walk_distance(source: int, target: int) -> int:
            total = 0
            position = source
            while position != target:
                total += distance[position]
                position = (position + 1) % stop_count
            return total

        return min(walk_distance(start, destination), walk_distance(destination, start))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The two walks cover disjoint arcs that together touch every stop exactly once, so the total stepping is at most `n`.

##### Space Complexity: `O(1)`

Only the running total and the walking position.

#### Key Insights

- A circle has exactly two routes between two stops, and the two arcs partition the circle, so together they cost the full loop and each is at most half of it.
- Counterclockwise travel is never encoded directly: swapping the endpoints and walking forward is the same trip in reverse.
- The modulo wrap `(position + 1) % n` is the whole circular structure; nothing else in the code knows the stops form a ring.

### Total-Loop Minus One Arc

#### Derivation

The two walks each pay for their arc, but the arcs are complements: the counterclockwise distance is the whole loop minus the clockwise one. Summing the edge list once fixes the loop length, and then only the clockwise arc has to be walked, because its complement falls out of a subtraction. This cannot beat the constant factor asymptotically (both stay `O(n)`), but it halves the walking and removes the second call. The observation generalizing it is prefix-sum thinking: any arc sum on a circle is a difference of two loop totals:

1. Compute `total_loop = sum(distance)`.
2. Normalize so the walk always goes up and around: when `start > destination`,
   swap the two endpoints, which just renames the clockwise arc.
3. Walk `position` from `start` to `destination` summing
   `clockwise_arc = distance[position]` per step (no wrap occurs after the
   swap, since `start <= destination`).
4. Return `min(clockwise_arc, total_loop - clockwise_arc)`.

#### Walkthrough

Example 2, `distance = [7,10,1,12]`, `start = 1`, `destination = 3`. The loop total is `7 + 10 + 1 + 12 = 30`:

```text
total_loop     = 30
clockwise_arc  = distance[1] + distance[2] = 10 + 1 = 11
complement     = 30 - 11 = 19
return         min(11, 19) = 11
```

The complement `19` is exactly the reverse trip `distance[3] + distance[0] = 12 + 7` from the statement's explanation: subtracting the walked arc leaves precisely the edges the reverse direction would have used. The minimum is `11`, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, distance: List[int], start: int, destination: int) -> int:
        total_loop = sum(distance)
        if start > destination:
            start, destination = destination, start

        clockwise_arc = 0
        for position in range(start, destination):
            clockwise_arc += distance[position]

        return min(clockwise_arc, total_loop - clockwise_arc)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass sums the loop and one pass walks the shorter index range, together touching every edge a constant number of times.

##### Space Complexity: `O(1)`

The loop total and the walking total.

#### Key Insights

- The two rival distances are complements, so computing one gives the other by subtraction from the loop total: only one arc ever needs walking.
- The endpoint swap is safe because the problem is symmetric under exchanging the two stops; the counterclockwise trip from `start` becomes the clockwise trip from `destination` after the swap.
- `sum(distance)` is the one-pass loop total; for repeated queries on the same route, a prefix-sum array would answer each query in `O(1)` instead of `O(n)`.

## Comparison of Solutions

### Time Complexity

- **Two Directional Walks**: `O(n)` - the two arcs partition the circle, so every edge is stepped over at most once across both walks.
- **Total-Loop Minus One Arc**: `O(n)` - one summing pass plus one walked arc, still linear but touching each edge at most once with a smaller constant.

### Space Complexity

- **Two Directional Walks**: `O(1)` - a running total and the walking position.
- **Total-Loop Minus One Arc**: `O(1)` - the loop total and the arc total.

### Trade-offs

- **Two Directional Walks**: mirrors the problem statement trip by trip, with no total to maintain, but it walks both arcs when the second is derivable.
- **Total-Loop Minus One Arc**: computes half the walking and states the complement identity explicitly, at the price of trusting the subtraction instead of watching both trips complete.

### When to Use Each

- **Total-Loop Minus One Arc (Recommended)**: the standard interview answer, since the complement identity is the insight the problem is testing.
- **Two Directional Walks**: as a first working answer or when the code should read exactly like the bus moves; it is also the natural base for variants where the reverse arc is not simply the complement (one-way segments, tolls per direction).

### Optimization Notes

- Many queries over one fixed route turn the page into a prefix-sum problem: prefix sums over a doubled `distance` array answer each start-to-destination query in `O(1)` after `O(n)` preprocessing.
- The endpoint swap keeps the walk inside a single index range with no modulo in the loop; without it, a wrapped arc (start near the end, destination near the front) would need the modular stepping of the first solution.
