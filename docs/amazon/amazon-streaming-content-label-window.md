# [Longest Content Window with Bounded Labels](https://www.fastprep.io/problems/amazon-streaming-content-label-window)

**Hard** | **NN minutes** | **Array, Hash Table, Sliding Window**

A content stream arrives in order. Each item carries a non-empty set of labels. Given contentLabels and a limit k, find the longest contiguous window of items whose combined label set contains at most k distinct labels.

Return the inclusive zero-based endpoints [start, end]. If several windows have the same maximum length, return the one with the smallest start. Return [-1, -1] when the stream is empty. Labels within one item are unique.

This finite batch represents the same ordered add(contentLabels) stream followed by a longest() query.

## Examples

### Example 1

**Input:** `contentLabels = [["toxic","ok"],["toxic","ok","spam"]]`, `k = 2`

**Output:** `[0,0]`

**Explanation:** The first item uses exactly two labels. Including the second item introduces spam, exceeding the limit.

### Example 2

**Input:** `contentLabels = [["toxic","ok"],["toxic","ok","spam"]]`, `k = 3`

**Output:** `[0,1]`

**Explanation:** All two items together use the three permitted labels.

### Example 3

**Input:** `contentLabels = [["a"],["b","c"],["a","b"],["d"]]`, `k = 3`

**Output:** `[0,2]`

**Explanation:** The first three items use a, b, c. Adding the final item introduces a fourth label.

## Constraints

- `0 <= contentLabels.length <= 200000.`
- `1 <= k <= 200000.`
- `Each item has between 1 and 20 unique non-empty labels.`
- `The total number of label occurrences does not exceed 400000.`

## Solutions

### Brute Force

#### Derivation

The most direct reading tests every contiguous window and keeps the longest one whose combined label set fits inside `k`. Rather than building each window's label set from scratch, anchor a `window_start` and grow `window_end` rightward, folding each new item's labels into a running `window_labels` count dict. The moment the distinct count passes `k`, no extension of this anchor can recover: every longer window starting at `window_start` contains a strict superset of the labels, so the anchor is abandoned:

1. Initialize `longest = -1` and `best_start, best_end = -1, -1`; the `-1`
   sentinel distinguishes "no valid window found" from any real window.
2. For each `window_start`, begin an empty `window_labels` count dict.
3. Extend `window_end` from `window_start` to the last item, incrementing the
   count of each of its labels.
4. If `len(window_labels)` exceeds `k`, break: no window from this anchor can
   ever be valid again.
5. Otherwise record the window when `window_end - window_start` beats
   `longest`.
6. Return `[best_start, best_end]`, which stays `[-1, -1]` when the stream is
   empty or no window fits.

#### Walkthrough

Let us run the anchors of Example 1, `contentLabels = [["toxic","ok"],["toxic","ok","spam"]]`, `k = 2`, by hand. Each line is one `window_end` step; the dict shows `window_labels` after the step's labels are folded in:

```text
start=0  end=0  add toxic, ok, spam? no: item 0 = ["toxic","ok"]
                window_labels {toxic:1, ok:1}  distinct 2 <= 2
                length 1 > longest -1   -> best [0, 0]
start=0  end=1  item 1 = ["toxic","ok","spam"]: spam raises distinct to 3
                3 > 2 -> break this anchor
start=1  end=1  window_labels {toxic:1, ok:1, spam:1}  distinct 3 > 2
                -> break immediately, no valid window starts at item 1
```

The only valid window is item `0` alone: item `1` carries all three labels and cannot join any window under `k = 2`. The function returns `[0, 0]`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's anchor-and-grow loop written down.

```python
from typing import List


class Solution:
    def longestContentWindow(self, contentLabels: List[List[str]],
                             k: int) -> List[int]:
        item_total = len(contentLabels)
        longest = -1
        best_start, best_end = -1, -1
        for window_start in range(item_total):
            window_labels: dict[str, int] = {}
            for window_end in range(window_start, item_total):
                for label in contentLabels[window_end]:
                    window_labels[label] = window_labels.get(label, 0) + 1
                if len(window_labels) > k:
                    break
                if window_end - window_start > longest:
                    longest = window_end - window_start
                    best_start, best_end = window_start, window_end
        return [best_start, best_end]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × L)`

