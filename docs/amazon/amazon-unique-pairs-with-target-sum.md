# [Unique Pairs With Target Sum](https://www.fastprep.io/problems/amazon-unique-pairs-with-target-sum)

**Easy** | **NN minutes** | **Array, Hash Table, Two Pointers**

Complete the function below. The function receives the full standard input as a single string and returns the exact standard output lines.

Problem Given an integer array and a target value, return all unique pairs whose sum equals the target. Each pair must be sorted in ascending order, and duplicate pairs must appear only once.

Output the pairs in lexicographic order as a,b. If there are no valid pairs, output None.

Function Description Complete solveUniquePairsWithTargetSum. It has one parameter, String input. The first line contains n target; the second line contains n integers. Return one output line per unique pair.

## Examples

### Example 1

**Input:** `input = "8 5\n1 4 2 3 3 2 0 5"`

**Output:** `["0,5","1,4","2,3"]`

**Explanation:** The pair 2,3 is output once even though both values appear multiple times.

### Example 2

**Input:** `input = "4 10\n1 2 3 4"`

**Output:** `["None"]`

**Explanation:** No pair sums to 10.

## Constraints

- `Pairs are value pairs, not index pairs; duplicates in the input should not create duplicate output lines.`

## Solutions

### Brute Force

#### Derivation

The most literal reading: a pair of values `(a, b)` with `a <= b` qualifies when `a + b` equals `target`, so try every pair of positions. Two details come from the output contract. First, pairs are value pairs, not index pairs, so the repeated values in Example 1 must collapse: `(2, 3)` is one pair no matter how many positions produce it, which a set absorbs for free. Second, the output is the lexicographic order of the formatted `"a,b"` strings, so the final sort runs on the formatted strings, not on the numeric tuples:

1. Parse `input`: the first two tokens are `count` and `target`; the next `count`
   tokens are `numbers`.
2. Double loop over `first_idx` and `second_idx` with `first_idx < second_idx`.
3. When `numbers[first_idx] + numbers[second_idx] == target`, add the normalized
   tuple `(min, max)` of the two values to `found_pairs`.
4. Return `["None"]` when `found_pairs` is empty; otherwise format each pair as
   `"smaller,larger"` and sort the strings.

#### Walkthrough

Example 1 has `numbers = [1, 4, 2, 3, 3, 2, 0, 5]` and `target = 5`. Most of the 28 position pairs miss; the trace below shows only the events that touch `found_pairs`:

```text
(0, 1)  1+4=5   add (1, 4)   found_pairs = {(1, 4)}
(2, 3)  2+3=5   add (2, 3)   found_pairs = {(1, 4), (2, 3)}
(2, 4)  2+3=5   (2, 3) already present, set unchanged
(3, 5)  3+2=5   (2, 3) already present, set unchanged
(4, 5)  3+2=5   (2, 3) already present, set unchanged
(6, 7)  0+5=5   add (0, 5)   found_pairs = {(0, 5), (1, 4), (2, 3)}
```

Four position pairs produce the value pair `(2, 3)`, and the set keeps one. Formatting and sorting the strings gives `["0,5", "1,4", "2,3"]`, the expected Output.

#### Solution

The code is the double loop from the walkthrough, with the parse and the set doing the bookkeeping.

