# [Minimum Merge Conflicts](https://www.fastprep.io/problems/amazon-minimum-merge-conflicts)

**Hard** | **NN minutes** | **Dynamic Programming, String**

Developers want to merge two source-control branches into one unified branch while preserving the relative order of commits from each branch.

Each branch is represented by a lowercase string. Each character represents a commit priority, where a lower alphabetical character has higher priority.

A conflict occurs when, in the merged branch, a lower-priority commit appears before a higher-priority commit. In other words, for positions i < j in the merged string, there is a conflict when merged[i] > merged[j].

Return the minimum possible number of conflicts over all valid merges of primary and secondary.

A valid merge must contain every character from both branches and preserve the original order within each input branch.

## Examples

### Example 1

**Input:** `primary = "zc"`, `secondary = "d"`

**Output:** `2`

**Explanation:** Valid merges include:

zcd with 2 merge conflicts (z being lower priority is placed before higher priority commits c and d).Similarly, zdc with 3 merge conflicts.Similarly, dzc with 2 merge conflicts.The minimum number of merge conflicts possible is 2.

### Example 2

**Input:** `primary = "dae"`, `secondary = "add"`

**Output:** `1`

**Explanation:** adadde has 1 merge conflict.

### Example 3

**Input:** `primary = "aaa"`, `secondary = "abb"`

**Output:** `0`

**Explanation:** aaaabb has no merge conflicts.

Added from a newer source found on June 24, 2026 🦒

## Constraints

- `1 <= |primary|, |secondary| <= 1000`
- `primary and secondary consist of lowercase English letters only.`

## Solutions

### Interleaving Enumeration

#### Derivation

