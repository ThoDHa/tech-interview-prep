# [Largest Binary-String Subset Within Bit Budgets](https://www.fastprep.io/problems/amazon-binary-strings-bounded-subset)

**Medium** | **NN minutes** | **Array, String, Dynamic Programming**

Given an array of binary strings strs and two budgets, maxOnes and maxZeroes, return the maximum number of strings you can select.

The selected strings must contain at most maxOnes ones in total and at most maxZeroes zeroes in total. Each array position may be selected at most once, including when two positions contain equal strings.

## Examples

### Example 1

**Input:** `strs = ["100","10","1","11","111"]`, `maxOnes = 3`, `maxZeroes = 0`

**Output:** `2`

**Explanation:** Select "1" and "11". They use exactly three ones and no zeroes.

### Example 2

**Input:** `strs = ["10","0001","111001","1","0"]`, `maxOnes = 3`, `maxZeroes = 5`

**Output:** `4`

**Explanation:** The strings "10", "0001", "1", and "0" use three ones and five zeroes.

### Example 3

**Input:** `strs = ["10","0","1"]`, `maxOnes = 1`, `maxZeroes = 1`

**Output:** `2`

**Explanation:** Selecting "0" and "1" uses both budgets and yields two strings.

## Constraints

- `1 <= strs.length <= 600.`
- `1 <= strs[i].length <= 100.`
- `Every strs[i] contains only 0 and 1.`
- `0 <= maxOnes, maxZeroes <= 100.`

## Solutions

### Exhaustive Selection

#### Derivation

The most literal reading tries every subset of positions and keeps the
largest one inside both budgets. The include-or-exclude recursion makes the
enumeration systematic: standing at position `position`, either the string
there is skipped and the budgets pass through untouched, or it is taken,
its bit costs are subtracted from the budgets, and the count grows by one.
Checking the budgets at take time keeps every reached subset legal, so no
post-filtering is needed:

1. Define `best_from(position, ones_left, zeroes_left)`: the most strings
   selectable from `strs[position:]` under the remaining budgets. It returns
   `0` when `position` reaches the end of the array.
2. Compute `skipped = best_from(position + 1, ones_left, zeroes_left)`.
3. Count the string's bits: `one_count` ones and `zero_count` zeroes. When
   either exceeds the remaining budget, the string is unusable and
   `skipped` is the whole answer for this call.
4. Otherwise compare `skipped` against `1 + best_from(position + 1, ...)` on
   the reduced budgets and return the larger.
5. The answer is `best_from(0, maxOnes, maxZeroes)`.

#### Walkthrough

Trace the recursion on Example 3: `strs = ["10","0","1"]`, `maxOnes = 1`,
`maxZeroes = 1`. The bit costs are `"10"` -> one one and one zero, `"0"` ->
zero ones and one zero, `"1"` -> one one and zero zeroes:

```text
best_from(0, 1, 1)                      budgets: 1 one, 1 zero left
├── skip "10" -> best_from(1, 1, 1)
│     ├── skip "0" -> best_from(2, 1, 1)
│     │     ├── skip "1" -> 0
│     │     └── take "1" -> 1 + best_from(3, 0, 1) = 1
│     │     -> 1
│     └── take "0" -> 1 + best_from(2, 1, 0)
│           ├── skip "1" -> 0
│           └── take "1" -> 1 + best_from(3, 0, 0) = 1
│           -> 1
│     -> max(1, 1 + 1) = 2              "0" then "1"
└── take "10" -> 1 + best_from(1, 0, 0)
      ├── skip "0" -> best_from(2, 0, 0): take "1" needs 1 one -> 0
      └── take "0" rejected: its 1 zero exceeds the spent budget
      -> 1 + 0 = 1                       "10" alone
-> max(2, 1) = 2
```

Taking `"10"` spends both budgets on a single string, while skipping it
leaves room for `"0"` and `"1"` together. The root returns `2`, matching the
expected Output.

#### Solution

The code is the walkthrough's skip branch, the budget check, and the
take branch.

