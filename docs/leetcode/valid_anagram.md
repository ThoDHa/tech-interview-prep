# [Valid Anagram](https://leetcode.com/problems/valid-anagram/)

**Easy** | **15 minutes** | **String**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Algorithm:** [Hash table](https://en.wikipedia.org/wiki/Hash_table) · [Sorting](https://en.wikipedia.org/wiki/Sorting_algorithm) · [Python `collections.Counter`](https://docs.python.org/3/library/collections.html#collections.Counter)

**Practice:** [`practice/valid_anagram/solution.py`](../../practice/valid_anagram/solution.py)

Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.

An **anagram** is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

## Examples

### Example 1

**Input:** `s = "anagram"`, `t = "nagaram"`

**Output:** `true`

### Example 2

**Input:** `s = "rat"`, `t = "car"`

**Output:** `false`

## Constraints

- `1 <= s.length, t.length <= 5 * 10^4`
- `s` and `t` consist of lowercase English letters.

## Follow-up

What if the inputs contain Unicode characters? How would you adapt your solution to such a case?

## Deriving the Solution

Rearranging the same letters means the two strings hold the same multiset of characters: every character appears in `t` exactly as many times as in `s`. Every solution below is a different way of comparing those two multisets, and all but the last two begin with the same length check, since strings of different lengths cannot possibly match.

1. **Start literal.** Act out "rearranging the letters": for each character of
   `t`, find an unused matching character in `s` and cross it off. Each cross-off rescans and rebuilds `s`, costing `O(n^2)`: see [Iterative Character Removal](#iterative-character-removal).
2. **Compare counts, not letters.** The order of letters never mattered, only
   how many times each one appears. Comparing `s.count(c)` against `t.count(c)` for each distinct character drops the string rebuilding, but every `count` call still rescans a whole string, leaving `O(n * k)`: see [Set-based Counting](#set-based-counting).
3. **Count in one pass.** Tally `s` into a dictionary once, then cancel counts
   while walking `t`. Two linear passes replace all the rescans, reaching `O(n)`: see [Hash Map Count](#hash-map-count).
4. **Exploit the fixed alphabet.** With only lowercase English letters, the
   dictionary collapses into a 26-slot array indexed by `ord(c) - ord("a")`: still `O(n)` time, now with true constant space and no hashing: see [Fixed Array Count](#fixed-array-count).
5. **Library shortcuts last.** Sorting both strings canonicalizes the multisets
   so a plain equality test decides the answer, at `O(n log n)`: see [Sorting](#sorting). `Counter` builds both frequency maps in one call each and compares them directly: see [Counter Comparison](#counter-comparison).

## Solutions

### Iterative Character Removal

#### Derivation

The definition says `t` is formed by rearranging the letters of `s`, using each exactly once. The most literal reading acts that sentence out: pair every character of `t` with an unused character of `s`, consuming `s` one character at a time:

1. If the strings differ in length they cannot be anagrams, so return `False`.
2. For each character `c` in `t`, look for `c` in the remaining `s`.
3. If `c` is present, remove a single occurrence with `replace(c, "", 1)`.
4. If `c` is missing, the strings are not anagrams, so return `False`.
5. If every character of `t` is matched and removed, return `True`.

Equal lengths plus a successful match for every character of `t` guarantees the two strings hold the same multiset of characters.

#### Walkthrough

Trace the removal loop on Example 1: `s = "anagram"`, `t = "nagaram"`. The lengths match (`7` and `7`), so the loop runs. Each row shows the character `c` taken from `t`, whether it is found in the current `s`, and the value of `s` after `replace(c, "", 1)` removes one copy:

| Step | `c` from `t` | Found in `s`? | `s` after removal |
|------|--------------|---------------|-------------------|
| start | - | - | `"anagram"` |
| 1 | `n` | yes | `"aagram"` |
| 2 | `a` | yes | `"agram"` |
| 3 | `g` | yes | `"aram"` |
| 4 | `a` | yes | `"ram"` |
| 5 | `r` | yes | `"am"` |
| 6 | `a` | yes | `"m"` |
| 7 | `m` | yes | `""` |

Every character of `t` was found and removed, so the loop never hits the `else` branch that would return `False`. After the final step `s` is empty, the loop ends, and the code returns `True`, which matches the expected Output `true`.

#### Solution

The code is the cross-off procedure from the walkthrough: one `replace` per character of `t`.

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        for c in t:
            if c in s:
                s = s.replace(c, "", 1)
            else:
                return False
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

For each of the `n` characters in `t` we search and rebuild `s`, and both the `in` test and `replace` scan the whole string in `O(n)`, giving `O(n²)` overall.

##### Space Complexity: `O(n)`

Strings are immutable, so each `replace` allocates a fresh copy of `s` whose length is proportional to the input.

#### Key Insights

- The most literal translation of "rearranging the same letters" into code.
- Quadratic time makes it unsuitable for the upper constraint of `5 * 10^4`.
- Repeated string copying compounds the cost because strings are immutable.

### Set-based Counting

#### Derivation

The removal loop wastes its effort on bookkeeping: rebuilding `s` after every match exists only to stop a character being used twice. The same guarantee falls out of counting: if every character appears equally often in both strings, no pairing step is needed at all. This version asks the counting question in the most direct way available, one distinct character at a time:

1. Reject mismatched lengths immediately.
2. Collect the distinct characters of `s` with `set(s)`.
3. For each distinct character, compare its occurrence count in `s` and `t`.
4. If any count differs, return `False`; otherwise return `True`.

Equal lengths mean that matching the count of every character present in `s` is sufficient: `t` cannot contain an extra unmatched character without exceeding the shared length.

#### Walkthrough

Trace the count comparison on Example 2: `s = "rat"`, `t = "car"`. The lengths match (`3` and `3`), so the loop runs over `set(s) = {'r', 'a', 't'}`. A set has no defined order, so the checks may come in any sequence; one possible run:

```text
c = 'r'   s.count('r') = 1   t.count('r') = 1   equal, continue
c = 'a'   s.count('a') = 1   t.count('a') = 1   equal, continue
c = 't'   s.count('t') = 1   t.count('t') = 0   differ -> return False
```

Counting by hand: `"rat"` holds one `'t'` but `"car"` holds none, so whichever order the set yields, the `'t'` check fails. The function returns `False`, matching the expected Output `false`.

#### Solution

The code is the per-character count comparison from the walkthrough, driven by the set of distinct characters.

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        for c in set(s):
            if s.count(c) != t.count(c):
                return False
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * k)`

Building the set is `O(n)`. For each of the up to `k` distinct characters, `count()` scans both strings in `O(n)`, yielding `O(n * k)`, which degrades to `O(n²)` when nearly every character is unique.

##### Space Complexity: `O(k)`

The set holds at most `k` distinct characters, where `k` is the alphabet size.

#### Key Insights

- Restricting the work to distinct characters trims the number of comparisons.
- Repeated `count()` calls reintroduce linear scans, so this is faster than
  iterative removal but slower than a single counting pass.
- Bounded only for a small alphabet; a large character set makes `k` grow.

### Hash Map Count

#### Derivation

The set-based version still rescans both strings once per distinct character, recomputing from scratch what a single pass could remember. The repair is to count each string only once: build a frequency table for `s`, then let `t` spend those counts back down. If `t` ever needs a character whose count is exhausted, the multisets differ:

1. Reject mismatched lengths immediately.
2. Build a [dictionary](https://en.wikipedia.org/wiki/Hash_table) `counter` mapping each character of `s` to its frequency.
3. Walk `t`, decrementing the matching count for each character.
4. If a character of `t` has no remaining count, return `False`.
5. Surviving the full walk means every count cancelled exactly, so return `True`.

The length check makes a single decrementing pass sufficient: if all counts stay non-negative and the totals match, the multisets are identical.

#### Walkthrough

Trace both passes on Example 1: `s = "anagram"`, `t = "nagaram"`. The first pass tallies `s` character by character:

```text
c = 'a'   counter = {'a': 1}
c = 'n'   counter = {'a': 1, 'n': 1}
c = 'a'   counter = {'a': 2, 'n': 1}
c = 'g'   counter = {'a': 2, 'n': 1, 'g': 1}
c = 'r'   counter = {'a': 2, 'n': 1, 'g': 1, 'r': 1}
c = 'a'   counter = {'a': 3, 'n': 1, 'g': 1, 'r': 1}
c = 'm'   counter = {'a': 3, 'n': 1, 'g': 1, 'r': 1, 'm': 1}
```

The second pass walks `t`, checking each character still has count left before decrementing it:

```text
c = 'n'   count 1 -> 0
c = 'a'   count 3 -> 2
c = 'g'   count 1 -> 0
c = 'a'   count 2 -> 1
c = 'r'   count 1 -> 0
c = 'a'   count 1 -> 0
c = 'm'   count 1 -> 0
```

No character of `t` ever finds a zero count, and after the walk every entry sits at exactly `0`: the counts cancelled perfectly. The function returns `True`, matching the expected Output `true`.

#### Solution

The code is the tally pass and the cancel pass from the walkthrough, in that order.

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        counter = {}
        for c in s:
            counter[c] = counter.get(c, 0) + 1
        for c in t:
            if counter.get(c, 0) == 0:
                return False
            counter[c] -= 1
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each string is traversed once, and every dictionary read or write is amortized `O(1)`, so the total is linear in the input length.

##### Space Complexity: `O(k)`

The dictionary stores at most `k` distinct characters, where `k` is the alphabet size (`26` for lowercase English letters).

#### Key Insights

- Linear time with no reliance on a counting library, making it portable to any
  language.
- A single decrement pass replaces repeated scans of the input.
- The length guard is what lets one-directional cancellation prove equality.

### Fixed Array Count

#### Derivation

The dictionary in the previous approach hashes every character it touches, yet the constraints promise only lowercase English letters: a known, fixed alphabet of 26. That means each character can be its own array index, `ord(c) - ord("a")`, and the dictionary shrinks to a 26-slot integer array with no hashing at all:

1. Reject mismatched lengths immediately.
2. Map each character to an index with `ord(c) - ord("a")`.
3. Increment the slot for every character in `s`.
4. Decrement the slot for every character in `t`, failing fast if any slot goes
   negative.
5. Equal lengths plus no negative slot means every count returned to zero, so
   return `True`.

#### Walkthrough

Trace the array on Example 2: `s = "rat"`, `t = "car"`, which exercises the fail-fast exit. With `base = ord("a") = 97`, the increment pass over `s` fills three slots (only nonzero slots are shown):

```text
c = 'r'   index 17   counts[17] = 1
c = 'a'   index 0    counts[0]  = 1
c = 't'   index 19   counts[19] = 1
```

The decrement pass over `t` starts with `'c'`:

```text
c = 'c'   index 2    counts[2] = 0 - 1 = -1   negative -> return False
```

`"rat"` contains no `'c'`, so slot `2` was never incremented and the very first decrement drives it to `-1`. The negative slot proves `t` needs a character `s` cannot supply, so the function returns `False` without ever reading `'a'` or `'r'`, matching the expected Output `false`.

#### Solution

The code is the two passes from the walkthrough over the 26-slot `counts` array.

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        counts = [0] * 26
        base = ord("a")
        for c in s:
            counts[ord(c) - base] += 1
        for c in t:
            counts[ord(c) - base] -= 1
            if counts[ord(c) - base] < 0:
                return False
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Both passes are linear, and array indexing by integer offset is a constant-time operation with no hashing.

##### Space Complexity: `O(1)`

The count array has a fixed size of `26` regardless of the input length, so the auxiliary space is constant.

#### Key Insights

- Trades generality for speed: direct integer indexing avoids hash overhead.
- Achieves true `O(1)` space because the alphabet size is fixed in advance.
- Fails fast on the first negative slot rather than counting `t` in full.

### Sorting

#### Derivation

All the counting approaches compare multisets entry by entry. A different question sidesteps the counting entirely: is there a canonical form that two anagrams, and only two anagrams, share? [Sorting](https://en.wikipedia.org/wiki/Sorting_algorithm) provides one. Placing the characters of each string in sorted order arranges equal multisets into identical sequences, so `sorted(s) == sorted(t)` decides the answer directly, and unequal lengths naturally produce unequal lists with no separate check:

1. Sort the characters of `s` and the characters of `t`.
2. Return whether the two sorted lists are equal.

#### Walkthrough

Trace the canonical forms on Example 1: `s = "anagram"`, `t = "nagaram"`. Here `sorted` is itself the technique: it rearranges each string's characters into ascending order, gathering equal letters together:

```text
sorted("anagram")  ['a', 'a', 'a', 'g', 'm', 'n', 'r']   3 a's, then g, m, n, r
sorted("nagaram")  ['a', 'a', 'a', 'g', 'm', 'n', 'r']   same letters, same order
```

Both strings hold three `'a'`s and one each of `'g'`, `'m'`, `'n'`, `'r'`, so sorting funnels them into the same sequence. The element-by-element list comparison finds every position equal and the function returns `True`, matching the expected Output `true`.

#### Solution

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return sorted(s) == sorted(t)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting each string costs `O(n log n)`, and the final list comparison is `O(n)`, which the sort dominates.

##### Space Complexity: `O(n)`

`sorted` materializes a new list of characters for each string, requiring linear additional space.

#### Key Insights

- Converts frequency matching into a canonical-form comparison through sorting.
- Cleaner to write than counting, at the cost of an `O(n log n)` sort rather than
  a linear pass.
- Scales naturally to Unicode because sorting assumes no fixed alphabet.

### Counter Comparison

#### Derivation

The Hash Map Count already showed that one tally per string settles the question; the only work left is writing the tally, and Python's standard library has done that too. [`Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) builds the frequency map of an iterable in one call, and two `Counter` objects compare equal exactly when every key has the same count. The length mismatch case comes free, since differing totals produce unequal counters:

1. Build `Counter(s)` and `Counter(t)`.
2. Return whether the two counters are equal.

#### Walkthrough

Trace the two counters on Example 1: `s = "anagram"`, `t = "nagaram"`. Here `Counter` is itself the technique: each constructor performs the same tally the Hash Map Count made by hand:

```text
Counter("anagram")   {'a': 3, 'n': 1, 'g': 1, 'r': 1, 'm': 1}
Counter("nagaram")   {'n': 1, 'a': 3, 'g': 1, 'r': 1, 'm': 1}
```

The two counters list their keys in different insertion orders, but dictionary equality ignores order: it checks that both hold the same keys with the same values. Every key (`a`, `n`, `g`, `r`, `m`) carries the same count in both, so `Counter(s) == Counter(t)` is `True`, matching the expected Output `true`.

#### Solution

```python
from collections import Counter


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return Counter(s) == Counter(t)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Constructing each `Counter` traverses its string once, and comparing the two counters for equality is linear in the number of distinct keys.

##### Space Complexity: `O(k)`

Each `Counter` stores at most `k` distinct characters, where `k` is the alphabet size.

#### Key Insights

- The most concise solution, leaning entirely on the standard library.
- Matches the hand-written counter's complexity while hiding the bookkeeping.
- A clear case of reaching for the right built-in tool when one exists.

## Comparison of Solutions

### Time Complexity

- **Iterative Character Removal**: `O(n²)` - Each removal rescans and rebuilds `s`.
- **Set-based Counting**: `O(n * k)` - Repeated `count()` scans per distinct character.
- **Hash Map Count**: `O(n)` - One counting pass plus one cancelling pass.
- **Fixed Array Count**: `O(n)` - Two linear passes over fixed-size integer slots.
- **Sorting**: `O(n log n)` - Sorting each string dominates the comparison.
- **Counter Comparison**: `O(n)` - Linear construction and comparison of counters.

### Space Complexity

- **Iterative Character Removal**: `O(n)` - New string copies on each replacement.
- **Set-based Counting**: `O(k)` - The set holds the distinct characters.
- **Hash Map Count**: `O(k)` - Dictionary of distinct character frequencies.
- **Fixed Array Count**: `O(1)` - A constant 26-slot array regardless of input.
- **Sorting**: `O(n)` - A new sorted list of characters for each string.
- **Counter Comparison**: `O(k)` - Each counter stores the distinct characters.

### Trade-offs

- **Iterative Character Removal** reads as the definition itself but is too slow
  for large inputs because of repeated string copying.
- **Set-based Counting** trims comparisons to distinct characters yet pays for
  repeated `count()` scans.
- **Hash Map Count** balances linear time with portable, library-free code.
- **Fixed Array Count** pushes to optimal constant space by exploiting the fixed
  alphabet, at the cost of being tied to that alphabet.
- **Sorting** is short and assumption-free about the alphabet, trading a linear
  pass for an `O(n log n)` sort.
- **Counter Comparison** is the most concise, delegating all bookkeeping to the
  standard library.

### When to Use Each

- **Iterative Character Removal**: Educational use or tiny inputs where speed is
  irrelevant.
- **Set-based Counting**: Small inputs or when set operations read more naturally.
- **Hash Map Count**: Production code and interviews that want linear time in any
  language (recommended for cross-language work).
- **Fixed Array Count**: Hot paths over a known small alphabet where constant
  space and no hashing matter.
- **Sorting**: When brevity matters, the `O(n log n)` cost is acceptable, or the
  alphabet cannot be assumed fixed.
- **Counter Comparison**: Python code that values readability and concision.

### Optimization Notes

- The early length check short-circuits every approach before any real work.
- The Fixed Array Count demonstrates the time-space tradeoff at its extreme:
  swapping the dictionary for a fixed array buys constant space and removes hashing overhead.
- For the Unicode follow-up, the Hash Map Count, Counter Comparison, and Sorting
  scale without modification, while the Fixed Array Count must widen or replace its 26-slot array, and Iterative Character Removal and Set-based Counting degrade further as the alphabet grows.
- Iterative Character Removal's repeated `replace` is especially costly because
  strings are immutable, forcing a fresh allocation on every step.
