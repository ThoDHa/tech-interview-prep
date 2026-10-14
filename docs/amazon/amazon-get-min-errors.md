# [Get Min Errors](https://www.fastprep.io/problems/amazon-get-min-errors)

**Hard** | **NN minutes** | **Dynamic Programming, String, Greedy**

Amazon's database doesn’t support very large numbers, so numbers are stored as a string of binary characters, '0' and '1'. Accidentally, a '!' was entered at some positions and it is unknown whether they should be '0' or '1'.



The string of incorrect data is made up of the characters '0', '1' and '!' where '!' is the character that got entered incorrectly. '!' can be replaced with either '0' or '1'. Due to some internal faults, some errors are generated every time '0' and '1' occur together as '01' or '10' in any subsequence of the string. It is observed that the number of errors a subsequence '01' generates is x, while a subsequence '10' generates y errors.



Determine the minimum total errors generated. Since the answer can be very large, return it modulo 10^9+7.



Note: A subsequence of a string is obtained by omitting zero or more characters from the original string without changing their order.



Hint: It can be proved that (a + b) % c = ((a% c) + (b % c)) % c where a, b, and c are integers and % represents the modulo operation.

## Examples

### Example 1

**Input:** `errorString = "101!1"`, `x = 2`, `y = 3`

**Output:** `9`

**Explanation:** If the '!' at index 3 is replaced with '0', the string is "10101". The number of times the subsequence 01 occurs is 3 at indices (1, 2), (1, 4), and (3, 4). The number of times the subsequence 10 occurs is also 3, indices (0, 1), (0, 3) and (2, 3). The number of errors is 3 * x + 3 * y = 6 + 9 = 15.

If the '!' is replaced with '1', the string is "10111". The subsequence 01 occurs 3 times and 10 occurs 1 time. The number of errors is 3 * x + y = 9.

The minimum number of errors is min(9, 15) modulo (10^9 + 7) = 9.

### Example 2

**Input:** `errorString = "01!0"`, `x = 2`, `y = 2`

**Output:** `6`

**Explanation:** The better string is 0100 with one substring 01 at index (0,1) and two subsequence of 10 at indices (1,2) and (2,3) making total errors generate = 2 * 1 + 2 * 2 = 6.

࣪𓏲ּ ᥫ᭡ ₊ ⊹ Credit to 𓇼 Suat 𓇼 ˑ🌷 ִֶ 𓂃

### Example 3

**Input:** `errorString = "!!!!!!!"`, `x = 23`, `y = 27`

**Output:** `0`

**Explanation:** There is a tie for the best string generated, 00000 or 11111, with zero substrings 01 or 10.

## Constraints

- `1<= len (errorString)<=105`
- `0 <= x, y <= 105`
- `s consists only of characters '0', '1', and 'l'`

## Solutions

### Per-Character Greedy

#### Derivation

The most literal reading prices each error at the moment it is created. Walking the string once, a concrete character's bill is already fixed when it arrives: a `'0'` pairs as the later element with every `'1'` seen so far, and a `'1'` pairs as the later element with every `'0'` seen so far. Only the `'!'` involves a choice, so choose for it on the spot: charge whichever of the two bills is cheaper and count the character accordingly:

1. Track `zeros` and `ones`, the counts of those characters among the positions
   already processed, and `errors_so_far`, the total error charge so far.
2. On `'0'`: add `y * ones` to `errors_so_far`, then increment `zeros`.
3. On `'1'`: add `x * zeros` to `errors_so_far`, then increment `ones`.
4. On `'!'`: add `min(y * ones, x * zeros)` and increment the count of the
   character whose charge was cheaper, `zeros` when the `'0'` charge wins or
   ties, `ones` otherwise.
5. Return `errors_so_far % 1_000_000_007`.

The pass is one loop with constant work per character, `O(len(errorString))`. The flaw hides in step 4: charging the wildcard by today's cheapest bill ignores the bills its choice creates for characters still to come, and the [Dynamic Programming over Prefix Counts](#dynamic-programming-over-prefix-counts) section shows a case where that discount costs more than it saves.

#### Walkthrough

