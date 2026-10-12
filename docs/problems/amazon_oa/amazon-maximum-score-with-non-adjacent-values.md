# [Maximum Score With Non-Adjacent Values](https://www.fastprep.io/problems/amazon-maximum-score-with-non-adjacent-values)

**unknown difficulty** | **NN minutes** | **unknown categories**

You are given a list of integers nums. You may choose any set of values from the list.

If you choose a value x, then you cannot choose x - 1 or x + 1. When you choose x, your score increases by x * frequency(x), where frequency(x) is the number of times x appears in nums.

Return the maximum score you can obtain.

## Examples

### Example 1

**Input:** `nums = [3,4,2]`

**Output:** `6`

**Explanation:** Choose values 2 and 4 for score 2 + 4 = 6. Choosing 3 would block both.

### Example 2

**Input:** `nums = [2,2,3,3,3,4]`

**Output:** `9`

**Explanation:** Choosing value 3 gives score 3 * 3 = 9, which is better than choosing 2 and 4 for score 8.

## Constraints

- `nums.length >= 1`

## Solutions

### Brute Force

#### Derivation

The statement is a permission slip, "you may choose any set of values", so the most literal reading enumerates the sets. Enumerating subsets of `nums` by position would even count the same value selection several times (the two 2s in `[2, 2, 3]` give two indistinguishable ways to pick `2` and `3`), and the score only depends on which *values* are chosen: choosing `x` banks `x * frequency(x)` and forbids `x - 1` and `x + 1`. Collapsing the list into a frequency table and walking the distinct values in sorted order turns the choice into a recursion with one clean binary split per distinct value:

1. Build `frequency = Counter(nums)` and `distinct_values = sorted(frequency)`.
2. Define `decide(value_position)` as the best score obtainable from
   `distinct_values[value_position:]` alone.
3. Skip branch: `decide(value_position + 1)`, leaving this value unchosen.
4. Take branch: `take + decide(next_position)` where
   `take = value * frequency[value]` and `next_position` is the first position
   past every value adjacent to `value` (each differing from it by exactly `1`).
5. Return `max(skip, take + decide(next_position))`, with `decide` returning
   `0` past the end of `distinct_values`; the answer is `decide(0)`.

Nothing is cached, so the two branches re-enumerate overlapping suffixes and the recursion is exponential in the number of distinct values.

#### Walkthrough

Trace Example 1: `nums = [3, 4, 2]`, so `distinct_values = [2, 3, 4]` with `frequency` `1` each. The entry call is `decide(0)`; each call splits into its skip branch and its take branch, and the take branch jumps past adjacent values:

```text
decide(0)  value 2
├── skip: decide(1)  value 3
│     ├── skip: decide(2)  value 4
│     │     ├── skip: decide(3) -> 0        past the end
│     │     └── take: 4 + decide(3) = 4
│     │     -> decide(2) = max(0, 4) = 4
│     ├── take: 3 + decide(3) = 3           (adjacent 4 jumped, left unchosen)
│     -> decide(1) = max(4, 3) = 4
└── take: 2 + decide(2) = 2 + 4 = 6         (adjacent 3 jumped, 4 still allowed)
-> decide(0) = max(4, 6) = 6
```

The winning branch takes `2`, jumps the adjacent `3`, and takes `4`: score `6`, matching the expected Output for Example 1. The trace also exposes the recursion's flaw: `decide(2)` is computed twice (under `decide(0)`'s skip branch and under its take branch), `decide(3)` appears three times, and on longer inputs the overlap explodes combinatorially.

#### Solution

The code is the walkthrough's two branches with the adjacent-value jump between them.

```python
from collections import Counter
from typing import List


class Solution:
    def maximumNonAdjacentValueScore(self, nums: List[int]) -> int:
        frequency = Counter(nums)
        distinct_values = sorted(frequency)
        total_distinct = len(distinct_values)

        def decide(value_position: int) -> int:
            if value_position == total_distinct:
                return 0
            value = distinct_values[value_position]
            skip = decide(value_position + 1)
            take = value * frequency[value]
            next_position = value_position + 1
            while (next_position < total_distinct
                   and distinct_values[next_position] - value == 1):
                next_position += 1
            return max(skip, take + decide(next_position))

        return decide(0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^d)`

