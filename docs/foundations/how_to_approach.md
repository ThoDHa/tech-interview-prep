# How to Approach a Problem

The hardest moment is the blank page: you have read the problem and have no idea where to start. This guide replaces that panic with a repeatable method. None of these steps require cleverness. They are a checklist you run every time, and the clever idea usually appears somewhere in the middle of running it.

## The method

### 1. Understand the problem exactly

Restate it in your own words. Identify the input (its type and size from the **Constraints**), the output, and any rules. Vague understanding is the most common cause of wrong solutions, so do not skip this. In an interview this step is a dialogue, not solo reading: paraphrase the problem back and ask your questions before you assume. [The Coding Interview, Phase by Phase](interview_practices.md) runs every step of this method as that conversation.

### 2. Walk through the examples by hand

Take the provided examples and solve them yourself on paper, slowly. Notice *how* you arrived at the answer. Your own manual process is very often the algorithm in disguise. If the examples do not cover a corner case (empty input, a single element, all-equal values), invent one and solve it too.

Draw what you are tracking while you do this. For trees, grids, linked lists, and graphs, a picture of the state after each step replaces paragraphs of confused reasoning: pointers you can see are easier to update than pointers you are holding in your head. Even for plain array problems, drawing the input mid-algorithm exposes structure that staring at the statement hides.

### 3. Write the brute force first

Find the most obvious, direct solution, even if it is slow. Try every pair, try every path, simulate the process literally. This matters for three reasons: it proves you understand the problem, it gives you a correct answer to check faster solutions against, and it often reveals the wasted work that the fast solution will eliminate. On every problem page in this guide, the first solution listed is deliberately the most direct baseline for exactly this reason: usually a brute force, sometimes named more specifically (Linear Scan, Simulation, Stack). Either way, it is always worth reading first.

You do not need the whole solution in your head to start writing. Write the skeleton first: the few high-level steps, each translated into a call to a helper function that does not exist yet. For [Number of Islands](../leetcode/number_of_islands.md), the skeleton is "for each land cell not yet visited, count one island and flood-fill from it", with `flood_fill(grid, row, col)` as a placeholder. Then fill the helpers in one at a time. Each helper is a smaller problem than the whole, and a half-filled skeleton is still a working plan.

### 4. Find the wasted work

Look at the brute force and ask: what is it recomputing? What does it look at more than once? The optimization is almost always "remember something so you do not redo it". A repeated search becomes a hash-map lookup. A recomputed subproblem becomes a memoized value. A repeated range-sum becomes a prefix sum.

### 5. Recognize the pattern

Most interview problems are one of a small number of patterns wearing a costume. The signals below point you to the right [pattern guide](../patterns/index.md), where the mental model is fully developed.

### 6. Check complexity against the constraints

Before coding, confirm your planned approach is fast enough. Look at the size of `n` in the **Constraints** and compare it to your approach's [Big-O](big_o.md). If `n` is 100,000 and your idea is `O(n²)`, stop and find a better one now, not after writing it. Once your idea clears the bar, [Optimizing a Working Solution](optimizing.md) is the checklist for pushing it further: the complexity floor, the redundant-work habits, and the space trades.

### 7. Code it, then test the edges

Write the solution, then run it against the examples and the corner cases from step 2. The places solutions break are almost always the boundaries: empty input, one element, the first or last position, duplicates, and the largest allowed value. In an interview, run these checks out loud and before announcing you are done: [the verify-and-test phase](interview_practices.md#5-verify-and-test) is this step performed visibly.

## Pattern recognition signals

When you see these clues in a problem, think of the matching pattern:

| Clue in the problem | Likely pattern |
|---------------------|----------------|
| "Have I seen this?", pairs that sum to a target, counting occurrences | [Hashing](../patterns/hashing/intuition.md) |
| Sorted input, "find the position", repeatedly halving | [Binary Search](../patterns/binary_search/intuition.md) |
| Longest or shortest contiguous run that satisfies a condition | [Sliding Window](../patterns/sliding_window/intuition.md) |
| Sorted array, pair or triplet from both ends | [Two Pointers](../patterns/two_pointers/intuition.md) |
| Many range-sum or "product of all except self" queries | [Prefix Sum](../patterns/prefix_sum/intuition.md) |
| Nesting, matching brackets, "most recent first", undo | [Stack](../patterns/stack/intuition.md) |
| Hierarchy, parent and child, "for each node" | [Tree](../patterns/tree/intuition.md) |
| Connectivity, islands, "reachable from", shortest steps on a grid | [Graph](../patterns/graph/intuition.md) |
| Ordering tasks with dependencies, prerequisites | [Topological Sort](../patterns/topological_sort/intuition.md) |
| "Generate all combinations / permutations / subsets" | [Backtracking](../patterns/backtracking_exploration/intuition.md) |
| "Number of ways", "minimum cost", overlapping subproblems | [Dynamic Programming](../patterns/dp_1d_linear/intuition.md) |
| "The k largest / smallest", a running median, merging sorted streams | [Heap](../patterns/heap/intuition.md) |
| Overlapping ranges, merging or inserting them | [Intervals](../patterns/interval/intuition.md) |
| Taking the best local choice, scheduling and covering | [Greedy](../patterns/greedy_core/intuition.md) |
| Next greater or smaller element, spans and ranges | [Monotonic Stack](../patterns/monotonic_stack/intuition.md) |
| Cycle detection, finding the middle, reversing a chain | [Linked List](../patterns/linked_list_in_place_reversal/intuition.md) |
| A dictionary of words, prefix queries | [Trie](../patterns/trie/intuition.md) |
| Grouping items as connections appear, connected components | [Union-Find](../patterns/union_find/intuition.md) |

## When you are stuck

Being stuck is part of the process, not a failure. A few reliable unsticking moves:

- Solve a smaller version of the problem first, then ask what changes as it
  grows.
- Sort the input and see whether order makes the structure obvious.
- Draw it. Set up the smallest example you can, step it by hand, and write
  down exactly what you are tracking after every step.
- Ask what you would store in a hash map to avoid a repeated search.
- Look at your brute force again and attack the single most wasteful line.

The goal of practice is not to memorize 75 solutions. It is to make these steps automatic, so that an unfamiliar problem becomes a familiar process.

---

*The draw-it-out and skeleton-decomposition moves are adapted from the Tech Interview Handbook's [Coding Interview Techniques](https://www.techinterviewhandbook.org/coding-interview-techniques/); the rest of the method is original to this project.*
