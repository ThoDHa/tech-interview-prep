# [Lazy Merge of Sorted Event Streams](https://www.fastprep.io/problems/amazon-lazy-event-stream-merge)

**Medium** | **NN minutes** | **Heap, Sorting**

Implement a forward iterator that merges event streams from earliest timestamp to latest. Each stream is already sorted. Do not load all events into the memory used for merging.

For this exercise, assume each event is represented only by its integer timestamp. Every row of streams is sorted in nondecreasing order. Preserve every event, including equal timestamps within or across streams.

Keep only the current event from each nonempty stream ready for comparison. The iterator must tell the caller whether another event exists. When it returns the next timestamp, advance only the stream that supplied that event. Exhausted streams contribute no more events.

The function returns the complete iterator output as an int[] for judging. The already-supplied input handles and serialized output are excluded from the O(k) merge-working-memory limit, where k is the number of streams.

## Examples

### Example 1

**Input:** `streams = [[1,4,4],[1,2,9],[],[3]]`

**Output:** `[1,1,2,3,4,4,9]`

**Explanation:** Both timestamp-1 events and both timestamp-4 events remain in the merged sequence.

### Example 2

**Input:** `streams = [[],[-3,-1],[-3,0]]`

**Output:** `[-3,-3,-1,0]`

**Explanation:** Empty streams contribute nothing, and negative timestamps are ordered normally.

## Constraints

- `For this exercise, assume 0 <= streams.length <= 10000.`
- `Rows are sorted in nondecreasing order and may be empty.`
- `The total number of events is at most 200000.`
- `Every timestamp is a signed 32-bit integer.`
- `Merge working memory is O(k), excluding input handles and returned output.`

## Deriving the Solution

The statement pins the shape of the computation before it pins the output: each sorted stream is allowed to expose only its current event, every emission advances exactly the stream that supplied it, and the merge may hold `O(k)` working memory for `k` streams no matter how many events flow past. The output is forced anyway: the merged sequence is the multiset of all events in nondecreasing order, equal timestamps preserved wherever they sit. [Merge k Sorted Lists](../leetcode/merge_k_sorted_lists.md) runs the same smallest-head-first merge, but its inputs are whole linked lists the merger may walk freely and its output is one eagerly built list, while this statement's streams expose only their current event and pin the merge's working memory at `O(k)`. The ladder moves the merge from one array into `k` hands:

