# [Reorganize a String](https://www.fastprep.io/problems/amazon-reorganize-string)

**Medium** | **NN minutes** | **String, Hash Table, Heap, Greedy**

Rearrange a lowercase string so that no two adjacent characters are equal. If no such arrangement exists, return the empty string.

To make the judged result deterministic, construct the answer with this rule: at each position, select the eligible character with the greatest remaining frequency. The previously placed character is not eligible. If several eligible characters have the same frequency, select the lexicographically smallest one.

## Examples

### Example 1

**Input:** `s = "aab"`

**Output:** `"aba"`

**Explanation:** The highest-frequency eligible character is chosen first, producing a valid arrangement.

### Example 2

**Input:** `s = "aaab"`

**Output:** `""`

**Explanation:** Three copies of one character cannot be separated by the single remaining character.

### Example 3

**Input:** `s = "aabbcc"`

**Output:** `"abcabc"`

**Explanation:** Frequency ties are resolved in lexicographic order while the previous character remains temporarily ineligible.

## Constraints

- `1 <= s.length <= 10^5`
- `s contains only lowercase English letters.`

## Solutions

### Greedy Frequency Scan

#### Derivation

The statement does more than ask for any valid arrangement: it fixes a deterministic selection rule, so the most direct reading is to simulate that rule literally. At each output position, scan all 26 letters, keep the ones with a positive remaining count that are not the previously placed character, and take the one with the greatest remaining frequency, breaking ties toward the lexicographically smallest letter. The rule is greedy because the most frequent remaining character is the hardest one to separate later; spending it first keeps the largest reserve of harmless filler:

1. Tally `counts`, a 26-entry table indexed by `ord(character) - ord("a")`, and note `total = len(s)`.
2. Repeat `total` times: scan `letter_index` over all 26 letters, tracking the eligible letter with the largest count, where eligible means `counts[letter_index] > 0` and the letter differs from `previous`. Ties keep the smaller `letter_index`, which is the lexicographically smaller letter.
3. Append the chosen letter to `result`, decrement its count, and record it as `previous`. If no letter is eligible while positions remain, return `""`.
4. Return `result` joined into a string.

The scan runs in constant letters per position, so the whole construction is linear in the string length.

#### Walkthrough

Example 3, `s = "aabbcc"`, exercises the tie-breaking rule, because the counts start level at `a:2, b:2, c:2`. Each row is one output position; the chosen letter is the eligible one with the greatest count, ties going to the smaller letter:

```text
position 0   counts a:2 b:2 c:2   previous none   all eligible -> choose a (tie, smallest)
position 1   counts a:1 b:2 c:2   previous a      a ineligible  -> choose b (tie b/c)
position 2   counts a:1 b:1 c:2   previous b      -> choose c   counts a:1 b:1 c:1
position 3   counts a:1 b:1 c:1   previous c      -> choose a   (tie, smallest)
position 4   counts a:0 b:1 c:1   previous a      -> choose b   (tie b/c)
position 5   counts a:0 b:0 c:1   previous b      -> choose c
```

Position 3 shows the rule steering after a placement: with all three counts level, the previously placed `c` drops out and `a` wins the tie. The built string is `"abcabc"`, which has no equal neighbors and matches the expected Output for Example 3.

#### Solution

The code is the walkthrough's selection loop: one scan per output position over the fixed 26-letter table.

```python
from typing import List


class Solution:
    def solve(self, s: str) -> str:
        total_letters = 26
        counts: List[int] = [0] * total_letters
        for character in s:
            counts[ord(character) - ord("a")] += 1

        result: List[str] = []
        previous_index = -1

        for _ in range(len(s)):
            chosen_index = -1
            for letter_index in range(total_letters):
                if counts[letter_index] == 0 or letter_index == previous_index:
                    continue
                if chosen_index == -1 or counts[letter_index] > counts[chosen_index]:
                    chosen_index = letter_index

            if chosen_index == -1:
                return ""

            result.append(chr(ord("a") + chosen_index))
            counts[chosen_index] -= 1
            previous_index = chosen_index

        return "".join(result)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × 26)`

Each of the `n` output positions scans the fixed 26-letter table once, and the tally is one pass over `s`.

##### Space Complexity: `O(n)`

The output builder `result` holds `n` characters; the count table is a fixed 26 entries.

#### Key Insights

- The strict selection rule makes correctness observable: the output of the scan is exactly the judged answer, with no room for an equivalent-but-different arrangement.
- Greedy by remaining frequency is sound for adjacency: the character just placed is temporarily barred, so always spending the largest remaining pile keeps filler available for the positions where the frequent character is ineligible.
- The failure mode is detected, not predicted: the construction returns `""` at the first position where every positive-count letter equals `previous`, so no feasibility formula is needed up front.

### Max-Heap Hold-Back

#### Derivation

