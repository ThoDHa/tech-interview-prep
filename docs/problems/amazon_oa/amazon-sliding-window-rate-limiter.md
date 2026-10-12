# [Sliding-Window Rate Limiter](https://www.fastprep.io/problems/amazon-sliding-window-rate-limiter)

**Medium** | **NN minutes** | **Queue, Hash Table, Sliding Window, Design**

You receive requests in nondecreasing timestamp order. Each request has a user ID and an integer timestamp in seconds.

A request is accepted when that user has fewer than 100 previously accepted requests in the interval (timestamp - 60, timestamp]. Otherwise it is rejected. Rejected requests do not consume capacity. Requests with the same timestamp are processed in input order.

Return one boolean per input request, where true means accepted and false means rejected.

## Examples

### Example 1

**Input:** `userIds = ["amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy","amy"]`, `timestamps = [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]`

**Output:** `[true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,false]`

**Explanation:** The first 100 requests for amy fill the window. The 101st request has the same timestamp and is rejected.

### Example 2

**Input:** `userIds = ["a","b","a","a"]`, `timestamps = [0,0,59,60]`

**Output:** `[true,true,true,true]`

**Explanation:** Users have independent windows. At timestamp 60, the accepted request for a at timestamp 0 lies on the excluded lower boundary and has expired.

## Constraints

- `0 <= userIds.length <= 5000.`
- `userIds.length == timestamps.length.`
- `User IDs contain 1 to 50 lowercase English letters or digits.`
- `0 <= timestamps[i] <= 10^9.`
- `Timestamps are nondecreasing.`

## Solutions

### Per-User History Scan

#### Derivation

The statement defines the decision directly: count the user's accepted requests inside `(timestamp - 60, timestamp]` and accept when the count is below 100. The most literal translation keeps one accepted-timestamp list per user and rescans that whole list for every arriving request. Rejected requests are simply not recorded, which is what "rejected requests do not consume capacity" demands:

1. Keep `accepted_by_user`, a map from user ID to the timestamps of that user's
   accepted requests.
2. For each request, look up the user's list (creating an empty one on first
   sight).
3. Count `requests_in_window`: the list entries greater than
   `timestamp - 60`, the excluded lower boundary.
4. Accept when `requests_in_window < 100`: record `True` and append `timestamp`
   to the list. Otherwise record `False` and append nothing.
5. Return the recorded booleans in input order.

#### Walkthrough

Example 2 (`userIds = ["a","b","a","a"]`, `timestamps = [0,0,59,60]`) exercises user independence, the excluded boundary, and expiry in four requests:

```text
request 1  user a, ts 0    history a: []          count 0 < 100 -> accept   [true]
request 2  user b, ts 0    history b: []          count 0 < 100 -> accept   [true]
request 3  user a, ts 59   history a: [0], window (-1, 59]: 0 counts
                                                  count 1 < 100 -> accept   [true]
request 4  user a, ts 60   history a: [0,59], window (0, 60]: 0 excluded, 59 counts
                                                  count 1 < 100 -> accept   [true]
```

The decisive entry is request 4: the accepted request at timestamp 0 lies on the window's excluded lower boundary, because only entries greater than `60 - 60 = 0` count, so the scan drops it and the request is still accepted. The output is `[true, true, true, true]`, matching Example 2's expected output.

#### Solution

The code is the walkthrough's per-request rule: count the window by scanning the history, then append only on acceptance.

```python
from typing import Dict, List


class Solution:
    def solve(self, user_ids: List[str], timestamps: List[int]) -> List[bool]:
        request_limit = 100
        window_seconds = 60
        accepted_by_user: Dict[str, List[int]] = {}
        decisions: List[bool] = []

        for user_id, timestamp in zip(user_ids, timestamps):
            accepted = accepted_by_user.setdefault(user_id, [])
            window_start = timestamp - window_seconds
            requests_in_window = 0
            for accepted_timestamp in accepted:
                if accepted_timestamp > window_start:
                    requests_in_window += 1
            if requests_in_window < request_limit:
                accepted.append(timestamp)
                decisions.append(True)
            else:
                decisions.append(False)

        return decisions
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)` worst case

Each request scans its user's entire accepted history, so one user collecting `n` accepted requests pays `1 + 2 + ... + n` comparisons.

