# The Coding Cheatsheet

One page for the minutes before an online assessment or a live coding round: reminders, not teaching. Every flagship link goes to this repository's problem bank, and the pattern guides behind them stay the source of truth. For the full method this condenses, see [How to Approach a Problem](../foundations/how_to_approach.md).

## The 30-second read-before-you-type checklist

1. **Restate the problem** in your own words: inputs, outputs, and what exactly counts as an answer.
2. **Re-check the constraints**: `n <= 20` says brute force is fine, `n <= 10^5` says it is not. The size picks the complexity, not the other way around.
3. **Clarify the output shape**: indices or values? Count or the items themselves? Any order, or sorted?
4. **Pick the data structure before writing code**: array, hash map, heap, stack, queue, trie. The structure carries the algorithm.
5. **State the complexities out loud** before coding: "this is O(n log n) time, O(n) space" is a check on the plan and a scored communication signal.

## Complexity intuition

| Constraint says | Complexity that usually fits | Reach for |
|-----------------|------------------------------|-----------|
| `n <= 20` | O(2ⁿ) exponential is fine | backtracking, enumerate everything |
| `n <= 10^3` | O(n²) | nested loops, 2-D DP grids |
| `n <= 10^5` | O(n log n) or O(n) | sort, heap, sliding window, hash map |
| `n <= 10^7` | O(n) | one clean pass |
| bigger | O(log n) or O(1) | math, binary search |

The thresholds above are a conservative version of the mapping in [Big-O Notation](../foundations/big_o.md), with the reasoning behind it.

## Pattern flash-cards

