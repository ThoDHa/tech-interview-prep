# [Combination Sum](https://leetcode.com/problems/combination-sum/)

**Medium** | **30 minutes** | **Backtracking**

**Pattern:** [Backtracking](../patterns/backtracking_exploration/intuition.md)

**Algorithm:** [Backtracking](https://en.wikipedia.org/wiki/Backtracking) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming)

**Practice:** [`practice/combination_sum/solution.py`](../../practice/combination_sum/solution.py)

Given an array of **distinct** integers `candidates` and a target integer `target`, return a list of all **unique combinations** of `candidates` where the chosen numbers sum to `target`. You may return the combinations in **any order**.

The **same** number may be chosen from `candidates` an **unlimited number of times**. Two combinations are unique if the frequency of at least one of the chosen numbers is different.

The test cases are generated such that the number of unique combinations that sum up to `target` is less than `150` combinations for the given input.

## Examples

### Example 1

**Input:** `candidates = [2,3,6,7]`, `target = 7`

**Output:** `[[2,2,3],[7]]`

**Explanation:**

```text
2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times.
7 is a candidate, and 7 = 7.
These are the only two combinations.
```

### Example 2

**Input:** `candidates = [2,3,5]`, `target = 8`

**Output:** `[[2,2,2,2],[2,3,3],[3,5]]`

### Example 3

**Input:** `candidates = [2]`, `target = 1`

**Output:** `[]`

## Constraints

- `1 <= candidates.length <= 30`
- `2 <= candidates[i] <= 40`
- All elements of `candidates` are **distinct**.
- `1 <= target <= 40`

## Deriving the Solution

Enumerating combinations rather than permutations is at heart a question about order: `[2,2,3]` and `[2,3,2]` are the same multiset, so every solution must build each combination in exactly one canonical order. All three approaches below share that discipline: once the search or the table moves past a candidate, it never returns to it, so no combination can ever be produced a second way.

1. **Start literal.** At each candidate, branch on a binary decision: include
   `candidates[index]` and stay on the same index (so it can be reused), or exclude it and move to `index + 1`. The exclude branch never revisits earlier candidates, so uniqueness is automatic; the cost is the full exponential decision tree: see [Include-Exclude Backtracking](#include-exclude-backtracking).
2. **Spot the waste.** The binary tree walks doomed branches one exclude at a
   time: once `remaining` drops below every candidate still available, no include can succeed, yet the tree still visits each exclusion step separately.
3. **Sort and prune.** Rewrite the fork as a loop over candidates from `start`
   onward and sort the input first: the moment one candidate exceeds `remaining`, every later one does too, so a single `break` discards the rest of the level: see [Sorted Backtracking with Pruning](#sorted-backtracking-with-pruning).
4. **Build up instead of searching down.** Replace the recursion with a table
   holding, for every sub-target `t`, all combinations summing to `t`, grown one candidate at a time; keeping candidates as the outer loop preserves non-decreasing order, which is what keeps every stored combination unique: see [Bottom-Up Dynamic Programming](#bottom-up-dynamic-programming).

## Solutions

### Include-Exclude Backtracking

#### Derivation

The most direct way to think about the problem is a [binary decision tree](https://en.wikipedia.org/wiki/Backtracking): at each candidate, we either include it (and stay put so it can be used again) or exclude it (and move to the next candidate). This frames the search without needing to sort the input first.

The steps:

1. Recurse with the current `index`, the `remaining` target, and the partial
   `current` combination.
2. If `remaining` reaches `0`, record a copy of `current` as a valid combination.
3. If `remaining` goes negative or we run out of candidates, abandon the branch.
4. Otherwise branch twice: include `candidates[index]` while recursing on the same
   `index` (enabling reuse), then exclude it and recurse on `index + 1`.

Because the "exclude" branch only ever advances the index, no candidate is ever revisited after we move past it. Each combination is therefore produced exactly once in the order its candidates first appear, guaranteeing uniqueness.

#### Walkthrough

Let us watch the Include-Exclude Backtracking code run on Example 1: `candidates = [2,3,6,7]`, `target = 7`. Expected output: `[[2,2,3],[7]]`.

Each call carries three pieces of state: `index` (which candidate we may take next), `remaining` (how much target is left), and `current` (the partial combination built so far). At every live node the code makes two recursive calls: include `candidates[index]` (staying on the same `index` so it can be reused), then exclude it (moving to `index + 1`). A call is recorded when `remaining` hits `0`, and abandoned when `remaining` goes negative or `index` runs off the end.

Below is the call tree, indented by depth. To keep it readable we show the two branches that succeed in full and collapse the overshooting branches to a single `dead` line. The candidates are `[2,3,6,7]`, so `index 0 -> 2`, `index 1 -> 3`, `index 2 -> 6`, `index 3 -> 7`.

```text
backtrack(index=0, remaining=7, current=[])          start: target 7, may take 2
  include 2 -> backtrack(index=0, remaining=5, current=[2])
    include 2 -> backtrack(index=0, remaining=3, current=[2,2])
      include 2 -> backtrack(index=0, remaining=1, current=[2,2,2])
        include 2 -> remaining=-1            dead (overshoot)
        exclude   -> index=1, remaining=1, current=[2,2,2]
          (every choice from here overshoots or runs out)   dead
      exclude   -> backtrack(index=1, remaining=3, current=[2,2])   now may take 3
        include 3 -> backtrack(index=1, remaining=0, current=[2,2,3])
                     remaining==0  ->  RECORD [2,2,3]
        exclude   -> index=2, remaining=3, current=[2,2]
          (6 and 7 both overshoot)                          dead
    exclude   -> backtrack(index=1, remaining=5, current=[2])
      (2+3, 2+6, 2+7 ... none reach 0)                      dead
  exclude   -> backtrack(index=1, remaining=7, current=[])          skip 2 entirely
    include 3 -> ... (3+3+..., 3+6, 3+7 all miss)           dead
    exclude   -> backtrack(index=2, remaining=7, current=[])        skip 2 and 3
      include 6 -> ... (6+anything overshoots)              dead
      exclude   -> backtrack(index=3, remaining=7, current=[])      only 7 left
        include 7 -> backtrack(index=3, remaining=0, current=[7])
                     remaining==0  ->  RECORD [7]
        exclude   -> index=4 (off the end)                  dead
```

Two leaves reached `remaining == 0` and were recorded, in the order they were found: first `[2,2,3]` (build `2 -> 2 -> 3`), then `[7]`. The function returns `result = [[2,2,3],[7]]`, which matches the expected Output.

Notice how reuse and uniqueness both fall out of the index handling: taking `2` three times was possible because the include branch kept `index=0`, while `[7]` was only ever reached through the exclude branches that skipped `2`, `3`, and `6` first. No combination is ever produced twice.

#### Solution

The code is the decision tree from the walkthrough: record at `remaining == 0`, abandon on overshoot, otherwise fork on include and exclude.

```python
from typing import List


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        result: List[List[int]] = []

        def backtrack(index: int, remaining: int, current: List[int]) -> None:
            if remaining == 0:
                result.append(current[:])
                return
            if remaining < 0 or index >= len(candidates):
                return

            # Include candidates[index], staying on the same index to allow reuse.
            current.append(candidates[index])
            backtrack(index, remaining - candidates[index], current)
            current.pop()

            # Exclude candidates[index] and move on to the next candidate.
            backtrack(index + 1, remaining, current)

        backtrack(0, target, [])
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^target)` (loosely; `O(N^(target / min_candidate))` tighter)

Every node makes a binary choice, so the decision tree has up to `2^target` leaves in the worst case. A tighter bound is `O(N^(target / m))` where `N` is the number of candidates and `m` the smallest candidate, since a combination can be at most `target / m` long. Copying each valid combination adds a factor proportional to its length.

##### Space Complexity: `O(target / min_candidate)`

Excluding the output, space is dominated by the recursion stack and the `current` list, both bounded by the maximum combination length `target / min_candidate`.

#### Key Insights

- The include/exclude framing needs no sorting: correctness comes purely from never
  revisiting a candidate on the exclude branch.
- Reuse is captured by recursing on the same `index` in the include branch.
- The `remaining < 0` guard is what stops a branch that has overshot the target.
- Always append a copy (`current[:]`), since `current` is mutated throughout.

### Sorted Backtracking with Pruning

#### Derivation

The include-exclude tree wastes effort in two ways: it walks the exclude decisions one at a time, and it cannot tell when a branch has become hopeless. The same search expressed as a loop repairs both. We explore with the classic ["choose, explore, unchoose"](https://en.wikipedia.org/wiki/Backtracking) pattern, where each call loops over the candidates it may still take, and add one preparation step that unlocks a real prune. Two details make it both correct and efficient:

1. Sort `candidates` ascending. This lets us `break` out of the loop the moment a
   candidate exceeds the remaining target, since every later candidate is at least as large.
2. Pass the current index `i` (rather than `i + 1`) into the recursive call. This
   allows a number to be reused an unlimited number of times while the `start` bound still prevents us from revisiting earlier candidates, which is what avoids counting `[2,3]` and `[3,2]` as distinct combinations.

The steps:

1. Sort the candidates.
2. Recurse with a `start` index, the running `remaining` target, and the partial
   `current` combination.
3. When `remaining` hits `0`, record a copy of `current` as a valid combination.
4. For each candidate from `start` onward, `break` if it exceeds `remaining`,
   otherwise pick it, recurse on the same `i` allowing reuse, then unpick and continue.

Because we only ever move the start index forward, each combination is generated in non-decreasing order exactly once, guaranteeing uniqueness.

#### Walkthrough

Let us run the pruned search on Example 1: `candidates = [2,3,6,7]` (already sorted), `target = 7`. Each call loops `i` upward from its `start`; a `take` line descends one level, and every `break` line kills the remainder of a loop in one stroke. Indices map to candidates as `i=0 -> 2`, `i=1 -> 3`, `i=2 -> 6`, `i=3 -> 7`.

```text
backtrack(start=0, remaining=7, current=[])
  i=0: take 2 -> backtrack(0, 5, [2])
    i=0: take 2 -> backtrack(0, 3, [2,2])
      i=0: take 2 -> backtrack(0, 1, [2,2,2])
        i=0: 2 > 1 -> break                 whole level dies in one test
      i=1: take 3 -> backtrack(1, 0, [2,2,3])
                     remaining == 0 -> RECORD [2,2,3]
      i=2: 6 > 3 -> break
    i=1: take 3 -> backtrack(1, 2, [2,3])
      i=1: 3 > 2 -> break
    i=2: 6 > 5 -> break
  i=1: take 3 -> backtrack(1, 4, [3])
    i=1: take 3 -> backtrack(1, 1, [3,3])
      i=1: 3 > 1 -> break
    i=2: 6 > 4 -> break
  i=2: take 6 -> backtrack(2, 1, [6])
    i=2: 6 > 1 -> break
  i=3: take 7 -> backtrack(3, 0, [7])
                 remaining == 0 -> RECORD [7]
```

Compare the `[2,2,2]` node with its include-exclude counterpart: there, the search still descended an exclude chain before every option died; here, `2 > 1` fails once and the `break` discards candidates `3`, `6`, and `7` unexamined, because sorting guarantees they are even larger. Reuse still comes from recursing on the same `i` (three `2`s in `[2,2,3]`), and `[7]` appears only after the loop has walked past `2`, `3`, and `6`. The two recorded leaves give `result = [[2,2,3],[7]]`, matching the expected Output.

#### Solution

The code is the loop from the walkthrough: sort once, then choose, explore, unchoose, with the `break` prune guarding the loop.

```python
from typing import List


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        # Sort so we can stop a branch as soon as a candidate overshoots.
        candidates.sort()
        result: List[List[int]] = []

        def backtrack(start: int, remaining: int, current: List[int]) -> None:
            if remaining == 0:
                result.append(current[:])
                return

            for i in range(start, len(candidates)):
                candidate = candidates[i]
                # Sorted order: once one candidate is too big, the rest are too.
                if candidate > remaining:
                    break
                current.append(candidate)
                # Pass i (not i + 1) so the same number may be reused.
                backtrack(i, remaining - candidate, current)
                current.pop()

        backtrack(0, target, [])
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N^(target / min_candidate))`

Let `N` be the number of candidates and `m` the smallest candidate. The recursion tree has depth at most `target / m` (the longest a combination can be), and each node branches up to `N` ways. Copying each valid combination costs an additional factor proportional to its length. This exponential bound is expected for an enumeration problem; the sort-and-prune keeps the constant factors low in practice.

##### Space Complexity: `O(target / min_candidate)`

Excluding the output, space is dominated by the recursion stack and the `current` list, both bounded by the maximum combination length `target / min_candidate`.

#### Key Insights

- Reuse is enabled simply by recursing with `i` instead of `i + 1`; the `start`
  index alone enforces uniqueness without any explicit duplicate filtering.
- Sorting unlocks an early `break`, turning a continue-style skip into a true prune
  that cuts entire subtrees.
- Always append a copy (`current[:]`) of the combination, since `current` is mutated
  throughout the search.
- Since all candidates are positive and distinct, no separate visited set or
  same-level duplicate skip is needed (unlike Combination Sum II).

### Bottom-Up Dynamic Programming

#### Derivation

Instead of recursing, we [build up answers for every sub-target](https://en.wikipedia.org/wiki/Dynamic_programming) from `0` to `target`. The outer loop over candidates (rather than an inner loop) is the trick that prevents duplicate combinations: by the time we consider a candidate, every combination already stored uses only earlier candidates, so appending the current candidate keeps each combination in non-decreasing order and unique. The Invariant below states that property formally, along with why the naive `dp[t] = union of dp[t - c] + [c]` relation would over-count.

The steps:

1. Sort the candidates so combinations are built in non-decreasing order.
2. Initialize `dp[0]` with one empty combination; every other `dp[t]` starts empty.
3. For each `candidate`, sweep sub-targets `t` from `candidate` up to `target`.
4. For each combination that sums to `t - candidate`, append `candidate` to form a
   new combination that sums to `t`, and store it in `dp[t]`.
5. Return `dp[target]`.

#### Invariant

This DP is collection-valued: each `dp[t]` holds a *list of combinations* summing to \(t\), not a scalar optimum. There is no honest recurrence to state here, because the obvious one is false. The relation to reach for is a union over the last candidate added:

$$ dp[t] \ \stackrel{?}{=} \bigcup_{\substack{c \,\in\, \text{candidates} \\ c \,\le\, t}} \bigl\{\, \textit{combo} + [c] \ :\ \textit{combo} \in dp[t - c] \,\bigr\} $$

```text
dp[t] =? union of { combo + [c] : combo in dp[t - c] }
         over c in candidates with c <= t
        (the ? marks this relation as FALSE: it is stated only to be refuted)
```

That relation over-counts. With `candidates = [2,3]` and \(t = 5\) it appends `3` to `[2]` drawn from \(dp[2]\), and appends `2` to `[3]` drawn from \(dp[3]\), producing both `[2,3]` and `[3,2]`: two permutations of one combination. The relation carries no notion of candidate order, so nothing in it can rule the duplicate out.

What the code maintains instead is a property of the outer loop. Let \(i\) be the number of sorted candidates processed so far. After each pass of the outer loop:

$$ \forall t,\ \forall \textit{combo} \in dp[t]:\quad \textit{combo} = [\,c_1 \le c_2 \le \cdots \le c_k\,] \quad\text{with every } c_j \in \{\text{candidates}[0], \ldots, \text{candidates}[i-1]\} $$

```text
for all t, for all combo in dp[t]:
    combo == [c_1 <= c_2 <= ... <= c_k]
    with every c_j in {candidates[0], ..., candidates[i-1]}
        (i = sorted candidates processed so far; holds after each outer pass)
```

Every combination stored anywhere in the table draws only on the first \(i\) candidates, and is listed in non-decreasing order.

Both writes to the table preserve it. The initialization `dp[0] = [[]]` holds it trivially at \(i = 0\): the empty combination is non-decreasing and uses no candidate at all. The single append step `dp[t].append(combo + [candidate])` holds it too. Because `candidates` is sorted and processed in order, `candidate` is greater than or equal to every candidate available to a stored `combo`, hence greater than or equal to every element of `combo` itself. Appending it at the *end* therefore keeps the combination non-decreasing, and introduces no candidate from beyond position \(i\).

At loop exit \(i\) is the full candidate count, so `dp[target]` holds every valid combination, each already in canonical non-decreasing order, and each exactly once, since a combination has exactly one non-decreasing listing and the appends can only have built it in that order. No deduplication pass is needed.

This is what makes the loop nesting load-bearing rather than stylistic. Candidates must be the outer loop and sub-targets the inner one. Swap them and each `dp[t]` is finished while later candidates are still unprocessed, so a smaller candidate can be appended after a larger one: the invariant fails, and the permutation duplicates of the naive relation come straight back.

#### Walkthrough

Let us grow the table by hand on Example 1: `candidates = [2,3,6,7]` (already sorted), `target = 7`. `dp[0]` starts as `[[]]` and every other `dp[t]` starts empty. Each candidate sweeps sub-targets `t` upward from its own value, appending itself to every combination in `dp[t - candidate]`; the lines below show only the entries each pass changes:

```text
start          dp[0] = [[]]                        all other dp[t] empty
candidate 2    dp[2] = [[2]]                       [] + [2]
               dp[4] = [[2,2]]                     [2] + [2], written this pass
               dp[6] = [[2,2,2]]                   [2,2] + [2], written this pass
candidate 3    dp[3] = [[3]]                       [] + [3]
               dp[5] = [[2,3]]                     [2] + [3]
               dp[6] = [[2,2,2], [3,3]]            [3] + [3]
               dp[7] = [[2,2,3]]                   [2,2] + [3]
candidate 6    dp[6] = [[2,2,2], [3,3], [6]]       [] + [6]
candidate 7    dp[7] = [[2,2,3], [7]]              [] + [7]
```

The candidate `2` pass shows reuse working through the upward sweep: `dp[4]` reads the `[2]` that the very same pass just wrote into `dp[2]`, and `dp[6]` reads `[2,2]`, so one candidate stacks on itself as many times as it fits. Uniqueness shows in what never happens: when candidate `3` reaches `t = 5` it extends `[2]` into `[2,3]`, but `[3,2]` can never arise, because by the invariant no stored combination ever has a smaller candidate appended after a larger one. The final `dp[7] = [[2,2,3], [7]]` is returned, matching the expected Output.

#### Solution

The code is the table growth from the walkthrough: three nested loops, candidates outermost.

```python
from typing import List


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        # dp[t] holds every combination summing to t, each in non-decreasing order.
        dp: List[List[List[int]]] = [[] for _ in range(target + 1)]
        dp[0] = [[]]

        for candidate in candidates:
            for t in range(candidate, target + 1):
                for combo in dp[t - candidate]:
                    dp[t].append(combo + [candidate])

        return dp[target]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N * target * K)`

For each of `N` candidates and each of up to `target` sub-targets, we copy every stored combination, where `K` bounds the total number and length of combinations. Since the result set itself can be exponential, this matches the inherent output size; the DP adds no asymptotic savings over backtracking for enumeration.

##### Space Complexity: `O(target * K)`

The `dp` table stores, for every sub-target, all combinations reaching it. This is strictly more memory than backtracking, which only keeps one path plus the output.

#### Key Insights

- Looping over candidates on the outside (and sub-targets on the inside) is what
  enforces non-decreasing order and therefore uniqueness.
- Every combination in `dp[t]` already comes out non-decreasing, so unlike the
  include-exclude approach only the outer ordering is arbitrary: an equality check needs the list of combinations sorted, not their contents.
- The table makes every intermediate combination explicit, which trades memory for
  the removal of recursion.

## Comparison of Solutions

### Time Complexity

- **Include-Exclude Backtracking**: `O(N^(target / m))` - explores the full
  decision tree without pruning.
- **Sorted Backtracking with Pruning**: `O(N^(target / m))` - same bound, but the
  sorted `break` cuts whole subtrees in practice.
- **Bottom-Up Dynamic Programming**: `O(N * target * K)` - dominated by copying the
  combinations stored per sub-target.

### Space Complexity

- **Include-Exclude Backtracking**: `O(target / m)` - recursion stack plus one path.
- **Sorted Backtracking with Pruning**: `O(target / m)` - recursion stack plus one
  path.
- **Bottom-Up Dynamic Programming**: `O(target * K)` - stores all combinations for
  every sub-target.

### Trade-offs

- **Include-Exclude Backtracking** is the easiest to reason about and needs no
  sorting, but it explores branches that the pruned version would skip.
- **Sorted Backtracking with Pruning** adds an `O(N log N)` sort to gain a strong
  early-exit prune, making it the fastest in practice on real inputs.
- **Bottom-Up Dynamic Programming** removes recursion at the cost of holding every
  intermediate combination in memory, which is rarely worth it here.

### When to Use Each

- **Include-Exclude Backtracking**: When you want the clearest mental model or are
  forbidden from mutating the input by sorting it.
- **Sorted Backtracking with Pruning** (Recommended): The default interview answer;
  cleanest balance of speed and simplicity.
- **Bottom-Up Dynamic Programming**: When sub-target answers are reused elsewhere or
  you specifically want an iterative, stack-free formulation.

### Optimization Notes

- Sorting enables the `if candidate > remaining: break` prune; without sorting you
  could only `continue`, which does not cut subtrees.
- Reuse always comes from staying on the same index (`i` or `index`) in the include
  branch, never from a separate counter.
- Include-Exclude Backtracking emits each combination in input order, so comparing
  its output needs the full `sorted(map(sorted, result))` canonicalization. The two sorted approaches already emit non-decreasing combinations, so for those only the outer list needs sorting.
