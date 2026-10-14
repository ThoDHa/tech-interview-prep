# [Decode Ways](https://leetcode.com/problems/decode-ways/)

**Medium** | **25 minutes** | **String, Dynamic Programming**

**Pattern:** [DP 1D Linear](../patterns/dp_1d_linear/intuition.md)

**Algorithm:** [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization) · [Recurrence relation](https://en.wikipedia.org/wiki/Recurrence_relation)

**Practice:** [`practice/decode_ways/solution.py`](../../practice/decode_ways/solution.py)

A string consisting of uppercase english characters can be encoded to a number using the following mapping:

```java
'A' -> "1"
'B' -> "2"
...
'Z' -> "26"
```

To **decode** a message, digits must be grouped and then mapped back into letters using the reverse of the mapping above. There may be multiple ways to decode a message. For example, `"1012"` can be mapped into:

* `"JAB"` with the grouping `(10 1 2)`
* `"JL"` with the grouping `(10 12)`

The grouping `(1 01 2)` is invalid because `01` cannot be mapped into a letter since it contains a leading zero.

Given a string `s` containing only digits, return the number of ways to **decode** it. You can assume that the answer fits in a **32-bit** integer.

## Examples

### Example 1

**Input:** `s = "12"`

**Output:** `2`

**Explanation:** "12" could be decoded as "AB" (1 2) or "L" (12).

### Example 2

**Input:** `s = "01"`

**Output:** `0`

**Explanation:** "01" cannot be decoded because "01" cannot be mapped into a letter.

## Constraints

- `1 <= s.length <= 100`
- `s` consists of digits

## Deriving the Solution

Every decoding is a partition of the string into one- and two-digit chunks, each chunk naming a letter, so the count of decodings is the count of legal partitions. Whether a chunk is legal depends only on its own digits: a one-digit chunk fails only on `0`, a two-digit chunk only when it is `00` through `09` or above `26`. That locality is the lever: the number of ways to decode a suffix does not depend on how the prefix before it was grouped, so one number per starting position is all any decision ever needs, and the approaches below differ in how they compute that number.

1. **Start literal.** Cut the string into every legal grouping: from each
   position, consume one digit if it is not `0`, consume two digits if they
   form `10` through `26`, and recurse on what remains, counting a partition
   complete when the string is exactly consumed. Correct, but every route to
   the same suffix re-cuts it, and the number of routes doubles per digit,
   costing `O(2^n)`: see [Brute Force](#brute-force).
2. **Spot the waste.** `decide(i)` asks about the suffix starting at `i` and
   nothing else: two different groupings that both reach position `i` get the
   same answer twice and grow the full subtree both times.
3. **Cache it.** Store each suffix's count the first time it is computed;
   every later visit is a dictionary lookup and the tree collapses to one
   computation per position, `O(n)`: see [Top-Down Memoization](#top-down-memoization).
4. **Flip the direction.** The memo fills from the string's end anyway, since
   the deepest calls are the shortest suffixes: skip the recursion and fill a
   `dp` table right-to-left with a plain loop: see [Bottom-Up DP](#bottom-up-dp).
5. **Shrink the state.** `dp[i]` reads only the two entries just above it, so
   two rolling totals replace the whole array and the space drops to `O(1)`:
   see [Space-Optimized DP](#space-optimized-dp).
6. **Hand the cache to the library.** Step 3 stacked two ideas: the
   one-or-two-digit recurrence, and a dictionary keeping it from redoing
   work. Only the recurrence is the algorithm, so decorating the Brute
   Force function with `functools.cache` deletes the bookkeeping and leaves
   the recursion verbatim: see [Top-Down Memoization with
   functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Brute Force

#### Derivation

The most literal reading of the problem enumerates the groupings themselves: standing at a position, the next chunk is either one digit or two, and only the digits decide which of those cuts name a letter. Trying every legal cut and counting the complete ones counts the decodings:

1. Define `decide(i)` as the number of ways to decode the suffix `s[i:]`,
   with `decide(len(s)) = 1`: consuming the whole string is one finished
   grouping.
2. A single-digit cut exists only when `s[i] != "0"`, since `"0"` maps to no
   letter; when it exists it contributes `decide(i + 1)`.
3. A two-digit cut `s[i:i+2]` exists only when there is a second digit
   (`i + 1 < len(s)`) and its value is between `10` and `26`; when it exists
   it contributes `decide(i + 2)`.
4. Return the sum of the two contributions; the answer is `decide(0)`.

The existence guard in step 3 is easy to drop, because the value check `int(s[i:i+2]) <= 26` looks self-sufficient: on the final position the slice reads one digit, which always passes the value check, and the recursion then steps two positions past the end. The guard needs both conditions.

Nothing is remembered between calls, so every suffix reached by more than one grouping is re-cut in full: each call forks up to two more, and the tree roughly doubles per digit.

#### Walkthrough

Trace the recursion on Example 1: `s = "12"`. The entry call is `decide(0)`, and each call shows its legal cuts and their returns:

```text
decide(0)  s = "12"        cuts "1" and "12"   both legal
├── cut "1":  decide(1)    s = "2"
│     cut "2": decide(2)   s = ""              -> 1  consumed
│     -> 1                 pair cut blocked: i + 1 == len(s)
│     -> 1
└── cut "12": decide(2)    s = ""              -> 1  consumed
-> decide(0) = 1 + 1 = 2
```

Both cuts survive their legality checks and each lands exactly on the consumed string, so the counts add to `2`, matching the expected Output for Example 1. Example 2 shows the checks rejecting: `decide(0)` on `"01"` finds `s[0] == "0"`, so neither cut exists and it returns `0` immediately. On a longer input such as `"11106"`, the per-suffix values `decide(0..5) = 2, 1, 1, 0, 1, 1` are each recomputed once per grouping that reaches them, which is the rework the next solution removes.

#### Solution

The code is the walkthrough's two legality-guarded cuts around the consumed base case.

```python
class Solution:
    def numDecodings(self, s: str) -> int:
        def decide(i: int) -> int:
            if i == len(s):
                return 1  # Consumed the whole string: one finished grouping.
            total = 0
            # Cut one digit, but "0" names no letter.
            if s[i] != "0":
                total += decide(i + 1)
                # Cut two digits: a second digit must exist, and the pair
                # must map to a letter ("10" through "26").
                if i + 1 < len(s) and int(s[i : i + 2]) <= 26:
                    total += decide(i + 2)
            return total

        return decide(0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

Each call forks into up to two more, so the call tree roughly doubles at every level of the `n` digits; nothing is shared between the branches, so every route pays in full. (The growth constant is the golden ratio rather than `2`, because single-digit chains fork one way, but the bound is exponential either way.)

##### Space Complexity: `O(n)`

No table is kept, but the recursion stack reaches depth `n` along the all-single-digit chain.

#### Key Insights

- The problem is a counting variant of partition search: the answer is the
  number of legal cuts, not any particular decoding, which is why the recursion returns counts rather than groupings.
- The two guard conditions carry the whole problem: `s[i] != "0"` for the
  one-digit cut, and second-digit-exists plus value-at-most-`26` for the two-digit cut. The outer `"0"` check is also what makes the bare `<= 26` pair test sound: `"06"` parses to `6` and would pass it, but a pair is only ever sliced when `s[i] != "0"`, so every leading-zero pair is already dead and every pair the value test admits is genuinely in `10` through `26`.
- The `len(s)` base case returning `1` (not `0`) is what makes the count
  work: reaching the end means the grouping currently being built is itself one complete decoding.

### Top-Down Memoization

#### Derivation

The Brute Force re-cuts the same suffix in exponentially many branches, yet `decide(i)` depends on nothing but `i`: every grouping that reaches position `i` gets the same answer. The repair is to [cache each suffix's count](https://en.wikipedia.org/wiki/Memoization) in a dictionary keyed by the position, so the routes into position `i` share one computation:

1. Keep `decide(i)` verbatim from the Brute Force: the `len(s)` base case,
   the `"0"` guard, and both conditions of the pair cut.
2. Before computing, check the `memo` dictionary and return a stored answer.
3. Otherwise compute the sum of the two legal cuts and store it under key `i`
   before returning.
4. Return `decide(0)`; each position from `0` to `n - 1` now runs its body
   exactly once, so the tree collapses from `O(2^n)` nodes to `O(n)`.

#### Walkthrough

Trace the recursion on `s = "226"`, the classic input where both cuts stay legal the longest. The trace indents one level per call; marked lines are memo hits:

```text
decide(0)   0 not in memo -> recurse     s = "226"
  decide(1) 1 not in memo -> recurse     s = "26"
    decide(2) 2 not in memo -> recurse   s = "6"
      cut "6": decide(3) -> 1            consumed, base case
    decide(2) -> 1                       pair cut blocked: i + 1 == len(s)
                                         store memo[2] = 1
  decide(1) -> 1 + decide(3) = 2         cuts "2" and "26" both legal
                                         store memo[1] = 2
decide(0) -> 2 + decide(2) = 3           cuts "2" and "22" both legal,
                                         decide(2) ** memo hit: no recursion **
                                         store memo[0] = 3
```

Note the two different routes into position `2`: the descent reaches it through `decide(1)`'s one-digit cut, and the root's two-digit cut `"22"` lands on it again after the subtree is already stored, so the second visit costs one dictionary lookup. The call returns `3`, the count of decodings of `"226"` (`"BBF"`, `"BZ"`, `"VF"`).

#### Solution

The code is the Brute Force recursion with the memo check and store wrapped around the two cuts.

```python
class Solution:
    def numDecodings(self, s: str) -> int:
        memo = {}

        def decide(i: int) -> int:
            if i == len(s):
                return 1
            if i in memo:
                return memo[i]

            total = 0
            if s[i] != "0":
                total += decide(i + 1)
                if i + 1 < len(s) and int(s[i : i + 2]) <= 26:
                    total += decide(i + 2)
            memo[i] = total
            return memo[i]

        return decide(0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each position from `0` to `n - 1` enters the body exactly once and does constant work combining two already-known values; every other call is a dictionary hit.

##### Space Complexity: `O(n)`

The memo stores one entry per position, and the recursion stack reaches depth `n` along the deepest single-digit chain.

#### Key Insights

- The dictionary is keyed by the position alone, which works because the suffix
  starting at `i` fully determines its count: no other state exists.
- Writing the check-compute-store cycle by hand shows the mechanism a decorator
  would hide, which is worth seeing once; `functools.cache` collapses those three lines, see [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).
- Memoization converts the exponential tree into linear time without touching
  the recursion's shape, which makes the correctness argument easy to carry over from the Brute Force.

### Bottom-Up DP

#### Derivation

The memoized recursion still starts at the answer and unwinds downward before producing its first useful value, paying call overhead and stack depth along the way. Watch the order its `memo` actually fills: the deepest position resolves first, then the levels above, up to position `0`. Bottom-up [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) produces that same table with a plain loop and no recursion. Let `dp[i]` be the number of ways to decode the suffix `s[i:]`, matching `decide(i)` exactly:

1. Allocate `dp` with one slot past the last index and set `dp[n] = 1`: the
   empty suffix is one finished grouping.
2. Seed `dp[n - 1] = 1` when `s[n - 1] != "0"`, else `0`: a one-digit suffix
   decodes only when its digit names a letter.
3. Sweep `i` from `n - 2` down to `0`, setting
   `dp[i] = dp[i + 1] if s[i] != "0" else 0`, plus `dp[i + 2]` when
   `s[i] != "0"` and `int(s[i:i+2]) <= 26`.
4. Return `dp[0]`, the count for the whole string.

The explicit boundary guard `i + 1 < len(s)` from the recursive versions becomes structural here: position `n - 1` is seeded by hand and the loop starts at `n - 2`, so the pair cut always has its second digit.

#### Recurrence

Let `dp[i]` be the number of ways to decode the suffix `s[i:]`, with `n = len(s)`:

$$ dp[i] = \begin{cases} 1, & i = n \\[4pt] 0, & i = n - 1,\ s[n-1] = 0 \\[4pt] \mathbf{1}[\,s[i] \ne 0\,]\,\Bigl( dp[i+1] + \mathbf{1}[\,10 \le \mathrm{int}(s[i{:}i{+}2]) \le 26\,]\,dp[i+2] \Bigr), & 0 \le i < n - 1 \end{cases} $$

```text
dp[n] = 1
dp[n - 1] = 0 if s[n - 1] == "0" else 1
dp[i] = 0                                       if s[i] == "0"
dp[i] = dp[i + 1] + (dp[i + 2] if 10 <= int(s[i:i+2]) <= 26 else 0)
                                                otherwise
```

The base case `dp[n] = 1` encodes that fully consuming the string completes one grouping; a suffix that starts with `0` decodes zero ways because its first chunk cannot exist. The indicator brackets fold the two legality guards into the transition: the outer one kills both cuts when `s[i]` is `"0"`, the inner one admits the pair cut only when the two digits name a letter, and `dp[i + 2]` is only ever read when that guard passed, so no out-of-range access occurs. The answer is read from `dp[0]`.

#### Walkthrough

Let us fill the table on the five-digit input `s = "11106"`, the example family's zero-embedding case, so `n = 5` and the table runs `dp[0]` through `dp[5]`. The slot past the end is seeded at `1`, and `dp[4]` is seeded from the final digit `6`:

```text
start    dp = [_, _, _, _, 1, 1]              dp[5] = 1, dp[4] = 1 (s[4] = "6")
i = 3    s[3:5] = "06"  int 6 <= 26          s[3] = "0" kills both cuts
         dp[3] = 0                            dp = [_, _, _, 0, 1, 1]
i = 2    s[2:4] = "10"  10 <= int <= 26       cut "1" -> dp[3] = 0
                                              cut "10" -> dp[4] = 1
         dp[2] = 0 + 1 = 1                    dp = [_, _, 1, 0, 1, 1]
i = 1    s[1:3] = "11"  10 <= int <= 26       cut "1" -> dp[2] = 1
                                              cut "11" -> dp[3] = 0
         dp[1] = 1 + 0 = 1                    dp = [_, 1, 1, 0, 1, 1]
i = 0    s[0:2] = "11"  10 <= int <= 26       cut "1" -> dp[1] = 1
                                              cut "11" -> dp[2] = 1
         dp[0] = 1 + 1 = 2                    dp = [2, 1, 1, 0, 1, 1]
```

The digit `"0"` at position `3` zeroes `dp[3]`: it cannot start a chunk, so no grouping may cut there, and both decodings of the string must consume positions `2` and `3` together as the pair `"10"`. The method returns `dp[0] = 2`, which are the groupings `(1 1 10 6)` and `(11 10 6)`, matching the verified count for this input.

#### Solution

The code is the table fill from the walkthrough: seed the past-the-end slot and the final digit, then loop the recurrence right-to-left.

```python
class Solution:
    def numDecodings(self, s: str) -> int:
        n = len(s)
        # dp[i] = number of ways to decode the suffix s[i:]
        dp = [0] * (n + 1)
        dp[n] = 1  # Empty suffix: the grouping built so far is complete.
        dp[n - 1] = 0 if s[n - 1] == "0" else 1

        for i in range(n - 2, -1, -1):
            if s[i] == "0":
                continue  # No chunk can start on "0": dp[i] stays 0.
            dp[i] = dp[i + 1]
            if int(s[i : i + 2]) <= 26:
                dp[i] += dp[i + 2]

        return dp[0]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One constant-time update per position in a single right-to-left sweep; each pair value is computed once with a two-character slice.

##### Space Complexity: `O(n)`

The table holds `n + 1` entries, one per suffix start plus the past-the-end slot.

#### Key Insights

- Defining `dp[i]` over suffixes rather than prefixes puts the answer at
  `dp[0]` and lets the table be filled in the direction the recursion used to unwind, which makes the equivalence with the memoized version line-for-line.
- The past-the-end slot `dp[n] = 1` is the whole base case: it is the count
  of the empty suffix, and it is what the final pair cut reads when the string ends in a legal two-digit letter.
- The `continue` on `s[i] == "0"` leaves `dp[i]` at its initialized `0`,
  which encodes the hardest rule of the problem (zeros only work inside `10` or `20`) in one line.

### Space-Optimized DP

#### Derivation

The table loop reads only the two entries just above the one it writes: `dp[i + 1]` and `dp[i + 2]`. Everything older is dead weight once position `i` is set, so the whole array collapses into two rolling totals, `one_back` standing in for `dp[i + 1]` and `two_back` for `dp[i + 2]`. Seeding `one_back = 1` installs the virtual `dp[n] = 1` entry, and `two_back` starts dead at `0` because the first update reads only `one_back`:

1. Start with `one_back = 1` (the empty suffix's count) and `two_back = 0`.
2. Sweep `i` from the last position down to `0`. Set `current = 0`; if
   `s[i] != "0"`, add `one_back` (the one-digit cut) and, when
   `i + 1 < len(s)` and `s[i:i+2] <= 26`, add `two_back` (the two-digit cut).
3. Shift the window: `two_back = one_back`, then `one_back = current`.
4. After the sweep, `one_back` holds the count for the whole string.

#### Walkthrough

Let us roll the two totals through `s = "11106"`, the same input as the Bottom-Up walkthrough. Before rolling, pin the notation to the Bottom-Up table: before the update at `i`, `one_back` holds `dp[i + 1]` and `two_back` holds `dp[i + 2]`, with the virtual `dp[n] = 1` already loaded into `one_back`. Reading each row's `current` and then the post-shift pair:

```text
start   one_back = dp[5] = 1   two_back = 0 (dp[6]: exists, never read)
i = 4  s[4]="6"  current = one_back = 1                  -> one_back = 1, two_back = 1
i = 3  s[3]="0"  current = 0                             -> one_back = 0, two_back = 1
i = 2  s[2]="1"  current = 0 + two_back = 1  ["10" legal] -> one_back = 1, two_back = 0
i = 1  s[1]="1"  current = one_back = 1                  -> one_back = 1, two_back = 1
i = 0  s[0]="1"  current = 1 + two_back = 2  ["11" legal] -> one_back = 2, two_back = 1
```

Each row reproduces exactly one `dp` entry from the Bottom-Up walkthrough: the update at `i` computes `dp[i]` from `dp[i + 1]` and `dp[i + 2]` before the shift renames them, and the `s[3] = "0"` row shows the zero zeroing its own entry while the window keeps moving. After the last update `one_back` holds `dp[0] = 2`, the count of `(1 1 10 6)` and `(11 10 6)`, matching the verified count for this input.

#### Solution

The code is the walkthrough's three lines per position: combine, then shift the window.

```python
class Solution:
    def numDecodings(self, s: str) -> int:
        one_back = 1  # dp[i + 1]: ways to decode the suffix one digit ahead
        two_back = 0  # dp[i + 2]: ways to decode the suffix two digits ahead
        for i in range(len(s) - 1, -1, -1):
            current = 0
            if s[i] != "0":
                current += one_back
                if i + 1 < len(s) and int(s[i : i + 2]) <= 26:
                    current += two_back
            two_back = one_back
            one_back = current
        return one_back
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The same single right-to-left sweep as the Bottom-Up DP, one constant-time update per position.

##### Space Complexity: `O(1)`

Two integer registers replace the whole table, regardless of `len(s)`.

#### Key Insights

- Only a two-entry window of the table is ever alive, which is the defining
  feature of a linear 1-D recurrence and the reason the space collapses to constants.
- Seeding `one_back = 1` is not sloppiness: it installs the recurrence's
  virtual `dp[n] = 1` entry, so the final position and the final legal pair are handled by the same update as every other position and no length guard on the base case survives.
- A `0` produces `current = 0` for its own position but still shifts the
  window correctly, which is exactly how `"10"` and `"20"` stay decodable: the `0` itself contributes nothing, while the pair cut over it reads the total stored two positions back.

### Top-Down Memoization with functools.cache

#### Derivation

The [Top-Down Memoization](#top-down-memoization) solution stacks two separate things: the one-or-two-digit recurrence, and a dictionary that stops the recursion from re-cutting a suffix it has already answered. Only the first is the algorithm. The second is pure bookkeeping, and the standard library already implements it. Decorating the function with [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) attaches an unbounded cache keyed by the call's arguments, consulted before the body runs and filled with whatever the body returns, so the recurrence and its base case stay on the page exactly as the Brute Force wrote them:

1. Keep `decide(i)` verbatim from the Brute Force: return `1` at
   `i == len(s)`, otherwise return the sum of the legality-guarded
   `decide(i + 1)` and `decide(i + 2)` cuts.
2. Decorate it with `@cache`, so each distinct `i` runs the body at most once
   and every later request for that suffix is answered from the cache.
3. Delete the three bookkeeping lines the decorator now owns: the `memo = {}`
   declaration, the `if i in memo` lookup, and the `memo[i] = ...` store.
4. Because `decide` is defined inside `numDecodings`, each call builds a
   fresh function object with a fresh cache, so nothing leaks between inputs.

One behavioural difference follows from where the decorator sits. The hand-rolled version computes `total` and stores it even when both cuts are dead (a `"0"` position stores `0`); `@cache` wraps the entire body the same way, so the stored values and the store events line up identically here.

#### Walkthrough

Run it on `s = "226"`, the same input as the memoized walkthrough. The trace indents one level per call and notes whether the decorator ran the body or answered from the cache:

```text
decide(0)   miss, run the body     s = "226"
  decide(1)   miss, run the body   s = "26"
    decide(2)   miss, run the body  s = "6"
      decide(3) -> 1                base case, cached under key 3
    decide(2) -> 1                  one-digit cut only, cached under key 2
  decide(1) -> 2                    cuts "2" and "26", cached under key 1
  decide(3) -> 1                    ** cache hit, the body does not run **
decide(0) -> 3                     cuts "2" and "22", cached under key 0
```

The descent fills the cache deepest-first; the root's two-digit cut `"22"` then asks for `decide(2)`, already computed and cached under key `2` from the one-digit chain, so no subtree is re-entered. The outer call returns `3`, matching the memoized count of decodings of `"226"`.

#### Solution

The Brute Force recursion, unchanged, with one decorator standing in for the memo dictionary.

```python
from functools import cache


class Solution:
    def numDecodings(self, s: str) -> int:
        # The cache lives on this inner function object, which is rebuilt on
        # every call, so results never carry over between inputs.
        @cache
        def decide(i: int) -> int:
            if i == len(s):
                return 1
            total = 0
            if s[i] != "0":
                total += decide(i + 1)
                if i + 1 < len(s) and int(s[i : i + 2]) <= 26:
                    total += decide(i + 2)
            return total

        return decide(0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- The cache admits each position from `0` to `n - 1` into the body exactly
  once, and each admission does one slice, one comparison, and at most two additions over already-known values
- Every other call is a dictionary lookup on a small integer key, which is
  constant time, so the total is linear in `n`

##### Space Complexity: `O(n)`

- The decorator's cache holds one entry per distinct argument, the `n`
  positions plus the one base-case key `n`
- The recursion still descends to depth `n` before the first value returns, so
  the stack matches the cache in order of growth

#### Key Insights

- The algorithm is untouched: the recurrence and the base case read exactly as
  they do in the Brute Force, which makes plain that memoization is an execution strategy rather than a change to the recursion.
- `@cache` keys on the argument tuple, so it is a drop-in replacement only when
  the arguments are hashable and the function is genuinely pure; `decide` reads nothing but `i` and the fixed string `s`, which is what licenses the substitution.
- Defining the cached function inside the method scopes the cache to a single
  call, avoiding the stale-results and unbounded-growth hazards of decorating a method or a module-level function.
- Use `functools.lru_cache(maxsize=...)` instead when the key space is unbounded
  and eviction matters; `cache` is `lru_cache(maxsize=None)`, which never evicts.

## Comparison of Solutions

The practice harness's `practice/decode_ways/reference.py` implements the **Space-Optimized DP** solution.

### Time Complexity

- **Brute Force**: `O(2^n)` - every route re-cuts the suffixes before it, and
  the tree branches up to two ways per digit.
- **Top-Down Memoization**: `O(n)` - one body run per position, later visits
  are dictionary hits.
- **Bottom-Up DP**: `O(n)` - one pass seeds the past-the-end slot, one pass
  applies the recurrence right-to-left.
- **Space-Optimized DP**: `O(n)` - the same single pass with two registers
  replacing the table.
- **Top-Down Memoization with functools.cache**: `O(n)` - the decorator
  reproduces the memoized run times.

### Space Complexity

- **Brute Force**: `O(n)` - recursion stack depth only.
- **Top-Down Memoization**: `O(n)` - one memo entry per position plus the
  stack.
- **Bottom-Up DP**: `O(n)` - the table holds `n + 1` entries.
- **Space-Optimized DP**: `O(1)` - two rolling totals.
- **Top-Down Memoization with functools.cache**: `O(n)` - the decorator's
  cache plus the stack.

### Trade-offs

- The Brute Force is the direct transcription of the cut-one-or-cut-two rule and needs no auxiliary structure, but it is the only approach here that misses the constraint budget for long strings.
- Both memoized versions keep the recursion's shape, which makes correctness easy to argue, at the price of stack depth `n` on top of the memo.
- The Bottom-Up DP pays the same linear time without recursion and keeps every suffix's count, which matters only when those counts are queried again later.
- The Space-Optimized DP gives up random access to old suffixes and keeps just the two live entries, reaching constant space with no new risk.

### When to Use Each

- **Brute Force**: as the derivational baseline and a correctness oracle for
  checking the faster versions on short strings.
- **Top-Down Memoization**: when the recurrence is easiest to trust in its
  recursive form and string lengths stay modest.
- **Bottom-Up DP**: when the per-suffix counts are reused by follow-up queries
  or variants of the problem.
- **Space-Optimized DP** (recommended): the default; the same linear pass at
  constant space, with the base case folded into the seed so no extra boundary slot survives.
- **Top-Down Memoization with functools.cache**: the Pythonic tidy-up when the
  recursive shape is wanted and the memo should not be hand-maintained.

### Optimization Notes

- The pair cut's value check `int(s[i:i+2]) <= 26` is only sound together with
  the boundary check `i + 1 < len(s)`: on the final position the two-character slice degrades to one character, which always passes the value check and pushes the recursion off the end. Every approach must state that boundary once, as an explicit guard (recursive versions), as a hand-seeded final entry (table), or as the loop's start index (rolling).
- The two rolling seeds `one_back = 1, two_back = 0` are the table's
  `dp[n] = 1` plus an unread slot; keeping the seed semantics in mind prevents the classic off-by-one where the empty suffix is seeded `0` and every count collapses to `0`.
- The memoized versions recurse to depth `n`, so a string at the constraint cap
  of 100 digits sits far below Python's default recursion limit; for much longer strings the iterative table or the rolling totals avoid the stack entirely.
- The suffix counts are Fibonacci numbers in disguise: on an all-nonzero string where every adjacent pair is at most `26` (for example `"111111"`), the recurrence reduces to `dp[i] = dp[i + 1] + dp[i + 2]`, and the counts grow as Fibonacci, which is why the gauntlet case of twenty-two `1`s expects `28657`.