Trace Example 1: `errorString = "101!1"`, `x = 2`, `y = 3`. One row per character; the cost column is the charge added on arrival, and the counts update after it:

| position | character | `zeros` / `ones` before | cost charged | `errors_so_far` | counts after |
| --- | --- | --- | --- | --- | --- |
| 0 | `'1'` | 0 / 0 | `x * 0 = 0` | 0 | 0 / 1 |
| 1 | `'0'` | 0 / 1 | `y * 1 = 3` | 3 | 1 / 1 |
| 2 | `'1'` | 1 / 1 | `x * 1 = 2` | 5 | 1 / 2 |
| 3 | `'!'` | 1 / 2 | `min(y * 2, x * 1) = min(6, 2) = 2` | 7 | 1 / 3 |
| 4 | `'1'` | 1 / 3 | `x * 1 = 2` | 9 | 1 / 4 |

The wildcard at position 3 charges `x * zeros = 2` as a `'1'` against `y * ones = 6` as a `'0'`, so it joins the ones. The pass returns `9 % 1_000_000_007 = 9`, matching the expected Output for Example 1, and it also lands on the right answers for Examples 2 and 3, which is exactly what makes the approach seductive: on friendly inputs the missing lookahead is free, and nothing in the examples reveals the inputs where it is not.

#### Solution

The code is the single charging pass from the walkthrough, one branch per character.

```python
from typing import List


class Solution:
    def getMinErrors(self, errorString: str, x: int, y: int) -> int:
        modulo = 1_000_000_007
        zeros = 0
        ones = 0
        errors_so_far = 0
        for character in errorString:
            if character == '0':
                errors_so_far += y * ones
                zeros += 1
            elif character == '1':
                errors_so_far += x * zeros
                ones += 1
            else:
                cost_zero = y * ones
                cost_one = x * zeros
                if cost_zero <= cost_one:
                    errors_so_far += cost_zero
                    zeros += 1
                else:
                    errors_so_far += cost_one
                    ones += 1
        return errors_so_far % modulo
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass over the `n = len(errorString)` characters with constant work each.

##### Space Complexity: `O(1)`

Two counters and a running total, regardless of the string length.

#### Key Insights

- Every `01` or `10` pair is charged exactly once, when its later element arrives, so the pass is a faithful accounting of any fully replaced string.
- The greedy is a heuristic, not a solution: on `"01!1"` with `x = 2`, `y = 1` it charges `min(y * 1, x * 1) = 1`, makes the `'!'` a `'0'`, and totals `7`, while replacing the `'!'` with `'1'` gives `"0111"` and `6`. The locally cheaper charge made the final `'1'` pay `4` instead of `2`.
- The failure mode is myopic, not structural: the approach would need to know how a wildcard's choice shifts every later charge, which is precisely the lookahead the Dynamic Programming solution builds.
- It is still valuable as a baseline: it documents the charge-on-arrival pricing that the optimal solution reuses, and it runs on any input, wrong or not.

### Dynamic Programming over Prefix Counts

#### Derivation

The greedy's flaw is deciding a wildcard from counts alone. What the decision actually needs is the total cost of the rest of the string under each choice, and that cost depends on the future only through one fact: how many zeros and ones the prefix supplies for the suffix to pair against. So the state to keep is not a single number but a frontier: for every possible zero count the prefix could expose, the best total cost achievable so far. Processing the next character extends that frontier in one or two directions, exactly mirroring the two replacements a wildcard admits:

1. Let `min_errors[zero_count]` be the minimum total error charge of the
   prefix processed so far, given that the prefix ends with exactly
   `zero_count` characters replaced-or-read as `'0'` (the ones count is then
   `position - zero_count`, known from how far the scan has traveled, so one
   dimension suffices).
2. Start from `min_errors = [0]`: the empty prefix has no zeros and no charge.
3. For each character at `position`, build `next_min_errors` of length one
   larger, reading the character's cost off the old frontier:
   - as `'0'` (concrete `'0'` or wildcard): from `min_errors[zero_count]`,
     add `y * (position - zero_count)`, the ones before this position, and
     write into `next_min_errors[zero_count + 1]`;
   - as `'1'` (concrete `'1'` or wildcard): from `min_errors[zero_count]`,
     add `x * zero_count` and write into `next_min_errors[zero_count]`.
4. A wildcard writes both entries, a concrete character one; when both writers
   target one entry, keep the smaller cost.
5. After the last character, return the minimum of the frontier, reduced
   modulo `1_000_000_007`.

Concrete characters keep the frontier narrow (a `'0'` shifts it one slot wider deterministically; a `'1'` leaves the width unchanged), but wildcards double the reachable assignments, so after a string of `k` wildcards the frontier holds up to `k + 1` live entries. The modulus is applied once at the end: per the hint, errors never decrease along the scan (every extension adds a non-negative charge), so the true minimum is found before any reduction, and `(a + b) % c = ((a % c) + (b % c)) % c` licenses deferring or interleaving the reductions freely.

#### Recurrence

Let `min_errors[zero_count]` be the minimum charge of the prefix `errorString[:position]` ending with exactly `zero_count` zeros, and let `ones_before = position - zero_count`:

$$ \text{min\_errors}[\text{zero\_count}] = \begin{cases} 0, & \text{position} = 0,\ \text{zero\_count} = 0 \\[4pt] \text{cost as } '0', & \text{character} = '0' \\[4pt] \text{cost as } '1', & \text{character} = '1' \\[4pt] \min(\text{cost as } '0',\ \text{cost as } '1'), & \text{character} = '!' \end{cases} $$

```text
min_errors = [0]                                    at position 0, zero_count 0
reading character at `position`:
  as '0':  next[zero_count + 1] <- min_errors[zero_count]
                                    + y * (position - zero_count)
  as '1':  next[zero_count]     <- min_errors[zero_count] + x * zero_count
  wildcards apply both writes; concrete characters apply one