For the `d` distinct values, every call forks into two branches, and when no two distinct values are adjacent the while-loop never skips, so the call tree grows like the Fibonacci recurrence, exponential in `d`; building the frequency table and sorting contribute the `O(n + d log d)` preprocessing.

##### Space Complexity: `O(n + d)`

The frequency table holds one entry per distinct value (at most `n`), and the recursion stack reaches depth `d` along the all-skip chain.

#### Key Insights

- Choosing a value `x` blocks exactly the values `x - 1` and `x + 1`, never an entire range, so the "non-adjacent" structure lives on the sorted distinct values, not on the original array positions.
- Frequency collapsing is what makes the recursion well-formed: duplicates of `x` are never a dilemma, since taking one effectively takes all of them (they block the same neighbors and pay out together).
- The recursion is correct but recomputes each suffix once per route reaching it; the waste is the same prefix-recomputation pattern the memoized House Robber ladder attacks.

### Bottom-Up DP over Value Points

#### Derivation

The brute force's suffix question, "what is the best score from `distinct_values[value_position:]`?", is answered from scratch by every route that reaches it. [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) with tabulation removes the waste by flipping the direction: answer the shortest suffixes first and build upward. Seen from the array's start, the table is one number per distinct value: the best score using values up to and including this one, with the take branch reading a compatible prefix and the skip branch reading the immediately previous one:

1. Build `frequency` and `distinct_values` as before.
2. Let `best_through[value_position]` be the best score over the values
   `distinct_values[0..value_position]`, seeded with
   `best_through[0] = value * frequency[value]` for the first distinct value.
3. For each next distinct value: when its gap to the previous distinct value is
   at least `2`, nothing conflicts, so its best is its own take plus the whole
   previous best; when the gap is exactly `1`, taking it discards the previous
   entry, and the best is `max` of skipping (previous best) and taking (entry
   before the previous, plus the take).
4. Return the last entry, the best over all distinct values.

A gap of `2` or more (for example values `2` and `4` with no `3` chosen) is conflict-free because choosing `x` blocks only `x - 1` and `x + 1`; this is the same reduction the [House Robber](../house_robber.md) ladder applies, with value points standing in for houses.

#### Recurrence

Let `best_through[value_position]` be the best score over `distinct_values[0..value_position]`, let `take = value * frequency[value]` at `value = distinct_values[value_position]`, and let `gap = value - distinct_values[value_position - 1]`:

$$ \text{best\_through}[\text{value\_position}] = \begin{cases} \text{take}, & \text{value\_position} = 0 \\[4pt] \text{best\_through}[\text{value\_position} - 1] + \text{take}, & \text{gap} \ge 2 \\[4pt] \max(\text{best\_through}[\text{value\_position} - 1],\ \text{best\_through}[\text{value\_position} - 2] + \text{take}), & \text{gap} = 1 \end{cases} $$

```text
best_through[0] = take                                  first distinct value
best_through[i] = best_through[i - 1] + take            gap to i - 1 is >= 2
best_through[i] = max(best_through[i - 1],
                      best_through[i - 2] + take)       gap to i - 1 is 1
answer = best_through[last]
```

The first row is the base case: one distinct value in play, its take is the whole answer. The middle row is the reward for a gap of `2` or more: with no forbidden neighbor between the value points, the take stacks on top of the previous best. The last row is the House Robber split: taking `value` retires the adjacent previous value but keeps everything through the one before it, so the entry two back resurfaces. The answer is read from the last entry, which covers every distinct value.

#### Walkthrough

Trace Example 2: `nums = [2, 2, 3, 3, 3, 4]`, so `frequency` is `2 -> 2`, `3 -> 3`, `4 -> 1` and `distinct_values = [2, 3, 4]`. Each row fills one entry:

```text
value 2   take = 2 * 2 = 4   first value   best_through[0] = 4
value 3   take = 3 * 3 = 9   gap = 1       max(best_through[0], 0 + 9)
                                           = max(4, 9) = 9
value 4   take = 4 * 1 = 4   gap = 1       max(best_through[1], best_through[0] + 4)
                                           = max(9, 8) = 9
```

