# [Interleaving String](https://www.fastprep.io/problems/amazon-interleaving-string)

**Medium** | **NN minutes** | **Dynamic Programming, String**

Given strings s1, s2, and s3, return whether s3 can be formed by interleaving s1 and s2.

An interleaving uses every character from both source strings exactly once while preserving the left-to-right order within each source. Characters chosen from the two sources may alternate in groups of any positive length.

## Examples

### Example 1

**Input:** `s1 = "aabcc"`, `s2 = "dbbca"`, `s3 = "aadbbcbcac"`

**Output:** `true`

**Explanation:** The target can choose characters from both source strings while retaining each source's internal order.

### Example 2

**Input:** `s1 = "aabcc"`, `s2 = "dbbca"`, `s3 = "aadbbbaccc"`

**Output:** `false`

**Explanation:** Every possible choice eventually needs to reverse or skip a character from one source, so the target is not an interleaving.

### Example 3

**Input:** `s1 = ""`, `s2 = ""`, `s3 = ""`

**Output:** `true`

**Explanation:** The empty target uses every character from both empty source strings.

## Constraints

- `0 <= s1.length, s2.length <= 100.`
- `0 <= s3.length <= 200.`
- `All three strings contain only lowercase English letters.`

## Solutions

### Exhaustive Merge Recursion

#### Derivation

The definition reads as a decision process: read `s3` left to right and decide, character by character, whether each character comes from `s1` or from `s2`, while each source keeps its own order. The most literal translation builds every merge this process can produce and compares the finished merge against `s3`; some merge matches exactly when the answer is true:

1. Define `dfs(i, j, built)` as the search over merges of `s1[i:]` and `s2[j:]`
   that extend the string `built` assembled so far.
2. When `i == len(s1)` and `j == len(s2)`, both sources are consumed: return
   `built == s3`.
3. Otherwise take the next character from `s1` when one remains, recursing with
   `dfs(i + 1, j, built + s1[i])`.
4. If that branch did not answer true, take the next character from `s2` the
   same way with `dfs(i, j + 1, built + s2[j])`.
5. Return `dfs(0, 0, "")`.

#### Walkthrough

The official inputs merge ten characters, so a tailored pair shows the whole tree: `s1 = "ab"`, `s2 = "cd"`, `s3 = "acbd"`. Each line is one branch; leaves compare the finished merge with `s3`:

```text
take s1[0]='a'
  take s1[1]='b'
    take s2[0]='c'
      take s2[1]='d'
        leaf "abcd" == "acbd"?  no
  take s2[0]='c'
    take s1[1]='b'
      take s2[1]='d'
        leaf "acbd" == "acbd"?  yes -> return True
```

The first merge spends `s1` completely and fails; the search backtracks to the second character choice and the second merge matches, so the root returns `True`. The official examples hide this combinatorial cost behind forced choices: Example 1 (`s1 = "aabcc"`, `s2 = "dbbca"`, `s3 = "aadbbcbcac"`) answers on essentially one path, while Example 2 (`s3 = "aadbbbaccc"`) walks all `C(10, 5) = 252` leaves to answer `False`.

#### Solution

The code is the walkthrough's merge tree: one fork per character, one completion test.

```python
class Solution:
    def solve(self, s1: str, s2: str, s3: str) -> bool:
        def dfs(i: int, j: int, built: str) -> bool:
            if i == len(s1) and j == len(s2):
                return built == s3
            if i < len(s1) and dfs(i + 1, j, built + s1[i]):
                return True
            return j < len(s2) and dfs(i, j + 1, built + s2[j])

        return dfs(0, 0, "")
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(C(m + n, m) × (m + n))`

Every way of choosing which `m` of the `m + n` merge positions come from `s1` is a leaf, and each step copies `built`, so one root-to-leaf path costs up to `m + n` characters.

##### Space Complexity: `O(m + n)`

The recursion stack holds one frame per merged character and `built` holds the merge assembled so far.

#### Key Insights