answer = min(min_errors)                            after the last character
```

The base case is the empty prefix: no zeros, no ones, no charge. Entries unreachable by the characters read so far hold `None` and are skipped. The answer is the cheapest frontier entry after the last character, because every pair inside the string has been charged exactly once by then.

#### Walkthrough

Trace Example 2: `errorString = "01!0"`, `x = 2`, `y = 2`. Each row shows the frontier after processing the character, with `None` marking unreachable zero counts and each write annotated by what the character became:

```text
start            min_errors = [0]
'0' at pos 0     as '0': next[1] <- 0 + y*(0-0) = 0
                 min_errors = [None, 0]
'1' at pos 1     as '1': next[1] <- 0 + x*1 = 2
                 min_errors = [None, 2]
'!' at pos 2     as '0': next[2] <- 2 + y*(2-1) = 4
                 as '1': next[1] <- 2 + x*1 = 4
                 min_errors = [None, 4, 4]
'0' at pos 3     as '0': next[2] <- 4 + y*(3-1) = 8
                         next[3] <- 4 + y*(3-2) = 6
                 min_errors = [None, None, 8, 6]
```

The decisive row is the wildcard: becoming `'0'` charges `y * 1 = 2` against the one one (total `4`, assignment `"010"`), and becoming `'1'` charges `x * 1 = 2` against the one zero (total `4`, assignment `"011"`), so both futures stay live. The final `'0'` then bills the `"011"`-future `y * 2 = 4` more (total `8`, assignment `"0110"`) and the `"010"`-future `y * 1 = 2` more (total `6`, assignment `"0100"`). The minimum of the last frontier is `6 % 1_000_000_007 = 6`, matching the expected Output for Example 2: the better string `"0100"` carries one `01` pair (`2 * 1`) and two `10` pairs (`2 * 2`) for `6` in all, while the only alternative, `"0110"`, prices at `8`. (Example 1 runs the same way and returns `9`; Example 3 returns `0`, since the all-ones assignment `"1111111"` ends at frontier slot `0` and the all-zeros assignment `"0000000"` at slot `7`, each with zero charge.)

#### Solution

The code is the frontier extension from the recurrence: one pass, one or two writes per character.

```python
from typing import List