At value `3` the take branch wins: `9` from taking all three 3s beats `4` from the 2s. At value `4` the skip branch wins: stacking `4` on the 2s' `4` gives only `8`, below the standing `9`. The last entry is `9`, matching the expected Output for Example 2, the score of choosing value `3` alone. (Example 1 runs the same way and returns `6`.)

#### Solution

The code is the table fill from the recurrence: seed the first entry, then one `max` per distinct value.

```python
from collections import Counter
from typing import List


class Solution:
    def maximumNonAdjacentValueScore(self, nums: List[int]) -> int:
        frequency = Counter(nums)
        distinct_values = sorted(frequency)
        best_through = [0] * len(distinct_values)

        for value_position, value in enumerate(distinct_values):
            take = value * frequency[value]
            if value_position == 0:
                best_through[value_position] = take
                continue
            gap = value - distinct_values[value_position - 1]
            if gap >= 2:
                best_through[value_position] = best_through[value_position - 1] + take
            else:
                best_through[value_position] = max(
                    best_through[value_position - 1],
                    best_through[value_position - 2] + take,
                )

        return best_through[-1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + d log d)`

Counting the `n` values is linear, sorting the `d` distinct values is `O(d log d)`, and the table fill is one constant-time `max` per distinct value; since `d <= n`, the sort term dominates, and the whole run is a single ordered pass with no exponential branching.

##### Space Complexity: `O(n + d)`

The frequency table holds at most `n` entries and the `best_through` table exactly `d`.

#### Key Insights

- Sorting folds the whole constraint into one comparison: after sorting, the only value that can conflict with `value` is its immediate sorted neighbor, so a single `gap` check replaces any adjacency search.
- The `gap >= 2` branch is the piece the plain House Robber recurrence lacks: on the value line, unoccupied points do not conflict, so non-adjacent values stack freely instead of forcing a skip decision.
- Duplicates never appear in the table because they were priced into `take` up front: `value * frequency[value]` is the all-or-nothing deal for that value, and it is always worth taking in full when the value is taken at all.

### Space-Optimized DP

#### Derivation

The table loop reads only the two entries just below the one it writes: `best_through[value_position - 1]` and `best_through[value_position - 2]`. Everything older is dead weight, so the array collapses into two rolling totals, `one_back` standing for the previous entry and `two_back` for the one before it, with the gap branch deciding whether the take stacks on `one_back` (big gap) or must fall back to `two_back` (adjacent values):

1. Seed `one_back = 0` and `two_back = 0`: no values considered, no score.
2. For each distinct `value` in sorted order, compute
   `take = value * frequency[value]`; when the gap to the previous distinct
   value is at least `2` (or this is the first value),
   `best_here = one_back + take`; when the gap is exactly `1`,
   `best_here = max(one_back, two_back + take)`.
3. Shift the window: `two_back = one_back`, then `one_back = best_here`.
4. After the last distinct value, `one_back` holds the answer.

#### Walkthrough

Let us roll the two totals through Example 1: `nums = [3, 4, 2]`, so `frequency` is `1` per value and `distinct_values = [2, 3, 4]`:

```text
value 2   take 2   first value  best_here = 0 + 2 = 2   -> one_back 2, two_back 0
value 3   take 3   gap 1        best_here = max(2, 0 + 3) = 3
                                              -> one_back 3, two_back 2
value 4   take 4   gap 1        best_here = max(3, 2 + 4) = 6
                                              -> one_back 6, two_back 3
```

At value `3` the take branch wins (`3` beats `2`), retiring the 2s for the moment; at value `4` the two-back branch wins: `two_back + 4 = 6` revives the 2s and stacks the 4 on top, since values `2` and `4` do not conflict. The final `one_back` holds `6`, matching the expected Output for Example 1, the score of choosing values `2` and `4`. Each row reproduces exactly one `best_through` entry from the Bottom-Up recurrence.

#### Solution

The code is the walkthrough's three lines per value: combine, then shift the window.