- Transcribes the definition directly: choose a source per character, compare when both sources run dry.
- The `built` string makes every step pay `O(m + n)`; the later solutions drop it and pay `O(1)` per step.
- The `C(m + n, m)` leaf count is the entire cost story: at the stated limits (`m + n = 200`) the tree is astronomically large, which is what the rest of the page repairs.

### Top-Down Memoization

#### Derivation

The enumeration re-explores equivalent subtrees: two branches that consumed the same amounts of `s1` and `s2` in different orders face identical futures. Those two amounts are all that matter. Whenever the search is still meaningful, `built` is forced to be the prefix of `s3` of length `i + j`, so the next character to match is `s3[i + j]` and the string argument carries no information. Dropping it turns `(i, j)` into a [memoizable](https://en.wikipedia.org/wiki/Memoization) state, and there are only `(m + 1) × (n + 1)` of them:

1. Return `False` up front when `len(s3) != len(s1) + len(s2)`: an interleaving
   consumes both sources exactly, so unequal lengths can never match.
2. Define `dfs(i, j)` as: can the first `i` characters of `s1` and the first `j`
   of `s2` interleave into the first `i + j` characters of `s3`?
3. When both sources are consumed, return `True`.
4. Otherwise the next character is `s3[i + j]`; answer `True` when it can come
   from `s1` (`s1[i] == s3[i + j]` and `dfs(i + 1, j)`) or from `s2`
   (`s2[j] == s3[i + j]` and `dfs(i, j + 1)`).
5. Store each `(i, j)` answer in `memo` before returning it.

#### Walkthrough

Example 2 (`s1 = "aabcc"`, `s2 = "dbbca"`, `s3 = "aadbbbaccc"`) is the failing input, and it is where the memo earns its keep. Each line is one call; the next needed character is `s3[i + j]`:

```text
dfs(0, 0)  s3[0]='a'  from s1
  dfs(1, 0)  s3[1]='a'  from s1
    dfs(2, 0)  s3[2]='d'  from s2   (s1 offers 'b')
      dfs(2, 1)  s3[3]='b'  both sources offer 'b', branch twice
        dfs(3, 1)  s3[4]='b'  from s2   (s1 offers 'c')
          dfs(3, 2)  s3[5]='b'  from s2
            dfs(3, 3)  s3[6]='a': s1 offers 'c', s2 offers 'c' -> False  stored
          dfs(3, 2) -> False  stored
        dfs(3, 1) -> False  stored
        dfs(2, 2)  s3[4]='b'  both sources offer 'b', branch twice
          dfs(3, 2) -> False  ** memo hit **
          dfs(2, 3)  s3[5]='b'  from s1   (s2 offers 'c')
            dfs(3, 3) -> False  ** memo hit **
          dfs(2, 3) -> False  stored
        dfs(2, 2) -> False  stored
      dfs(2, 1) -> False  stored
    dfs(2, 0) -> False  stored
  dfs(1, 0) -> False  stored
dfs(0, 0) -> False  stored
```

Nine distinct states are solved and two repeat lookups are answered from `memo`. The root returns `False`: at `(3, 3)` the next needed character is `s3[6] = 'a'`, but the leftover suffixes of `s1` (`"cc"`) and `s2` (`"ca"`) can only offer `'c'` next. Example 1 runs the same recursion against `s3 = "aadbbcbcac"` and returns `True`.

#### Solution

The code is the walkthrough's state recursion with the length gate in front.

```python
class Solution:
    def solve(self, s1: str, s2: str, s3: str) -> bool:
        if len(s3) != len(s1) + len(s2):
            return False
        memo = {}

        def dfs(i: int, j: int) -> bool:
            if i == len(s1) and j == len(s2):
                return True
            if (i, j) in memo:
                return memo[(i, j)]
            next_position = i + j
            found = (
                i < len(s1) and s1[i] == s3[next_position] and dfs(i + 1, j)
            ) or (
                j < len(s2) and s2[j] == s3[next_position] and dfs(i, j + 1)
            )
            memo[(i, j)] = found
            return found

        return dfs(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

At most `(m + 1) × (n + 1)` states, each solved once with two constant-time character tests.

##### Space Complexity: `O(m × n)`

The `memo` dictionary plus a recursion stack of up to `m + n` frames.

#### Key Insights

- Dropping `built` is the move: `(i, j)` alone determines both the next character of `s3` and the prefix any surviving branch must have matched.
- The length gate is a correctness guard, not a speedup: without it a state could read `s3` past its end.
- Greedy matching fails when both sources offer the same character; trying both branches is exactly what the memo makes affordable.

### Bottom-Up 2-D DP

#### Derivation

The memoized recursion asks from the top and pays for a call stack. Flipping the question tabulates it: let `dp[i][j]` record whether the first `i` characters of `s1` and the first `j` of `s2` interleave into the first `i + j` of `s3`. Cell `(0, 0)` is `True`; row 0 and column 0 inherit along a single path (`s2`-only and `s1`-only prefixes); every interior cell is reachable from the cell above by consuming an `s1` character or from the left by consuming an `s2` character, tested against `s3[i + j - 1]`. Filling row by row never reads an undecided cell:

1. Allocate `dp` as an `(m + 1) × (n + 1)` table of `False`; set `dp[0][0] = True`.
2. Fill column 0: `dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]`. Fill
   row 0 symmetrically with `s2`.
3. For each interior cell, with `position = i + j - 1`:
   `dp[i][j] = (dp[i - 1][j] and s1[i - 1] == s3[position]) or
   (dp[i][j - 1] and s2[j - 1] == s3[position])`.
4. Return `dp[m][n]`.

#### Recurrence

Let \(dp_i[j]\) be whether the first `i` characters of `s1` and the first `j` of `s2` interleave into the first `i + j` of `s3`, with \(k = i + j - 1\):

$$ dp_i[j] = (dp_{i-1}[j] \wedge s_1[i-1] = s_3[k]) \vee (dp_i[j-1] \wedge s_2[j-1] = s_3[k]), \qquad dp_0[0] = \text{True} $$

```text
dp[0][0] = True
dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]   (s1-only prefixes)
dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]   (s2-only prefixes)
dp[i][j] = (dp[i - 1][j] and s1[i - 1] == s3[k])
           or (dp[i][j - 1] and s2[j - 1] == s3[k])  (k = i + j - 1)