class Solution:
    def getMinErrors(self, errorString: str, x: int, y: int) -> int:
        modulo = 1_000_000_007
        min_errors: List = [0]
        for position, character in enumerate(errorString):
            next_min_errors: List = [None] * (len(min_errors) + 1)
            if character in ('0', '!'):
                for zero_count, errors in enumerate(min_errors):
                    if errors is None:
                        continue
                    ones_before = position - zero_count
                    cost = errors + y * ones_before
                    zero_target = zero_count + 1
                    if next_min_errors[zero_target] is None or cost < next_min_errors[zero_target]:
                        next_min_errors[zero_target] = cost
            if character in ('1', '!'):
                for zero_count, errors in enumerate(min_errors):
                    if errors is None:
                        continue
                    cost = errors + x * zero_count
                    if next_min_errors[zero_count] is None or cost < next_min_errors[zero_count]:
                        next_min_errors[zero_count] = cost
            min_errors = next_min_errors
        return min(errors for errors in min_errors if errors is not None) % modulo
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n = len(errorString)` positions scans a frontier whose width is bounded by `position + 1` slots, so the total work is `1 + 2 + ... + n = O(n^2)`; wildcards widen the frontier but never past its `O(n)` ceiling, and the per-entry work is constant.

##### Space Complexity: `O(n)`

Two frontiers coexist during one position's update, and the wider of the two holds at most `n + 1` entries.

#### Key Insights

- The state collapses to one integer per frontier slot: the ones count is `position - zero_count`, so the classic `(zeros, ones)` grid folds into a single diagonal, which is what turns an `O(n^3)`-looking table into `O(n^2)` time.
- Errors only ever increase along the scan, so the minimum can be taken at the very end; this is what makes the single deferred `% 1_000_000_007` correct even with `x, y` up to `10^5` and `n` up to `10^5` (raw totals reach `10^15`, far inside Python integers, though a C++ port must reduce per step).
- The two loop bodies differ only in the target slot and the charge formula, which is the whole content of the recurrence: a `'0'` moves the frontier's zero-count axis, a `'1'` charges against zeros in place, and a `'!'` is honestly both.
- Against the greedy: the DP keeps every wildcard alternative alive until the last character has spoken, which is exactly the lookahead the `"01!1"`, `x = 2`, `y = 1` counterexample shows the greedy lacking.

## Comparison of Solutions

### Time Complexity

- **Per-Character Greedy**: `O(n)` - one pass with constant work per character.
- **Dynamic Programming over Prefix Counts**: `O(n^2)` - each position extends a frontier of up to `position + 1` slots with constant work per slot.

### Space Complexity

- **Per-Character Greedy**: `O(1)` - two counters and a running total.
- **Dynamic Programming over Prefix Counts**: `O(n)` - the live frontier plus the one being built.

### Trade-offs

- **Per-Character Greedy**: linear time and trivial to write, but it is not correct: locally cheaper wildcard charges create globally costlier futures, as `"01!1"` with `x = 2`, `y = 1` shows (it returns `7`; the minimum is `6`).
- **Dynamic Programming over Prefix Counts**: quadratic time, linear space, and exact; the extra cost over the greedy buys the guarantee that no wildcard decision is made before the whole suffix has been priced.

### When to Use Each

- **Per-Character Greedy**: as a first pass to understand the per-pair pricing, as a fast approximation when inputs are known to have no wildcards (where it is exact), and as a reference when hand-testing the DP on small strings.
- **Dynamic Programming over Prefix Counts (Recommended)**: for the actual answer; with wildcards present and `len(errorString)` up to `10^5`, only an exact method earns the output.

### Optimization Notes

- The frontier scan visits some `None` slots on mixed strings; tracking the lowest and highest reachable `zero_count` would trim the inner loops, a constant-factor win that leaves the `O(n^2)` bound intact.
- In a language with fixed-width integers, apply the modulus on every charge (`((a % c) + (b % c)) % c` from the hint); the per-step comparison `cost < next_min_errors[...]` stays valid because reductions are monotone on the non-negative totals this DP produces. Python integers make the deferred single reduction safe and slightly faster.
- The dimension drop from `(zeros, ones)` to `zero_count` alone is worth stating in an interview: it relies on `ones = position - zeros`, the same prefix-length identity that makes prefix sums one-dimensional.
