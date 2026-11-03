# [Find Word-Multiset Windows](https://www.fastprep.io/problems/amazon-word-multiset-window-search)

**Medium** | **NN minutes** | **Array, String, Hash Table, Sliding Window**

You are given a tokenized text textWords and a nonempty list targetWords. Return every word index at which a consecutive window contains exactly the same multiset of words as targetWords.

Order within a matching window does not matter, duplicate target words retain their multiplicity, matching is case-sensitive, and result indices must be ascending.

## Examples

### Example 1

**Input:** `textWords = ["red","blue","green","blue","red"]`, `targetWords = ["blue","red"]`

**Output:** `[0,3]`

**Explanation:** The first and last two-word windows each contain one red and one blue word.

### Example 2

**Input:** `textWords = ["a","a","b","a"]`, `targetWords = ["a","a"]`

**Output:** `[0]`

**Explanation:** Only the first window contains two copies of a.

## Constraints

- `1 <= targetWords.length <= textWords.length <= 100000.`
- `Every word is a nonempty ASCII string of length at most 40.`

## Deriving the Solution

The answer is every window whose word multiset equals the target's, and the multiset of consecutive windows barely changes: sliding one position removes one word and adds one other. Sorting re-derives a whole window to learn what two counters already know. The counting window is the same instrument [Minimum Window Substring](../leetcode/minimum_window_substring.md) slides over characters, but that problem keeps only the shortest window that covers its target with surplus allowed, while this statement records every window whose word multiset equals the target exactly. The ladder:

