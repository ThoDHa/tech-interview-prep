# [Group Anagrams](https://www.fastprep.io/problems/amazon-group-anagrams)

**Medium** | **NN minutes** | **String, Array, Hash Table, Sorting**

Group the strings in strs so that two strings appear in the same group exactly when they are anagrams.

For this exercise, assume every string contains only lowercase English letters. Do not sort the characters of a string to determine its group. Build a fixed 26-entry character-count vector and use that vector as the grouping key.

## Examples

### Example 1

**Input:** `strs = ["eat","tea","tan","ate","nat","bat"]`

**Output:** `[["ate","eat","tea"],["bat"],["nat","tan"]]`

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-group-anagrams; fill them in. -->

## Solutions

### Brute Force

#### Derivation

The most literal reading of "group the anagrams" keeps a growing list of groups and files each incoming string into the first group it belongs to. Belonging is decided by the anagram test from [Valid Anagram](../leetcode/valid_anagram.md): two strings are anagrams exactly when their 26-slot character counts cancel to zero:

1. Keep an empty list `groups`, where each entry holds the members of one
   anagram class.
2. For each string `s`, compare it against the first member of every existing
   group with a count-based anagram test.
3. On the first match, append `s` to that group and move to the next string.
4. If no group matches, start a new group containing only `s`.
5. Return the groups in the deterministic output order: sort the strings
   inside each group, then sort the groups by their first string.

#### Walkthrough

Trace the filing loop on Example 1: `strs = ["eat","tea","tan","ate","nat","bat"]`. Each row shows the incoming string and the state of `groups` after it is filed:

```text
"eat"   no groups yet     -> groups = [["eat"]]
"tea"   vs "eat": anagram -> groups = [["eat","tea"]]
"tan"   vs "eat": no      -> groups = [["eat","tea"], ["tan"]]
"ate"   vs "eat": anagram -> groups = [["eat","tea","ate"], ["tan"]]
"nat"   vs "eat": no, vs "tan": anagram
                          -> groups = [["eat","tea","ate"], ["tan","nat"]]
"bat"   vs "eat": no, vs "tan": no
                          -> groups = [["eat","tea","ate"], ["tan","nat"], ["bat"]]
```

Every string lands in a group, and no two groups hold a shared character multiset. The final `groups` contains `[["eat","tea","ate"], ["tan","nat"], ["bat"]]`; sorting members inside each group and then the groups by their first string yields `[["ate","eat","tea"], ["bat"], ["nat","tan"]]`, matching the expected Output.

#### Solution

The code is the filing loop from the walkthrough, with the anagram test as a helper and the deterministic output sort on return.

```python
from typing import List


class Solution:
    def solve(self, strs: List[str]) -> List[List[str]]:
        groups: List[List[str]] = []
        for s in strs:
            for group in groups:
                if self._is_anagram(group[0], s):
                    group.append(s)
                    break
            else:
                groups.append([s])
        return sorted(sorted(group) for group in groups)

    def _is_anagram(self, first: str, second: str) -> bool:
        counts = [0] * 26
        for character in first:
            counts[ord(character) - ord("a")] += 1
        for character in second:
            counts[ord(character) - ord("a")] -= 1
        return all(count == 0 for count in counts)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n² × k)`

Filing one string costs one `O(k)` anagram test against each existing group, and up to `n` groups can exist, so the total is `O(n² × k)` for `n` strings of length up to `k`.

##### Space Complexity: `O(n × k)`

The output holds every input string exactly once, which is linear in the total input size.

#### Key Insights

- Reads directly as the problem statement, with the anagram test as the only helper; the counts decide group membership, and sorting touches only the finished groups.
- The pairwise rescans are the bottleneck: nothing about a settled comparison is remembered.
- Correct for any alphabet, since the test never assumes a fixed letter set beyond what the counts array covers.

### Character Count Key

#### Derivation

The brute force re-asks "are these two the same multiset?" for every string against every group. Collapsing each string to one canonical value turns that pairwise question into a bucketing question: two strings are anagrams exactly when their canonical forms are equal, so a hash map from canonical form to group members files every string in one pass. The counts themselves are the canonical form. With only lowercase English letters, each string's multiset fits a 26-slot array, and arrays compare equal exactly when the multisets match. A raw list cannot hash because it is mutable, but its `tuple` is immutable and hashes by value:

1. Create an empty dictionary `groups`.
2. For each string `s`, build `counts`, a 26-slot array indexed by
   `ord(c) - ord("a")`.
3. Use `tuple(counts)` as the bucket key and append `s` to its bucket,
   creating the bucket on first sight.
4. Return the buckets in the deterministic output order: sort the strings
   inside each group, then sort the groups by their first string.

Two strings land in the same bucket exactly when every letter occurs equally often in both, which is the definition of an anagram pair.

