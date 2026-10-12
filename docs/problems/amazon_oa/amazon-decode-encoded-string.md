# [Decode an Encoded String](https://www.fastprep.io/problems/amazon-decode-encoded-string)

**Medium** | **NN minutes** | **String, Stack, Parsing**

An encoded string uses positive repeat counts followed by bracketed segments. Decode it using these rules:

k[segment] means the decoded segment is repeated exactly k times.Segments may be nested.Letters outside brackets appear once and remain in order.Return the fully decoded string.

## Examples

### Example 1

**Input:** `s = "3[a2[c]]"`

**Output:** `"accaccacc"`

**Explanation:** The inner block becomes acc, then the outer count repeats it three times.

### Example 2

**Input:** `s = "2[ab]3[c]"`

**Output:** `"ababccc"`

**Explanation:** The two adjacent encoded blocks decode independently and are concatenated.

## Constraints

- `1 <= s.length <= 10^4`
- `s is a well-formed encoding made of lowercase English letters, digits, and brackets.`
- `Every repeat count is between 1 and 300.`
- `The decoded string has at most 10^5 characters.`

## Solutions

### Recursive Descent by Cursor

#### Derivation

The encoding is a grammar in disguise: a segment is a sequence of letters and `k[segment]` blocks, and blocks nest. The most direct reading of that grammar is to write the decoder for one segment and let the bracket nesting drive the recursion: scanning a segment letter by letter, a letter is appended, a digit run starts a block whose body is decoded by a recursive call to the same routine. A shared cursor `position` marks where the scan stands, and every branch advances it:

1. Define `decode_segment`, reading from the shared cursor `position` and
   appending to a `decoded` list until it sees `]` or the end of `s`.
2. On a digit, accumulate the full multi-digit run into `repeat_count`, then
   step past the `[` and recurse; the call returns when it hits the matching
   `]`.
3. Multiply the returned segment by `repeat_count`, append it to `decoded`, and
   step past the `]`.
4. On a letter, append it and advance one place.
5. Return `"".join(decoded)`; the top-level call returns the whole string.

#### Walkthrough

Example 1, `s = "3[a2[c]]"`. Each line is one cursor event; `depth` is the recursion level:

```text
depth 0   position 0   digit run "3" -> repeat_count = 3, position 1
          position 1   consume '[' -> position 2, recurse
depth 1   position 2   letter 'a' -> decoded ["a"], position 3
          position 3   digit run "2" -> repeat_count = 2, position 4
          position 4   consume '[' -> position 5, recurse
depth 2   position 5   letter 'c' -> decoded ["c"], position 6
          position 6   ']' -> return "c"
depth 1   position 6   consume ']' -> position 7; decoded ["a" + "c" x 2] = ["acc"]
          position 7   ']' -> return "acc"
depth 0   position 7   consume ']' -> position 8; decoded ["acc" x 3] = ["accaccacc"]
          position 8   end of s -> return "accaccacc"
```

The returned `"accaccacc"` matches the expected Output. Note where the recursion hands work back: the inner call stops at the matching `]` without consuming it, and the caller is the one that steps over it, which is what keeps each level's multiplier attached to its own block.

#### Solution

The code is the walkthrough's cursor loop and its three branches:

```python
from typing import List


class Solution:
    def solve(self, s: str) -> str:
        """Return the fully decoded string.

        Time:  O(output_length): every decoded character is appended once per
            replication level it participates in, and joins are linear.
        Space: O(output_length) for the decoded pieces plus recursion depth
            bounded by the nesting depth.
        """
        position = 0

        def decode_segment() -> str:
            nonlocal position
            decoded: List[str] = []
            while position < len(s) and s[position] != "]":
                if s[position].isdigit():
                    repeat_count = 0
                    while s[position].isdigit():
                        repeat_count = repeat_count * 10 + int(s[position])
                        position += 1
                    position += 1
                    decoded.append(decode_segment() * repeat_count)
                    position += 1
                else:
                    decoded.append(s[position])
                    position += 1
            return "".join(decoded)

        return decode_segment()
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(output_length)`

Every character of the output is produced a constant number of times: once when first decoded and once per enclosing replication when the enclosing blocks repeat it, so the total work is linear in the final string length (bounded at `10^5` by the constraints).

##### Space Complexity: `O(output_length)`

The `decoded` pieces and their joins hold at most the output, plus recursion depth equal to the bracket nesting depth.

#### Key Insights

