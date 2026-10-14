# [Maximize Protected City Population](https://www.fastprep.io/problems/amazon-maximize-protected-city-population)

**Medium** | **NN minutes** | **Array, Greedy, Dynamic Programming**

You are given n cities arranged in a line. City i has population population[i] and may contain a security unit described by unit[i], where unit[i] = '1' means a unit is initially stationed in city i.

Each security unit may stay where it is, or if it is not in the first city, it may move exactly one city to the left. Every unit can move at most once.

After all moves are chosen, a city is protected if at least one security unit is stationed there. Return the maximum total population of all protected cities.

## Examples

### Example 1

**Input:** `population = [10, 5, 8, 9, 6]`, `unit = "01101"`

**Output:** `27`

**Explanation:** Move the unit from city 2 to city 1, keep the unit in city 3, and move the unit from city 5 to city 4. Cities 1, 3, and 4 are then protected, for a total population of 10 + 8 + 9 = 27.

### Example 2

**Input:** `population = [7, 4]`, `unit = "01"`

**Output:** `7`

**Explanation:** Move the only unit left from city 2 to city 1. Protecting city 1 yields the larger total population.

## Constraints

- `population.length = unit.length()`
- `unit contains only '0' and '1'`
- `Each security unit may move left by at most one city, and may move at most once.`

## Solutions

### Try Every Move Combination

#### Derivation

Each unit independently stays or moves one city left, so the full choice space is the product over units: `2^u` combinations for `u` units. The baseline evaluates each combination's protected set and keeps the maximum population total:

1. Enumerate the move bits for every unit.
2. For each combination, mark protected cities and sum their populations.
3. Return the best total.

#### Walkthrough

Example 1, `population = [10, 5, 8, 9, 6]`, `unit = "01101"`: units sit at cities 2, 3, and 5 (1-indexed). Moving 2 to 1 and 5 to 4 while 3 stays protects cities 1, 3, 4 for `10 + 8 + 9 = 27`; moving nothing protects 2, 3, 5 for 19; any other combination collides units or protects smaller totals. The expected 27 wins. Example 2, `[7, 4]`, `"01"`: staying protects city 2 (4); moving protects city 1 (7); the answer is 7.

#### Solution

```python
from itertools import product as bit_product
from typing import List


class Solution:
    def solve(self, population: List[int], unit: str) -> int:
        """Return the maximum protected population over all move choices.

        Time:  O(2^u * n) with u the unit count.
        Space: O(n) for the protected marks.
        """
        positions = [index for index, mark in enumerate(unit) if mark == "1"]
        best = 0
        for moves in bit_product((False, True), repeat=len(positions)):
            protected = set()
            for position, moved in zip(positions, moves):
                protected.add(position - 1 if moved and position > 0 else position)
            best = max(best, sum(population[city] for city in protected))
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^u * n)`

One full evaluation per move combination.

##### Space Complexity: `O(n)`

The protected set per evaluation.

#### Key Insights

- Units are independent actors; only the protected set they jointly form couples them.
- The first city's unit can never move, and two units landing on one city waste one of them.

### Chain Walk Over Unit Positions

#### Derivation

Scan units left to right. When the walker stands at the unit on city `index`, exactly one earlier decision can block a left move: the occupancy of city `index - 1`. That city is occupied precisely when the previously processed unit stayed (a mover from `index` would land on `index - 1` itself, and units further left can only occupy cities at most `index - 2`). So the whole history reduces to one carried value: the city the previous unit occupied. A recursion over unit positions with that carried value prices both options (stay on `index`, collecting `population[index]` and carrying `index` forward; or, when `index - 1` is free, move there, collecting `population[index - 1]` and carrying `index - 1`), and takes the maximum. With positions strictly increasing, each state is visited once, giving a linear walk:

1. Recurse over the next unit position, carrying the city the previous unit occupied.
2. Stay always exists; move exists when the previous unit did not occupy `index - 1`.
3. Memoize; the answer is the maximum over the first unit's options.

#### Walkthrough

Example 1, `[10, 5, 8, 9, 6]`, `"01101"` (0-indexed units at 1, 2, 4): at unit 1, moving collects 10 and carries city 0; at unit 2, city 1 is free (0 is occupied, 1 is not), so both options exist: staying collects 8, moving collects 5; the walk continues from each. At unit 4, city 3 is free in both branches: moving collects 9 versus staying 6. The best path is move, stay, move: `10 + 8 + 9 = 27`, matching. Example 2, `[7, 4]`, `"01"`: the unit at 1 sees city 0 free: moving collects 7 versus staying 4; the answer is 7.

#### Solution

```python
from functools import lru_cache
from typing import List


class Solution:
    def solve(self, population: List[int], unit: str) -> int:
        """Return the maximum protected population over all move choices.

        Time:  O(n): each unit position is resolved once with at most
            two options.
        Space: O(n) for the memo table.
        """

        @lru_cache(maxsize=None)
        def best(next_index: int, occupied_city: int) -> int:
            index = next_index
            while index < len(unit) and unit[index] != "1":
                index += 1
            if index == len(unit):
                return 0
            stay = population[index] + best(index + 1, index)
            if index > 0 and occupied_city != index - 1:
                move = population[index - 1] + best(index + 1, index - 1)
                return max(stay, move)
            return stay

        return best(0, -1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The scan advances monotonically; each unit position computes once (the carried city takes at most two values per position).

##### Space Complexity: `O(n)`

The memo table plus recursion depth.

#### Key Insights

- Occupancy of `index - 1` is decided solely by the previous unit's stay: movers land at most one city left, and previous-previous units sit at least two cities left.
- Carrying the occupied city (not a boolean) is what keeps the state exact: free versus occupied differs per target city.
- The recursion degenerates to a simple loop when written bottom-up over unit positions.

## Comparison of Solutions

### Time Complexity

- **Try Every Move Combination**: `O(2^u * n)` - the definition as search.
- **Chain Walk Over Unit Positions**: `O(n)`.

### Space Complexity

- **Try Every Move Combination**: `O(n)`.
- **Chain Walk Over Unit Positions**: `O(n)` memo, `O(1)` iterative.

### Trade-offs

- The enumeration is unarguably correct and costs exponential time.
- The chain walk needs the single-occupancy observation; once granted, it is one linear pass.

### When to Use Each

- **Try Every Move Combination**: unit tests as the oracle.
- **Chain Walk Over Unit Positions**: any real input.

### Optimization Notes

- A greedy that tracks only a boolean "previous stayed" flag is subtly wrong (a stayed unit two cities back frees the adjacent city without the flag knowing); the carried-city state is the minimal exact history.
- Bottom-up, the walk is two rolling values: the best totals ending with the previous unit at either of its two landing cities.