```

The two disjuncts are the only moves an interleaving allows at its last position: `s3[k]` was taken from `s1` (the cell above) or from `s2` (the cell to the left). Both readings sit in the partially filled row or the row above, so the row-by-row fill never consults an undecided cell. The answer is read from \(dp_m[n]\), guarded by the length check that keeps every \(k\) inside `s3`.

#### Walkthrough

The full table on Example 1 (`s1 = "aabcc"`, `s2 = "dbbca"`, `s3 = "aadbbcbcac"`); rows are `s1` prefixes, columns are `s2` prefixes, and `T` marks reachable cells:

```text
        ''  d  b  b  c  a
  ''     T  .  .  .  .  .
  a      T  .  .  .  .  .
  a      T  T  T  T  T  .
  b      .  T  T  .  T  .
  c      .  .  T  T  T  T
  c      .  .  .  T  .  T
```

The `'a'` rows reach across all five columns because either source can supply the leading `'a'`s. Row `b` survives only where an `s2` character continues the prefix, and the bottom-right cell ends `T`, so the expected output is `true`. The failing Example 2 computes the same table against `s3 = "aadbbbaccc"`; its bottom-right cell stays `.`, returning `False`.

#### Solution

The code is the row-by-row fill of the walkthrough's table.

```python
class Solution:
    def solve(self, s1: str, s2: str, s3: str) -> bool:
        m, n = len(s1), len(s2)
        if len(s3) != m + n:
            return False
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True
        for i in range(1, m + 1):
            dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]
        for j in range(1, n + 1):
            dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                position = i + j - 1
                dp[i][j] = (
                    dp[i - 1][j] and s1[i - 1] == s3[position]
                ) or (
                    dp[i][j - 1] and s2[j - 1] == s3[position]
                )
        return dp[m][n]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

One test pair per table cell.

##### Space Complexity: `O(m × n)`

The full table.

#### Key Insights