The scan repeats a full 26-letter sweep per position just to find the largest eligible count. A [max-heap](https://en.wikipedia.org/wiki/Heap_(data_structure)) over `(-count, letter_index)` pairs exposes the largest count at the top in constant time for a fixed alphabet, but one obstacle remains: the heap's top may be the previously placed character, which is ineligible. The fix is a hold-back of one: pop the top, and if it is barred, place the next-best pair instead and push the held one back for later positions:

1. Tally `counts` with a 26-entry table and push every letter with a positive count onto `eligible` as `(-count, letter_index)` pairs.
2. Repeat `len(s)` times: pop the top pair. If it is the previous letter, return `""` when the heap is empty, otherwise hold it, pop the runner-up, place the runner-up, and push the held pair back. If the popped pair was not barred, place it directly.
3. Placing a letter decrements its count; the letter re-enters the heap only while its count is still positive.
4. Join the placed letters and return the string.

The heap orders by count first and by letter index second, so ties resolve to the lexicographically smallest letter and the judged selection rule is preserved exactly.

#### Walkthrough

Example 1, `s = "aab"`, starts from `eligible = [(-2, 'a'), (-1, 'b')]` in heap order. Each line is one output position:

```text
position 0   pop (-2,'a'), not previous -> place 'a', counts a:1, push (-1,'a')
             eligible = [(-1,'a'), (-1,'b')]   previous a    result "a"
position 1   pop (-1,'a'), equals previous -> hold it, pop (-1,'b') instead
             place 'b', counts b:0, push held (-1,'a') back
             eligible = [(-1,'a')]             previous b    result "ab"
position 2   pop (-1,'a'), not previous -> place 'a', counts a:0, nothing pushed
             eligible = []                     previous a    result "aba"
```

The `position 1` row is the mechanism: the heap's most frequent letter `a` is barred by `previous`, so the runner-up `b` is placed and `a` returns to the heap for the next position. The string is `"aba"`, which matches the expected Output for Example 1.

Example 2, `s = "aaab"`, shows the failure branch. After `positions 0` and `1` the state is `result "ab"`, `counts a:2`, `eligible = [(-2, 'a')]`, `previous b`:

```text
position 2   pop (-2,'a'), previous is b -> place 'a', counts a:1, push (-1,'a')
             eligible = [(-1,'a')]             previous a    result "aba"
position 3   pop (-1,'a'), equals previous -> hold it, heap is empty -> return ""
```

The last position needs a separator that no longer exists, so the function returns `""`, the expected Output for Example 2.

#### Solution

The code is the walkthrough's pop, hold-back, and push-back discipline over the 26-letter heap.

```python
import heapq
from typing import List, Tuple


class Solution:
    def solve(self, s: str) -> str:
        total_letters = 26
        counts: List[int] = [0] * total_letters
        for character in s:
            counts[ord(character) - ord("a")] += 1

        eligible: List[Tuple[int, int]] = []
        for letter_index in range(total_letters):
            if counts[letter_index] > 0:
                heapq.heappush(eligible, (-counts[letter_index], letter_index))

        result: List[str] = []
        previous_index = -1

        for _ in range(len(s)):
            top_pair = heapq.heappop(eligible)
            if top_pair[1] == previous_index:
                if not eligible:
                    return ""
                held_pair = top_pair
                top_pair = heapq.heappop(eligible)
                heapq.heappush(eligible, held_pair)

            chosen_index = top_pair[1]
            result.append(chr(ord("a") + chosen_index))
            counts[chosen_index] -= 1
            if counts[chosen_index] > 0:
                heapq.heappush(eligible, (-counts[chosen_index], chosen_index))
            previous_index = chosen_index

        return "".join(result)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log 26)`

Each of the `n` positions performs a constant number of heap operations on a heap of at most 26 pairs; the initial tally and heap build are proportional to the input length.

##### Space Complexity: `O(n)`

The output builder `result` holds `n` characters; the heap and the count table hold at most 26 entries each.

#### Key Insights

- The hold-back converts the "not the previous character" rule into heap mechanics: pop, and if the top is barred, place the runner-up and return the top to the heap.
- The heap's pair ordering `(-count, letter_index)` reproduces the tie rule exactly: most frequent first, lexicographically smallest on equal counts.
- The push-back after a hold is what keeps the held letter available for later positions; a letter with a positive count must always be present in the heap exactly once.
- The failure branch lives in the hold-back: the previous letter is barred and no runner-up exists, so no separator remains for the current position.

## Comparison of Solutions

### Time Complexity

- **Greedy Frequency Scan**: `O(n × 26)` - one full 26-letter scan per output position.
- **Max-Heap Hold-Back**: `O(n log 26)` - a constant number of heap operations per position on a heap capped at 26 pairs.

### Space Complexity

- **Greedy Frequency Scan**: `O(n)` - the output builder; the count table is fixed at 26 entries.
- **Max-Heap Hold-Back**: `O(n)` - the output builder; the heap and the count table are capped at 26 entries.

### Trade-offs

- **Greedy Frequency Scan**: the most direct transcription of the statement's rule, trivially verifiable against the judged output, but it re-scans all 26 letters at every position.
- **Max-Heap Hold-Back**: reaches each position's letter through heap operations instead of a scan, at the cost of the pop-and-hold-back choreography and a subtler failure branch.

### When to Use Each

- **Greedy Frequency Scan (Recommended)**: the interview default: it mirrors the statement's rule line for line, which makes correctness easy to argue and debug under time pressure.
- **Max-Heap Hold-Back**: when the alphabet outgrows a fixed 26 letters, where the scan's per-position sweep would stop being constant, or when a priority-queue idiom fits the surrounding code better.

### Optimization Notes

- Both approaches are `O(n)` up to the constant alphabet factor; the heap variant's `log 26` is a fixed constant, so the practical difference is code shape, not speed.
- A common pitfall is holding back the barred pair and forgetting to push it back: the held letter still has a positive count and must be available for the next position.
- An infeasible input is detected during construction, at the first position with no eligible letter; predicting feasibility before building requires the frequency bound `max_count <= (n + 1) // 2`.
