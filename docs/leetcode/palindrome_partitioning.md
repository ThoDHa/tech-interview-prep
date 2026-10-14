# [Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/)

**Medium** | **25 minutes** | **String, Dynamic Programming, Backtracking**

**Pattern:** [Backtracking](../patterns/backtracking_exploration/intuition.md), [String DP](../patterns/string_dp/intuition.md)

**Algorithm:** [Backtracking](https://en.wikipedia.org/wiki/Backtracking) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Longest palindromic substring](https://en.wikipedia.org/wiki/Longest_palindromic_substring)

**Practice:** [`practice/palindrome_partitioning/solution.py`](../../practice/palindrome_partitioning/solution.py)

Given a string `s`, split `s` into substrings where every substring is a palindrome. Return all possible lists of palindromic substrings.

You may return the solution in **any order**.

## Examples

### Example 1

**Input:** `s = "aab"`

**Output:** `[["a","a","b"],["aa","b"]]`

### Example 2

**Input:** `s = "a"`

**Output:** `[["a"]]`

## Constraints

- `1 <= s.length <= 20`
- `s` contains only lowercase English letters.

## Deriving the Solution

Reading the definition from left to right turns one global question into many local ones: a partition of `s` is a choice of cut positions, each piece between consecutive cuts must be a palindrome, and whether a slice of `s` is a palindrome depends only on that slice. Every solution below places cuts one at a time from the left, so a partial answer is always a list of palindromic pieces covering a prefix of `s`. The approaches differ in when they test palindromicity and how often they repeat the same test.

1. **Start literal.** Every cut set is a candidate: enumerate all `2^(n-1)`
   ways to place cuts, build each split's pieces, and test every piece after
   the fact, costing `O(n × 2^n)` with nothing rejected early: see
   [Brute Force](#brute-force).
2. **Test during construction.** A slice that is not a palindrome disqualifies
   every split through it, so test `s[start:end]` the moment it is proposed
   and never descend into a doomed prefix: the explored tree now ends only in
   answers. See [Backtracking](#backtracking).
3. **Answer the palindrome question once.** The search asks the same
   question over and over: is `s[i..j]` a palindrome? Fill an `n × n` table
   of verdicts in one `O(n^2)` pass, the Longest Palindromic Substring
   recurrence, and let the search read cells instead of scanning slices: see
   [Palindrome Table](#palindrome-table).
4. **Fill the partition table directly.** Every partition of the suffix
   `s[i:]` is a palindromic prefix followed by a partition of a later suffix,
   so a single descending sweep composes `parts[i]` from already-finished
   rows with no search at all: see [Bottom-Up DP](#bottom-up-dp).
5. **Memoize instead of tabulating.** The bottom-up fill computes every
   suffix's partitions, reached or not. Decorate the top-down recursion with
   [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache)
   and only the suffix positions the search actually visits are computed,
   once each: see [Top-Down Memoization](#top-down-memoization).

## Solutions

### Brute Force

#### Derivation

The most literal reading treats a partition as a set of cut positions: place cuts anywhere, read off the pieces between them, and keep the placements whose pieces are all palindromes. Nothing in that reading looks at the characters until the finished split is tested, which makes it the simplest complete enumeration of the answer:

1. Define `all_splits(start)` to return every split of the suffix `s[start:]`.
2. Base case: when `start == len(s)` the suffix is empty, and `[[]]` is its
   one split.
3. Otherwise, for each `end` from `start + 1` through `len(s)`, prepend the
   prefix `s[start:end]` to every split of the suffix `s[end:]`.
4. Filter `all_splits(0)` with the per-piece test
   `piece == piece[::-1]` and return what survives.

#### Walkthrough

Let us split Example 1 by hand: `s = "aab"` has two cut slots, one after each character, so there are `2^2 = 4` raw splits, each checked with the palindrome test:

```text
["a", "a", "b"]  every piece is a palindrome  -> keep
["a", "ab"]      ["ab"] reversed is ["ba"]    -> discard
["aa", "b"]      every piece is a palindrome  -> keep
["aab"]          ["aab"] reversed is ["baa"]  -> discard
```

Two of the four survive, and the function returns `[["a", "a", "b"], ["aa", "b"]]`, matching the expected Output for Example 1. Note what the discard rows cost: `["aab"]` was built piece by piece and scanned in full even though its single piece fails the test in one comparison. The enumeration never looks at characters until a split is complete, so no cut placement is ever rejected early.

#### Solution

The code is the walkthrough's two layers: the suffix recursion that produces every split, and the per-piece palindrome test that filters it.

```python
from typing import List


class Solution:
    def partition(self, s: str) -> List[List[str]]:
        def all_splits(start: int) -> List[List[str]]:
            if start == len(s):
                return [[]]
            splits: List[List[str]] = []
            for end in range(start + 1, len(s) + 1):
                for rest in all_splits(end):
                    splits.append([s[start:end]] + rest)
            return splits

        return [
            parts for parts in all_splits(0)
            if all(piece == piece[::-1] for piece in parts)
        ]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × 2^n)`

The suffix recursion forks at every position, producing `2^(n-1)` raw splits (each of the `n - 1` cut slots is independently present or absent). Building and testing each split touches every piece in it, `O(n)` work per split, and no split is ever rejected before it is complete.

##### Space Complexity: `O(n × 2^n)`

The result holds up to `2^(n-1)` partitions of up to `n` pieces. The filter runs only after `all_splits(0)` has returned, so at its peak the full unfiltered list of `2^(n-1)` raw splits is alive at once, and the recursion stack adds `O(n)`.

#### Key Insights

- Renaming the problem makes the search space exact: partitions of `s` are
  precisely the splits of `s`, and the suffix recursion enumerates each cut
  set exactly once, so no deduplication is ever needed.
- The palindrome test runs only on finished splits: a raw split containing
  `ab` is discovered invalid only after every piece around it has been built
  and copied.
- Simple to derive and hard to get wrong, which is exactly what makes it a
  good baseline for correctness-checking the faster versions.

### Backtracking

#### Derivation

The brute force learns a split is not a partition only after the finished split is tested, but the palindrome definition already judges every prefix: a piece is a contiguous slice of `s`, and if `s[start:end]` is not a palindrome, no completion of the split can repair it. Moving the test to construction time turns enumeration into [backtracking](https://en.wikipedia.org/wiki/Backtracking): push palindromic prefixes onto a shared `path`, recurse on the remainder, and pop on the way out. Every explored prefix stays extendable to a full partition, so the tree's leaves are exactly the answers:

1. Carry the shared `path` list of pieces and recurse on `start`, the
   position the next piece must begin at.
2. Base case: when `start == len(s)`, `path` covers all of `s`; append a copy
   `path[:]` to `result` and return.
3. For each `end` from `start + 1` through `len(s)`, take
   `prefix = s[start:end]`; when `prefix == prefix[::-1]`, append it to
   `path`, recurse with `backtrack(end)`, and pop it back off.
4. Launch `backtrack(0)` and return `result`.

#### Walkthrough

Let us run the search on Example 1: `s = "aab"`. The trace indents one level per call; each push is paired with a pop, and a non-palindromic prefix is skipped in place with one comparison:

```text
backtrack(0)   path = []
  prefix s[0:1] = "a"  palindrome -> push   path = []
  backtrack(1)
    prefix s[1:2] = "a"  palindrome -> push   path = ["a"]
    backtrack(2)
      prefix s[2:3] = "b"  palindrome -> push   path = ["a", "a"]
        backtrack(3)  -> record ["a", "a", "b"]
      pop "b"      -> path = ["a", "a"]
    pop "a"      -> path = ["a"]
    prefix s[1:3] = "ab"  "ab" != "ba"  skip
  pop "a"      -> path = []
  prefix s[0:2] = "aa"  palindrome -> push   path = []
  backtrack(2)
    prefix s[2:3] = "b"  palindrome -> push   path = ["aa"]
      backtrack(3)  -> record ["aa", "b"]
    pop "b"      -> path = ["aa"]
  pop "aa"     -> path = []
  prefix s[0:3] = "aab"  "aab" != "baa"  skip
```

The two leaves recorded, in the order found, are `["a", "a", "b"]` and `["aa", "b"]`, which is the expected Output for Example 1. The two skip lines are the whole pruning story: `s[1:3]` and `s[0:3]` were each rejected by a single comparison and never descended into, while every branch the search did walk ended in a recorded partition. Nothing that could not become a partition was ever built.

#### Solution

The code is the walkthrough's tree: the palindrome guard before each push, the pop undoing each push, the copy at each leaf.

```python
from typing import List


class Solution:
    def partition(self, s: str) -> List[List[str]]:
        result: List[List[str]] = []
        path: List[str] = []

        def backtrack(start: int) -> None:
            if start == len(s):
                result.append(path[:])
                return
            for end in range(start + 1, len(s) + 1):
                prefix = s[start:end]
                if prefix == prefix[::-1]:
                    path.append(prefix)
                    backtrack(end)
                    path.pop()

        backtrack(0)
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × 2^n)`

Pruning removes the doomed branches, but the answer itself is exponential: every partition is a distinct leaf, and there are inputs (a string of one repeated character) where all `2^(n-1)` cut placements survive, so up to `2^n` nodes are explored. A node's loop tests every remaining prefix, and a prefix of length `d` is proposed only on paths that leave the `d - 1` slots inside it uncut, exponentially few as `d` grows; summed over the tree, the slice tests cost `O(n × 2^n)` character comparisons. Copying the up-to-`2^(n-1)` answer partitions at `O(n)` each adds another `O(n × 2^n)`, and the two together give the bound.

##### Space Complexity: `O(n)`

Excluding the output, the search keeps one shared `path` of at most `n` pieces plus the recursion stack at the same depth. No per-branch copies exist: the copy at a leaf goes straight into `result`, and the pops restore `path` before each sibling branch runs.

#### Key Insights

- The guard placement is the entire algorithm: testing `prefix` before the
  push, not after the leaf, is what makes every explored branch productive.
- The `path[:]` copy at the leaf is load-bearing: appending `path` itself
  would record the same list `n` times, and the final pops would empty it.
- Branch order is free: reordering the `end` loop changes only the output's
  order, which the problem states is arbitrary.

### Palindrome Table

#### Derivation

The search repeats a question the string can answer once for all: is `s[i..j]` a palindrome? The same verdict is recomputed at every tree node whose branch proposes that slice. This is the [Longest Palindromic Substring](https://en.wikipedia.org/wiki/Longest_palindromic_substring) situation, and its classical dynamic program answers every pair `(i, j)` in one `O(n^2)` fill. The palindrome property composes inward: a slice is a palindrome exactly when its end characters match and its interior is one, so a slice's verdict reads a verdict for a strictly shorter slice. Filling by descending `i` guarantees the inner verdict is finished before anything reads it:

1. Let `is_pal[i][j]` record whether the slice `s[i..j]` is a palindrome,
   with every cell starting `False`.
2. Fill with `i` descending from `n - 1` and `j` ascending from `i`:
   `is_pal[i][j]` is `s[i] == s[j]` and, when the slice is longer than two,
   `is_pal[i + 1][j - 1]`.
3. Redefine the search over cell lookups: `backtrack(start)` loops `end` from
   `start` to `len(s) - 1` and pushes `s[start:end + 1]` whenever
   `is_pal[start][end]` is `True`; the base case at `start == len(s)` is
   unchanged.
4. Launch `backtrack(0)` after the fill completes and return `result`.

#### Walkthrough

Two phases. First the fill, computed for Example 1 with `i` descending so each cell reads the row below it, which is already final; each cell shows its slice and its verdict:

```text
       j=0      j=1      j=2
i=0    "a":1    "aa":1   "aab":0
i=1             "a":1    "ab":0
i=2                      "b":1
```

Every diagonal cell is `1` because single characters are palindromes by definition, `"aa"` holds because its two characters match with no interior to check, and `"aab"` fails because `s[0] != s[2]`. Then the search runs on lookups alone:

```text
backtrack(0)   path = []
  is_pal[0][0] ("a")  True   -> push   path = []
  backtrack(1)
    is_pal[1][1] ("a")  True   -> push   path = ["a"]
    backtrack(2)
      is_pal[2][2] ("b")  True   -> push   path = ["a", "a"]
        backtrack(3)  -> record ["a", "a", "b"]
      pop "b"      -> path = ["a", "a"]
    pop "a"      -> path = ["a"]
    is_pal[1][2] ("ab")  False  -> skip
  pop "a"      -> path = []
  is_pal[0][1] ("aa")  True   -> push   path = []
  backtrack(2)
    is_pal[2][2] ("b")  True   -> push   path = ["aa"]
      backtrack(3)  -> record ["aa", "b"]
    pop "b"      -> path = ["aa"]
  pop "aa"     -> path = []
  is_pal[0][2] ("aab")  False  -> skip
```

The recorded partitions are the same two as before, in the same order: the lookup answers exactly the question the inline test asked. The tree's shape is identical to the Backtracking version's; the difference is that each node's test read a precomputed cell instead of scanning a slice, which pays when wide branching makes the same cells get read over and over.

#### Solution

The code is the fill followed by the same search, reading cells instead of slicing.

```python
from typing import List


class Solution:
    def partition(self, s: str) -> List[List[str]]:
        n = len(s)
        is_pal: List[List[bool]] = [[False] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            for j in range(i, n):
                is_pal[i][j] = s[i] == s[j] and (
                    j - i < 2 or is_pal[i + 1][j - 1]
                )

        result: List[List[str]] = []
        path: List[str] = []

        def backtrack(start: int) -> None:
            if start == n:
                result.append(path[:])
                return
            for end in range(start, n):
                if is_pal[start][end]:
                    path.append(s[start:end + 1])
                    backtrack(end + 1)
                    path.pop()

        backtrack(0)
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × 2^n)`

The fill is `O(n^2)` and the search is the Backtracking search with a cheaper per-node test, so the same output-proportional bound holds with the `O(n^2)` fill absorbed by it for all but the smallest outputs.

##### Space Complexity: `O(n^2)`

The `is_pal` grid holds `n^2` booleans regardless of how many partitions exist, which dominates the `O(n)` shared `path` and recursion stack. The output is excluded as before.

#### Key Insights

- The recurrence looks only one cell inward because a palindrome loses its
  two outer characters at once: one step of `i + 1, j - 1` per comparison,
  not a rescan of the interior.
- The descending `i` fill order is what makes the two-line recurrence sound:
  `is_pal[i + 1][j - 1]` sits in the row finished just before row `i` runs.
- This is the exact setup of the follow-up problem Palindrome Partitioning
  II, where the same grid serves a minimization instead of an enumeration.

### Bottom-Up DP

#### Derivation

The top-down versions build each partition by walking, but the partitions of a suffix are compositions of smaller ones: the suffix `s[i:]` has exactly one partition for every way of peeling a palindromic prefix `s[i:j]` off the front and continuing with any partition of `s[j:]`. Since `j > i`, those continuations live in strictly later rows, so one descending sweep composes every row from already-finished ones and the search disappears into a [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) fill:

1. Let `parts[i]` hold every partition of the suffix `s[i:]`, and seed
   `parts[n] = [[]]` for the empty suffix.
2. Sweep `i` from `n - 1` down to `0`.
3. For each cut `j` from `i + 1` through `n`: when `s[i:j]` is a palindrome,
   append `[s[i:j]] + rest` to `parts[i]` for every `rest` in `parts[j]`.
4. Return `parts[0]`.

#### Recurrence

Let `parts[i]` be every partition of the suffix `s[i:]`:

$$ parts[i] = \begin{cases}
[[]], & i = n \\[4pt]
\bigl[\; [\, s[i:j] \,] + rest \;:\; j \in (i, n],\ s[i:j] \text{ a palindrome},\ rest \in parts[j] \;\bigr], & i < n
\end{cases} $$

```text
parts[n] = [[]]
parts[i] = [ [s[i:j]] + rest
             for j in i+1 .. n with s[i:j] a palindrome
             for rest in parts[j] ]
```

The base case gives the empty suffix its one empty partition, and every other row concatenates each palindromic prefix with every already-finished partition of the remainder. No row over-counts: a partition of `s[i:]` has exactly one first piece, so exactly one `j` can produce it, and the union is disjoint. The answer is read from `parts[0]`.

#### Walkthrough

Let us fill the table for Example 1 by hand. Each palindrome branch appends its completions to its row; the row summaries show the finished entries:

```text
parts[3] = [[]]                the empty suffix has the empty partition
i = 2:  s[2:3] = "b"  palindrome -> [["b"]]              parts[2] grows by 1
          parts[2] = [["b"]]
i = 1:  s[1:2] = "a"  palindrome -> [["a", "b"]]         parts[1] grows by 1
i = 1:  s[1:3] = "ab"  not a palindrome -> nothing appended
          parts[1] = [["a", "b"]]
i = 0:  s[0:1] = "a"  palindrome -> [["a", "a", "b"]]    parts[0] grows by 1
i = 0:  s[0:2] = "aa"  palindrome -> [["aa", "b"]]       parts[0] grows by 1
i = 0:  s[0:3] = "aab"  not a palindrome -> nothing appended
          parts[0] = [["a", "a", "b"], ["aa", "b"]]
```

Reading `parts[0]` gives `[["a", "a", "b"], ["aa", "b"]]`, the expected Output for Example 1. The two entries differ exactly in whether the first cut fell after position 1 or after position 2, and each was appended by exactly one branch of the fill, so no deduplication pass is ever needed.

#### Solution

The code is the fill: three nested loops and one concatenation.

```python
from typing import List


class Solution:
    def partition(self, s: str) -> List[List[str]]:
        n = len(s)
        parts: List[List[List[str]]] = [[] for _ in range(n + 1)]
        parts[n] = [[]]

        for i in range(n - 1, -1, -1):
            for j in range(i + 1, n + 1):
                prefix = s[i:j]
                if prefix == prefix[::-1]:
                    for rest in parts[j]:
                        parts[i].append([prefix] + rest)

        return parts[0]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × 2^n)`

Each completed partition is copied once into its row at `O(n)` per copy, and the `O(n^2)` prefix tests run whether or not they complete anything. For small outputs the tests dominate, exactly as in the Palindrome Table fill; for large ones the copies do, and the bound is the output's either way.

##### Space Complexity: `O(n × 2^n)`

The table holds the partitions of every suffix at once, and `parts[0]`, the answer, is nearly the whole of it: every partition of `s` appears in `parts[0]`, and later rows hold progressively smaller fractions.

#### Key Insights

- The base case `parts[n] = [[]]` is the only seed: one empty partition of
  the empty suffix, and every other entry in the table grows out of it.
- The descending sweep is what makes the fill sound: `parts[i]` is finished
  before any earlier row reads it, so no partition is ever composed from a
  half-built continuation.
- It computes every suffix's partitions even though only `parts[0]` is
  asked, which costs memory against the search versions while removing the
  recursion entirely.

### Top-Down Memoization

#### Derivation

The bottom-up fill proves how the partitions of a suffix compose, but it computes every suffix's list, including suffixes the search from `0` would never visit. The top-down recursion visits only what the answer needs. Keep the relation and the loop exactly as the fill wrote them, and let [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) stand in for the table: the decorator runs the body once per distinct `start` and answers every repeat visit from its dictionary, which collapses the shared subtrees the plain search re-walked:

1. Define `parts(start)` to return every partition of the suffix
   `s[start:]`, decorated with `@cache`.
2. Base case: return `[[]]` when `start == len(s)`.
3. Otherwise loop `end` from `start + 1` through `len(s)`; for each
   palindromic `s[start:end]`, extend the result with `[prefix] + rest` for
   every `rest` in `parts(end)`.
4. Return `parts(0)`. Every suffix position reached is computed at most
   once, and any later arrival is a dictionary lookup.

#### Walkthrough

Let us run the decorated recursion on Example 1, `s = "aab"`, showing for each call which child computations it requested and which arrived from the cache:

```text
parts(3)   base case -> [[]]
parts(2)   "b" -> parts(3)
parts(1)   "a" -> parts(2)  "ab" not a palindrome
parts(0)   "a" -> parts(1)  "aa" -> parts(2)   cache hit  "aab" not a palindrome
result = [["a", "a", "b"], ["aa", "b"]]
parts.cache_info() -> hits=1, misses=4, currsize=4
```

Position `2` is reached twice, once as the remainder after the piece `"a"` and once after `"aa"`. The first arrival ran the body and stored the result; the second was answered from the dictionary without entering it. `cache_info()` confirms the shape: four misses, one per distinct position reached (`3`, `2`, `1`, `0`), and exactly one hit. The result is `[["a", "a", "b"], ["aa", "b"]]`, the expected Output for Example 1.

#### Solution

The bottom-up relation with the table swapped for a decorator.

```python
from functools import cache
from typing import List


class Solution:
    def partition(self, s: str) -> List[List[str]]:
        n = len(s)

        @cache
        def parts(start: int) -> List[List[str]]:
            if start == n:
                return [[]]
            out: List[List[str]] = []
            for end in range(start + 1, n + 1):
                prefix = s[start:end]
                if prefix == prefix[::-1]:
                    for rest in parts(end):
                        out.append([prefix] + rest)
            return out

        return parts(0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × 2^n)`

Each distinct suffix position runs its loop at most once, and one run performs `O(n)` prefix tests and one `O(n)` copy per completed partition; repeat visits are dictionary lookups. Collapsing shared subtrees changes the constant against the plain search, not the class: on inputs where every cut placement survives there is nothing to share and the full `2^(n-1)`-leaf work remains.

##### Space Complexity: `O(n × 2^n)`

The cache holds one result list per distinct position reached, and those lists together hold every partition of every visited suffix; the returned structure shares its entries with the cache rather than copying them. The recursion stack adds `O(n)`.

#### Key Insights

- Whether the memo pays depends on the input's overlap: on Example 1 exactly
  one subtree is shared, while on `"aaaa"` nearly every suffix is reachable
  by many piece sequences and the cache collapses all of that re-derivation.
- `@cache` is safe here only because the cached function takes the integer
  `start` alone: `s` stays captured by the closure, so the key is always
  hashable and per-call. A module-level memo over `s` would return one
  input's partitions for another's.
- In side-by-side timings against the Bottom-Up DP fill, the two track the
  same asymptotic work but not the same constant: on every input timed, the
  decorator's C-implemented dictionary version ran 30 to 50 percent faster
  than the hand-written table. Its edge is also strict in reach: whenever
  some suffixes are unreachable from position `0`, they are never computed
  at all.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n × 2^n)` - builds and scans all `2^(n-1)` raw splits,
  testing each only when finished.
- **Backtracking**: `O(n × 2^n)` - one palindrome comparison per branch, but
  every explored branch ends in a real partition.
- **Palindrome Table**: `O(n × 2^n)` - an `O(n^2)` fill replaces the
  per-branch scan; the output bound absorbs the fill beyond small outputs.
  Measured on 15-to-17-character inputs it traded places with plain
  Backtracking: about 20 percent ahead on the maximal cut-set input, about
  55 percent behind on a periodic input whose search tree is shallow.
- **Bottom-Up DP**: `O(n × 2^n)` - copies every completed partition once and
  runs all `O(n^2)` prefix tests besides.
- **Top-Down Memoization**: `O(n × 2^n)` - the search with shared subtrees
  collapsed to one run each.

### Space Complexity

- **Brute Force**: `O(n × 2^n)` - the raw split list holds everything
  unfiltered at its peak.
- **Backtracking**: `O(n)` - shared `path` plus recursion stack, output
  excluded.
- **Palindrome Table**: `O(n^2)` - the boolean grid dominates the `O(n)`
  path and stack.
- **Bottom-Up DP**: `O(n × 2^n)` - the table keeps every suffix's partitions.
- **Top-Down Memoization**: `O(n × 2^n)` - the cache holds every visited
  suffix's partitions.

### Trade-offs

- **Brute Force**: nothing subtle to get wrong beyond the split recursion,
  but it constructs and scans splits that no partition ever wanted.
- **Backtracking**: the pure pruning view with constant extra space, but it
  re-tests the same slices whenever different paths propose them.
- **Palindrome Table**: precomputes every palindrome verdict once so the
  search cannot re-ask the question, at the price of an `n^2` grid that
  never shrinks with the output.
- **Bottom-Up DP**: removes the recursion and visits every branch exactly
  once, but materializes partitions for suffixes the answer may barely use.
- **Top-Down Memoization**: computes only the suffix positions actually
  reached, skipping doomed branches and recomputation alike, with the
  decorator hiding the table management the Bottom-Up DP writes by hand.

### When to Use Each

- **Brute Force**: as the derivational baseline and the correctness oracle
  the other four were checked against.
- **Backtracking** (recommended): the interview default; it is the smallest
  correct program and its guard is the problem's whole idea.
- **Palindrome Table**: when the input is dense in shared slices or a
  variant eliminates the repeated palindrome checks by precomputing, as the
  Palindrome Partitioning II follow-up does.
- **Bottom-Up DP**: when recursion depth matters or the suffix tables
  themselves are wanted.
- **Top-Down Memoization**: when the bottom-up loop feels mechanical: it is
  the same relation stated top-down, computing only what is reached.

### Optimization Notes

- The `is_pal` fill is the Longest Palindromic Substring dynamic program
  unrestricted: it answers every pair `(i, j)` rather than only the longest.
  Expanding around centers produces the same verdicts with a smaller
  constant, and Manacher's algorithm computes all palindromic radii in
  `O(n)`, from which any `is_pal[i][j]` verdict follows in constant time if
  the grid's `O(n^2)` space ever mattered at `n = 20`.
- All timing statements in these notes were measured on CPython, best of
  nine runs with garbage collection disabled, on 15-to-17-character inputs
  near the constraint limit. Top-Down Memoization was the fastest version on
  every input timed. Its margin over plain Backtracking widened as the
  output shrank: on `"a" * 16`, whose answer is the full `32768`-partition
  cut-set tree, Backtracking ran about three times the compositional
  pair's time, and on a 15-character periodic input with `465` partitions
  it ran about four times their time, because shared prefixes were
  re-tested on every path.
- The Palindrome Table traded places with plain Backtracking across the
  inputs timed: the `O(n^2)` fill is paid once up front, while the inline
  reversal is paid per branch, so which wins depends on how much the search
  re-tests shared slices. On `"a" * 16`, whose answer is the full cut-set
  tree and nearly every proposed slice is a palindrome, the table ran about
  20 percent ahead; on a 15-character periodic input dense in near-miss
  prefixes it ran about 55 percent behind, the fill wasted on slices the
  shallow search tree never proposed.
- The copy discipline differs by structure, not by taste: the two search
  versions mutate one shared `path` and copy at the leaf, while the two
  compositional versions build fresh `[prefix] + rest` lists per completion.
  Mixing the styles, such as appending `path` itself at the leaf, aliases one
  list into every answer and is the classic bug of this problem family.
- Branch and loop order are free correctness-wise: any order of `end` values
  or of `i` within a row changes only the output's order, which the problem
  states is arbitrary. The descending `i` fill is the one ordering that is
  not free: it is what guarantees `parts[j]` and `is_pal[i + 1][j - 1]` are
  finished before they are read.