- The cell test is the memoized recursion with the cache replaced by an evaluation order.
- Row 0 and column 0 are single-path borders: "formed from `s2` only" and "formed from `s1` only".
- The table records reachability, not counts, because the question is a decision, not a tally.

### Space-Optimized Two-Row DP

#### Derivation

An interior cell reads only `dp[i - 1][j]` (the row above) and `dp[i][j - 1]` (the cell just built). Row `i - 2` and older are dead weight, so the table collapses to two rows: `previous` for row `i - 1` and `current` under construction. The borders move into the loop (`current[0]` inherits from `previous[0]` alone), and replacing `previous` with `current` after each row plays the role the index decrement played in the recursion:

1. Build row 0 into `previous`: `previous[0] = True`, then
   `previous[j] = previous[j - 1] and s2[j - 1] == s3[j - 1]`.
2. For each `i` in `1..m`, build `current` from `previous`:
   `current[0] = previous[0] and s1[i - 1] == s3[i - 1]`, and for `j` in `1..n`
   with `position = i + j - 1`:
   `current[j] = (previous[j] and s1[i - 1] == s3[position]) or
   (current[j - 1] and s2[j - 1] == s3[position])`.
3. Replace `previous` with `current` and continue.
4. Return `previous[n]`, the last cell of the last row.

#### Walkthrough

The rolling rows on Example 1 (`s1 = "aabcc"`, `s2 = "dbbca"`, `s3 = "aadbbcbcac"`); each line is one completed row:

```text
i=0 (s2 only)   previous = [T, ., ., ., ., .]
i=1 (a)         current  = [T, ., ., ., ., .]
i=2 (a)         current  = [T, T, T, T, T, .]
i=3 (b)         current  = [., T, T, ., T, .]
i=4 (c)         current  = [., ., T, T, T, T]
i=5 (c)         current  = [., ., ., T, ., T]
```

Each row equals the corresponding row of the Bottom-Up 2-D DP table, reproduced with two lists instead of seven. `previous[n]` in the final row is `T`, matching the expected output `true` for Example 1.

#### Solution

The code is the walkthrough's row loop: build `current` from `previous`, then rotate.

```python
class Solution:
    def solve(self, s1: str, s2: str, s3: str) -> bool:
        m, n = len(s1), len(s2)
        if len(s3) != m + n:
            return False
        previous = [True] + [False] * n
        for j in range(1, n + 1):
            previous[j] = previous[j - 1] and s2[j - 1] == s3[j - 1]
        for i in range(1, m + 1):
            current = [False] * (n + 1)
            current[0] = previous[0] and s1[i - 1] == s3[i - 1]
            for j in range(1, n + 1):
                position = i + j - 1
                from_s1 = previous[j] and s1[i - 1] == s3[position]
                from_s2 = current[j - 1] and s2[j - 1] == s3[position]
                current[j] = from_s1 or from_s2
            previous = current
        return previous[n]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

One test pair per cell, exactly as in the full table.

##### Space Complexity: `O(n)`

Two rows of `n + 1` cells; the discarded predecessor is garbage-collected.

#### Key Insights

- The dependency pattern fixes the memory: a cell reads its top and left neighbors only, so one spare row suffices.
- `current` must be a fresh list per row; updating `previous` in place would destroy the top neighbor before it is read.
- What the compression gives up is the map: reconstructing a witnessing interleaving needs the full table to walk backward.

### Top-Down Memoization with functools.cache

#### Derivation

The dict in Top-Down Memoization is bookkeeping, not logic: it exists to remember what `dfs(i, j)` returned, which is precisely what [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) does around any pure function. Decorating the recursion deletes the dict, the membership test, and the store, leaving the length gate, the base case, and the two character tests exactly as written:

1. Keep the memoized recursion's structure: the length gate, the shared
   completion base case, the two branch tests.
2. Replace `memo` with `@cache` on `dfs`, keyed automatically by the argument
   pair.
3. Return `dfs(0, 0)`.

The one behavioral cost: the decorator keeps every visited `(i, j)` pair alive for the life of the process, so memory matches the dict version but cannot be freed early.

#### Walkthrough

The decorated recursion on Example 2 (`s1 = "aabcc"`, `s2 = "dbbca"`, `s3 = "aadbbbaccc"`) follows the Top-Down Memoization trace line for line; only the lookup changes:

```text
dfs(0, 0) -> dfs(1, 0) -> dfs(2, 0) -> dfs(2, 1) -> ...
  identical descent, identical branches at (2, 1) and (2, 2)
