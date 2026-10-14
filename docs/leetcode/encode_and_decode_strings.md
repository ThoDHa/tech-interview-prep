# [Encode and Decode Strings](https://leetcode.com/problems/encode-and-decode-strings/)

**Medium** | **25 minutes** | **Array, String, Design**

**Pattern:** [Data-Structure Design](../patterns/design/intuition.md)

**Algorithm:** [Delimiter](https://en.wikipedia.org/wiki/Delimiter) · [Escape character](https://en.wikipedia.org/wiki/Escape_character) · [Netstring](https://en.wikipedia.org/wiki/Netstring)

**Practice:** [`practice/encode_and_decode_strings/solution.py`](../../practice/encode_and_decode_strings/solution.py)

> This problem is locked behind [LeetCode Premium](https://leetcode.com/problems/encode-and-decode-strings/); read it free on [NeetCode](https://neetcode.io/problems/string-encode-and-decode).

Design an algorithm to encode **a list of strings** to **a string**. The **encoded string** is then sent over the network and is **decoded** back to the **original list** of strings.

**Machine 1 (sender)** has the function:

```java
String encode(List<String> strs) {
    // ... your code
    return encoded_string;
}
```

**Machine 2 (receiver)** has the function:

```java
List<String> decode(String encoded_string) {
    // ... your code
    return decoded_strs;
}
```

So **Machine 1** does:
```java
String encoded_string = encode(strs);
```

and **Machine 2** does:
```java
List<String> decoded_strs = decode(encoded_string);
```

`decoded_strs` in Machine 2 should be the **same** as the input `strs` in Machine 1.

Implement the `encode` and `decode` methods.

## Examples

### Example 1

**Input:** `strs = ["Hello","World"]`

**Output:** `["Hello","World"]`

**Explanation:**

```java
Solution solution = new Solution();
String encoded_string = solution.encode(strs);

// Machine 1 ---encoded_string---> Machine 2

List<String> decoded_strs = solution.decode(encoded_string);
```

### Example 2

**Input:** `strs = [""]`

**Output:** `[""]`

## Constraints

- `0 <= strs.length < 100`
- `0 <= strs[i].length < 200`
- `strs[i]` contains any possible characters out of `256` valid ASCII characters.

## Follow-up

Could you write a generalized algorithm to work on any possible set of characters?

## Deriving the Solution

Decoding a flat string back into a list needs one thing: a way to find each string's boundary inside the stream. Every design below either *escapes* the payload so boundaries cannot be confused with content, or *declares* each payload's length so content is never inspected at all, and the designs divide exactly along that line.

1. **Start literal.** Join the strings with a chosen delimiter such as `","` and split on it. One payload holding that same character corrupts the round trip: see [Naive Delimiter](#naive-delimiter).
2. **Spot the flaw.** The boundary marker must be *distinguishable* from payload content, and joining alone guarantees the opposite: content flows into the boundary grammar unchecked.
3. **Fix it by escaping.** Quote the delimiter inside payloads so content can no longer produce a real boundary, then split on the unquoted ones: see [Escaped Delimiter](#escaped-delimiter).
4. **Fix it by counting instead.** Rather than hiding boundaries inside content, state each payload's length up front (`len#content`); the decoder reads digits up to `#` and slices exactly that many characters, never examining payload bytes at all. Content cannot corrupt anything it is never parsed: see [Length-Prefixed Encoding](#length-prefixed-encoding).

## Solutions

### Naive Delimiter

#### Derivation

The most direct reading of "send a list as one string" picks a separator that cannot appear in ordinary text, glues the strings together, and cuts them apart on the other side:

1. `encode` joins `strs` with a delimiter such as `","`.
2. `decode` calls `split` on the same delimiter.
3. The resulting list is returned as the decoded payload.

#### Walkthrough

Trace the round trip on Example 1: `strs = ["Hello","World"]`. The join glues the two payloads with a comma:

```text
encode ["Hello","World"]  ->  "Hello,World"
split "Hello,World" on ","  ->  ["Hello", "World"]
```

The decoded list matches the input. The design only holds while payloads obey the assumption, which Example-level inputs do: nothing above contains a bare comma.

#### Solution

The code is the join and the split from the walkthrough.

```python
from typing import List


class Solution:
    def encode(self, strs: List[str]) -> str:
        return ",".join(strs)

    def decode(self, s: str) -> List[str]:
        return s.split(",")
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(total)`

Both directions touch every character of every string a constant number of times, where `total` is the combined length of the payloads.

##### Space Complexity: `O(total)`

The encoded string and the decoded list each hold the full payload once.

#### Key Insights

- Perfectly correct *under its assumption* that the delimiter never occurs in a payload.
- The constraint section explicitly breaks that assumption: payloads may contain any of 256 ASCII characters, `","` included.
- This solution exists to be the baseline that later designs repair, and naming the exact broken input is the interview value here: `[",", ","]` encodes to `",,,"`, which decodes to four empty strings, and a single `","` payload is lost entirely.

### Escaped Delimiter

#### Derivation

The naive design fails because payload bytes are allowed to impersonate a boundary. Escaping removes the impersonation: inside a payload, every occurrence of the delimiter's own character is rewritten to a two-character sequence no real boundary can produce, so the only unescaped delimiters left in the stream are genuine separators:

1. Pick a delimiter, here `,`, and an escape prefix, here `\`.
2. In `encode`, replace every `\` in a payload with `\\` first, then every `,` with `\,`, and join with `,`.
3. In `decode`, walk the string one character at a time.
4. A `\` means the next character is literal payload: record it and skip ahead two.
5. A `,` ends the current payload; anything else is literal.
6. Emit the final payload after the last delimiter.

Doubling the backslash first is what makes the encoding reversible: a lone `\` in the stream can only ever be an escape prefix, never the tail of a doubled one.

#### Walkthrough

Trace both directions on an input chosen to exercise the escape rules (the statement's examples contain no escapable characters): `strs = ["a,b", "c\d"]`.

```text
encode (raw characters, no quoting):
"a,b"   doubling: no backslash present, unchanged
        comma escape: , -> \,            ->  a\,b
"c\d"   doubling: \ -> \\                ->  c\\d
        comma escape: none
join with ,                             ->  a\,b,c\\d

decode (stream a \ , b , c \ \ d):
scan "a"     literal            -> payload "a"
scan "\,"    escaped comma      -> payload "a,"
scan "b"     literal            -> payload "a,b"
scan ","     real delimiter     -> emit payload 1 = "a,b"; start payload 2
scan "c"     literal            -> payload "c"
scan "\\"    escaped backslash  -> payload "c\"
scan "d"     literal            -> payload "c\d"
end of stream                   -> emit payload 2 = "c\d"
```

The decode returns `["a,b", "c\d"]`, the original input: every escaped byte survived the round trip. The naive design on the same input splits at `a,b`'s real comma and loses.

#### Solution

The code is the two rewrite passes into the stream, and the two-mode scan out of it.

```python
from typing import List


class Solution:
    def encode(self, strs: List[str]) -> str:
        escaped = [s.replace("\\", "\\\\").replace(",", "\\,") for s in strs]
        return ",".join(escaped)

    def decode(self, s: str) -> List[str]:
        decoded = []
        current = []
        position = 0
        while position < len(s):
            if s[position] == "\\":
                current.append(s[position + 1])
                position += 2
            elif s[position] == ",":
                decoded.append("".join(current))
                current = []
                position += 1
            else:
                current.append(s[position])
                position += 1
        decoded.append("".join(current))
        return decoded
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(total)`

Encoding rewrites each character once; decoding advances `position` by `1` or `2` per step, so the whole stream is read once.

##### Space Complexity: `O(total)`

The escaped stream and the decoded list each hold the payload plus at most one escape byte per special character.

#### Key Insights

- Restores correctness by making the boundary grammar unambiguous: content can mention the delimiter only in quoted form.
- Generalizes to any delimiter/prefix pair; the follow-up's "any possible set of characters" is answered by choosing a prefix and escaping it and the delimiter consistently.
- The trailing `decoded.append` after the loop exists because the stream carries no delimiter after the last payload; forgetting it drops the final string (and mishandles `strs = [""]`, whose encoding is the empty string).

### Length-Prefixed Encoding

#### Derivation

Escaping repairs a broken grammar, but the deeper move is to stop parsing payload bytes altogether. Each string's length is known to the encoder and is itself payload-free data; declaring it in the stream (`len#content`) hands the decoder a count it can trust and a slice it can take blind. The `#` matters only because the digit run needs an end marker: `12abc` could be length `1` then `2abc`, or length `12` then `abc`. Digits stop being ambiguous the moment a non-digit, here `#`, closes them:

1. In `encode`, build `"len(s) # s"` for each string and concatenate.
2. In `decode`, find the next `#` from the current position.
3. Parse the digits before it as `length` and slice the `length` characters after it as the payload.
4. Advance past the payload and repeat until the stream is exhausted.

A payload of digits and `#` characters cannot interfere: those bytes sit *after* the count, and the decoder jumps over them without reading them.

#### Walkthrough

Trace the round trip on Example 1: `strs = ["Hello","World"]`:

```text
encode:
"Hello" -> "5#Hello"   "World" -> "5#World"
concatenate            ->  "5#Hello5#World"

decode:
position 0   next "#" at 1   length = int("5") = 5
             slice [2:7]     -> "Hello"    position = 7
position 7   next "#" at 8   length = int("5") = 5
             slice [9:14]    -> "World"    position = 14
end of stream -> ["Hello", "World"]
```

The decode returns `["Hello","World"]`, matching Example 1 exactly. Example 2's `strs = [""]` encodes to `"0#"`, and one iteration reads length `0` and slices an empty payload, returning `[""]`: an empty list entry survives because its *length* is transmitted, not its content. The same mechanism defeats hostile payloads: `"3#abc"` as a single string encodes to `"5#3#abc"`, and the decoder reads count `5`, slices all of `"3#abc"`, and stops.

#### Solution

The code is the walkthrough's two loops: concatenate on the way in, count-and-slice on the way out.

```python
from typing import List


class Solution:
    def encode(self, strs: List[str]) -> str:
        return "".join(f"{len(s)}#{s}" for s in strs)

    def decode(self, s: str) -> List[str]:
        decoded = []
        position = 0
        while position < len(s):
            delimiter = s.index("#", position)
            length = int(s[position:delimiter])
            start = delimiter + 1
            decoded.append(s[start : start + length])
            position = start + length
        return decoded
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(total)`

Encoding writes every character once; decoding's `s.index` and slice together advance `position` across each byte a constant number of times.

##### Space Complexity: `O(total)`

The encoded stream carries every payload character plus a short header per string, and the decoded list restores the payloads.

#### Key Insights

- Self-describing data: the length header means the decoder never inspects payload bytes, so no character set can corrupt the framing (this answers the follow-up directly).
- The `#` is not decoration: without a terminator for the digit run, `12abc` would not parse.
- This framing is not an interview artifact: HTTP chunked transfer encoding, netstrings, and Redis's protocol all declare lengths for exactly this reason.
- Against the Escaped Delimiter design it needs no forbidden-character rules and its decoder never backtracks; its cost is a few header bytes per string.

## Comparison of Solutions

### Time Complexity

- **Naive Delimiter**: `O(total)` - one join and one split over the stream.
- **Escaped Delimiter**: `O(total)` - one rewrite pass and one linear scan.
- **Length-Prefixed Encoding**: `O(total)` - one concatenation pass and one count-and-slice scan.

### Space Complexity

- **Naive Delimiter**: `O(total)` - the stream plus the decoded list.
- **Escaped Delimiter**: `O(total)` - the stream with escape bytes plus the decoded list.
- **Length-Prefixed Encoding**: `O(total)` - the stream with headers plus the decoded list.

### Trade-offs

- **Naive Delimiter** is two standard-library calls, and incorrect on the very inputs the constraints permit.
- **Escaped Delimiter** is fully general but its correctness rests on an escape discipline the reader must trace (double the prefix first, scan with a two-character skip).
- **Length-Prefixed Encoding** separates framing data from payload data entirely, so correctness is structural rather than conventional; it pays a small per-string header.

### When to Use Each

- **Naive Delimiter**: demonstrations of the boundary problem; never for the stated constraints.
- **Escaped Delimiter**: streaming settings where a sender cannot compute a length before transmitting.
- **Length-Prefixed Encoding**: the default wire format and the interview answer (recommended here).

### Optimization Notes

- Nothing per-character can be trimmed: every byte must cross the wire once, so `O(total)` is a floor and the designs differ in correctness, not speed.
- The header overhead is `digits(len) + 1` bytes per string; with the given constraints (length under 200) it is at most 4 bytes per payload.
- If a truly arbitrary character set included the length digits themselves, the Length-Prefixed design still works unchanged: digits in payloads are never parsed, only skipped over.
