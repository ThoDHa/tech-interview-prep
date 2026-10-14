# [Squirrel Nut Collection Shortest Path](https://www.fastprep.io/problems/amazon-squirrel-nut-collection-shortest-path)

**Medium** | **NN minutes** | **Array, Greedy, Math**

A squirrel, a tree, and several nuts occupy distinct cells on a rectangular Manhattan grid. The squirrel can carry one nut at a time. Every nut must be delivered to the tree.

## Examples

### Example 1

**Input:** `tree = [2,2]`, `squirrel = [4,4]`, `nuts = [[3,0],[2,5]]`

**Output:** `12`

**Explanation:** Taking the nut at [2,5] first avoids any extra distance versus a tree round trip.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-squirrel-nut-collection-shortest-path; fill them in. -->

## Solutions

### Try Every First Nut

#### Derivation

The squirrel carries one nut at a time, so once the first nut is chosen the rest of the route is forced: after delivering that nut to the tree the squirrel stands at the tree, and every remaining nut is gathered on a tree round trip, `tree -> nut -> tree`. The route therefore has exactly one degree of freedom, the choice of the first nut, and `n` nuts give `n` candidate routes. The most literal reading of the problem simulates each candidate and keeps the shortest:

1. Define `manhattan_distance(first_cell, second_cell)` as the sum of the absolute row and column differences.
2. For each `first_position` in `nuts`, treat `nuts[first_position]` as the first nut and build the route: `manhattan_distance(squirrel, nuts[first_position]) + manhattan_distance(nuts[first_position], tree)` plus `2 * manhattan_distance(nuts[other_position], tree)` for every other `other_position`.
3. Track the smallest route in `shortest_route` and return it after all candidates are simulated.

#### Walkthrough

Let us simulate both candidates by hand on Example 1: `tree = [2,2]`, `squirrel = [4,4]`, `nuts = [[3,0],[2,5]]`. Each line gathers the candidate first, then rounds the tree for the other nut:

```text
candidate [3,0]   gather 1+4 = 5   deliver 1+2 = 3   round trip [2,5] = 2*(0+3) = 6   route = 14
candidate [2,5]   gather 2+1 = 3   deliver 0+3 = 3   round trip [3,0] = 2*(1+2) = 6   route = 12
shortest_route = min(14, 12) = 12
```

The shorter route gathers `[2,5]` first: walking from the squirrel to that nut costs exactly what the tree round trip would have cost, so nothing is wasted. The function returns `12`, matching the expected Output for Example 1.

#### Solution

The code is the candidate loop from the walkthrough: pick a first nut, add its gather and deliver legs, then add a round trip for every other nut.