| Pattern | Trigger | The move | Flagship | One-line pitfall |
|---------|---------|----------|----------|------------------|
| [Hashing](../patterns/hashing/intuition.md) | unsorted data, "have I seen X?", pairs or counts | walk once, record in a dict or set, look backward instead of rescanning | [Two Sum](../problems/two_sum.md) | query the complement *before* storing x, or the x + x case (two occurrences needed) breaks |
| [Two pointers](../patterns/two_pointers/intuition.md) | sorted sequence, pairs from both ends | move the pointer whose current side provably cannot be part of an answer | [Valid Palindrome](../problems/valid_palindrome.md) | loop on `left < right`, not `<=`, on pair-shaped problems |
| [Sliding window](../patterns/sliding_window/intuition.md) | contiguous subarray or substring, longest/shortest with a property | grow right; while the invariant is broken, shrink from left; update window state in O(1) | [Longest Substring Without Repeating Characters](../problems/longest_substring_without_repeating_characters.md) | keep the last-seen map or counts in sync while shrinking, or the window's promise lies |
| [Prefix sum](../patterns/prefix_sum/intuition.md) | many range-sum queries, products without division | `prefix[right+1] - prefix[left]` answers a range in O(1); two sweeps give before-i and after-i | [Product of Array Except Self](../problems/product_of_array_except_self.md) | do not divide (zeros break it); for subarray-sum counting, seed the map with `{0: 1}` |
| [Binary search on the answer](../patterns/binary_search/intuition.md) | "minimum speed/capacity/k that can finish" | binary search the answer range with a feasibility predicate; the first True is the answer | [Koko Eating Bananas](../problems/koko_eating_bananas.md) | the predicate must be monotonic (if k works, k+1 works), or halving proves nothing |
| [Rotated-array binary search](../patterns/binary_search/intuition.md) | sorted array, then rotated | at any mid one half is sorted; test the target against that half's exact bounds, else take the other half | [Find Minimum in Rotated Sorted Array](../problems/find_minimum_in_rotated_sorted_array.md) | when duplicates make left, mid, and right equal, shrink linearly: worst case O(n) |
| [Monotonic stack](../patterns/monotonic_stack/intuition.md) | nearest greater/smaller element, spans, "how many days until" | keep candidates ordered on a stack; when the new element dominates, pop and resolve them | [Daily Temperatures](../problems/daily_temperatures.md) | store indices, not values; leftovers on the stack have no boundary, so default their answer (0) |
| [Heap / top-K](../patterns/heap/intuition.md) | k largest/smallest/closest, extremes of a stream | keep a size-k heap; the root is the weakest keeper, replace it when something better arrives | [Kth Largest Element In a Stream](../problems/kth_largest_element_in_a_stream.md) | k largest wants a min-heap (root = kth largest); heapq is min-only, negate for max-heap behavior |
| [Merge intervals](../patterns/interval/intuition.md) | intervals to merge, select, or count rooms | sort by start to merge, by end to select greedily, then walk adjacent pairs | [Non-Overlapping Intervals](../problems/non_overlapping_intervals.md) | touching endpoints ([1,2], [2,3]) overlap or not depending on the problem; decide before coding |
| [Graph BFS/DFS](../patterns/graph/intuition.md) | grid or adjacency graph: count regions, minimum steps | DFS for existence and counting, BFS for shortest distance (levels = steps) | [Number of Islands](../problems/number_of_islands.md) | the count is the number of traversal starts; mark visited when pushing, not when popping |
| [Topological sort](../patterns/topological_sort/intuition.md) | "prerequisites", order under dependencies | Kahn's: track in-degrees, repeatedly peel the in-degree-0 nodes | [Course Schedule II](../problems/course_schedule_ii.md) | `[1, 0]` means edge 0 → 1 (prerequisite first); a cycle leaves `len(order) < n` |
| [Union-find](../patterns/union_find/intuition.md) | dynamic "are x and y connected?", components, cycle test | union roots with union by rank and path compression; same root means connected | [Graph Valid Tree](../problems/graph_valid_tree.md) | uniting two nodes that already share a root closes a cycle; a tree is n-1 edges and one component |
| [Trie](../patterns/trie/intuition.md) | many strings, prefix queries, autocomplete | walk character by character down shared paths, mark word ends | [Implement Trie (Prefix Tree)](../problems/implement_trie_prefix_tree.md) | a path existing is not a word existing: search checks `is_end`, not just the node |
| [Backtracking](../patterns/backtracking_exploration/intuition.md) | enumerate all subsets, combinations, permutations | choose, explore, unchoose; restore the state exactly on return | [Subsets II](../problems/subsets_ii.md) | sort first, then skip `nums[i] == nums[i-1]` when `i > start`, or duplicates flood the output |
| [1-D DP](../patterns/dp_1d_linear/intuition.md) | max/min with no adjacent picks, counting ways | `dp[i]` from a fixed lookback (`dp[i-1]`, `dp[i-2]`), then compress to two variables | [House Robber](../problems/house_robber.md) | `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`: dropping the skip branch maxes wrong; set `dp[0]`, `dp[1]` first |
| [2-D DP](../patterns/string_dp/intuition.md) | two sequences compared: edit distance, LCS | fill a grid from diagonal (match/replace), up (delete), left (insert) | [Edit Distance](../problems/edit_distance.md) | `dp[i][j]` is `s[:i]` vs `t[:j]`, so the characters are `s[i-1]`, `t[j-1]`; seed the empty row and column |
| Bit tricks | O(1) space on pairs and parity | XOR: `a ^ a == 0` and `a ^ 0 == a`; fold everything, pairs cancel | [Single Number](../problems/single_number.md) | XOR cancels exact pairs only: "each appears twice but one" is the shape it solves |
| [Linked-list in-place reversal](../patterns/linked_list_in_place_reversal/intuition.md) | reverse a list or a segment with no extra memory | three pointers: save next, flip `curr.next`, step prev and curr forward | [Reverse Linked List](../problems/reverse_linked_list.md) | save `curr.next` before flipping it away, and return `prev`, not `head` |
| [Tree DFS recursion](../patterns/tree/intuition.md) | tree property from subtrees: depth, diameter, balance | recurse on children, combine at the node (postorder thinking) | [Maximum Depth of Binary Tree](../problems/maximum_depth_of_binary_tree.md) | return the single-branch value (`1 + max`); through-node answers also need a global update |

## Warm-up set

