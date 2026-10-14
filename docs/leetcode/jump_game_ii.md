# [Jump Game II](https://leetcode.com/problems/jump-game-ii/)

**Medium** | **25 minutes** | **Array, Dynamic Programming, Greedy**

**Pattern:** [Greedy](../patterns/greedy_core/intuition.md)

**Algorithm:** [Recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science)) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Greedy algorithm](https://en.wikipedia.org/wiki/Greedy_algorithm) · [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)

**Practice:** [`practice/jump_game_ii/solution.py`](../../practice/jump_game_ii/solution.py)

You are given an array of integers `nums`, where `nums[i]` represents the maximum length of a jump towards the right from index `i`. For example, if you are at `nums[i]`, you can jump to any index `i + j` where:

* `j <= nums[i]`
* `i + j < nums.length`

You are initially positioned at `nums[0]`.

Return the minimum number of jumps to reach the last position in the array (index `nums.length - 1`). You may assume there is always a valid answer.

## Examples

### Example 1

**Input:** `nums = [2,4,1,1,1,1]`

**Output:** `2`

**Explanation:** Jump from index `0` to index `1`, then jump from index `1` to the last index.

### Example 2

**Input:** `nums = [2,1,2,1,0]`

**Output:** `2`

## Constraints

- `1 <= nums.length <= 1000`
- `0 <= nums[i] <= 100`

## Deriving the Solution

Every index offers up to `nums[i]` landing spots, so "fewest jumps to the end" is a shortest path over those choices, and each jump costs exactly `1`. Every solution below runs that shortest-path computation; they differ in how much of it they notice is unnecessary.

1. **Start literal.** From each index, try every jump and recurse on what
   remains: the answer is `1` plus the cheapest continuation. Every route is
   explored, so the minimum falls out, at exponential cost: see
   [Brute Force](#brute-force).
2. **Spot the waste.** The question "fewest jumps from here" is a question
   about the index alone, yet every route re-asks it. Cache one number per
   index: see [Top-Down Memoization](#top-down-memoization).
3. **Flip the direction.** The cached cost of index `j` only ever feeds
   indices left of it, so a left-to-right pass that relaxes every reachable
   landing spot computes the same numbers with no recursion: see
   [Bottom-Up DP](#bottom-up-dp).
4. **Stop pricing individual landings.** All spots one jump away share the
   same cost, so per-spot bookkeeping repeats one number across a whole
   window. Track the frontier instead: the range of spots the current jump
   can reach, and the farthest spot the next jump could reach. Counting how
   often the frontier must advance *is* the answer, in one pass with two
   integers: see [Greedy](#greedy).

## Solutions

### Brute Force

#### Derivation

The most literal reading tries every route: standing at index `i`, take each jump length `1` through `nums[i]`, and the cheapest way onward is `1` plus the cheapest continuation from the landing spot. The base case is standing on (or past) the last index, where no jump remains:

1. Define `min_jumps(i)` as the fewest jumps from index `i` to the last index.
2. Base case: `i >= len(nums) - 1`, return `0`.
3. For each `step` in `1 .. nums[i]`, consider `1 + min_jumps(i + step)`.
4. Return the minimum; the answer is `min_jumps(0)`.

The guarantee of a valid answer means every input has at least one route; the recursion finds the cheapest by pricing all of them.

#### Walkthrough

Trace the recursion on a tailored input: `nums = [2, 1, 1, 1]`, small enough to show both of the root's branches resolving. Each line is a call returning; children print above their parent, and `s1`/`s2` name the jump step taken:

```text
            c0.s1.s1.s1: min_jumps(3) -> 0    last index reached
        c0.s1.s1: min_jumps(2) -> 1    min of 1 + min_jumps(3) = 1
    c0.s1: min_jumps(1) -> 2    min of 1 + min_jumps(2) = 2
        c0.s2.s1: min_jumps(3) -> 0    last index reached
    c0.s2: min_jumps(2) -> 1    min of 1 + min_jumps(3) = 1
c0: min_jumps(0) -> 2    min of 1 + min_jumps(1) = 3;  1 + min_jumps(2) = 2
-> 2
```

Both root branches resolve the suffix `2, 1` but the direct hop `0 -> 2` prices it at `1 + 1 = 2` while the two single hops cost `1 + 2 = 3`. The root returns `2`: jump to index `2`, then to index `3`. Note `min_jumps(2)` is computed twice, once per route that lands there, which is exactly the repeat work the next solution caches.

#### Solution

The code is the walkthrough's step loop around the base case, taking the minimum.

```python
from typing import List


class Solution:
    def jump(self, nums: List[int]) -> int:
        def min_jumps(i: int) -> int:
            if i >= len(nums) - 1:
                return 0
            best = len(nums)
            for step in range(1, nums[i] + 1):
                best = min(best, 1 + min_jumps(i + step))
            return best

        return min_jumps(0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

Each index branches into `nums[i]` calls and overlapping suffixes are re-priced once per route, so on adversarial inputs the call tree grows exponentially; the `len(nums)` seed for `best` is a stand-in for "unreachable", not a real route cost.

##### Space Complexity: `O(n)`

The recursion stack reaches depth `n` along the longest hop-one chain.

#### Key Insights

- The guarantee "there is always a valid answer" is what lets `min_jumps`
  return a plain number; without it, unreachable starts would need a sentinel.
- The recursion's shape, "one jump plus the rest", is the shortest-path
  relaxation written in the problem's own vocabulary.
- Success is the expensive case here, the mirror image of Jump Game: every
  route must be priced to prove the cheapest one is cheapest.

### Top-Down Memoization

#### Derivation

`min_jumps(i)` depends on nothing but `i`, so the Brute Force's repeated suffix pricing is pure waste. [Caching](https://en.wikipedia.org/wiki/Memoization) one number per index makes every repeat a lookup:

1. Keep `min_jumps(i)` verbatim from the Brute Force, base case included.
2. Before computing, check `memo` for `i` and return the stored number.
3. Otherwise run the step loop, store the minimum in `memo[i]`, and return it.
4. At most `n` indices each try up to `nums[i]` steps, so the tree collapses
   to `O(n^2)` in the worst case.

#### Walkthrough

Trace the memoized recursion on a tailored input, the classic `[2, 3, 1, 1, 4]`, which is smaller than this problem's Examples and shows hits clearly. Each line is a call returning; children print above their parent, and marked lines are memo hits (`s1`/`s2`/`s3` name the jump step):

```text
        min_jumps(4) -> 0    last index reached
      min_jumps(3) -> 1    s1: 1
    min_jumps(2) -> 2    s1: 2
    min_jumps(3) -> 1    ** memo hit **
    min_jumps(4) -> 0    last index reached
  min_jumps(1) -> 1    s1: 3;  s2: 2;  s3: 1
  min_jumps(2) -> 2    ** memo hit **
min_jumps(0) -> 2    s1: 2;  s2: 3
-> 2
```

The first descent prices every index on the way down (`4 -> 3 -> 2 -> 1`); the branches that revisit those indices get their numbers from `memo` instead of growing subtrees. The root compares hopping to `1` (then one big jump to the end) against hopping to `2` (then two more hops) and returns `2`.

#### Solution

The Brute Force recursion with the memo check and store wrapped around the step loop.

```python
from typing import List


class Solution:
    def jump(self, nums: List[int]) -> int:
        memo = {}

        def min_jumps(i: int) -> int:
            if i >= len(nums) - 1:
                return 0
            if i in memo:
                return memo[i]
            best = len(nums)
            for step in range(1, nums[i] + 1):
                best = min(best, 1 + min_jumps(i + step))
            memo[i] = best
            return best

        return min_jumps(0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n` indices runs its body once and tries up to `nums[i]` steps; every repeat visit is a dictionary hit. The sum of all jump widths bounds the total work.

##### Space Complexity: `O(n)`

The memo holds one number per index, and the recursion stack reaches depth `n`.

#### Key Insights

- One number per index is the whole state: the cheapest way onward cannot
  depend on how the jump got there.
- The guarantee of a valid answer also guarantees every index on some route
  gets a real value; no sentinel survives into the answer.
- The memo table is the bridge to the bottom-up form: its fill order is
  already visible in the recursion.

### Bottom-Up DP

#### Derivation

The memoized recursion discovers costs in an order that reads "later indices first", which a forward sweep can produce directly: process indices left to right, and when index `i`'s cost is final, use it to relax every spot `i + 1 .. i + nums[i]`. This is [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) as shortest-path relaxation, one jump per edge, all edges costing `1`:

1. Let `table[i]` hold the fewest jumps from index `0` to index `i`; seed
   `table[0] = 0` and everything else at `n`, a cost no real route can reach.
2. Sweep `i` from `0` to `n - 1`; for each step landing in range, relax
   `table[j] = min(table[j], table[i] + 1)`.
3. Return `table[n - 1]`.

#### Recurrence

Let `table[i]` be the fewest jumps from index `0` to index `i`:

$$ table[i] = \begin{cases}
0, & i = 0 \\[4pt]
\min\limits_{k + nums[k] \ge i,\ 1 \le nums[k]} \bigl(table[k] + 1\bigr), & i > 0
\end{cases} $$

```text
table[0] = 0
table[i] = min over k < i with k + nums[k] >= i of (table[k] + 1)
answer   = table[n - 1]
```

The forward sweep computes the same relation without the quantifier: when the sweep is standing at `k`, `table[k]` is final (only strictly earlier indices can jump to `k`, and they were all processed), so writing `table[k] + 1` into every reachable landing spot installs the minimum. The answer is the last entry.

#### Walkthrough

Let us fill the table on the classic `[2, 3, 1, 1, 4]`:

```text
seed     table[0] = 0;  everything else starts at 5 (unreachable)
i = 0    table[1] = min(5, 0 + 1) = 1;  table[2] = min(5, 0 + 1) = 1
      table = [0, 1, 1, 5, 5]
i = 1    table[2] = min(1, 1 + 1) = 1;  table[3] = min(5, 1 + 1) = 2;  table[4] = min(5, 1 + 1) = 2
      table = [0, 1, 1, 2, 2]
i = 2    table[3] = min(2, 1 + 1) = 2
      table = [0, 1, 1, 2, 2]
i = 3    table[4] = min(2, 2 + 1) = 2
      table = [0, 1, 1, 2, 2]
i = 4    +1: 5 out of range;  +2: 6 out of range;  +3: 7 out of range;  +4: 8 out of range
      table = [0, 1, 1, 2, 2]
-> table[4] = 2
```

Index `1`'s long jump relaxes `3` and `4` in one stride, and nothing later beats those numbers: the relaxations only ever lower a cost, never raise one. The last entry is `table[4] = 2`, matching the verdict the memoized recursion reached on this input.

#### Solution

The code is the walkthrough's forward sweep: finalize an index, relax its landing spots.

```python
from typing import List


class Solution:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        # table[i] = fewest jumps from index 0 to index i
        table = [n] * n
        table[0] = 0
        for i in range(n):
            for step in range(1, nums[i] + 1):
                j = i + step
                if j < n:
                    table[j] = min(table[j], table[i] + 1)
        return table[n - 1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

The sweep pairs each index with up to `nums[i]` landing spots, and the sum of all jump widths bounds the relaxations; each pair is examined once.

##### Space Complexity: `O(n)`

The `table` stores one number per index.

#### Key Insights

- Seeding at `n` (rather than infinity) is safe because the guarantee of a
  valid answer means the last index is relaxed before the sweep ends.
- The sweep's correctness rests on fill order: `table[i]` is final before it
  relaxes anything, since jumps only go right.
- The whole table is a staircase of plateaus: every spot inside one jump of
  the start carries cost `1`, every spot inside one jump of those carries
  cost `2`, and so on. The Greedy reads exactly that staircase without
  building it.

### Greedy

#### Derivation

The table holds a staircase of plateaus, and a route only ever cares about where one plateau ends and the next begins. During the current jump's window, `current_end` marks where it must land by, and scanning the window records `farthest`, the best spot any of its members could reach. The moment the scan walks past `current_end`, the jump is spent: the next jump's window now runs as far as `farthest`, and one more jump is charged. The window boundaries install the plateau structure without storing it:

1. Start with `jumps = 0`, `current_end = 0` (the empty first window), and
   `farthest = 0`.
2. Scan `i` from `0` to `n - 2`; update `farthest = max(farthest, i + nums[i])`.
3. When `i == current_end`, the current jump's window is spent: increment
   `jumps` and extend `current_end` to `farthest`.
4. After the scan, `jumps` is the minimum jump count.

The last index is excluded from the scan on purpose: standing there means the journey is over, and charging a jump for reaching it would overcount by one.

#### Walkthrough

Trace Example 1: `nums = [2, 4, 1, 1, 1, 1]`:

```text
start    jumps = 0, current_end = 0, farthest = 0
i = 0    farthest = max(2, 0 + 2) = 2;  i == current_end -> jump 1 lands, window extends to 2
i = 1    farthest = max(5, 1 + 4) = 5;  inside the window, keep scanning
i = 2    farthest = max(5, 2 + 1) = 5;  i == current_end -> jump 2 lands, window extends to 5
i = 3    farthest = max(5, 3 + 1) = 5;  inside the window, keep scanning
i = 4    farthest = max(5, 4 + 1) = 5;  inside the window, keep scanning
-> jumps = 2
```

The first jump's window is just `{0}`; landing on `1` opens a window that reaches `5`, the last index, so the second jump finishes the route: `jumps = 2`, matching the expected Output for Example 1. On Example 2 (`nums = [2, 1, 2, 1, 0]`) the same sweep charges its second jump at `i = 2` (`2 + 2 = 4`) and also returns `2`.

#### Solution

The code is the walkthrough's window scan: extend `farthest`, charge a jump when the window is spent.

```python
from typing import List


class Solution:
    def jump(self, nums: List[int]) -> int:
        jumps = 0
        current_end = 0
        farthest = 0
        for i in range(len(nums) - 1):
            farthest = max(farthest, i + nums[i])
            if i == current_end:
                jumps += 1
                current_end = farthest
        return jumps
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One forward pass with a constant-time update per index.

##### Space Complexity: `O(1)`

Three integers of state, regardless of input length.

#### Key Insights

- Charging a jump exactly when `i == current_end` is the BFS in disguise:
  windows are BFS levels, `farthest` is the next level's frontier, and `jumps`
  counts levels. The sorted-by-nothing input order never matters because
  reachability windows are contiguous.
- Scanning to `n - 2` rather than `n - 1` is what keeps the count honest: a
  jump is charged for leaving a window, not for arriving at the destination.
- No explicit route is kept. When the count is all that is asked, the frontier
  summary carries strictly more information than the answer needs, which is
  why the space collapses to constants.

## Comparison of Solutions

The practice harness's `practice/jump_game_ii/reference.py` implements the **Greedy** solution.

### Time Complexity

- **Brute Force**: `O(2^n)` - every route is priced to prove the cheapest is cheapest.
- **Top-Down Memoization**: `O(n^2)` - one body per index, trying up to `nums[i]` steps.
- **Bottom-Up DP**: `O(n^2)` - one relaxation per index/landing pair.
- **Greedy**: `O(n)` - one forward pass, constant work per index.

### Space Complexity

- **Brute Force**: `O(n)` - recursion stack only.
- **Top-Down Memoization**: `O(n)` - memo numbers plus the stack.
- **Bottom-Up DP**: `O(n)` - the `table` array.
- **Greedy**: `O(1)` - three integers.

### Trade-offs

- The Brute Force is the direct transcription of "one jump plus the rest" and
  the easiest version to trust, but it is the only one here that misses the
  constraint budget.
- Both `O(n^2)` versions produce per-index answers, which variants asking
  "how many jumps to each index" get for free; the Greedy computes only the
  total.
- The Greedy drops the tables for a frontier summary, gaining a linear pass
  and constant space at the cost of trusting that windows, not spots, are the
  right unit of bookkeeping.

### When to Use Each

- **Brute Force**: as the derivational baseline and a correctness oracle for
  checking the faster versions on tiny inputs.
- **Top-Down Memoization**: when the recursive pricing is easiest to trust and
  inputs stay modest.
- **Bottom-Up DP**: when per-index jump counts are wanted, or as the form that
  makes the plateau staircase visible.
- **Greedy** (recommended): the default; one pass, constant space, and the
  BFS-level structure read directly off the scan.

### Optimization Notes

- The Greedy is level-order BFS with the queue deleted: windows are levels,
  `current_end` is the current level's end, `farthest` is the next level's
  end, and `jumps` is the level count. Naming that mapping is the cleanest
  correctness argument the approach has.
- `current_end` starts at `0`, so the first scan position `i = 0` immediately
  charges the first jump; the loop bound `n - 1` then guarantees the last
  index never charges one, which is why no arrival adjustment is needed.
- On inputs with a frozen index inside a window (`nums[i] = 0` mid-window) the
  Greedy still works: a frozen index extends `farthest` by nothing, and the
  guarantee of a valid answer means some other window member reaches past it.
- The two Jump Game greedies differ in direction, not family: this one walks
  forward counting level boundaries, Jump Game walks backward dragging one
  target, and both replace the reachability table with a single summary.
