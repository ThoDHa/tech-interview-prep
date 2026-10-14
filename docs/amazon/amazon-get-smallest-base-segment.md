# [Get Smallest Base Segment](https://www.fastprep.io/problems/amazon-get-smallest-base-segment)

**unknown difficulty** | **NN minutes** | **unknown categories**

In Amazon's distributed storage network, some critical data segments are missing. They are represented by a string missingData. The system restores data by choosing a base segment of length segmentSize and repeatedly appending copies of that base segment to a generated string.

A base segment is valid if, after some number of replications, the generated string contains every character in missingData at least as many times as it appears in missingData.

Among all valid base segments, choose one that requires the fewest replications. If more than one base segment requires that same minimum number of replications, return the lexicographically smallest one. If no valid base segment exists, return "-1".

## Examples

### Example 1

**Input:** `segmentSize = 2`, `missingData = "aavvavv"`

**Output:** `"av"`

**Explanation:** The character a appears 3 times and v appears 4 times. Both "av" and "va" require 4 replications. Since "av" is lexicographically smaller, it is returned.

### Example 2

**Input:** `segmentSize = 1`, `missingData = "abc"`

**Output:** `"-1"`

**Explanation:** A base segment of length 1 can contain only one distinct character, so it cannot generate all three required characters.

## Constraints

- `1 <= segmentSize <= missingData.length`
- `missingData consists of lowercase English letters.`

## Solutions

### Brute Force Over All Segments

#### Derivation

The most literal reading tests every base segment the string can supply. A base segment is any substring of length `segmentSize`; replication can only multiply character counts, so a candidate is valid exactly when it contains every character of `missingData` at least once. If `need` is how often a letter is required and `have` is how often the candidate carries it, `replays` copies deliver `replays × have` of that letter, so the smallest sufficient count is the ceiling of `need / have`, and the whole segment needs the maximum of these ceilings over the required letters:

1. Tally `needed_counts` over `missingData`.
2. For each start position, take `candidate`, the substring of length
   `segmentSize`, and tally `segment_counts`.
3. Skip the candidate when any required letter is missing from it entirely.
4. Otherwise compute `replays` as the maximum of
   `(need_count + have_count - 1) // have_count` over required letters.
5. Keep the candidate with the smallest `(replays, candidate)` pair; the pair
   comparison applies the replication tie rule and the lexicographic tie rule
   in one step.
6. Return the winning segment, or `-1` when none was valid.

#### Walkthrough

Example 1, `segmentSize = 2` on `"aavvavv"`, has five candidate windows. The needed counts are `a: 3` and `v: 4`:

```text
start 0  "aa"   no v            invalid
start 1  "av"   a:1, v:1        replays = max(3/1, 4/1) = 4   best = (4, "av")
start 2  "vv"   no a            invalid
start 3  "va"   v:1, a:1        replays = max(4/1, 3/1) = 4   not better than (4, "av")
start 4  "av"   a:1, v:1        replays = 4                   equal replays, "av" not < "av"
return "av"
```

Both surviving windows need 4 replications, and the `(replays, candidate)` pair keeps `"av"` because it is lexicographically smaller, matching the expected Output. Example 2 ends with no valid window: every length-1 window of `"abc"` is missing two of the three required letters, so the function returns `-1`.

#### Solution

```python
from typing import Dict


class Solution:
    def getSmallestBaseSegment(self, segmentSize: int, missingData: str) -> str:
        length = len(missingData)
        needed_counts: Dict[str, int] = {}
        for letter in missingData:
            needed_counts[letter] = needed_counts.get(letter, 0) + 1

        best_key = None
        for start in range(length - segmentSize + 1):
            candidate = missingData[start:start + segmentSize]
            segment_counts: Dict[str, int] = {}
            for letter in candidate:
                segment_counts[letter] = segment_counts.get(letter, 0) + 1
            if any(letter not in segment_counts for letter in needed_counts):
                continue
            replays = 1
            for needed_letter, need_count in needed_counts.items():
                have_count = segment_counts[needed_letter]
                replays = max(replays, (need_count + have_count - 1) // have_count)
            key = (replays, candidate)
            if best_key is None or key < best_key:
                best_key = key
        return best_key[1] if best_key is not None else "-1"
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × (L + 26))`

With `n = len(missingData)` and `L = segmentSize`, there are `n - L + 1` windows and each is tallied in `O(L)` and checked in `O(26)` for validity and replay count.

##### Space Complexity: `O(L)`

The candidate slice and its tally hold at most `L` characters (the needed-count table holds at most 26).

#### Key Insights

