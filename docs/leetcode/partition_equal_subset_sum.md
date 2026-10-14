# [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/)

**Medium** | **30 minutes** | **Array, Dynamic Programming**

**Pattern:** [DP Knapsack/Subset](../patterns/dp_knapsack_subset/intuition.md)

**Algorithm:** [Subset sum problem](https://en.wikipedia.org/wiki/Subset_sum_problem) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem)

**Practice:** [`practice/partition_equal_subset_sum/solution.py`](../../practice/partition_equal_subset_sum/solution.py)

Given an integer array `nums`, return `true` if you can partition the array into two subsets such that the sum of the elements in both subsets is equal.

## Examples

### Example 1

**Input:** `nums = [1,5,11,5]`

**Output:** `true`

**Explanation:** The array can be partitioned as `[1, 5, 5]` and `[11]`.

### Example 2

**Input:** `nums = [1,2,3,5]`

**Output:** `false`

**Explanation:** The array cannot be partitioned into equal sum subsets.

## Constraints

- `1 <= nums.length <= 200`
- `1 <= nums[i] <= 100`

## Deriving the Solution

Two subsets cover the whole array with equal sums exactly when the total is even and some subset sums to `total // 2`: the other subset then holds the rest, which also sums to `total // 2`. Every solution below starts with this reframing, which turns "partition into two equal halves" into a single-target subset-sum question.

1. **Start literal.** Ask the reframed question directly: does any subset sum
   to `target = total // 2`? Decide for each number whether it joins the subset, and try both choices. That enumerates every subset and costs `O(2^n)`: see [Brute Force](#brute-force).
2. **Spot the waste.** Many different include/exclude histories land in the
   same place: the same next index with the same amount of target still unmet. The answer from that point on depends only on the pair `(index, remaining)`, not on how the search got there, yet the brute force re-solves each pair every time it reappears.
3. **Cache it.** Store each `(index, remaining)` answer the first time it is
   computed and reuse it afterward. The same recursion now does at most `n × target` units of work: see [Top-Down Memoization](#top-down-memoization).
4. **Flip the direction.** Instead of asking from the top "can the remaining
   numbers cover what is left?", build up from the bottom "which sums can the numbers seen so far reach?". Feeding numbers in one at a time and growing the reachable sums is the same `n × target` work without recursion. The reachable sums can be stored as a boolean array indexed by sum, in [Bottom-Up DP](#bottom-up-dp), or sparsely as a set of attainable values, in [Reachable Sum Set](#reachable-sum-set).
5. **Pack the row into bits.** A boolean array indexed by sum is just a string
   of bits, so store it as one big integer: adding a number to every reachable sum at once becomes a single shift-and-OR. Same idea, machine-word speed: see [Bitmask DP](#bitmask-dp).
6. **Let the library hold the cache.** Step 3 spends five lines declaring a
   dictionary, reading it on entry, and writing it on exit. Decorating the recursion with `functools.cache` deletes all five while the include/exclude fork and the three base cases stay exactly as the brute force wrote them: the same states, the same bound, less bookkeeping on the page, see [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Brute Force

#### Derivation

The most direct idea is to ask the question literally: can any subset of `nums` add up to exactly half the total? Two subsets have equal sum only when the total is even and one of them sums to `total // 2`, so an odd total returns `False` immediately.

To find such a subset we try every possibility by hand. Walking the array index by index, each number is either included in the chosen subset or left out, and we [recurse](https://en.wikipedia.org/wiki/Recursion_(computer_science)) on both branches:

1. Compute `total = sum(nums)`. If it is odd, return `False`.
2. Set `target = total // 2`.
3. Recurse from index `0` with `remaining = target`. At each index, subtract `nums[i]`
   (include it) or leave `remaining` untouched (exclude it).
4. Succeed when `remaining` reaches `0`; fail when `remaining` goes negative or the
   array runs out before the target is met.

#### Walkthrough

Let us run the recursion by hand on Example 1: `nums = [1, 5, 11, 5]`.

First the setup: `total = sum(nums) = 22`, which is even, so we continue. `target = 22 // 2 = 11`, and we call `search(0, 11)`. Each call tries the include branch first (`search(i + 1, remaining - nums[i])`), and only falls through to the exclude branch if that returns `False`. The tree below indents one level per recursive call, showing `remaining` shrinking as numbers are included:

```text
search(i=0, remaining=11)              include nums[0]=1
  search(i=1, remaining=10)            include nums[1]=5
    search(i=2, remaining=5)           include nums[2]=11 -> remaining=-6
      search(i=3, remaining=-6)        -> False  (remaining < 0)
    search(i=2, remaining=5)           exclude nums[2]=11, try nums[3]=5
      search(i=3, remaining=5)         include nums[3]=5 -> remaining=0
        search(i=4, remaining=0)       -> True   (remaining hit 0)
      search(i=3, remaining=5)         -> True   (include branch)
    search(i=2, remaining=5)           -> True   (after exclude branch)
  search(i=1, remaining=10)            -> True   (include branch)
search(i=0, remaining=11)             -> True   (include branch)
```

Reading the successful path from the top: we include `1` (remaining `11 -> 10`), include `5` (remaining `10 -> 5`), skip `11` (it would drive remaining to `-6`), then include the final `5` (remaining `5 -> 0`). When `remaining` hits `0` at `i=4`, the base case returns `True`, and that `True` bubbles back up through every parent call.

The chosen subset is `{1, 5, 5}`, summing to `11`. The call returns `True`, which matches the expected Output for Example 1, and corresponds to the partition `[1, 5, 5]` and `[11]`.

#### Solution

The code is the walkthrough's recursion written down: the base cases first, then the include/exclude fork.

```python
from typing import List


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)

        # An odd total can never split into two equal halves.
        if total % 2 != 0:
            return False

        target = total // 2

        # Try every subset: at each index, either take nums[i] toward the
        # target or skip it. Succeed the moment the running sum hits target.
        def search(i: int, remaining: int) -> bool:
            if remaining == 0:
                return True
            if remaining < 0 or i == len(nums):
                return False
            # Include nums[i], or exclude it and move on.
            return search(i + 1, remaining - nums[i]) or search(i + 1, remaining)

        return search(0, target)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

Every element forks into an include branch and an exclude branch, so the search tree holds up to `2^n` leaves. The early exits on `remaining <= 0` prune some paths but do not change the worst case.

##### Space Complexity: `O(n)`

The recursion descends one level per element, so the call stack reaches depth `n`. No other storage grows with the input.

#### Key Insights

- This states the problem with zero cleverness: enumerate every subset and check its
  sum against `target`.
- The include/exclude fork is the raw shape that the dynamic programming solutions
  later collapse into overlapping subproblems.
- It is correct but exponential, so it is only viable for tiny inputs; the same states
  (a given index with a given remaining target) get recomputed across many branches.

### Top-Down Memoization

#### Derivation

The brute force pays for its honesty: the same subproblem is solved over and over. The observation that saves it is that a call to `search(i, remaining)` depends only on its two arguments: which index comes next and how much of the target is still unmet. Different include/exclude histories that arrive at the same `(i, remaining)` pair face the exact same subproblem, so computing it more than once is wasted work. The fix is a [cache](https://en.wikipedia.org/wiki/Memoization) keyed on that pair, wrapped around the otherwise unchanged recursion:

1. Compute `total = sum(nums)`. If it is odd, return `False`.
2. Set `target = total // 2` and recurse from `search(0, target)`, exactly as the
   Brute Force does.
3. Before branching, look up `(i, remaining)` in the memo dictionary; on a hit, return
   the stored answer without recursing.
4. Otherwise evaluate the include branch (`search(i + 1, remaining - nums[i])`) and the
   exclude branch (`search(i + 1, remaining)`), store the result under `(i, remaining)`, and return it.

The index ranges over `n + 1` values and `remaining` over `target + 1` values, so the cache admits at most `(n + 1) × (target + 1)` distinct states. Each state is computed once; every revisit is a dictionary lookup. That single change collapses the `O(2^n)` search tree into pseudo-polynomial work, and it is the recursive twin of the Bottom-Up DP below: the memo holds the same information as the classic 2D `dp[i][s]` table, filled lazily on demand instead of row by row. The recursion depth is bounded by `n` (at most 200 under the constraints), so no recursion-limit adjustment is needed.

#### Walkthrough

Example 1 succeeds so quickly that no state is ever revisited, and Example 2 exits at the parity check, so neither exercises the memo. To see a cache hit we use a small tailored input instead: `nums = [2, 2, 2]`, where `total = 6` is even, `target = 3`, and no subset of even numbers can reach an odd target.

The trace below indents one level per call. States are stored in the memo as they resolve, and the marked line shows the search reaching a state it has already solved:

```text
search(i=0, remaining=3)               include nums[0]=2
  search(i=1, remaining=1)             include nums[1]=2 -> remaining=-1
    search(i=2, remaining=-1)          -> False  (remaining < 0)
    search(i=2, remaining=1)           exclude nums[1], include nums[2]=2
      search(i=3, remaining=-1)        -> False  (remaining < 0)
      search(i=3, remaining=1)         -> False  (out of numbers)
    search(i=2, remaining=1)           -> False, memo[(2, 1)] = False
  search(i=1, remaining=1)             -> False, memo[(1, 1)] = False
  search(i=1, remaining=3)             exclude nums[0]=2
    search(i=2, remaining=1)           -> False  ** memo hit, no recursion **
    search(i=2, remaining=3)           include/exclude nums[2]=2 both fail
      search(i=3, remaining=1)         -> False  (out of numbers)
      search(i=3, remaining=3)         -> False  (out of numbers)
    search(i=2, remaining=3)           -> False, memo[(2, 3)] = False
  search(i=1, remaining=3)             -> False, memo[(1, 3)] = False
search(i=0, remaining=3)               -> False, memo[(0, 3)] = False
```

The state `(2, 1)` is reached twice: once through "include `nums[0]`, exclude `nums[1]`" and once through "exclude `nums[0]`, include `nums[1]`". The first visit computes it and stores `False`; the second visit answers from the memo without recursing. On this tiny input that saves only a few calls, but on adversarial inputs the same mechanism collapses an exponential tree into at most `n × target` computed states. The final answer is `False`: `[2, 2, 2]` cannot split into equal halves.

#### Solution

The code is the Brute Force solution with the memo lookup and store wrapped around the fork; nothing else changes.

```python
from typing import List


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)

        # An odd total can never split into two equal halves.
        if total % 2 != 0:
            return False

        target = total // 2

        # memo[(i, remaining)] records whether some subset of nums[i:] can
        # sum to exactly remaining.
        memo = {}

        # The same include/exclude recursion as the Brute Force, with a cache.
        def search(i: int, remaining: int) -> bool:
            if remaining == 0:
                return True
            if remaining < 0 or i == len(nums):
                return False
            if (i, remaining) in memo:
                return memo[(i, remaining)]
            # Include nums[i], or exclude it and move on.
            result = search(i + 1, remaining - nums[i]) or search(i + 1, remaining)
            memo[(i, remaining)] = result
            return result

        return search(0, target)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × target)`

There are at most `(n + 1) × (target + 1)` distinct `(index, remaining)` states, and each is fully evaluated exactly once: outside its two recursive calls, a state does `O(1)` work. Every subsequent visit to a cached state costs one `O(1)` dictionary lookup, and each computed state spawns at most two child calls, so total work is bounded by the state count.

##### Space Complexity: `O(n × target)`

The memo dictionary can grow to one entry per reachable `(index, remaining)` state, up to `(n + 1) × (target + 1)` entries. The recursion stack adds `O(n)` on top, since each call advances the index by one; the memo term dominates.

#### Key Insights

- The state `(index, remaining)` is a complete description of a subproblem: nothing
  about how the recursion got there changes the answer, which is what makes the states cacheable.
- Remaining targets repeat because many different subsets of the prefix produce the
  same partial sum; the memo collapses all of those branches onto one entry, turning `2^n` paths into at most `n × target` states.
- This is the memoized form of the 0/1 knapsack decision problem: index plays the item
  dimension and `remaining` plays the capacity dimension of the classic `dp[i][s]` table, which the Bottom-Up DP fills exhaustively and this approach fills only where the search actually lands.
- Writing the dictionary out by hand costs five lines of lookup and store, and
  buys the ability to shape the key or inspect the table mid-run; when neither is needed, `functools.cache` performs the identical lookup and store for free (see [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache)).
- The base cases (`remaining == 0`, `remaining < 0`, index exhausted) are
  identical to the Brute Force, which is the sign that memoization added a cache rather than a new algorithm.

### Bottom-Up DP

#### Derivation

The memoized recursion still asks the question from the top: "can the numbers from index `i` onward cover what remains?". Turn the question around and build the answer from the bottom instead: "which sums can the numbers seen so far reach?". Starting from the empty subset (sum `0`) and feeding in one number at a time, every reachable sum either stays as it is (the new number is left out) or grows by the new number (it is taken). This is the textbook 0/1 subset-sum [dynamic program](https://en.wikipedia.org/wiki/Dynamic_programming).

Let `dp[s]` be `True` when some subset of the numbers seen so far sums to `s`, so each number updates the row as `dp[s] = dp[s] or dp[s - num]`:

1. Initialize `dp` of size `target + 1` with `dp[0] = True` (the empty subset).
2. For each `num`, update `dp[s]` for `s` from `target` down to `num`. Iterating
   downward ensures `dp[s - num]` still refers to a state without the current `num`, enforcing the 0/1 (use-each-element-once) constraint.
3. Return `dp[target]`.

#### Recurrence

A split into two equal halves exists only when the total is even and some subset hits exactly half of it:

$$ \text{target} = \frac{1}{2}\sum_{i=0}^{n-1} \text{nums}[i] $$

```text
target = (sum over i = 0 to n - 1 of nums[i]) / 2
         (only defined when that sum is even)
```

Let \(dp_k[s]\) be true when some subset of the first `k` numbers sums to `s`. Each number is either taken or left:

$$ dp_k[s] = dp_{k-1}[s] \ \vee \ dp_{k-1}[s - \text{nums}[k-1]], \qquad dp_0[s] = [\,s = 0\,] $$

```text
dp_0[s] = (s == 0)
dp_k[s] = dp_(k-1)[s] or dp_(k-1)[s - nums[k - 1]]
          (second term only when s >= nums[k - 1])
```

The code keeps a single row and walks `s` downward, so every read of \(dp[s - \text{num}]\) still refers to row \(k-1\). Iterating upward would let one number be reused within the same pass, which solves the *unbounded* knapsack instead of the 0/1 one this problem needs. The answer is \(dp_n[\text{target}]\).

#### Walkthrough

Let us fill the row by hand on Example 1: `nums = [1, 5, 11, 5]`, so `total = 22`, `target = 11`, and `dp` has 12 entries. Rather than printing twelve booleans per line, each snapshot lists the indices currently holding `True`, which are exactly the sums reachable so far:

```text
start           dp true at {0}                      only the empty subset
num = 1         dp true at {0, 1}                   dp[1] |= dp[0]
num = 5         dp true at {0, 1, 5, 6}             dp[6] |= dp[1], dp[5] |= dp[0]
num = 11        dp true at {0, 1, 5, 6, 11}         dp[11] |= dp[0]
num = 5         dp true at {0, 1, 5, 6, 10, 11}     dp[10] |= dp[5]; dp[11] stays
```

Each pass sweeps `s` from `11` down to `num`, marking `dp[s]` wherever `dp[s - num]` was already `True`. After the `11` pass, `dp[11]` is set because `dp[0]` was: the subset `{11}` reaches the target. The final `5` also re-derives `dp[11]` through `dp[6]`, matching the subset `{1, 5, 5}` found by the Brute Force.

The function returns `dp[11] = True`, matching the expected Output for Example 1.

#### Solution

The code is the row update from the walkthrough: one downward sweep of `dp` per number.

```python
from typing import List


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)

        # An odd total can never split into two equal halves.
        if total % 2 != 0:
            return False

        target = total // 2

        # dp[s] is True when some subset of the processed numbers sums to s.
        dp = [False] * (target + 1)
        dp[0] = True  # The empty subset sums to 0.

        for num in nums:
            # Walk downward so each number is used at most once (0/1 knapsack).
            for s in range(target, num - 1, -1):
                if dp[s - num]:
                    dp[s] = True

        return dp[target]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × target)`

Each of the `n` numbers sweeps the `dp` array of size `target + 1`. Since `target = total // 2`, this is `O(n × total)`: pseudo-polynomial in the sum.

##### Space Complexity: `O(target)`

A single boolean array of `target + 1` entries, reused across all numbers.

#### Key Insights

- The downward inner loop is what distinguishes 0/1 knapsack (each item once) from
  unbounded knapsack (an upward loop would let a number be reused).
- Rolling the classic 2D `dp[i][s]` table down to one row is safe precisely because
  the update only reads smaller indices of the previous state.
- The parity check is a free early exit that also guarantees `target` is an integer.

### Reachable Sum Set

#### Derivation

The Bottom-Up DP row is mostly `False` early on: it burns a full sweep of `target + 1` entries per number even when only a handful of sums are reachable. Store only the `True` part instead. A set of reachable sums holds exactly the information the boolean row holds, but iterates over just the sums that actually exist, and it can stop the moment the target appears:

1. Compute `total = sum(nums)`. If it is odd, return `False`.
2. Set `target = total // 2`.
3. Maintain a set `reachable` of achievable subset sums, seeded with `0` (the empty
   subset).
4. For each `num`, extend every existing reachable sum by `num`. If any reaches
   `target`, return `True`. Discard sums that exceed `target`, since they can never contribute to a valid partition.
5. After processing all numbers, return whether `target` was reached.

Capping reachable sums at `target` keeps the set bounded by `target + 1` distinct values, which is what gives the algorithm the same pseudo-polynomial bound as the row-based DP. Building `next_reachable` as a copy before extending is the set counterpart of the DP's downward sweep: additions in this pass never feed on each other, so each number is used at most once.

#### Walkthrough

Let us grow the set by hand on Example 1: `nums = [1, 5, 11, 5]`, so `total = 22` and `target = 11`. Each line shows the set after processing one number:

```text
start           reachable = {0}                     the empty subset
num = 1         reachable = {0, 1}                  0+1=1
num = 5         reachable = {0, 1, 5, 6}            0+5=5, 1+5=6
num = 11        0 + 11 = 11 == target -> return True
```

Processing `11`, the very first extension `0 + 11` hits the target, so the function returns `True` immediately without touching the final `5`. The witnessing subset is `{11}`, whose complement `{1, 5, 5}` also sums to `11`: exactly the partition from the Explanation of Example 1.

#### Solution

The code is the set growth from the walkthrough, with the early exit on hitting `target` and the cap that discards larger sums.

```python
from typing import List


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)

        # An odd total can never split into two equal halves.
        if total % 2 != 0:
            return False

        target = total // 2

        # reachable holds every subset sum we can form so far.
        # Start with 0 (the empty subset).
        reachable = {0}

        for num in nums:
            next_reachable = set(reachable)
            for partial_sum in reachable:
                new_sum = partial_sum + num
                if new_sum == target:
                    return True
                if new_sum < target:
                    next_reachable.add(new_sum)
            reachable = next_reachable

        return target in reachable
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × target)`

We process each of the `n` numbers once, and for each we iterate over the reachable set, which holds at most `target + 1` distinct values. Since `target = total // 2`, this is `O(n × total)` work overall: pseudo-polynomial in the sum of the elements.

##### Space Complexity: `O(target)`

The reachable set stores at most `target + 1` distinct subset sums.

#### Key Insights

- Equal partition is impossible unless the total is even, so the parity check is a
  free early exit that also guarantees `total // 2` is an integer.
- The problem reduces to a 0/1 subset-sum decision against the single target
  `total // 2`; each element is used at most once.
- Pruning sums above `target` bounds the state space and prevents wasted work.
- This reachable-set formulation is the dynamic programming recurrence in disguise:
  the Bottom-Up DP approach makes the same `dp[s]` explicit, while the Bitmask DP approach below packs it into a single integer.

### Bitmask DP

#### Derivation

The Bottom-Up DP row is a sequence of booleans indexed by sum, and a sequence of booleans is exactly what the bits of an integer are. Pack the whole row into one Python integer, with bit `s` playing the role of `dp[s]`. The payoff is that adding `num` to every reachable sum at once is a single shift: `bits << num` moves every set bit up by `num`, and OR-ing that back in keeps the old sums too. Python's arbitrary-precision integers make this a clean, fast formulation:

1. Start with `bits = 1`, meaning only sum `0` is reachable (bit 0 set).
2. For each `num`, `bits << num` shifts every currently reachable sum up by `num`;
   OR-ing it back in (`bits |= bits << num`) records all the new reachable sums in a single machine-word-parallel operation.
3. After processing every number, test bit `target` with `(bits >> target) & 1`.

#### Walkthrough

Let us follow the integer on Example 1: `nums = [1, 5, 11, 5]`, `target = 11`. Each line shows the operation and the positions of the set bits afterward, which are the reachable sums:

```text
start        bits = 1               set bits {0}
num = 1      bits |= bits << 1      set bits {0, 1}
num = 5      bits |= bits << 5      set bits {0, 1, 5, 6}
num = 11     bits |= bits << 11     set bits {0, 1, 5, 6, 11, 12, 16, 17}
num = 5      bits |= bits << 5      set bits {0, 1, 5, 6, 10, 11, 12, 16, 17, 21, 22}
```

The `11` pass shifts `{0, 1, 5, 6}` up to `{11, 12, 16, 17}` and merges the two sets, setting bit `11` (the subset `{11}`). Unlike the capped set solution, sums above the target such as `12`, `16`, and `22` are carried along: they are harmless because only bit `11` is inspected at the end.

The final test `(bits >> 11) & 1` extracts a `1`, so the function returns `True`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's shift-and-OR, applied once per number.

```python
from typing import List


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)

        # An odd total can never split into two equal halves.
        if total % 2 != 0:
            return False

        target = total // 2

        # Bit s of `bits` is set when some subset sums to s; only sum 0 starts set.
        bits = 1
        for num in nums:
            # Shifting left by num marks every (reachable sum + num) at once.
            bits |= bits << num

        # The answer is whether the target bit ended up set.
        return (bits >> target) & 1 == 1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × target / w)`

Each of the `n` shifts/ORs operates on a `target`-bit integer, which the interpreter processes in machine words of width `w`. The asymptotic class matches the table DP, but the per-bit constant factor is dramatically smaller.

##### Space Complexity: `O(target)`

A single integer holding `target + 1` significant bits.

#### Key Insights

- Bit `s` being set is exactly `dp[s]`; the shift-and-OR is the recurrence
  `dp[s] |= dp[s - num]` applied to all `s` simultaneously.
- Unlike the explicit downward loop, the bitset never risks reusing a number within
  one step because the shift reads the pre-update value of `bits`.
- This is the most concise and fastest approach in Python, but it leans on
  big-integer bit tricks and is less transparent than the table.

### Top-Down Memoization with functools.cache

#### Derivation

The recursion is the algorithm, and none of it changes here: the same include/exclude fork over the same `(index, remaining)` state, guarded by the same three base cases the Brute Force wrote. Only the bookkeeping moves. [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) wraps a function in an unbounded dictionary keyed on its arguments, consulting that dictionary before the body runs and storing the return value after, which is precisely what the explicit `memo` did with the `(i, remaining)` pair. Both arguments are integers, so they hash directly and the decorator builds the key without any help.

1. Compute `total = sum(nums)`. If it is odd, return `False`.
2. Set `target = total // 2`, exactly as every approach above does.
3. Decorate the inner `search` with `@cache`, then write its body as the Brute
   Force wrote it: `True` at `remaining == 0`, `False` at `remaining < 0` or an exhausted index, and otherwise the include/exclude fork.
4. Call `search(0, target)`. Each distinct `(i, remaining)` pair runs the body
   once, and every repeat is answered from the decorator's dictionary before the body is entered.

Five lines vanish: the `memo = {}` declaration, the two-line lookup, and the two-line store. What remains on the page is the recursion and its base cases. Defining `search` inside `canPartition` also keeps the cache per call, so it is discarded with the frame and never grows across inputs; decorating a method instead would retain every entry for the process lifetime and pin `self` in memory along with them.

#### Walkthrough

Let us run the decorated recursion on Example 1: `nums = [1, 5, 11, 5]`. The total is `22`, which is even, so `target = 11` and the search starts at `search(0, 11)`. The trace indents one level per call, and each line records whether the decorator ran the body (a miss) or answered from its dictionary:

```text
search(i=0, remaining=11)         miss: include nums[0]=1
  search(i=1, remaining=10)       miss: include nums[1]=5
    search(i=2, remaining=5)      miss: include nums[2]=11 -> remaining=-6
      search(i=3, remaining=-6)   miss -> False  (remaining < 0)
      search(i=3, remaining=5)    miss: exclude nums[2], include nums[3]=5
        search(i=4, remaining=0)  miss -> True   (remaining hit 0)
      search(i=3, remaining=5)    -> True
    search(i=2, remaining=5)      -> True
  search(i=1, remaining=10)       -> True
search(i=0, remaining=11)         -> True
```

Every call on this input is a first visit, because trying the include branch first walks straight to the subset `{1, 5, 5}` without ever backtracking into a state already solved. Asking the decorator confirms it: `search.cache_info()` reports `hits=0, misses=6` with six entries stored. Feed the same code the `nums = [2, 2, 2]` input from the Top-Down Memoization walkthrough and it reports `hits=2, misses=9`, one of those hits landing on the same `(2, 1)` state the explicit memo caught. The counts differ slightly from that section because the decorator wraps the whole body and therefore stores the base-case states too, which the hand-written memo returned before ever reaching its store. Here the call returns `True`, matching the expected Output `true` for Example 1.

#### Solution

The Brute Force recursion character for character, with one decorator line above it doing what the memo lookup and store did.

```python
from functools import cache
from typing import List


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)

        # An odd total can never split into two equal halves.
        if total % 2 != 0:
            return False

        target = total // 2

        # @cache keys on (i, remaining), the same pair the memo dictionary
        # stored, and both arguments are integers so they hash directly.
        @cache
        def search(i: int, remaining: int) -> bool:
            if remaining == 0:
                return True
            if remaining < 0 or i == len(nums):
                return False
            # Include nums[i], or exclude it and move on.
            return search(i + 1, remaining - nums[i]) or search(i + 1, remaining)

        return search(0, target)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × target)`

The reachable states are unchanged: at most `(n + 1) × (target + 1)` distinct `(index, remaining)` pairs, each running its body once and doing `O(1)` work outside its two recursive calls. The decorator's lookup hashes a two-integer tuple, which is `O(1)`, so it replaces the manual `in memo` test at the same cost and leaves the bound untouched.

##### Space Complexity: `O(n × target)`

The decorator's dictionary holds one entry per computed state, up to `(n + 1) × (target + 1)` of them, and the recursion stack adds `O(n)` beneath it. The key is the same `(i, remaining)` tuple the manual memo built, so the per-entry footprint is effectively unchanged and the dictionary term dominates either way.

#### Key Insights

- Decorating the Brute Force recursion produces the memoized solution outright,
  which shows how little of memoization is algorithm: the states, the fork, and the base cases are all already present in the exponential version.
- `functools.cache` requires hashable arguments, and this recursion passes two
  integers, so it qualifies with nothing to work around. A recursion that carried the candidate list itself would raise `TypeError` on the first call.
- The cache is unbounded, which is the right choice here because the state space
  is capped at `(n + 1) × (target + 1)` and the constraints bound `target` at `100 × 200 / 2 = 10000`; `lru_cache(maxsize=...)` would only add eviction bookkeeping and risk evicting states the search still needs.
- Attaching the cache to a function nested inside `canPartition` keeps it
  per call, so repeated calls on different inputs neither share stale entries nor leak memory the way a decorated method would.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(2^n)` - fork into include/exclude at every element.
- **Top-Down Memoization**: `O(n × target)` - compute each `(index, remaining)` state once.
- **Bottom-Up DP**: `O(n × target)` - sweep the boolean array per number.
- **Reachable Sum Set**: `O(n × target)` - iterate the bounded set per number.
- **Bitmask DP**: `O(n × target / w)` - same class with a small bitwise constant factor.
- **Top-Down Memoization with functools.cache**: `O(n × target)`, the same states
  computed once each, with the decorator hashing a two-integer tuple per call.

### Space Complexity

- **Brute Force**: `O(n)` - recursion stack depth proportional to the element count.
- **Top-Down Memoization**: `O(n × target)` - memo dictionary plus an `O(n)` recursion stack.
- **Bottom-Up DP**: `O(target)` - one boolean array.
- **Reachable Sum Set**: `O(target)` - at most `target + 1` distinct sums.
- **Bitmask DP**: `O(target)` - one integer of `target + 1` bits.
- **Top-Down Memoization with functools.cache**: `O(n × target)`, the decorator's
  dictionary plus the same `O(n)` recursion stack.

### Trade-offs

- The Brute Force approach is the most direct statement of the problem (enumerate every
  subset) but recomputes overlapping states, making it exponential.
- The Top-Down Memoization approach keeps the Brute Force recursion intact and computes
  only the states the search reaches, but pays dictionary and call overhead and stores the full two-dimensional `(index, remaining)` state space.
- The Bottom-Up DP approach is the clearest expression of the
  0/1 knapsack recurrence and the easiest to adapt to variants.
- The Reachable Sum Set approach reads naturally and prunes eagerly, but set objects
  carry more per-element overhead than a flat array.
- The Bitmask DP approach is the fastest and most compact, at the cost of relying on
  big-integer bit manipulation that is harder to read.
- The Top-Down Memoization with functools.cache approach is the same solution with
  five lines of dictionary handling deleted, so the recursion stands alone on the page. It gives up direct access to the table, which matters when the key needs custom shaping or when the entries have to be inspected or reused after the call.

### When to Use Each

- **Brute Force**: Only for tiny inputs or to reason about the problem; it captures the
  include/exclude structure that Top-Down Memoization caches and the DP solutions tabulate.
- **Top-Down Memoization**: When the recursive framing feels more natural, or when the
  states reachable from the target are sparse enough that filling the whole table would be wasted work.
- **Bottom-Up DP**: The default choice for clarity and for
  explaining the knapsack structure.
- **Reachable Sum Set**: When a set-based formulation is more intuitive or when most
  sums stay sparse relative to `target`.
- **Bitmask DP**: When performance matters most in Python and the bitwise idiom is
  acceptable.
- **Top-Down Memoization with functools.cache**: The Pythonic default whenever the
  recursive framing is the one you want. It reads as the plain recursion plus a decorator, so reach for it over the hand-written memo unless the exercise is specifically to demonstrate how caching works, or unless the state table itself must be examined afterwards.

### Optimization Notes

- The Brute Force search recomputes the same `(index, remaining)` states across many
  branches; caching those states is exactly the Top-Down Memoization approach, and it is what turns the search polynomial.
- The four polynomial approaches share the same pseudo-polynomial `O(n × target)` time
  class; the differences are constant factors, memory, and readability.
- Memoization stores the full `(index, remaining)` state space; the Bottom-Up DP
  collapses it to a single `O(target)` row because each update reads only the previous state, which is why the table approaches win on space.
- The downward inner loop in the table approach is the crucial detail that keeps the
  recurrence 0/1; an upward loop would silently solve the unbounded-knapsack variant.
- The bitmask formulation is typically the fastest in practice because CPython
  performs the shift and OR on wide machine words rather than per-element Python loops.
- `functools.cache` is the shortest route to the memoized bound: it changes no
  states and no complexity, only which code performs the lookup and the store, so it costs nothing to prefer it over writing the dictionary out.
- Recursion depth stays within `n` (at most 200 under the constraints) in both
  top-down forms, so neither needs `sys.setrecursionlimit`; a variant that recursed once per unit of `remaining` rather than once per index would.
