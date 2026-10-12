# [Recent Advertisement Click Counts](https://www.fastprep.io/problems/amazon-ad-click-counts-sliding-window)

**Medium** | **NN minutes** | **Queue, Hash Table, Sliding Window, Design**

You receive a finite sequence of advertisement click and count operations. Each operation is one of:

CLICK <adId> <timestamp>: record one click for the advertisement.COUNT <adId> <timestamp>: report how many clicks that advertisement received during the latest kMinutes.Timestamps are integer seconds and never decrease. Process operations in input order, including operations with the same timestamp. For a count at time t, include clicks whose timestamps are in the inclusive interval [t - 60 * kMinutes + 1, t].

Return one integer for each COUNT operation, in query order. CLICK operations produce no output.

## Examples

### Example 1

**Input:** `operations = ["CLICK shoes 100","CLICK books 120","CLICK shoes 159","COUNT shoes 160","COUNT books 180","COUNT shoes 220"]`, `kMinutes = 1`

**Output:** `[1,0,0]`

**Explanation:** At time 160, only the shoes click at 159 remains in [101,160]. The books click at 120 is outside [121,180], and both shoes clicks are outside [161,220].

### Example 2

**Input:** `operations = ["CLICK ad1 10","CLICK ad1 69","COUNT ad1 69","COUNT ad1 70"]`, `kMinutes = 1`

**Output:** `[2,1]`

**Explanation:** At time 69, timestamp 10 is exactly the inclusive lower boundary. At time 70, the lower boundary advances to 11, so only the click at 69 remains.

## Constraints

- `1 <= operations.length <= 100000.`
- `1 <= kMinutes <= 100000.`
- `Every operation is exactly CLICK <adId> <timestamp> or COUNT <adId> <timestamp>, with single spaces between tokens.`
- `Each advertisement ID contains 1 to 50 lowercase English letters or digits.`
- `0 <= timestamp <= 10^12, and timestamps are nondecreasing.`
- `Use signed 64-bit arithmetic for timestamps and window boundaries.`

## Solutions

### Brute Force Scan of Click Logs

#### Derivation

The most literal reading of a COUNT is: look at every click ever recorded for the advertisement and count the ones whose timestamps fall in the query's interval. No ordering assumption is needed, no eviction happens, and the interval arithmetic is stated directly: a count at time `t` covers the inclusive range `[t - 60 * kMinutes + 1, t]`. The structure is one map from advertisement ID to the list of its click timestamps, appended on CLICK and scanned on COUNT:

1. Parse each operation into `kind`, `ad_id`, and `timestamp`.
2. Set `window_size = 60 * kMinutes`.
3. On CLICK, append `timestamp` to `clicks_by_ad[ad_id]`.
4. On COUNT, compute `oldest_allowed = timestamp - window_size + 1` and count
   the recorded clicks of `ad_id` lying in `[oldest_allowed, timestamp]`.
5. Collect one integer per COUNT in `counts` and return it.

#### Walkthrough

Run Example 1: `operations = ["CLICK shoes 100","CLICK books 120","CLICK shoes 159","COUNT shoes 160","COUNT books 180","COUNT shoes 220"]`, `kMinutes = 1`, so `window_size = 60` seconds. The three CLICKs build the logs:

```text
CLICK shoes 100   clicks_by_ad = {shoes: [100]}
CLICK books 120   clicks_by_ad = {shoes: [100], books: [120]}
CLICK shoes 159   clicks_by_ad = {shoes: [100, 159], books: [120]}
```

Each COUNT then scans the queried advertisement's full log:

```text
COUNT shoes 160   oldest_allowed = 160 - 60 + 1 = 101, window [101, 160]
                  100 < 101: outside      159 in [101, 160]: inside
                  -> 1
COUNT books 180   oldest_allowed = 121, window [121, 180]
                  120 < 121: outside
                  -> 0
COUNT shoes 220   oldest_allowed = 161, window [161, 220]
                  100, 159 both < 161: outside
                  -> 0
```

