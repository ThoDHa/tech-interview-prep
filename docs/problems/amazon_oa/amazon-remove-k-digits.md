# [Remove K Digits](https://www.fastprep.io/problems/amazon-remove-k-digits)

**Medium** | **NN minutes** | **Stack, Greedy, String**

You are given a string num that represents a non-negative integer, and an integer k.

Remove exactly k digits from num so the remaining digits stay in their original relative order and form the smallest possible integer.

Return that integer as a string. Do not keep leading zeros, except for the integer 0 itself.

## Examples

### Example 1

**Input:** `num = "1432219"`, `k = 3`

**Output:** `"1219"`

**Explanation:** Removing the digits 4, 3, and 2 from 1432219 leaves 1219, which is the smallest remaining integer.

### Example 2

**Input:** `num = "10200"`, `k = 1`

**Output:** `"200"`

**Explanation:** Removing the leading 1 leaves 0200, which becomes 200 after leading zeros are stripped.

### Example 3

**Input:** `num = "10"`, `k = 2`

**Output:** `"0"`

**Explanation:** Every digit is removed, so the result is 0.

## Constraints

- `1 <= num.length <= 10^5.`
- `1 <= k <= num.length.`
- `num consists of digits only.`
- `num has no leading zeros except when num is "0".`

## Solutions

### Brute Force

#### Derivation

The most literal reading of the problem: removing exactly `k` digits from a string of length `n` is choosing which `k` positions to drop, so enumerate every choice, form the surviving string, and keep the smallest. Only one small refinement is needed to compare candidates correctly: leading zeros must be stripped before judging a candidate, because `10200` with the leading `1` dropped is worth 200, not 0200. The search walks one position at a time and decides drop or keep, which enumerates every removal choice exactly once:

1. `recurse(start, removals_left, kept)` processes position `start` with the
   digits collected so far in `kept`.
2. When the remaining digit count equals `removals_left`, all remaining digits
   must be dropped: judge the candidate `''.join(kept)` and return.
3. When `removals_left == 0`, nothing may be dropped: judge
   `''.join(kept) + num[start:]` and return.
4. Otherwise branch both ways: recurse dropping `num[start]` (append nothing),
   then recurse keeping it (append, recurse, pop in backtracking style).
5. After the search, strip leading zeros from the best candidate and return
   `"0"` if nothing survives the strip.

#### Walkthrough

Example 1 has 35 candidate choices, too many to draw, so we use the smaller tailored input `num = "112"`, `k = 1` (the tie between the two leading digits is exactly what the search must handle):

```text
recurse(0, 1, [])
  drop '1'    recurse(1, 0, [])          removals exhausted
              -> candidate "12"          value 12
  keep '1'    recurse(1, 1, ['1'])
    drop '1'  recurse(2, 0, ['1'])       -> candidate "1" + tail "2" = "12"   value 12
    keep '1'  recurse(2, 1, ['1', '1'])  1 digit left, 1 removal due
                                         -> candidate "11"                   value 11
best of 12, 12, 11  ->  "11"
```

The third leaf wins: dropping the final `2` leaves 11, the smallest possible, while the tie between the two leading `1`s produces the same candidate `"12"` on both branches and is settled harmlessly. The same search over Example 1 (`"1432219"`, `k = 3`) evaluates 35 candidates and returns `"1219"`, matching the expected Output.

#### Solution

The code is the decision tree from the walkthrough: at each position drop or keep, judging a candidate whenever a branch is forced.

```python
from typing import List


class Solution:
    def solve(self, num: str, k: int) -> str:
        best_value = None
        best_text = ""

        def consider(kept: List[str], tail: str) -> None:
            nonlocal best_value, best_text
            candidate = ''.join(kept) + tail
            value = int(candidate or "0")
            if best_value is None or value < best_value:
                best_value = value
                best_text = candidate

        def recurse(start: int, removals_left: int, kept: List[str]) -> None:
            remaining_choices = len(num) - start
            if remaining_choices == removals_left:
                consider(kept, "")
                return
            if removals_left == 0:
                consider(kept, num[start:])
                return
            recurse(start + 1, removals_left - 1, kept)
            kept.append(num[start])
            recurse(start + 1, removals_left, kept)
            kept.pop()

        recurse(0, k, [])
        return best_text.lstrip('0') or "0"
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(C(n, k) × n)`

The search produces one leaf per choice of dropped positions, `C(n, k)` leaves, and each leaf builds and judges an `n`-character candidate.

##### Space Complexity: `O(n)`

The recursion descends at most `n` levels and `kept` never exceeds `n` characters; the candidate string at a leaf is also `O(n)`.

#### Key Insights

- Comparing candidates as integers (or after stripping leading zeros) is mandatory: string length order lies when leading zeros are present.
- Judging with `value = int(candidate or "0")` absorbs the all-digits-dropped case, where the candidate is the empty string.
- The forced branches (nothing left to drop, or nothing left to keep) are what keep the tree at exactly `C(n, k)` leaves instead of an untidy `2^n` with duplicates.
- Correct but hopeless at scale: with `n = 10^5` the candidate count is astronomical, which motivates the greedy structure the next solution exploits.

### Greedy with Monotonic Stack

#### Derivation

