# [Permutation In String](https://leetcode.com/problems/permutation-in-string/)

**Medium** | **25 minutes** | **Hash Table, Two Pointers, String, Sliding Window**

**Pattern:** [Sliding Window](../patterns/sliding_window/intuition.md), [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Algorithm:** [Sliding window](https://usaco.guide/gold/sliding-window) · [Hash table](https://en.wikipedia.org/wiki/Hash_table)

**Practice:** [`practice/permutation_in_string/solution.py`](../../practice/permutation_in_string/solution.py)

You are given two strings `s1` and `s2`.

Return `true` if `s2` contains a permutation of `s1`, or `false` otherwise. That means if a permutation of `s1` exists as a substring of `s2`, then return `true`.

Both strings only contain lowercase letters.

## Examples

### Example 1

**Input:** `s1 = "abc", s2 = "lecabee"`

**Output:** `true`

**Explanation:** The substring `"cab"` is a permutation of `"abc"` and is present in `"lecabee"`.

### Example 2

**Input:** `s1 = "abc", s2 = "lecaabee"`

**Output:** `false`

## Constraints

- `1 <= s1.length, s2.length <= 10000`

## Deriving the Solution

A permutation of `s1` inside `s2` is any window of exactly `len(s1)` characters holding the same *multiset* of letters as `s1`; the order inside the window is irrelevant. So the question "is some permutation present?" becomes "does some fixed-width window match this multiset?", and every solution below is a strategy for comparing letter counts across windows.

1. **Start literal.** Generate every permutation of `s1` and search for each as a literal substring. There are up to `n1!` permutations, so this explodes immediately: see [Permutation Search](#permutation-search).
2. **Count, don't order.** Order is irrelevant, so instead of searching for each arrangement, count `s1`'s letters once and test every window of `s2` of the same width for identical counts. Each window test costs a 26-letter comparison: see [Fixed Window Count Compare](#fixed-window-count-compare).
3. **Update the count, don't rebuild it.** Adjacent windows differ by exactly one letter leaving and one letter entering, so the running comparison can be maintained in `O(1)` per slide. Track how many of the 26 letters are fully *matched*, and a window is an anagram exactly when all 26 are: see [Sliding Window with Match Count](#sliding-window-with-match-count).

## Solutions

### Permutation Search

#### Derivation

The most literal reading of "contains a permutation of `s1`" enumerates the permutations and looks for each one literally inside `s2`. Python's standard library supplies the arrangements (`itertools.permutations`) and the substring search (`in`):

1. Reject immediately when `len(s1) > len(s2)`: no window can be wide enough.
2. Generate every distinct ordering of `s1`'s characters as a string.
3. Return `True` on the first ordering found in `s2`; otherwise return `False`.

#### Walkthrough

Trace the search on Example 1: `s1 = "abc"`, `s2 = "lecabee"`. The six orderings are checked in turn:

```text
"abc"  in "lecabee"?  no
"acb"  in "lecabee"?  no
"bac"  in "lecabee"?  no
"bca"  in "lecabee"?  no
"cab"  in "lecabee"?  yes -> return True
```

`"cab"` occurs at index 2, so the search succeeds, matching Example 1's expected Output. Example 2, `s2 = "lecaabee"`, exhausts all six orderings with no hit and returns `False`, also matching.

#### Solution

```python
from itertools import permutations


class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False
        seen = set()
        for candidate in permutations(s1):
            ordering = "".join(candidate)
            if ordering not in seen:
                seen.add(ordering)
                if ordering in s2:
                    return True
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n1! * n1 * n2)`

Up to `n1!` orderings, each built in `O(n1)` and searched in `O(n2)`. Even `s1` of length 10 has 3.6 million orderings.

##### Space Complexity: `O(n1!)`

The `seen` set may hold every distinct ordering of `s1`.

#### Key Insights

- Correct by construction, since it checks every candidate arrangement directly.
- The factorial blow-up makes it unusable beyond trivial `s1` lengths, which is the point of the exercise: permutations of a *multiset* are the wrong search key.
- The deduplication set handles repeated letters (as in `"aab"`, whose 6 raw permutations collapse to 3 distinct strings) but does not touch the exponential growth.

### Fixed Window Count Compare

#### Derivation

Order is a red herring: two strings are permutations of each other exactly when every letter occurs equally often in both. So build `s1`'s frequency count once, then slide a window of width `len(s1)` across `s2`, rebuilding the window's count from scratch at each position, and compare the two 26-slot tables for equality:

1. Reject immediately when `len(s1) > len(s2)`.
2. Build `need`, `s1`'s 26-slot count array.
3. For each window start `left` in `0..len(s2) - len(s1)`, build the window's count array.
4. Return `True` the first time the arrays are equal; otherwise return `False`.

#### Walkthrough

Trace the window tests on Example 1: `s1 = "abc"`, `s2 = "lecabee"`, windows of width 3. Only nonzero letters are shown:

```text
left=0  "lec"   {l:1, e:1, c:1}   != {a:1, b:1, c:1}
left=1  "eca"   {e:1, c:1, a:1}   != {a:1, b:1, c:1}
left=2  "cab"   {c:1, a:1, b:1}   == {a:1, b:1, c:1} -> return True
```

The third window's counts match `need` exactly, so the function returns `True`, matching Example 1's expected Output. On Example 2, `s2 = "lecaabee"`, no window of width 3 holds one each of `a`, `b`, `c` (the windows are `"lec"`, `"eca"`, `"caa"`, `"aab"`, `"abe"`, `"bee"`), so every comparison fails and the function returns `False`.

#### Solution

The code is the per-window rebuild-and-compare loop over 26-slot arrays.

```python
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        n1, n2 = len(s1), len(s2)
        if n1 > n2:
            return False
        need = [0] * 26
        base = ord("a")
        for char in s1:
            need[ord(char) - base] += 1
        for left in range(n2 - n1 + 1):
            window = [0] * 26
            for i in range(left, left + n1):
                window[ord(s2[i]) - base] += 1
            if window == need:
                return True
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n1 * n2)`

There are `O(n2)` windows, and each is filled and compared in `O(n1 + 26)`.

##### Space Complexity: `O(1)`

Two 26-slot arrays regardless of input sizes.

#### Key Insights

- Reframes the problem from ordering (factorial) to counting (linear per window), which is the conceptual leap the whole file rests on.
- The 26-letter alphabet bound keeps every comparison constant, making this solvable, though the window rebuild still rescans `s1`'s worth of letters per position.
- `window == need` compares lists element-wise, so dictionary-free equality over fixed slots is both correct and fast.

### Sliding Window with Match Count

#### Derivation

Rebuilding each window from scratch ignores what adjacent windows share: sliding right by one retires exactly one letter and admits exactly one. Maintain the window's count incrementally, and derive a cheaper equality signal than comparing 26 slots per step. Keep `need`, the count the window still owes for each letter, and `matches`, the number of letters (of the 26) whose window count equals its `need` count. A window is an anagram exactly when `matches == 26`. Each slide touches two letters and each letter's arrival or departure moves `matches` by at most one:

1. Reject immediately when `n1 > n2`.
2. Seed `need` from `s1` and `window` from `s2`'s first `n1` letters; count `matches` over all 26 letters.
3. Return `True` at once if the seed window already matches.
4. For each new `right` from `n1` to `n2 - 1`: admit `s2[right]`, updating `matches` when its count crosses to or away from equality; retire `s2[right - n1]` the same way.
5. Return `True` whenever `matches == 26` after a slide; `False` if the sweep ends without one.

The update rules are where care belongs. Admitting letter `x` raises `window[x]`: if that lands exactly on `need[x]`, a letter just became matched (`matches += 1`); if it lands on `need[x] + 1`, a letter just broke (`matches -= 1`); otherwise equality state did not change. Retiring letter `x` lowers `window[x]` symmetrically: landing on `need[x]` gains a match, landing on `need[x] - 1` loses one.

#### Walkthrough

Trace the sweep on a short tailored input (Example 1's full 7-slide trace is long; this one shows every rule firing): `s1 = "ab"`, `s2 = "ba"`:

```text
seed:    need {a:1, b:1}   window "ba" {b:1, a:1}
         letters a,b matched; other 24 letters trivially match (need 0, have 0)
         matches = 26 -> return True
```

The seed window alone settles it. A case that exercises the slide rules is `s1 = "adcda"`, `s2 = "cda"`, rejected at once by the length guard (`5 > 3`). Take instead `s1 = "ab"`, `s2 = "acb"`:

```text
seed:    window "ac"  {a:1, c:1}   need {a:1, b:1}
         a: have 1, need 1 -> matched
         b: have 0, need 1 -> unmatched
         c: have 1, need 0 -> unmatched
         matches = 25

right=2  admit 'b':  window[b] 0 -> 1 == need[b] 1  -> matches += 1 -> 26
         retire 'a': window[a] 1 -> 0 != need[a] 1  (0 == need - 1)  -> matches -= 1 -> 25
         matches = 25 -> continue
end of sweep -> return False
```

Both rules fire on the same slide: admitting `b` completes a letter, retiring `a` breaks one, and the two cancel. `"acb"` correctly holds no permutation of `"ab"`. On Example 1 the sweep reaches the window `"cab"` at `right = 4`: admitting `b` raises `matches` to 26 and the function returns `True` on the spot. On Example 2 no window ever reaches 26 matches and the function returns `False`.

#### Solution

The code is the seeded match count plus the two update rules per slide.

```python
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        n1, n2 = len(s1), len(s2)
        if n1 > n2:
            return False
        need = [0] * 26
        window = [0] * 26
        base = ord("a")
        for i in range(n1):
            need[ord(s1[i]) - base] += 1
            window[ord(s2[i]) - base] += 1
        matches = sum(1 for i in range(26) if need[i] == window[i])
        if matches == 26:
            return True
        for right in range(n1, n2):
            index = ord(s2[right]) - base
            window[index] += 1
            if window[index] == need[index]:
                matches += 1
            elif window[index] == need[index] + 1:
                matches -= 1
            left_index = ord(s2[right - n1]) - base
            window[left_index] -= 1
            if window[left_index] == need[left_index]:
                matches += 1
            elif window[left_index] == need[left_index] - 1:
                matches -= 1
            if matches == 26:
                return True
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n1 + n2)`

Seeding touches each string once. Each of the `n2 - n1` slides does constant work: two array updates, two comparisons, and one integer test against 26.

##### Space Complexity: `O(1)`

Two 26-slot arrays regardless of input sizes.

#### Key Insights

- The `matches` counter is the optimization: window equality is re-established in `O(1)` by tracking only how the two touched letters' equality states changed.
- Letters with `need == 0` participate too: admitting one necessarily walks its count from 0 (matched) to 1 (unmatched), which is why `"abc"` inside a sea of `z`s can never falsely match.
- Admit-and-retire order within a slide is irrelevant because the two letters' updates touch independent counters; only the final `matches == 26` test matters.
- This match-count pattern generalizes to Find All Anagrams and Minimum Window Substring, with the same need/window bookkeeping.

## Comparison of Solutions

### Time Complexity

- **Permutation Search**: `O(n1! * n1 * n2)` - factorial orderings, each searched linearly.
- **Fixed Window Count Compare**: `O(n1 * n2)` - every window rebuilt and compared from scratch.
- **Sliding Window with Match Count**: `O(n1 + n2)` - one pass with constant work per slide.

### Space Complexity

- **Permutation Search**: `O(n1!)` - the set of distinct orderings.
- **Fixed Window Count Compare**: `O(1)` - two 26-slot arrays.
- **Sliding Window with Match Count**: `O(1)` - two 26-slot arrays and a counter.

### Trade-offs

- **Permutation Search** is a direct transcription of the problem's words and is unusable beyond toy sizes.
- **Fixed Window Count Compare** is easy to trust: no incremental state, so no update bugs, but each window is built from zero.
- **Sliding Window with Match Count** eliminates the redundant rebuild; its subtlety is concentrated in the four match-update rules, which must cover exactly the equality crossings.

### When to Use Each

- **Permutation Search**: only to illustrate why order-first thinking fails.
- **Fixed Window Count Compare**: when correctness clarity matters more than speed, and inputs are small.
- **Sliding Window with Match Count**: the answer to the problem as stated (recommended here).

### Optimization Notes

- Comparing `window == need` per slide (26 slot tests per position) also passes the stated bounds and is simpler to write; `matches` matters when the alphabet or the window count grows.
- The early length guard `n1 > n2` is not merely an optimization: without it the seed loop would index out of bounds on `s2`.
- The same deficit-count pattern with a variable window solves Minimum Window Substring; here the window width is fixed, which is what reduces the check to a single integer comparison.
