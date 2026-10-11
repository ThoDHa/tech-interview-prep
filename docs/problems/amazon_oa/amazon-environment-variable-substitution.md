# [Environment Variable Store and Substitution](https://www.fastprep.io/problems/amazon-environment-variable-substitution)

**Medium** | **NN minutes** | **String, Hash Table, Simulation**

Process a sequence of environment-variable operations:

["SET", key, value] stores or overwrites a value.["GET", key] emits the value or NULL when missing.["PARSE", text] emits text after replacing every complete %KEY% placeholder whose key exists. Missing placeholders remain unchanged.Substitution is one pass: replacement values are not expanded again during the same operation.

## Examples

### Example 1

**Input:** `operations = [["SET","NAME","Tom"],["PARSE","Hello I am %NAME%"]]`

**Output:** `["Hello I am Tom"]`

**Explanation:** The stored NAME value replaces its placeholder.

### Example 2

**Input:** `operations = [["GET","MISSING"],["PARSE","%MISSING%"]]`

**Output:** `["NULL","%MISSING%"]`

**Explanation:** Missing GET and PARSE have distinct deterministic outputs.

## Constraints

- `1 <= operations.length <= 10^5.`
- `Keys contain letters, digits, or underscores and are nonempty.`
- `Each operation row has the required fields.`

## Solutions

### Character Scanner with Store Lookup

#### Derivation

The literal reading of `PARSE` is a scanning duty: walk the text, and every time a `%` appears, decide whether it opens a complete placeholder. The statement pins down what "complete" means: a `%`, then a nonempty key of letters, digits, or underscores, then a closing `%`. A placeholder whose key is in the store is replaced; a well-formed placeholder whose key is missing stays exactly as written; a `%` that never closes, or that opens a malformed candidate, is an ordinary character. Scanning the original text only, never the output, is precisely the statement's one-pass rule:

1. Keep `store` as a dict; process operations in order. `SET` writes,
   `GET` appends the value or `"NULL"`, `PARSE` appends `parse(text)`.
2. Inside `parse`, batch the literal run up to the next `%` in one slice.
3. At a `%`, find the closing `%`. No closer means the rest of the text is
   literal.
4. The text between the two `%` marks is the candidate. When the candidate is a
   syntactically valid key, consume the whole `%candidate%` chunk: its store
   value if present, the chunk itself when missing. When the candidate is
   malformed, such as the empty text between two adjacent `%` marks, emit a
   single `%` and resume one character later, so the next `%` can still open a
   real placeholder.
5. Join the pieces.

#### Walkthrough

Example 1, `operations = [["SET","NAME","Tom"],["PARSE","Hello I am %NAME%"]]`. The `SET` fills the store, then the scan walks `"Hello I am %NAME%"` (the `%` marks sit at indices 11 and 16):

```text
SET NAME=Tom                store = {NAME: "Tom"}
PARSE "Hello I am %NAME%"
  pos 0   literal run up to '%' at 11   pieces = ["Hello I am "]
  pos 11  closing '%' at 16, candidate "NAME" (indices 12..15)
          valid key, in store -> value  pieces = ["Hello I am ", "Tom"]
  pos 17  end of text
join -> "Hello I am Tom"
```

Example 2 exercises both deterministic fallbacks, the `GET` miss and the missing placeholder:

```text
GET MISSING                 not in store -> "NULL"
PARSE "%MISSING%"
  pos 0   closing '%' at 8, candidate "MISSING" (indices 1..7)
          valid key, missing -> keep the chunk  pieces = ["%MISSING%"]
  pos 9   end of text
join -> "%MISSING%"
```

The output list collects the two emitted strings in order: `["NULL", "%MISSING%"]`, the expected Output.

#### Solution

The code is the scan from the walkthrough, with `is_placeholder_key` carrying the key-shape rule.

