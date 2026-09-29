# Linked List In-Place Reversal: Building Intuition

**Reference:** [Linked list](https://en.wikipedia.org/wiki/Linked_list)

> **Core Insight**: Reverse direction by changing where arrows point, not by moving data.

---

## The Mental Model: Flipping Train Cars

Imagine a train where each car has a coupler pointing to the next car:

```
Engine → Car1 → Car2 → Car3 → Caboose → (nothing)
```

To reverse the train, you don't physically move the cars. Instead, you **flip the direction of each coupler**:

```
(nothing) ← Engine ← Car1 ← Car2 ← Car3 ← Caboose
```

The Caboose becomes the new Engine (new head), and the original Engine points to nothing (new tail).

### The Three-Pointer Dance

At each step, you work with three positions:

```
             previous    current    next_node
                ↓           ↓           ↓
(reversed) ← [ A ] <- [ B ] -> [ C ] -> (to process)

Action:
1. Save next_node = current.next (or we lose C forever!)
2. Flip: current.next = previous (B now points backward to A)
3. Advance previous = current (previous moves to B)
4. Advance current = next_node (current moves to C)
```

It's like a caterpillar inching forward while flipping tracks behind it.

---

## Visual Intuition: The Domino Effect

### Full List Reversal (LC 206)

Think of dominoes standing in a row. To reverse them, you tip each one backward instead of forward:

```
Step 0: Stand behind first domino
        ●→●→●→●→●→ (all pointing right)

Step 1: Tip first one left (into empty space)
        ←● ●→●→●→●→

Step 2: Tip second one into first
        ←●←● ●→●→●→

Step 3: Continue...
        ←●←●←● ●→●→

Step 4: ...until done
        ←●←●←●←●←●
```

The last domino becomes the "head" of the reversed sequence.

### Segment Reversal (LC 92)

Same idea, but you only flip dominoes in a specific range:

```
Original:    ●→●→●→●→●→● (positions 1-6)
Reverse 2-4: ●→ ←●←●←● →●→●

You need to:
1. Walk to position 1 (before the segment)
2. Remember this anchor point
3. Flip dominoes 2,3,4
4. Reconnect: anchor→4, and 2→5
```

### K-Group Reversal (LC 25)

Like reversing sections of a marching band, k musicians at a time:

```
Original (k=2):  [1,2] [3,4] [5]
After groups:    [2,1] [4,3] [5]

For each group:
1. Check: are there k musicians available?
2. If yes: flip their order
3. If no: leave them (the lonely 5 stays)
4. Move to next group
```

---

## Why Three Pointers?

Consider reversing just one link without helpers:

```python
# WRONG - we lose access to the rest!
current.next = previous   # Oops, where's the next node?
```

The moment you flip `current.next`, you've severed the connection to everything after `current`. That's why you MUST save `current.next` first:

```python
# CORRECT
next_node = current.next   # Save the bridge before burning it
current.next = previous    # Now safe to flip
```

This is the most common bug in reversal problems!

---

## The Dummy Node Trick

When you might change the first node, anchor to a fake "pre-head":

```
Without dummy (dangerous when left=1):
    head → [ ] → [ ] → [ ]
    What do we return if head changes?

With dummy (safe):
    dummy → head → [ ] → [ ]
    dummy.next is always the true head, even after changes!
```

Rule of thumb: **If the head might move, use a dummy.**

---

## Segment Reversal: The Bookmark Pattern

For reversing a middle portion, think of bookmarking a book:

```
Book (list):    [ Cover | Pages 1-5 | Pages 6-10 | Pages 11-15 | Back ]

To reverse pages 6-10:
1. Put bookmark BEFORE page 6 (after page 5)
2. Take out pages 6-10
3. Reverse them: 10-9-8-7-6
4. Reinsert: bookmark → page 10, and page 6 → page 11
```

In code:
- `before_segment` = the bookmark (node before left)
- `segment_start` = first page to reverse (becomes tail after)
- `previous` after reversal = last page reversed (becomes head)
- `current` after reversal = first page NOT reversed (page 11)

---

## K-Group: The Assembly Line

Imagine a factory assembly line with stations processing k items at a time:

```
Conveyor belt:  [1][2][3][4][5][6][7]

Station 1 (k=3): Take [1][2][3], reverse to [3][2][1], pass on
Conveyor belt:  [3][2][1][4][5][6][7]

Station 2 (k=3): Take [4][5][6], reverse to [6][5][4], pass on
Conveyor belt:  [3][2][1][6][5][4][7]

Station 3 (k=3): Only [7] left (< 3), leave as-is
Final:          [3][2][1][6][5][4][7]
```

The key insight: **check availability BEFORE processing each group**.

---

## Fast and Slow Pointers: The Other Pointer Dance

Reversal rewires the train. A sibling family of linked-list problems asks a different question: *what is happening further down the track?* You could walk the train twice (once to count, once to stop at the right car), or you can send two travelers down the track at different speeds and let their spacing do the measuring.

### The Invariant: The Gap Does the Measuring

Slow moves one car per step; fast moves two. That single difference carries everything:

- On a **straight track**, fast falls off the end while slow stands at the middle. Fast travels twice the distance, so slow has traveled exactly half.
- On a **circular track**, fast eventually laps slow. Once both are inside the cycle, the gap closes by exactly one car per step (fast gains only 1, since slow is also moving). A finite cycle cannot dodge a gap that shrinks by one: a collision is inevitable.

> **The promise**: whatever the problem asks for (a cycle, a midpoint, a cycle's entrance) can be read off the moment fast runs out of track or collides with slow. No counting pass, no extra memory, O(1) space.

### Use 1: Cycle Detection (LC 141, Grind 75 #12)

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        return True    # fast lapped slow inside the cycle
return False           # fast fell off the end: straight track
```

If a cycle exists, slow always enters it before fast exits the list, and from that moment the closing gap guarantees a meeting.

### Use 2: Middle of the Linked List (LC 876, Grind 75 #22)

Same dance, minus the comparison. When fast reaches the end, slow stands at the middle:

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
return slow    # second-middle convention when the length is even
```

Watch the parity: with `while fast and fast.next`, an even-length list leaves slow on the **second** of the two middle nodes. If the first middle is wanted, loop on `while fast.next and fast.next.next` instead (guard the empty list first: this variant dereferences `fast.next` immediately).

### Use 3: Floyd's Cycle Start

Detecting the cycle is half the job; some problems want the node where the cycle begins. Phase 1 is the collision above. Phase 2 exploits the arithmetic of the meeting point:

```
head ──── a ────▶ cycle entrance ──── c ────▶ meeting point
                     ▲                          │
                     └──── n - c (loop is n) ───┘
```

Say the head is `a` steps before the entrance, and the pointers meet `c` steps past it. At the meeting:

- slow has traveled `a + c`
- fast has traveled `2(a + c)`, and fast's extra distance is whole laps: `2(a + c) = a + c + k·n`

So `a + c = k·n`, which means `a = k·n - c`: the distance from head to the entrance equals the distance from the meeting point to the entrance, plus whole laps (which land on the same node). Two same-speed walkers starting from head and meeting point therefore converge exactly at the entrance:

```python
# meet = the collision node from Use 1
slow = head
while slow != meet:
    slow = slow.next
    meet = meet.next
return slow    # the cycle start
```

### Why This Lives Next to Reversal

The same discipline as the three-pointer dance: a fixed number of pointer variables, O(n) time, O(1) space, and an invariant you can state in one sentence. Fast/slow is the *measuring* counterpart of reversal's *rewiring*. The [Two Pointers guide](../two_pointers/intuition.md) lists the same shape among its six (Shape 3, the tortoise and the hare); this section is the full derivation.

---

## Common Pitfalls & Fixes

### Pitfall 1: Losing the Next Node
```python
# WRONG
current.next = previous
current = current.next  # Oops, current.next is now previous!

# FIXED
next_node = current.next
current.next = previous
current = next_node
```

### Pitfall 2: Returning Wrong Head
```python
# WRONG
return head  # head is still the original first node (now tail)

# FIXED
return previous  # previous is the new head after loop ends
```

### Pitfall 3: Off-By-One in Segment
```python
# WRONG: Starting from head when left=2
for _ in range(left):  # Goes one too far!
    before = before.next

# FIXED: Navigate left-1 times from dummy
for _ in range(left - 1):
    before = before.next
```

### Pitfall 4: Forgetting Reconnection
```python
# WRONG: Reversed segment is now floating!
# ... reversal code ...
return dummy.next  # Lost connection!

# FIXED: Reconnect both ends
segment_start.next = current        # old head → after segment
before_segment.next = previous      # before → new head
```

### Pitfall 5: Advancing Fast Without Checking the Road Ahead
```python
# WRONG: fast.next.next dereferences before the loop rechecks
while fast:
    slow = slow.next
    fast = fast.next.next   # Crashes when fast.next is null

# FIXED
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
```

---

## Corner Cases

- Empty list or single node: the loop bodies must be guarded so they simply never run
- Two nodes: the smallest input that rotates all three pointers fully
- Segment of one node (left == right) or a segment starting at the head (left == 1): only the head-starting case strictly requires the dummy node
- A trailing k-group shorter than k: the availability check leaves it un-reversed and in order
- A cycle that is the entire list (tail points at head): fast laps inside immediately and still collides with slow
- Even-length midpoint: slow lands on the second middle; the alternate loop condition moves it to the first
- Stepping fast twice per loop: fast.next.next is touched only after fast and fast.next both exist

---

## Complexity Guarantees

| Variant | Time | Space | Key Factor |
|---------|------|-------|------------|
| Full Reversal | O(N) | O(1) | Visit each node once |
| Segment Reversal | O(N) | O(1) | Navigate + reverse subset |
| K-Group Reversal | O(N) | O(1) | Each node: 1 count + 1 reverse |
| Fast/Slow (cycle, midpoint, cycle start) | O(N) | O(1) | Fixed two-pointer gap |
| Recursive Variants | O(N) | O(N) or O(N/k) | Call stack depth |

The iterative versions are strictly O(1) space because we only use a fixed number of pointer variables, regardless of input size.

---

## Practice Progression

1. **[Reverse Linked List (LC 206)](../../problems/reverse_linked_list.md)**: the full three-pointer dance on the whole list. Master this first.
2. **Reverse Linked List II (LC 92)**: segment reversal. Add the dummy node and the bookmark reconnection.
3. **[Reverse Nodes in k-Group (LC 25)](../../problems/reverse_nodes_in_k_group.md)**: repeated segment reversal, with an availability check before each group.
4. **[Linked List Cycle (LC 141, Grind 75 #12)](../../problems/linked_list_cycle.md)**: fast/slow cycle detection; the lap-and-collide argument in action.
5. **[Middle of the Linked List (LC 876, Grind 75 #22)](../../problems/middle_of_the_linked_list.md)**: the same gap used as a measuring tape; when fast exits, slow stands at the middle.

---

## Pattern Recognition Checklist

When you see a linked list problem, ask:

1. **Does it mention "reverse"?** → This pattern
2. **"Without extra space"?** → Must be in-place (not array copy)
3. **"Swap adjacent pairs"?** → K-group with k=2
4. **"Reverse between positions"?** → Segment reversal
5. **"Reverse every k nodes"?** → K-group reversal
6. **"Detect a cycle" or "find the middle"?** → Fast/slow pointers (the other pointer dance above)

If yes to any, reach for the three-pointer technique!


