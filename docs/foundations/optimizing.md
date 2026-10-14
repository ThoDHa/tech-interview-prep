# Optimizing a Working Solution

A working solution is the midpoint of an interview answer, not the end. [How to Approach a Problem](how_to_approach.md) takes you from a blank page to code that passes. This page is about what comes after: proving how fast your solution is *allowed* to be, stripping the wasted work that is left in it, and cutting its memory when the interviewer asks "can we do better?".

None of it requires a clever idea. It is a short checklist: find the floor, remove redundant work, then trade memory.

## Find the floor: the best theoretical complexity

[Big-O](big_o.md) sets the bar your solution must clear: the **Constraints** tell you how big `n` is, and the table there tells you what cost is fast enough. Every problem also sets a floor from the other side: the **best theoretical time complexity** is the cost you provably cannot beat, because any correct answer must at least touch every piece of the input the answer depends on.

- Summing a list is `O(n)`. Until you have read every element, the one you
  skipped could have held any value, so no algorithm can be sure of the sum.
- Deciding whether a list [Contains
  Duplicate](../leetcode/contains_duplicate.md) is `O(n)` for the same reason: a duplicate could hide in the last element you have not looked at.
- Counting [islands](../leetcode/number_of_islands.md) in an `m × n` grid is
  `O(m·n)`: every cell can change the count, so every cell must be visited.

Knowing the floor earns you two things. First, it tells you when to stop: if your approach already meets the floor, hunting for something faster is a waste of the clock. Second, it is a positive interview signal: the sentence "every element must be read at least once, so `O(n)` is the best possible" is exactly what interviewers want to hear.

One warning: **properties change the floor**. On an unsorted array, finding a value costs `O(n)`; on a sorted one, [binary search](../patterns/binary_search/intuition.md) finds it in `O(log n)` ([Search in Rotated Sorted Array](../leetcode/search_in_rotated_sorted_array.md)) and the minimum or maximum is `O(1)`, because it is sitting at an end. Ask what the input's properties guarantee before you accept a floor.

When you are already at the floor, there are exactly two directions left, and interviewers name them: do *less work* (fewer passes over the data) or use *less space*. The rest of this page is those two directions.

## Remove redundant work

Six habits remove work that buys nothing. Each is small; a finished solution usually has one or two of them still hiding in it.

### 1. Terminate early

Return the moment the answer is known, instead of finishing the loop out of momentum:

```python
def contains_duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
```

[Valid Palindrome](../leetcode/valid_palindrome.md) is the same habit: the first mismatched pair settles the answer, so return `False` and stop. In the [Binary Search](../patterns/binary_search/intuition.md) loop, `return mid` is early termination too.

### 2. Hoist invariant work out of loops

Anything the loop recomputes that does not actually change from one iteration to the next does not belong inside it. Compute it once, before the loop starts. In [Find All Anagrams in a String](../leetcode/find_all_anagrams_in_a_string.md), every window position is compared against the letter counts of `p`, but `p` itself never changes with the window:

```python
# rebuilds the counts of p from scratch, at every window position
for left in range(len(s) - len(p) + 1):
    if Counter(s[left:left + len(p)]) == Counter(p):
        matches.append(left)

# the counts of p are identical for every window: build them once
target = Counter(p)
for left in range(len(s) - len(p) + 1):
    if Counter(s[left:left + len(p)]) == target:
        matches.append(left)
```

The [Sliding Window](../patterns/sliding_window/intuition.md) guide shows the step after hoisting: update the window's own counts incrementally as it slides, instead of recounting each window from scratch.

### 3. Cache derived values