- The bracket nesting *is* the call structure: a recursive-descent decoder falls out of the grammar with no explicit data structure beyond the cursor.
- The digit run must be accumulated before recursing, because counts like `300` span several digits and the loop would otherwise read only one.
- Recursion depth equals nesting depth, so a hostile deeply-nested input pushes against Python's recursion limit; the stack version below removes that exposure.

### Iterative Two-Stack

#### Derivation

The recursive decoder leaves two jobs to the call stack: remembering the multiplier of each open block, and remembering the text built so far outside it. The repair that removes the call stack is to hold both in explicit stacks, `count_stack` and `segment_stack`, and keep the text of the block currently being read in `current_segment`. Reading `[` saves the unfinished text as a prefix and starts fresh; reading `]` finishes the block, multiplies it by its saved count, and glues it back onto the saved prefix. One left-to-right pass, no recursion:

1. Keep `current_segment` as a list of characters, `repeat_count` as the digit
   accumulator, and both stacks empty.
2. On a digit: extend `repeat_count` (`repeat_count * 10 + digit`).
3. On `[`: push `repeat_count` onto `count_stack`, push the joined
   `current_segment` onto `segment_stack`, then reset both to empty.
4. On a letter: append it to `current_segment`.
5. On `]`: pop `(repeat, prefix)`; rebuild `current_segment` as the single piece
   `prefix + joined_current × repeat`.
6. Return the joined `current_segment`.

#### Walkthrough

Example 1, `s = "3[a2[c]]"`, one line per input character:

```text
read 3    repeat_count = 3
read [    push (3, "");            current = [],  count_stack [3],       segments [""]
read a    current = "a"
read 2    repeat_count = 2
read [    push (2, "a");           current = [],  count_stack [3,2],     segments ["", "a"]
read c    current = "c"
read ]    pop (2, "a"): current = "a" + "c" x 2 = "acc"
read ]    pop (3, ""):  current = "" + "acc" x 3 = "accaccacc"
```

`current` ends as `"accaccacc"`, matching the expected Output. The decisive beat is the first `]`: the pair `(2, "a")` popped is exactly the multiplier and prefix saved when the inner `[` was read, so the reconstruction `prefix + text × repeat` rebuilds `acc` in one step. Example 2, `s = "2[ab]3[c]"`, runs the same loop without nesting: the first `]` produces `abab`, the letters `c` extend it to `ababc`, and the second `]` replaces the final `c` with `ccc`, giving `ababccc`.

#### Solution

The code is the walkthrough's five-branch scan over the stacks:

```python
from typing import List


class Solution:
    def solve(self, s: str) -> str:
        """Return the fully decoded string.

        Time:  O(output_length): each input character is processed once, and
            each `]` rebuild copies text proportional to what it contributes to
            the final string.
        Space: O(output_length) for the segment stacks and current_segment.
        """
        segment_stack: List[str] = []
        count_stack: List[int] = []
        current_segment: List[str] = []
        repeat_count = 0

        for character in s:
            if character.isdigit():
                repeat_count = repeat_count * 10 + int(character)
            elif character == "[":
                count_stack.append(repeat_count)
                segment_stack.append("".join(current_segment))
                current_segment = []
                repeat_count = 0
            elif character == "]":
                repeat = count_stack.pop()
                prefix = segment_stack.pop()
                current_segment = [prefix + "".join(current_segment) * repeat]
            else:
                current_segment.append(character)

        return "".join(current_segment)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(output_length)`

The scan reads each input character once; each `]` joins text that later contributes directly to the output, so total copying stays linear in the final length.

##### Space Complexity: `O(output_length)`

The two stacks hold one prefix and one count per open bracket, and the prefixes plus `current_segment` never exceed the output size.

#### Key Insights

- The pair pushed at `[` (count, prefix) is exactly the call frame the recursive version kept: the multiplier and the text to resume with after the block closes.
- Keeping `current_segment` as a character list and joining only at push and pop time avoids quadratic string concatenation in the letter branch.
- This is the version to write in an interview: one pass, no recursion limit, and the stack contents are easy to draw in a walkthrough.

### Regex Expansion

#### Derivation

