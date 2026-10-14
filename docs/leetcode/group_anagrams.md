# [Group Anagrams](https://leetcode.com/problems/group-anagrams/)

**Medium** | **25 minutes** | **Array, Hash Table, String, Sorting**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Algorithm:** [Hash table](https://en.wikipedia.org/wiki/Hash_table) · [Sorting](https://en.wikipedia.org/wiki/Sorting_algorithm) · [Python `collections.Counter`](https://docs.python.org/3/library/collections.html#collections.Counter)

**Practice:** [`practice/group_anagrams/solution.py`](../../practice/group_anagrams/solution.py)

Given an array of strings `strs`, group all *anagrams* together into sublists. You may return the output in **any order**.

An **anagram** is a string that contains the exact same characters as another string, but the order of the characters can be different.

## Examples

### Example 1

**Input:** `strs = ["act","pots","tops","cat","stop","hat"]`

**Output:** `[["hat"],["act", "cat"],["stop", "pots", "tops"]]`

### Example 2

**Input:** `strs = ["x"]`

**Output:** `[["x"]]`

### Example 3

**Input:** `strs = [""]`

**Output:** `[[""]]`

## Constraints

- `1 <= strs.length <= 10000`.
- `0 <= strs[i].length <= 100`
- `strs[i]` is made up of lowercase English letters.

## Deriving the Solution

Two strings are anagrams exactly when they hold the same multiset of characters, so every anagram class shares one property: some canonical form derived from the character counts is identical across the class and different outside it. Every solution below either re-tests that property pairwise or reduces each string to such a form and buckets on it.

1. **Start literal.** Group by asking, for each string, whether it is an anagram of the first member of each group found so far, using a linear anagram test. Each string rescans every existing group, costing `O(n² * k)`: see [Brute Force](#brute-force).
2. **Spot the waste.** The pairwise test recomputes the same equality over and over: "act" versus "cat" and "tops" versus "stop" are settled independently, and nothing remembers what was learned. If each string collapsed to one canonical value, equal values could be collected in a single pass.
3. **Canonicalize by sorting.** Sorting a string's characters gathers the multiset into one agreed order, so anagrams sort to the same string. Use the sorted string as a hash key and bucket in one pass, `O(n * k log k)`: see [Sorted String Key](#sorted-string-key).
4. **Canonicalize by counting instead.** The order sorting produces is irrelevant; only the letter counts matter. With lowercase English letters a 26-slot count tuple is the same signature without any sorting, reaching `O(n * k)`: see [Character Count Key](#character-count-key).
5. **Library shortcut last.** [`Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) performs the tally in one call, and a `frozenset` of its items serves as the hashable signature: see [Counter Key](#counter-key).

## Solutions

### Brute Force

#### Derivation

The most literal reading of "group the anagrams" keeps a growing list of groups and files each incoming string into the first group it belongs to. Belonging is decided by the anagram test from [Valid Anagram](valid_anagram.md): two strings are anagrams exactly when their 26-slot character counts cancel to zero:

1. Keep an empty list `groups`, where each entry holds the members of one anagram class.
2. For each string `s`, compare it against the first member of every existing group with a count-based anagram test.
3. On the first match, append `s` to that group and move to the next string.
4. If no group matches, start a new group containing only `s`.
5. Return `groups` after every string is filed.

#### Walkthrough

Trace the filing loop on Example 1: `strs = ["act","pots","tops","cat","stop","hat"]`. Each row shows the incoming string and the state of `groups` after it is filed:

```text
"act"   no groups yet            -> groups = [["act"]]
"pots"  vs "act": not anagrams   -> groups = [["act"], ["pots"]]
"tops"  vs "act": no             vs "pots": yes
                                 -> groups = [["act"], ["pots","tops"]]
"cat"   vs "act": yes            -> groups = [["act","cat"], ["pots","tops"]]
"stop"  vs "act": no             vs "pots": yes
                                 -> groups = [["act","cat"], ["pots","tops","stop"]]
"hat"   vs "act": no             vs "pots": no
                                 -> groups = [["act","cat"], ["pots","tops","stop"], ["hat"]]
```

Every string lands in a group, and no two groups hold a shared character multiset. The final `groups` contains `[["act","cat"], ["pots","tops","stop"], ["hat"]]`, which is Example 1's output up to the allowed reordering.

#### Solution

The code is the filing loop from the walkthrough, with the anagram test as a helper.

```python
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups: List[List[str]] = []
        for s in strs:
            for group in groups:
                if self._is_anagram(group[0], s):
                    group.append(s)
                    break
            else:
                groups.append([s])
        return groups

    def _is_anagram(self, a: str, b: str) -> bool:
        counts = [0] * 26
        for c in a:
            counts[ord(c) - ord("a")] += 1
        for c in b:
            counts[ord(c) - ord("a")] -= 1
        return all(count == 0 for count in counts)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n² * k)`

Filing one string costs one `O(k)` anagram test against each existing group, and up to `n` groups can exist, so the total is `O(n² * k)` for `n` strings of length up to `k`.

##### Space Complexity: `O(n * k)`

The output holds every input string exactly once, which is linear in the total input size.

#### Key Insights

- Reads directly as the problem statement, with the anagram test reused from Valid Anagram.
- The pairwise rescans are the bottleneck: nothing about a settled comparison is remembered.
- Correct for any alphabet, since the test never assumes a fixed letter set beyond what the counts array covers.

### Sorted String Key

#### Derivation

The brute force pays because it re-asks "are these two the same multiset?" for every pair. Collapsing each string to one canonical value turns that pairwise question into a bucketing question: two strings are anagrams exactly when their canonical forms are equal, so a hash map from canonical form to group members files every string in one pass. [Sorting](https://en.wikipedia.org/wiki/Sorting_algorithm) supplies the simplest canonical form: a string's characters in sorted order are identical for all and only its anagrams:

1. Create an empty dictionary `groups`.
2. For each string `s`, compute `key = "".join(sorted(s))`.
3. Append `s` to the bucket `groups[key]`, creating the bucket on first sight.
4. Return the list of bucket values.

The map never inspects two strings together; equality of keys does all the comparing.

#### Walkthrough

Trace the key computation on Example 1: `strs = ["act","pots","tops","cat","stop","hat"]`. Each row shows the string, its sorted key, and the bucket it lands in:

```text
"act"   sorted -> "act"    bucket "act"           = ["act"]
"pots"  sorted -> "opst"    bucket "opst"          = ["pots"]
"tops"  sorted -> "opst"    bucket "opst"          = ["pots","tops"]
"cat"   sorted -> "act"     bucket "act"           = ["act","cat"]
"stop"  sorted -> "opst"    bucket "opst"          = ["pots","tops","stop"]
"hat"   sorted -> "aht"     bucket "aht"           = ["hat"]
```

Three distinct keys emerge, `"act"`, `"opst"`, and `"aht"`, and every anagram of Example 1 shares one of them. The bucket values are `[["act","cat"], ["pots","tops","stop"], ["hat"]]`, matching the expected output up to reordering.

#### Solution

The code is the walkthrough's key-and-bucket step, repeated for every string.

```python
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = {}
        for s in strs:
            key = "".join(sorted(s))
            groups.setdefault(key, []).append(s)
        return list(groups.values())
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * k log k)`

Each of the `n` strings is sorted in `O(k log k)`, and the bucketing itself is amortized `O(1)` per string.

##### Space Complexity: `O(n * k)`

The dictionary stores the keys (one sorted string per distinct group) and all `n` input strings across the buckets.

#### Key Insights

- Replaces pairwise comparison with canonical-form equality: each string is processed once.
- The sort is the only cost beyond a linear pass, and it is paid per string rather than per pair.
- Works for any alphabet, since sorting assumes nothing about which characters appear.

### Character Count Key

#### Derivation

The sorted key spends `O(k log k)` arranging characters into an order that is then immediately forgotten: only the letter totals distinguish anagrams. The counts themselves are a tighter canonical form. With only lowercase English letters, each string's multiset fits a 26-slot array, and arrays compare equal exactly when the multisets match. A raw list cannot hash because it is mutable, but its `tuple` is immutable and hashes by value:

1. Create an empty dictionary `groups`.
2. For each string `s`, build `counts`, a 26-slot array indexed by `ord(c) - ord("a")`.
3. Use `tuple(counts)` as the bucket key and append `s` to its bucket.
4. Return the list of bucket values.

Two strings land in the same bucket exactly when every letter occurs equally often in both, which is the definition of an anagram pair.

#### Walkthrough

Trace the count tuples on Example 1: `strs = ["act","pots","tops","cat","stop","hat"]`. Only the nonzero slots are shown, written as letter-count pairs:

```text
"act"   counts (a:1, c:1, t:1)   tuple key lands in bucket 1
"pots"  counts (o:1, p:1, s:1, t:1)   new bucket 2
"tops"  counts (o:1, p:1, s:1, t:1)   same key as "pots" -> bucket 2
"cat"   counts (a:1, c:1, t:1)   same key as "act"  -> bucket 1
"stop"  counts (o:1, p:1, s:1, t:1)   same key again     -> bucket 2
"hat"   counts (a:1, h:1, t:1)   new bucket 3
```

Three tuples survive, and each string joined the bucket holding its exact letter totals. The buckets are `[["act","cat"], ["pots","tops","stop"], ["hat"]]`, matching the expected output up to reordering. The same mechanism keeps different totals apart: `"ddddddddddg"` and `"dggggggggggg"` share only the letters `d` and `g`, but their tuples put `d:10, g:1` against `d:1, g:10`, so they never collide.

#### Solution

The code is the walkthrough's tally-and-bucket step over the fixed 26-slot array.

```python
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = {}
        for s in strs:
            counts = [0] * 26
            for c in s:
                counts[ord(c) - ord("a")] += 1
            groups.setdefault(tuple(counts), []).append(s)
        return list(groups.values())
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * k)`

Each of the `n` strings is tallied in `O(k)`, and hashing a 26-slot tuple is constant per string, so the sort cost of the previous approach disappears.

##### Space Complexity: `O(n * k)`

The buckets hold all input strings, and each distinct group contributes one fixed-size 26-slot tuple key.

#### Key Insights

- Counting replaces sorting: the multiset itself, not any ordering of it, is the signature.
- The fixed alphabet bounds the key size at 26 slots regardless of string length.
- Wrapping the mutable count list in a `tuple` is what makes it hashable.

### Counter Key

#### Derivation

The Character Count Key already established that the letter tallies are the whole signature; the only remaining work is writing the tally, and Python's standard library has done that too. [`Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) builds the frequency map in one call. A `Counter` is a mutable `dict` and cannot hash directly, but its `(character, count)` items are unique pairs, so a `frozenset` of them is an immutable value that equals another exactly when the two counters hold the same items:

