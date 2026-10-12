# [Next Smaller Ticket Price](https://www.fastprep.io/problems/amazon-next-smaller-ticket-price)

**Medium** | **NN minutes** | **Array, Stack**

You are given an integer array prices, where prices[i] is the price of ticket i.

For each ticket, find the next strictly smaller price to its right. If no later ticket is cheaper, the answer for that ticket is -1.

Return an array of the same length as prices containing those answers in index order.

## Examples

### Example 1

**Input:** `prices = [8,4,6,2,3]`

**Output:** `[4,2,2,-1,-1]`

**Explanation:** Ticket 8 is followed by cheaper 4. Ticket 4 is followed by cheaper 2. Ticket 6 is followed by cheaper 2. Tickets 2 and 3 have no later cheaper price.

### Example 2

**Input:** `prices = [5,4,3,2,1]`

**Output:** `[4,3,2,1,-1]`

**Explanation:** Each ticket is immediately followed by a cheaper ticket except the last.

### Example 3

**Input:** `prices = [1,2,3]`

**Output:** `[-1,-1,-1]`

**Explanation:** Every later ticket is more expensive, so every answer is -1.

## Constraints

- `1 <= prices.length <= 10^5.`
- `1 <= prices[i] <= 10^9.`

## Solutions

### Brute Force

#### Derivation

The most literal reading of the problem: for each ticket, walk to the right until the first strictly cheaper price appears, and record -1 when the walk reaches the end empty-handed. The definition itself is the algorithm, a scan per ticket:

1. Allocate `next_smaller` with `count` entries, initialized to `-1`.
2. For each `position`, scan `later` from `position + 1` upward.
3. The first `prices[later] < prices[position]` is the answer for that ticket:
   record it and break the inner scan.
4. When the inner scan finishes without a hit, the initialized `-1` stands.

#### Walkthrough

Example 1, `prices = [8, 4, 6, 2, 3]`, one row per ticket. Each inner scan stops at the first strictly smaller price:

```text
position 0  price 8   later 1: 4 < 8  -> answer 4
position 1  price 4   later 2: 6 no;  later 3: 2 < 4  -> answer 2
position 2  price 6   later 3: 2 < 6  -> answer 2
position 3  price 2   later 4: 3 no;  end of array    -> answer -1
position 4  price 3   no later tickets                -> answer -1
```

Reading the answers in index order gives `[4, 2, 2, -1, -1]`, matching the expected Output.

#### Solution

The code is the per-ticket scan from the walkthrough:

```python
from typing import List


class Solution:
    def solve(self, prices: List[int]) -> List[int]:
        count = len(prices)
        next_smaller = [-1] * count
        for position in range(count):
            for later in range(position + 1, count):
                if prices[later] < prices[position]:
                    next_smaller[position] = prices[later]
                    break
        return next_smaller
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each ticket scans forward up to the end of the array; a non-increasing input such as Example 2 drives the inner scan to its full length for every ticket.

##### Space Complexity: `O(1)`

Only the output array, which the problem statement requires anyway; no auxiliary structure grows with the input.

#### Key Insights

- The inner scan can stop at the first hit because the problem asks for the *next* smaller price, not the smallest one anywhere to the right.
- Strictly smaller is the comparison that matters: an equal price must be stepped over, not accepted (Example 3's rising sequence never trips this, but `[2, 2]` would: the answer for the first ticket is -1, not 2).
- The quadratic worst case is structural, not an implementation slip: no early exit helps when every later price is larger.

### Right-to-Left Monotonic Stack

#### Derivation

The brute force re-walks the same tail of the array once for every ticket: ticket `position` and ticket `position + 1` scan almost identical territory. The observation that removes the waste is what the answer depends on: only the *prices to the right*, in order, and among them only those that could ever be the next smaller price of something. A later price that is not smaller than a candidate between it and the current ticket can never surface. Collecting the still-relevant prices in a [monotonic stack](https://en.wikipedia.org/wiki/Monotonic_function), kept strictly increasing from bottom to top, answers each ticket after popping the irrelevant ones:

1. Walk `position` from the last ticket to the first, so the stack always
   holds exactly the prices to the right of `position`.
2. Pop every `seen_prices` entry with `seen_prices[-1] >= price`: an equal or
   higher price cannot serve as a strictly smaller answer for the current
   ticket, and it cannot serve for anything farther left either, because the
   current `price` is closer and smaller.
3. After the pops, `seen_prices[-1]`, if any price remains, is the nearest
   surviving strictly smaller price: record it in `next_smaller[position]`,
   otherwise record `-1`.
4. Push `price` onto `seen_prices` before moving one step left.

#### Invariant

The invariant is what makes step 3 safe to trust without re-scanning:

```text
seen_prices is strictly increasing bottom to top, and holds exactly the
prices of tickets to the right of the current position that have not been
discarded as dominated.
```

- **Strictly increasing:** before pushing `price`, every entry `>= price` was
  popped, so the new top is smaller than `price`, and the pre-push stack was
  inductive strictly increasing.
- **Exactly the right tickets:** each iteration removes entries and then adds
  exactly one, so the stack tracks the suffix sweep one ticket at a time.
- **Dominance is safe:** a popped entry `p >= price` can never be the next
  smaller price of a ticket farther left: if it beat that ticket, then
  `price < p` would also beat it, and `price` sits closer, so the *next*
  smaller is `price` or something even nearer.

At sweep end the stack is empty and every slot of `next_smaller` has been filled by a correct nearest-smaller lookup.

#### Walkthrough

Example 1, `prices = [8, 4, 6, 2, 3]`, traced right to left. Each line is one iteration: the pops caused by the current price, the recorded answer, and the stack after the push:

```text
position 4  price 3   pop: (empty)          answer -1   seen_prices = [3]
position 3  price 2   pop 3 (3 >= 2)        answer -1   seen_prices = [2]
position 2  price 6   pop: 2 < 6 stays      answer  2   seen_prices = [2, 6]
position 1  price 4   pop 6 (6 >= 4)        answer  2   seen_prices = [2, 4]
            top 2 < 4, stop popping
