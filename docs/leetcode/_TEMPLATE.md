# [Problem Title](https://leetcode.com/problems/problem-slug/)

**Easy | Medium | Hard** | **NN minutes** | **Category, Category**

<!--
One to three short paragraphs restating the problem in plain prose. Keep the
wording close to LeetCode's, wrapping at a comfortable line width. Use `inline
code` for variable names and literal values.
-->

## Examples

### Example 1

**Input:** `arg = value`, `arg2 = value`

**Output:** `value`

**Explanation:** Why this output follows from the input. Use `inline code` for values. Omit this line when the mapping is self-evident.

### Example 2

**Input:** `arg = value`

**Output:** `value`

## Constraints

- `1 <= n <= 10^5`
- `-10^4 <= nums[i] <= 10^4`
- One bullet per constraint, copied from the problem.

## Follow-up

<!-- Optional. Include only when the problem poses a follow-up question. -->

Can you come up with an algorithm that beats the obvious approach?

## Deriving the Solution

<!--
==============================================================================
DERIVING THE SOLUTION (problem-level derivation arc):

  - This section answers "how would I ever come up with this?" for the problem
    as a whole, BEFORE any code appears. It walks from the most literal reading
    of the problem to the optimal insight, one idea per step.
  - Each step states an idea, names the specific cost or obstacle it hits, and
    lets that obstacle motivate the next step. The last step reaches the best
    approach in the file.
  - Each step links to the solution section it leads to, by heading anchor.
  - Keep it tight: one short framing paragraph plus 3-6 numbered steps. The
    per-solution Derivation sections carry the detail; this is the map, not
    the territory.
  - When several solutions are the same idea in different clothes (a boolean
    array vs a set vs a bitmask), one step may cover the family and link to
    each member.
==============================================================================
-->

One or two sentences framing the key reformulation or observation that every solution shares.

1. **Start literal.** The most direct reading of the problem: try the obvious
   thing. It works, but costs `O(...)`: see [Brute Force](#brute-force).
2. **Spot the waste.** Name the repeated or unnecessary work the literal
   approach performs.
3. **Fix it.** State what removing that waste buys and the approach it yields:
   see [Approach Name](#approach-name).
4. **Refine.** The final observation that reaches the optimal approach: see
   [Optimal Name](#optimal-name).

## Solutions

<!--
==============================================================================
SOLUTION CONVENTIONS (apply to every problem):

NAMING
  - Name each solution by its approach. Use the established algorithm name when
    one exists (Kadane's Algorithm, Boyer-Moore Voting, Dutch National Flag,
    Floyd's Cycle Detection, Morris Traversal), otherwise a clean technique name
    (Brute Force, Hash Map, Two Pointers, Sliding Window, Recursive DFS,
    Iterative BFS, Bottom-Up DP, Top-Down Memoization, Monotonic Stack, Sorting).
  - Never number solutions (no "### Solution 1"). Order alone conveys sequence.
  - No editorializing parenthetical qualifiers: avoid "(Optimal)", "(Educational)",
    "(Alternative)", "(Pythonic)", "(Most Common)", "(Hand-Written)", and the
    "Dynamic Programming (Subset-Sum Table)" style. ("(Recommended)" is fine
    inside a When-to-Use bullet, which is not a header.)

ORDERING (by discoverability, not raw speed)
  - The first solution is the most intuitive / self-derivable one: brute force,
    direct simulation, an obvious hashmap/set/sort written out by hand, or a
    plain DFS/BFS.
  - Later solutions are progressively more specialized: named algorithms and
    clever tricks you would have to learn or look up. The optimal solution
    usually lands last among the from-scratch approaches.
  - A LIBRARY TIDY-UP OF AN EARLIER APPROACH RANKS BETWEEN THE TWO: after every
    from-scratch solution, before any one-liner. This is the same algorithm with
    only its bookkeeping handed to the standard library (`Counter` for a
    hand-rolled tally, `functools.cache` for a hand-rolled memo dict, `bisect`
    for a hand-written binary search, `itertools.accumulate` for a running-total
    loop, `deque` for a `list.pop(0)` queue). The algorithm itself stays visible
    on the page: only the bookkeeping moves.
  - PYTHONIC ONE-LINERS GO LAST, after every from-scratch approach, even when
    they look trivially simple. A solution that leans on a built-in or stdlib
    call to do the core work (`sorted(s) == sorted(t)`, `Counter(a) == Counter(b)`,
    `len(set(x)) < len(x)`, `itertools.permutations`, `int(s, 2)` / `bin`, `re`)
    is ranked by what the language does for you, not by how short it reads. When
    several such shortcuts exist, the most library-driven one is last of all.

SECTION ORDER (within each solution)
  - Every solution section follows the derive-first flow: the reader should be
    able to reinvent the approach and execute it by hand before seeing code.
      #### Derivation       - how to arrive at the idea, ending in concrete steps
      #### Recurrence      - optional formula block (see FORMULAS below)
      #### Walkthrough     - hand-trace of the technique on a concrete input
      #### Solution        - the code block
      #### Time and Space Complexity Analysis
      #### Key Insights
  - The ordering serves one goal, the "click test": by the time the reader
    reaches the code, nothing in it should be new. The Derivation motivates
    every mechanism, the Walkthrough executes it by hand, and the code then
    reads as a transcript of what the reader has already done. If a line of
    code would surprise someone who stopped at the Walkthrough, a beat is
    missing earlier in the section.

DERIVATION
  - How the idea is arrived at, not a description of the finished algorithm:
    state the question this approach asks, and, for every solution after the
    first, the specific flaw of the previous approach it repairs. The chain of
    Derivation sections retells the Deriving the Solution arc in full detail.
  - End with the concrete numbered steps the code will follow, using the
    identifier names the code uses.

WALKTHROUGH
  - Trace the technique by hand on a concrete input, preferably an official
    Example. When no official Example exercises the mechanism worth showing
    (a memo hit, a rotation, a collision), a small tailored input may be used
    and must be introduced as such.
  - Show the evolving state (array, set, stack, call tree, table row) in a
    fenced ```text block, one snapshot or event per line.
  - Narrate with the identifier names the code will use (`dp`, `remaining`,
    `bits`), so the code that follows reads as the trace written down.
  - End by tying the final state to the expected output.
  - The walkthrough must execute the problem's core technique from scratch. It
    must NOT dodge the technique with a built-in (`sorted`/`.sort`, `Counter`,
    `bisect`, `heapq`, `itertools`, `re`, `int(s, 2)`): a built-in is allowed
    only when it is genuinely the core of the technique being taught (sorting
    in Merge Intervals), never as a substitute for the real logic.