The library view of the problem: an encoding is decoded by repeatedly rewriting every innermost block `k[letters]`, one with no nested brackets of its own, into its expansion, until no bracket remains. That is a text-substitution loop, and [regular expressions](https://docs.python.org/3/library/re.html) express the rewrite rule directly: `(\d+)\[([a-z]*)\]` matches a bracket-free block, and each pass replaces every match with its letters repeated `k` times. The algorithm is the loop itself; the derivation is recognizing that innermost-first rewriting converges to the decoded string:

1. Compile `pattern = (\d+)\[([a-z]*)\]`, which matches exactly the blocks
   without nested brackets.
2. While `pattern` finds a match in `s`, replace all matches with
   `letters × count` in one pass.
3. When no match remains, no bracket remains either, and `s` is decoded.

#### Walkthrough

Example 2, `s = "2[ab]3[c]"`, where both blocks are innermost from the start:

```text
pass 1   matches "2[ab]" -> "abab",  "3[c]" -> "ccc"
         s = "ababccc"
pass 2   no bracket remains -> return "ababccc"
```

The returned `"ababccc"` matches the expected Output. Nesting takes more passes, each peeling one level: Example 1, `s = "3[a2[c]]"`, rewrites `2[c]` into `cc` on pass 1 (leaving `3[acc]`) and expands the outer block on pass 2, ending at `"accaccacc"`.

#### Solution

The code is the rewrite loop over `pattern.sub`:

```python
import re


class Solution:
    def solve(self, s: str) -> str:
        """Return the fully decoded string.

        Time:  O(passes × length): each pass scans and rebuilds the whole
            string, and the number of passes equals the bracket nesting depth.
        Space: O(output_length) for the rebuilt string each pass.
        """
        pattern = re.compile(r"(\d+)\[([a-z]*)\]")
        while pattern.search(s):
            s = pattern.sub(lambda match: int(match.group(1)) * match.group(2), s)
        return s
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(passes × length)`

Each pass scans and rebuilds the entire current string; the pass count equals the nesting depth, so the total is the depth times the string length at its largest, strictly worse than the single-pass stack version.

##### Space Complexity: `O(output_length)`

Every pass allocates a fresh rebuilt string of at most the output size.

#### Key Insights

- The pattern matches only bracket-free blocks, which is what makes innermost-first expansion well defined: a pass never rewrites a block whose body is still encoded.
- Adjacent blocks collapse in a single pass (`re.sub` replaces every match), but nesting costs one pass per level, so deeply nested inputs pay repeatedly.
- The one-liner earns its place as a cross-check or a quick script; an interview answer should reach for the stack version first and mention this one as the library observation.

## Comparison of Solutions

### Time Complexity

- **Recursive Descent by Cursor**: `O(output_length)` - one pass whose copying work is linear in the final string.
- **Iterative Two-Stack**: `O(output_length)` - one pass over the input with linear-time joins at each `]`.
- **Regex Expansion**: `O(passes × length)` - one full scan and rebuild per nesting level.

### Space Complexity

- **Recursive Descent by Cursor**: `O(output_length)` - decoded pieces plus recursion depth equal to the nesting depth.
- **Iterative Two-Stack**: `O(output_length)` - two stacks of open-block prefixes and counts.
- **Regex Expansion**: `O(output_length)` - a rebuilt string per pass.

### Trade-offs

- **Recursive Descent by Cursor**: the closest transcription of the grammar and easy to extend to richer syntaxes, but the call stack grows with nesting depth and the shared cursor needs the `nonlocal` discipline to stay correct.
- **Iterative Two-Stack**: single pass, no recursion limit, and the explicit stacks make the state drawable, at the cost of bookkeeping branches for every bracket kind.
- **Regex Expansion**: the shortest program and a natural mental model (rewrite innermost blocks), but it rescans the string once per nesting level and leans on a regular expression to do the core parsing.

### When to Use Each

- **Iterative Two-Stack (Recommended)**: the interview default: one pass, no recursion-depth exposure, and the walkthrough draws itself.
- **Recursive Descent by Cursor**: when the encoding grammar may grow (multiple block kinds, separators) and a parser-shaped answer generalizes cleanly.
- **Regex Expansion**: for a quick script, a test oracle, or as the closing observation that the problem is repeated innermost-first rewriting.

### Optimization Notes

- The count is multi-digit (`1 <= repeat count <= 300`), so both hand-rolled versions must accumulate `repeat_count * 10 + digit` until the `[`; reading a single digit silently breaks on `300[a]`.
- Building segments as character lists and joining only at bracket events keeps the letter branch `O(1)`; concatenating strings per letter is the classic quadratic slip.
- All three versions are linear-or-better in the decoded length, which the constraints cap at `10^5`; if decoded outputs were unbounded, the right move would be to return a lazy segment tree or stream pieces instead of materializing the string.
