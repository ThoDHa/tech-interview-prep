# [Domain Weight Calculation](https://www.fastprep.io/problems/amazon-domain-weight-calculation)

**Medium** | **NN minutes** | **String, Hash Table, Trie, Depth First Search**

Source note: This came from a real onsite interview report. The original report shared the core domain-score task and a concrete example, and FastPrep filled in the runnable function format, ordering rule, and extra practice examples so you can try it here. Estimated match rate: 90% for the core task, 75% for interface and examples, and 35% for exact original wording. If you find a fuller version, feel free to let us know and we will update it.

You are given an array of strings domainScores. Each string has this format:

domain scoredomain is a dot-separated domain name, and score is an integer weight assigned directly to that domain.

For every leaf domain, compute its total score. A domain is a leaf domain if it appears in domainScores and no other input domain has it as a suffix child.

The total score of a leaf domain is the sum of the scores assigned to that domain and all of its suffix ancestors that appear in the input.

For example, the suffix ancestors of mail.domain.com are domain.com and com.

Return one string for each leaf domain in lexicographic order. Each output string should have this format:

domain=totalScoreWhat the interview report sharedThe interview report described a domain-score task: every domain has its own score, and the candidate had to output each leaf domain's accumulated score. The report included an example where mail.domain.com accumulated scores from mail.domain.com, domain.com, and com, and contact.user.test.com accumulated scores from all of its suffix ancestors. The report did not specify the function signature, constraints, or output ordering.

How FastPrep adapted itFastPrep turned that report into a runnable practice problem by using an array of "domain score" strings as input and returning sorted "domain=score" strings. The lexicographic ordering rule and additional examples are practice scaffolding based on the reported task, not exact original wording.

## Examples

### Example 1

**Input:** `domainScores = ["com 20", "domain.com 10", "mail.domain.com 5", "test.com 10", "user.test.com 30", "contact.user.test.com -5"]`

**Output:** `["contact.user.test.com=55", "mail.domain.com=35"]`

**Explanation:** mail.domain.com is a leaf, and its total is 5 + 10 + 20 = 35.

contact.user.test.com is also a leaf, and its total is -5 + 30 + 10 + 20 = 55.

### Example 2

**Input:** `domainScores = ["com 5", "a.com 2", "b.com 3"]`

**Output:** `["a.com=7", "b.com=8"]`

**Explanation:** a.com and b.com are leaves. Both include the score of their suffix ancestor com.

### Example 3

**Input:** `domainScores = ["api.shop.com 4", "shop.com -2", "com 1", "cdn.shop.com 7", "img.cdn.shop.com 3"]`

**Output:** `["api.shop.com=3", "img.cdn.shop.com=9"]`

**Explanation:** cdn.shop.com is not a leaf because img.cdn.shop.com is one of its suffix children.

## Constraints

- `1 <= domainScores.length <= 100000`
- `Each input string contains exactly one domain and one integer score separated by one space.`
- `Domain names contain lowercase English letters and dots.`
- `Each domain label has length at least 1.`
- `Each domain appears at most once.`
- `-10^9 <= score <= 10^9`
- `The sum of all domain string lengths is at most 300000.`

## Solutions

### Suffix-Sum with Pairwise Leaf Check

#### Derivation

The most literal reading assigns the function two duties per domain: decide whether it is a leaf, and if so sum its suffix chain. The first duty is a question about the other inputs: `domain` is a leaf exactly when no other input domain ends with `"." + domain`. The second duty becomes cheap once the entries live in a dictionary, because walking the suffix chain is just repeated dictionary lookups down progressively shorter names:

1. Parse each entry into `domain_score`, mapping the domain string to its
   integer score.
2. For each `domain`, set the `is_leaf` predicate by scanning every other key
   for one that ends with `"." + domain`.
3. Skip the domain when `is_leaf` is false.
4. Walk the suffix chain: strip the labels before the first dot, adding each
   suffix's score from `domain_score` (an absent suffix contributes nothing).
5. Emit `domain=accumulated` for each leaf, then sort the results.

#### Walkthrough

Trace both duties on Example 3, whose five domains include a non-leaf middle node:

```text
domain_score = {api.shop.com: 4, shop.com: -2, com: 1,
                cdn.shop.com: 7, img.cdn.shop.com: 3}

api.shop.com       leaf (nothing ends with ".api.shop.com")
                   chain: 4 + shop.com (-2) + com (1)                      -> 3
shop.com           not a leaf: cdn.shop.com ends with ".shop.com"
com                not a leaf: api.shop.com ends with ".com"
cdn.shop.com       not a leaf: img.cdn.shop.com ends with ".cdn.shop.com"
img.cdn.shop.com   leaf
                   chain: 3 + cdn.shop.com (7) + shop.com (-2) + com (1)   -> 9
```

The two survivors are exactly the domains no other input extends. Sorting their formatted strings yields `["api.shop.com=3", "img.cdn.shop.com=9"]`, matching the expected Output for Example 3.

#### Solution

The code is the two duties written down: the pairwise leaf scan, then the chain walk.

```python
from typing import List


class Solution:
    def solve(self, domain_scores: List[str]) -> List[str]:
        """Return sorted "domain=total" strings for every leaf domain.

        Time:  O(D^2 * L): each of the D domains is leaf-tested against every
            other with an O(L) suffix comparison; parsing and the chain sums
            are linear in the total input length and dominated by the scan.
        Space: O(S) for the parsed score map and the results.
        """
        domain_score: dict[str, int] = {}
        for entry in domain_scores:
            domain, score_text = entry.split(" ")
            domain_score[domain] = int(score_text)

        results: List[str] = []
        for domain, score in domain_score.items():
            is_leaf = all(
                not other.endswith("." + domain)
                for other in domain_score
            )
            if not is_leaf:
                continue
            accumulated = score
            suffix = domain
            while "." in suffix:
                suffix = suffix[suffix.index(".") + 1:]
                accumulated += domain_score.get(suffix, 0)
            results.append(f"{domain}={accumulated}")
        return sorted(results)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(D² × L)`

Each of the `D` domains is tested against `D - 1` others with an `O(L)` `endswith` comparison (`L` the mean domain length); parsing and the per-leaf chain walks add only `O(S)`.

##### Space Complexity: `O(S)`

The parsed `domain_score` map plus the result strings hold at most the total input length.

#### Key Insights

- A string can never end with `"." + itself`, so the pairwise leaf test needs no self-comparison guard even before invoking the uniqueness constraint.
- `domain_score.get(suffix, 0)` makes absent ancestors contribute nothing, which is exactly the statement's "suffix ancestors that appear in the input".
- Negative scores flow through the chain walk unchanged: Example 1's leaf totals are computed with `-5` and `20` in the same sum.

### Suffix-Count Hash Map

#### Derivation

The pairwise scan re-asks "does anything end with this?" once per domain, paying `D` comparisons for a question one pass could answer for everybody. Flipping the direction removes the quadratic: every input domain donates its proper dot-suffixes to a tally, so a domain that is somebody's suffix ancestor shows up in `suffix_counts` at least once. The leaf verdict collapses to a threshold test, `suffix_counts[domain] == 0`, with no pair comparisons at all:

1. Parse `domain_score` as before.
2. For each domain, scan its characters; at every `.`, increment
   `suffix_counts` for the substring after that dot.
3. Skip any domain whose `suffix_counts` entry is nonzero: it is a suffix
   ancestor of some other input domain, so it is not a leaf.
4. Chain-sum each surviving leaf exactly as in the baseline and sort.

#### Walkthrough

Example 1 builds the tally in one pass; each line lists the proper suffixes the domain donates:

```text
com 20                    no dot        (no donations)
domain.com 10             com           suffix_counts[com] = 1
mail.domain.com 5         domain.com, com   counts[domain.com] = 1, counts[com] = 2
test.com 10               com           counts[com] = 3
user.test.com 30          test.com, com     counts[test.com] = 1, counts[com] = 4
contact.user.test.com -5  user.test.com, test.com, com
                                        counts[user.test.com] = 1,
                                        counts[test.com] = 2, counts[com] = 5
```

Only `mail.domain.com` and `contact.user.test.com` end with count zero: everything else was donated by somebody deeper. Their chain walks give `5 + 10 + 20 = 35` and `-5 + 30 + 10 + 20 = 55`, so the sorted output is `["contact.user.test.com=55", "mail.domain.com=35"]`, matching the expected Output for Example 1.

#### Solution