LIBRARY COVERAGE (BOTH DIRECTIONS)
  - Library first: if a solution leans on a library to do the CORE work (Counter,
    heapq, bisect, itertools, OrderedDict, re, math), the file must ALSO include
    a from-scratch, library-free solution (hand-written binary search instead of
    bisect, hashmap + doubly linked list instead of OrderedDict, a 26-int count
    array instead of Counter). The idiomatic containers `deque` and `defaultdict`
    do NOT count as "the library doing the work" and may be used freely.
  - From-scratch first: the converse holds too. If every solution is hand-rolled
    and a stdlib helper would express one of them more cleanly, the file must
    ALSO include that tidied version, ranked per ORDERING above. A `deque` or
    `defaultdict` swap earns a section of its own only where the file
    deliberately teaches the hand-rolled container first (as Flood Fill does with
    `list.pop(0)`).
  - To tell which kind of section a helper yields, ask whether it replaces the
    ALGORITHM or only the BOOKKEEPING. Replacing bookkeeping gives a tidy-up.
    Replacing the algorithm gives a one-liner, which still belongs, but last, and
    only when the insight it evaluates is derived in full above it.
  - Never present avoiding an import as a virtue in itself. "Import-free" and
    "without any imported X" are not selling points: state the real trade instead
    (no hashing, a tighter constant, no version floor). Calling an approach
    library-free is legitimate only as one property inside a genuine trade-off,
    and only in a file that does carry its library section.

CODE
  - LeetCode style: `class Solution`, type hints, no Python 2 `(object)`. Keep
    code correct and verified against the examples. The code block lives under
    `#### Solution`.
  - `#### Solution` may open with a single bridging sentence tying the code
    back to the walkthrough (for example, "The code is the row update from
    the walkthrough: one downward sweep of `dp` per number."). One sentence
    at most; omit it when the tie-back is obvious.

FORMULAS
  - LaTeX renders site-wide (pymdownx.arithmatex + MathJax). Use `$$...$$` for
    display math and `\(...\)` inline.
  - Give a formula its own subsection between `#### Derivation` and
    `#### Walkthrough` when the solution rests on a stated relation: the
    derivation produces the relation, the walkthrough executes it, the code
    implements it. Name the block for what it holds: `#### Recurrence` for a
    DP transition, `#### Closed Form` for a direct expression (Binet, a
    binomial coefficient, the Task Scheduler frame), `#### Formula` for a
    defining equation the code evaluates, and `#### Invariant` when
    correctness rests on a property the loop preserves rather than on a
    formula. A more specific name is fine when it is more honest about the
    content: `#### Overlap Condition`, `#### Termination Condition`,
    `#### Invariant and Bound`.
  - An invariant block should say what the property is, why each branch
    preserves it, and what it implies at loop exit. The payoff is explaining a
    line of code that otherwise looks arbitrary: why Dutch National Flag does
    not advance `current` after a right swap, why the majority vote may adopt
    any value at `count == 0`, why sorting by start collapses a two-sided
    overlap test into a one-sided one.
  - When a DP's states hold collections rather than a scalar optimum (a list of
    combinations per sub-target, a set of strings per index) and uniqueness
    comes from the iteration order rather than from the transition, the honest
    block is `#### Invariant`, not `#### Recurrence`: the naive set-union
    relation over-counts permutations of the same collection and would be wrong
    written down. Combination Sum states what the loop order preserves instead.
  - One such block per file, on the solution where the relation is clearest
    (usually the bottom-up DP). Do NOT repeat it on every solution that shares
    the recurrence; later solutions refer back to it in prose. A genuinely
    different formulation of the same problem (a matrix power, a closed form)
    earns its own block on its own solution.
  - Keep the plain-text `inline code` version in the Derivation prose. The
    typeset block is the formal statement; the prose stays readable in the raw
    file on GitHub, where LaTeX does not render.
  - Every display equation inside the block must be followed by a fenced `text`
    block restating the same relation in plain ASCII, so the statement is
    legible in the raw file where the LaTeX is not rendered. Include the base
    case or side condition, and use the identifier names the code uses, not the
    typeset symbols. Where two display equations state one relation together,
    one fence covering both is enough. Keep it to the relation: the prose
    reading stays in prose.
  - State what the symbols mean and what the base case is. A formula with no
    reading of it is decoration.
  - Skip it when the relation is a single obvious assignment. Not every
    solution needs one.
  - Literal dollar signs in prose must be escaped as `\$`, or arithmatex will
    parse the text between two of them as inline math. Inside backticks or
    fenced code they are already safe.