Let `m` be the item count and `L` the total number of label occurrences: each of the `m` anchors re-walks up to all `L` occurrences before its break, and every step folds that item's labels into the dict.

##### Space Complexity: `O(D)`

`window_labels` never holds more than one entry per distinct label in the stream, `D` in total.

#### Key Insights

- Correct from first principles: every window is tested, so the tie-break (smallest start among equal lengths) falls out of the outer loop order for free.
- The break is the only pruning, and it is sound because label sets only grow as a window extends: one violation retires the whole anchor.
- Under the stated limits (`m` up to 200000, `L` up to 400000) the quadratic re-walking is exactly what disqualifies this as the final answer, but it remains the reference oracle against which the linear version is checked.

### Sliding Window with Label Counts

#### Derivation

The brute force pays because each new anchor rebuilds a window that is almost identical to the one just examined. When a window violates `k`, only its oldest items are at fault: every label they carry may be carried by later items too, so the repair is local. Keep one `window_start` for the whole run and shrink the window from the left, removing item `window_start`'s labels (dropping entries whose count reaches zero, so `len(window_labels)` stays an exact distinct count) until the window is valid again. Each item then enters the window once and leaves at most once, which is the classic sliding window over the item stream, the same shape as the longest-substring-without-repeats family but stepping item by item and counting up to 20 labels per step:

1. Initialize `label_counts`, `window_start = 0`, `longest = -1`, and
   `best_start, best_end = -1, -1`.
2. For each `window_end`, increment the count of every label the item carries.
3. While `len(label_counts)` exceeds `k`, decrement every label of item
   `window_start`, delete any entry that reaches `0`, and advance
   `window_start`.
4. Record `[window_start, window_end]` whenever `window_end - window_start`
   strictly beats `longest`.
5. Return `[best_start, best_end]`; the sentinels survive unchanged when the
   stream is empty or nothing fits.

#### Invariant

The loop preserves this property at every `window_end`: `window_start` is the smallest start for which the window `[window_start, window_end]` holds at most `k` distinct labels.

```text
label_counts   = exact label multiset of items window_start..window_end
len(label_counts) <= k            (after the shrink loop)
no j < window_start makes items j..window_end valid
```

Why each part holds: `label_counts` is exact because every entering item adds its labels and every leaving item removes exactly its own. The shrink loop restores the bound by evicting whole items from the left until the count is legal again, and eviction is the only repair possible. Minimality survives because a smaller start means a strict superset of items and therefore of labels: if the current window violates, every window starting earlier violates too, so `window_start` never needs to move back when a later, smaller item arrives. At loop exit over all ends, every window has been the recorded candidate at its own `window_end`, so the best window overall cannot be missed; and because strict comparison keeps earlier recordings, equal-length ties resolve to the smallest start automatically.

#### Walkthrough

Let us slide over Example 3, `contentLabels = [["a"],["b","c"],["a","b"],["d"]]`, `k = 3`. Each line shows `label_counts` after the step, with the shrink loop's work spelled out:

```text
end=0  add a            {a:1}                 distinct 1  window [0,0] len 1
end=1  add b, c         {a:1, b:1, c:1}       distinct 3  window [0,1] len 2
end=2  add a, b         {a:2, b:2, c:1}       distinct 3  window [0,2] len 3
end=3  add d            {a:2, b:2, c:1, d:1}  distinct 4 > 3
        shrink item 0 "a":    a drops to 1        distinct still 4
        shrink item 1 "b","c": b drops to 1, c hits 0 and is deleted
                              {a:1, b:1, d:1}     distinct 3, window_start = 2
                              window [2,3] len 2 < 3, best unchanged
```