One problem per pattern family from the cards above, loosely escalating from warm fingers to full flow: fifteen problems, each carrying its write-up's cold-solve target. Short on time? The five starred rows are the time-boxed core: their targets total 75 minutes; the full set totals 320 minutes.

Rule of thumb: redo each from a blank file, no peeking; if a solve takes more than 2x its target, re-read that flash-card before moving on.

| Problem | Pattern it drills | Target | The check |
|---------|-------------------|--------|-----------|
| [Single Number](../problems/single_number.md) ★ | Bit tricks | 15 min | Did you fold everything with XOR and let the pairs cancel? |
| [Maximum Depth of Binary Tree](../problems/maximum_depth_of_binary_tree.md) ★ | Tree DFS recursion | 15 min | Did you return `1 + max` over the children? |
| [Two Sum](../problems/two_sum.md) ★ | Hashing | 15 min | Did you query the complement *before* storing `x`? |
| [Valid Palindrome](../problems/valid_palindrome.md) ★ | Two pointers | 15 min | Did you loop on `left < right`, not `<=`? |
| [Kth Largest Element In a Stream](../problems/kth_largest_element_in_a_stream.md) ★ | Heap / top-K | 15 min | Did you keep a size-k min-heap whose root is the answer? |
| [Valid Parentheses](../problems/valid_parentheses.md) | Stack | 20 min | Did you pop-match every closer and require an empty stack at the end? |
| [Reverse Linked List](../problems/reverse_linked_list.md) | Linked-list in-place reversal | 20 min | Did you save `curr.next` before flipping it away? |
| [Find Minimum In Rotated Sorted Array](../problems/find_minimum_in_rotated_sorted_array.md) | Rotated-array binary search | 25 min | Did you identify the sorted half before discarding the other? |
| [Number of Islands](../problems/number_of_islands.md) | Graph BFS/DFS | 25 min | Did you count traversal starts, marking visited when pushing? |
| [Course Schedule II](../problems/course_schedule_ii.md) | Topological sort | 25 min | Did you orient every edge prerequisite-first (`[1, 0]` means `0 → 1`)? |
| [Graph Valid Tree](../problems/graph_valid_tree.md) | Union-find | 25 min | Did you check both n-1 edges and one component? |
| [Subsets II](../problems/subsets_ii.md) | Backtracking | 25 min | Did you sort first, then skip `nums[i] == nums[i-1]` when `i > start`? |
| [House Robber](../problems/house_robber.md) | 1-D DP | 25 min | Did you keep the skip branch (`max(dp[i-1], dp[i-2] + nums[i])`)? |
| [Edit Distance](../problems/edit_distance.md) | 2-D DP | 25 min | Did you seed the empty row and column before filling the grid? |
| [Merge Intervals](../problems/merge_intervals.md) | Merge intervals | 30 min | Did you sort by start and merge each interval into the last output one? |

## The corner-case shotgun

Run every finished solution past this list, out loud, before announcing you are done:

- **Empty input**: empty array, string, or tree. Does returning empty, 0, or None fall out without a crash?
- **Single element**: loops, windows, and pointer pairs must survive `n = 1`.
- **All elements equal**: dedup logic, strict versus non-strict comparisons, window invariants.
- **All negative**: running sums and max products, sliding-window monotonicity assumptions.
- **Zeros**: division and product tricks break on zeros, and a target sum of 0 collides with the empty prefix.
- **Duplicates**: does the hash map overwrite when it should count? Do pointer skips skip too much?
- **Overflow risk**: sums of large values. Python ints are safe; in fixed-width languages prefix sums overflow even when elements fit.
- **Deep recursion**: Python's default ~1000 recursion limit kills an otherwise-correct DFS on chain-shaped inputs, and LeetCode raises it while many OA sandboxes do not.
- **Sorted versus unsorted**: two pointers and binary search are void on unsorted input unless you sort first.
- **Whitespace and unicode in strings**: `"a"` versus `"A"`, spaces, accents. Normalize deliberately or not at all.

## Python quick-refs

The [session language](language.md) toolkit, one line each:

```python
from collections import Counter, defaultdict, deque
import heapq, bisect

Counter(s)                        # frequency map in one call; .most_common(k) for top-k
d = defaultdict(list)             # no KeyError on first touch of a key
d.get(key, 0)                     # read with a default, no membership branch
heapq.nlargest(k, nums)           # and heapq.nsmallest; k largest = min-heap of size k
heapq.heappush(h, -x)             # heapq is min-only: negate on push and pop for a max-heap
bisect.bisect_left(a, x)          # first index with a[i] >= x; bisect.insort keeps it sorted
for i, x in enumerate(nums): ...  # index and value in one walk
for a, b in zip(xs, ys): ...      # parallel walks, stops at the shorter
sorted(items, key=lambda p: (p[0], -p[1]))  # tuples compare lexicographically: multi-key sorts
q = deque(); q.popleft()          # O(1) queue for BFS; list.pop(0) is O(n), never use it
-7 // 2 == -4                     # floor division rounds toward negative infinity
-7 % 2 == 1                       # the result takes the divisor's sign; plan for negatives
parts.append(chunk); "".join(parts)  # build strings as a list, join once at the end
```

### Initialization one-liners

Build the container before the loop, one line each:

```python
from collections import Counter, defaultdict, deque
import heapq

# demo inputs so every line below runs as-is
s, xs, lines = "mississippi", [1, 2, 2, 3], ["abc", "de"]
n, rows, cols, k, x = 3, 2, 3, 2, 0
f, key, default, chunk = abs, "a", 0, "ab"

# 1-D: n slots of one immutable fill
[0] * n; [x] * n
# built elementwise
[f(i) for i in range(n)]
# THE 2-D ARRAY: a fresh row per _, so rows stay independent
[[0] * cols for _ in range(rows)]
# THE TRAP: one row shared rows times; writing any cell rewrites every row
[[0] * cols] * rows
# 3-D: nest one level deeper per dimension
[[[0] * k for _ in range(cols)] for _ in range(rows)]

# empty dict; dict() is the same thing
d = {}
# read with a fallback, no membership branch
d.get(key, default)
# fetch-or-create and mutate in one call
d.setdefault(key, []).append(x)
# counter that works from the very first touch
defaultdict(int)
# graph[u].append(v) builds the adjacency list
graph = defaultdict(list)
# per-key membership, per-key O(1) queue
defaultdict(set); defaultdict(deque)
# frequency map in one call, ranked top k
Counter(s); Counter("mississippi").most_common(k)

# empty set and literal set; {} alone is a dict
set(); {1, 2, 3}
# dedupe; frozenset when the set itself must hash
set(xs); frozenset(xs)

# min-heap on a plain list; heapify(xs) converts in place; negate for a max-heap
heap = []; heapq.heappush(heap, x)
# O(1) queue; maxlen=k caps it: a full deque evicts from the far end
deque(); deque(xs)

# append chunks, "".join(parts) once
parts = []; parts.append(chunk); "".join(parts)

# the comma makes the tuple
(); (x,)
# grid of characters; [line.split() for line in lines] for token rows
[list(line) for line in lines]
```

## The stuck protocol

1. **Say the brute force out loud**, with its complexity. It is a floor, not a failure, and often where the interviewer starts steering.
2. **Solve a smaller case by hand** (`n = 3`). Write down exactly what you track at each step; your hand is usually the algorithm in disguise.
3. **Look for the invariant**: is the data sorted or sortable? Is the answer bounded (a speed, a capacity) with a monotonic test? Those are the sorting, two-pointer, and binary-search-on-answer openings.
4. **Name the structure you need**: "give me the max quickly" is a heap, "have I seen this?" is a hash map, "nearest greater element" is a monotonic stack. Naming it is half the solution.
5. **Keep narrating** while you weigh two candidate approaches. Silence reads as being stuck; talking reads as working.

---

*This page condenses this repository's own material: each flagship link goes to the problem bank, and the linked [pattern guides](../patterns/index.md) carry the full derivations. Original to this project.*