1. **Start literal.** Collect every event into one list and sort it: correct, and it loads everything at once, the one thing the statement forbids: see [Collect All and Sort](#collect-all-and-sort).
2. **Hold one head per stream.** A sorted stream offers its smallest unemitted event at its head, so each step only has to find the smallest head and advance that one stream: see [Head Scan Merge](#head-scan-merge).
3. **Let a heap watch the heads.** The scan re-finds the same minimum every step; a min-heap over the heads answers it in logarithmic time and keeps the working set at `k` entries: see [Min-Heap of Stream Heads](#min-heap-of-stream-heads).

## Solutions

### Collect All and Sort

#### Derivation

The most literal reading of the output: the merged sequence is every event, ordered. Concatenate the streams and sort:

1. Concatenate all rows of `streams` into one list.
2. Sort it ascending.
3. Return the list.

#### Walkthrough

Example 1 (`streams = [[1,4,4],[1,2,9],[],[3]]`):

```text
concatenate    [1, 4, 4, 1, 2, 9, 3]
sort           [1, 1, 2, 3, 4, 4, 9]
```

The sorted concatenation is `[1,1,2,3,4,4,9]`, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def mergeEventStreams(self, streams: List[List[int]]) -> List[int]:
        events = [timestamp for stream in streams for timestamp in stream]
        events.sort()
        return events
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N log N)`

One sort over all `N` events.

##### Space Complexity: `O(N)`

The concatenated list holds every event at once, which breaks the statement's `O(k)` merge-memory rule and disqualifies this form wherever the constraint is enforced.

#### Key Insights

- The output is the sorted multiset of events, so this one-liner is the oracle the other approaches are checked against.
- The statement's memory rule is about the merge, and this approach ignores it completely: it is the definition of what went wrong, written in two lines.
- Stability never matters here: equal timestamps are indistinguishable, so any comparison sort lands on the same sequence.

### Head Scan Merge

#### Derivation

Each stream is already sorted, so its smallest unemitted event is its head. Holding one cursor per stream is exactly the statement's contract: keep only the current event of every nonempty stream ready, emit the smallest head, and advance only the stream that supplied it:

1. Keep a cursor per stream, starting at column `0` of each nonempty row.
2. While any cursor is live: scan the live cursors and take the smallest head, breaking ties by stream index to make the scan deterministic.
3. Append that timestamp, advance that stream's cursor, and drop the stream when its row runs out.

#### Walkthrough

Example 1 (`streams = [[1,4,4],[1,2,9],[],[3]]`), the live heads before each step:

```text
step 1   heads (1, s0) (1, s1) (3, s3)   -> take s0   emit 1
step 2   heads (4, s0) (1, s1) (3, s3)   -> take s1   emit 1
step 3   heads (4, s0) (2, s1) (3, s3)   -> take s1   emit 2
step 4   heads (4, s0) (9, s1) (3, s3)   -> take s3   emit 3
step 5   heads (4, s0) (9, s1)           -> take s0   emit 4
step 6   heads (4, s0) (9, s1)           -> take s0   emit 4
step 7   heads (9, s1)                   -> take s1   emit 9
```

Stream 2 is empty from the start and never joins. The emissions read `[1,1,2,3,4,4,9]`, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def mergeEventStreams(self, streams: List[List[int]]) -> List[int]:
        cursors = {index: 0 for index, stream in enumerate(streams) if stream}
        merged_events = []

        while cursors:
            source = min(cursors, key=lambda index: (streams[index][cursors[index]], index))
            merged_events.append(streams[source][cursors[source]])
            cursors[source] += 1
            if cursors[source] == len(streams[source]):
                del cursors[source]

        return merged_events
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N * k)`

Every one of the `N` events requires a scan of at most `k` live heads.

##### Space Complexity: `O(k)`

One cursor per stream, the statement's own budget, plus the output.

#### Key Insights

- The head invariant is the whole idea: sortedness per row means nothing behind a head can be smaller, so heads are the only candidates.
- Empty streams simply never enter the cursor table; exhausted streams leave it the moment their last event is emitted.
- At the statement's bounds, `N <= 200000` and `k <= 10000`, the scan is up to two billion comparisons; the heap replaces exactly that factor.

### Min-Heap of Stream Heads

#### Derivation

The scan's repeated question, which live head is smallest, is a minimum priority queue query. Pushing every stream's head once and repairing with logarithmic pops and pushes keeps the working set at the statement's `O(k)` budget while the per-event cost drops from `k` to `log k`. Heap tuples are `(timestamp, stream_index, cursor)` so ties on timestamp break deterministically by stream index, and the value emitted is unaffected either way because tied timestamps are equal:

1. Build `(stream[0], index, 0)` for every nonempty stream and `heapq.heapify` it.
2. While the heap is nonempty: pop the smallest tuple, append its timestamp, and push `(streams[index][cursor + 1], index, cursor + 1)` when that stream still has events.
3. Return the appended timestamps.

#### Walkthrough

Example 1 (`streams = [[1,4,4],[1,2,9],[],[3]]`), the heap shown in sorted order for reading; the heap itself only guarantees the smallest at the root:

```text
seed              heap = [(1, 0, 0), (1, 1, 0), (3, 3, 0)]
pop (1, 0, 0)     emit 1   push (4, 0, 1)
pop (1, 1, 0)     emit 1   push (2, 1, 1)
pop (2, 1, 1)     emit 2   push (9, 1, 2)
pop (3, 3, 0)     emit 3   stream 3 exhausted
pop (4, 0, 1)     emit 4   push (4, 0, 2)
pop (4, 0, 2)     emit 4   stream 0 exhausted
pop (9, 1, 2)     emit 9   stream 1 exhausted, heap empty
```

The emissions read `[1,1,2,3,4,4,9]`, matching the expected Output.

#### Solution

```python
import heapq
from typing import List


class Solution:
    def mergeEventStreams(self, streams: List[List[int]]) -> List[int]:
        stream_heads = [
            (stream[0], index, 0)
            for index, stream in enumerate(streams)
            if stream
        ]
        heapq.heapify(stream_heads)

        merged_events = []
        while stream_heads:
            timestamp, index, cursor = heapq.heappop(stream_heads)
            merged_events.append(timestamp)
            next_cursor = cursor + 1
            if next_cursor < len(streams[index]):
                heapq.heappush(
                    stream_heads, (streams[index][next_cursor], index, next_cursor)
                )
        return merged_events
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N log k)`

Every one of the `N` events pops once and pushes at most once from a heap that never holds more than `k` entries; the seeding is one `heapify`.

##### Space Complexity: `O(k)`

The heap holds one head per nonempty stream, the statement's merge budget, plus the output.

#### Key Insights

- This is the statement's iterator contract written as a loop: the heap entries are exactly the "current event of each nonempty stream", and each pop advances only the stream that supplied the event.
- Empty rows are filtered at seeding, so the `k` in the complexity is the count of streams that ever hold an event, never worse than the row count.
- Equal timestamps survive in every copy because each copy lives in its own stream and leaves through its own pop; no comparison ever needs to distinguish them.

## Comparison of Solutions

### Time Complexity

- **Collect All and Sort**: `O(N log N)` - one sort over everything.
- **Head Scan Merge**: `O(N * k)` - one full head scan per event.
- **Min-Heap of Stream Heads**: `O(N log k)` - one logarithmic pop and push per event.

### Space Complexity

- **Collect All and Sort**: `O(N)` - all events held at once.
- **Head Scan Merge**: `O(k)` - one cursor per nonempty stream.
- **Min-Heap of Stream Heads**: `O(k)` - one head per nonempty stream.

### Trade-offs

- **Collect All and Sort**: the definition, usable as the oracle; it breaks the statement's `O(k)` merge-memory rule.
- **Head Scan Merge**: no library and no heap invariant to trust, at a per-event cost that grows with the stream count.
- **Min-Heap of Stream Heads**: the same merge with the scan replaced by a log-time query; at `k <= 10000` the log is about fourteen comparisons per event.

### When to Use Each

- **Collect All and Sort**: as the independent checker for the other two, and as the answer only where the memory rule does not apply.
- **Head Scan Merge**: when asked to merge without a heap; it exposes the head structure the heap exploits.
- **Min-Heap of Stream Heads (Recommended)**: the interview default on this statement: the statement describes it, `O(N log k)` time inside `O(k)` memory.

### Optimization Notes

- **Min-Heap of Stream Heads** is the recommended choice: at the statement's bounds (`k <= 10000` streams, `N <= 200000` events) it is about three million comparisons against the scan's up to two billion.
- `streams` itself may be empty (`0 <= streams.length`), and the loop over an empty heap returns `[]` without a special case.
- Timestamps span the full signed 32-bit range; comparisons are exact in Python, but in fixed-width languages the heap tuple is the place a widening rule would matter.
- A lazy iterator over these heads would expose `has_next` and `next` as the heap's emptiness check and pop; the judge shape here drains the iterator into one list, which is why the loop appends instead of yielding.