The most literal reading tries every valid merge and keeps the cheapest. The
order rule makes generation easy: a merge is built one character at a time,
and at every step the next character may come from the head of whichever
branch still has characters left. Taking only from heads means each branch's
characters leave in their original order, so every string the recursion
produces is a valid merge and no validity check is ever needed. Counting a
finished merge's conflicts is the literal scan the definition suggests:
conflicts are exactly the [inversions](https://en.wikipedia.org/wiki/Inversion_(discrete_mathematics))
of `merged`, the pairs of positions `left < right` with
`merged[left] > merged[right]`:

1. Define `count_conflicts(merged)` that counts the pairs
   `left < right` with `merged[left] > merged[right]`.
2. Define `best_merge(i, j, merged)`: `i` commits have been taken from
   `primary` and `j` from `secondary`, and `merged` is the string built so
   far.
3. When both branches are exhausted, return `count_conflicts(merged)`.
4. When only one branch remains, the rest of the merge is forced: append its
   head and recurse.
5. Otherwise fork over the two heads and return the smaller result.

#### Walkthrough

Trace the enumeration on Example 1: `primary = "zc"`, `secondary = "d"`. The
root call `best_merge(0, 0, "")` forks over `"z"` and `"d"`, and each fork
keeps forking until both branches are empty:

```text
best_merge(0,0,"")
├── take z (P)   -> best_merge(1,0,"z")
│     ├── take c (P) -> best_merge(2,0,"zc")   forced d
│     │     └── take d (S) -> "zcd"  conflicts: z>c, z>d      = 2
│     └── take d (S) -> best_merge(1,1,"zd")  forced c
│           └── take c (P) -> "zdc"  conflicts: z>d, z>c, d>c = 3
└── take d (S)   -> best_merge(0,1,"d")  forced z, then c
      └── "dzc"          conflicts: d>c, z>c               = 2
```

Only three merges exist, and the invalid orderings such as `"dcz"` (which
would place `c` before `z` and break `primary`'s order) are never generated,
because characters can only leave each branch head-first. The minimum of
`2, 3, 2` is `2`, matching the expected Output.

#### Solution

The code is the fork over the two heads, the forced takes when a branch runs
dry, and the inversion count at each leaf.

```python
from typing import List


class Solution:
    def getMinimumConflicts(self, primary: str, secondary: str) -> int:
        def count_conflicts(merged: str) -> int:
            conflicts = 0
            for left in range(len(merged)):
                for right in range(left + 1, len(merged)):
                    if merged[left] > merged[right]:
                        conflicts += 1
            return conflicts

        def best_merge(i: int, j: int, merged: str) -> int:
            if i == len(primary) and j == len(secondary):
                return count_conflicts(merged)
            if i == len(primary):
                return best_merge(i, j + 1, merged + secondary[j])
            if j == len(secondary):
                return best_merge(i + 1, j, merged + primary[i])
            return min(best_merge(i + 1, j, merged + primary[i]),
                       best_merge(i, j + 1, merged + secondary[j]))

        return best_merge(0, 0, "")
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^(m + n) × (m + n)^2)`

With `m` and `n` the branch lengths, the recursion reaches roughly
`2^(m + n)` leaves, and each leaf runs an `O((m + n)^2)` inversion count
over a merge of length `m + n`; the string concatenations along each
root-to-leaf path add another quadratic term per path.

##### Space Complexity: `O((m + n)^2)`

The recursion depth is `m + n`, and each frame holds its own `merged`
string of length up to `m + n`.

#### Key Insights

- Building from heads only makes every generated string a valid merge, so
  the order rule costs no explicit checking.
- A conflict is an inversion of `merged`; equal characters never conflict
  because the definition demands strictly greater.
- The tree doubles at every fork, so at the constraint cap of 1000
  characters per branch the search space is astronomically larger than any
  machine could walk; the rest of the page removes that blowup.

### Top-Down Memoization

#### Derivation

The enumeration carries the whole `merged` string through every call, yet the
future cost depends on the past in a much coarser way. Reformulate the
counting to placement from the front: when a character `ch` is placed first
in a merge, the conflicts it creates are exactly the number of characters
placed after it that are strictly smaller than `ch`. The characters placed
after it come from `primary[i:]` and `secondary[j:]` (minus the one just
placed), and their letter multiset is fixed by `(i, j)` alone. So the cost
of the cheapest merge of the remaining suffixes is a function of the state
`(i, j)` and nothing else, which makes the recursion [memoizable](https://en.wikipedia.org/wiki/Memoization):

1. Precompute `primary_after` and `secondary_after`, suffix letter-count
   tables where `primary_after[i]` holds how many of each letter appear in
   `primary[i:]`.
2. Define `fewest(i, j)`: the minimum conflicts merging `primary[i:]` and
   `secondary[j:]` as standalone strings. It returns `0` when both are
   exhausted.
3. Place `primary[i]` first: the added cost is the number of letters smaller
   than `primary[i]` in `primary[i + 1:]` plus `secondary[j:]`, read from
   the suffix tables; add `fewest(i + 1, j)`.
4. Place `secondary[j]` first: the added cost is the number of letters
   smaller than `secondary[j]` in `primary[i:]` plus `secondary[j + 1:]`;
   add `fewest(i, j + 1)`.
5. Store the smaller candidate in `memo[(i, j)]`; the answer is
   `fewest(0, 0)`.

#### Walkthrough

Trace `fewest` on Example 1: `primary = "zc"`, `secondary = "d"`. The suffix
counts are `primary_after[0] = {z: 1, c: 1}`, `primary_after[1] = {c: 1}`,
and `secondary_after[0] = {d: 1}`. Each line shows one call deciding between
its two placements:

```text
fewest(2,1)  both exhausted            -> 0
fewest(2,0)  place d: smaller = 0      -> 0 + fewest(2,1) = 0
fewest(1,1)  place c: smaller = 0      -> 0 + fewest(2,1) = 0
fewest(1,0)  place c: smaller = 0      -> 0 + fewest(2,0) = 0
             place d: smaller = 1 (c)  -> 1 + fewest(1,1) = 1
             min(0, 1)                 -> 0
fewest(0,0)  place z: smaller = 2 (c,d)-> 2 + fewest(1,0) = 2
             place d: smaller = 1 (c)  -> 1 + fewest(0,1)
fewest(0,1)    place z: smaller = 1 (c)-> 1 + fewest(1,1)   ** memo hit, 0 **
               -> 1
             min(2, 1 + 1)             -> 2
```

Both top-level candidates reach `2`: placing `z` first commits to the merge
`zcd` with conflicts against both `c` and `d`, while placing `d` first leads
to `dzc`, whose `z` still lands before `c`. The problem statement's own
tally of `zcd = 2` and `dzc = 2` matches, and the memo hit on `fewest(1, 1)`
shows the two routes into the state `(1, 1)` sharing one computation. The
root returns `2`, matching the expected Output.

#### Solution

The code is the suffix-count tables, the two placement candidates, and the
memo around `fewest`.

```python
from typing import List


class Solution:
    def getMinimumConflicts(self, primary: str, secondary: str) -> int:
        def letters_after(text: str) -> List[List[int]]:
            suffix = [[0] * 26 for _ in range(len(text) + 1)]
            for position in range(len(text) - 1, -1, -1):
                suffix[position] = suffix[position + 1][:]
                suffix[position][ord(text[position]) - ord('a')] += 1
            return suffix

        primary_len = len(primary)
        secondary_len = len(secondary)
        primary_after = letters_after(primary)
        secondary_after = letters_after(secondary)
        memo = {}

        def fewest(i: int, j: int) -> int:
            if i == primary_len and j == secondary_len:
                return 0
            key = (i, j)
            if key in memo:
                return memo[key]

            candidates = []
            if i < primary_len:
                cutoff = ord(primary[i]) - ord('a')
                smaller = (sum(primary_after[i + 1][:cutoff])
                           + sum(secondary_after[j][:cutoff]))
                candidates.append(smaller + fewest(i + 1, j))
            if j < secondary_len:
                cutoff = ord(secondary[j]) - ord('a')
                smaller = (sum(primary_after[i][:cutoff])
                           + sum(secondary_after[j + 1][:cutoff]))
                candidates.append(smaller + fewest(i, j + 1))

            memo[key] = min(candidates)
            return memo[key]

        return fewest(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(26 × m × n)`

The memo admits each of the `(m + 1) × (n + 1)` states into the body once,
and each body run sums two letter-count slices of at most 26 entries per
placement; the 26 is a constant, so the bound is usually quoted as
`O(m × n)`.

##### Space Complexity: `O(m × n)`

The memo holds one entry per state and the recursion stack reaches depth
`m + n`; the two suffix tables add `O(26 × (m + n))`.

#### Key Insights

- The state collapses from the whole merged string to the pair `(i, j)`
  because a placement's cost depends only on how many of each letter
  remain, never on the order they were placed in.
- Equal characters never conflict (`merged[left] > merged[right]` is
  strict), which is why only the counts of strictly smaller letters enter
  the cost.
- The recursion descends `m + n` times, which at the constraint cap of
  2000 total characters exceeds Python's default recursion limit of 1000;
  the Bottom-Up DP below removes the stack entirely.

### Bottom-Up DP

#### Derivation

The memoized recursion computes `fewest(i, j)` from `fewest(i + 1, j)` and
`fewest(i, j + 1)`, so a table filled with `i` running from `m` down to `0`
and `j` from `n` down to `0` reproduces exactly the order the recursion
discovered its values, with a plain loop and no call stack.
[Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming)
with tabulation writes it down as `conflicts`, an `(m + 1) × (n + 1)` table
where `conflicts[i][j]` is the minimum conflicts merging `primary[i:]` and
`secondary[j:]`:

1. Allocate `conflicts` with every entry `0`; the base case
   `conflicts[m][n] = 0` needs no seeding.
2. For each row `i`, start a running letter `pool` holding the letter counts
   of `primary[i:]`, then let `j` decrease, adding `secondary[j]` to `pool`
   before computing each cell; `pool` then holds the letter counts of
   `primary[i:] + secondary[j:]`.
3. Fill each cell from the two placement candidates, taking the minimum.
4. Return `conflicts[0][0]`.

#### Recurrence

Let `conflicts[i][j]` be the minimum conflicts merging `primary[i:]` and
`secondary[j:]`, and let `smaller(i, j, ch)` count the letters strictly
smaller than `ch` in `primary[i:] + secondary[j:]`:

$$ conflicts[i][j] = \begin{cases} 0, & i = m \text{ and } j = n \\[4pt] \min\big(\text{smaller}(i + 1, j,\ \text{primary}[i]) + conflicts[i+1][j],\ \text{smaller}(i, j + 1,\ \text{secondary}[j]) + conflicts[i][j+1]\big), & \text{otherwise} \end{cases} $$

```text
conflicts[m][n] = 0
conflicts[i][j] = min(
    smaller_letters(primary[i], pool(i, j)) + conflicts[i + 1][j],
    smaller_letters(secondary[j], pool(i, j)) + conflicts[i][j + 1],
)
where pool(i, j) holds the letter counts of primary[i:] + secondary[j:]
```

The base case is the empty merge with nothing to conflict; each branch of
the minimum places one head character and pays for every remaining character
strictly smaller than it. The answer is read from `conflicts[0][0]`, the
full merge of both branches.

#### Walkthrough

Fill the table on Example 1: `primary = "zc"` (`m = 2`), `secondary = "d"`
(`n = 1`). The table has rows `i = 2, 1, 0` and columns `j = 1, 0`, and each
row's `pool` starts as the letter counts of `primary[i:]`:

```text
row i=2   pool starts {}                  conflicts[2][1] = 0 (base case)
          j=0: pool += d -> {d:1}
          place d: smaller = 0            conflicts[2][0] = 0 + conflicts[2][1] = 0
row i=1   pool starts {c:1}
          j=0: pool += d -> {c:1, d:1}
          (1,1): place c: smaller = 0     conflicts[1][1] = 0 + conflicts[2][1] = 0
          (1,0): place c: smaller = 0     -> 0 + conflicts[2][0] = 0
                place d: smaller = 1 (c)  -> 1 + conflicts[1][1] = 1
                min(0, 1)                 conflicts[1][0] = 0
row i=0   pool starts {z:1, c:1}
          j=0: pool += d -> {z:1, c:1, d:1}
          (0,1): place z: smaller = 2     conflicts[0][1] = 2 + conflicts[1][1] = 2
          (0,0): place z: smaller = 2     -> 2 + conflicts[1][0] = 2
                place d: smaller = 1 (c)  -> 1 + conflicts[0][1] = 3
                min(2, 3)                 conflicts[0][0] = 2
```

The decisive cell is `(0, 0)`: placing `z` first pays `2` (both `c` and `d`
follow it and both are smaller) but inherits a clean suffix, while placing
`d` first pays only `1` yet forces `z` into `conflicts[0][1] = 2` where it
still precedes `c`. The cheaper total is `2`, matching the expected Output.

#### Solution

The code is the row-by-row fill from the walkthrough: copy the running
`primary` pool, fold `secondary` letters in as `j` decreases, and take the
minimum of the two placements per cell.

```python
from typing import List


class Solution:
    def getMinimumConflicts(self, primary: str, secondary: str) -> int:
        def smaller_letters(pool: List[int], letter: str) -> int:
            cutoff = ord(letter) - ord('a')
            return sum(pool[:cutoff])

        primary_len = len(primary)
        secondary_len = len(secondary)
        conflicts = [[0] * (secondary_len + 1)
                     for _ in range(primary_len + 1)]

        primary_pool = [0] * 26
        for i in range(primary_len, -1, -1):
            if i < primary_len:
                primary_pool[ord(primary[i]) - ord('a')] += 1
            pool = primary_pool[:]
            for j in range(secondary_len, -1, -1):
                if j < secondary_len:
                    pool[ord(secondary[j]) - ord('a')] += 1
                if i == primary_len and j == secondary_len:
                    continue
                candidates = []
                if i < primary_len:
                    candidates.append(
                        smaller_letters(pool, primary[i])
                        + conflicts[i + 1][j])
                if j < secondary_len:
                    candidates.append(
                        smaller_letters(pool, secondary[j])
                        + conflicts[i][j + 1])
                conflicts[i][j] = min(candidates)

        return conflicts[0][0]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(26 × m × n)`

Each of the `(m + 1) × (n + 1)` cells sums two letter-count prefixes of at
most 26 entries; the 26 is a constant, so the bound is usually quoted as
`O(m × n)`, comfortably inside the 1000-per-branch constraint cap.

##### Space Complexity: `O(m × n)`

The `conflicts` table dominates; the letter pools are fixed 26-entry arrays
and the suffix tables of the memoized version are gone entirely.

#### Key Insights

- The table is the memo turned upright: same states, same values, filled in
  the order the recursion used to discover them, with no recursion-depth
  risk at the constraint cap.
- Maintaining the letter pool incrementally per row removes the suffix
  tables: the pool for cell `(i, j)` is assembled from the row-start copy
  plus the `secondary` letters folded in as `j` decreases.
- The two-placement minimum hides the whole difficulty of the problem: a
  valid merge is any sequence of head placements, and each placement's cost
  is a fixed function of the state, so the minimum over merges is the
  minimum over the two choices per state.

## Comparison of Solutions

### Time Complexity

- **Interleaving Enumeration**: `O(2^(m + n) × (m + n)^2)` - the fork tree
  doubles per placement and each leaf counts inversions naively.
- **Top-Down Memoization**: `O(26 × m × n)` - one body run per state with
  constant-size letter-count sums.
- **Bottom-Up DP**: `O(26 × m × n)` - the same per-state work in a double
  loop.

### Space Complexity

- **Interleaving Enumeration**: `O((m + n)^2)` - recursion depth `m + n`
  with a merge string per frame.
- **Top-Down Memoization**: `O(m × n)` - memo table plus suffix count
  tables and a stack of depth `m + n`.
- **Bottom-Up DP**: `O(m × n)` - the `conflicts` table plus fixed-size
  letter pools.

### Trade-offs

- **Interleaving Enumeration** is a direct transcription of the problem
  statement and doubles as a correctness oracle, but its time explodes past
  toy inputs.
- **Top-Down Memoization** keeps the placement recursion readable and pays
  only for states it actually visits, at the cost of stack depth `m + n`
  and the suffix tables.
- **Bottom-Up DP** removes the recursion and the suffix tables, runs inside
  the constraint caps with room to spare, and needs the most careful loop
  and pool bookkeeping.

### When to Use Each

- **Interleaving Enumeration**: as the derivational baseline and a correctness
  oracle for checking the DP on small branches.
- **Top-Down Memoization**: when the placement recursion is easiest to trust
  in its recursive form and the combined length stays modest.
- **Bottom-Up DP** (recommended): the default for the stated constraints;
  the same linear-in-states cost with no recursion-depth risk.

### Optimization Notes

- The 26-letter alphabet is what makes each state `O(1)`: the count of
  smaller remaining letters is a prefix sum over at most 26 counters. For a
  general alphabet the state cost would grow with the alphabet size.
- The `conflicts` table rolls to two rows of length `n + 1` because row `i`
  reads only row `i + 1` and the cell to its right; that drops the space to
  `O(n)` when memory matters.
- A common pitfall is counting equal characters as conflicts: the definition
  is strictly greater, so `smaller_letters` must exclude the placed letter
  and its equals, which is also what makes merges like `aaaabb` in Example 3
  cost `0`.
