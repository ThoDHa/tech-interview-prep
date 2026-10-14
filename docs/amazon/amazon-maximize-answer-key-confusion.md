# [Maximize Consecutive Equal Answers](https://www.fastprep.io/problems/amazon-maximize-answer-key-confusion)

**Medium** | **NN minutes** | **String, Sliding Window**

A string contains only T and F. You may change at most maxChanges characters. Return the maximum length of a contiguous substring that can be made entirely equal.

## Examples

### Example 1

**Input:** `answers = "TTFF"`, `maxChanges = 2`

**Output:** `4`

**Explanation:** Case 1 exercises the documented deterministic contract.

### Example 2

**Input:** `answers = "TFFT"`, `maxChanges = 1`

**Output:** `3`

**Explanation:** Case 2 exercises the documented deterministic contract.

### Example 3

**Input:** `answers = "TTFTTFTT"`, `maxChanges = 1`

**Output:** `5`

**Explanation:** Case 3 exercises the documented deterministic contract.

## Constraints

- `1 <= answers.length <= 200000.`
- `0 <= maxChanges <= answers.length.`

## Solutions

### Brute Force

#### Derivation

The most literal reading of the problem tests every contiguous window. A window can be made entirely equal exactly when its minority letter is small enough to change wholesale: a window holding `true_count` Ts and `false_count` Fs converts fully by changing `min(true_count, false_count)` characters. So each window is judged by one inequality, and a window is a candidate whenever `min(true_count, false_count) <= maxChanges`. Because both counts only grow as the window extends, the minority count is non-decreasing under extension: the first violation at an anchor retires every longer window from that anchor, so the inner loop can break:

1. For each `window_start`, reset `true_count` and `false_count` to `0`.
2. Extend `window_end` rightward, counting the letter just entered.
3. When `min(true_count, false_count)` exceeds `maxChanges`, break: no
   longer window from this anchor can recover.
4. Otherwise record `window_end - window_start + 1` when it beats `longest`.
5. Return `longest`.

#### Walkthrough

Let us run the anchors by hand on Example 2: `answers = "TFFT"`, `maxChanges = 1`. Each line is one `window_end` step, with the counts after the step and the minority test:

```text
start=0  end=0 'T'  T1 F0  min 0 <= 1  len 1  longest = 1
         end=1 'F'  T1 F1  min 1 <= 1  len 2  longest = 2
         end=2 'F'  T1 F2  min 1 <= 1  len 3  longest = 3
         end=3 'T'  T2 F2  min 2 > 1  -> break this anchor
start=1  end=1 'F'  T0 F1  min 1 <= 1  len 1
         end=2 'F'  T0 F2  min 2 > 1  -> break
start=2  end=2 'F'  T0 F1  min 1 <= 1  len 1
         end=3 'T'  T1 F1  min 1 <= 1  len 2  longest stays 3
start=3  end=3 'T'  T1 F0  min 0 <= 1  len 1
```

The best window is `"TFF"` (positions 0 through 2): changing its single T makes `"FFF"`, a fully equal window of length 3. The function returns `3`, matching the expected Output for Example 2.

#### Solution

The code is the walkthrough's anchor-and-grow loop written down: two counters, one minority test, one break.

```python
class Solution:
    def maximizeConfusion(self, answers: str, maxChanges: int) -> int:
        length = len(answers)
        longest = 0
        for window_start in range(length):
            true_count = 0
            false_count = 0
            for window_end in range(window_start, length):
                if answers[window_end] == "T":
                    true_count += 1
                else:
                    false_count += 1
                if min(true_count, false_count) > maxChanges:
                    break
                longest = max(longest, window_end - window_start + 1)
        return longest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

Every anchor re-walks a prefix of the suffix of windows until the first violation, which across all anchors is up to one window per anchor-end pair, quadratic in the string length `n`.

##### Space Complexity: `O(1)`

Only the two counters, the anchor, and the running best are kept; nothing grows with the input.

#### Key Insights

- The validity test reduces the whole "make it all equal" question to one number: the minority count. Everything else is bookkeeping.
- `min(true_count, false_count)` never decreases when the window extends, because both counters only increase; that monotonicity is what licenses the break.
- Correct everywhere, but each anchor repeats almost all of the previous anchor's counting, which is the waste the sliding window removes.

### Sliding Window with Per-Letter Passes

#### Derivation

The brute force's anchors rebuild windows that share almost all of their characters. The fix is the classic [sliding window](https://en.wikipedia.org/wiki/Sliding_window_protocol): keep one window and move its left edge forward only when validity breaks, so each character enters and leaves the window at most once per pass. This problem needs one twist beyond its closest relative, flipping at most `k` zeros into ones: there the target letter is fixed (keep ones), while here the target can be either T or F depending on the window. The resolution is two passes over the same structure, one per target: a pass that counts Fs finds the best all-T window under the change budget, and a pass that counts Ts finds the best all-F window. The answer is the larger of the two:

1. Define `longest_changing(changed_letter)`: the longest window holding at
   most `maxChanges` occurrences of the *other* letter, which the changes
   convert entirely to `changed_letter`.
2. Inside a pass, extend `window_end`; when the entering character equals
   `changed_letter`, increment `changed_count`.
3. While `changed_count > maxChanges`, advance `window_start`, decrementing
   `changed_count` when the character leaving equals `changed_letter`.
4. Record `window_end - window_start + 1` when it beats the pass's `longest`.
5. Return the maximum of the two passes, `F`-counting and `T`-counting.

#### Walkthrough

Let us slide over Example 2, `answers = "TFFT"`, `maxChanges = 1`, in both passes. Each line is one `window_end` step; the shrink rows show `window_start` moving:

```text
F pass (count Fs; window becomes all T)   changed_count = Fs
  end=0 'T'  F0  window [0,0] len 1
  end=1 'F'  F1  window [0,1] len 2
  end=2 'F'  F2 > 1 -> shrink: [0]='T' not F, window_start 1;
                     [1]='F' F1, window_start 2   window [2,2] len 1
  end=3 'T'  F1  window [2,3] len 2                 pass longest = 2