```python
from typing import List


class Solution:
    def solve(self, input: str) -> List[str]:
        tokens = input.split()
        count = int(tokens[0])
        target = int(tokens[1])
        numbers = [int(token) for token in tokens[2:2 + count]]

        found_pairs = set()
        for first_idx in range(count):
            for second_idx in range(first_idx + 1, count):
                if numbers[first_idx] + numbers[second_idx] == target:
                    first_value, second_value = numbers[first_idx], numbers[second_idx]
                    found_pairs.add((min(first_value, second_value),
                                     max(first_value, second_value)))

        if not found_pairs:
            return ["None"]
        return sorted(f"{smaller},{larger}" for smaller, larger in found_pairs)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

The double loop performs `n(n-1)/2` sums; at most `O(n)` distinct value pairs exist (one per distinct smaller value), so formatting and sorting them never dominates the quadratic term.

##### Space Complexity: `O(n)`

The parsed `numbers` list plus `found_pairs`, which holds at most one pair per distinct smaller value.

#### Key Insights

- Normalizing each hit to `(min, max)` before insertion is what makes the set deduplicate value pairs while the raw loop keeps rediscovering them.
- Sorting the formatted strings (not the numeric tuples) is required for a correct lexicographic order: numeric and string order diverge once values of different digit counts appear, such as `"10,9"` versus `"2,3"`.
- Correct on every input, but the `O(n^2)` summing loop is the cost of re-checking pairs that a smarter structure could answer in one pass.

### Sort and Two Pointers

#### Derivation

The brute force re-discovers the same value pair from many position pairs, because it never looks at the values in order. Sorting groups equal values into runs and lines the array up so that a single [two-pointer](https://en.wikipedia.org/wiki/Two-pointer_technique) sweep can visit each unique value pair at most once: with `left` at the smallest value and `right` at the largest, a sum below `target` can only be raised by advancing `left`, a sum above `target` can only be lowered by retreating `right`, and a hit is followed by hopping both pointers over their entire runs of duplicates:

1. Sort `numbers` ascending.
2. Set `left = 0` and `right = count - 1`.
3. While `left < right`: if the sum equals `target`, record
   `f"{numbers[left]},{numbers[right]}"`, then advance `left` past its run and
   retreat `right` past its run; if the sum is low, advance `left`; if high,
   retreat `right`.
4. Sort the formatted strings for the lexicographic order, or return `["None"]`.

#### Walkthrough

Sorting Example 1 gives `numbers = [0, 1, 2, 2, 3, 3, 4, 5]`. Each line is one sweep event; the duplicate runs at values `2` and `3` are skipped in a single hop:

```text
left=0 (0)  right=7 (5)  0+5=5  record "0,5"; skip 0-run -> left=1; skip 5-run -> right=6
left=1 (1)  right=6 (4)  1+4=5  record "1,4"; skip 1-run -> left=2; skip 4-run -> right=5
left=2 (2)  right=5 (3)  2+3=5  record "2,3"; skip 2-run -> left=4; skip 3-run -> right=4
left == right -> sweep ends
```

The pair `(2, 3)`, which cost the brute force four separate discoveries, is recorded exactly once because both duplicate runs are hopped in the same step. The sweep ends with `pairs = ["0,5", "1,4", "2,3"]`, the expected Output.

#### Solution

The code is the sweep from the walkthrough: compare, record, hop the runs.

```python
from typing import List


class Solution:
    def solve(self, input: str) -> List[str]:
        tokens = input.split()
        count = int(tokens[0])
        target = int(tokens[1])
        numbers = sorted(int(token) for token in tokens[2:2 + count])

        pairs = []
        left, right = 0, count - 1
        while left < right:
            current_sum = numbers[left] + numbers[right]
            if current_sum == target:
                pairs.append(f"{numbers[left]},{numbers[right]}")
                left_value, right_value = numbers[left], numbers[right]
                while left < right and numbers[left] == left_value:
                    left += 1
                while left < right and numbers[right] == right_value:
                    right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1

        return sorted(pairs) if pairs else ["None"]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting dominates; the sweep itself is `O(n)` because every iteration either records a pair and consumes two whole runs, or moves one pointer inward.

##### Space Complexity: `O(n)`

The sorted copy of `numbers` plus the `pairs` output, which holds at most one entry per distinct smaller value.

#### Key Insights

- The sorted order is what turns "is this exact value pair used yet?" into a pointer-hop: duplicates are contiguous, so skipping a run once skips every position pair it would have produced.
- Sorting alone does not order the output: the sweep emits pairs in ascending numeric order, but the statement asks for lexicographic string order, so the final `sorted(pairs)` stays.
- A value pair `(a, a)` with `2a == target` still works: it is recorded only when two positions of value `a` exist, because `left < right` is checked throughout.

### Hash Set

#### Derivation

The two-pointer sweep pays `O(n log n)` for an ordering it does not really need. The question it answers at each step is "have I already seen the complement?", and a hash set answers that in `O(1)` average time without any ordering: walk the values once, keep `seen_values` of everything visited so far, and when `target - value` is already in the set, emit the pair. Checking `seen_values` before inserting `value` is what keeps a single occurrence from pairing with itself:

1. Parse `input` as before.
2. For each `value`: if `target - value` is in `seen_values`, add the normalized
   tuple to `found_pairs`; then insert `value` into `seen_values`.
3. Sort the formatted strings for the lexicographic order, or return `["None"]`.

#### Walkthrough