position 0  price 8   pop: 4 < 8 stays      answer  4   seen_prices = [2, 4, 8]
```

Answers read in index order: `[4, 2, 2, -1, -1]`, matching the expected Output. The decisive beats are at positions 3 and 1: position 3 pops the lone 3 and rightly reports -1 (the only later price was not strictly smaller), and position 1 pops the 6 pushed one step earlier, showing the stack is a filter of survivors rather than the array's tail.

#### Solution

The code is the sweep from the walkthrough: pop dominated prices, read the top, push the current price.

```python
from typing import List


class Solution:
    def solve(self, prices: List[int]) -> List[int]:
        count = len(prices)
        next_smaller = [0] * count
        seen_prices: List[int] = []
        for position in range(count - 1, -1, -1):
            price = prices[position]
            while seen_prices and seen_prices[-1] >= price:
                seen_prices.pop()
            next_smaller[position] = seen_prices[-1] if seen_prices else -1
            seen_prices.append(price)
        return next_smaller
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each price is pushed exactly once and popped at most once across the whole sweep, so total stack activity is proportional to `n`.

##### Space Complexity: `O(n)`

The stack can hold every price to the right when the input is increasing from that point (Example 3 leaves all three prices stacked); the output array is required by the statement.

#### Key Insights

- Sweeping right to left turns "search to the right" into "consult what is already summarized": the stack is the suffix's surviving candidates.
- The pop condition is `>=`, not `>`: an equal price is not strictly smaller, and keeping equal prices on the stack would let a later lookup accept a non-smaller answer.
- Total work is `O(n)` despite the nested-looking loop because each price enters and leaves the stack at most once; the pops are paid for by the pushes that created them.
- The same sweep with `<=` and a "next greater" reading solves the mirror problem, and an index stack instead of a price stack solves the distance variant; the structure, not the prices, is the reusable part.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - each ticket scans forward until its answer or the array's end, and non-increasing inputs defeat every shortcut.
- **Right-to-Left Monotonic Stack**: `O(n)` - one push and at most one pop per price across the entire sweep.

### Space Complexity

- **Brute Force**: `O(1)` - no structure beyond the required output array.
- **Right-to-Left Monotonic Stack**: `O(n)` - the stack of surviving candidate prices.

### Trade-offs

- **Brute Force**: writes itself straight from the definition and allocates nothing, which makes it a trustworthy test oracle; at `n = 10^5` its inner scans reach ten billion comparisons and it is unusable.
- **Right-to-Left Monotonic Stack**: linear time at the cost of an auxiliary stack and a correctness argument (the dominance invariant) that must be stated rather than seen.

### When to Use Each

- **Right-to-Left Monotonic Stack (Recommended)**: whenever the constraints allow `n` beyond a few thousand, which here (`n <= 10^5`) they do from the start.
- **Brute Force**: for tiny inputs, for property-based cross-checks of the stack version, or as the first spoken step in an interview before improving it.

### Optimization Notes

- Initialize `next_smaller` to a placeholder (`0`) and always overwrite it, or initialize to `-1` and skip writes when the stack empties; both work, but the overwrite form keeps the hot loop branch-free apart from the pop test.
- The pop condition `seen_prices[-1] >= price` does double duty: it discards non-smaller answers for the current ticket and prunes dominated candidates for every ticket still to come.
- The loop `for position in range(count - 1, -1, -1)` walks indices right to left without reversing the input or the output; reversing the array instead would force an output reversal at the end and obscure the index bookkeeping.
