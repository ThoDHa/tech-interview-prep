# [Stack with Constant-Time Middle Queries](https://www.fastprep.io/problems/amazon-middle-stack-operations)

**Medium** | **NN minutes** | **Array, Stack, Design, Simulation**

Process a sequence of stack operations. Each operation is ["push", value], ["pop"], ["top"], or ["middle"]. Values are signed decimal integers encoded as strings.

Return one string for every non-push operation. For an empty stack, return EMPTY. For an even-sized stack, middle returns the lower middle element, the one closer to the bottom. Every operation must run in constant time; preallocated array storage is allowed.

## Examples

### Example 1

**Input:** `operations = [["push","1"],["push","2"],["push","3"],["middle"],["top"],["pop"],["middle"]]`

**Output:** `["2","3","3","1"]`

**Explanation:** The lower middle of three values is 2; after popping 3, the lower middle of [1,2] is 1.

### Example 2

**Input:** `operations = [["top"],["middle"],["pop"]]`

**Output:** `["EMPTY","EMPTY","EMPTY"]`

**Explanation:** All three queries use the empty sentinel.

### Example 3

**Input:** `operations = [["push","-4"],["middle"],["pop"]]`

**Output:** `["-4","-4"]`

**Explanation:** A one-element stack has the same top and middle.

## Constraints

- `1 ≤ operations.length ≤ 100000.`
- `Every operation has one of the four documented forms.`
- `Push values are integers in [-10^9, 10^9].`
- `The output contains one entry for every non-push operation.`

## Solutions

### Array with Index Formula

#### Derivation

