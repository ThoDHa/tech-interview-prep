# [Make Value Groups Contiguous](https://www.fastprep.io/problems/amazon-make-value-groups-contiguous)

**Medium** | **NN minutes** | **Array, Hash Table, Greedy**

You are given an integer array arr. In one operation, choose two values x and y (where y may be any value, including an existing value in the array), and replace every occurrence of x in the array with y.

An array is called contiguous by value if, for every distinct value present, all occurrences of that value appear in one uninterrupted block with no other values in between.

Return the minimum number of operations needed to make the array contiguous by value.

Function Description Complete the function minOperationsToMakeValuesContiguous in the editor below.

minOperationsToMakeValuesContiguous has the following parameter:

int[] arr: the input arrayReturns int: the minimum number of replacement operations

## Examples

### Example 1

**Input:** `arr = [1, 2, 1]`

**Output:** `1`

**Explanation:** Replace every 2 with 1 to get [1, 1, 1]. Now the only distinct value, 1, appears in one contiguous block. This requires 1 operation.

### Example 2

**Input:** `arr = [1, 2, 3]`

**Output:** `0`

**Explanation:** Every value already occupies a single contiguous block: 1 appears once, 2 appears once, 3 appears once. No operations are needed.

## Constraints

- `1 <= arr.length <= 105`
- `1 <= arr[i] <= 105`
- `Each operation replaces all occurrences of one chosen value x globally with any chosen value y.`
- `After all operations are complete, each distinct value remaining in the array must appear in a single contiguous block.`
- `The minimum number of operations equals the total number of distinct values minus the maximum number of distinct values that can simultaneously remain unmerged (i.e., each already occupies a single contiguous block in the original array independently of the others).`

## Solutions

### Merge Simulation

#### Derivation

The most literal reading plays the game: look at the array, spot the trouble, and perform one of the permitted operations. The trouble always has the same shape: a value reappears after other values have interrupted it, so one of the interrupting values must be folded away. Folding it into the value sitting immediately left of the reappearance is the natural move, because that left neighbor's block is where the interrupted run wants to continue:

1. Scan `values` (a copy of `arr`, so the caller's array survives) for the
   first `disrupted_position` whose value has been seen before at some
   `last_seen` position and differs from the value at
   `disrupted_position - 1`: a genuine interruption, not just the run
   continuing.
2. When no such position exists, every value occupies one uninterrupted run,
   and the accumulated `operations` is the answer.
3. Otherwise merge: replace every occurrence of `merged_value =
   values[disrupted_position]` with `left_value = values[disrupted_position -
   1]`, and increment `operations`.
4. Repeat. Each merge removes exactly one distinct value (the merged one), so
   the loop runs at most `distinct - 1` times.

Each round costs a full scan plus a full replacement, and the rounds can approach the distinct-value count, which is the quadratic bill this baseline pays for its simplicity.

#### Walkthrough

The examples are too small to show a merge, so this walkthrough uses the tailored array `arr = [4, 2, 4, 3, 2, 5]`, whose span layout earns its keep below as well. Each row is one round: the scan reports the first disrupted position, and the merge folds that value into its left neighbor:

```text
round 0   [4, 2, 4, 3, 2, 5]
          first disruption at position 2 (4 seen at 0, left neighbor is 2)
          merge 4 -> 2:      [2, 2, 2, 3, 2, 5]      operations = 1
round 1   first disruption at position 4 (2 seen at 0, left neighbor is 3)
          merge 2 -> 3:      [3, 3, 3, 3, 3, 5]      operations = 2
round 2   scan finds every run uninterrupted: return 2
```

The result is `2`, which is in fact the minimum for this array (one operation cannot clear both the stray `4` and the stray `2`), and the final `while` scan confirms contiguity before returning. The cost is visible in the round count: each round re-scans an array that changed in exactly one place.

#### Solution

The code is the walkthrough's loop: find the first disruption, merge, repeat.

```python
from typing import List


class Solution:
    def minOperationsToMakeValuesContiguous(self, arr: List[int]) -> int:
        values = list(arr)
        operations = 0
        while True:
            last_seen = {}
            disrupted_position = -1
            for position, value in enumerate(values):
                if value in last_seen and values[position - 1] != value:
                    disrupted_position = position
                    break
                last_seen[value] = position
            if disrupted_position == -1:
                return operations
            left_value = values[disrupted_position - 1]
            merged_value = values[disrupted_position]
            values = [left_value if value == merged_value else value
                      for value in values]
            operations += 1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × d)`

Each round is one `O(n)` scan plus one `O(n)` replacement, and there are at most `d - 1` rounds because every merge erases one of the `d` distinct values; arrays like `[1, 2, 1, 3, 1, 4, ...]` drive the round count toward `d` while `n` stays in the same order, so the product is the honest bound.

##### Space Complexity: `O(n)`

The `values` copy that keeps the caller's array intact; mutating `arr` in place would drop the extra space to `O(1)` at the price of destroying the input.

#### Key Insights

- The disruption test needs both halves: `value in last_seen` catches the reappearance, and `values[position - 1] != value` keeps an ongoing run from being mistaken for one (dropping that second half would loop forever merging a value into itself on inputs like `[2, 2, 3, 2, 2]`).
- Each merge erases exactly one distinct value, which caps the loop at `distinct - 1` rounds and makes the per-round rescan the only cost concern; the merge target is a heuristic, and the count it lands on is justified by the Value Counting solution below.
- The simulation is a correct algorithm but a wasteful one: every round re-reads the whole array to learn something the first and last occurrence positions already encode, which is exactly the information the value-counting solution works from.

### Value Counting over Clean Cuts

#### Derivation

The simulation never asks the question that decides the answer: how many values were already fine? The statement's own note names the target, "the maximum number of distinct values that can simultaneously remain unmerged", and a value is fine precisely when its occurrences form one uninterrupted block in the original array. Blocks of different values either overlap or do not, and non-overlapping blocks can be kept side by side forever, while overlapping ones cannot both survive. So the answer reduces to counting a boundary structure: a cut between positions `cut` and `cut + 1` is clean when no value's span (its first occurrence through its last) crosses it, and the clean cuts partition the array into maximal independent segments, each of which needs `segment_distinct - 1` merges no matter what the neighbors do:

1. Record `first_occurrence[value]` and `last_occurrence[value]` in one pass
   over `arr`.
2. Build `marks` of length `len(arr) + 1`: at each value's first occurrence add
   `+1` to `marks`, at its last occurrence add `-1`, so the running sum of
   `marks` over a prefix counts the value spans currently crossing into the
   next position.
3. Sweep the `len(arr) - 1` cuts: after adding `marks[cut]`, a running sum of
   `active_spans = 0` means no value crosses that cut, a clean cut.
4. Return `distinct - 1 - clean_cuts`: the distinct values split across the
   clean-cut segments, each segment internally collapsing to one value, and
   the segments never interfere.

Two claims make the count exact. First, an operation cannot create trouble across a clean cut: replacing all of a value never moves an element, so a value whose span already fits inside one segment still fits after the operation, and every operation's changes stay inside the span of the merged value, which some segment fully contains. Second, each segment of length `length` holding `segment_distinct` distinct values needs exactly `segment_distinct - 1` merges, since every operation erases one value and one value must remain. The simulation's left-merge rule achieves exactly this per-segment count (each merge inside a segment erases one of its values while leaving the segment's elements in place), so the bound is tight, and the example walkthrough below shows both sides landing on the same number.

#### Walkthrough

Example 1 is one merge deep; the tailored array `arr = [4, 2, 4, 3, 2, 5]` shows the machinery. The spans are `4: (0, 2)`, `2: (1, 4)`, `3: (3, 3)`, `5: (5, 5)`, and the marks accumulate as the cut sweep advances, with `active_spans` the running sum:

| `cut` | `marks[cut]` | `active_spans` | verdict |
| --- | --- | --- | --- |
| 0 | +1 (value 4 starts) | 1 | dirty |
| 1 | +1 (value 2 starts) | 2 | dirty |
| 2 | -1 (value 4 ends) | 1 | dirty |
| 3 | +1, -1 (value 3 starts and ends) | 1 | dirty |
| 4 | -1 (value 2 ends) | 0 | clean |

`distinct = 4`, `clean_cuts = 1`, so the method returns `4 - 1 - 1 = 2`, matching the Merge Simulation's `2` on the same array. The single clean cut at position 4 separates the self-sufficient prefix `[4, 2, 4, 3, 2]` from `[5]`: value `5` needs no merge, the other three values collapse into one, and the segments never interact. (Example 1 gives `marks = [1, 0, -1, 0]`, so cut 0 reads `active_spans = 1` and cut 1 reads `active_spans = 1`: no clean cuts, and the method returns `2 - 1 - 0 = 1`. Example 2 gives `marks = [0, 0, 0, 0]`: both cuts are clean, and the method returns `3 - 1 - 2 = 0`.)

#### Solution

The code is the two bookkeeping passes: spans into marks, then the cut sweep.

```python
from typing import List


class Solution:
    def minOperationsToMakeValuesContiguous(self, arr: List[int]) -> int:
        first_occurrence = {}
        last_occurrence = {}
        for position, value in enumerate(arr):
            first_occurrence.setdefault(value, position)
            last_occurrence[value] = position

        distinct_count = len(first_occurrence)
        marks = [0] * (len(arr) + 1)
        for value in first_occurrence:
            marks[first_occurrence[value]] += 1
            marks[last_occurrence[value]] -= 1

        clean_cuts = 0
        active_spans = 0
        for cut in range(len(arr) - 1):
            active_spans += marks[cut]
            if active_spans == 0:
                clean_cuts += 1

        return distinct_count - 1 - clean_cuts
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Three linear passes: one to record the first and last occurrence of every value, one to fill `marks`, and one to sweep the cuts, each with constant work per position.

##### Space Complexity: `O(n)`

The occurrence maps hold one entry per distinct value (at most `n`) and the `marks` array exactly `len(arr) + 1` slots.

#### Key Insights

- "Contiguous by value" is a property of spans, not of the operation sequence: a value is already correct exactly when its first and last occurrence bound one run, which two dictionary passes decide.
- The clean cut is the unit of independence: it survives every operation, and `distinct - 1 - clean_cuts` is the count of values that must still be erased, one per merge.
- This is a lower bound that comes with a strategy: the simulation's left-merge rule spends exactly one operation per still-dirty value, so bound and construction meet and the answer needs no search.
- The single pass over `arr` to build the occurrence maps is what retires the simulation's rescanning; nothing about the array is read twice, which is the whole `O(n × d)` to `O(n)` win.

## Comparison of Solutions

### Time Complexity

- **Merge Simulation**: `O(n × d)` - up to `d - 1` rounds, each rescanning and rewriting all `n` positions.
- **Value Counting over Clean Cuts**: `O(n)` - three linear passes over the array, with no rescanning.

### Space Complexity

- **Merge Simulation**: `O(n)` - the working copy of the array (constant if the input may be destroyed).
- **Value Counting over Clean Cuts**: `O(n)` - the occurrence maps and the marks array.

### Trade-offs

- **Merge Simulation**: direct and easy to trust, and it hands back a finished array; but its round-based rescanning is quadratic in the worst case, and each round's merge decision hides the global argument for why the count is minimal.
- **Value Counting over Clean Cuts**: one pass, a two-line formula for the answer, and a correctness argument (clean cuts survive everything) that fits in a sentence; it returns only the count, not a transformed array, and needs the span-overlap insight to trust.

### When to Use Each

- **Merge Simulation**: when the task also wants the resulting array, when inputs are known to be small, or when explaining the operation mechanics to an interviewer before optimizing.
- **Value Counting over Clean Cuts (Recommended)**: for the answer itself under `1 <= arr.length <= 10^5`; the linear bound and the tightness argument make it the defensible choice.

### Optimization Notes

- The `marks` diff technique (add at span start, subtract at span end, read the running sum) is the standard span-overlap sweep; the same skeleton solves meeting-room occupancy and calendar coverage problems.
- `active_spans == 0` can only occur at a cut, never at the final position, because the total sum of `marks` is zero once every value has both started and ended; that is why the sweep stops at `len(arr) - 1`.
- The simulation can be driven to the same linear count by iterating first occurrences in sorted-by-first order and counting, at which point it has become the Value Counting solution wearing simulation clothes; the merge-target bookkeeping adds nothing to the count.
- A common pitfall is defining clean cuts with `marks[last_occurrence[value] + 1] -= 1`: that treats a value as still spanning the cut directly after its last occurrence, miscounting single-occurrence values; the subtraction belongs at `last_occurrence[value]` because the sweep reads `marks[cut]` before judging cut `cut`.