- Replication multiplies counts, so validity needs only presence: every required letter must appear at least once in the base segment, not `need` times.
- The required replication count is a per-letter ceiling, `ceil(need / have)`, maximized over letters; a letter the segment carries in bulk is never the bottleneck.
- Comparing `(replays, candidate)` tuples collapses two tie rules into one comparison.

### Sliding Window with Letter Counts

#### Derivation

The brute force retallies each window from scratch, yet two neighboring windows share `segmentSize - 1` characters: sliding one step drops the leftmost letter and adds one new letter. Maintaining the window tally across the sweep removes the `O(L)` rebuild, and maintaining how many distinct required letters the window covers removes the `O(26)` validity scan, which runs only to answer "is every required letter present?":

1. Tally `needed_counts` once; keep `window_counts` for the current window and
   `distinct_covered`, the number of required letters present at least once.
2. For each `end`, absorb `missingData[end]` into `window_counts`, bumping
   `distinct_covered` when a required letter reaches count 1.
3. From `window_start = end - segmentSize + 1` onward the window is full: when
   `distinct_covered == distinct_needed`, compute `replays` from
   `window_counts` and compare `(replays, segment)` against the best pair.
4. Release `missingData[window_start]`, decrementing `distinct_covered` if a
   required letter falls back to count 0.
5. Return the best segment, or `-1` when no full window ever covered all
   required letters.

The per-step cost drops to `O(1)` for the slide and validity, with the `O(26)` replay computation paid only by windows that are valid.

#### Walkthrough

Example 1 again, `segmentSize = 2` on `"aavvavv"`, needed counts `a: 3`, `v: 4`, so `distinct_needed = 2`:

```text
end 0  absorb a   window_counts {a:1}        covered 1   window not full
end 1  absorb v   window_counts {a:1, v:1}   covered 2
       full window "av": valid, replays = max(3/1, 4/1) = 4    best = (4, "av")
       release a  -> {v:1}, covered 1
end 2  absorb v   {v:2}                      covered 1   window "vv" invalid
       release v  -> {v:1}, covered 1
end 3  absorb a   {v:1, a:1}                 covered 2
       full window "va": valid, replays = 4   not better than (4, "av")
       release v  -> {a:1}, covered 1
end 4  absorb v   {a:1, v:1}                 covered 2
       full window "av": valid, replays = 4   not better than (4, "av")
       release a  -> {v:1}, covered 1
return "av"
```

The count of `distinct_covered` rose to 2 only at the three windows that mix both letters, and the best pair never left `(4, "av")`, the expected Output.

#### Solution

```python
from typing import Dict


class Solution:
    def getSmallestBaseSegment(self, segmentSize: int, missingData: str) -> str:
        length = len(missingData)
        needed_counts: Dict[str, int] = {}
        for letter in missingData:
            needed_counts[letter] = needed_counts.get(letter, 0) + 1

        window_counts: Dict[str, int] = {}
        distinct_needed = len(needed_counts)
        distinct_covered = 0
        best_key = None
        for end in range(length):
            letter = missingData[end]
            window_counts[letter] = window_counts.get(letter, 0) + 1
            if window_counts[letter] == 1:
                distinct_covered += 1

            window_start = end - segmentSize + 1
            if window_start < 0:
                continue

            if distinct_covered == distinct_needed:
                replays = 1
                for needed_letter, need_count in needed_counts.items():
                    have_count = window_counts[needed_letter]
                    replays = max(replays, (need_count + have_count - 1) // have_count)
                key = (replays, missingData[window_start:end + 1])
                if best_key is None or key < best_key:
                    best_key = key

            leaving = missingData[window_start]
            if window_counts[leaving] == 1:
                distinct_covered -= 1
            window_counts[leaving] -= 1
        return best_key[1] if best_key is not None else "-1"
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × 26)`

Each character enters and leaves the window once; the per-step slide and validity check are constant, and the replay computation over at most 26 required letters runs only on valid windows.

##### Space Complexity: `O(26)`

Both count tables and the covered counter hold one entry per distinct letter; the window slice exists only inside the pair comparison.

#### Key Insights

- Sliding a fixed-size window converts the `O(L)` per-window rebuild into one removal and one addition per step.
- `distinct_covered` is the whole validity test: because replication multiplies counts, coverage means count at least 1, and a single integer mirrors exactly that.
- The release runs after the comparison so the window leaving at step `end` is the one just scored; releasing first would score a half-empty window.

### Sliding Window with Counter

#### Derivation