The widest valid window is items `0` through `2`, whose combined labels are exactly `a`, `b`, `c`, so the function returns `[0, 2]`, matching the expected Output for Example 3. Note the shrink on `end=3` never moved `window_start` past item `1`: item `2`'s labels were already present, so re-adding the window from scratch, as the brute force does, would have been pure waste.

#### Solution

The code is the walkthrough: one dict of live counts, one left edge that only ever moves forward.

```python
from typing import List


class Solution:
    def longestContentWindow(self, contentLabels: List[List[str]],
                             k: int) -> List[int]:
        item_total = len(contentLabels)
        label_counts: dict[str, int] = {}
        window_start = 0
        longest = -1
        best_start, best_end = -1, -1
        for window_end in range(item_total):
            for label in contentLabels[window_end]:
                label_counts[label] = label_counts.get(label, 0) + 1
            while len(label_counts) > k:
                for label in contentLabels[window_start]:
                    label_counts[label] -= 1
                    if label_counts[label] == 0:
                        del label_counts[label]
                window_start += 1
            if window_end - window_start > longest:
                longest = window_end - window_start
                best_start, best_end = window_start, window_end
        return [best_start, best_end]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(L)`

Each of the `L` label occurrences is incremented once when its item enters the window and decremented at most once when an item leaves, and every other per-item step is constant or proportional to that item's own labels.

##### Space Complexity: `O(D)`

`label_counts` holds one entry per distinct label currently in the window, bounded by the `D` distinct labels in the stream.

#### Key Insights

- Deleting counts that reach `0` is what keeps `len(label_counts)` a true distinct-label count; decrementing without deleting would make the violation test `> k` fire late and produce wrong windows.
- Items are the atoms, not labels: the shrink loop always evicts whole items, because a window is a contiguous range of items and partially evicting an item's labels would corrupt `label_counts`.
- Strict comparison on `window_end - window_start` against `longest` encodes the smallest-start tie-break with no extra bookkeeping: an equal-length window found later necessarily starts later.
- The `-1` sentinels do double duty: they report the empty stream and, as a byproduct of the length test, any stream where even a single item exceeds `k`.
- The statement's streaming framing (repeated `add` calls followed by one `longest` query) is served by this exact loop: `add` extends the right edge and `longest` reads the recorded best, with no state ever rebuilt.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(m × L)` - every anchor re-walks the suffix of label occurrences until the limit breaks it.
- **Sliding Window with Label Counts**: `O(L)` - each label occurrence is added once and removed at most once across the whole run.

### Space Complexity

- **Brute Force**: `O(D)` - one count dict per anchor, bounded by the distinct labels.
- **Sliding Window with Label Counts**: `O(D)` - a single count dict held for the whole run.

### Trade-offs

- The brute force is the straightforward translation of the sentence "try every window", trivial to trust, but its per-anchor restart repeats almost all of the work the previous anchor just did.
- The sliding window keeps its work between anchors, reaching linear time in the total label occurrences; the price is the shrink loop, the delete-on-zero rule, and the invariant argument for why `window_start` never rewinds.

### When to Use Each

- **Brute Force**: tiny streams, or as the reference oracle when testing the sliding window version.
- **Sliding Window with Label Counts (Recommended)**: the interview answer, and the only one of the two that survives the stated limits of 200000 items and 400000 label occurrences.

### Optimization Notes

- The count-dict-with-deletion pattern is the multi-label generalization of the character-count sliding window: the invariant `len(label_counts) <= k` replaces the repeat-character test, and eviction granularity is the item rather than the character.
- Both versions return `[-1, -1]` through the same sentinel mechanism, so the empty-stream rule and the nothing-fits rule cost no separate code path.
- If labels arrived as hashable objects other than strings, nothing in the loop changes: the dict keys are the only assumption, which is why no per-label special casing appears anywhere.
- For a true streaming service, the same structure supports an online `add` in amortized time proportional to the incoming item's label count, while `longest` is a field read; the batch function here is that loop run once over the whole stream.
