# [Valid Parenthesis String](https://leetcode.com/problems/valid-parenthesis-string/)

**Medium** | **25 minutes** | **String, Dynamic Programming, Stack, Greedy**

**Pattern:** [Greedy Core](../patterns/greedy_core/intuition.md), [Stack](../patterns/stack/intuition.md)

**Algorithm:** [Greedy algorithm](https://en.wikipedia.org/wiki/Greedy_algorithm) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science))

**Practice:** [`practice/valid_parenthesis_string/solution.py`](../../practice/valid_parenthesis_string/solution.py)

You are given a string `s` which contains only three types of characters: `'('`, `')'` and `'*'`.

Return `true` if `s` is **valid**, otherwise return `false`.

A string is valid if it follows all of the following rules:

* Every left parenthesis `'('` must have a corresponding right parenthesis `')'`.
* Every right parenthesis `')'` must have a corresponding left parenthesis `'('`.
* Left parenthesis `'('` must go before the corresponding right parenthesis `')'`.
* A `'*'` could be treated as a right parenthesis `')'` character or a left parenthesis `'('` character, or as an empty string `""`.

## Examples

### Example 1

**Input:** `s = "((**)"`

**Output:** `true`

**Explanation:** One of the `'*'` could be a `')'` and the other could be an empty string.

### Example 2

**Input:** `s = "(((*)"`

**Output:** `false`

**Explanation:** The string is not valid because there is an extra `'('` at the beginning, regardless of the extra `'*'`.

## Constraints

- `1 <= s.length <= 100`

## Deriving the Solution

The wildcard `*` is the whole problem: it splits every deterministic question into three branches, and validity becomes "does some assignment of the stars produce a balanced string?". Every solution below is a strategy for searching or summarizing those assignments; they differ in whether the uncertainty is explored, cached, bounded, or compressed into one interval.

1. **Start literal.** Recurse position by position: at each `*` fork into its
   three readings, and let an open-parenthesis counter say whether a prefix
   can still become valid. Exponential in the number of stars: see
   [Brute Force Branching](#brute-force-branching).
2. **Spot the waste.** The recursion re-answers the same question, "can the
   suffix from position `ch` balance `open` opens?", for the same `(ch, open)`
   pairs reached by different star assignments: memoize the pair and the tree
   collapses to one computation per distinct state: see
   [Top-Down Memoization](#top-down-memoization).
3. **Bound instead of search.** A prefix never needs the exact open count,
   only whether some assignment keeps it in `[low, high]`: `low` the fewest
   possible opens, `high` the most. Both bounds update locally per character,
   and validity is `low == 0` at the end: see
   [Greedy Range Tracking](#greedy-range-tracking).
4. **Balance from both ends.** Symmetrically, count open parens left-to-right
   treating every `*` as `(`, and close parens right-to-left treating every
   `*` as `)`; the string is valid exactly when neither count ever goes
   negative: see [Two-Pass Balance Count](#two-pass-balance-count).

## Solutions

### Brute Force Branching

#### Derivation

The most direct reading tries every reading of every `*`. Walk the string with a recursion over positions, carrying `open`, the number of unmatched `'('` so far. A prefix with `open < 0` is already broken (a `')'` with no partner), `open` past the remaining length is hopeless, and reaching the end with `open == 0` is success:

1. Define `valid_from(ch, open)`: whether `s[ch:]` can complete to a valid
   string given `open` unmatched opens.
2. On `'('` recurse with `open + 1`; on `')'` recurse with `open - 1`.
3. On `'*'` recurse three ways: as `'('` (`open + 1`), as `')'`
   (`open - 1`), and as `""` (`open`).
4. Return false the moment `open < 0`; at `ch == len(s)` return `open == 0`.

The recursion explores a binary tree per star, so its size is `O(3^k)` for `k` stars.

#### Walkthrough

Trace the recursion on Example 1: `s = "((**)"`. Positions and their readings, with `open` tracked down each branch; the trace shows the first success found (characters consumed left to right, depth indented):

```text
pos0 (      open=1
pos1 (      open=2
pos2 *      fork 1: as (  open=3
pos3 *      fork 1a: as ( open=4
pos4 )      open=3
end         open=3 != 0 -> fail
            fork 1b: as ) open=2
pos4 )      open=1
end         open=1 != 0 -> fail
            fork 1c: as "" open=3
pos4 )      open=2 -> fail
      fork 2: as )  open=1
pos3 *      fork 2a: as ( open=2
pos4 )      open=1 -> fail
            fork 2b: as ) open=0
pos4 )      open=-1 -> fail
            fork 2c: as "" open=1
pos4 )      open=0 -> SUCCESS
```

The winning assignment reads position 2's `*` as `')'` and position 3's `*` as `""`, giving `"(( )"` with the last `')'` matched by the second `'('`: the recursion returns `True`, matching the expected Output for Example 1. On Example 2, `"(((*)"`, every branch ends with a positive open count (three leading opens against one `')'`-at-most from the star and one real close), so all leaves fail and the recursion returns `False`.

#### Solution

The code is the walkthrough's fork tree around the `open` counter.

```python
class Solution:
    def checkValidString(self, s: str) -> bool:
        def valid_from(ch: int, open: int) -> bool:
            if open < 0:
                return False
            if ch == len(s):
                return open == 0
            if s[ch] == "(":
                return valid_from(ch + 1, open + 1)
            if s[ch] == ")":
                return valid_from(ch + 1, open - 1)
            return (
                valid_from(ch + 1, open + 1)
                or valid_from(ch + 1, open - 1)
                or valid_from(ch + 1, open)
            )

        return valid_from(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(3^n)`

Every `*` forks the search three ways, so a string of `n` characters, all stars, grows a tree of `3^n` leaves; each node does constant work.

##### Space Complexity: `O(n)`

The recursion stack reaches depth `n` along the deepest chain.

#### Key Insights

- The `open` counter is the only state the future cares about: two assignments that reach the same position with the same open count have identical futures.
- Early pruning on `open < 0` keeps the search honest without changing its exponential shape.
- The exponential blow-up is pure rework: the same `(ch, open)` state is re-derived by different star assignments, which is precisely what the next solution caches.

### Top-Down Memoization

#### Derivation

The branching tree re-derives states relentlessly, yet `valid_from(ch, open)` depends on nothing but the pair `(ch, open)`: every route that arrives there gets the same answer. The repair is to cache each pair's result in a dictionary keyed by `(ch, open)`, so the many routes into one state share one computation. The state space is small: `ch` has `n` values and `open` never exceeds `n`, so at most `O(n^2)` states exist:

1. Keep `valid_from` verbatim from the Brute Force, including the pruning.
2. Before computing, return any answer stored under `(ch, open)` in `memo`.
3. Otherwise compute, store, and return.
4. The answer is `valid_from(0, 0)`.

Distinct states never exceed `O(n^2)`, and each does constant branching work, which is the whole improvement.

#### Walkthrough

Trace the memoized search on Example 1: `s = "((**)"`, showing the state each call computes and where later calls hit the cache. The trace lists calls in the order issued:

```text
valid_from(0, 0)   miss  s[0]='(' -> recurse (1,1)
valid_from(1, 1)   miss  s[1]='(' -> recurse (2,2)
valid_from(2, 2)   miss  s[2]='*' -> recurse (3,3), then (3,1)
  valid_from(3, 3) miss  s[3]='*' -> recurse (4,4), (4,2), (4,3)
    valid_from(4, 4) miss  s[4]=')' -> (5,3): end, open=3 -> False   memo[(4,4)]=False
    valid_from(4, 2) miss  s[4]=')' -> (5,1): end, open=1 -> False   memo[(4,2)]=False
    valid_from(4, 3) miss  s[4]=')' -> (5,2): end, open=2 -> False   memo[(4,3)]=False
  valid_from(3, 3) -> False
  valid_from(3, 1) miss  s[3]='*' -> recurse (4,2), (4,0), (4,1)
    valid_from(4, 2) -> False                       ** memo hit **
    valid_from(4, 0) miss  s[4]=')' -> (5,-1) -> False   memo[(4,0)]=False
    valid_from(4, 1) miss  s[4]=')' -> (5,0): end, open=0 -> True   memo[(4,1)]=True
  valid_from(3, 1) -> True
valid_from(2, 2) -> True
valid_from(1, 1) -> True
valid_from(0, 0) -> True
```

Two decisive cache events: the `(3, 3)` subtree computed `(4, 2)`'s answer, and the `(3, 1)` subtree recovered it by lookup, the fence's only cache hit; the star-as-empty branch from `(3, 1)` reaches `(4, 1)`, whose close lands the end at `open == 0`. The star at `(2, 2)` tries its branches in order, so once `(3, 1)` returns `True` the third branch `(3, 2)` is never issued: the `or` short-circuits. The recursion returns `True`, matching the expected Output for Example 1.

#### Solution

The code is the branching recursion with the memo check and store wrapped around it.

```python
class Solution:
    def checkValidString(self, s: str) -> bool:
        memo = {}

        def valid_from(ch: int, open: int) -> bool:
            if open < 0:
                return False
            if ch == len(s):
                return open == 0
            if (ch, open) in memo:
                return memo[(ch, open)]

            if s[ch] == "(":
                result = valid_from(ch + 1, open + 1)
            elif s[ch] == ")":
                result = valid_from(ch + 1, open - 1)
            else:
                result = (
                    valid_from(ch + 1, open + 1)
                    or valid_from(ch + 1, open - 1)
                    or valid_from(ch + 1, open)
                )
            memo[(ch, open)] = result
            return result

        return valid_from(0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

At most `n` positions times `n + 1` open counts are computed once each; every other call is a dictionary hit.

##### Space Complexity: `O(n^2)`

The memo holds one entry per computed `(ch, open)` pair, and the recursion stack adds depth `n`.

#### Key Insights

- Memoization works because `open` summarizes everything the past contributes: no other history matters, so the pair is a complete state.
- Caching a boolean search is the same trick as caching a numeric recurrence; the dictionary does not care what the values are.
- The quadratic bound is fine at the constraints, but the algorithm still searches; the greedy below shows the same question needs no search at all.

### Greedy Range Tracking

#### Derivation

The memoized search asks, per state, "can this exact open count survive?". But survival is monotone: if open count `k` can reach the end balanced, so can any count the same suffix would accept. The search collapses into tracking an interval of possible open counts: `low`, the fewest opens some assignment could have, and `high`, the most. Each character shifts both bounds:

1. Start `low = high = 0`.
2. On `'('` raise both: `low += 1`, `high += 1`.
3. On `')'` lower both: `low -= 1`, `high -= 1`.
4. On `'*'` widen: `high += 1` (read as `'('`) and `low -= 1` (read as `')'`).
5. Clamp `low` at `0`: open counts are never negative for a live prefix.
6. The string is valid exactly when `low == 0` at the end; `high < 0` at any
   point means even the most generous reading cannot absorb a `')'`, an
   immediate `False`.

Clamping `low` to `0` is not sloppiness: an open count below zero is dead, so keeping `low` at zero says "some assignment sits at zero", the tightest live floor.

#### Walkthrough

Trace the interval through Example 1: `s = "((**)"`. Each row is one character's update:

```text
start   low=0  high=0
(       low=1  high=1      both raised
(       low=2  high=2      both raised
*       low=1  high=3      low 2-1=1, high 2+1=3
*       low=0  high=4      low 1-1=0, high 3+1=4
)       low=-1 high=3      low clamped -> 0
end     low=0
```

The final `low` of `0` certifies some assignment ends balanced, so the function returns `True`, matching the expected Output for Example 1. On Example 2, `"(((*)"`: the three opens drive the interval to `low=3, high=3` before the star widens it to `[2, 4]` (clamped) and the close drops it to `low=1, high=3`; the final `low` is `1`, no assignment ends balanced, and the function returns `False` there.

#### Solution

The code is the walkthrough's two bounds with the clamp and the early exit.

```python
class Solution:
    def checkValidString(self, s: str) -> bool:
        low = 0
        high = 0
        for letter in s:
            if letter == "(":
                low += 1
                high += 1
            elif letter == ")":
                low -= 1
                high -= 1
            else:
                low -= 1
                high += 1
            if high < 0:
                return False
            low = max(low, 0)
        return low == 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass with a constant number of arithmetic updates per character.

##### Space Complexity: `O(1)`

Two integers, regardless of length.

#### Key Insights

- The interval `[low, high]` is the set of live open counts compressed to its endpoints: every value between them is reachable by some assignment, which is why endpoint bookkeeping suffices.
- The clamp `low = max(low, 0)` discards dead negative counts instead of letting them masquerade as a live floor.
- The early exit on `high < 0` is the only case where even the most `(`-favorable reading fails; everything else is decided at the end.

#### Invariant

The interval updates preserve reachability. Let `reachable` be the set of open counts some prefix assignment can hold after processing a prefix:

$$ \text{after each character}\quad [\,low,\ high\,] = \{\, k \in reachable : k \ge 0 \,\} \text{ clamped and shifted} $$

```text
[low, high] = the live open counts (k >= 0) some assignment can hold,
              shrunk to the interval endpoints
```

Concretely: every integer in `[low, high]` is held by some assignment of the processed prefix, and no assignment holds anything outside it. Each branch preserves this: `'('` shifts all counts up one (both endpoints move), `')'` shifts all down one and kills any assignment that would go negative, `'*'` unions the three shifted copies, whose union is again one interval. At the end, a balanced reading exists exactly when `0` is in the live set, which is `low == 0`; the clamp guarantees `low` never under-reports by holding a dead negative.

### Two-Pass Balance Count

#### Derivation

The range tracker needs both endpoints updated per character. A different cut at the same insight: balance errors are directional, and the two directions can be checked independently. Scanning left to right, treating every `*` as `'('`, the only way to fail is a surplus of `')'` no star can absorb; scanning right to left, treating every `*` as `')'`, the only failure is a surplus of `'('`. Each pass is a plain counter, and validity requires both to survive:

1. Sweep left to right with `open_left`: `+1` for `'('` and `'*'`, `-1` for
   `')'`; fail if it goes negative.
2. Sweep right to left with `open_right`: `+1` for `')'` and `'*'`, `-1` for
   `'('`; fail if it goes negative.
3. Return `True` only when neither pass fails.

One star cannot be both `(` and `)` in a single assignment, but it never has to be: the left pass uses it greedily as `(` against close-surpluses, the right pass as `)` against open-surpluses, and a string failing neither direction has some assignment failing neither, which is the Greedy Range Tracking invariant split in two.

#### Walkthrough

Run both passes on Example 1: `s = "((**)"`. The left pass treats stars as opens, the right pass as closes:

```text
left pass   open_left:  start 0
  (         1
  (         2
  * (as ()  3
  * (as ()  4
  )         3        never negative -> survive
right pass  open_right:  start 0
  )         1
  * (as ))  2
  * (as ))  3
  (         2
  (         1        never negative -> survive
both survive -> return True
```

Neither direction finds an unfixable surplus: the left pass absorbs the lone `')'` under a pile of opens, the right pass absorbs the two `'('` under star-closes plus the real close. The function returns `True`, matching the expected Output for Example 1. On Example 2, `"(((*)"`: the left pass ends at `4` without going negative, but the right pass counts `)`-side credits `2` (star plus close) against three opens and drops to `-1` at the final `'('`, so the function returns `False`.

#### Solution

The code is the two counters with their respective negative checks.

```python
class Solution:
    def checkValidString(self, s: str) -> bool:
        open_left = 0
        for letter in s:
            if letter == ")":
                open_left -= 1
            else:
                open_left += 1
            if open_left < 0:
                return False

        open_right = 0
        for letter in reversed(s):
            if letter == "(":
                open_right -= 1
            else:
                open_right += 1
            if open_right < 0:
                return False

        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Two passes with constant work per character.

##### Space Complexity: `O(1)`

Two counters.

#### Key Insights

- The two passes are the Greedy Range Tracking invariant split by direction: the left pass certifies `low` can be kept `>= 0`, the right pass certifies a mirrored `high` bound.
- Treating a star as `(` in one pass and `)` in the other is legal because the passes certify independent necessary conditions; together they are sufficient.
- Neither pass alone is correct: `"*("` survives the left pass but fails the right, which is why the check needs both directions.

## Comparison of Solutions

The practice harness's `practice/valid_parenthesis_string/reference.py` implements the **Greedy Range Tracking** solution.

### Time Complexity

- **Brute Force Branching**: `O(3^n)` - three recursive branches per star.
- **Top-Down Memoization**: `O(n^2)` - one computation per `(ch, open)` state.
- **Greedy Range Tracking**: `O(n)` - one pass of endpoint updates.
- **Two-Pass Balance Count**: `O(n)` - two counter passes.

### Space Complexity

- **Brute Force Branching**: `O(n)` - recursion stack depth.
- **Top-Down Memoization**: `O(n^2)` - the memo table over states.
- **Greedy Range Tracking**: `O(1)` - two integers.
- **Two-Pass Balance Count**: `O(1)` - two counters.

### Trade-offs

- The brute force is the definition written as code and the natural oracle, but its tree is exponential and unusable beyond toy strings.
- The memoized version keeps the recursive shape and stays quadratic, which is comfortable at these constraints but pays `O(n^2)` memory for states the answer never needs individually.
- The range tracker compresses the search into two integers and one pass; its correctness rests on the reachability invariant, which is one honest paragraph of proof.
- The two-pass counter is the least stateful of all, but it needs the both-directions argument, and getting it wrong in one direction is the classic trap.

### When to Use Each

- **Brute Force Branching**: as the derivational baseline and the oracle for checking the fast versions on small inputs.
- **Top-Down Memoization**: when the constraints are small and a provably exhaustive search is wanted without reasoning about intervals.
- **Greedy Range Tracking** (recommended): the interview answer: linear time, constant space, and a two-line statement of what `[low, high]` means.
- **Two-Pass Balance Count**: when a single counter loop is preferred twice over one interval update, or as a cross-check on the range tracker.

### Optimization Notes

- The clamp is load-bearing: removing `low = max(low, 0)` lets the floor track dead negative counts and produces wrong `True` answers on inputs like `"(*)"` variants where an over-credited star must be re-used as `(`.
- `high < 0` is a total, immediate failure: no later character can repair a close surplus, so the early return is safe wherever it fires.
- All fast versions agree with the brute force on every input; disagreement between Greedy Range Tracking and Two-Pass Balance Count signals a bug, since both certify the same reachability.
- The reachable set is always an interval: `'('`, `')'`, and `'*'` update it by shifting and uniting intervals, never by splitting it, which is why two endpoints capture it exactly.