```python
from collections import Counter
from typing import List


class Solution:
    def maximumNonAdjacentValueScore(self, nums: List[int]) -> int:
        frequency = Counter(nums)
        distinct_values = sorted(frequency)
        one_back = 0
        two_back = 0
        previous_value = None

        for value in distinct_values:
            take = value * frequency[value]
            if previous_value is not None and value - previous_value == 1:
                best_here = max(one_back, two_back + take)
            else:
                best_here = one_back + take
            two_back = one_back
            one_back = best_here
            previous_value = value

        return one_back
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + d log d)`

The same single pass as the Bottom-Up DP: one max, one take product, and two assignments per distinct value, plus the shared counting and sorting.

##### Space Complexity: `O(n + d)`

The frequency table is the only structure left (one entry per distinct value, at most `n`); the score state itself is two totals and the previous value, constant beyond the counting.

#### Key Insights

- A two-entry window is always sufficient because the constraint reaches exactly one value point back: adjacency to `value - 1` is the only interaction, so `dp[i - 2]` is the deepest lookup the recurrence ever needs.
- The gap branch preserves the two-back entry's meaning: `two_back` is the best through the value before the previous one, which is precisely the prefix a take may legally stack onto when the immediate predecessor is skipped.
- Seeding both totals at `0` installs the recurrence's virtual entries before the first value, so the first distinct value flows through the same `gap`-free branch as every gap-`>= 2` step and no length guard is needed.
- This is the optimal trade for the single-query problem: the explicit table buys reusable per-value-point answers that this version deliberately gives up; the sort's `O(d log d)` remains the true lower bound driver either way.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(2^d)` - the recursion forks per distinct value and shares no work between routes, exponential in `d` distinct values.
- **Bottom-Up DP over Value Points**: `O(n + d log d)` - linear counting, a sort of the `d` distinct values, and one constant-time step per value point.
- **Space-Optimized DP**: `O(n + d log d)` - the identical pass with two totals instead of a table.

### Space Complexity

- **Brute Force**: `O(n + d)` - frequency table plus a recursion stack of depth `d`.
- **Bottom-Up DP over Value Points**: `O(n + d)` - the frequency table plus the `best_through` table.
- **Space-Optimized DP**: `O(n + d)` - the frequency table dominates; the score state is constant.

### Trade-offs

- **Brute Force**: the direct transcription of the rules and a correctness oracle for small inputs, but unusable at scale: an adjacency-free input doubles the tree at every distinct value.
- **Bottom-Up DP over Value Points**: exact and polynomial, and the table keeps every prefix's best score for follow-up queries, at the price of one array entry per distinct value.
- **Space-Optimized DP**: exact with the same asymptotics and constant score state, giving up random access to old prefix answers that single-query runs never need.

### When to Use Each

- **Brute Force**: as the derivational baseline and an oracle for hand-checking the DP on tiny inputs; never for constraint-sized inputs.
- **Bottom-Up DP over Value Points (Recommended)**: the interview default; one sorted pass, a recurrence you can state cleanly, and the table to answer variant questions like the best score over a bounded value range.
- **Space-Optimized DP**: when the answer alone is wanted and memory pressure is real; the rolling window is the same recurrence with the array deleted.

### Optimization Notes

- The `gap >= 2` stacking branch is where this recurrence deliberately leaves House Robber's shape: with no forbidden neighbor between the value points, the take stacks straight onto `one_back` instead of falling back two entries. Because `best_through` never decreases, the uniform `max(one_back, two_back + take)` returns the same numbers even on wide gaps; the explicit branch keeps the reasoning tied to the constraint instead of leaning on that monotonicity.
- Adding a `@functools.cache` on the brute force's `decide` reproduces the memoized run in `O(d)` time and is the quickest bridge from the recursion to the table; the hand-rolled ladder on the [House Robber](../house_robber.md) page shows the technique step by step.
- A common pitfall is iterating raw `nums` positions instead of distinct values: the constraint is on values, so unsorted iteration breaks the "only the neighbor conflicts" property that the sort buys.
- With values bounded by `V`, a counting sort of the value points would drop the `d log d` sort term to `O(V + n)`; for unbounded values the comparison sort stands.