```python
from typing import List


def manhattan_distance(first_cell: List[int], second_cell: List[int]) -> int:
    return abs(first_cell[0] - second_cell[0]) + abs(first_cell[1] - second_cell[1])


class Solution:
    def solve(self, tree: List[int], squirrel: List[int], nuts: List[List[int]]) -> int:
        shortest_route = None
        for first_position in range(len(nuts)):
            route = (manhattan_distance(squirrel, nuts[first_position])
                     + manhattan_distance(nuts[first_position], tree))
            for other_position in range(len(nuts)):
                if other_position != first_position:
                    route += 2 * manhattan_distance(nuts[other_position], tree)
            if shortest_route is None or route < shortest_route:
                shortest_route = route
        return shortest_route
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

Each of the `n` candidate first nuts triggers an inner scan over all `n` nuts, so the simulations cost `n × n` distance computations.

##### Space Complexity: `O(1)`

Only the running `route` and `shortest_route` scalars are stored, whatever the input size.

#### Key Insights

- The first nut is the only free choice; every other nut costs a fixed tree round trip, so the whole route is determined by that one decision.
- Exhaustive simulation stays polynomial, not factorial, because the choice collapses the remaining route into a fixed formula.
- The quadratic cost comes from rebuilding the round-trip total for every candidate, which is exactly the waste the next approach removes.

### Greedy First-Pick Savings

#### Derivation

The brute force recomputes the same round-trip total once per candidate. Comparing two candidate routes isolates what actually differs: gathering nut `nut` first replaces its tree round trip `2 * manhattan_distance(nut, tree)` with the walk `manhattan_distance(squirrel, nut) + manhattan_distance(nut, tree)`, and every other nut's round trip appears in both routes unchanged. The substitution changes the total by the saving `manhattan_distance(nut, tree) - manhattan_distance(squirrel, nut)`, so the best first nut is simply the nut with the largest saving, and one pass finds it:

1. Accumulate `round_trip_total`, the sum of `2 * manhattan_distance(nut, tree)` over all nuts: the route length if every trip could start at the tree.
2. In the same pass compute each nut's saving `manhattan_distance(nut, tree) - manhattan_distance(squirrel, nut)` and keep the maximum in `best_saving`.
3. Return `round_trip_total - best_saving`, the round-trip total minus the one substitution the squirrel is allowed to make.

#### Walkthrough

Let us compute the savings by hand on Example 1: `tree = [2,2]`, `squirrel = [4,4]`, `nuts = [[3,0],[2,5]]`:

```text
nut [3,0]   to tree 1+2 = 3   from squirrel 1+4 = 5   saving 3 - 5 = -2
nut [2,5]   to tree 0+3 = 3   from squirrel 2+1 = 3   saving 3 - 3 =  0
round_trip_total = 2*3 + 2*3 = 12
best_saving = max(-2, 0) = 0
answer = round_trip_total - best_saving = 12 - 0 = 12
```

Nut `[3,0]` sits behind the squirrel relative to the tree, so gathering it first would cost extra and its saving is negative. The best available first nut is `[2,5]` with saving `0`, which the page's Explanation describes as avoiding any extra distance versus a tree round trip. The function returns `12`, matching the expected Output for Example 1.

#### Solution

The code is the single pass from the walkthrough: one accumulator for the round trips, one for the best saving.

```python
from typing import List


def manhattan_distance(first_cell: List[int], second_cell: List[int]) -> int:
    return abs(first_cell[0] - second_cell[0]) + abs(first_cell[1] - second_cell[1])


class Solution:
    def solve(self, tree: List[int], squirrel: List[int], nuts: List[List[int]]) -> int:
        round_trip_total = 0
        best_saving = None
        for nut in nuts:
            distance_to_tree = manhattan_distance(nut, tree)
            round_trip_total += 2 * distance_to_tree
            saving = distance_to_tree - manhattan_distance(squirrel, nut)
            if best_saving is None or saving > best_saving:
                best_saving = saving
        return round_trip_total - best_saving
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass computes the round-trip contribution and the saving for each of the `n` nuts, two distance evaluations per nut.

##### Space Complexity: `O(1)`

The two accumulators `round_trip_total` and `best_saving` are constant extra space.

#### Key Insights

- The route decomposes into a fixed round-trip total plus one substitution, which turns route planning into picking a maximum saving.
- Savings may all be negative; taking the maximum still selects the least costly first nut, so no special case is needed.
- The two accumulators are independent, which is what lets a single pass produce the answer.

## Comparison of Solutions

### Time Complexity

- **Try Every First Nut**: `O(n²)` - each candidate first nut triggers a full rescan of the nut list.
- **Greedy First-Pick Savings**: `O(n)` - a single pass accumulates the round trips and the best saving together.

### Space Complexity

- **Try Every First Nut**: `O(1)` - two scalar accumulators regardless of input size.
- **Greedy First-Pick Savings**: `O(1)` - two scalar accumulators regardless of input size.

### Trade-offs

- Try Every First Nut is the direct transcription of the route rules and needs no algebra, but its quadratic rescan grows quickly with the number of nuts.
- Greedy First-Pick Savings requires the observation that only the first pick matters, but once stated it is shorter, single-pass, and just as easy to verify.

### When to Use Each

- **Try Every First Nut**: When the route rules are unclear or in flux, exhaustive simulation is the safest way to produce a trusted reference answer.
- **Greedy First-Pick Savings**: The choice for real inputs: it scales linearly and the saving formula doubles as the proof of correctness.

### Optimization Notes

- The local `distance_to_tree` serves two duties, the round-trip contribution and the saving term, so each nut costs exactly two absolute-difference sums.
- Only the magnitude of the best saving matters for the total, so the code never records which nut goes first; track the best position alongside `best_saving` when the route itself must be reported.
