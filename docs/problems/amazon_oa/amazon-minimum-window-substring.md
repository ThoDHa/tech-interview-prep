# [Minimum Window Substring](https://www.fastprep.io/problems/amazon-minimum-window-substring)

**Hard** | **NN minutes** | **String, Hash Table, Sliding Window**

Given non-empty strings s and t, return the shortest contiguous substring of s that contains every character of t, including duplicate occurrences.

If no window exists, return the empty string. If several shortest windows exist, return the one with the smallest starting index.

## Examples

### Example 1

**Input:** `s = "ADOBECODEBANC"`, `t = "ABC"`

**Output:** `"BANC"`

**Explanation:** BANC is the shortest window containing A, B, and C.

### Example 2

**Input:** `s = "a"`, `t = "a"`

**Output:** `"a"`

**Explanation:** The whole one-character string is the answer.

### Example 3

**Input:** `s = "a"`, `t = "aa"`

**Output:** `""`

**Explanation:** The source does not contain enough copies of a.

## Constraints

- `1 ≤ s.length, t.length ≤ 100000.`
- `s and t contain printable ASCII characters.`
- `The total input length fits in memory.`

## Solutions

### Brute Force

#### Derivation

The most direct reading enumerates substrings: fix a start, extend an end one character at a time, and stop at the first end where the window holds every character of `t`, duplicates included. That first valid window is the shortest one for its start, so no later end from the same start can improve the answer. Validity is a counting question: build the required multiplicity of `t` into a [dictionary](https://en.wikipedia.org/wiki/Hash_table), walk the window decrementing each matched count, and call the window valid when every required count has reached zero.

The smallest-start tie-break falls out of the scan order. Starts are tried in ascending order and a candidate replaces the recorded best only on a strict length improvement, so among equally short windows the one from the smallest start is found first and kept:

1. Guard: when `len(s) < len(t)`, no window can hold enough copies; return `""`.
2. For each `start` from `0` upward, scan `end`, the inclusive last position,
   from `start + len(t) - 1` to the end of `s`.
3. `covers_target(start, end)` rebuilds `remaining`, the required counts of `t`,
   decrements one count for every matched window character, and reports valid
   when the dictionary empties.
4. On the first valid window from a start, compare `end - start + 1` against
   `min_len`; on a strict improvement record `min_len` and `min_left = start`,
   then stop extending this start.
5. Return `s[min_left:min_left + min_len]`, or `""` when no window was ever
   valid.

#### Walkthrough

Example 1, `s = "ADOBECODEBANC"`, `t = "ABC"`. Each row is one outer iteration: the start character, the first valid window found from that start, and whether it beats the running best. From the row's start, the inner scan checks windows of growing length until `covers_target` first reports valid.

| `start` | `s[start]` | First valid window from `start` | Length | Best window after |
|-----|--------|-----------------------------|--------|--------------------|
| 0 | `A` | `"ADOBEC"` | 6 | `"ADOBEC"` (new minimum) |
| 1 | `D` | `"DOBECODEBA"` | 10 | `"ADOBEC"` |
| 2 | `O` | `"OBECODEBA"` | 9 | `"ADOBEC"` |
| 3 | `B` | `"BECODEBA"` | 8 | `"ADOBEC"` |
| 4 | `E` | `"ECODEBA"` | 7 | `"ADOBEC"` |
| 5 | `C` | `"CODEBA"` | 6 | `"ADOBEC"` |
| 6 | `O` | `"ODEBANC"` | 7 | `"ADOBEC"` |
| 7 | `D` | `"DEBANC"` | 6 | `"ADOBEC"` |
| 8 | `E` | `"EBANC"` | 5 | `"EBANC"` (new minimum) |
| 9 | `B` | `"BANC"` | 4 | `"BANC"` (new minimum) |
| 10 | `A` | none | - | `"BANC"` |
| 11 | `N` | none | - | `"BANC"` |
| 12 | `C` | none | - | `"BANC"` |

Walking the first row concretely: from `start = 0` the inner scan starts at `end = 2` (the window `"ADO"`), which `covers_target` rejects because no `B` or `C` is present, and keeps extending through `end = 5` (the window `"ADOBEC"`), which finally holds `A`, `B`, and `C`. That becomes the first best window and the `break` fires. Starts `10` through `12` have no `B` remaining after them, so no window from those starts is ever valid. The shortest recorded window is `"BANC"` (length 4) from `start = 9`: the expected Output.

#### Solution

The code is the two nested scans of the table, with `covers_target` doing the per-candidate recount.

```python
from typing import Dict


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if len(s) < len(t):
            return ""

        def covers_target(start: int, end: int) -> bool:
            remaining: Dict[str, int] = {}
            for char in t:
                remaining[char] = remaining.get(char, 0) + 1
            for position in range(start, end + 1):
                char = s[position]
                if char in remaining:
                    remaining[char] -= 1
                    if remaining[char] == 0:
                        del remaining[char]
            return not remaining

        min_len = len(s) + 1
        min_left = -1
        for start in range(len(s)):
            for end in range(start + len(t) - 1, len(s)):
                if covers_target(start, end):
                    if end - start + 1 < min_len:
                        min_len = end - start + 1
                        min_left = start
                    break

        if min_left == -1:
            return ""
        return s[min_left:min_left + min_len]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(|s|² × (|s| + |t|))`

There are `O(|s|²)` `(start, end)` candidates before the early break, and each `covers_target` call rebuilds the counts of `t` in `O(|t|)` and scans up to `O(|s|)` window positions.

##### Space Complexity: `O(|t|)`

Only the required-count dictionary lives inside each check; the windows are compared through indices and never materialized as slices.

#### Key Insights

- Draining a count dictionary is the direct translation of "contains every character of `t`, duplicates included": a character is fully supplied exactly when its count reaches zero.
- The first valid window from a given start is the shortest one for that start, which is what licenses the `break`.
- Ascending starts plus a strict `<` comparison together honor the smallest-start tie-break without extra bookkeeping.
- The linear window solutions below exist because this approach repeats the same counting work on almost entirely overlapping windows.

### Sliding Window with Hash Maps

#### Derivation

The brute force discards everything it learns: the window from one start and the window from the next overlap almost entirely, yet each validity check recounts from zero. The repair is to keep one window and update its counts incrementally as the boundaries move, which is the [sliding window](https://usaco.guide/gold/sliding-window) pattern: `right` extends the window until it becomes valid, then `left` contracts it, because once a window is valid only shrinking can shorten it, and every window it passes through on the way is a candidate.

One question remains: how does the loop know the window is valid without rescanning its counts? With a saturation counter. `t_count` holds the required multiplicity of each character of `t` and `required` counts the distinct characters; `formed` counts how many of those characters the window currently holds at full multiplicity. Counts move by one, so `formed` changes only when a count crosses its requirement, and the validity test collapses to the single comparison `formed == required`:

1. Build `t_count` and set `required = len(t_count)`, `formed = 0`, `left = 0`,
   `min_len = len(s) + 1`, `min_left = -1`.
2. Advance `right` over `s`: add `s[right]` to `window_counts`; when the count
   lands exactly on `t_count[char]`, increment `formed`.
3. While `formed == required`, record the window when `right - left + 1 < min_len`
   (remembering `min_left`), then drop `s[left]` from `window_counts`,
   decrement `formed` when its count falls below `t_count[left_char]`, and
   advance `left`.
4. Return `s[min_left:min_left + min_len]`, or `""` when `min_left` was never
   set.

The strict `<` in step 3 is also the tie-break: equal-length windows are measured in order of nondecreasing end position, so the first one measured carries the smallest start, and only a strict improvement replaces it.

#### Invariant

`window_counts` holds the window's multiplicities and `t_count` the required ones; `required = len(t_count)`. Call a character \(c\) of `t` *satisfied* when the window holds at least as many copies as `t` demands. The loop maintains:

$$ \textit{formed} = \bigl|\{\, c \in \textit{t\_count} \ :\ \textit{window\_counts}[c] \ge \textit{t\_count}[c] \,\}\bigr| $$

```text
formed = number of characters c in t_count with window_counts[c] >= t_count[c]
```

Each of the `required` characters is either satisfied or not, so the count saturates exactly on validity:

$$ \textit{formed} = \textit{required} \iff \text{the window contains every character of } t \text{, duplicates included} $$

```text
formed == required
    if and only if  the window contains every character of t, duplicates included
```

The definition uses \(\ge\), not \(=\): surplus copies are permitted and must not change a character's status. That fixes both comparison operators, since counts move by one and `formed` can change only at a crossing. Going up, a character becomes satisfied exactly when its count lands on `t_count[char]`, hence the `==` in the expansion test. Going down, it becomes unsatisfied exactly when the count falls to `t_count[char] - 1`, hence the strict `<` after the decrement. Relaxing that `<` to `!=` breaks the invariant whenever the window carries surplus: with `t = "AB"` and `s = "AAAB"` the window holds three copies of `A` where one is needed; removing one leaves two, `2 != 1` fires, and `formed` drops while `A` is still satisfied, so the shrink loop exits early and reports `"AAAB"`.

The minimum-window update sits inside the shrink loop for the same reason. The `while` condition asserts `formed == required` at the top of the body, so the window is valid *there*, and the drop below is the only step that can invalidate it. Recording on every pass before that drop measures every valid window at this `right`, down to the shortest. At exit `min_left == -1` means no window was ever valid: the empty-string case.

#### Walkthrough

Let us slide the window across Example 1: `s = "ADOBECODEBANC"`, `t = "ABC"`, so `t_count = {A: 1, B: 1, C: 1}` and `required = 3`, with `min_len` starting at `13`. Each line shows `right` advancing by one character; indented lines show the shrink loop firing whenever `formed` reaches `3`:

```text
right=0  'A'   A reaches 1 in window_counts       formed 1
right=1  'D'   not in t_count                     formed 1
right=2  'O'   not in t_count                     formed 1
right=3  'B'   B reaches 1                        formed 2
right=4  'E'   not in t_count                     formed 2
right=5  'C'   C reaches 1                        formed 3 -> valid, shrink
  left=0 'A'   len 6 < 13: min_len=6, min_left=0  ("ADOBEC")
               drop A -> 0 < 1                    formed 2, left=1, stop
right=6  'O'                                      formed 2
right=7  'D'                                      formed 2
right=8  'E'                                      formed 2
right=9  'B'   B reaches 2, surplus               formed 2
right=10 'A'   A reaches 1 again                  formed 3 -> valid, shrink
  left=1 'D'   len 10, no update                  formed 3, left=2
  left=2 'O'   len 9, no update                   formed 3, left=3
  left=3 'B'   len 8, no update; drop B -> 1 >= 1 formed 3, left=4
  left=4 'E'   len 7, no update                   formed 3, left=5
  left=5 'C'   len 6, not < 6; drop C -> 0 < 1    formed 2, left=6, stop
right=11 'N'                                      formed 2
right=12 'C'   C reaches 1                        formed 3 -> valid, shrink
  left=6 'O'   len 7, no update                   formed 3, left=7
  left=7 'D'   len 6, not < 6                     formed 3, left=8
  left=8 'E'   len 5 < 6: min_len=5, min_left=8   ("EBANC"), left=9
  left=9 'B'   len 4 < 5: min_len=4, min_left=9   ("BANC")
               drop B -> 0 < 1                    formed 2, left=10, stop
```

Two details of the invariant show up in the trace. At `right=9` the second `B` enters as surplus: its count moves to `2`, past the requirement rather than onto it, so `formed` stays `2`. And in the shrink at `right=10`, dropping that same surplus `B` (count `2 -> 1`, still `>= 1`) leaves `formed` at `3`, so the window keeps shrinking past it. The loop ends with `min_len = 4` and `min_left = 9`, so the function returns `s[9:13] = "BANC"`, the expected Output.

#### Solution

The code is the expand/contract loop from the trace, with the `formed` crossings guarding both counter updates.

```python
from typing import Dict


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if len(s) < len(t):
            return ""

        t_count: Dict[str, int] = {}
        for char in t:
            t_count[char] = t_count.get(char, 0) + 1
        required = len(t_count)

        window_counts: Dict[str, int] = {}
        formed = 0
        left = 0
        min_len = len(s) + 1
        min_left = -1

        for right in range(len(s)):
            char = s[right]
            window_counts[char] = window_counts.get(char, 0) + 1
            if char in t_count and window_counts[char] == t_count[char]:
                formed += 1

            while formed == required:
                if right - left + 1 < min_len:
                    min_len = right - left + 1
                    min_left = left
                left_char = s[left]
                window_counts[left_char] -= 1
                if (left_char in t_count
                        and window_counts[left_char] < t_count[left_char]):
                    formed -= 1
                left += 1

        if min_left == -1:
            return ""
        return s[min_left:min_left + min_len]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(|s| + |t|)`

Building `t_count` scans `t`; each character of `s` is added to the window once when `right` reaches it and dropped at most once when `left` passes it.

##### Space Complexity: `O(|t| + A)`

`t_count` scales with `t`; `window_counts` holds one entry per distinct character of the window, bounded by the printable ASCII alphabet `A` (at most about 100 characters).

#### Key Insights

- Tracking `formed` versus `required` reduces the validity test to one integer comparison instead of a per-step recount of the window.
- The shrink loop measures every valid window at the current `right`, down to the shortest, before the drop that invalidates it; that placement is where the answer comes from.
- Surplus copies must not disturb `formed`: the expansion test crosses at `==`, the contraction test at `<`.
- The strict `<` on the running minimum is the smallest-start tie-break the page demands, costing no extra state.

### Optimized Sliding Window

#### Derivation

Characters of `s` that never occur in `t` cannot change validity, yet the standard window steps over every one of them (`D`, `O`, `E`, `N` in Example 1). When `|s|` is much larger than `|t|`, most iterations are spent on such filler. The repair filters once, up front: keep only the positions of `s` that hold a character of `t` and slide the same window over that shorter list. The original positions must ride along, because the reported window still spans the full string, filler included. Every minimal window both starts and ends on a character of `t` (otherwise it could be trimmed), so measuring only between filtered endpoints loses nothing:

1. Build `t_count`, `required`, and `filtered`, the `(position, char)` pairs of
   `s` whose character occurs in `t_count`.
2. Run the same expand/contract loop over `filtered`, maintaining
   `window_counts` and `formed`; here every character inside the window is
   relevant, so the crossing tests read `window_counts[char] == t_count[char]`
   and `< t_count[char]` directly.
3. Measure through the stored positions: `start = filtered[left][0]`,
   `end = filtered[right][0]`, candidate length `end - start + 1`.
4. Return `s[min_left:min_left + min_len]`, or `""` when no window was valid.

#### Walkthrough

Example 1 again. Only six of the thirteen positions survive the filter:

```text
filtered = [(0,'A'), (3,'B'), (5,'C'), (9,'B'), (10,'A'), (12,'C')]
```

The loop runs the same `formed` machinery over those six entries, with `min_len` starting at `13`:

```text
right=0  (0,'A')   A reaches 1                      formed 1
right=1  (3,'B')   B reaches 1                      formed 2
right=2  (5,'C')   C reaches 1                      formed 3 -> valid, shrink
  left=0 (0,'A')   start=0, end=5, len 6 < 13:      min_len=6, min_left=0 ("ADOBEC")
                   drop A -> 0 < 1                  formed 2, left=1, stop
right=3  (9,'B')   B reaches 2, surplus             formed 2
right=4  (10,'A')  A reaches 1 again                formed 3 -> valid, shrink
  left=1 (3,'B')   start=3, end=10, len 8, no update
                   drop B -> 1, still >= 1          formed 3, left=2
  left=2 (5,'C')   start=5, end=10, len 6, not < 6
                   drop C -> 0 < 1                  formed 2, left=3, stop
right=5  (12,'C')  C reaches 1                      formed 3 -> valid, shrink
  left=3 (9,'B')   start=9, end=12, len 4 < 5:      min_len=4, min_left=9 ("BANC")
                   drop B -> 0 < 1                  formed 2, left=4, stop
```

Six expansion steps replace thirteen; the filler characters never enter the loop. The window measured at `left=3` spans three filtered entries but has length `12 - 9 + 1 = 4` in `s`, because the stored positions measure the true span. The final answer is `s[9:13] = "BANC"`, the expected Output, identical to the unfiltered version.

#### Solution

The code is the filtered trace written down: the same window machinery, indexed through `filtered`.

```python
from typing import Dict, List, Tuple


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        t_count: Dict[str, int] = {}
        for char in t:
            t_count[char] = t_count.get(char, 0) + 1
        required = len(t_count)

        filtered: List[Tuple[int, str]] = []
        for position, char in enumerate(s):
            if char in t_count:
                filtered.append((position, char))

        window_counts: Dict[str, int] = {}
        formed = 0
        left = 0
        min_len = len(s) + 1
        min_left = -1

        for right in range(len(filtered)):
            char = filtered[right][1]
            window_counts[char] = window_counts.get(char, 0) + 1
            if window_counts[char] == t_count[char]:
                formed += 1

            while formed == required:
                start = filtered[left][0]
                end = filtered[right][0]
                if end - start + 1 < min_len:
                    min_len = end - start + 1
                    min_left = start
                left_char = filtered[left][1]
                window_counts[left_char] -= 1
                if window_counts[left_char] < t_count[left_char]:
                    formed -= 1
                left += 1

        if min_left == -1:
            return ""
        return s[min_left:min_left + min_len]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(|s| + |t|)`

Building `filtered` scans `s`, and the window loop touches each filtered entry at most twice. The asymptotic bound is unchanged; the constant improves when most of `s` is filler.

##### Space Complexity: `O(|s| + |t|)`

`filtered` holds up to one pair per position of `s`, on top of the two count dictionaries.

#### Key Insights

- Pre-filtering spends iterations only on positions that can change the window's validity.
- The original positions ride along with each filtered character, so lengths are measured in `s` rather than in the compressed list.
- Minimal windows start and end on characters of `t`, which is why measuring between filtered endpoints never misses a candidate.
- The gain is constant-factor only, and it materializes when `|s| >> |t|` with `t` covering a small slice of the alphabet.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(|s|² × (|s| + |t|))` - each of the `O(|s|²)` candidates pays an `O(|s|)` window scan plus an `O(|t|)` target recount.
- **Sliding Window with Hash Maps**: `O(|s| + |t|)` - every character enters and leaves the window at most once.
- **Optimized Sliding Window**: `O(|s| + |t|)` - same bound, fewer iterations when `s` is mostly filler.

### Space Complexity

- **Brute Force**: `O(|t|)` - only the required-count dictionary.
- **Sliding Window with Hash Maps**: `O(|t| + A)` - both dictionaries, with the window counts capped by the printable ASCII alphabet.
- **Optimized Sliding Window**: `O(|s| + |t|)` - the filtered position list dominates in the worst case.

### Trade-offs

- **Brute Force**: needs no auxiliary insight and almost no state, but it repeats the same counting work on overlapping windows and is unusable at the constraint ceiling.
- **Sliding Window with Hash Maps**: linear time with a two-pointer loop whose only subtlety is the `formed` counter; the least code that meets the bound.
- **Optimized Sliding Window**: same asymptotics and slightly more machinery; pays off only when `|s|` dwarfs the characters `t` actually needs.

### When to Use Each

- **Brute Force**: tiny inputs, or as the correctness oracle when testing the faster versions.
- **Sliding Window with Hash Maps (Recommended)**: the interview and online-assessment default: it meets the linear bound with the least subtlety.
- **Optimized Sliding Window**: when `|s| >> |t|` and `t` covers a small slice of the alphabet, so the filter removes most of the string.

### Optimization Notes

- **Sliding Window with Hash Maps** is the recommended choice: the `formed`-versus-`required` counter is the one mechanism to present clearly in an interview.
- The smallest-start tie-break needs no extra state in either window solution: measuring inside the shrink loop with a strict `<` keeps the earliest start among equally short windows.
- The classic pitfall is surplus copies: a character's count can pass its requirement and later fall back toward it, so the expansion test is `==` while the contraction test is `<`. Relaxing `<` to `!=` returns `"AAAB"` for `s = "AAAB"`, `t = "AB"`.
- Frequencies, not presence, are what "including duplicate occurrences" demands: `s = "a"`, `t = "aa"` has no valid window even though `a` occurs in `s`.