The previous solution hand-rolls two dictionaries and two coverage bumps per step. `collections.Counter` absorbs the tally bookkeeping: building `needed_counts` is one constructor call, window updates are `+= 1` and `-= 1`, and the coverage test becomes a single `all` over the needed letters, which no longer needs its own integer. The algorithm is unchanged; only the ledger moves:

1. Build `needed_counts` and `window_counts` as `Counter` objects.
2. Slide as before, but test coverage with
   `all(window_counts[letter] > 0 for letter in needed_counts)` (a missing
   `Counter` key simply reads as 0).
3. Compute `replays` and compare `(replays, segment)` pairs as before.
4. Decrement the leaving letter; no coverage counter to maintain.

#### Walkthrough

The sweep on Example 1 produces the same events as the hand-tracked version; only the notation changes. `window_counts` after absorbing position 1 is `Counter({'a': 1, 'v': 1})`, the coverage test `all(window_counts[letter] > 0 ...)` passes because both letters hold positive counts, and the best pair settles at `(4, "av")`. The remaining steps track the hand trace line for line, ending at `"av"`, the expected Output. Example 2 never passes the `all` test with a full window, so the function returns `-1`.

#### Solution

```python
from collections import Counter


class Solution:
    def getSmallestBaseSegment(self, segmentSize: int, missingData: str) -> str:
        length = len(missingData)
        needed_counts = Counter(missingData)
        window_counts = Counter()
        best_key = None
        for end in range(length):
            window_counts[missingData[end]] += 1

            window_start = end - segmentSize + 1
            if window_start < 0:
                continue

            if all(window_counts[letter] > 0 for letter in needed_counts):
                replays = max(-(-need_count // window_counts[needed_letter])
                              for needed_letter, need_count in needed_counts.items())
                key = (replays, missingData[window_start:end + 1])
                if best_key is None or key < best_key:
                    best_key = key

            window_counts[missingData[window_start]] -= 1
        return best_key[1] if best_key is not None else "-1"
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × 26)`

Same sweep as the hand-tracked window; the coverage `all` and the replay maximum each iterate at most 26 letters per position.

##### Space Complexity: `O(26)`

Two `Counter` objects over lowercase letters.

#### Key Insights

- `Counter`'s missing-key default of 0 makes the coverage test read directly off the tally, deleting the `distinct_covered` counter and both bump branches.
- `-(-need // have)` is the ceiling of `need / have` without a floating-point round trip.
- The tidy-up changes bookkeeping, not asymptotics: the sweep is still one pass with per-position work bounded by the alphabet.

## Comparison of Solutions

### Time Complexity

- **Brute Force Over All Segments**: `O(n × (L + 26))` - every window is rebuilt from scratch in `O(L)` and checked in `O(26)`.
- **Sliding Window with Letter Counts**: `O(n × 26)` - each character enters and leaves once; validity is `O(1)` and the replay scan is `O(26)` on valid windows.
- **Sliding Window with Counter**: `O(n × 26)` - identical sweep with `Counter` carrying the ledger.

### Space Complexity

- **Brute Force Over All Segments**: `O(L)` - the candidate slice and its per-window tally.
- **Sliding Window with Letter Counts**: `O(26)` - two count tables and one integer.
- **Sliding Window with Counter**: `O(26)` - two `Counter` objects over the lowercase alphabet.

### Trade-offs

- **Brute Force Over All Segments**: shortest to write and hardest to get wrong, but it pays the window rebuild on every start position.
- **Sliding Window with Letter Counts**: removes the rebuild and makes validity a constant-time integer check, at the cost of maintaining the covered counter through every absorb and release.
- **Sliding Window with Counter**: the same algorithm with the ledger handed to the standard library, trading two bookkeeping lines per step for one `all` scan over the needed letters.

### When to Use Each

- **Brute Force Over All Segments**: the right first draft and the oracle for checking the window versions on small inputs.
- **Sliding Window with Letter Counts (Recommended)**: the interview answer: it demonstrates the sliding-window discipline while keeping every mechanism visible.
- **Sliding Window with Counter**: the version to ship, where the standard library ledger reads cleaner and the coverage check survives schema tweaks for free.

### Optimization Notes

- Early exit: when `segmentSize < distinct_needed`, no window can ever cover the required letters, so an explicit guard at the top returns `-1` without sweeping at all.
- The replay computation runs only on windows that pass the coverage check; computing it unconditionally would spend an `O(26)` scan on windows that the check rejects in `O(1)`.
- The slice `missingData[window_start:end + 1]` is built only inside the coverage branch, and only when a valid window beats or ties the current best pair; the sweep proper never copies window content.