The code replaces the leaf scan with the donation pass; the chain walk is unchanged.

```python
from collections import Counter
from typing import List


class Solution:
    def solve(self, domain_scores: List[str]) -> List[str]:
        """Return sorted "domain=total" strings for every leaf domain.

        Time:  O(S * k): parsing is linear in the total input length S, and
            enumerating proper suffixes slices one string per dot, costing the
            suffix's length each time, O(S * k) where k is the largest label
            count of any single domain; chain sums and the sort are smaller.
        Space: O(S * k) for the tally's suffix strings in the worst case.
        """
        domain_score: dict[str, int] = {}
        for entry in domain_scores:
            domain, score_text = entry.split(" ")
            domain_score[domain] = int(score_text)

        suffix_counts: Counter = Counter()
        for domain in domain_score:
            for dot_position, character in enumerate(domain):
                if character == ".":
                    suffix_counts[domain[dot_position + 1:]] += 1

        results: List[str] = []
        for domain, score in domain_score.items():
            if suffix_counts[domain]:
                continue
            accumulated = score
            suffix = domain
            while "." in suffix:
                suffix = suffix[suffix.index(".") + 1:]
                accumulated += domain_score.get(suffix, 0)
            results.append(f"{domain}={accumulated}")
        return sorted(results)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(S × k)`

Parsing reads the total input length `S` once; enumerating proper suffixes slices one string per dot at the cost of the suffix's own length, which totals `O(S × k)` with `k` the largest label count in one domain; the chain walks and the final sort are within that bound.

##### Space Complexity: `O(S × k)`

The tally stores at most one string per dot occurrence, and the stored suffixes can total `O(S × k)` characters in the worst case.

#### Key Insights

- Donating suffixes once per domain replaces the `D²` pairwise scan with a single enumeration pass; the leaf verdict becomes `suffix_counts[domain] == 0`.
- Slices start after a dot, so a full domain never lands in its own tally: the counts are proper-suffix counts, which is what the leaf definition demands.
- The tally needs only counts, not sets of donors: the question is existence, and a threshold test answers it.

### Reversed-Label Trie with DFS

#### Derivation

Both earlier solutions re-derive each domain's suffix family from its string. A [trie](https://en.wikipedia.org/wiki/Trie) built from the top-level label down stores that family once: inserting a domain label by label in reverse makes the path from `root` to its terminal node spell the domain's suffix-ancestor chain, one label per edge. Two structural facts then finish the problem. A domain is a leaf exactly when its terminal node has no children, because a child would be a deeper input domain extending it. And a leaf's total is the sum of the scores on the path from `root` down to that node, since the path visits the leaf and every suffix ancestor present in the input:

1. Build `root`; for each entry, walk `reversed(domain.split("."))` from
   `root`, creating missing children with `setdefault`, then set the final
   node's `score` and mark it `terminal`.
2. DFS from `root`, carrying `accumulated` (the running path sum) and `name`
   (the domain spelled so far, joined root-down).
3. At a child with `terminal` true and no children, emit
   `child_name = accumulated + child.score` as `f"{child_name}={...}"`.
4. Otherwise recurse deeper; sort the collected results.

#### Walkthrough

Example 2 keeps the trie small enough to draw whole:

```text
insert "com 5"    root -> com(terminal, 5)
insert "a.com 2"  root -> com(terminal, 5) -> a(terminal, 2)
insert "b.com 3"  root -> com(terminal, 5) -> a(terminal, 2)
                                          -> b(terminal, 3)
```

The DFS leaves `root` with `accumulated = 0`. The `com` child raises the sum to `5`, but `com` is terminal with children `a` and `b`, so it is not a leaf and the walk descends instead of emitting. `a` raises the sum to `5 + 2 = 7` and has no children: emit `a.com=7`. `b` raises it to `5 + 3 = 8`: emit `b.com=8`. Sorted, the output is `["a.com=7", "b.com=8"]`, matching the expected Output for Example 2. The `com` node's score participates in both leaf totals yet is never emitted itself, because `com` is nobody's leaf.

#### Solution

The code is the reverse insertion plus the sum-carrying DFS.

