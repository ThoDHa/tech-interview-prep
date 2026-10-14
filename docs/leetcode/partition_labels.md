# [Partition Labels](https://leetcode.com/problems/partition-labels/)

**Medium** | **25 minutes** | **Hash Table, Two Pointers, String, Greedy**

**Pattern:** [Greedy Core](../patterns/greedy_core/intuition.md), [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Algorithm:** [Greedy algorithm](https://en.wikipedia.org/wiki/Greedy_algorithm) · [Hash table](https://en.wikipedia.org/wiki/Hash_table) · [Two-pointer technique](https://usaco.guide/silver/two-pointers)

**Practice:** [`practice/partition_labels/solution.py`](../../practice/partition_labels/solution.py)

You are given a string `s` consisting of lowercase english letters.

We want to split the string into as many substrings as possible, while ensuring that each letter appears in at most one substring.

Return a list of integers representing the size of these substrings in the order they appear in the string.

## Examples

### Example 1

**Input:** `s = "xyxxyzbzbbisl"`

**Output:** `[5, 5, 1, 1, 1]`

**Explanation:** The string can be split into `["xyxxy", "zbzbb", "i", "s", "l"]`.

### Example 2

**Input:** `s = "abcabc"`

**Output:** `[6]`

## Constraints

- `1 <= s.length <= 100`

## Deriving the Solution

A partition is legal exactly when no letter crosses a cut, so the question "where may the next cut go?" is answered by a reachability fact: after cutting at position `cut`, every letter seen so far must have its final occurrence at or before `cut`. Each letter's last occurrence is a fixed property of the string, so every solution first reads those positions off and then decides cuts; the approaches differ in how much bookkeeping they keep while sweeping.

1. **Start literal.** Grow one partition at a time: for the current start, scan
   forward to find the farthest last occurrence among the letters inside, and
   extend the window whenever the scan uncovers a letter reaching farther.
   Each extension can force a rescan, so a partition costs up to `O(n)`: see
   [Brute Force Window Growth](#brute-force-window-growth).
2. **Spot the waste.** The growth loop re-derives "how far does this letter
   reach?" from the remaining string, when that answer is the same every time:
   one precomputed last-occurrence map turns each letter's reach into a lookup.
3. **Sweep with the map.** One pass records `last[s[ch]]`; a second pass walks
   the string once, carrying `partition_end` as the max reach of everything
   seen, and cuts exactly where the position catches up to it: see
   [Last-Occurrence Sweep](#last-occurrence-sweep).
4. **Re-price the bookkeeping.** Positions are not the only reach
   representation: occurrence counts are exact on sight, where last
   positions are only exact in hindsight. Sweeping with per-letter
   remaining counts and a live-letter window set decides the same cuts
   with cheaper state: see [Counting Sweep](#counting-sweep).

## Solutions

### Brute Force Window Growth

#### Derivation

The most direct reading builds one partition at a time. A partition starting at `start` must extend at least to the last occurrence of every letter it contains, and every extension can import a letter that reaches farther, so the honest brute force keeps rescanning until the window stops growing:

1. Start a window at `start = 0`.
2. Scan from `start` to the current `window_end`, and for each letter take its
   last occurrence by searching the rest of the string.
3. If that last occurrence exceeds `window_end`, push `window_end` out to it
   and rescan the grown window.
4. When a full scan finds nothing past `window_end`, cut there, record the
   size `window_end - start + 1`, and restart at `start = window_end + 1`.

The loop terminates because every window is finite and `start` strictly advances at each cut.

#### Walkthrough

Trace the growth on Example 2: `s = "abcabc"`, the input where one extension forces a rescan. Indexes are 0-based. The window starts at `start = 0` with `window_end = last("a") = 3` found by the initial scan:

```text
start=0  window_end=3  scan s[0..3] = "abca"
         last(a)=3, last(b)=4 -> 4 > 3   grow -> window_end=4, rescan
         last(c)=5 -> 5 > 4             grow -> window_end=5, rescan
         scan s[0..5] = "abcabc"  last(a)=3, last(b)=4, last(c)=5: none past 5
cut at 5 -> size 6, next start = 6 = end of string
```

Two grows each forced a fresh scan of the window, and the settled window covers the whole string: cutting anywhere earlier would split some letter's occurrences. The recorded sizes list is `[6]`, matching the expected Output for Example 2.

#### Solution

The code is the walkthrough's grow-and-rescan loop, with `last_index` doing the rest-of-string search per letter.

```python
from typing import List


class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        def last_index(ch: str) -> int:
            for position in range(len(s) - 1, -1, -1):
                if s[position] == ch:
                    return position
            return -1

        sizes: List[int] = []
        start = 0
        while start < len(s):
            window_end = last_index(s[start])
            cursor = start
            while cursor <= window_end:
                reach = last_index(s[cursor])
                if reach > window_end:
                    window_end = reach
                cursor += 1
            sizes.append(window_end - start + 1)
            start = window_end + 1
        return sizes
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each `last_index` call walks up to the whole string, and a single partition can trigger `O(n)` of them while its window grows, so one partition costs `O(n^2)` in the worst case; every window overall still touches `O(n)` positions, and `n` windows gives the `O(n^2)` bound. Strings built so that each new letter extends the window by one (the first half of a doubled alphabet) realize it.

##### Space Complexity: `O(1)`

Beyond the output list, only the window bounds and cursors are kept.

#### Key Insights

- The growth rule is the problem's core: a window is settled only when the farthest reach of everything inside it is inside it.
- The brute force recomputes each letter's reach from the string every time it needs it, which is the waste every later solution removes.
- The rescan is not paranoia: growing the window imports new letters whose reaches may lie past the old end, and skipping the rescan would cut through them.

### Last-Occurrence Sweep

#### Derivation

The growth loop's waste is re-deriving reach: "where does `ch` last occur?" has one answer for the whole run, so ask it once per letter up front. A hash map from letter to final position is filled in one pass, and then the sweep is mechanical: carry `partition_end`, the farthest reach among the letters seen in the current partition, and the partition is complete exactly when the cursor arrives at `partition_end`:

1. Fill `last` so `last[s[ch]]` is the final index of letter `ch`.
2. Start `partition_end = 0` and `partition_start = 0`.
3. For each position `ch`, set `partition_end` to
   `max(partition_end, last[s[ch]])`.
4. When `ch == partition_end`, the partition is closed: record
   `ch - partition_start + 1` and restart at `partition_start = ch + 1`.

The cut condition is safe because `last` is precomputed: nothing later in the string can retroactively extend a settled partition, which is exactly the fact the brute force had to keep re-verifying by rescanning.

#### Invariant

The cut fires at position `ch` only when `ch == partition_end`, and `partition_end` is maintained as the maximum `last` over the window's letters:

$$ \text{partition\_end} = \max_{\text{start} \le p \le \text{ch}} \text{last}[s[p]] $$

```text
partition_end = max of last[s[p]]  for every p in start..ch
```

Each step either reads a letter whose `last` is already `<= partition_end` (the max is unchanged) or raises `partition_end` to that letter's reach. So when the cursor reaches `partition_end`, every letter in `s[partition_start..ch]` has its final occurrence at or before `ch`: no letter crosses the cut. Every earlier position `q < partition_end` is a position where some seen letter still has `last > q`, so no earlier cut is legal either: the sweep cuts at the earliest legal point, which maximizes the partition count.

#### Walkthrough

Trace the sweep on Example 1: `s = "xyxxyzbzbbisl"`. The precomputed `last` is `x: 3, y: 4, z: 7, b: 9, i: 10, s: 11, l: 12`. Each row is one position's work; `partition_start` restarts one past every cut:

```text
ch=0  x   partition_end = max(0, 3)  = 3
ch=1  y   partition_end = max(3, 4)  = 4
ch=2  x   partition_end = max(4, 3)  = 4
ch=3  x   partition_end = max(4, 3)  = 4
ch=4  y   partition_end = max(4, 4)  = 4    ch == partition_end -> cut, size 4-0+1 = 5
ch=5  z   partition_end = max(0, 7)  = 7    partition_start = 5
ch=6  b   partition_end = max(7, 9)  = 9
ch=7  z   partition_end = max(9, 7)  = 9
ch=8  b   partition_end = max(9, 9)  = 9
ch=9  b   partition_end = max(9, 9)  = 9    ch == partition_end -> cut, size 9-5+1 = 5
ch=10 i   partition_end = max(0, 10) = 10   ch == partition_end -> cut, size 1
ch=11 s   partition_end = max(0, 11) = 11   ch == partition_end -> cut, size 1
ch=12 l   partition_end = max(0, 12) = 12   ch == partition_end -> cut, size 1
```

The cuts split `"xyxxy"`, `"zbzbb"`, and three singletons, and the recorded sizes are `[5, 5, 1, 1, 1]`, matching the expected Output for Example 1. The second partition shows the bound working: `z` at position 5 pushed `partition_end` to 7, the `b` at position 6 pushed it to 9, and the window grew until `b`'s final occurrence was inside it.

#### Solution

The code is the walkthrough's two phases: fill `last`, then sweep with the cut condition `ch == partition_end`.

```python
from typing import List


class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        last = {}
        for ch, letter in enumerate(s):
            last[letter] = ch

        sizes: List[int] = []
        partition_end = 0
        partition_start = 0
        for ch, letter in enumerate(s):
            partition_end = max(partition_end, last[letter])
            if ch == partition_end:
                sizes.append(ch - partition_start + 1)
                partition_start = ch + 1
        return sizes
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass fills `last` and one pass sweeps; each position does a lookup and a max.

##### Space Complexity: `O(1)`

The map holds at most one entry per lowercase letter, bounded by the alphabet rather than `n`.

#### Key Insights

- Precomputing `last` converts the brute force's repeated searches into lookups, collapsing the growth loop into a single ordered sweep.
- The cut condition `ch == partition_end` is both necessary and sufficient: positions before it still have a letter reaching past, positions at it have none.
- The sweep cuts at the earliest legal boundary everywhere, and earliest cuts are what maximize the number of partitions, so greedy correctness needs no further argument.

### Counting Sweep

#### Derivation

The write-then-cut fold of the last-occurrence map is unfixable as stated: on `"aa"` the write at position 0 makes position 0 look settled, and no amount of ordering discipline inside a single pass can see the `a` still to come. But the information a cut needs has a cheaper online form than positions: counts. Precompute `remaining[letter]`, the number of times each letter still appears; then sweep with `window`, the set of letters currently inside the open partition. A letter enters `window` when seen and leaves exactly when its count hits zero, so `window` empties precisely when every letter seen so far is exhausted, which is the cut condition:

1. Fill `remaining` by counting each letter's occurrences.
2. Sweep with `window = set()` and `size = 0`.
3. Per letter: add it to `window`, decrement `remaining[letter]`, grow
   `size`.
4. When `remaining[letter]` hits 0, discard the letter from `window`.
5. When `window` empties, the partition is complete: record `size`, reset it.

Both passes are online in the sense that matters: the counting pass is a single aggregate scan, and the cut pass never consults a position, only whether any seen letter still owes occurrences.

#### Walkthrough

Trace the counting sweep on Example 1: `s = "xyxxyzbzbbisl"`. The counting pass fills `remaining = x: 3, y: 2, z: 2, b: 3, i: 1, s: 1, l: 1`. Each row is one position of the cut pass, with `size` shown since the last cut:

```text
ch=0   x  window={x}              size=1
ch=1   y  window={x, y}           size=2
ch=2   x  window={x, y}           size=3
ch=3   x  x exhausted (3rd)       window={y}      size=4
ch=4   y  y exhausted (2nd)       window={}       size=5  -> CUT [xyxxy]
ch=5   z  window={z}              size=1
ch=6   b  window={b, z}           size=2
ch=7   z  z exhausted (2nd)       window={b}      size=3
ch=8   b  window={b}              size=4
ch=9   b  b exhausted (3rd)       window={}       size=5  -> CUT [zbzbb]
ch=10  i  i exhausted             window={}       size=1  -> CUT [i]
ch=11  s  s exhausted             window={}       size=1  -> CUT [s]
ch=12  l  l exhausted             window={}       size=1  -> CUT [l]
```

The five cuts split `"xyxxy"`, `"zbzbb"`, and three singletons, and the sizes read `[5, 5, 1, 1, 1]`, matching the expected Output for Example 1. On `"aa"`, the trap that killed the write-then-cut fold: position 0 leaves `window = {a}` (one occurrence still owed), and only position 1 exhausts it, so the string closes as the single partition `[2]`.

#### Solution

The code is the two passes: count, then sweep the window set to exhaustion.

```python
from typing import List


class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        remaining: dict = {}
        for letter in s:
            remaining[letter] = remaining.get(letter, 0) + 1

        sizes: List[int] = []
        window: set = set()
        size = 0
        for letter in s:
            window.add(letter)
            remaining[letter] -= 1
            size += 1
            if remaining[letter] == 0:
                window.discard(letter)
            if not window:
                sizes.append(size)
                size = 0
        return sizes
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One counting pass and one cut pass, constant work per position in each.

##### Space Complexity: `O(1)`

`remaining` and `window` are each bounded by the alphabet.

#### Key Insights

- Counts replace positions as the reach representation: "how many left" is exact the moment it is read, where "where is the last one" is only exact after the whole string is known.
- `window` emptying is the cut condition, and it is self-maintaining: letters enter on first sight, leave on exhaustion, and nothing else ever touches the set.
- This is the streaming version of the problem: if the counts arrive from elsewhere (a known alphabet frequency table, a prior aggregate), the cut pass runs with no lookahead at all, which is the legitimate form of the online sweep the naive fold tried to fake.

## Comparison of Solutions

The practice harness's `practice/partition_labels/reference.py` implements the **Last-Occurrence Sweep** solution.

### Time Complexity

- **Brute Force Window Growth**: `O(n^2)` - each reach is re-searched from the string, and a growing window rescans.
- **Last-Occurrence Sweep**: `O(n)` - one map-fill pass plus one cut pass.
- **Counting Sweep**: `O(n)` - a counting pass plus a window-set cut pass.

### Space Complexity

- **Brute Force Window Growth**: `O(1)` - window bounds and cursors only.
- **Last-Occurrence Sweep**: `O(1)` - a map bounded by the alphabet.
- **Counting Sweep**: `O(1)` - a count map and a window set, both alphabet-bounded.

### Trade-offs

- The brute force states the growth rule in its purest form, which makes it a readable correctness reference, but its rescan loop is quadratic and easy to get subtly wrong.
- The Last-Occurrence Sweep separates "learn the reaches" from "use them", which is the easiest of the linear versions to explain and to prove.
- The Counting Sweep trades position bookkeeping for counters; its counting pass overlaps conceptually with the map-fill pass of the Last-Occurrence Sweep, so the two linear versions cost the same in practice.

### When to Use Each

- **Brute Force Window Growth**: as a derivation of the growth rule and an oracle on short strings.
- **Last-Occurrence Sweep** (recommended): the interview default: two trivially correct passes, one invariant, constant extra space.
- **Counting Sweep**: when the letter frequencies are already known (the genuinely streaming case) or when counts read more naturally than index chasing.

### Optimization Notes

- Both linear sweeps cut at the earliest legal boundary; the partition count maximality is a corollary, never a separate greedy step to argue.
- The naive online fold (write the last position, test the cut in the same visit) fails on `"aa"`: a position can look settled while its letter still owes occurrences. Reach-by-count is the repair.
- The alphabet bound is what makes the maps `O(1)` space: for a general alphabet the map is `O(min(n, |Σ|))`, still linear-shaped but no longer constant.