1. Create an empty dictionary `groups`.
2. For each string `s`, compute `key = frozenset(Counter(s).items())`.
3. Append `s` to the bucket `groups[key]`, creating the bucket on first sight.
4. Return the list of bucket values.

#### Walkthrough

Trace the keys on Example 1's two largest classes. Here `Counter` performs the same tally the Character Count Key built by hand:

```text
"act"   Counter -> {a:1, c:1, t:1}       frozenset {(a,1), (c,1), (t,1)}
"cat"   Counter -> {c:1, a:1, t:1}       frozenset {(a,1), (c,1), (t,1)}  equal
"pots"  Counter -> {p:1, o:1, t:1, s:1}  frozenset {(p,1), (o,1), (t,1), (s,1)}
"tops"  Counter -> {t:1, o:1, p:1, s:1}  same frozenset  equal
"stop"  Counter -> {s:1, t:1, o:1, p:1}  same frozenset  equal
"hat"   Counter -> {h:1, a:1, t:1}       new frozenset
```

Set equality ignores insertion order and compares the pairs as values, so the three classes separate exactly as before: `[["act","cat"], ["pots","tops","stop"], ["hat"]]`, matching the expected output up to reordering.

#### Solution

The code is the walkthrough's tally delegated to `Counter`, with the `frozenset` as the hashable signature.