1. **Start literal.** Sort the target once, sort each candidate window, and compare the sorted lists: correct, and it re-sorts on every slide: see [Sorted-Window Comparison](#sorted-window-comparison).
2. **Keep counts, not orders.** Multiset equality is per-word count equality; maintain the window's counts and a tally of words whose counts are off, updating it only for the word leaving and the word entering, so a slide costs O(1): see [Match-Count Sliding Window](#match-count-sliding-window).

## Solutions

### Sorted-Window Comparison

#### Derivation

The statement's most literal reading: for each start index, collect the window's words, put both the window and the target into a canonical order, and compare. Sorting is the multiset equality test:

1. Sort `targetWords` once into `target_sorted`.
2. For each `start` from 0 through `len(textWords) - window_size`: sort the slice `textWords[start:start + window_size]`.
3. Append `start` whenever the sorted slice equals `target_sorted`; the loop itself keeps the output ascending.

#### Walkthrough

Example 1 (`textWords = ["red","blue","green","blue","red"]`, `targetWords = ["blue","red"]`), `target_sorted = [blue, red]`:

```text
start 0   window [red, blue]     sorted [blue, red] == [blue, red]   -> record 0
start 1   window [blue, green]   sorted [blue, green]                -> no
start 2   window [green, blue]   sorted [blue, green]                -> no
start 3   window [blue, red]     sorted [blue, red]                  -> record 3
```

The starts collect into `[0, 3]`, matching the expected Output: only the two windows holding one red and one blue word survive.

#### Solution

```python
from typing import List


class Solution:
    def wordWindowStarts(self, textWords: List[str], targetWords: List[str]) -> List[int]:
        window_size = len(targetWords)
        target_sorted = sorted(targetWords)
        starts: List[int] = []
        for start in range(len(textWords) - window_size + 1):
            if sorted(textWords[start:start + window_size]) == target_sorted:
                starts.append(start)
        return starts
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * k log k)`

`n - k + 1` windows at target length `k`, each re-sorted in `O(k log k)`.

##### Space Complexity: `O(k)`

The sorted target plus one sorted window slice at a time.

#### Key Insights

- Sorting is the canonical form that makes multiset equality a plain `==`; order inside the window stops mattering the moment both sides are sorted.
- Every slide re-sorts `k - 1` words that were already sorted one step earlier, which is the entire waste the next approach removes.

### Match-Count Sliding Window

#### Derivation

Multiset equality says nothing about order, only about counts: the window matches when every word's window count equals its target count. So keep two count maps, `needed` for the target and `window` for the current slice, and a `mismatched` tally counting the distinct words whose two counts differ. A slide changes exactly two counts, the word leaving and the word entering; each single-count change can flip at most one word between matched and mismatched, so the tally updates in O(1) and a window is judged by reading one integer:

1. Build `needed` from `targetWords`.
2. Count the first window into `window` and initialize `mismatched` by one scan over the union of both maps' keys.
3. Record start 0 when `mismatched == 0`.
4. On each slide: remove the word leaving (its count drops by one) and add the word entering; each update bumps the tally when it breaks a matched count and clears it when it lands exactly on the needed count.
5. Record every start where `mismatched == 0`; the loop keeps the output ascending.

#### Invariant

After every update, `mismatched` equals the number of distinct words (in the union of `window`'s and `needed`'s keys) whose two counts differ, so `mismatched == 0` is exactly multiset equality:

```text
mismatched = | { word : window.get(word, 0) != needed.get(word, 0) } |

add:    count leaving the matched value -> +1; landing on it -> -1
remove: count leaving the matched value -> +1; landing on it -> -1
```

Each update moves one word's count by exactly one, so it can cross the matched value at most once: the two checks per update catch that crossing and nothing else, which keeps the tally exact without ever rescanning. The initial scan pays for the first window once, and every later window is judged by the O(1) tally read.

#### Walkthrough

Example 1, `needed` = blue: 1, red: 1. Each line shows the window and the tally after the slide:

```text
start 0   window [red, blue]     counts on target: mismatched 0  -> record 0
slide 1   drop red, add green    red runs out, green surplus:  mismatched 2
start 1   window [blue, green]                                   no
slide 2   drop blue, add blue    blue restored, red still out,
                                 green still surplus:          mismatched 2
start 2   window [green, blue]                                   no
slide 3   drop green, add red    every count back on target:   mismatched 0
start 3   window [blue, red]                                     -> record 3
```

The starts collect into `[0, 3]`, matching the expected Output. Slide 2 is the subtle one: dropping and adding the same word returns the tally to where it was, and the counts never lied about the two true mismatches (red absent, green surplus).

#### Solution

The code is the invariant maintained by hand: one scan to seed the tally, then two checks per edge word.

```python
from typing import Dict, List


class Solution:
    def wordWindowStarts(self, textWords: List[str], targetWords: List[str]) -> List[int]:
        needed: Dict[str, int] = {}
        for word in targetWords:
            needed[word] = needed.get(word, 0) + 1

        window_size = len(targetWords)
        window: Dict[str, int] = {}
        for word in textWords[:window_size]:
            window[word] = window.get(word, 0) + 1
        mismatched = sum(
            1
            for word in set(window) | set(needed)
            if window.get(word, 0) != needed.get(word, 0)
        )

        def add(word: str) -> None:
            nonlocal mismatched
            if window.get(word, 0) == needed.get(word, 0):
                mismatched += 1
            window[word] = window.get(word, 0) + 1
            if window[word] == needed.get(word, 0):
                mismatched -= 1

        def remove(word: str) -> None:
            nonlocal mismatched
            if window[word] == needed.get(word, 0):
                mismatched += 1
            window[word] -= 1
            if window[word] == needed.get(word, 0):
                mismatched -= 1

        starts: List[int] = []
        if mismatched == 0:
            starts.append(0)
        for start in range(1, len(textWords) - window_size + 1):
            remove(textWords[start - 1])
            add(textWords[start + window_size - 1])
            if mismatched == 0:
                starts.append(start)
        return starts
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + k)`

Building `needed` and the first window is `O(k)` plus one `O(k)`-sized scan to seed the tally; each of the `n - k` slides is a constant number of average O(1) dict updates. With `k <= n` the total is linear in the input.

##### Space Complexity: `O(n + k)`

The two count maps hold at most the distinct words of text and target, plus the result list.

#### Key Insights

- The mismatch tally is the multiset comparison made incremental: equality of whole maps is replaced by a counter that only the two edge words can move.
- Words absent from the target are handled by one default: `needed.get(word, 0)` is 0, so any occurrence is automatically a mismatch.
- Seeding the tally by scan instead of starting it at zero is what makes the invariant true from the first slide; the increments alone would miscount the initial window.

## Comparison of Solutions

### Time Complexity

- **Sorted-Window Comparison**: `O(n * k log k)` - every window re-sorted.
- **Match-Count Sliding Window**: `O(n + k)` - constant work per slide after one seed scan.

### Space Complexity

- **Sorted-Window Comparison**: `O(k)` - the sorted target and one window.
- **Match-Count Sliding Window**: `O(n + k)` - two count maps over the distinct input words.

### Trade-offs

- **Sorted-Window Comparison**: the definition written down, trivially correct, and the natural oracle; the per-window sort is wasted work on stable windows.
- **Match-Count Sliding Window**: linear in the input and insensitive to window size; it pays for two count maps and the discipline of the tally invariant.

### When to Use Each

- **Sorted-Window Comparison**: for short texts, as the baseline to state first, and as the independent checker for the sliding version.
- **Match-Count Sliding Window (Recommended)**: the interview answer, and the only one that meets the statement's 100000-word bound comfortably when windows are long.

### Optimization Notes

- **Match-Count Sliding Window** is the recommended choice: `O(n + k)` stays flat as `k` grows, where the sorted comparison multiplies by `k log k`.
- The `remove` helper's final check does fire when a surplus count drops onto the needed value, so the two checks per update are symmetric and neither can be dropped.
- The statement's ascending-output rule needs no sort: scanning starts in increasing order records them sorted; never post-sort a result the loop already ordered.