Example 1 again, `numbers = [1, 4, 2, 3, 3, 2, 0, 5]` in input order, `target = 5`:

```text
value 1  need 4  seen = {}                        no pair     seen = {1}
value 4  need 1  hit                              add (1, 4)  seen = {1, 4}
value 2  need 3  seen = {1, 4}                    no pair     seen = {1, 2, 4}
value 3  need 2  hit                              add (2, 3)  seen = {1, 2, 3, 4}
value 3  need 2  hit, (2, 3) already present      no change   seen = {1, 2, 3, 4}
value 2  need 3  hit, (2, 3) already present      no change   seen = {1, 2, 3, 4}
value 0  need 5  seen = {1, 2, 3, 4}              no pair     seen = {0, 1, 2, 3, 4}
value 5  need 0  hit                              add (0, 5)
```

The set never holds an entry the scan has not reached, which is why the first `1` cannot pair with a `4` that has not arrived yet, and why a lone `3` cannot pair with itself. `found_pairs = {(0, 5), (1, 4), (2, 3)}` sorts to `["0,5", "1,4", "2,3"]`, the expected Output.

#### Solution

The code is the single pass from the walkthrough: look up the complement, record the pair, remember the value.

```python
from typing import List


class Solution:
    def solve(self, input: str) -> List[str]:
        tokens = input.split()
        count = int(tokens[0])
        target = int(tokens[1])
        numbers = [int(token) for token in tokens[2:2 + count]]

        seen_values = set()
        found_pairs = set()
        for value in numbers:
            needed = target - value
            if needed in seen_values:
                found_pairs.add((min(value, needed), max(value, needed)))
            seen_values.add(value)

        if not found_pairs:
            return ["None"]
        return sorted(f"{smaller},{larger}" for smaller, larger in found_pairs)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

One pass with `O(1)` average set lookups, plus sorting the output pairs; up to `n` distinct pairs can exist, so the output sort can dominate the linear pass.

##### Space Complexity: `O(n)`

`seen_values` and `found_pairs` each hold at most one entry per distinct value.

#### Key Insights

- Looking up the complement before inserting the current value is the whole correctness argument for self-pairs: `value` can only match a strictly earlier occurrence, never itself.
- This is the one approach whose pass order is irrelevant: the scan works on the input in arrival order, so it also answers streaming versions of the question where the array is not fully known up front.
- The unordered result still needs the lexicographic sort of formatted strings; the hash set buys time on discovery, not on output order.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - every position pair is summed once.
- **Sort and Two Pointers**: `O(n log n)` - sorting the input dominates the linear sweep.
- **Hash Set**: `O(n log n)` - a linear pass with average constant-time lookups, plus sorting up to `n` output pairs.

### Space Complexity

- **Brute Force**: `O(n)` - the parsed values plus at most one set entry per distinct smaller value.
- **Sort and Two Pointers**: `O(n)` - the sorted copy plus the output list.
- **Hash Set**: `O(n)` - the seen-values set plus the found-pairs set.

### Trade-offs

- **Brute Force**: impossible to get wrong, and it doubles as the correctness oracle for the other two, but it pays for every position pair even when the answer is tiny.
- **Sort and Two Pointers**: removes the quadratic scan with a sort, keeps memory flat, and needs the most careful bookkeeping (the run-hopping) to avoid duplicate output.
- **Hash Set**: finds every pair in a single pass over the input in arrival order, with no input ordering needed; both it and the sweep still pay a log factor on the output sort when the pair count is large.

### When to Use Each

- **Brute Force**: short inputs, or as the reference implementation you test the faster versions against.
- **Sort and Two Pointers (Recommended)**: the standard interview answer when the input arrives sorted or sorting is free; it signals the classic pattern and keeps auxiliary memory to the output.
- **Hash Set**: large unsorted inputs, streaming settings, or anywhere the input cannot be reordered before the pass.

### Optimization Notes

- All three approaches sort the formatted `"a,b"` strings at the end. Sorting numeric tuples instead is a real bug: for the pairs `(9, 17)` and `(12, 14)`, numeric order sorts `(9, 17)` first while lexicographic order sorts `"12,14"` before `"9,17"`.
- The parse reads exactly `count` values after the first two tokens, so trailing garbage in `input` is ignored rather than silently treated as data.
- Duplicate pairs are prevented at insert time in all three approaches (normalized tuples, run-hopping, complement-before-insert), never by filtering the output afterward.
