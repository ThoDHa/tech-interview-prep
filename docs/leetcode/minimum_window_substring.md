# [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/)

**Hard** | **45 minutes** | **Hash Table, String, Sliding Window**

**Pattern:** [Sliding Window](../patterns/sliding_window/intuition.md)

**Algorithm:** [Sliding window](https://usaco.guide/gold/sliding-window) · [Two-pointer technique](https://usaco.guide/silver/two-pointers) · [Hash table](https://en.wikipedia.org/wiki/Hash_table)

**Practice:** [`practice/minimum_window_substring/solution.py`](../../practice/minimum_window_substring/solution.py)

Given two strings s and t of lengths m and n respectively, return the **minimum window substring** of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "".

The testcases will be generated such that the answer is **unique**.

## Examples

### Example 1

**Input:** `s = "ADOBECODEBANC"`, `t = "ABC"`

**Output:** `"BANC"`

**Explanation:** The minimum window substring `"BANC"` includes 'A', 'B', and 'C' from string t.

### Example 2

**Input:** `s = "a"`, `t = "a"`

**Output:** `"a"`

**Explanation:** The entire string s is the minimum window.

### Example 3

**Input:** `s = "a"`, `t = "aa"`

**Output:** `""`

**Explanation:** Both 'a's from t must be included in the window. Since the largest window of s only has one 'a', return empty string.

## Constraints

- `m == s.length`
- `n == t.length`
- `1 <= m, n <= 10^5`
- `s` and `t` consist of uppercase and lowercase English letters.

## Follow-up

Could you find an algorithm that runs in `O(m + n)` time?

## Deriving the Solution

A window of `s` is valid when it holds every character of `t`, duplicates included, which is a comparison between two frequency counts: what the window contains versus what `t` demands. Every solution below is a strategy for checking as few windows as cheaply as possible against that count.

1. **Start literal.** Enumerate every substring and validate each one by
   counting from scratch. Correct, but there are `O(|s|^2)` substrings and each check rescans its window, `O(|s|^3 + |s|^2 × |t|)` in total: see [Brute Force](#brute-force).
2. **Spot the waste.** Adjacent windows differ by a single character, yet every
   validity check recounts the whole window. And the candidates are not independent: once a window is valid, growing it further can never make it shorter, while shrinking it from the left is the only move that can.
3. **Slide instead of enumerate.** Keep one window between two pointers and
   update its counts incrementally: extend `right` until the window turns valid, then shrink from `left` while it stays valid, recording the minimum. A `formed`-versus-`required` counter makes each validity test `O(1)`, and each character enters and leaves the window once, giving the follow-up's `O(|s| + |t|)`: see [Sliding Window with Hash Maps](#sliding-window-with-hash-maps).
4. **Skip the irrelevant.** Characters that never occur in `t` cannot change
   validity, so pre-filter `s` down to the positions that hold `t`'s characters and slide over that shorter list, keeping original indices for measuring. Same bound, better constants when `|s| >> |t|`: see [Optimized Sliding Window](#optimized-sliding-window).

## Solutions

### Brute Force

#### Derivation

The most direct reading of the problem is to enumerate every substring and keep the shortest one that contains all of `t`. Validity is checked from scratch by counting `t`'s characters into a [dictionary](https://en.wikipedia.org/wiki/Hash_table) and decrementing as the window is scanned.

1. Build a frequency dictionary of `t` by hand inside `is_valid_window`, then scan the candidate substring decrementing each matched count until the dictionary empties.
2. For each start index `i`, extend the end `j` from the smallest feasible length upward, testing each substring for validity.
3. Stop extending a given start the moment a valid window is found, since any longer window from that same start cannot be smaller.
4. Track the shortest valid window seen across all starts and return it.

#### Walkthrough

Let us watch the Brute Force run on Example 1: `s = "ADOBECODEBANC"`, `t = "ABC"`. The outer loop fixes a start index `i`, and the inner loop grows the end `j` until `s[i:j]` first contains an `A`, a `B`, and a `C`. The moment a start produces a valid window, the `break` stops extending it (a longer window from the same start cannot be shorter). We keep `min_window`, the shortest valid window seen so far.

Each row below is one outer iteration: the start character, the first valid window found from that start, and whether it beats the running minimum.

| `i` | `s[i]` | First valid window from `i` | Length | `min_window` after |
|-----|--------|-----------------------------|--------|--------------------|
| 0 | `A` | `"ADOBEC"` | 6 | `"ADOBEC"` (new min) |
| 1 | `D` | `"DOBECODEBA"` | 10 | `"ADOBEC"` |
| 2 | `O` | `"OBECODEBA"` | 9 | `"ADOBEC"` |
| 3 | `B` | `"BECODEBA"` | 8 | `"ADOBEC"` |
| 4 | `E` | `"ECODEBA"` | 7 | `"ADOBEC"` |
| 5 | `C` | `"CODEBA"` | 6 | `"ADOBEC"` |
| 6 | `O` | `"ODEBANC"` | 7 | `"ADOBEC"` |
| 7 | `D` | `"DEBANC"` | 6 | `"ADOBEC"` |
| 8 | `E` | `"EBANC"` | 5 | `"EBANC"` (new min) |
| 9 | `B` | `"BANC"` | 4 | `"BANC"` (new min) |
| 10 | `A` | none | : | `"BANC"` |
| 11 | `N` | none | : | `"BANC"` |
| 12 | `C` | none | : | `"BANC"` |

Walking the first row concretely: at `i = 0` the inner loop starts at length 3 (`"ADO"`), which `is_valid_window` rejects since it has no `B` or `C`. It keeps extending: `"ADOB"`, `"ADOBE"`, then `"ADOBEC"`, which finally holds all of `A`, `B`, `C`. That becomes the first `min_window`, and the `break` fires.

From `i = 10` onward only `"...ANC"` remains, which can never supply a `B`, so no start past index 9 yields a valid window. The shortest window recorded across all starts is `"BANC"` (length 4), found at `i = 9`.

The function returns `min_window`, which is `"BANC"`: this matches the expected Output `"BANC"`.

#### Solution

The code is the two nested loops from the table, with `is_valid_window` doing the per-candidate recount.

```python
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """
        Brute force approach: check all possible substrings
        """
        if not s or not t or len(s) < len(t):
            return ""

        def is_valid_window(window_str: str, target: str) -> bool:
            """Check if window contains all characters from target"""
            t_count = {}
            for char in target:
                t_count[char] = t_count.get(char, 0) + 1

            for char in window_str:
                if char in t_count:
                    t_count[char] -= 1
                    if t_count[char] == 0:
                        del t_count[char]

            return len(t_count) == 0

        min_window = ""
        min_len = float('inf')

        # Check all possible substrings
        for i in range(len(s)):
            for j in range(i + len(t), len(s) + 1):
                window = s[i:j]
                if is_valid_window(window, t):
                    if len(window) < min_len:
                        min_len = len(window)
                        min_window = window
                    break  # Found valid window starting at i, no need to extend

        return min_window
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(|s|³ + |s|² × |t|)`

There are O(|s|²) candidate substrings, and each `is_valid_window` call rebuilds the count of `t` (O(|t|)) and then scans the whole window, which can be up to O(|s|) characters long. The per-check cost is therefore O(|s| + |t|), giving O(|s|³ + |s|² × |t|) overall.

##### Space Complexity: `O(|t|)`

Space for character counting in validation function.

#### Key Insights

- Enumerating every substring is the most direct reading of the problem and needs no auxiliary insight, which makes it a useful baseline.
- The early `break` after the first valid window from a given start prunes longer windows that share that start, but the quadratic substring count still dominates.
- It is correct for all inputs yet impractical once `|s|` grows, so it serves comparison and intuition rather than production use.

### Sliding Window with Hash Maps

#### Derivation

The Brute Force throws away everything it learns: the window starting at `i` and the window starting at `i + 1` overlap almost entirely, yet each validity check recounts from zero. The repair is to keep a single window and update its counts incrementally as the boundaries move, which is the **[sliding window technique](https://usaco.guide/gold/sliding-window)** with two pointers. `right` expands the window until it becomes valid; `left` then contracts it, because once valid, only shrinking can improve it, and each shrink step measures a candidate.

One question remains: how do we know the window is valid without rescanning its counts? Track it with a saturation counter. `t_count` holds `t`'s required frequencies and `required` its number of distinct characters; `formed` counts how many of those characters the window currently satisfies at full multiplicity. `formed` only changes when a count crosses its requirement, so the validity test is a single integer comparison:

1. Count `t` into `t_count` and set `required = len(t_count)`, `formed = 0`,
   `left = right = 0`, with empty `window_counts`.
2. Expand: add `s[right]` to `window_counts`; when that character's count
   reaches exactly `t_count[char]`, increment `formed`.
3. While `formed == required`, the window is valid: record it if
   `right - left + 1` beats `min_len` (remembering `min_left`), then remove `s[left]` from `window_counts`, decrement `formed` when that character's count falls below `t_count[char]`, and advance `left`.
4. Advance `right` and repeat; at the end return `s[min_left:min_left + min_len]`,
   or `""` when `min_len` was never set.

The Invariant below pins down exactly what `formed` counts, why the expansion test uses `==` while the contraction test uses `<`, and why the minimum-window update must sit inside the shrink loop.

#### Invariant

`t_count` holds the required multiplicity of each character of `t`, and `required = len(t_count)`. Call a character \(c\) of `t` *satisfied* when the window holds at least as many copies as `t` demands. The loop maintains:

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

The definition uses \(\ge\), not \(=\): surplus copies are permitted and must not change a character's status. That fixes both comparison operators, since counts move by one and `formed` can change only at a crossing. Going up, a character becomes satisfied exactly when its count lands on `t_count[char]`, hence the `==` in the expansion test. Going down, it becomes unsatisfied exactly when the count falls to `t_count[char] - 1`, hence the strict `<` after the decrement.

Relaxing that `<` to `!=` breaks the invariant whenever the window carries surplus. With `t = "AB"` and `s = "AAAB"` the window holds three copies of `A` where one is needed; removing one leaves two, `2 != 1` fires, and `formed` drops while `A` is still satisfied, so the shrink loop exits and reports `"AAAB"`.

The minimum-window update sits inside the shrink loop for the same reason. The `while` condition asserts `formed == required` at the top of the body, so the window is valid *there*, and the decrement below is the only step that can invalidate it. Updating on every pass before that decrement therefore measures every valid window at this `right`, down to the shortest. Hoisted above the loop it would run unconditionally and measure windows before they are known valid at all; hoisted below, `left` has already passed validity.

At exit `min_len` is the shortest valid width over all `right`, and `min_len == inf` means no window was ever valid: the empty-string case.

#### Walkthrough

Let us slide the window across Example 1: `s = "ADOBECODEBANC"`, `t = "ABC"`, so `t_count = {A: 1, B: 1, C: 1}` and `required = 3`. Each line shows `right` advancing by one character; indented lines show the shrink loop firing whenever `formed` reaches `3`:

```text
right=0  'A'   A reaches 1 in window_counts       formed 1
right=1  'D'   not in t_count                     formed 1
right=2  'O'   not in t_count                     formed 1
right=3  'B'   B reaches 1                        formed 2
right=4  'E'   not in t_count                     formed 2
right=5  'C'   C reaches 1                        formed 3 -> valid, shrink
  left=0 'A'   len 6 < inf: min_len=6, min_left=0 ("ADOBEC")
               drop A -> 0 < 1                    formed 2, left=1, stop
right=6  'O'                                      formed 2
right=7  'D'                                      formed 2
right=8  'E'                                      formed 2
right=9  'B'   B reaches 2, surplus (2 != 1)      formed 2
right=10 'A'   A reaches 1 again                  formed 3 -> valid, shrink
  left=1 'D'   len 10, no update; D not in t      formed 3, left=2
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
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """
        Two-pointer sliding window approach with frequency tracking
        """
        if not s or not t or len(s) < len(t):
            return ""

        # Count characters in t
        t_count = {}
        for char in t:
            t_count[char] = t_count.get(char, 0) + 1

        required = len(t_count)  # Number of unique characters in t
        formed = 0  # Number of unique characters matched with desired frequency

        # Sliding window
        left = right = 0
        window_counts = {}

        # Result: (window length, left, right)
        min_len = float('inf')
        min_left = 0

        while right < len(s):
            # Expand window by including character at right
            char = s[right]
            window_counts[char] = window_counts.get(char, 0) + 1

            # Check if frequency of current character matches desired count in t
            if char in t_count and window_counts[char] == t_count[char]:
                formed += 1

            # Contract window until it ceases to be 'desirable'
            while left <= right and formed == required:
                char = s[left]

                # Update minimum window if current is smaller
                if right - left + 1 < min_len:
                    min_len = right - left + 1
                    min_left = left

                # Remove character at left from window
                window_counts[char] -= 1
                if char in t_count and window_counts[char] < t_count[char]:
                    formed -= 1

                left += 1

            right += 1

        return "" if min_len == float('inf') else s[min_left:min_left + min_len]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(|s| + |t|)`

Each character in s is visited at most twice (once by right pointer, once by left pointer). Building t_count takes O(|t|) time.

##### Space Complexity: `O(|s| + |t|)`

In the worst case, window_counts could contain all characters from s, and t_count contains all characters from t.

#### Key Insights

- Tracking `formed` versus `required` (unique characters matched at their exact frequency) reduces the validity check to `O(1)` instead of rescanning counts each step.
- The window only contracts while it remains valid, so the moment `formed` drops below `required` the left pointer stops, capturing the smallest window precisely.
- Counting frequencies rather than mere presence is what makes duplicate characters in `t` handled correctly.

### Optimized Sliding Window

#### Derivation

In the standard sliding window, every character of `s` passes through the loop, including characters like `D`, `O`, `E`, and `N` that never occur in `t` and can never change the window's validity. When `|s|` is much larger than `|t|` and `t` has few unique characters, most iterations are spent stepping over such filler. The repair is to filter it out once, up front: keep only the positions of `s` that hold a character of `t`, and slide the same window over that shorter list. The original indices must ride along, because the reported window still spans the full string, filler included.

1. Count `t` into `dict_t` and set `required = len(dict_t)`.
2. Build `filtered_s`, the list of `(i, char)` pairs for every position `i` of
   `s` whose character occurs in `dict_t`.
3. Run the same expand/contract loop over `filtered_s`, maintaining
   `window_counts` and `formed` exactly as before.
4. When measuring a valid window, read the true boundaries from the stored
   indices: `start = filtered_s[left][0]` and `end = filtered_s[right][0]`, and compare `end - start + 1` against `min_len`.
5. Return `s[min_left:min_left + min_len]`, or `""` when no valid window was
   found.

#### Walkthrough

Let us rerun Example 1 (`s = "ADOBECODEBANC"`, `t = "ABC"`) over the filtered list. Only six of the thirteen positions survive the filter:

```text
filtered_s = [(0,'A'), (3,'B'), (5,'C'), (9,'B'), (10,'A'), (12,'C')]

right=0  (0,'A')   A reaches 1                    formed 1
right=1  (3,'B')   B reaches 1                    formed 2
right=2  (5,'C')   C reaches 1                    formed 3 -> valid, shrink
  left=0 (0,'A')   start=0, end=5, len 6 < inf:   min_len=6, min_left=0 ("ADOBEC")
                   drop A -> 0 < 1                formed 2, left=1, stop
right=3  (9,'B')   B reaches 2, surplus           formed 2
right=4  (10,'A')  A reaches 1 again              formed 3 -> valid, shrink
  left=1 (3,'B')   start=3, end=10, len 8, no update
                   drop B -> 1 >= 1               formed 3, left=2
  left=2 (5,'C')   start=5, end=10, len 6, not < 6
                   drop C -> 0 < 1                formed 2, left=3, stop
right=5  (12,'C')  C reaches 1                    formed 3 -> valid, shrink
  left=3 (9,'B')   start=9, end=12, len 4 < 6:    min_len=4, min_left=9 ("BANC")
                   drop B -> 0 < 1                formed 2, left=4, stop
```

The loop runs six expansion steps instead of thirteen; the filler characters never enter it. The window lengths are still measured in the original string through the stored indices, which is why the window at `left=3, right=5` has length `12 - 9 + 1 = 4` even though it spans only three filtered entries. The final answer is `s[9:13] = "BANC"`, the expected Output, identical to the unfiltered version.

#### Solution

The code is the filtered trace written down: the same window machinery, indexed through `filtered_s`.

```python
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """
        Optimized sliding window that only considers relevant characters
        """
        if not s or not t:
            return ""

        # Count characters in t
        dict_t = {}
        for char in t:
            dict_t[char] = dict_t.get(char, 0) + 1

        required = len(dict_t)

        # Filter s to only include characters present in t
        # This optimization helps when |s| >> |t|
        filtered_s = []
        for i, char in enumerate(s):
            if char in dict_t:
                filtered_s.append((i, char))

        left = right = 0
        formed = 0
        window_counts = {}

        min_len = float('inf')
        min_left = 0

        while right < len(filtered_s):
            # Expand window
            char = filtered_s[right][1]
            window_counts[char] = window_counts.get(char, 0) + 1

            if window_counts[char] == dict_t[char]:
                formed += 1

            # Contract window
            while left <= right and formed == required:
                char = filtered_s[left][1]

                # Calculate actual window size in original string
                start = filtered_s[left][0]
                end = filtered_s[right][0]

                if end - start + 1 < min_len:
                    min_len = end - start + 1
                    min_left = start

                window_counts[char] -= 1
                if window_counts[char] < dict_t[char]:
                    formed -= 1

                left += 1

            right += 1

        return "" if min_len == float('inf') else s[min_left:min_left + min_len]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(|s| + |t|)`

Same asymptotic complexity, but with better practical performance when |s| >> |t|.

##### Space Complexity: `O(|s| + |t|)`

Additional space for filtered_s in worst case, but typically much smaller.

#### Key Insights

- Pre-filtering skips characters irrelevant to `t`, so iterations are spent only on positions that can change the window's validity.
- The original indices are carried alongside each filtered character so the true window length in `s` is measured even though we iterate over the compressed list.
- The asymptotic bound is unchanged; the gain is purely in constant factors and only materializes when `|s| >> |t|` and `t` has few unique characters.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(|s|³ + |s|² × |t|)` - Each of the O(|s|²) substrings pays an O(|s| + |t|) validity scan, unacceptable for large inputs
- **Sliding Window with Hash Maps**: `O(|s| + |t|)` - Optimal linear time
- **Optimized Sliding Window**: `O(|s| + |t|)` - Same complexity, better constants

### Space Complexity

- **Brute Force**: `O(|t|)` - Only target character counting
- **Sliding Window with Hash Maps**: `O(|s| + |t|)` - Hash maps for character counting
- **Optimized Sliding Window**: `O(|s| + |t|)` - Additional filtered array

### Trade-offs

- **Brute Force**: Implementation complexity is low and space usage is minimal, with excellent code clarity. However, performance is poor, making it practically applicable for learning only.
- **Sliding Window with Hash Maps**: Implementation complexity is medium with reasonable space usage and good code clarity. Performance is excellent, making it the best general solution for practical use.
- **Optimized Sliding Window**: Implementation complexity is high with higher space usage and medium code clarity. Performance is better than the standard sliding window for sparse t, making it the best choice for those specific cases.

### When to Use Each

- **Brute Force**: Only for understanding the problem or when constraints are very small
- **Sliding Window with Hash Maps**: Best general-purpose solution for production code and interviews
- **Optimized Sliding Window**: When t has very few unique characters compared to s

### Optimization Notes

- The **Sliding Window with Hash Maps** solution is the recommended choice: it achieves the follow-up's requested `O(m + n)` time complexity using the classic expand/contract pattern with two pointers, balancing simplicity and efficiency for production code and interviews.
- Key implementation detail: track `formed` versus `required` (the count of unique characters matched at their desired frequency) so the window only contracts while it remains valid, allowing the minimum to be captured precisely.
- The **Optimized Sliding Window** pre-filters s to only relevant characters, which delivers real benefits only when `|s| >> |t|` and t has few unique characters. Otherwise the extra filtered array adds overhead without asymptotic improvement.
- Common pitfall: mishandling corner cases such as empty strings, impossible cases where t is longer than s, and duplicate characters in t. Frequency counts (not mere presence) must be tracked to handle duplicates correctly.
