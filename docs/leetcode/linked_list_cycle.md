# [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/)

**Easy** | **20 minutes** | **Linked List, Two Pointers**

**Pattern:** [Two Pointers](../patterns/two_pointers/intuition.md)

**Algorithm:** [Floyd's cycle detection](https://en.wikipedia.org/wiki/Cycle_detection) · [Hash table](https://en.wikipedia.org/wiki/Hash_table)

**Practice:** [`practice/linked_list_cycle/solution.py`](../../practice/linked_list_cycle/solution.py)

Given `head`, the head of a linked list, determine if the linked list has a cycle in it.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the `next` pointer. Internally, `pos` is used to denote the index of the node that tail's `next` pointer is connected to. **Note that `pos` is not passed as a parameter**.

Return `true` if there is a cycle in the linked list. Otherwise, return `false`.

## Examples

### Example 1

![Linked List Cycle Example 1](assets/linked_list_cycle_example1.png)

**Input:** `head = [3,2,0,-4]`, `pos = 1`

**Output:** `true`

**Explanation:** There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed).

### Example 2

![Linked List Cycle Example 2](assets/linked_list_cycle_example2.png)

**Input:** `head = [1,2]`, `pos = 0`

**Output:** `true`

**Explanation:** There is a cycle in the linked list, where the tail connects to the 0th node.

### Example 3

![Linked List Cycle Example 3](assets/linked_list_cycle_example3.png)

**Input:** `head = [1]`, `pos = -1`

**Output:** `false`

**Explanation:** There is no cycle in the linked list.

## Constraints

- The number of the nodes in the list is in the range `[0, 10^4]`.
- `-10^5 <= Node.val <= 10^5`
- `pos` is `-1` or a valid index in the linked-list.

## Deriving the Solution

A cycle shows itself in exactly one way: following `next` pointers revisits a node instead of reaching null. Every solution below is a different way of noticing that revisit.