```python
from typing import List


class Solution:
    def largestBoundedSubset(self, strs: List[str], maxOnes: int,
                             maxZeroes: int) -> int:
        def best_from(position: int, ones_left: int,
                      zeroes_left: int) -> int:
            if position == len(strs):
                return 0

            skipped = best_from(position + 1, ones_left, zeroes_left)
            text = strs[position]
            one_count = text.count('1')
            zero_count = len(text) - one_count
            if one_count > ones_left or zero_count > zeroes_left:
                return skipped

            taken = 1 + best_from(position + 1, ones_left - one_count,
                                  zeroes_left - zero_count)
            return max(skipped, taken)

        return best_from(0, maxOnes, maxZeroes)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

Each of the `n` positions forks into a skip and a take branch, so the call
tree roughly doubles at every level; every call does constant work beyond
its recursion.

##### Space Complexity: `O(n)`

No table is kept, but the recursion stack reaches depth `n` along the
all-skip chain.

#### Key Insights

- Equal strings at different positions are independent choices: nothing in
  the recursion deduplicates `strs`, which is exactly the rule the statement
  states.
- The budget check at take time prunes illegal subsets for free; there is
  never a need to validate a finished subset.
- Correct but exponential: at the constraint cap of 600 strings the tree is
  unwalkable, which is what the rest of the page fixes.

### Top-Down Memoization

#### Derivation

The enumeration revisits the same situation through different orders: taking
string A then B and taking B then A land at the same position with the same
remaining budgets, yet the recursion re-explores everything after that point
twice. The state is small, though: the future depends only on
`(position, ones_left, zeroes_left)`, never on which strings produced the
budgets. [Memoization](https://en.wikipedia.org/wiki/Memoization) stores one
answer per state in a dictionary, so every distinct situation is solved once:

1. Keep the Exhaustive Selection recursion verbatim, base case included.
2. Before computing, check `memo` for the key
   `(position, ones_left, zeroes_left)` and return a stored answer.
3. Otherwise compute the skip/take maximum and store it under the key before
   returning.
4. The state space has `(n + 1) × (maxOnes + 1) × (maxZeroes + 1)` keys, so
   the exponential tree collapses to one body run per state.

#### Walkthrough

The official examples never revisit a state, so we use a tailored input that
does: `strs = ["1","1","1"]`, `maxOnes = 2`, `maxZeroes = 0`, three distinct
positions holding the same string. The expected best is any two of them.
Budgets after each take shrink by one one:

```text
decide(2, 2, 0)   skip -> 0; take -> 1 + decide(3, 1, 0) = 1    -> 1   miss
decide(2, 1, 0)   skip -> 0; take -> 1 + decide(3, 0, 0) = 1    -> 1   miss, stored
decide(2, 0, 0)   skip -> 0; take rejected: budget spent        -> 0   miss
decide(1, 2, 0)   skip -> decide(2, 2, 0) = 1
                  take -> 1 + decide(2, 1, 0) = 2               -> 2   miss
decide(1, 1, 0)   skip -> decide(2, 1, 0) = 1   ** memo hit **
                  take -> 1 + decide(2, 0, 0) = 1               -> 1   miss
decide(0, 2, 0)   skip -> decide(1, 2, 0) = 2
                  take -> 1 + decide(1, 1, 0) = 2               -> 2
```

The decisive beat is `decide(1, 1, 0)`'s skip branch: the state
`(2, 1, 0)` was already solved inside `decide(1, 2, 0)`'s take branch, and
the dictionary answers the second request without re-exploring position 2.
The root returns `2`, matching the expected best of two strings, and the
example also shows duplicates staying selectable as separate positions.

#### Solution

The code is the Exhaustive Selection recursion with the memo check and store
wrapped around the split.

```python
from typing import List