```python
from typing import List


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.terminal = False
        self.score = 0


class Solution:
    def solve(self, domain_scores: List[str]) -> List[str]:
        """Return sorted "domain=total" strings for every leaf domain.

        Time:  O(S + L log L): parsing and insertion touch each of the S
            input characters a constant number of times, the DFS visits each
            trie node once, and sorting the L leaf names costs L log L
            comparisons.
        Space: O(S) for the trie (one node per label occurrence) and results.
        """
        root = TrieNode()
        for entry in domain_scores:
            domain, score_text = entry.split(" ")
            node = root
            for label in reversed(domain.split(".")):
                node = node.children.setdefault(label, TrieNode())
            node.score = int(score_text)
            node.terminal = True

        results: List[str] = []

        def dfs(node: TrieNode, accumulated: int, name: str) -> None:
            for next_label, child in node.children.items():
                child_accumulated = accumulated + child.score
                child_name = f"{next_label}.{name}" if name else next_label
                if child.terminal and not child.children:
                    results.append(f"{child_name}={child_accumulated}")
                else:
                    dfs(child, child_accumulated, child_name)

        dfs(root, 0, "")
        return sorted(results)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(S + L log L)`

Splitting and insertion read each input character a constant number of times (`S` the total input length), each label creates at most one node so the DFS is linear in the trie, and sorting the `L` leaf names costs `L log L` comparisons.

##### Space Complexity: `O(S)`

The trie holds one node per label occurrence, bounded by the total input length, plus the result list; the DFS stack depth is the label count of the deepest domain.

#### Key Insights

- Reversing the labels puts the top-level domain at the root, so a root-to-node path is exactly that node's suffix-ancestor chain.
- The leaf test becomes structural: terminal with no children replaces every string comparison of the earlier solutions.
- Scores live on terminal nodes and the DFS carries the running sum downward, so each leaf's total is assembled on the way down; a score is used by every leaf below it but emitted only at a leaf.
- Scores reach `10^9` in magnitude, which is a non-issue in Python: integers do not overflow, so no accumulation strategy needs guarding.

## Comparison of Solutions

### Time Complexity

- **Suffix-Sum with Pairwise Leaf Check**: `O(D² × L)` - each domain is leaf-tested against every other with a linear suffix comparison.
- **Suffix-Count Hash Map**: `O(S × k)` - one suffix enumeration per domain, priced at the suffix lengths.
- **Reversed-Label Trie with DFS**: `O(S + L log L)` - linear insertion and traversal, plus sorting the leaf names.

### Space Complexity

- **Suffix-Sum with Pairwise Leaf Check**: `O(S)` - the parsed score map and results.
- **Suffix-Count Hash Map**: `O(S × k)` - the tally stores every donated suffix string.
- **Reversed-Label Trie with DFS**: `O(S)` - one trie node per label occurrence.

### Trade-offs

- **Suffix-Sum with Pairwise Leaf Check**: the statement translated directly into code, and the easiest to trust; it pays a quadratic leaf scan that nothing else on the page needs.
- **Suffix-Count Hash Map**: removes the pairwise scan with a dictionary and one enumeration pass, but stores every donated suffix string and stays sensitive to deep label counts within a single domain.
- **Reversed-Label Trie with DFS**: linear overall and the leaf test is a node shape, at the cost of building trie machinery and a DFS whose stack tracks the deepest label chain.

### When to Use Each

- **Suffix-Sum with Pairwise Leaf Check**: tiny inputs, or as the spoken baseline that defines "leaf" before optimizing it.
- **Suffix-Count Hash Map**: the pragmatic online-assessment choice: short to write, no custom structures, and comfortably fast for realistic domain depths.
- **Reversed-Label Trie with DFS** (Recommended): when the input is large or adversarially deep, or when the interviewer names a trie: it is the only variant with a linear time bound.

### Optimization Notes

- Sorting once at the end, after collecting formatted strings, keeps the ordering concern out of every solution's inner loops; the required lexicographic order is plain string order.
- `entry.split(" ")` relies on the stated format of exactly one separating space; `rsplit(" ", 1)` is the defensive variant if that guarantee ever weakens.
- The chain walk visits every suffix of a leaf even when an intermediate ancestor is absent from the input; the trie merges those absent intermediates into existing paths instead, which is where its linearity comes from.
- In an online assessment the hash-map variant is usually the fastest to write correctly; reserve the trie for when constraints or the interviewer demand the linear bound.