The brute force re-decides the whole string for every combination, but most digits' fates are local. Compare two adjacent surviving digits: if a digit is followed by a smaller digit, dropping the larger digit (and spending one removal) makes the number smaller no matter what follows, because the decrease lands on the most significant affected place. So a digit should be dropped precisely when a smaller digit arrives after it while removals remain. Scanning left to right with a stack of kept digits turns this into a local rule: [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) top is the most recent survivor, so an incoming digit that is smaller than the top pops the top:

1. Scan `num` left to right with `kept` acting as the stack and
   `removals_left` counting down from `k`.
2. Before pushing `digit`, while `kept` is non-empty, `removals_left > 0`, and
   the top `kept[-1] > digit`, pop: that surviving digit is worse than the
   smaller arrival, spend one removal on it.
3. Push `digit`. The stack stays non-decreasing bottom to top, which is why it
   is called [monotonic](https://en.wikipedia.org/wiki/Monotonic_function).
4. After the scan, if `removals_left > 0`, the kept digits are non-decreasing
   and the largest digits sit at the end: drop the last `removals_left` of them.
5. Join `kept`, strip leading zeros, and return `"0"` for an empty result.

#### Walkthrough

Example 1, `num = "1432219"`, `k = 3`, traced digit by digit. Each line shows the incoming digit, the pops it causes, and the stack after it is pushed:

```text
digit '1'   no pop (stack empty)                  kept = [1]
digit '4'   top 1 not > 4, no pop                 kept = [1, 4]
digit '3'   pop 4  (removals_left 3 -> 2)         kept = [1]
            top 1 not > 3, push                   kept = [1, 3]
digit '2'   pop 3  (removals_left 2 -> 1)         kept = [1]
            top 1 not > 2, push                   kept = [1, 2]
digit '2'   top 2 not > 2 (equal digits stay), push
                                                  kept = [1, 2, 2]
digit '1'   pop 2  (removals_left 1 -> 0)         kept = [1, 2]
            removals_left = 0, stop popping, push kept = [1, 2, 1]
digit '9'   removals_left = 0, no pop, push       kept = [1, 2, 1, 9]
```

Every pop spent a removal on a digit a smaller arrival beat, and the budget of 3 ran out exactly as the final `1` arrived, so `9` (which no later digit threatens) survives untouched. Joining gives `"1219"` with no leading zeros to strip, matching the expected Output. The other examples exercise the two tail rules: `"10200"` with `k = 1` pops the leading `1` when `0` arrives, then pushes the remaining digits for a stack reading `"0200"`, which strips to `"200"`; `"10"` with `k = 2` empties to a trimmed `"0"`.

#### Solution

The code is the scan from the walkthrough: pop while the incoming digit beats the top and the removal budget lasts, then handle the leftover budget and the zeros.

```python
from typing import List


class Solution:
    def solve(self, num: str, k: int) -> str:
        kept: List[str] = []
        removals_left = k
        for digit in num:
            while kept and removals_left > 0 and kept[-1] > digit:
                kept.pop()
                removals_left -= 1
            kept.append(digit)
        if removals_left > 0:
            kept = kept[:len(kept) - removals_left]
        trimmed = ''.join(kept).lstrip('0')
        return trimmed if trimmed else "0"
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each digit is pushed once and popped at most once, so the total work across all stack activity is proportional to `n`.

##### Space Complexity: `O(n)`

The `kept` stack holds every surviving digit, which is `n - k` plus digits not yet popped; the joined result is the same size.

#### Key Insights

- The greedy rule "drop a survivor when a strictly smaller digit arrives while removals remain" is optimal because each removal buys the largest possible improvement at the most significant place still reachable.
- Strict inequality (`kept[-1] > digit`) is load-bearing: popping on equal digits would spend removals without changing the digit sequence.
- The leftover-budget trim exists for the non-decreasing case (`"112"`, `k = 1`): no digit was beatable, so the removals are best spent chopping off the tail.
- Leading zeros are a presentation problem, not a stack problem: strip once at the end with `lstrip('0')` and fall back to `"0"`.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(C(n, k) × n)` - one leaf per removal choice, each building and judging an `n`-character candidate.
- **Greedy with Monotonic Stack**: `O(n)` - each digit is pushed once and popped at most once.

### Space Complexity

- **Brute Force**: `O(n)` - recursion depth and the `kept` buffer, both bounded by the string length.
- **Greedy with Monotonic Stack**: `O(n)` - the stack of surviving digits.

### Trade-offs

- **Brute Force**: impossible to get wrong once the tie-breaking rules (leading zeros, equal digits) are encoded, and it doubles as a reference implementation for testing; it cannot run anywhere near the constraint sizes.
- **Greedy with Monotonic Stack**: linear time and short code, but its correctness rests on the exchange argument (a smaller arrival always justifies popping), which is the part an interviewer will probe.

### When to Use Each

- **Greedy with Monotonic Stack (Recommended)**: always, in an interview: it is the expected solution and runs comfortably at `n = 10^5`.
- **Brute Force**: only for tiny inputs, as a cross-check oracle when writing tests, or to explore the tie-breaking rules before committing to the greedy.

### Optimization Notes

- The pop loop checks `removals_left > 0` before comparing digits; ordering the three conditions cheapest-first (stack emptiness, budget, comparison) avoids work when the budget is spent.
- Slicing with `kept[:len(kept) - removals_left]` (rather than `[:-removals_left]`) is the same expression, written to stay readable when `removals_left` could be read as a negative index.
- A common pitfall is returning an empty string when every digit is removed or stripped; the final `return trimmed if trimmed else "0"` encodes the statement's exception for the integer 0.