class Solution:
    def largestBoundedSubset(self, strs: List[str], maxOnes: int,
                             maxZeroes: int) -> int:
        memo = {}

        def best_from(position: int, ones_left: int,
                      zeroes_left: int) -> int:
            if position == len(strs):
                return 0
            key = (position, ones_left, zeroes_left)
            if key in memo:
                return memo[key]

            skipped = best_from(position + 1, ones_left, zeroes_left)
            text = strs[position]
            one_count = text.count('1')
            zero_count = len(text) - one_count
            best_here = skipped
            if one_count <= ones_left and zero_count <= zeroes_left:
                taken = 1 + best_from(position + 1,
                                      ones_left - one_count,
                                      zeroes_left - zero_count)
                best_here = max(skipped, taken)
            memo[key] = best_here
            return best_here

        return best_from(0, maxOnes, maxZeroes)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × maxOnes × maxZeroes)`

The memo admits each of the `(n + 1) × (maxOnes + 1) × (maxZeroes + 1)`
states into the body at most once, and each body run does constant work
beyond its two subcalls; at the constraint caps that is about
600 × 101 × 101 ≈ 6.1 million state visits.

##### Space Complexity: `O(n × maxOnes × maxZeroes)`

The memo holds one entry per reachable state, and the recursion stack adds
depth `n`.

#### Key Insights

- The position belongs in the state: without it, two identical strings would
  look interchangeable and one position could be spent twice.
- Memoization changes only the execution strategy; the skip/take logic reads
  exactly as it did in the Exhaustive Selection, which makes correctness
  easy to carry over.
- The recursion still descends to depth `n = 600`, safely inside Python's
  default recursion limit, but the Space-Optimized DP below removes the
  stack entirely.

### Bottom-Up DP

#### Derivation

The memoized recursion fills its memo in a discoverable order: layer by
layer over `position`, from the array's end back to its start. Watch the
order states are first computed and reproduce that order with a plain loop,
no recursion and no dictionary. [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming)
with tabulation keeps every layer explicitly, so the derivation of each
entry from the layer behind it is visible in the data:

1. Precompute each string's `(one_count, zero_count)` pair once.
2. Let `layers[i][o][z]` be the most strings selectable from the first `i`
   strings under budgets `o` ones and `z` zeroes; layer 0 is all zeros.
3. For each string, copy the previous layer, then overwrite every cell whose
   budgets cover the string's costs with the better of skipping and taking.
4. Return `layers[n][maxOnes][maxZeroes]`.

#### Recurrence

Let `layers[i][o][z]` be the most strings selectable from the first `i`
strings under budgets `o` ones and `z` zeroes, and let `ones_i` and
`zeroes_i` be the bit costs of `strs[i - 1]`, the string layer `i` admits:

$$ layers[i][o][z] = \begin{cases} 0, & i = 0 \\[4pt] \max\big(layers[i-1][o][z],\ 1 + layers[i-1][o - \text{ones}_i][z - \text{zeroes}_i]\big), & o \ge \text{ones}_i \text{ and } z \ge \text{zeroes}_i \\[4pt] layers[i-1][o][z], & \text{otherwise} \end{cases} $$

```text
layers[0][o][z] = 0
layers[i][o][z] = max(layers[i - 1][o][z],
                      1 + layers[i - 1][o - ones_i][z - zeroes_i])
                      when o >= ones_i and z >= zeroes_i
layers[i][o][z] = layers[i - 1][o][z]                   otherwise
```

The base case says no strings admit no selections. Each cell takes or skips
`strs[i - 1]` only: taking reads the previous layer at the reduced budgets,
so one position can never be spent twice. The answer is read from
`layers[n][maxOnes][maxZeroes]`.

#### Walkthrough

Fill the layers on Example 1: `strs = ["100","10","1","11","111"]`,
`maxOnes = 3`, `maxZeroes = 0`. Each layer is a column indexed by the ones
budget `o = 0, 1, 2, 3`; the zero budget has the single value `0`, which
disqualifies `"100"` (two zeroes) and `"10"` (one zero) outright:

```text
layer 0 (no strings)                     [0, 0, 0, 0]
layer 1  "100" cost (1,2)  skipped       [0, 0, 0, 0]
layer 2  "10"  cost (1,1)  skipped       [0, 0, 0, 0]
layer 3  "1"   cost (1,0)  take reads previous layer at o - 1:
           o=1: max(0, 1 + prev[0]) = 1
           o=2: max(0, 1 + prev[1]) = 1
           o=3: max(0, 1 + prev[2]) = 1  -> [0, 1, 1, 1]
layer 4  "11"  cost (2,0):
           o=2: max(1, 1 + prev[0]) = 1
           o=3: max(1, 1 + prev[1]) = 2  -> [0, 1, 1, 2]
layer 5  "111" cost (3,0):
           o=3: max(2, 1 + prev[0]) = 2  -> [0, 1, 1, 2]
```

The decisive update is layer 4 at `o = 3`: taking `"11"` adds one to the
best plan over the first three strings at budget `1` (which holds `"1"`),
reaching two strings where skipping kept one. Layer 5 cannot improve on
that: taking `"111"` spends all three ones for a single string. The final
entry `layers[5][3][0] = 2` matches the expected Output.

#### Solution

The code is the layer-by-layer fill from the walkthrough: copy the previous
layer, then improve every cell whose budgets cover the string's costs.

```python
from typing import List