1. **Start literal.** Do not detect the revisit at all: just walk, and if the
   walk outlives the largest list the constraints allow (`10^4` nodes), the pointers must be looping. Constant space, but the argument leans on a known size cap rather than on the list itself: see [Brute Force](#brute-force).
2. **Remember where you have been.** Detect the revisit directly: store every
   visited node in a set and stop the moment one repeats. Works for any list, but spends `O(n)` memory remembering the past: see [Hash Set](#hash-set).
3. **Store the memory in the list.** The set only records one bit per node,
   "visited"; write that bit into the nodes themselves as a sentinel value. Space drops to `O(1)`, but the caller's list is destroyed in the process: see [Marking Visited Nodes](#marking-visited-nodes).
4. **Race two pointers.** Replace memory with relative motion: a fast pointer
   gains one node per step on a slow one, so inside any cycle it must catch it, and on an acyclic list it simply runs off the end. Constant space, no mutation, no size cap: see [Floyd's Cycle Detection](#floyds-cycle-detection).

## Solutions

### Brute Force

#### Derivation

The most direct idea uses no extra data structure at all: just walk the list and count steps. A list without a cycle has at most `n` nodes, so following `next` pointers must reach a null terminator within `n` steps. If we keep walking past the largest list the constraints allow, the only explanation is that the pointers loop back on themselves.

1. Read the upper bound on the node count from the constraints (`10^4`) and use
   it as the step budget `MAX_NODES`.
2. Traverse the list one node at a time, incrementing the counter `steps`.
3. If `steps` ever exceeds the budget, declare a cycle; if traversal reaches
   null first, declare no cycle.

This is correct because the budget is the maximum possible chain length: any walk longer than that cannot be a simple acyclic chain.

#### Walkthrough

Tracing this brute force on Example 1 (`head = [3,2,0,-4]`, `pos = 1`) would take more than `10^4` steps before the `steps > MAX_NODES` budget triggers, far too many to follow by hand. So we trace the easier-to-watch acyclic case instead: the same four values `[3,2,0,-4]` but with `pos = -1`, meaning the tail's `next` is null and there is no cycle. This shows how the loop terminates normally and returns `false`.

We start with `steps = 0` and `head` pointing at the first node (value `3`). Each iteration checks the budget, then advances `head` to `head.next` and increments `steps`:

| `steps` (at loop top) | `head.val` | budget exceeded? | action |
| --- | --- | --- | --- |
| `0` | `3` | no (`0 > 10000` is false) | `head = head.next` (to `2`), `steps` becomes `1` |
| `1` | `2` | no | `head = head.next` (to `0`), `steps` becomes `2` |
| `2` | `0` | no | `head = head.next` (to `-4`), `steps` becomes `3` |
| `3` | `-4` | no | `head = head.next` (to `null`), `steps` becomes `4` |

Now `head` is `null`, so the `while head:` condition is false and the loop ends. The budget was never exceeded, so the method reaches the final line and returns `false`.

For this acyclic list the result is `false`. Example 1 itself has a cycle (`pos = 1`), so its `head` pointer would never reach `null`: the walk would keep looping back, the step counter would climb past `10000`, and the `steps > MAX_NODES` guard would return `true`, matching Example 1's expected Output of `true`.

#### Solution

The code is the walkthrough's counted walk, with the budget check at the top of each step.

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
from typing import Optional


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        MAX_NODES = 10**4
        steps = 0
        while head:
            # A cycle-free list of n nodes ends within n steps. The constraints
            # cap n at 10^4, so passing that many steps without reaching null
            # means we are revisiting nodes: a cycle.
            if steps > MAX_NODES:
                return True
            head = head.next
            steps += 1
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes. An acyclic list ends in at most `n` steps; a cyclic list is detected after at most `MAX_NODES + 1` steps, which is also `O(n)` since `n` is bounded by that constant.

##### Space Complexity: `O(1)`

Only a counter and the traversal pointer are kept, regardless of input size.

#### Key Insights

- The self-derivable observation: walking longer than the largest possible list means you must be going in circles.
- Needs no auxiliary structure and never mutates the list.
- The weakness is that it hard-codes a step bound from the constraints rather than reasoning about the list itself, so it does not generalize to inputs without a known size cap.

### Hash Set

#### Derivation

The Brute Force never actually observes a revisit; it infers a cycle from a size cap that only the constraints happen to provide, so it fails to generalize to lists of unknown size. Detect the revisit itself instead: a cycle exists exactly when the walk reaches some node a second time, so remember every node visited so far in a [hash set](https://en.wikipedia.org/wiki/Hash_table) and stop when one repeats. The set stores node objects, not values, so duplicate values in distinct nodes cannot cause a false positive.

1. Start with an empty set `seen`.
2. Walk the list; at each node, if `head` is already in `seen`, return `True`.
3. Otherwise add `head` to `seen` and advance to `head.next`.
4. Reaching null means the chain terminates, so return `False`.

#### Walkthrough

Trace the set on Example 1: `head = [3,2,0,-4]`, `pos = 1`. Label the four nodes `n0` through `n3` by position, since the set keys on node identity, not value; `pos = 1` means the tail `n3` points back to `n1`:

```text
visit n0 (val 3)     n0 not in seen -> seen = {n0}
visit n1 (val 2)     n1 not in seen -> seen = {n0, n1}
visit n2 (val 0)     n2 not in seen -> seen = {n0, n1, n2}
visit n3 (val -4)    n3 not in seen -> seen = {n0, n1, n2, n3}
visit n1 (val 2)     n1 in seen -> return True
```

Following `n3.next` lands back on `n1`, the node the tail connects to. The membership test recognizes the same object it added on the second step, and the function returns `True`, matching Example 1's expected Output.

#### Solution

The code is the walkthrough's check-then-add walk.

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
from typing import Optional


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        seen = set()
        while head:
            if head in seen:
                return True
            seen.add(head)
            head = head.next
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes in the linked list. In the worst case, we might need to visit all nodes once.

##### Space Complexity: `O(n)`

We store each node in the hash set, which in the worst case would contain all `n` nodes.

#### Key Insights

- Hash set provides `O(1)` lookups to quickly check if a node was seen before
- Simple implementation that's easy to understand
- The space complexity is proportional to the size of the list

### Marking Visited Nodes

#### Derivation

The hash set spends `O(n)` memory to remember a single bit per node: "visited". The list itself can carry that bit. Overwrite each visited node's value with a sentinel that no real node holds (`float('inf')` is safe here because the constraints bound values by `10^5`); encountering the sentinel again means the walk has come back around. The price is mutating the caller's list, which is not always permitted.

1. Walk the list from `head`.
2. If `head.val` equals the sentinel, this node was visited before, so return
   `True`.
3. Otherwise overwrite `head.val` with `float('inf')` and advance to
   `head.next`.
4. Reaching null means no node repeated, so return `False`.

#### Walkthrough

Trace the marking on Example 1: `head = [3,2,0,-4]`, `pos = 1`, with the nodes labeled `n0` through `n3` and the tail `n3` pointing back to `n1`:

```text
visit n0 (val 3)      not inf -> n0.val = inf, advance to n1
visit n1 (val 2)      not inf -> n1.val = inf, advance to n2
visit n2 (val 0)      not inf -> n2.val = inf, advance to n3
visit n3 (val -4)     not inf -> n3.val = inf, advance to n3.next = n1
visit n1 (val inf)    head.val == inf -> return True
```

When the walk wraps back to `n1`, the sentinel written on the second step is still there, so the check fires and the function returns `True`, matching Example 1's expected Output. Note that all four original values have been destroyed along the way.

#### Solution

The code is the walkthrough's check-then-mark walk.

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
from typing import Optional


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        while head:
            if head.val == float('inf'):
                return True
            head.val = float('inf')
            head = head.next
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes. We traverse the list once.

##### Space Complexity: `O(1)`

We don't use any extra data structures that scale with input size.

#### Key Insights

- Very space-efficient as it uses constant extra space
- Simple implementation
- The main drawback is that it modifies the original list, which may not be allowed in some scenarios

### Floyd's Cycle Detection

#### Derivation

Marking reaches `O(1)` space only by damaging the list. [Floyd's Cycle-Finding Algorithm](https://en.wikipedia.org/wiki/Cycle_detection), the "tortoise and hare", achieves `O(1)` space with the list untouched by replacing memory with relative motion: run two pointers from the head, `slow` advancing one step per iteration and `fast` advancing two. On an acyclic list `fast` simply reaches the end. Inside a cycle, `fast` gains on `slow` by exactly one node per iteration (`gap = (gap - 1) mod L`, where `L` is the cycle length), so the gap cannot skip past zero: the pointers must meet, and meeting is the proof of a cycle. The Invariant below states that argument formally, along with why `fast.next` reaching null is the correct no-cycle exit.

1. Start `slow = head` and `fast = head`.
2. Each iteration, advance `slow = slow.next` and `fast = fast.next.next`,
   guarded by `while slow and fast and fast.next` so both dereferences are safe.
3. If `slow == fast` after a step, return `True`.
4. If the guard fails, `fast` ran off the end of an acyclic chain: return
   `False`.

#### Invariant

Suppose the list contains a cycle of length \(L\). Once both pointers are inside that cycle, let \(d\) be the forward distance from `fast` to `slow` around it: the number of `next` steps `fast` still needs to take to land on `slow`, so \(0 \le d < L\). Each iteration moves `slow` one step forward (adding \(1\) to the gap) and `fast` two steps forward (subtracting \(2\)):

$$ d_{k+1} = (d_k + 1 - 2) \bmod L = (d_k - 1) \bmod L $$

```text
d[k + 1] = (d[k] + 1 - 2) mod L = (d[k] - 1) mod L
           where d[k] = forward distance from fast to slow after k iterations,
           0 <= d[k] < L, and L = cycle length
```

The gap closes by *exactly* one node per iteration, and that exactness is what makes the 2:1 ratio non-arbitrary rather than a convention. A quantity that decreases by one cannot step over zero, so the pointers can never pass each other unmet. Since \(d_0 < L\), the gap reaches \(0\) within \(L\) iterations, and \(d = 0\) is precisely the condition `slow == fast`. The `return True` is therefore forced after at most one cycle length of passes, which is where the `O(n)` bound comes from.

A faster hare does not lose the meeting, but it does lose this argument. With `fast` advancing three steps the gap changes by \(-2\) each pass, and a quantity falling by two can step over \(0\) instead of landing on it, so nothing about termination follows from the invariant alone. It still meets here, but only for reasons outside the invariant, and they differ by parity. When \(L\) is even, the entry offsets save it: both pointers start at the head, so `slow` enters the cycle after \(\mu\) steps with `fast` at in-cycle offset \(2\mu\), forcing \(d_0\) even, and a gap falling by two then lands on \(0\) rather than stepping over it. When \(L\) is odd, \(d_0\) is no longer forced even, so the gap can step over \(0\) and wrap, and meeting then rests on something else: \(2\) is invertible modulo an odd \(L\), so \((d_0 - 2k) \bmod L\) sweeps every residue and cannot avoid \(0\). At a 2:1 ratio neither argument is needed, which is the sense in which the ratio is not arbitrary.

The other exit is equally forced. Coincidence requires \(d = 0\) inside a cycle, so on an acyclic list the pointers can never meet and the loop can only end by its guard failing. `fast` and `fast.next` are exactly the two references that `fast = fast.next.next` dereferences, so the guard fails the moment the hare runs out of track ahead of it. A null `next` anywhere means the chain terminates, which means no node is reachable twice: `return False` is not a fallback but the correct reading of the invariant.

#### Walkthrough

Trace both pointers on Example 1: `head = [3,2,0,-4]`, `pos = 1`. Label the nodes `n0` through `n3`; the tail `n3` points back to `n1`, so the cycle is `n1 -> n2 -> n3 -> n1` with length `L = 3`:

```text
start    slow = n0 (val 3)     fast = n0 (val 3)
iter 1   slow = n1 (val 2)     fast = n2 (val 0)     slow != fast
iter 2   slow = n2 (val 0)     fast = n1 (val 2)     slow != fast   (fast wrapped: n3.next = n1)
iter 3   slow = n3 (val -4)    fast = n3 (val -4)    slow == fast -> return True
```

In iteration 2 the hare crosses the tail: from `n2` its two steps pass through `n3` and wrap along `n3.next` to `n1`. Both pointers are now inside the cycle, with the forward distance from `fast` (at `n1`) to `slow` (at `n2`) equal to `d = 1`. Iteration 3 closes that gap by exactly one, to `d = 0`: `slow` steps to `n3` while `fast` takes two steps `n1 -> n2 -> n3`, and the pointers coincide. The meeting at `n3` returns `True`, matching Example 1's expected Output.

#### Solution

The code is the walkthrough's two-pointer chase with the null guard.

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
from typing import Optional


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = head
        fast = head
        while slow and fast and fast.next:
            slow = slow.next          # advance slow by one step
            fast = fast.next.next     # advance fast by two steps
            if slow == fast:
                return True
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes. In the worst case with a cycle, the slow and fast pointers will meet after the slow pointer has traversed at most `n` steps.

##### Space Complexity: `O(1)`

We only use two pointers regardless of the input size.

#### Key Insights

- Uses constant extra space, making it more memory-efficient than the hash set approach
- Elegant mathematical solution that leverages the cycle property
- When pointers move at different speeds in a cycle, they'll eventually meet

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n)` - Walks until the step budget is exceeded or null is reached
- **Hash Set**: `O(n)` - Traverses the list once
- **Marking Nodes**: `O(n)` - Single traversal of the list
- **Floyd's Cycle Detection**: `O(n)` - Also traverses the list with slow and fast pointers

### Space Complexity

- **Brute Force**: `O(1)` - Only a counter and a pointer
- **Hash Set**: `O(n)` - Stores all nodes in a hash set
- **Marking Nodes**: `O(1)` - No additional data structures
- **Floyd's Cycle Detection**: `O(1)` - Uses only two pointers

### Trade-offs

- The brute force is the easiest to derive but relies on a hard-coded step bound from the constraints, so it does not generalize beyond inputs with a known size cap
- The hash set solution is intuitive and self-contained but uses more memory
- The marking approach is memory-efficient but modifies the original list
- The two-pointer solution is memory-efficient and doesn't modify the list

### When to Use Each

- **Brute Force**: As a teaching baseline that needs no extra structure, when a strict size cap is known
- **Hash Set**: When simplicity is valued over memory efficiency
- **Marking Nodes**: When memory efficiency is important and modifying the list is allowed
- **Floyd's Cycle Detection**: When memory efficiency is important and we can't modify the list

### Optimization Notes

- **Floyd's Cycle Detection is the optimal solution**: it achieves `O(n)` time and `O(1)` space while leaving the list untouched and never relying on an external size bound, combining the best properties of the other approaches
- The brute force is the easiest to reach without prior knowledge, but it leans on the `10^4` node cap from the constraints; the other three approaches reason about the list itself and stay correct for any size
- A key implementation detail is the loop guard `while slow and fast and fast.next`: the fast pointer advances two steps per iteration, so both `fast` and `fast.next` must be non-null before dereferencing `fast.next.next`, otherwise an empty or odd-length acyclic list raises an `AttributeError`
- Avoid the Marking Nodes approach unless mutation is explicitly permitted: overwriting `val` with `float('inf')` destroys the original data and produces a false positive if any legitimate node already held that sentinel value
- The Hash Set approach keys on node identity rather than value, so it correctly handles duplicate values; do not refactor it to store `head.val`, which would falsely report a cycle whenever two distinct nodes share the same value