#### Walkthrough

Trace the count tuples on Example 1: `strs = ["eat","tea","tan","ate","nat","bat"]`. Only the nonzero slots are shown, written as letter-count pairs:

```text
"eat"   counts (a:1, e:1, t:1)   new bucket 1
"tea"   counts (a:1, e:1, t:1)   same key as "eat" -> bucket 1
"tan"   counts (a:1, n:1, t:1)   new bucket 2
"ate"   counts (a:1, e:1, t:1)   same key again    -> bucket 1
"nat"   counts (a:1, n:1, t:1)   same key as "tan" -> bucket 2
"bat"   counts (a:1, b:1, t:1)   new bucket 3
```

Three tuples survive, and each string joined the bucket holding its exact letter totals. The buckets are `[["eat","tea","ate"], ["tan","nat"], ["bat"]]`; sorting members inside each group and then the groups by their first string yields `[["ate","eat","tea"], ["bat"], ["nat","tan"]]`, matching the expected Output. The same mechanism keeps different totals apart: `"dddddddddd"` and `"dggggggggg"` share only the letters `d` and `g`, but their tuples put `d:10, g:1` against `d:1, g:10`, so they never collide.

#### Solution

The code is the walkthrough's tally-and-bucket step over the fixed 26-slot array.

```python
from typing import List


class Solution:
    def solve(self, strs: List[str]) -> List[List[str]]:
        groups = {}
        for s in strs:
            counts = [0] * 26
            for character in s:
                counts[ord(character) - ord("a")] += 1
            groups.setdefault(tuple(counts), []).append(s)
        return sorted(sorted(group) for group in groups.values())
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × k)`

Each of the `n` strings is tallied in `O(k)`, and hashing a 26-slot tuple is constant per string.

##### Space Complexity: `O(n × k)`

The buckets hold all input strings, and each distinct group contributes one fixed-size 26-slot tuple key.

#### Key Insights

- Counting is the signature: the multiset itself, not any ordering of it, identifies the anagram class.
- The fixed alphabet bounds the key size at 26 slots regardless of string length, so the per-key hashing cost is constant.
- Wrapping the mutable count list in a `tuple` is what makes it hashable.

### Sorted String Key

#### Derivation