```python
from typing import Dict, List

KEY_CHARACTERS = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
)


def is_placeholder_key(candidate: str) -> bool:
    return bool(candidate) and all(
        character in KEY_CHARACTERS for character in candidate
    )


class Solution:
    def solve(self, operations: List[List[str]]) -> List[str]:
        store: Dict[str, str] = {}
        outputs: List[str] = []

        def parse(text: str) -> str:
            pieces: List[str] = []
            scan_position = 0
            while scan_position < len(text):
                if text[scan_position] != "%":
                    next_placeholder = text.find("%", scan_position)
                    if next_placeholder == -1:
                        pieces.append(text[scan_position:])
                        break
                    pieces.append(text[scan_position:next_placeholder])
                    scan_position = next_placeholder
                    continue
                closing_index = text.find("%", scan_position + 1)
                if closing_index == -1:
                    pieces.append(text[scan_position:])
                    break
                candidate = text[scan_position + 1:closing_index]
                if is_placeholder_key(candidate):
                    pieces.append(
                        store.get(candidate, text[scan_position:closing_index + 1])
                    )
                    scan_position = closing_index + 1
                else:
                    pieces.append("%")
                    scan_position += 1
            return "".join(pieces)

        for operation in operations:
            command = operation[0]
            if command == "SET":
                store[operation[1]] = operation[2]
            elif command == "GET":
                value = store.get(operation[1])
                outputs.append("NULL" if value is None else value)
            else:
                outputs.append(parse(operation[1]))
        return outputs
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(l)`

For a parsed text of length `l`, every character is consumed exactly once: literal runs move `scan_position` by whole slices, each placeholder chunk is skipped in one jump, and each store lookup hashes only the candidate key.

##### Space Complexity: `O(l)`

The pieces and the joined result hold at most the input text; the store is charged to the `SET` operations that filled it.

#### Key Insights

- The one-pass rule costs nothing to honor here: `parse` reads the input text and appends values into `pieces`, and nothing re-scans what it has already emitted, so a value containing `%SOMETHING%` stays unexpanded.
- A well-formed but missing key must be consumed as a whole chunk, not re-entered: resuming one character past a failed `%MISSING%` would let its closing `%` masquerade as the next opener and misparse what follows.
- Adjacent `%` marks degrade gracefully: the empty candidate fails the key check, a single `%` is emitted, and the scan resumes so the following `%KEY%` still resolves.
- `is_placeholder_key` looks redundant next to `candidate in store`, because stored keys are always well-formed; it is what tells a missing key (keep the chunk) apart from a malformed one (step over one character).

### Regex Substitution with Resolver

#### Derivation

The scanner's pointer bookkeeping buries the actual rule, which is a single sentence: replace every `%KEY%` whose `KEY` consists of key characters. That sentence is a [regular expression](https://en.wikipedia.org/wiki/Regular_expression), and `re.sub` accepts a function as the replacement, so the whole scan collapses into a pattern plus a resolver that consults the store. The character class comes straight from the constraints: keys are letters, digits, or underscores, which is `[A-Za-z0-9_]+`. A missing key returns `match.group(0)`, the untouched match, which also makes `re.sub` resume after the whole chunk, exactly the consume-or-keep behavior the scanner implements by hand:

1. Compile `PLACEHOLDER_PATTERN = %([A-Za-z0-9_]+)%` once at module level.
2. `parse` defines `resolve(match)`: return `store[key]`, or `match.group(0)`
   when the key is missing.
3. `parse` returns `PLACEHOLDER_PATTERN.sub(resolve, text)`.
4. The operation loop is unchanged.

#### Walkthrough

Example 1, `"Hello I am %NAME%"` with `store = {NAME: "Tom"}`. The pattern engine scans from the left and the first place a full `%KEY%` fits is the placeholder at the end:

```text
scan "Hello I am %NAME%"
  no match through index 10 (no '%' opens a candidate)
  match at span (11, 17): group(1) = "NAME"
  resolve: "NAME" in store -> replacement "Tom"
result "Hello I am Tom"
```

Example 2 matches but cannot resolve:

```text
scan "%MISSING%"
  match at span (0, 9): group(1) = "MISSING"
  resolve: "MISSING" not in store -> replacement match.group(0) = "%MISSING%"
result "%MISSING%"
```

`GET MISSING` contributes `"NULL"` before the parse, so the emitted list is `["NULL", "%MISSING%"]`, the expected Output.

#### Solution

The code is the pattern and resolver from the walkthrough; the operation loop is identical to the scanner's.

