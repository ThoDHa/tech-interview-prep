# Interval Patterns: Mental Models & Intuition

**Reference:** [Interval scheduling](https://en.wikipedia.org/wiki/Interval_scheduling)

> Build deep understanding of when and why interval patterns work.

## The Core Insight

**Intervals on a timeline are like segments on a number line.** The key operations are:

1. **Merging**: Combining overlapping segments into one
2. **Selecting**: Choosing maximum non-overlapping segments
3. **Intersecting**: Finding common regions between segments

The magic of interval problems lies in **sorting**:
- Sort by start → overlapping intervals become adjacent
- Sort by end → enables greedy selection

---

## Mental Model 1: The Timeline View

Visualize intervals as horizontal bars on a timeline:

```
Time:  0  1  2  3  4  5  6  7  8  9  10
       |--|--|--|--|--|--|--|--|--|--|
A:     [--------]
B:           [--------]
C:                       [--]
D:                             [-----]

A = [0,3]   B = [2,5]   C = [6,7]   D = [8,10]
```

**Key questions:**
- Which bars overlap? (A and B)
- Which bars can coexist? (A and C, or B and D)
- Where do bars intersect? (A∩B = [2,3])

---

## Mental Model 2: Sort Strategy Selection

### Sort by Start (for Merging)

```
Why: After sorting by start, overlapping intervals are ADJACENT.

Before sort: [3,5], [1,4], [2,6]
After sort:  [1,4], [2,6], [3,5]
              ↑      ↑      ↑
              All adjacent overlaps visible!
```

**Use for:** Merging, inserting, combining

### Sort by End (for Scheduling)

```
Why: Ending earlier = more room for future intervals.

Intervals:   [1,3], [2,4], [3,5]
Greedy:      Pick [1,3] first (ends earliest)
             Skip [2,4] (overlaps)
             Pick [3,5] (starts at 3, prev ends at 3)
Result:      2 non-overlapping intervals
```

**Use for:** Max selection, min removal, counting groups

### Memory Aid

```
"Start for Stack, End for Earnings"
- Sort by START when STACKING (merging) intervals
- Sort by END when EARNING (maximizing) selections
```

---

## Mental Model 3: Overlap Detection

Two intervals [a,b] and [c,d] overlap if and only if:
```
NOT (b < c OR d < a)
= a <= d AND c <= b
```

Visual:
```
Overlap:     [a----b]
               [c----d]
No overlap:  [a----b]
                      [c----d]
```

**After sorting by start** (c >= a guaranteed):
```
Simplified: c <= b  (current starts before previous ends)
```

---

## Mental Model 4: The Three-Phase Pattern

For insertion problems, think in **three phases**:

```
Phase 1: BEFORE   [====]  [====]  |  newInterval  |  [====]
Phase 2: MERGE    [====]  [====]  |←===overlap===→|
Phase 3: AFTER    [====]  [====]  |  (merged)     |  [====]
```

This works because the input is already sorted. That sortedness buys a refinement too: you can locate the overlap window with binary search in O(log n) before the O(n) rebuild (the Insert Interval problem page walks through this).

---

## Mental Model 5: Greedy Proof Intuition

**Why does "pick earliest ending" work?**

```
Claim: Greedy selection by end time is optimal.

Proof intuition:
- Suppose we pick interval X instead of Y (X ends later)
- Any interval compatible with X is also compatible with Y
- But Y might be compatible with more intervals (ends earlier)
- Therefore, Y is at least as good as X

Greedy choice: Always safe to pick earliest-ending interval.
```

---

## Pattern Recognition Checklist

| Signal Words | Pattern | Sort By |
|-------------|---------|---------|
| "merge", "combine", "union" | Interval Merge | Start |
| "insert into sorted" | Three-Phase | (Already sorted) |
| "minimum removal" | Scheduling | End |
| "maximum non-overlapping" | Scheduling | End |
| "minimum arrows/points" | Group Counting | End |
| "intersection", "common" | Two-Pointer | (Both sorted) |

---

## Common Pitfalls

### Pitfall 1: Wrong Sort Key

```python
# WRONG for scheduling:
intervals.sort(key=lambda x: x[0])  # Sort by start

# CORRECT for scheduling:
intervals.sort(key=lambda x: x[1])  # Sort by end
```

### Pitfall 2: Off-by-One in Overlap Check

```text
# "Touching" intervals - problem dependent!
# [1,2] and [2,3]: Do they overlap?

# LC 56 (Merge): YES - they touch, so merge
if current[0] <= previous[1]:  # <= means touching merges

# LC 435 (Scheduling): Depends on definition
if current[0] >= previous[1]:  # >= means touching is OK
```

### Pitfall 3: Not Using max() for Merge

```python
# WRONG:
merged[-1][1] = current[1]  # What if current is nested?

# CORRECT:
merged[-1][1] = max(merged[-1][1], current[1])

# Example: [1,10] + [2,5] should give [1,10], not [1,5]
```

---

## Corner Cases

- Touching intervals ([1,2] and [2,3]): merging problems combine them, scheduling problems keep them apart; the boundary convention is the problem
- Empty input or a single interval: the merge result is a copy of the input, not an error
- Fully nested intervals ([2,3] inside [1,10]): extend with max(prev_end, curr_end), never a blind overwrite
- Insert interval landing before the first, after the last, or spanning many: each of the three phases gets exercised
- Zero-length intervals ([5,5]): legal endpoints; the overlap test must survive an empty span
- Sorted versus unsorted input: insert problems get sortedness for free, merge problems must sort first
- Intersecting two lists of very different lengths: pointers advance by the smaller end; either list can empty out first

---

## Complexity Analysis Framework

| Operation | Complexity | Reason |
|-----------|------------|--------|
| Sort intervals | O(n log n) | Comparison-based sort |
| Single pass (merge/select) | O(n) | Each interval visited once |
| Two-pointer intersection | O(m + n) | Each pointer moves forward only |
| **Total** | O(n log n) | Dominated by sorting |

Space is typically O(n) for the output array, O(1) additional.

---

## Practice Progression

### Level 1: Core Patterns
1. **[LC 56 - Merge Intervals](../../problems/merge_intervals.md)** (Merge, Sort by start)
2. **[LC 435 - Non-overlapping Intervals](../../problems/non_overlapping_intervals.md)** (Schedule, Sort by end)

### Level 2: Variants
3. **[LC 57 - Insert Interval](../../problems/insert_interval.md)** (Three-phase)
4. **LC 452 - Minimum Arrows** (Group counting)

### Level 3: Two Lists
5. **LC 986 - Interval List Intersections** (Two-pointer)

### Level 4: Advanced
6. **[LC 253 - Meeting Rooms II](../../problems/meeting_rooms_ii.md)** (Concurrent intervals)
7. **[LC 1235 - Maximum Profit in Job Scheduling](../../problems/maximum_profit_in_job_scheduling.md)** (Weighted scheduling)

---

## Quick Reference Card

```
┌───────────────────────────────────────────────────────────────────────┐
│                  INTERVAL PATTERNS                                    │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  MERGE (LC 56)               SCHEDULE (LC 435, 452)                   │
│  ─────────────────           ──────────────────────                   │
│  Sort by: START              Sort by: END                             │
│  Action:  Extend end         Action:  Count/Skip                      │
│  Check:   current[0]<=previous[1]   Check:   current[0]>=previous[1]  │
│                                                                       │
│  INTERSECT (LC 986)                                                   │
│  ──────────────────                                                   │
│  Two pointers: i, j                                                   │
│  Intersection: [max(starts), min(ends)]                               │
│  Advance: pointer with smaller end                                    │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

LC 57 (Insert Interval) uses the merge check but needs no sort: the input is already sorted, so a single linear three-phase pass suffices.
