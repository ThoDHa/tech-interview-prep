# [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/)

**Medium** | **25 minutes** | **Array, Stack, Monotonic Stack**

**Pattern:** [Monotonic Stack](../patterns/monotonic_stack/intuition.md)

**Algorithm:** [Monotonic stack](https://usaco.guide/gold/stacks) · [Stack (abstract data type)](https://en.wikipedia.org/wiki/Stack_(abstract_data_type))

**Practice:** [`practice/daily_temperatures/solution.py`](../../practice/daily_temperatures/solution.py)

You are given an array of integers `temperatures` where `temperatures[i]` represents the daily temperatures on the `ith` day.

Return an array `result` where `result[i]` is the number of days after the `ith` day before a warmer temperature appears on a future day. If there is no day in the future where a warmer temperature will appear for the `ith` day, set `result[i]` to `0` instead.

## Examples

### Example 1

**Input:** `temperatures = [30,38,30,36,35,40,28]`

**Output:** `[1,4,1,2,1,0,0]`

### Example 2

**Input:** `temperatures = [22,21,20]`

**Output:** `[0,0,0]`

## Constraints

- `1 <= temperatures.length <= 100,000`.
- `1 <= temperatures[i] <= 100`

## Deriving the Solution

For each day the question is "how far ahead is the first strictly warmer temperature?": a distance-to-next-larger-element query, one per day. Every solution answers that query for all days at once; they differ in which days are re-scanned to answer it.

1. **Start literal.** For each day, walk forward until a warmer day appears.
   Faithful to the question, but a cold streak forces every one of its days to
   rescan the same run, costing `O(n²)`: see [Brute Force](#brute-force).
2. **Learn from the answer to a later day.** If day `j` needed `d` days to find
   warmth, the days between `i` and `j` colder than `temperatures[i]` can jump
   straight past day `i + 1` to day `i + d`: warmer-than-`i` is warmer-than-them.
   Chaining these jumps still degenerates on adversarial inputs:
   see [Jump Forward](#jump-forward).
3. **Answer in reverse, remembering colder days.** Scan right to left holding
   the indices of days with no warmer day yet seen: a stack of candidates
   ordered by increasing temperature. Each day pops the candidates it dominates
   and reads its answer from the survivor on top. Each index is pushed once and
   popped once: `O(n)`: see [Monotonic Stack (Reverse)](#monotonic-stack-reverse).
4. **The same stack, forward.** Walking left to right, an unresolved day is
   resolved the moment a warmer day arrives: pop every colder day off the stack
   and record its distance. Identical costs, and the resolution order matches
   the input order: see [Monotonic Stack (Forward)](#monotonic-stack-forward).

## Solutions

### Brute Force

#### Derivation

The most direct reading of the question walks forward from each day until a strictly warmer temperature shows up:

1. For each index `i`, set `days = 0`.
2. Scan `j = i + 1, i + 2, ...`; on the first `temperatures[j] > temperatures[i]`,
   set `result[i] = j - i`.
3. If the scan runs off the end, `result[i]` stays `0`.

#### Walkthrough

Trace the forward scans on Example 2: `temperatures = [22,21,20]`, which is the cold streak that hurts this approach:

```text
i=0  temp 22   j=1: 21 > 22? no   j=2: 20 > 22? no   end of array -> 0
i=1  temp 21   j=2: 20 > 21? no   end of array -> 0
i=2  temp 20   no j to scan                        -> 0
```

No later day is ever warmer, so every scan runs to the end and the result is `[0, 0, 0]`, matching the expected Output for Example 2. The scans never share work: day `0`'s scan already compared `21` and `20`, and day `1`'s scan compares `20` again.

#### Solution

The code is the walkthrough's per-day forward scan.

```python
from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        length = len(temperatures)
        result = [0] * length
        for i in range(length):
            for j in range(i + 1, length):
                if temperatures[j] > temperatures[i]:
                    result[i] = j - i
                    break
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

A strictly decreasing input makes every scan run to the array's end, so the nested loops do `n + (n-1) + ... + 1` comparisons.

##### Space Complexity: `O(1)`

Only the loop indices and the pre-sized output are used.

#### Key Insights

- The clearest expression of the question, and the baseline every faster
  approach must beat.
- Fails the constraint sizes: `100,000` strictly decreasing days mean roughly
  five billion comparisons.
- The repeated rescans of shared suffixes are the waste later approaches remove.

### Jump Forward

#### Derivation

The brute force re-walks cold stretches that later scans have already measured. Turn the answer into a shortcut: if day `j` found its warmer day at distance `d = result[j]`, then every day `i < j` with `temperatures[i] < temperatures[j]` knows its answer is either inside `(i, j)` or exactly `j - i`... but if `temperatures[i] >= temperatures[j]`, then the first day warmer than `i` that lies at or beyond `j` is at or beyond `j + result[j]`, so the scan can hop there directly. Chaining these hops walks a path of increasing temperatures instead of stepping one day at a time:

1. Iterate `i` from right to left, so `result[j]` is final before day `i` uses it.
2. Start `j = i + 1`.
3. While `j < n` and `temperatures[j] <= temperatures[i]`, replace `j` with
   `j + result[j]`, hopping over the stretch day `j` already measured as cold.
   A `result[j]` of `0` certifies no warmer day exists anywhere after `j`,
   which settles day `i` at `0` too: jump straight to the end.
4. `result[i] = j - i` when `j < n`, else `0`.

#### Walkthrough

Trace the hops on a tailored input `[73, 74, 71, 75]`, which forces a real hop chain (official Example 1's first day resolves on its first comparison):

```text
i=3  temp 75   j=4 = n                       -> 0
i=2  temp 71   j=3: 75 > 71                  -> 1
i=1  temp 74   j=2: 71 <= 74, hop j=2+1=3; 75 > 74   -> 2
i=0  temp 73   j=1: 74 > 73                  -> 1
```

Day `1` is the one that profits: instead of comparing day `2` (71, colder) day by day, it reads day `2`'s already-final answer (`result[2] = 1`) and lands on day `3` directly, finding 75 warmer after a single hop. The result `[1, 2, 1, 0]` matches the hand-computed expectations.

#### Solution

The code is the right-to-left sweep with the hop chain from the walkthrough.

```python
from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        length = len(temperatures)
        result = [0] * length
        for i in range(length - 2, -1, -1):
            j = i + 1
            # Hop over stretches a later day already measured as cold
            while j < length and temperatures[j] <= temperatures[i]:
                if result[j] == 0:
                    # No warmer day after j means none after i either
                    j = length
                else:
                    j += result[j]
            result[i] = j - i if j < length else 0
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

Crafted inputs can make every hop advance a single day (long stretches of short answers under a cold prefix), degrading repeated chains to quadratic work in the worst case. Random and realistic inputs hop over long stretches, making the sweep fast in practice, close to linear; the zero-answer shortcut removes the degenerate stall a plain `j += result[j]` would suffer.

##### Space Complexity: `O(1)`

Only the loop indices and the pre-sized output are used.

#### Key Insights

- Reuses measured answers as jumps, the same amortizing spirit as path
  compression.
- Its worst case is data-dependent, unlike the stack's guaranteed `O(n)`.
- A stepping stone toward the stack: the insight "day `j`'s answer certifies
  coldness in between" is what the stack encodes structurally.

### Monotonic Stack (Reverse)

#### Derivation

Both slower versions re-examine days whose fate is already decided. The stack version makes "decided" explicit: scanning right to left, a day sits unresolved only while no warmer day has appeared to its right. Holding those unresolved days on a stack of indices, temperatures increasing from bottom to top, each new day pops the candidates it dominates and reads its answer from the survivor on top, an `O(1)` resolution per pop:

1. Walk days right to left with a `stack` of indices and `result` preset to `0`.
2. Pop every keeper that is not strictly warmer than the current day; the top
   that survives is the nearest strictly warmer day to the right.
3. If a keeper survives, set `result[day] = stack[-1] - day`; push `day` and
   continue. Days never popped had no warmer day and keep `0`.

#### Walkthrough

Trace the reverse stack on Example 1: `temperatures = [30,38,30,36,35,40,28]`. Each row shows the day being processed, the pops it triggers, the answer read from the surviving top, and the stack of unresolved indices afterward:

```text
day=6  temp 28   pops: none, stack empty   result[6] = 0           stack [6]
day=5  temp 40   pop 6 (28 <= 40)          result[5] = 0           stack [5]
day=4  temp 35   pops: none, keeper 40     result[4] = 5 - 4 = 1   stack [5, 4]
day=3  temp 36   pop 4 (35 <= 36)          result[3] = 5 - 3 = 2   stack [5, 3]
day=2  temp 30   pops: none, keeper 36     result[2] = 3 - 2 = 1   stack [5, 3, 2]
day=1  temp 38   pop 3 (36 <= 38)          result[1] = 5 - 1 = 4   stack [5, 1]
                 pop 2 (30 <= 38), keeper 40
day=0  temp 30   pops: none, keeper 38     result[0] = 1 - 0 = 1   stack [5, 1, 0]
```

Day `1` (the 38) pops two waiting days in one step, the batching that gives the approach its linearity: those pops are the only times indices `2` and `3` are ever compared again. The loop ends with `[1, 4, 1, 2, 1, 0, 0]` recorded (day `5` keeps its preset `0` because nothing to its right is warmer), matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's pop-then-read-then-push per day, run right to left:

```python
from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        stack = []
        result = [0] * len(temperatures)
        for day in range(len(temperatures) - 1, -1, -1):
            # Pop keepers that are not strictly warmer than the current day
            while stack and temperatures[stack[-1]] <= temperatures[day]:
                stack.pop()
            if stack:
                result[day] = stack[-1] - day
            stack.append(day)
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each index is pushed exactly once and popped at most once, so the while loop's total work across the entire run is bounded by the number of pushes.

##### Space Complexity: `O(n)`

The stack holds every day still lacking a strictly warmer day to its right.

#### Key Insights

- The stack holds exactly the days awaiting a warmer day, which is why nothing
  is ever rescanned.
- The push/pop accounting argument (each index in once, out once) is the proof
  of linearity and recurs across the whole monotonic-stack family.
- Strictness lives on the pop side: popping on `<=` drops equal days, so the
  earlier of two equal days answers.

### Monotonic Stack (Forward)

#### Derivation

The reverse stack resolved each day while walking away from it; the forward
scan runs the same idea in the input's own direction. A day sits unresolved
only while no warmer day has appeared after it. The moment a warmer day `day`
arrives, every unresolved day colder than `temperatures[day]` finds its answer
and leaves. Holding the unresolved days on a stack, coldest-nearest-to-`day` on
top, gives each resolution an `O(1)` pop and keeps the temperatures along the
stack strictly decreasing from bottom to top:

1. Walk days left to right with a `stack` of indices and `result` preset to `0`.
2. While the stack is non-empty and `temperatures[stack[-1]] < temperature`,
   pop `colder_day` and set `result[colder_day] = day - colder_day`.
3. Push `day` and continue; days never popped had no warmer day and keep `0`.

#### Walkthrough

Trace the forward stack on Example 1: `temperatures = [30,38,30,36,35,40,28]`. Each row shows the day being processed, the pops it triggers, and the stack of unresolved indices afterward:

```text
day=0  temp 30   pops: none             stack [0]
day=1  temp 38   pop 0 (30 < 38) -> result[0] = 1
                                        stack [1]
day=2  temp 30   pops: none             stack [1, 2]
day=3  temp 36   pop 2 (30 < 36) -> result[2] = 1
                 38 > 36, stop          stack [1, 3]
day=4  temp 35   pops: none             stack [1, 3, 4]
day=5  temp 40   pop 4 (35 < 40) -> result[4] = 1
                 pop 3 (36 < 40) -> result[3] = 2
                 pop 1 (38 < 40) -> result[1] = 4
                                        stack [5]
day=6  temp 28   pops: none             stack [5, 6]
```

Day `5` (the 40) resolves three waiting days in one step, the batching that gives the approach its linearity: those three pops are the only times indices `1`, `3`, `4` are ever compared again. The loop ends with `[1, 4, 1, 2, 1, 0, 0]` recorded (days `5` and `6` keep their preset `0`), matching the expected Output for Example 1.

#### Solution

The forward variant, the walkthrough's pop-then-push per day:

```python
from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        stack = []
        result = [0] * len(temperatures)
        for day, temperature in enumerate(temperatures):
            # A warmer day resolves every colder day waiting on the stack
            while stack and temperatures[stack[-1]] < temperature:
                colder_day = stack.pop()
                result[colder_day] = day - colder_day
            stack.append(day)
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each index is pushed exactly once and popped at most once, so the while loop's total work across the entire run is bounded by the number of pushes.

##### Space Complexity: `O(n)`

A strictly decreasing suffix fills the stack with every unresolved day.

#### Key Insights

- The stack holds exactly the days awaiting a warmer day, which is why nothing
  is ever rescanned.
- The push/pop accounting argument (each index in once, out once) is the proof
  of linearity and recurs across the whole monotonic-stack family.
- Strictness lives on the pop side: popping on `<` keeps equal days stacked, so
  the later of two equal days answers.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n²)` - each day may rescan the whole suffix.
- **Jump Forward**: `O(n²)` worst case - hop chains stall on non-increasing runs.
- **Monotonic Stack (Reverse)**: `O(n)` - one push and at most one pop per index.
- **Monotonic Stack (Forward)**: `O(n)` - the same push/pop accounting, run left to right.

### Space Complexity

- **Brute Force**: `O(1)` - loop indices only.
- **Jump Forward**: `O(1)` - the answer array doubles as the hop table.
- **Monotonic Stack (Reverse)**: `O(n)` - days without a warmer keeper to the right.
- **Monotonic Stack (Forward)**: `O(n)` - the same unresolved days, held left to right.

### Trade-offs

- The brute force is simple but quadratic, unusable at `100,000` days.
- The jump-forward version rides existing answers and is near-linear on
  realistic data, but carries a data-dependent worst case.
- Both monotonic stacks pay linear memory for a guaranteed linear sweep and are
  the canonical interview answer for next-greater-element questions; the forward
  scan is the usual form, the reverse scan its mirror image.

### When to Use Each

- **Brute Force**: Tiny inputs or as the oracle when testing faster versions.
- **Jump Forward**: When memory is tight and the data is known not to have
  long non-increasing runs.
- **Monotonic Stack (Reverse)**: The default when the answer reads most naturally
  as "nearest warmer day to my right".
- **Monotonic Stack (Forward)**: The default, and the pattern to reach for whenever
  a problem asks for the next element satisfying a comparison; resolution order
  matches the input order (recommended here).

### Optimization Notes

- The output is pre-sized and filled by index, never appended, so both stack
  variants allocate once.
- Equal temperatures are the classic bug: popping on `<` (forward) versus `<=`
  (reverse) decides whether the earlier or later of two equal days answers;
  mixing the conventions silently produces off-by-a-few results.
- The stack can hold indices only, as here; storing `(value, index)` pairs
  doubles memory without changing the algorithm.