```python
import re
from typing import Dict, List

PLACEHOLDER_PATTERN = re.compile(r"%([A-Za-z0-9_]+)%")


class Solution:
    def solve(self, operations: List[List[str]]) -> List[str]:
        store: Dict[str, str] = {}
        outputs: List[str] = []

        def parse(text: str) -> str:
            def resolve(match: re.Match[str]) -> str:
                key = match.group(1)
                return store.get(key, match.group(0))

            return PLACEHOLDER_PATTERN.sub(resolve, text)

        for operation in operations:
            command = operation[0]
            if command == "SET":
                store[operation[1]] = operation[2]
            elif command == "GET":
                value = store.get(operation[1])
                outputs.append("NULL" if value is None else value)
            else:
                outputs.append(parse(operation[1]))
        return outputs
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(l)`

The pattern engine scans the text once; each position either joins a match or is skipped, and the resolver is one dict lookup per match.

##### Space Complexity: `O(l)`

The built result holds at most the input text plus the replacement values; the compiled pattern is a one-time module constant.

#### Key Insights

- The constraints are the pattern: `[A-Za-z0-9_]+` is the key grammar restated, so validity checking disappears into the match itself.
- Returning `match.group(0)` for a missing key is the whole keep-the-placeholder rule, and it inherits the consume-the-whole-chunk resume behavior for free.
- One-pass semantics hold because `re.sub` assembles its result from the original string; replacement text is never fed back into the scan.
- The resolver closes over `store`, so later `SET` operations are visible to later `PARSE` calls without any reconfiguration.

### Segment Cache with Deferred Resolution

#### Derivation

Both earlier versions weld the two halves of a parse together: the structural scan and the store lookup happen in one pass, so nothing reusable survives the call. When the same text is parsed repeatedly, which an environment store invites, the structure never changes while the values do. Splitting the pass in two fixes that: `segment_text` scans once into a list of segments, each a literal chunk or a key name, and `render` resolves segments against the store on demand. The resolution becomes the only per-parse work once a text's segments are cached:

1. `segment_text(text)` applies the same leftmost discipline as the scanner but
   records `("literal", chunk)` and `("key", name)` segments instead of
   resolving; a malformed candidate is recorded as a one-character literal `%`.
2. `solve` keeps `segment_cache`, a dict from parsed text to its segments, and
   fills it on first sight.
3. `render(segments, store)` joins the pieces, substituting `store[key]` for a
   key segment whose key exists and `%key%` for one that does not.
4. `GET` and `SET` are unchanged.

#### Walkthrough

Example 1 parses `"Hello I am %NAME%"` once and renders against the store:

```text
segment_text "Hello I am %NAME%"
  segments = [("literal", "Hello I am "), ("key", "NAME")]
render against {NAME: "Tom"}
  literal kept, key replaced -> "Hello I am Tom"
```

The payoff needs a tailored repeat, which the examples do not exercise: parse the same text again after `SET NAME=Andy`. The cache hit skips `segment_text` entirely, and `render` runs against the updated store:

```text
second PARSE "Hello I am %NAME%"
  segment_cache hit: segments reused, no scan
render against {NAME: "Andy"} -> "Hello I am Andy"
```

`GET MISSING` and the Example 2 parse behave as before (`"NULL"`, then the `%MISSING%` segment rendered unchanged), so the outputs match the expected Output.

#### Solution

The code separates the two passes from the walkthrough: `segment_text` is the scanner's discipline without the lookups, `render` is pure resolution.

