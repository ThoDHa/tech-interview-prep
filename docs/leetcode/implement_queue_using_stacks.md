# [Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/)

**Easy** | **20 minutes** | **Stack, Queue, Design**

**Pattern:** [Data-Structure Design](../patterns/design/intuition.md)

**Algorithm:** [Queue](https://en.wikipedia.org/wiki/Queue_(abstract_data_type)) · [Stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type))

**Practice:** [`practice/implement_queue_using_stacks/solution.py`](../../practice/implement_queue_using_stacks/solution.py)

Implement a first in first out (FIFO) queue using only two stacks. The implemented queue should support all the functions of a normal queue (`push`, `pop`, `peek`, and `empty`).

Implement the `MyQueue` class:

- `void push(int x)` Pushes element x to the back of the queue.
- `int pop()` Removes the element from the front of the queue and returns it.
- `int peek()` Returns the element at the front of the queue.
- `boolean empty()` Returns `true` if the queue is empty, `false` otherwise.

**Notes:**

- You must use only standard operations of a stack, which means only `push to top`, `peek/pop from top`, `size`, and `is empty` operations are valid.
- Depending on your language, the stack may not be supported natively. You may simulate a stack using a list or deque (double-ended queue) as long as you use only a stack's standard operations.

## Examples

### Example 1

**Input:**

```text
["MyQueue", "push", "push", "peek", "pop", "empty"]
[[], [1], [2], [], [], []]
```

**Output:**

```text
[null, null, null, 1, 1, false]
```

**Explanation:**

```text
MyQueue myQueue = new MyQueue();
myQueue.push(1); // queue is: [1]
myQueue.push(2); // queue is: [1, 2] (leftmost is front of the queue)
myQueue.peek(); // return 1
myQueue.pop(); // return 1, queue is [2]
myQueue.empty(); // return false
```

## Constraints

- `1 <= x <= 9`
- At most `100` calls will be made to `push`, `pop`, `peek`, and `empty`.
- All the calls to `pop` and `peek` are valid.

## Follow-up

Can you implement the queue such that each operation is amortized `O(1)` time complexity? In other words, performing n operations will take overall `O(n)` time even if one of those operations may take longer.

## Deriving the Solution

A stack hands elements back newest-first; a queue must hand them back oldest-first. Draining one stack into another reverses its order, and two reversals cancel, so both solutions move elements between two stacks until the queue's front sits on top of the stack that `pop` and `peek` read. They differ only in *when* they pay for that reversal.

1. **Start literal.** Keep the whole queue in one stack, front on top, at all
   times. Then `pop`, `peek`, and `empty` are single stack operations, but every `push` must place the new element at the *bottom*, which costs a full drain into a helper stack and back: `O(n)` per push: see [Eager Push](#eager-push).
2. **Spot the waste.** Eager Push re-shuffles every element on every push, even
   when no pop is coming. A burst of pushes pays the full reversal each time, and each reversal undoes the previous one's work.
3. **Pay lazily.** Let pushes pile up untouched in an input stack, and reverse them
   into an output stack only when a `pop` or `peek` finds that output stack empty. Each element then crosses over at most once in its lifetime, which makes every operation amortized `O(1)` and answers the Follow-up: see [Lazy Pop](#lazy-pop).

## Solutions

### Eager Push

#### Derivation

Start from the operations that must be fast to feel like a queue: `pop` and `peek` read the front. If the main stack `queue` always holds the elements in queue order with the oldest on top, both are single [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) operations. The question becomes: how does `push` insert a new element at the *bottom* of that stack using only stack operations? By clearing the way: drain everything into a helper stack, drop the new element into the empty main stack, and pour the helper back on top. The two transfers reverse the order twice, so the old elements come back in their original order, now sitting above the newcomer. The steps:

1. `push(x)`: pop every element off `queue` onto `stack`, append `x` to the
   now-empty `queue`, then pop everything off `stack` back onto `queue`. The new element ends at the bottom; the older elements return above it, oldest on top.
2. `pop()`: return `self.queue.pop()`, the top of the stack, which is the front of
   the queue.
3. `peek()`: return `self.queue[-1]` without removing it.
4. `empty()`: report `len(self.queue) == 0`; the helper `stack` is always empty
   between operations.

#### Walkthrough

Let us watch the Eager Push solution run on Example 1, the call sequence `push(1)`, `push(2)`, `peek()`, `pop()`, `empty()`. The key idea to hold in mind: `queue` is a list used as a stack, so its last element (rightmost, written here as the top) is what `pop()` and `peek()` see. The whole trick keeps the front of the queue sitting at that top.

`push(1)`: `queue` starts empty, so the first `while self.queue` loop does nothing. We append `1`, giving `queue = [1]`. The second loop finds `stack` empty, so nothing moves back.

`push(2)`: now `queue = [1]` is not empty. The first loop pops `1` off `queue` and pushes it onto `stack`: `queue = []`, `stack = [1]`. We append the new element: `queue = [2]`. The second loop pops `1` off `stack` and pushes it onto `queue`: `queue = [2, 1]`, `stack = []`. Notice `1` (the older element, the front of the queue) is now at the top (rightmost), exactly where `pop` and `peek` look.

Tracking the state after each push:

| Call | `queue` (top is rightmost) | `stack` |
| --- | --- | --- |
| `push(1)` | `[1]` | `[]` |
| `push(2)` | `[2, 1]` | `[]` |

`peek()`: returns `self.queue[-1]`, which is `1`. The queue is unchanged: `queue = [2, 1]`.

`pop()`: returns `self.queue.pop()`, removing and returning the top, `1`. Now `queue = [2]`, leaving `2` ready as the next front.

`empty()`: checks `len(self.queue) == 0`. Since `queue = [2]` has one element, it returns `false`.

The three non-`null` calls return `1`, `1`, and `false`, so the full output sequence is `[null, null, null, 1, 1, false]`, matching the expected Output.

#### Solution

The code is the drain-drop-restore cycle from the walkthrough, run inside `push`; the other three methods read the top of `queue` directly.

```python
class MyQueue:
    def __init__(self):
        self.stack = []  # Temporary stack for rearranging elements
        self.queue = []  # Main stack that holds elements in queue order

    def push(self, x: int) -> None:
        # Transfer all elements to temporary stack (reversing order)
        while self.queue:
            self.stack.append(self.queue.pop())

        # Add new element to empty queue (will be at the bottom when elements are moved back)
        self.queue.append(x)

        # Transfer elements back to queue (restoring original order with new element at bottom)
        while self.stack:
            self.queue.append(self.stack.pop())

    def pop(self) -> int:
        # Front of queue is at the top of our queue stack
        return self.queue.pop()

    def peek(self) -> int:
        # Front of queue is at the top of our queue stack
        return self.queue[-1]

    def empty(self) -> bool:
        # Check if the queue stack is empty
        return len(self.queue) == 0
```

#### Time and Space Complexity Analysis

##### Time Complexity

- **push**: `O(n)` - We need to move all n elements twice for each push operation
- **pop**: `O(1)` - Simply remove from the top of the stack
- **peek**: `O(1)` - Simply view the top of the stack
- **empty**: `O(1)` - Just check if the stack is empty

##### Space Complexity: `O(n)`

We need space proportional to the number of elements in the queue.

#### Key Insights

- This implementation sacrifices push efficiency to make pop and peek operations very fast
- The main stack always maintains elements in queue order, with oldest elements at the top
- This approach provides consistent (non-amortized) `O(1)` time for pop and peek operations
- The rearrangement during push operations ensures proper queue ordering

### Lazy Pop

#### Derivation

The Eager Push pays its `O(n)` reversal on every single push, even when no pop ever looks at the result, and each push's reversal undoes the previous one's. The repair is to defer the work until it is actually needed. Give the [two stacks](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) different jobs: `stack_input` receives every `push` untouched, and `stack_output` serves every `pop` and `peek`. When the output stack runs dry, one transfer drains `stack_input` into it, and that single reversal puts the oldest element on top, exactly where the front belongs.

The condition on the transfer is the heart of the approach: refill *only when `stack_output` is empty*. Refilling any earlier would drop newer elements on top of older ones still waiting in the output stack, letting them jump the line. The [Invariant](#invariant) below states this precisely and derives the amortized bound from it. The steps:

1. `push(x)`: append `x` to `stack_input`. Nothing else moves.
2. `_ensure_output_has_values()`: when `stack_output` is empty, pop every element
   off `stack_input` and append it to `stack_output`, reversing the order so the oldest element lands on top.
3. `pop()` and `peek()`: call `_ensure_output_has_values()`, then pop or read the
   top of `stack_output`.
4. `empty()`: the queue is empty only when *both* stacks are empty, since elements
   may be waiting on either side.

#### Invariant

List `stack_output` bottom to top as \(o_1, \ldots, o_p\) and `stack_input` bottom to top as \(i_1, \ldots, i_q\). The queue those two stacks represent, read front to back, is:

$$ \underbrace{o_p,\, o_{p-1},\, \ldots,\, o_1}_{\text{reversed}(\textit{stack\_output})} \;,\;\; \underbrace{i_1,\, i_2,\, \ldots,\, i_q}_{\textit{stack\_input}} $$

```text
queue front to back = reversed(stack_output), then stack_input
                      (both stacks listed bottom to top)
```

The front of the queue is therefore the *top* of `stack_output` whenever \(p > 0\), which is what lets `pop` and `peek` be plain stack operations.

Every method preserves this. `push` appends to the top of `stack_input`, adding \(i_{q+1}\) at the back, where a newly pushed element belongs. `pop` and `peek` read the top of `stack_output`, which is the front. A refill moves all of `stack_input` across, and because it runs only when \(p = 0\) the queue at that moment is exactly \(i_1, \ldots, i_q\); popping those top to bottom and appending leaves `stack_output` \(= i_q, \ldots, i_1\), whose reverse is \(i_1, \ldots, i_q\) again. The order is unchanged.

This is why `if not self.stack_output:` is the correctness condition and not an optimization. Refilling while \(p > 0\) would leave `stack_output` \(= o_1, \ldots, o_p, i_q, \ldots, i_1\), which reads front to back as \(i_1, \ldots, i_q, o_p, \ldots, o_1\): every newly pushed element jumps ahead of elements that were already waiting, and the structure stops being FIFO.

The same guard carries the amortized bound. A refill drains `stack_input` completely, and an element enters `stack_input` exactly once (on its `push`), so each element takes part in at most one refill. Its entire lifetime is a fixed number of stack operations: one append to `stack_input`, at most one pop-and-append across, and one pop from `stack_output`. Across \(n\) operations the total work is \(O(n)\), which is amortized \(O(1)\) each even though a single refill can cost \(O(n)\) on its own.

#### Walkthrough

Let us run the Lazy Pop solution on Example 1, the call sequence `push(1)`, `push(2)`, `peek()`, `pop()`, `empty()`. Both stacks are written bottom to top, so the rightmost element is the top. Watch where the reversal happens: not during the pushes, but inside the first `peek()`.

```text
push(1)   stack_input = [1]      stack_output = []      queue front to back: 1
push(2)   stack_input = [1, 2]   stack_output = []      queue front to back: 1, 2
peek()    stack_output is empty -> refill: pop 2 across, then pop 1 across
          stack_input = []       stack_output = [2, 1]  top is 1, the front
          returns stack_output[-1] = 1
pop()     stack_output is not empty -> no refill
          stack_input = []       stack_output = [2]     returns 1
empty()   stack_input = [] but stack_output = [2] -> returns false
```

The refill inside `peek()` reverses `[1, 2]` into `[2, 1]`, landing the oldest element `1` on top; the subsequent `pop()` finds `stack_output` already populated and touches nothing else, which is the laziness paying off. The three non-`null` calls return `1`, `1`, and `false`, so the full output sequence is `[null, null, null, 1, 1, false]`, matching the expected Output.

#### Solution

The code is the walkthrough's two stacks written down, with the refill guard isolated in `_ensure_output_has_values`.

```python
class MyQueue:
    def __init__(self):
        self.stack_input = []  # For push operations
        self.stack_output = []  # For pop/peek operations

    def push(self, x: int) -> None:
        # Simply push element to input stack
        self.stack_input.append(x)

    def pop(self) -> int:
        # Ensure output stack has elements
        self._ensure_output_has_values()
        # Return and remove the front element
        return self.stack_output.pop()

    def peek(self) -> int:
        # Ensure output stack has elements
        self._ensure_output_has_values()
        # Return the front element without removing it
        return self.stack_output[-1]

    def empty(self) -> bool:
        # Queue is empty if both stacks are empty
        return len(self.stack_input) == 0 and len(self.stack_output) == 0

    def _ensure_output_has_values(self) -> None:
        # If output stack is empty, transfer all elements from input stack
        if not self.stack_output:
            while self.stack_input:
                self.stack_output.append(self.stack_input.pop())
```

#### Time and Space Complexity Analysis

##### Time Complexity

- **push**: `O(1)` - Simply append to the input stack
- **pop**: Amortized `O(1)` - While a single pop might take `O(n)` when transferring elements,
  across multiple operations it averages to `O(1)` per operation
- **peek**: Amortized `O(1)` - Same reasoning as pop
- **empty**: `O(1)` - Just check if both stacks are empty

##### Space Complexity: `O(n)`

We need space proportional to the number of elements in the queue.

#### Key Insights

- This approach optimizes push operations at the expense of occasional costly pop/peek operations
- Elements are only transferred when necessary, avoiding redundant operations
- Each element is moved at most twice (once to input stack, once to output stack)
- The amortization of the transfer cost makes this approach efficient for n operations
- This implementation directly addresses the follow-up question about amortized `O(1)` time complexity

## Comparison of Solutions

### Time Complexity

- **Eager Push**: `push` is `O(n)` because every push moves all elements twice, while `pop`, `peek`, and `empty` are each a guaranteed `O(1)`.
- **Lazy Pop**: `push` is `O(1)` (a simple append to the input stack), `pop` and `peek` are amortized `O(1)` (an occasional transfer costs `O(n)` but averages out across operations), and `empty` is `O(1)`.

### Space Complexity

Both approaches use `O(n)` space to store all queue elements.

### Trade-offs

- **Eager Push**:
    - Pros: Predictable performance for pop/peek with guaranteed `O(1)` time
    - Cons: Every push operation is expensive (`O(n)`), regardless of subsequent operations
    - Best when: Pop/peek operations are much more frequent than push operations

- **Lazy Pop**:
    - Pros: More efficient overall, with better amortized performance
    - Cons: Individual pop/peek operations might occasionally be expensive
    - Best when: Push operations are frequent or balanced with pop/peek operations

### When to Use Each

- **Use Eager Push when**:
    - Consistent, non-amortized time for pop/peek is critical
    - Queue size remains small, limiting the cost of push operations
    - Pop/peek operations significantly outnumber push operations

- **Use Lazy Pop when**:
    - Overall efficiency across multiple operations is the priority
    - Amortized performance is acceptable
    - Push operations are frequent
    - The follow-up requirement for amortized `O(1)` operations needs to be satisfied

### Optimization Notes

- The lazy approach is generally more efficient in practice for most use cases
- For the follow-up question requiring amortized `O(1)` operations, the lazy approach is the appropriate solution
- Both approaches demonstrate the fundamental computer science principle of time-space tradeoffs
- The lazy approach exemplifies how amortization analysis can reveal algorithms that are efficient over a sequence of operations, even if individual operations sometimes take longer