If you compute something more than once, keep it. This is [step 4 of the method](how_to_approach.md#4-find-the-wasted-work), "remember something so you do not redo it", applied at the level of a single variable:

```python
# the minimum of everything before day i, recomputed every day
best = 0
for i in range(1, len(prices)):
    best = max(best, prices[i] - min(prices[:i]))

# one variable, updated as you go
min_price = prices[0]
best = 0
for price in prices:
    best = max(best, price - min_price)
    min_price = min(min_price, price)
```

([Best Time to Buy and Sell Stock](../leetcode/best_time_to_buy_and_sell_stock.md): the first version is `O(n²)`, the second `O(n)`.) The pattern-scale versions of this habit are the [Hashing](../patterns/hashing/intuition.md) guide, which remembers what you have seen, and the [Prefix Sum](../patterns/prefix_sum/intuition.md) guide, which remembers running totals.

### 4. Order conditions: cheap first, likely first

`and` and `or` short-circuit left to right, so put the `O(1)` check before the `O(n)` one, and the check that is usually decisive before the one that rarely is:

```python
def is_anagram(s, t):
    if len(s) != len(t):
        return False
    return Counter(s) == Counter(t)
```

([Valid Anagram](../leetcode/valid_anagram.md); the same guard applies to [Ransom Note](../leetcode/ransom_note.md).) The `O(1)` length check settles the common mismatch for free, and the `O(n)` counting runs only when it can succeed.

### 5. Be lazy

Do not do work before you know it is needed. Skip setup for empty inputs, and when the remainder of a job is "everything that is left", take it whole instead of processing it item by item. [Merge Two Sorted Lists](../leetcode/merge_two_sorted_lists.md):

```python
# eager: walk the remaining nodes one at a time, re-pointing each
while current:
    tail.next = current
    tail, current = tail.next, current.next

# lazy: the remainder is already linked: attach it in one move
tail.next = current
```

### 6. Delete redundant conditions

Conditions that can never change the outcome are not safety nets, they are noise, and every extra branch is a place for a future bug to hide. This is all [Invert Binary Tree](../leetcode/invert_binary_tree.md) needs:

```python
def invert_tree(node):
    if not node:
        return None
    node.left, node.right = invert_tree(node.right), invert_tree(node.left)
    return node
```

The tempting extra guard `if not node.left and not node.right: return node` never changes the output: a leaf's children are `None`, and the base case already handles them. When a condition cannot change the result, deleting it is the optimization.

## Cut space

### Overwrite the input, with care

The cheapest extra memory is memory you do not allocate: reuse the input as your workspace. The pattern guides already use this trick in several places:

- [Two Pointers](../patterns/two_pointers/intuition.md): the writer-pointer
  form compacts a list in place, no second array.
- [Backtracking](../patterns/backtracking_exploration/intuition.md): visited
  cells are marked directly in the grid ([Word Search](../leetcode/word_search.md)).
- [Grid DP](../patterns/grid_dp/intuition.md): the `m × n` table collapses
  into one row that is overwritten as you go.
- [Sort Colors](../leetcode/sort_colors.md): three value classes swap into
  position inside the original array.

One caution, and it matters: overwriting the input destroys the caller's data. Interviews accept this (the input is disposable); production code usually does not (callers expect their arguments back unharmed). So say it out loud: "this mutates the input; I'd copy it first outside an interview." Naming the trade is the signal, not avoiding the trick. Whether the input may be modified is worth settling while you [clarify the question](interview_practices.md#2-clarify-the-question).

### Change the data structure

The other way to cut both time and space is to hold the data in a structure where the expensive operation is cheap:

- A [Trie](../patterns/trie/intuition.md) stores shared prefixes once, so
  repeated prefix walks become short descents ([Implement Trie](../leetcode/implement_trie_prefix_tree.md), [Word Break](../leetcode/word_break.md)).
- A [Heap](../patterns/heap/intuition.md) answers "the `k` largest" without
  fully sorting: [K Closest Points to Origin](../leetcode/k_closest_points_to_origin.md) drops from `O(n log n)` to `O(n log k)`.
- A [Hashing](../patterns/hashing/intuition.md) set trades `O(n)` memory for
  `O(1)` lookups ([Two Sum](../leetcode/two_sum.md)), and a set holding the characters seen an odd number of times so far settles [Longest Palindrome](../leetcode/longest_palindrome.md) in a single pass.

## When to stop

You are done when your time meets the best theoretical complexity the problem allows and your extra space is reasonable for the constraints. Beyond the floor there is nothing to reach, and past the constraints there is nothing to prove. Optimizing further is a hobby, not an interview signal: state your complexity, name the trade you would make with more time, and move on.

---

*The best-theoretical-complexity floor, the redundant-work techniques, and the space-optimization techniques are adapted from the Tech Interview Handbook's [Coding Interview Techniques](https://www.techinterviewhandbook.org/coding-interview-techniques/); the Grind75 problem examples and cross-links are this project's own.*