dfs(3, 3) -> False                    ** cached: no recompute **
dfs(3, 2) -> False                    ** cached: no recompute **
dfs(0, 0) -> False
```

9 distinct `(i, j)` states are computed once each, 2 repeat lookups come from the cache, and the root returns `False`, matching the expected output for Example 2.

#### Solution

The code is the memoized recursion with the dict replaced by the decorator.

```python
from functools import cache


class Solution:
    def solve(self, s1: str, s2: str, s3: str) -> bool:
        if len(s3) != len(s1) + len(s2):
            return False

        @cache
        def dfs(i: int, j: int) -> bool:
            if i == len(s1) and j == len(s2):
                return True
            next_position = i + j
            return (
                i < len(s1) and s1[i] == s3[next_position] and dfs(i + 1, j)
            ) or (
                j < len(s2) and s2[j] == s3[next_position] and dfs(i, j + 1)
            )

        return dfs(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n)`

The cache admits each `(i, j)` pair once and the body is constant work.

##### Space Complexity: `O(m × n)`

The decorator's cache plus the recursion stack.

#### Key Insights

- `functools.cache` is the dict memo with the ceremony removed: same asymptotics, no key-tuple mistakes.
- The recursion body becomes the interleaving definition in its purest form, which makes it the version to quote in an interview after sketching the dict.
- The length gate stays outside the recursion: it is a property of the whole input, not of a state.

## Comparison of Solutions

### Time Complexity

- **Exhaustive Merge Recursion**: `O(C(m + n, m) × (m + n))` - every merge is built and compared.
- **Top-Down Memoization**: `O(m × n)` - one solve per `(i, j)` state.
- **Bottom-Up 2-D DP**: `O(m × n)` - one test pair per cell.
- **Space-Optimized Two-Row DP**: `O(m × n)` - the same cells, two rows at a time.
- **Top-Down Memoization with functools.cache**: `O(m × n)` - the dict memo with library bookkeeping.

### Space Complexity

- **Exhaustive Merge Recursion**: `O(m + n)` - the stack plus the `built` string.
- **Top-Down Memoization**: `O(m × n)` - the memo plus the stack.
- **Bottom-Up 2-D DP**: `O(m × n)` - the full table.
- **Space-Optimized Two-Row DP**: `O(n)` - the two live rows.
- **Top-Down Memoization with functools.cache**: `O(m × n)` - the cache plus the stack.

### Trade-offs

- The merge recursion is the definitional baseline; its leaf count grows combinatorially, which makes it a correctness oracle rather than a solution.
- The memoized recursions carry a call stack and an `O(m × n)` cache; the table versions trade the stack for an explicit evaluation order.
- The two-row table is the production form: the same time as everything else at linear memory.

### When to Use Each

- **Exhaustive Merge Recursion**: tiny inputs, or as the oracle when checking the DP versions by hand.
- **Top-Down Memoization**: when deriving live; stating why `built` can be dropped for the pair `(i, j)` is the insight worth saying out loud.
- **Bottom-Up 2-D DP**: when the reachable-cell map itself matters, for example to reconstruct a witnessing interleaving by walking it backward.
- **Space-Optimized Two-Row DP**: the answer to the problem as stated (recommended here).
- **Top-Down Memoization with functools.cache**: Python code that wants the memoized recursion without the dict ceremony.

### Optimization Notes

- The length gate `len(s3) != m + n` rejects impossible inputs in constant time and keeps every state's `s3[i + j]` access in bounds.
- Greedy matching (always take from `s1` when it matches) fails when both sources hold the same character but only one choice leaves a completable suffix.
- Reconstructing an actual interleaving needs the full table: walk from `dp[m][n]`, preferring the top neighbor when it is `True` and its character test passes, which is the one feature the space optimization gives up.