The most direct reading: keep a [list](https://en.wikipedia.org/wiki/Dynamic_array) `values`, push with `append`, pop with `pop()`, and answer `top` and `middle` by indexing. The index arithmetic is the only subtlety. With `count` elements, `top` is `values[-1]`. The middle query must read the exact center for odd sizes and the lower of the two center slots for even sizes; counting from the bottom, Example 1's `[1, 2]` has middle `1`, at index `0`, and its `[1, 2, 3]` has middle `2`, at index `1`. Both fit one formula, `middle_position = (count - 1) // 2`. The trick the formula exploits is that the requested middle is *bottom-anchored*: elements above it never shift it, so a plain array index answers the query:

1. Keep `values` and `results`.
2. On `push`, convert the payload with `int` and `append` it.
3. On `pop`, append `"EMPTY"` when `values` is empty, else `str(values.pop())`.
4. On `top`, append `"EMPTY"` when empty, else `str(values[-1])`.
5. On `middle`, append `"EMPTY"` when empty, else
   `str(values[(len(values) - 1) // 2])`.

#### Walkthrough

Example 1, shown as the state after each operation finishes. `count` is the stack size and `middle_position = (count - 1) // 2` the index the middle query reads:

```text
push 1     values = [1]                    count 1
push 2     values = [1, 2]                 count 2
push 3     values = [1, 2, 3]              count 3
middle     middle_position = (3-1)//2 = 1  values[1] = 2   -> "2"
top        values[-1] = 3                  -> "3"
pop        removes 3                       values = [1, 2] -> "3"
middle     middle_position = (2-1)//2 = 0  values[0] = 1   -> "1"
```

The decisive row is the final `middle`: with two elements the formula picks index `0`, the lower of the two center slots, which is exactly the element closer to the bottom. The collected returns are `["2", "3", "3", "1"]`, matching the expected Output. Example 3 exercises the one-element stack: `count = 1` puts the formula at index `0`, so `middle` and `top` both read `-4`.

#### Solution

The code is the walkthrough's dispatch loop with the index formula from the trace.

```python
from typing import List


class Solution:
    def processMiddleStack(self, operations: List[List[str]]) -> List[str]:
        values: List[int] = []
        results: List[str] = []
        for operation in operations:
            action = operation[0]
            if action == "push":
                values.append(int(operation[1]))
            elif action == "pop":
                if not values:
                    results.append("EMPTY")
                else:
                    results.append(str(values.pop()))
            elif action == "top":
                if not values:
                    results.append("EMPTY")
                else:
                    results.append(str(values[-1]))
            else:
                if not values:
                    results.append("EMPTY")
                else:
                    middle_position = (len(values) - 1) // 2
                    results.append(str(values[middle_position]))
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity

- **push**: `O(1)` amortized - list append resizes geometrically.
- **pop**: `O(1)` - removal at the back.
- **top**: `O(1)` - direct index read.
- **middle**: `O(1)` - direct index read; no shifting is ever required because the lower middle is bottom-anchored.

For `m` operations this is `O(m)` overall.

##### Space Complexity: `O(u)`

`values` holds the `u` elements present at peak; `results` accumulates one string per non-push operation.

#### Key Insights

- The requested middle never moves when elements are added or removed above it: a bottom-anchored array index answers the query in constant time with no reordering.
- The parity-free formula `(count - 1) // 2` reads the exact center for odd sizes and the lower center for even sizes; checking it against `[1, 2] -> 1` and `[1, 2, 3] -> 2` fixes the off-by-one on both parities at once.
- The requirement is per-operation constant time, which this version already meets; what it lacks is a reusable design, and the two versions below are what the follow-up has in mind.
- `pop` and `top` on the empty stack share the `"EMPTY"` sentinel, and `push` never reports.

### Doubly Linked List with Middle Pointer

#### Derivation

The array version answers in constant time, so the honest question is what structure expresses the *design* the problem teaches: every operation in `O(1)` worst case, with no amortization asterisk and no capacity resizing. A [doubly linked list](https://en.wikipedia.org/wiki/Doubly_linked_list) gives push and pop at the top in constant pointer work, and one extra pointer finishes the job: `middle`, aimed at the lower-middle node, plus a `count`. Each operation perturbs the center by exactly one position, so `middle` moves at most one hop. Sentinels `head` and `tail` bracket the list so the ends need no special cases.

The parity bookkeeping is where the care goes. With `count` elements, the lower middle is the node at index `(count - 1) // 2` from the bottom. A push to an odd count moves that index one step up (the new node *is* the odd-size center), so `middle = middle.next_node`; a push to an even count leaves the index unchanged. A pop is the mirror image: a pop to an even count moves the index one step down, so `middle = middle.prev_node`; a pop to an odd count leaves it in place. Both rules follow from the one formula: advance `middle` exactly when the new count is odd:

1. Keep the `head`/`tail` sentinels, `middle` (starting at `head`), and
   `count = 0`.
2. `push(value)`: insert a node just before `tail`, increment `count`, and
   advance `middle` when the new `count` is odd.
3. `pop()`: when `count` is zero report `EMPTY`; otherwise unlink
   `tail.prev_node`, decrement `count`, and retreat `middle` when the new
   `count` is even.
4. `top()` reads `tail.prev_node`'s value and `middle()` reads `middle`'s
   value; both return `"EMPTY"` when `count` is zero.
5. Collect one string per non-push operation into `results`.

#### Walkthrough

Example 1, with the list read bottom to top and `middle` marked at its node:

```text
push 1   count 0 -> 1 (odd):  middle advances off head, onto node 1
         head <-> 1 <-> tail                  middle = 1
push 2   count 1 -> 2 (even): middle stays
         head <-> 1 <-> 2 <-> tail            middle = 1
push 3   count 2 -> 3 (odd):  middle advances 1 -> 2
         head <-> 1 <-> 2 <-> 3 <-> tail      middle = 2
middle   reads node 2   -> "2"
top      reads tail.prev_node = 3   -> "3"
pop      unlinks 3, count 3 -> 2 (even): middle retreats 2 -> 1
         head <-> 1 <-> 2 <-> tail            middle = 1
middle   reads node 1   -> "1"
```

The decisive event is the `pop`: with three elements `middle` sits on the exact center `2`, but the two-element stack `[1, 2]` demands the lower slot `1`, so the retreat fires. The collected returns are `["2", "3", "3", "1"]`, matching the expected Output. Example 3 exercises the first push: `count` reaching `1` (odd) advances `middle` off the `head` sentinel onto the new node, and both `middle` and `top` read `-4`.

#### Solution

The code is the dispatch loop with the advance-when-odd rule from the walkthrough embedded in `push` and `pop`.

```python
from typing import List, Optional


class Node:
    def __init__(self, value: int = 0) -> None:
        self.value = value
        self.prev_node: Optional["Node"] = None
        self.next_node: Optional["Node"] = None


class Solution:
    def processMiddleStack(self, operations: List[List[str]]) -> List[str]:
        head = Node()
        tail = Node()
        head.next_node = tail
        tail.prev_node = head
        middle: Optional[Node] = head
        count = 0
        results: List[str] = []

        def push(value: int) -> None:
            nonlocal middle, count
            node = Node(value)
            last_node = tail.prev_node
            node.prev_node = last_node
            node.next_node = tail
            last_node.next_node = node
            tail.prev_node = node
            count += 1
            if count % 2 == 1:
                middle = middle.next_node

        def pop() -> Optional[int]:
            nonlocal middle, count
            if count == 0:
                return None
            node = tail.prev_node
            last_node = node.prev_node
            last_node.next_node = tail
            tail.prev_node = last_node
            count -= 1
            if count % 2 == 0:
                middle = middle.prev_node
            return node.value

        for operation in operations:
            action = operation[0]
            if action == "push":
                push(int(operation[1]))
            elif action == "pop":
                popped = pop()
                results.append("EMPTY" if popped is None else str(popped))
            elif action == "top":
                if count == 0:
                    results.append("EMPTY")
                else:
                    results.append(str(tail.prev_node.value))
            else:
                if count == 0:
                    results.append("EMPTY")
                else:
                    results.append(str(middle.value))
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity

- **push**: `O(1)` worst case - four pointer writes plus at most one `middle` hop.
- **pop**: `O(1)` worst case - two pointer writes plus at most one `middle` hop.
- **top**: `O(1)` - one dereference through the tail sentinel.
- **middle**: `O(1)` - one dereference.

For `m` operations this is `O(m)` worst case, with no amortized resizing.

##### Space Complexity: `O(u)`

One `Node` per element present at peak, plus the two sentinels and `results`.

#### Key Insights

- One extra pointer turns the problem into ordinary stack code: `middle` moves at most one hop per operation because push and pop perturb the center by exactly one position.
- The parity rule is one sentence, advance `middle` exactly when the count is odd; applied after a push it is `middle.next_node`, after a pop it is `middle.prev_node`, and the even outcomes leave it in place.
- Sentinels make the first push (middle advancing off `head`) and the last pop work without special cases.
- Empty-stack handling differs by operation: `pop` must return without touching `middle`, while `top` and `middle` only report the sentinel.

### Bottom Half Stack and Top Half Deque

#### Derivation

A different decomposition needs no pointer bookkeeping at all: hold the bottom `ceil(count / 2)` elements in a list `bottom_stack` and the top `count - len(bottom_stack)` elements in a [deque](https://en.wikipedia.org/wiki/Double-ended_queue) `top_half`. The boundary between the halves always sits just above the lower middle, so `middle` peeks at `bottom_stack[-1]`. Pushing lands on the top of the stack, at the back of `top_half`; popping removes the back of `top_half`. Each operation moves the boundary by at most one slot, and one transfer restores the split:

1. Keep `bottom_stack` (a list) and `top_half` (a deque), both empty.
2. On `push`, append to the back of `top_half`; when `bottom_stack` now holds
   fewer than `ceil(count / 2)` elements, move the *bottom-most* element of the
   stack, `top_half.popleft()`, to the top of `bottom_stack`.
3. On `pop`, return `"EMPTY"` when both halves are empty; when `top_half` is
   empty the lone element sits on `bottom_stack`, so move it up and pop it.
   Otherwise pop the back of `top_half`; when `bottom_stack` now holds more
   than `ceil(count / 2)` elements, move its top back up with
   `top_half.appendleft(bottom_stack.pop())`.
4. `top` reads the back of `top_half`, or the top of `bottom_stack` when the
   top half is empty; `middle` reads `bottom_stack[-1]` whenever the stack is
   non-empty.

Two details make the transfers order-preserving and constant. `appendleft` pushes the returned element onto the boundary side of the deque, which keeps the deque's order aligned with the stack order it came from, and the deque's `popleft` removes the boundary-side element in constant time, where a list's `pop(0)` would shift the rest. That is the one place the standard library is doing work a plain list cannot.

#### Walkthrough

Example 1, halves shown bottom to top, with the lower middle readable at `bottom_stack[-1]`:

```text
push 1   top [1]      bottom []      bottom holds 0 < ceil(1/2)=1 -> move 1 down
         top []       bottom [1]
push 2   top [2]      bottom [1]     bottom holds 1 == ceil(2/2)=1, no move
push 3   top [2, 3]   bottom [1]     bottom holds 1 < ceil(3/2)=2 -> move 2 down
         top [3]      bottom [1, 2]
middle   bottom[-1] = 2   -> "2"          (count 3, exact center)
top      top[-1] = 3      -> "3"
pop      3 leaves;        top []  bottom [1, 2]
         bottom holds 2 > ceil(2/2)=1 -> move bottom's top (2) back up
         top [2]      bottom [1]
middle   bottom[-1] = 1   -> "1"          (count 2, lower slot)
```

The decisive event is the transfer after the `pop`: with three elements the exact center `2` sat on `bottom_stack`, but the two-element stack `[1, 2]` demands the lower slot, so the boundary moves up and `2` rejoins the top half. The collected returns are `["2", "3", "3", "1"]`, matching the expected Output. Example 3 exercises the lone-element pop: after `push -4` the transfer put `-4` on `bottom_stack` and left `top_half` empty, so the `pop` moves it back up, pops it, and the transfer stays quiet; `middle` and the popped value both read `-4`.

#### Solution

The code is the walkthrough's dispatch loop with the two one-transfer rebalances.

```python
from collections import deque
from typing import List


class Solution:
    def processMiddleStack(self, operations: List[List[str]]) -> List[str]:
        bottom_stack: List[int] = []
        top_half = deque()
        results: List[str] = []

        for operation in operations:
            action = operation[0]
            if action == "push":
                top_half.append(int(operation[1]))
                if len(bottom_stack) < (len(bottom_stack) + len(top_half) + 1) // 2:
                    bottom_stack.append(top_half.popleft())
            elif action == "pop":
                if not bottom_stack and not top_half:
                    results.append("EMPTY")
                    continue
                if not top_half:
                    top_half.append(bottom_stack.pop())
                popped = top_half.pop()
                if len(bottom_stack) > (len(bottom_stack) + len(top_half) + 1) // 2:
                    top_half.appendleft(bottom_stack.pop())
                results.append(str(popped))
            elif action == "top":
                if top_half:
                    results.append(str(top_half[-1]))
                elif bottom_stack:
                    results.append(str(bottom_stack[-1]))
                else:
                    results.append("EMPTY")
            else:
                if bottom_stack:
                    results.append(str(bottom_stack[-1]))
                else:
                    results.append("EMPTY")
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity

- **push**: `O(1)` - one append plus at most one constant-time `popleft` transfer.
- **pop**: `O(1)` - one pop plus at most one constant-time transfer.
- **top**: `O(1)` - a peek at a deque end or the list top.
- **middle**: `O(1)` - a peek at `bottom_stack[-1]`.

For `m` operations this is `O(m)` worst case.

##### Space Complexity: `O(u)`

The two halves together hold exactly the `u` present elements, plus `results`.

#### Key Insights

- Splitting at the boundary turns the middle query into a peek, the same trick a two-stack queue plays on its front: the structure's job is keeping the boundary honest, not answering the query.
- The bottom half must hold exactly `ceil(count / 2)` elements; a split at the raw half would misplace the lower middle on even counts.
- Both transfers must preserve order across the boundary: `appendleft` returns an element to the deque's boundary side, and `popleft` takes one from it in constant time, where `pop(0)` on a list would shift the rest.
- Each operation fires at most one transfer because push and pop move the boundary by one slot; the deque earns its import at exactly one method pair.

## Comparison of Solutions

### Time Complexity

- **Array with Index Formula**: `O(1)` per operation, push amortized - appends, back pops, and direct index reads.
- **Doubly Linked List with Middle Pointer**: `O(1)` worst case per operation - pointer splices plus at most one `middle` hop.
- **Bottom Half Stack and Top Half Deque**: `O(1)` worst case per operation - one append or pop plus at most one constant-time transfer.

### Space Complexity

- **Array with Index Formula**: `O(u)` - the one element list plus results.
- **Doubly Linked List with Middle Pointer**: `O(u)` - one node per element plus two sentinels.
- **Bottom Half Stack and Top Half Deque**: `O(u)` - the two halves hold exactly the present elements.

### Trade-offs

- **Array with Index Formula**: the least code and already constant-time per operation because the requested middle is bottom-anchored; it carries no reusable design and leans on the dynamic array's amortized resizing.
- **Doubly Linked List with Middle Pointer**: strict worst-case constant time with a single explicit pointer invariant, at the price of node plumbing and the parity rule applied in two places.
- **Bottom Half Stack and Top Half Deque**: the clearest decomposition, boundary maintenance rather than query answering, built from two stock containers with no node class; the cost is the boundary invariant, which must hold `ceil` exactly.

### When to Use Each

- **Array with Index Formula**: when the target language array already gives constant-time indexing and the code must be shortest.
- **Doubly Linked List with Middle Pointer (Recommended)**: when the interviewer asks for the design lesson: explicit `O(1)` worst case for every operation, no amortization caveat.
- **Bottom Half Stack and Top Half Deque**: when the explanation should center on the boundary invariant, or in languages whose native deque makes the two-container version the shortest strict solution.

### Optimization Notes

- **Doubly Linked List with Middle Pointer** is the recommended choice: every operation is `O(1)` in the strict worst case, which is what the page's requirement asks for.
- The single subtlety shared by both designed versions is parity: the lower middle of an even-sized stack is the last element of the bottom half, and every push or pop flips the parity that decides whether the middle moves.
- The array version's `(count - 1) // 2` formula is its whole middle logic; check it against both parities (`[1, 2] -> 1`, `[1, 2, 3] -> 2`) before trusting it.
- The two-container version borrows the deque for one reason: `popleft` and `appendleft` keep the boundary transfers constant-time and order-preserving, where list `pop(0)` and `insert(0, ...)` would shift every element above the boundary.
