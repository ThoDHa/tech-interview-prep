# [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/)

**Medium** | **25 minutes** | **Hash Table, String, Sliding Window**

**Pattern:** [Sliding Window](../patterns/sliding_window/intuition.md)

**Algorithm:** [Sliding window](https://usaco.guide/gold/sliding-window) · [Hash table](https://en.wikipedia.org/wiki/Hash_table)

**Practice:** [`practice/longest_repeating_character_replacement/solution.py`](../../practice/longest_repeating_character_replacement/solution.py)

You are given a string `s` consisting of only uppercase english characters and an integer `k`. You can choose up to `k` characters of the string and replace them with any other uppercase English character.

After performing at most `k` replacements, return the length of the longest substring which contains only one distinct character.

## Examples

### Example 1

**Input:** `s = "XYYX", k = 2`

**Output:** `4`

**Explanation:** Either replace the 'X's with 'Y's, or replace the 'Y's with 'X's.

### Example 2

**Input:** `s = "AAABABB", k = 1`

**Output:** `5`

## Constraints

- `1 <= s.length <= 100,000`
- `0 <= k <= s.length`
- `s` consists of only uppercase english characters.

## Deriving the Solution

"Change up to `k` letters to make one letter dominate" has a counting restatement that unlocks everything: a substring can be made uniform exactly when its *minority* letters (everything that is not the most frequent character in it) number at most `k`. Every solution below is a way of asking, over all substrings, which one satisfies that budget.

1. **Start literal.** Examine every substring, count its letters, and test the budget. The substrings number `O(n²)`, so this is hopeless at the stated bounds: see [Brute Force over Substrings](#brute-force-over-substrings).
2. **Spot the structure.** The budget is *monotone*: shrinking a valid substring keeps it valid, and growing an invalid one keeps it invalid. Monotone validity over a linear order of windows is the signature of the [sliding window](https://en.wikipedia.org/wiki/Sliding_window_protocol) technique.
3. **Slide instead of enumerate.** Grow the right edge greedily; when the budget breaks, advance the left edge just enough to restore it. The window never shrinks, and the answer is the largest window ever reached: see [Sliding Window with Max Frequency](#sliding-window-with-max-frequency).

## Solutions

### Brute Force over Substrings

#### Derivation

The most literal reading enumerates the candidates: every `(start, end)` pair defines a substring, and the replacement budget question is answered by counting that substring's letters. The letter whose count is highest is kept; every other letter must be replaced, so the substring is achievable exactly when `length - highest_count <= k`:

1. Iterate `start` over every index, then `end` from `start` onward.
2. Maintain `counts` for the current substring incrementally as `end` advances.
3. Track `max_count`, the largest letter count inside it.
4. If `end - start + 1 - max_count <= k`, the substring is achievable; record its length.
5. Return the longest length seen.

#### Walkthrough

Trace the enumeration on Example 1: `s = "XYYX"`, `k = 2`. Only the interesting windows are shown, with their counts and budget check:

```text
"X"        counts {X:1}          max 1   1 - 1 = 0 <= 2  valid, length 1
"XYY"      counts {X:1, Y:2}     max 2   3 - 2 = 1 <= 2  valid, length 3
"XYYX"     counts {X:2, Y:2}     max 2   4 - 2 = 2 <= 2  valid, length 4
```

The full string passes its budget check: either letter can be the kept one and two replacements cover the other. The longest valid length is `4`, matching Example 1's expected Output.

#### Solution

The code is the double loop with the incremental count update and the budget test.

```python
from collections import Counter


class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        longest = 0
        for start in range(len(s)):
            counts = Counter()
            for end in range(start, len(s)):
                counts[s[end]] += 1
                max_count = max(counts.values())
                if (end - start + 1) - max_count > k:
                    break
                longest = max(longest, end - start + 1)
        return longest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

The two loops visit `O(n²)` windows, and each step's `max(counts.values())` scans up to 26 letters, a constant factor. The early `break` trims windows that already violate the budget but the worst case stays quadratic.

##### Space Complexity: `O(1)`

`counts` holds at most 26 uppercase letters.

#### Key Insights

- States the budget condition exactly: `window length - max letter count` is the number of replacements needed, and that is all the problem is.
- Correct and clear, but `O(n²)` against a `100,000`-length input cannot run in time.
- The early break is the first hint of monotonicity: once a budget breaks, growing the window never repairs it.

### Sliding Window with Max Frequency

#### Derivation

The enumeration redoes the budget test for windows that are extensions of windows already tested. Monotonicity removes that redundancy: if a window is invalid, every strictly larger window containing it is invalid too, so a valid window can be grown greedily and only ever trimmed minimally. Sweep the right edge forward one letter at a time; after each addition, if the budget broke, advance the left edge until the window is valid again:

1. Keep `counts` for the current window and `max_frequency`, the largest count ever seen in any window state.
2. For each `right`, add `s[right]` to `counts` and raise `max_frequency` if this letter's count now exceeds it.
3. The window is valid while `(right - left + 1) - max_frequency <= k`.
4. When invalid, decrement `counts[s[left]]` and advance `left`, then re-test.
5. Record `right - left + 1` as a candidate for `longest`.

Two details make this both correct and linear. First, `max_frequency` is never decremented when letters leave the window: a smaller true maximum can only produce a *smaller* answer, and since the answer only improves when a strictly larger frequency arrives, the stale value is harmless. Second, the left edge never moves backward, so both edges sweep the string once.

#### Walkthrough

Trace the window on Example 2: `s = "AAABABB"`, `k = 1`:

```text
right=0 'A'  window "A"        counts {A:1}  max_freq 1   1-1=0  <= 1  longest 1
right=1 'A'  window "AA"       counts {A:2}  max_freq 2   2-2=0  <= 1  longest 2
right=2 'A'  window "AAA"      counts {A:3}  max_freq 3   3-3=0  <= 1  longest 3
right=3 'B'  window "AAAB"     counts {A:3,B:1}  4-3=1    <= 1  longest 4
right=4 'A'  window "AAABA"    counts {A:4,B:1}  5-4=1    <= 1  longest 5
right=5 'B'  window "AAABAB"   6-4=2 > 1 -> shrink once (drop leading 'A')
             window "AABAB"    5-4=1    <= 1             longest 5
right=6 'B'  window "AABABB"   6-4=2 > 1 -> shrink once (drop leading 'A')
             window "ABABB"    5-4=1    <= 1             longest 5
```

The largest valid window ever held spans 5 letters, `"AAABA"`, which one replacement (the lone `B`) turns into `"AAAAA"`. That matches Example 2's expected Output. Note both details of the stale-max design in the last two rows: `max_frequency` stays `4` even as `'A'`s leave the window, so each oversized window needs a single shrink, and the window ends smaller than 5 anyway because the answer is the maximum ever reached, not the final state. Example 1, `"XYYX"` with `k = 2`, never trims at all (`4 - 2 = 2 <= k`) and reports the full length `4`.

#### Solution

The code is the walkthrough's grow-and-trim loop with the never-decreasing `max_frequency`.

```python
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        counts = {}
        left = 0
        max_frequency = 0
        longest = 0
        for right, char in enumerate(s):
            counts[char] = counts.get(char, 0) + 1
            max_frequency = max(max_frequency, counts[char])
            while (right - left + 1) - max_frequency > k:
                counts[s[left]] -= 1
                left += 1
            longest = max(longest, right - left + 1)
        return longest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Both edges only move forward: `right` advances `n` times and `left` advances at most `n` times in total, so the work is `O(n)` despite the nested `while`.

##### Space Complexity: `O(1)`

`counts` holds at most 26 uppercase letters regardless of input length.

#### Key Insights

- The whole problem reduces to one inequality: `window length - max_frequency <= k`.
- `max_frequency` deliberately lags (it never decreases): the answer needs only the best frequency seen, and recomputing the true per-window max would cost `O(26)` per step for no gain in the final answer.
- The sliding window applies because validity is monotone in the window bounds; recognizing that property is the transferable skill.

## Comparison of Solutions

### Time Complexity

- **Brute Force over Substrings**: `O(n²)` - every substring is budget-tested (with early breaks).
- **Sliding Window with Max Frequency**: `O(n)` - each index enters and leaves the window at most once.

### Space Complexity

- **Brute Force over Substrings**: `O(1)` - one 26-letter counter per starting index.
- **Sliding Window with Max Frequency**: `O(1)` - one 26-letter counter plus scalar trackers.

### Trade-offs

- **Brute Force over Substrings** derives directly from the statement and needs no monotonicity argument, but cannot handle the stated input bound.
- **Sliding Window with Max Frequency** is linear and barely more code; its subtlety is concentrated in the stale `max_frequency`, which must be reasoned about once and then trusted.

### When to Use Each

- **Brute Force over Substrings**: interviews that ask for a correct baseline first, or inputs of trivial length.
- **Sliding Window with Max Frequency**: the answer to the problem as stated (recommended here).

### Optimization Notes

- Replacing `max_frequency = max(max_frequency, counts[char])` with a true recomputation `max(counts.values())` also passes and is easier to trust, at an `O(26)` per-step constant; the amortized-linear claim is what the stale version buys.
- Decrementing `max_frequency` on shrink is a correctness trap: it can make `longest` miss the true maximum window, because the answer window may have been seen earlier with a larger frequency.
- The same budget inequality solves the related "longest window with at most k distinct" family; only the validity condition changes.