The three scan results assemble into `counts = [1, 0, 0]`, matching the expected Output for Example 1. The first scan shows the boundary excluding the click at `100`: it is one second too old for the window starting at `101`.

#### Solution

The code is the parse, the append, and the full scan with the inclusive boundary from the walkthrough.

```python
from typing import Dict, List


class Solution:
    def countRecentAdClicks(self, operations: List[str], kMinutes: int) -> List[int]:
        window_size = 60 * kMinutes
        clicks_by_ad: Dict[str, List[int]] = {}
        counts: List[int] = []

        for operation in operations:
            kind, ad_id, timestamp_text = operation.split()
            timestamp = int(timestamp_text)
            if kind == "CLICK":
                clicks_by_ad.setdefault(ad_id, []).append(timestamp)
            else:
                oldest_allowed = timestamp - window_size + 1
                recent_clicks = sum(
                    1
                    for click_time in clicks_by_ad.get(ad_id, [])
                    if oldest_allowed <= click_time <= timestamp
                )
                counts.append(recent_clicks)

        return counts
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

With `n` operations and up to `n` recorded clicks, each COUNT scans the queried advertisement's entire log, so a run of counts after a run of clicks costs up to `n` scans of length `n`.

##### Space Complexity: `O(n)`

Every click is recorded and never evicted, so the logs grow with the number of CLICK operations.

#### Key Insights

- The whole problem is interval membership plus storage; the brute version is worth writing first because the boundary `[t - 60 * kMinutes + 1, t]` is the only subtle part and it must be right in every approach.
- Clicks arrive with nondecreasing timestamps only across the operation stream; the brute scan ignores that gift entirely and re-examines expired clicks on every query.
- Storing clicks forever buys nothing: a click outside the window at one COUNT stays outside at every later COUNT, since timestamps never decrease and the window only slides forward.

### Per-Ad Deque Sliding Window

#### Derivation

The brute force re-scans expired clicks on every query, yet the nondecreasing timestamps make expiry a one-way street: once a click falls behind the window's leading edge, it can never return. A [deque](https://en.wikipedia.org/wiki/Double-ended_queue) per advertisement turns that observation into `O(1)` amortized queries. Keep only clicks still plausibly inside the window, ordered by timestamp; on COUNT, pop from the front while the oldest click is older than `oldest_allowed`, and the remaining length is the answer. Nothing inside the deque can exceed `timestamp` either, because operations carry nondecreasing timestamps and future clicks have not happened yet:

1. Group clicks into `clicks_by_ad`, a map from advertisement ID to a deque of
   timestamps, with `defaultdict(deque)`.
2. Set `window_size = 60 * kMinutes`.
3. On CLICK, append `timestamp` to the advertisement's deque.
4. On COUNT, compute `oldest_allowed = timestamp - window_size + 1`; while the
   deque's front is strictly below `oldest_allowed`, popleft it.
5. Append `len(ad_clicks)` to `counts` and continue.

The strict comparison `ad_clicks[0] < oldest_allowed` is what implements the inclusive left boundary: a click exactly at `oldest_allowed` stays. Evicting at query time (rather than at insert time) is safe because the deque front only expires, and it keeps CLICK work constant.

#### Walkthrough

Run Example 2, `operations = ["CLICK ad1 10","CLICK ad1 69","COUNT ad1 69","COUNT ad1 70"]`, `kMinutes = 1`, `window_size = 60`. This input exercises both sides of the inclusive boundary:

```text
CLICK ad1 10   deque ad1 = [10]
CLICK ad1 69   deque ad1 = [10, 69]

COUNT ad1 69   oldest_allowed = 69 - 60 + 1 = 10
               front 10 < 10? no -> nothing evicted
               count = len([10, 69]) = 2

COUNT ad1 70   oldest_allowed = 70 - 60 + 1 = 11
               front 10 < 11? yes -> popleft, deque = [69]
               front 69 < 11? no -> stop
               count = len([69]) = 1