```python
from collections import Counter
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = {}
        for s in strs:
            key = frozenset(Counter(s).items())
            groups.setdefault(key, []).append(s)
        return list(groups.values())
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * k)`

Each `Counter` construction is a linear pass over its string, and freezing and hashing the item set touches at most one entry per distinct letter.

##### Space Complexity: `O(n * k)`

The buckets hold all input strings; each distinct group adds one frozen item set bounded by the alphabet size.

#### Key Insights

- The most concise tally: `Counter` replaces the hand-rolled 26-slot loop.
- `frozenset` of `(character, count)` pairs is the hashable stand-in for Counter equality, because counts make every pair unique per character.
- Tied with the count tuple on asymptotics; prefer it for readability in Python, and prefer the tuple when hashing cost per key must stay constant regardless of how many distinct letters a string uses.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n² * k)` - each string is anagram-tested against every existing group.
- **Sorted String Key**: `O(n * k log k)` - sorting each string dominates the single bucketing pass.
- **Character Count Key**: `O(n * k)` - one linear tally per string, no sorting.
- **Counter Key**: `O(n * k)` - the same tally delegated to the standard library.

### Space Complexity

- **Brute Force**: `O(n * k)` - the output groups plus the scratch counts per test.
- **Sorted String Key**: `O(n * k)` - bucket members plus one sorted key per group.
- **Character Count Key**: `O(n * k)` - bucket members plus one fixed-size tuple key per group.
- **Counter Key**: `O(n * k)` - bucket members plus one frozen item set per group.

### Trade-offs

- **Brute Force** needs no canonical form and works on any alphabet, but the pairwise rescans collapse on large inputs.
- **Sorted String Key** is the shortest from-scratch route to canonical form, paying a per-string sort.
- **Character Count Key** removes the sort by leaning on the fixed lowercase alphabet, and its keys hash in constant time.
- **Counter Key** trades a little of the tuple's strict constant-factor control for the most readable tally.

### When to Use Each

- **Brute Force**: tiny inputs or settings where no hashable canonical form is available.
- **Sorted String Key**: the default when the alphabet is unknown or unbounded.
- **Character Count Key**: production and interviews over a known small alphabet (recommended here).
- **Counter Key**: Python code that values readability and leans on the standard library.

### Optimization Notes

- All bucketing approaches share one property worth stating in an interview: the output preserves every input string, so total space equals the input size plus the keys.
- The Character Count Key's per-key hashing cost is constant (26 slots), while the Sorted String Key's key length grows with `k`; hashing is the hidden term when comparing the two.
- For the any-order output, no ordering of groups or of members within a group is significant, which is why every walkthrough compares its result up to reordering.