##### Space Complexity: `O(n)`

The accepted-timestamp lists record each accepted request once.

#### Key Insights

- Transcribes the rule directly; nothing is ever evicted, history is simply recounted per request.
- Appending only on acceptance is what makes rejected requests free of capacity, with no extra bookkeeping.
- The scan is the cost: it re-reads entries the previous request already classified, and the later solutions remove exactly that re-reading.

### Per-User Deque of Accepted Timestamps

#### Derivation

The scan re-reads a history that is already sorted: timestamps arrive in nondecreasing order, so each user's accepted list is sorted too. Sorted histories expire from the front. The oldest entries are the ones that fall out of the window as `timestamp` advances, and once expired an entry can never re-enter a later window. A [deque](https://en.wikipedia.org/wiki/Double-ended_queue) per user holds exactly the accepted timestamps still in the window, and evicting the expired prefix keeps the deque's length equal to the in-window count, so the acceptance test becomes a length comparison:

1. Keep `accepted_by_user` mapping each user to a deque of accepted timestamps
   still in the window.
2. For each request, evict from the deque's front while the oldest entry
   satisfies `accepted[0] <= timestamp - 60` (at or below the excluded
   boundary).
3. Accept when `len(accepted) < 100`: append `timestamp` and record `True`.
4. Otherwise record `False` and leave the deque untouched.

#### Walkthrough

The four requests of Example 2 again (`userIds = ["a","b","a","a"]`, `timestamps = [0,0,59,60]`), now as deque events:

```text
request 1  user a, ts 0    deque a: []      nothing to evict; len 0 < 100 -> accept
                           deque a: [0]                                            [true]
request 2  user b, ts 0    deque b: []      accept; deque b: [0]                    [true]
request 3  user a, ts 59   evict while deque[0] <= 59 - 60 = -1: 0 stays
                           len 1 < 100 -> accept; deque a: [0, 59]                 [true]
request 4  user a, ts 60   evict while deque[0] <= 60 - 60 = 0: 0 <= 0 -> popleft
                           deque a: [59]; len 1 < 100 -> accept; deque a: [59, 60] [true]
```

Request 4 is the boundary beat: timestamp 0 satisfies `0 <= 60 - 60` and is evicted before the count, reproducing the statement's rule that the lower boundary is excluded. The output is `[true, true, true, true]`. Example 1 stresses the cap instead: all 101 requests share one user and one window, so the deque fills to length 100 and request 101 finds `len(accepted) == 100`, records `false`, and appends nothing.

#### Solution

The code is the walkthrough's eviction-then-count: trim the expired prefix, compare the length to the cap, append only on acceptance.

```python
from collections import deque
from typing import Deque, Dict, List


class Solution:
    def solve(self, user_ids: List[str], timestamps: List[int]) -> List[bool]:
        request_limit = 100
        window_seconds = 60
        accepted_by_user: Dict[str, Deque[int]] = {}
        decisions: List[bool] = []

        for user_id, timestamp in zip(user_ids, timestamps):
            accepted = accepted_by_user.setdefault(user_id, deque())
            while accepted and accepted[0] <= timestamp - window_seconds:
                accepted.popleft()
            if len(accepted) < request_limit:
                accepted.append(timestamp)
                decisions.append(True)
            else:
                decisions.append(False)

        return decisions
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each request does constant work plus its evictions, and every accepted timestamp is appended once and popped at most once across the whole run.

##### Space Complexity: `O(n)`

The deques hold only accepted timestamps.

#### Key Insights

- Nondecreasing input timestamps make every per-user history sorted, which is what legitimizes eviction from the front.
- Evicting before counting keeps the deque's length equal to the in-window count, so the acceptance test is an `O(1)` length comparison.
- Amortized analysis is the linear-time argument: an entry can only leave once per time it entered.

### Per-User Sorted List with Bisect

#### Derivation

The baseline's only expensive step is counting the in-window entries by hand. That count is a range query on a sorted list, which is precisely what [`bisect_left`](https://docs.python.org/3/library/bisect.html) answers without touching the expired prefix: find the first position holding an in-window timestamp, and everything from there to the end is in window. Appends keep the list sorted for free because timestamps are nondecreasing, so no insertion logic is needed:

1. Keep `accepted_by_user` mapping each user to the sorted list of that user's
   accepted timestamps.
2. For each request, compute `first_in_window = bisect_left(accepted,
   timestamp - 59)`, the first entry greater than `timestamp - 60` (timestamps
   are integers, so the smallest in-window value is `timestamp - 60 + 1`).
3. The in-window count is `len(accepted) - first_in_window`; accept when it is
   below 100 and append `timestamp`.

#### Walkthrough

Example 2's fourth request is again the boundary case: user `a` holds `accepted = [0, 59]` and arrives at `timestamp = 60`. The smallest in-window integer is `60 - 60 + 1 = 1`, and `bisect_left([0, 59], 1)` returns position `1` (the value `0` sorts before `1`), so the count is `2 - 1 = 1`, below 100, and the request is accepted. Example 1's decisive request works out to `first_in_window = bisect_left(accepted, 10 - 60 + 1) = 0` over a full list of 100 accepted timestamps: the count is `100`, the request records `false`, and the list stays at 100 entries.

#### Solution

The code is the baseline with the counting loop replaced by one binary search.

```python
from bisect import bisect_left
from typing import Dict, List