```

At time 69 the click at 10 sits exactly on `oldest_allowed`, so the strict comparison keeps it and the count is 2. One second later the boundary advances to 11, the same click expires, and the count drops to 1. The returned list `[2, 1]` matches the expected Output for Example 2.

#### Solution

The code is the per-ad deque with evict-then-measure from the walkthrough.

```python
from collections import defaultdict, deque
from typing import DefaultDict, Deque, List


class Solution:
    def countRecentAdClicks(self, operations: List[str], kMinutes: int) -> List[int]:
        window_size = 60 * kMinutes
        clicks_by_ad: DefaultDict[str, Deque[int]] = defaultdict(deque)
        counts: List[int] = []

        for operation in operations:
            kind, ad_id, timestamp_text = operation.split()
            timestamp = int(timestamp_text)
            if kind == "CLICK":
                clicks_by_ad[ad_id].append(timestamp)
            else:
                oldest_allowed = timestamp - window_size + 1
                ad_clicks = clicks_by_ad[ad_id]
                while ad_clicks and ad_clicks[0] < oldest_allowed:
                    ad_clicks.popleft()
                counts.append(len(ad_clicks))

        return counts
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each CLICK appends once and each click is evicted at most once across the whole run, so the popleft loop is amortized `O(1)` per operation and the total is linear in `n`, the number of operations.

##### Space Complexity: `O(n)`

The deques hold only clicks still inside their advertisement's latest window, which is bounded by the total number of clicks, `O(n)` in the worst case where every click stays recent.

#### Key Insights

- Nondecreasing timestamps upgrade a re-scanning count into an amortized eviction queue: expiry is monotone, so a deque front is always the next to die.
- The inclusive boundary lives in one character: `ad_clicks[0] < oldest_allowed` evicts strictly-older clicks only, which Example 2 pins on both sides (keep at boundary, evict one second later).
- Counting by `len(ad_clicks)` after eviction needs no per-ad counters and no recomputation; the queue's length is the answer.
- Eviction happens on COUNT, not on CLICK, so the hot write path stays `O(1)` and stale clicks cost nothing until someone asks about them.

## Comparison of Solutions

### Time Complexity

- **Brute Force Scan of Click Logs**: `O(n^2)` - each COUNT scans the advertisement's full click history.
- **Per-Ad Deque Sliding Window**: `O(n)` - each click is appended once and evicted at most once across the run.

### Space Complexity

- **Brute Force Scan of Click Logs**: `O(n)` - every click is stored forever, expired or not.
- **Per-Ad Deque Sliding Window**: `O(n)` - only clicks still inside their window are stored, bounded by the total click count.

### Trade-offs

- **Brute Force Scan of Click Logs**: the interval rule appears verbatim in one expression, making correctness obvious, but it pays for the whole history on every query.
- **Per-Ad Deque Sliding Window**: amortized constant queries rely on the nondecreasing-timestamp guarantee, and the deque silently discards history that later queries cannot need.

### When to Use Each

- **Brute Force Scan of Click Logs**: as a first correct version to test against, or when queries are rare compared with clicks.
- **Per-Ad Deque Sliding Window (Recommended)**: the interview answer: linear overall, and it uses exactly the ordering guarantee the constraints announce.

### Optimization Notes

- `window_size = 60 * kMinutes` is computed once before the loop; hoisting it out of the parse loop keeps the per-operation work to comparison and queue moves.
- The boundary can reach below zero for small timestamps (`t - 60 * kMinutes + 1` may be negative); Python integers need no care here, but in a language with fixed-width integers the constraint's signed 64-bit note applies because timestamps reach `10^12`.
- `defaultdict(deque)` means COUNT on an advertisement with no clicks creates an empty deque and reports 0 without a membership check; a plain dict would need `clicks_by_ad.get(ad_id)`.
- Test both boundary sides when the window edge is involved: a click exactly at `oldest_allowed` (Example 2 at time 69) must survive, and the next second's COUNT must evict it.