class Solution:
    def largestBoundedSubset(self, strs: List[str], maxOnes: int,
                             maxZeroes: int) -> int:
        layers = [[[0] * (maxZeroes + 1) for _ in range(maxOnes + 1)]]
        for text in strs:
            one_count = text.count('1')
            zero_count = len(text) - one_count
            previous = layers[-1]
            layer = [row[:] for row in previous]
            for ones_budget in range(one_count, maxOnes + 1):
                for zeroes_budget in range(zero_count, maxZeroes + 1):
                    layer[ones_budget][zeroes_budget] = max(
                        previous[ones_budget][zeroes_budget],
                        1 + previous[ones_budget - one_count]
                            [zeroes_budget - zero_count])
            layers.append(layer)
        return layers[-1][maxOnes][maxZeroes]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × maxOnes × maxZeroes)`

Each of the `n` strings triggers one sweep over `(maxOnes + 1) ×
(maxZeroes + 1)` cells with constant work per cell.

##### Space Complexity: `O(n × maxOnes × maxZeroes)`

Every layer is kept; at the constraint caps that is about 6.1 million
integers, which the Space-Optimized DP cuts down next.

#### Key Insights

- The table is the memo turned upright: same states, same values, filled in
  the order the recursion discovered them, with the whole layer history on
  hand.
- Keeping every layer costs a factor of `n` in space, but it is what makes
  variants answerable (for example, the best count under smaller budgets,
  or over a prefix of the strings).
- Strings whose bit costs exceed both budgets' relevant dimension are
  handled by the loop ranges starting at the costs: their layers are pure
  copies, which is the tabulated form of the take-time budget check.

### Space-Optimized DP

#### Derivation

The layer loop reads only `layers[i - 1]` while writing `layers[i]`, so
every layer except the previous one is dead weight once computed. The whole
stack collapses onto a single table `best` if one discipline holds: process
the budgets in descending order inside each string's sweep, so every
`best[o - one_count][z - zero_count]` read still holds the previous layer's
value. An ascending sweep would read cells already overwritten this round,
letting the same string be counted twice:

1. Allocate `best`, an `(maxOnes + 1) × (maxZeroes + 1)` table of zeros.
2. For each string, sweep `ones_budget` from `maxOnes` down to `one_count`
   and `zeroes_budget` from `maxZeroes` down to `zero_count`.
3. In each cell, take the better of keeping `best[o][z]` and
   `1 + best[o - one_count][z - zero_count]`; the descending order makes
   the read behave like the previous layer.
4. After the last string, `best[maxOnes][maxZeroes]` is the answer.

#### Walkthrough

Roll the single table through Example 1: `strs = ["100","10","1","11","111"]`,
`maxOnes = 3`, `maxZeroes = 0`. As before the zero budget is pinned at `0`,
so each table prints as one column over `o = 0, 1, 2, 3`, and `"100"` and
`"10"` never enter their sweeps:

```text
start                      best = [0, 0, 0, 0]
"1"   cost (1,0)  sweep o = 3, 2, 1 descending:
     o=3: 1 + best[2] = 1 -> best[3] = 1
     o=2: 1 + best[1] = 1 -> best[2] = 1
     o=1: 1 + best[0] = 1 -> best[1] = 1
     best = [0, 1, 1, 1]
"11"  cost (2,0)  sweep o = 3, 2:
     o=3: 1 + best[1] = 2 -> best[3] = 2
     o=2: 1 + best[0] = 1 -> best[2] stays 1
     best = [0, 1, 1, 2]
"111" cost (3,0)  sweep o = 3:
     o=3: 1 + best[0] = 1 < 2 -> best[3] stays 2
     best = [0, 1, 1, 2]
```

The descending sweep is what makes the `"1"` update safe: at `o = 3` the
read `best[2]` still holds `0` from before the sweep, so the string is
counted once. Sweeping ascending would instead update `best[1]` first and
then read it at `o = 2`, claiming two strings from the single `"1"`
position. The final table ends at `best[3][0] = 2`, matching the expected
Output and every entry of the Bottom-Up DP's last layer.

#### Solution

The code is the walkthrough's per-string sweep: descending budgets, one
max per cell, one table forever.

```python
from typing import List