class Solution:
    def solve(self, user_ids: List[str], timestamps: List[int]) -> List[bool]:
        request_limit = 100
        window_seconds = 60
        accepted_by_user: Dict[str, List[int]] = {}
        decisions: List[bool] = []

        for user_id, timestamp in zip(user_ids, timestamps):
            accepted = accepted_by_user.setdefault(user_id, [])
            first_in_window = bisect_left(
                accepted, timestamp - window_seconds + 1
            )
            if len(accepted) - first_in_window < request_limit:
                accepted.append(timestamp)
                decisions.append(True)
            else:
                decisions.append(False)

        return decisions
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Each request pays one binary search over its user's history, and appends keep the list sorted at amortized `O(1)`.

##### Space Complexity: `O(n)`

The accepted-timestamp lists record each accepted request once.

#### Key Insights

- `bisect_left` replaces the baseline's counting loop; the algorithm (sorted history, count the window) is unchanged, only the lookup moves to the library.
- The integer boundary needs care: the window excludes `timestamp - 60`, so the first in-window value is `timestamp - 60 + 1`, and `bisect_left` (not `bisect_right`) is the probe that returns that position.
- No eviction happens at all: this version pays a logarithm per request to keep expired entries, which suits workloads that still need the full history later.

## Comparison of Solutions

### Time Complexity

- **Per-User History Scan**: `O(n^2)` worst case - every request rescans its user's whole accepted history.
- **Per-User Deque of Accepted Timestamps**: `O(n)` - each accepted timestamp is appended once and evicted at most once.
- **Per-User Sorted List with Bisect**: `O(n log n)` - one binary search per request over a sorted history.

### Space Complexity

- **Per-User History Scan**: `O(n)` - accepted-timestamp lists.
- **Per-User Deque of Accepted Timestamps**: `O(n)` - deques holding accepted timestamps.
- **Per-User Sorted List with Bisect**: `O(n)` - accepted-timestamp lists.

### Trade-offs

- The scan is the shortest to write and the slowest to run; its cost grows with history length, not with the window.
- The deque pays a small eviction loop to keep only live entries, which is the optimal shape for the streaming decision this problem asks for.
- The bisect variant never forgets: it keeps expired entries and pays one binary search per request, slower than the deque but the only version whose full history stays queryable.

### When to Use Each

- **Per-User History Scan**: as the baseline to state in an interview before improving it, or when histories are known to stay tiny.
- **Per-User Deque of Accepted Timestamps (Recommended)**: the interview answer: linear time, constant amortized work per request, and only live entries in memory.
- **Per-User Sorted List with Bisect**: when accepted history must remain queryable after expiry (audits, running totals) or when the language lacks an efficient deque.

### Optimization Notes

- Evicting before counting is what keeps the deque's length equal to the in-window count; counting first would need a separate tally.
- The boundary is off by one by design: the window `(timestamp - 60, timestamp]` excludes its left edge, so the deque evicts entries `<= timestamp - 60` while the bisect probe searches for `timestamp - 60 + 1`.
- In a real service the user map would be bounded (an LRU over users), since inactive users' deques otherwise live forever; the OA input bounds make that unnecessary here.