==============================================================================
CHOOSE ONE LAYOUT:

  A) SINGLE SOLUTION   - one approach. Keep the one named `### <Name>` block
                         below, delete the multi-solution block AND the
                         `## Comparison of Solutions` section. Deriving the
                         Solution still appears, as a short arc deriving the
                         single approach.

  B) MULTIPLE SOLUTIONS - two or more approaches. Delete the single-solution
                          block, keep one named `### <Name>` block per solution,
                          and keep the `## Comparison of Solutions` section.
==============================================================================
-->

<!-- ----------------------------- LAYOUT A ----------------------------- -->

### Hash Map

#### Derivation

Derivation prose: the question this approach asks, the observation that makes it work, and where the idea comes from. End with the concrete steps:

1. First step.
2. Second step.
3. Third step.

#### Recurrence

<!--
Optional. See the FORMULAS conventions above. Name the block `#### Recurrence`,
`#### Closed Form`, or `#### Formula` to match what it states, and delete it
when the solution has no relation worth writing down.
-->

Let `dp[i]` be <what the state means>:

$$ dp[i] = \begin{cases}
<base case>, & i = 0 \\[4pt]
<transition>, & i > 0
\end{cases} $$

```text
dp[0] = <base case>
dp[i] = <transition>   for i > 0
```

One or two sentences reading the formula back: what the base case encodes, why the bounds are what they are, and where the answer is read from.

#### Walkthrough

Hand-trace of the technique on a concrete input (see the WALKTHROUGH conventions above), showing the evolving state:

```text
step 1   state after step 1
step 2   state after step 2
```

Closing sentence tying the final state to the expected output.

#### Solution

```python
class Solution:
    def method(self, ...) -> ...:
        # implementation
        ...
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Why the time bound holds.

##### Space Complexity: `O(1)`

Why the space bound holds.

#### Key Insights

- The non-obvious observation that makes the solution work.
- A tradeoff or corner case the approach handles cleanly.
- A pitfall avoided.

<!-- --------------------------- END LAYOUT A --------------------------- -->

<!-- ----------------------------- LAYOUT B ----------------------------- -->

### Brute Force

#### Derivation

The most literal reading of the problem and the steps it dictates:

1. First step.
2. Second step.

#### Walkthrough

Hand-trace on a concrete input:

```text
step 1   state after step 1
step 2   state after step 2
```

Closing sentence tying the final state to the expected output.

#### Solution

```python
class Solution:
    def method(self, ...) -> ...:
        # implementation
        ...
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Why the time bound holds.

##### Space Complexity: `O(1)`

Why the space bound holds.

#### Key Insights

- Insight specific to this approach.
- Why it is simple but limited.

### Hash Map

#### Derivation

The flaw in the previous approach this one repairs, the observation that repairs it, and the steps that follow:

1. First step.
2. Second step.

#### Walkthrough

Hand-trace on a concrete input:

```text
step 1   state after step 1
step 2   state after step 2
```

Closing sentence tying the final state to the expected output.

#### Solution

```python
class Solution:
    def method(self, ...) -> ...:
        # implementation
        ...
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Why the time bound holds.

##### Space Complexity: `O(n)`

Why the space bound holds.

#### Key Insights

- Insight specific to this approach.
- The space-time tradeoff it represents.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - one-line reason.
- **Hash Map**: `O(n)` - one-line reason.

### Space Complexity

- **Brute Force**: `O(1)` - one-line reason.
- **Hash Map**: `O(n)` - one-line reason.

### Trade-offs

- What the Brute Force approach gives up and gains.
- What the Hash Map approach gives up and gains.

### When to Use Each

- **Brute Force**: The situation where it is the right call.
- **Hash Map**: The situation where it is the right call.

### Optimization Notes

- Implementation detail worth highlighting (for example, computing `mid` as
  `left + (right - left) // 2` to avoid overflow).
- Production considerations.

<!-- --------------------------- END LAYOUT B --------------------------- -->