class Solution:
    def largestBoundedSubset(self, strs: List[str], maxOnes: int,
                             maxZeroes: int) -> int:
        best = [[0] * (maxZeroes + 1) for _ in range(maxOnes + 1)]
        for text in strs:
            one_count = text.count('1')
            zero_count = len(text) - one_count
            for ones_budget in range(maxOnes, one_count - 1, -1):
                for zeroes_budget in range(maxZeroes, zero_count - 1, -1):
                    taken = 1 + best[ones_budget - one_count] \
                                    [zeroes_budget - zero_count]
                    best[ones_budget][zeroes_budget] = max(
                        best[ones_budget][zeroes_budget], taken)
        return best[maxOnes][maxZeroes]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × maxOnes × maxZeroes)`

One sweep over the budget table per string, constant work per cell; the
loop ranges starting at the string's costs only shrink the constant.

##### Space Complexity: `O(maxOnes × maxZeroes)`

The single `best` table, independent of how many strings stream through;
at the constraint caps that is 101 × 101 ≈ 10 thousand integers.

#### Key Insights

- Descending budget order is the entire trick: it turns "read the previous
  layer" into "read cells this sweep has not reached yet", which is why one
  table can stand in for all `n + 1` layers.
- The reverse is the hazard to remember: an ascending sweep over budgets
  lets one string contribute twice, the classic 0/1 knapsack bug, and it
  produces plausible-looking wrong answers.
- This is the optimal trade for the single-query problem: the layered table
  buys reusable per-prefix answers that this version deliberately gives up.

## Comparison of Solutions

### Time Complexity

- **Exhaustive Selection**: `O(2^n)` - the skip/take tree doubles at every
  one of the `n` positions.
- **Top-Down Memoization**: `O(n × maxOnes × maxZeroes)` - one body run per
  `(position, budget)` state.
- **Bottom-Up DP**: `O(n × maxOnes × maxZeroes)` - one full budget-table
  sweep per string.
- **Space-Optimized DP**: `O(n × maxOnes × maxZeroes)` - the same sweeps
  over one shared table.

### Space Complexity

- **Exhaustive Selection**: `O(n)` - recursion stack only.
- **Top-Down Memoization**: `O(n × maxOnes × maxZeroes)` - one memo entry
  per state plus the stack.
- **Bottom-Up DP**: `O(n × maxOnes × maxZeroes)` - every layer kept.
- **Space-Optimized DP**: `O(maxOnes × maxZeroes)` - a single budget table.

### Trade-offs

- **Exhaustive Selection** transcribes the statement directly and serves as
  the correctness oracle, but its time is unrunnable past small inputs.
- **Top-Down Memoization** keeps the skip/take recursion readable and pays
  only for reachable states, at the price of memo bookkeeping and stack
  depth `n`.
- **Bottom-Up DP** removes the recursion and keeps the full layer history,
  which only variants that query other layers can use.
- **Space-Optimized DP** reaches the table's floor size, but the descending
  sweep discipline is a correctness requirement, not a style choice.

### When to Use Each

- **Exhaustive Selection**: as the derivational baseline and a correctness
  oracle for checking the faster versions on small inputs.
- **Top-Down Memoization**: when the recursive formulation is easiest to
  trust and inputs stay modest.
- **Bottom-Up DP**: when follow-up queries need answers for other layers or
  reduced budgets.
- **Space-Optimized DP** (recommended): the default for the stated
  constraints; the same linear-in-states time at the minimum table size.

### Optimization Notes

- Strings whose costs exceed a budget outright can be filtered before the
  main loop; the sweeps already skip them via their loop ranges, but
  dropping them upfront shrinks the string count that drives the time
  bound.
- The bit counts are recomputed per string in each solution's single pass
  over `strs`; hoisting them into a precomputed list matters only when the
  same counts are needed more than once.
- The state count `(maxOnes + 1) × (maxZeroes + 1)` is what tames the
  problem: budgets are capped at 100, so about 10 thousand cells absorb any
  string length up to 100; without budget caps the problem would be
  intractable.
- A common pitfall is iterating budgets ascending in the in-place table;
  the Space-Optimized walkthrough shows exactly how that counts one string
  twice.