```python
from typing import Dict, List, Tuple

Segment = Tuple[str, str]

KEY_CHARACTERS = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
)


def is_placeholder_key(candidate: str) -> bool:
    return bool(candidate) and all(
        character in KEY_CHARACTERS for character in candidate
    )


def segment_text(text: str) -> List[Segment]:
    segments: List[Segment] = []
    scan_position = 0
    while scan_position < len(text):
        placeholder_start = text.find("%", scan_position)
        if placeholder_start == -1:
            segments.append(("literal", text[scan_position:]))
            break
        if placeholder_start > scan_position:
            segments.append(("literal", text[scan_position:placeholder_start]))
        closing_index = text.find("%", placeholder_start + 1)
        if closing_index == -1:
            segments.append(("literal", text[placeholder_start:]))
            break
        candidate = text[placeholder_start + 1:closing_index]
        if is_placeholder_key(candidate):
            segments.append(("key", candidate))
            scan_position = closing_index + 1
        else:
            segments.append(("literal", "%"))
            scan_position = placeholder_start + 1
    return segments


def render(segments: List[Segment], store: Dict[str, str]) -> str:
    pieces: List[str] = []
    for kind, content in segments:
        if kind == "key":
            pieces.append(store.get(content, "%" + content + "%"))
        else:
            pieces.append(content)
    return "".join(pieces)


class Solution:
    def solve(self, operations: List[List[str]]) -> List[str]:
        store: Dict[str, str] = {}
        segment_cache: Dict[str, List[Segment]] = {}
        outputs: List[str] = []

        for operation in operations:
            command = operation[0]
            if command == "SET":
                store[operation[1]] = operation[2]
            elif command == "GET":
                value = store.get(operation[1])
                outputs.append("NULL" if value is None else value)
            else:
                text = operation[1]
                if text not in segment_cache:
                    segment_cache[text] = segment_text(text)
                outputs.append(render(segment_cache[text], store))
        return outputs
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(l)`

The first parse of a text scans its `l` characters once and every render walks the segment list once; repeated parses of cached text pay only the render.

##### Space Complexity: `O(l)`

The segment list holds each character of its text once, and the cache keeps one such list per distinct parsed text.

#### Key Insights

- Separating structure from values turns one `PARSE` into two cheaper duties: an `O(l)` scan that depends only on the text, and an `O(l)` join that depends only on the store.
- The cache is sound exactly because segments never consult the store: a `SET` between parses changes the render, never the structure.
- The scan half keeps the scanner's hard-won rules: well-formed keys are consumed whole, malformed candidates step over one `%`, and one-pass is automatic because values only ever enter `render`'s output.
- Against a single parse, the second list and the cache are pure overhead; the approach only earns its keep when texts repeat.

## Comparison of Solutions

### Time Complexity

- **Character Scanner with Store Lookup**: `O(l)` - one consuming pass over each parsed text with a dict lookup per well-formed placeholder.
- **Regex Substitution with Resolver**: `O(l)` - one engine pass per parsed text, the resolver charging one lookup per match.
- **Segment Cache with Deferred Resolution**: `O(l)` - one scan per distinct text, then a segment walk per parse, which repeated texts reduce to the walk alone.

### Space Complexity

- **Character Scanner with Store Lookup**: `O(l)` - the pieces list and the joined result for the current parse only.
- **Regex Substitution with Resolver**: `O(l)` - the built result per parse, plus one shared compiled pattern.
- **Segment Cache with Deferred Resolution**: `O(l)` - a retained segment list per distinct parsed text, on top of each render's output.

### Trade-offs

- **Character Scanner with Store Lookup**: no dependencies and every rule visible, at the cost of pointer bookkeeping that must get the consume-versus-step-over distinction right.
- **Regex Substitution with Resolver**: the shortest faithful expression of the rule, but the matching semantics live in a pattern string and a callback rather than in readable control flow.
- **Segment Cache with Deferred Resolution**: the only design that reuses parsing work across operations, paid for with a retained cache and a second function.

### When to Use Each

- **Character Scanner with Store Lookup (Recommended)**: the interview default: it demonstrates the scanning discipline and needs no library beyond a dict.
- **Regex Substitution with Resolver**: in production glue, where the pattern-plus-resolver pair is the idiomatic and least buggy way to state the rule.
- **Segment Cache with Deferred Resolution**: when templates repeat, such as re-rendering the same configuration text as the store evolves between parses.

### Optimization Notes

- All three are one-pass by construction: values enter the output from the store and are never re-scanned, which is exactly the statement's no-re-expansion rule; a naive loop of `text.replace("%KEY%", value)` calls would violate it, because a value containing `%OTHER%` could be expanded by a later iteration.
- The compiled pattern in the regex version lives at module level, so the compilation cost is paid once per process rather than once per parse.
- The malformed-candidate rule (step over one `%`) and the missing-key rule (consume the whole chunk) are easy to swap by accident; the walkthroughs' adjacent-`%` and repeated-placeholder traces are the tests that catch the swap.
- Literal runs are sliced in whole chunks rather than appended character by character, which keeps the constant factor low without changing the asymptotics.