The Character Count Key needs the lowercase-only assumption to bound its array at 26 slots. When the alphabet is unknown or unbounded, [sorting](https://en.wikipedia.org/wiki/Sorting_algorithm) supplies the canonical form instead: a string's characters in sorted order are identical for all and only its anagrams, with no assumption about which characters appear:

1. Create an empty dictionary `groups`.
2. For each string `s`, compute `key = "".join(sorted(s))`.
3. Append `s` to the bucket `groups[key]`, creating the bucket on first sight.
4. Return the buckets in the deterministic output order: sort the strings
   inside each group, then sort the groups by their first string.

The map never inspects two strings together; equality of keys does all the comparing.

#### Walkthrough

Trace the key computation on Example 1: `strs = ["eat","tea","tan","ate","nat","bat"]`. Each row shows the string, its sorted key, and the bucket it lands in:

```text
"eat"   sorted -> "aet"    bucket "aet" = ["eat"]
"tea"   sorted -> "aet"    bucket "aet" = ["eat","tea"]
"tan"   sorted -> "ant"    bucket "ant" = ["tan"]
"ate"   sorted -> "aet"    bucket "aet" = ["eat","tea","ate"]
"nat"   sorted -> "ant"    bucket "ant" = ["tan","nat"]
"bat"   sorted -> "abt"    bucket "abt" = ["bat"]
```

Three distinct keys emerge, `"aet"`, `"ant"`, and `"abt"`, and every anagram of Example 1 shares one of them. The bucket values are `[["eat","tea","ate"], ["tan","nat"], ["bat"]]`; the output sort yields `[["ate","eat","tea"], ["bat"], ["nat","tan"]]`, matching the expected Output.

#### Solution

The code is the walkthrough's key-and-bucket step, repeated for every string.

```python
from typing import List


class Solution:
    def solve(self, strs: List[str]) -> List[List[str]]:
        groups = {}
        for s in strs:
            key = "".join(sorted(s))
            groups.setdefault(key, []).append(s)
        return sorted(sorted(group) for group in groups.values())
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × k log k)`

Each of the `n` strings is sorted in `O(k log k)`, and the bucketing itself is amortized `O(1)` per string.

##### Space Complexity: `O(n × k)`

The dictionary stores the keys (one sorted string per distinct group) and all `n` input strings across the buckets.

#### Key Insights

- Replaces pairwise comparison with canonical-form equality: each string is processed once.
- The sort is the only cost beyond a linear pass, and it is paid per string rather than per pair.
- Works for any alphabet, since sorting assumes nothing about which characters appear.

### Counter Key

#### Derivation

The Character Count Key already established that the letter tallies are the whole signature; the only remaining work is writing the tally, and Python's standard library has done that too. [`Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) builds the frequency map in one call. A `Counter` is a mutable `dict` and cannot hash directly, but its `(character, count)` items are unique pairs, so a `frozenset` of them is an immutable value that equals another exactly when the two counters hold the same items:

1. Create an empty dictionary `groups`.
2. For each string `s`, compute `key = frozenset(Counter(s).items())`.
3. Append `s` to the bucket `groups[key]`, creating the bucket on first sight.
4. Return the buckets in the deterministic output order: sort the strings
   inside each group, then sort the groups by their first string.

#### Walkthrough

Trace the keys on Example 1's two largest classes. Here `Counter` performs the same tally the Character Count Key built by hand:

```text
"eat"   Counter -> {e:1, a:1, t:1}       frozenset {(e,1), (a,1), (t,1)}
"tea"   Counter -> {t:1, e:1, a:1}       frozenset {(t,1), (e,1), (a,1)}  equal
"tan"   Counter -> {t:1, a:1, n:1}       frozenset {(t,1), (a,1), (n,1)}
"ate"   Counter -> {a:1, t:1, e:1}       same frozenset as "eat"  equal
"nat"   Counter -> {n:1, a:1, t:1}       same frozenset as "tan"  equal
"bat"   Counter -> {b:1, a:1, t:1}       new frozenset
```

Set equality ignores insertion order and compares the pairs as values, so the three classes separate exactly as before: the buckets are `[["eat","tea","ate"], ["tan","nat"], ["bat"]]`, and the output sort yields `[["ate","eat","tea"], ["bat"], ["nat","tan"]]`, matching the expected Output.

#### Solution

The code is the walkthrough's tally delegated to `Counter`, with the `frozenset` as the hashable signature.

```python
from collections import Counter
from typing import List


class Solution:
    def solve(self, strs: List[str]) -> List[List[str]]:
        groups = {}
        for s in strs:
            key = frozenset(Counter(s).items())
            groups.setdefault(key, []).append(s)
        return sorted(sorted(group) for group in groups.values())
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × k)`

Each `Counter` construction is a linear pass over its string, and freezing and hashing the item set touches at most one entry per distinct letter.

##### Space Complexity: `O(n × k)`

The buckets hold all input strings; each distinct group adds one frozen item set bounded by the alphabet size.

#### Key Insights

- The most concise tally: `Counter` replaces the hand-rolled 26-slot loop.
- `frozenset` of `(character, count)` pairs is the hashable stand-in for Counter equality, because counts make every pair unique per character.
- Tied with the count tuple on asymptotics; prefer the tuple when hashing cost per key must stay constant regardless of how many distinct letters a string uses.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n² × k)` - each string is anagram-tested against every existing group.
- **Character Count Key**: `O(n × k)` - one linear tally per string, no sorting.
- **Sorted String Key**: `O(n × k log k)` - sorting each string dominates the single bucketing pass.
- **Counter Key**: `O(n × k)` - the same tally delegated to the standard library.

### Space Complexity

- **Brute Force**: `O(n × k)` - the output groups plus the scratch counts per test.
- **Character Count Key**: `O(n × k)` - bucket members plus one fixed-size tuple key per group.
- **Sorted String Key**: `O(n × k)` - bucket members plus one sorted key per group.
- **Counter Key**: `O(n × k)` - bucket members plus one frozen item set per group.

### Trade-offs

- **Brute Force** needs no canonical form and works on any alphabet, but the pairwise rescans collapse on large inputs.
- **Character Count Key** removes the sort by leaning on the fixed lowercase alphabet, and its keys hash in constant time.
- **Sorted String Key** is the shortest route to a canonical form when the alphabet is unknown, paying a per-string sort.
- **Counter Key** trades a little of the tuple's strict constant-factor control for the most readable tally.

### When to Use Each

- **Brute Force**: tiny inputs or settings where no hashable canonical form is available.
- **Character Count Key**: production and interviews over a known small alphabet (recommended here, and the variant this exercise asks for).
- **Sorted String Key**: the default when the alphabet is unknown or unbounded.
- **Counter Key**: Python code that values readability and leans on the standard library.

### Optimization Notes

- All bucketing approaches share one property worth stating in an interview: the output preserves every input string, so total space equals the input size plus the keys.
- The Character Count Key's per-key hashing cost is constant (26 slots), while the Sorted String Key's key length grows with `k`; hashing is the hidden term when comparing the two.
- All bucketing versions pay one extra `O(n log n × k)` sort over the finished groups for the deterministic output order (members sorted, groups sorted by first string); the grouping itself never reorders anything, so a caller that accepts any order can skip the final sort.