T pass (count Ts; window becomes all F)   changed_count = Ts
  end=0 'T'  T1  window [0,0] len 1
  end=1 'F'  T1  window [0,1] len 2
  end=2 'F'  T1  window [0,2] len 3                 pass longest = 3
  end=3 'T'  T2 > 1 -> shrink: [0]='T' T1, window_start 1
                     window [1,3] len 3             pass longest = 3
```

The T pass finds the window `"FFT"` (positions 1 through 3): changing its single T makes `"FFF"`, and the function returns `max(2, 3) = 3`, matching the expected Output for Example 2. On Example 3, `"TTFTTFTT"` with `maxChanges = 1`, the same two passes return `5` and `2`, so the function returns `5`, matching its expected Output.

#### Solution

The code is the walkthrough's pass, run once per target letter, with the maximum taken across passes.

```python
class Solution:
    def maximizeConfusion(self, answers: str, maxChanges: int) -> int:
        def longest_changing(changed_letter: str) -> int:
            changed_count = 0
            window_start = 0
            longest = 0
            for window_end in range(len(answers)):
                if answers[window_end] == changed_letter:
                    changed_count += 1
                while changed_count > maxChanges:
                    if answers[window_start] == changed_letter:
                        changed_count -= 1
                    window_start += 1
                longest = max(longest, window_end - window_start + 1)
            return longest

        return max(longest_changing("F"), longest_changing("T"))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each pass advances `window_end` exactly `n` times and `window_start` at most `n` times, and both passes together are a constant number of such sweeps.

##### Space Complexity: `O(1)`

The pass holds one counter and two indices; nothing grows with the input.

#### Key Insights

- Counting the letter that gets *changed* (not the letter kept) keeps the violation test a plain `>` on one counter: a window is all-T-convertible exactly when it holds at most `maxChanges` Fs.
- Two passes replace the missing fixed target: every best window is all-T or all-F, so the better pass always contains it.
- The shrink loop's after-state (smallest valid `window_start` for the current `window_end`) is what makes each pass linear: neither edge ever moves backward.
- This is the same window discipline as flipping at most `k` zeros into ones; the only addition is running it once per target letter.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n²)` - every anchor re-counts a prefix of its suffix until the first violation.
- **Sliding Window with Per-Letter Passes**: `O(n)` - two sweeps in which each edge moves forward only, so each character is processed a constant number of times.

### Space Complexity

- **Brute Force**: `O(1)` - two counters and the running best.
- **Sliding Window with Per-Letter Passes**: `O(1)` - one counter and two indices per pass.

### Trade-offs

- The brute force states the validity condition directly and needs no argument about window edges, but its per-anchor restart repeats nearly all of the previous anchor's counting work.
- The sliding window keeps the work between anchors and reaches linear time; the price is the shrink loop and the two-pass argument for why no best window is missed.

### When to Use Each

- **Brute Force**: tiny inputs, or as the reference oracle when testing the sliding window version.
- **Sliding Window with Per-Letter Passes (Recommended)**: the interview answer, and the only one of the two that survives the stated limit of 200000 characters under adversarial inputs.

### Optimization Notes

- The problem is the two-target generalization of the flip-at-most-k-zeros window: with the target fixed, one pass suffices; with both targets allowed, the union of two fixed-target passes covers every candidate window.
- A single-pass variant tracking `true_count` and `false_count` simultaneously and shrinking while `min(true_count, false_count) > maxChanges` also works, for the same monotonicity the brute force's break relies on; it saves the second sweep but couples the shrink logic to both counters.
- The recording line after the shrink loop evaluates only the final, valid window: every intermediate window visited during the shrink is invalid by construction, so no length check happens inside the shrink loop itself.
- Budget comparison belongs in the interview: with a `T`/`F` alphabet the two-pass window is optimal at `O(n)`; for a larger alphabet the same idea needs one pass per target letter, which changes the constant but not the asymptotic shape.
