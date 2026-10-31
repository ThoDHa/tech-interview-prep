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

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
