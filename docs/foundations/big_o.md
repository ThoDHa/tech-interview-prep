# Big-O Notation

Big-O is a way to answer one question: **as the input grows, how does the amount of work grow?** It is not about seconds on your laptop. It is about the *shape* of the growth, because that shape is what decides whether your solution survives a large input or times out.

## The core idea

Imagine an input of size `n` (the length of an array, the number of nodes in a tree). Big-O describes how the number of steps grows as `n` gets bigger. We drop constants and small terms and keep only the dominant growth, because for large `n` that is all that matters.

Two examples make the idea concrete:

- A loop that touches every element once does about `n` steps. We call that
  **O(n)**: the work grows in step with the input.
- A loop nested inside another loop, each over the input, does about `n × n`
  steps. We call that **O(n²)**: double the input, quadruple the work.

The letter `O` means "on the order of", and `n` is the input size. So `O(n)` reads as "on the order of `n` steps".

## The classes you will meet

From best to worst, the ones that appear in this guide:

| Big-O | Name | Plain meaning | Everyday analogy |
|-------|------|---------------|------------------|
| `O(1)` | Constant | Same work no matter the input size | Looking up a word you already memorized |
| `O(log n)` | Logarithmic | Each step throws away half the remaining work | Finding a name in a phone book by halving |
| `O(√n)` | Square root | Work grows with the square root of the input | Testing whether `n` is prime by trying divisors only up to `√n` |
| `O(n)` | Linear | Work grows in step with the input | Reading every page of a book once |
| `O(n log n)` | Linearithmic | About `log n` rounds of linear work: the cost of good sorting algorithms | Sorting a deck of cards efficiently |
| `O(n·m)` | Bilinear | For every item of one input, touch every item of a *second* input | Filling in every cell of an `m × n` grid |
| `O(n²)` | Quadratic | For every item, you touch every item | Comparing every person in a room to every other |
| `O(2ⁿ)` | Exponential | Each new item doubles the work | Trying every yes/no combination of `n` switches |

A quick note on notation: prose math keeps its superscripts (`O(n²)`, `O(2ⁿ)`), while inline code and constraint blocks use the caret forms LeetCode prints (`2^31 - 1`, `2^k`). Text quoted from LeetCode is never altered.

`O(1)` and `O(log n)` are excellent. `O(n)` and `O(n log n)` are the usual targets for a good solution. `O(n²)` is often the brute force you start from. `O(2ⁿ)` is usually only acceptable when `n` is tiny.

The two less common classes have specific shapes. `O(√n)` appears whenever you can stop at the square root: divisors of `n` come in pairs, so checking candidates up to `√n` covers all of them. `O(n·m)` is what a nested loop becomes when the two loops run over *different* inputs rather than the same one: a grid with `m` rows and `n` columns has `m × n` cells, and [Number of Islands](../leetcode/number_of_islands.md) has to touch every one of them.

## Why the halving classes are so fast

`O(log n)` keeps appearing because halving is powerful. Each step of [binary search](../patterns/binary_search/intuition.md) discards half of what is left. Starting from a million items, you reach the answer in about 20 steps, because you can only halve a million about 20 times before nothing is left. That is the difference between `O(n)` (a million steps) and `O(log n)` (twenty).

## When to worry: matching Big-O to the input size

Competitive judges and interviewers care about Big-O because it predicts whether you finish in time. A rough rule of thumb, assuming a budget of roughly one hundred million simple operations:

| If `n` is up to | Then this is usually fast enough |
|-----------------|----------------------------------|
| 1,000,000,000+ | `O(log n)` or `O(1)` |
| 1,000,000 | `O(n)` or `O(n log n)` |
| 10,000 | `O(n²)` |
| 20 | `O(2ⁿ)` |

This is why the **Constraints** section on every problem page matters: it tells you the size of `n`, which tells you what Big-O you must reach. If the constraint says `n` can be 100,000, an `O(n²)` solution doing ten billion steps will be too slow, and you know to look for an `O(n)` or `O(n log n)` approach. For what to do once your solution clears the bar, see [Optimizing a Working Solution](optimizing.md).

## Counting the Big-O of your own code

A practical way to estimate:

- A single loop over the input is `O(n)`.
- A loop nested inside another loop over the same input is `O(n²)`.
- A loop over one input nested inside a loop over a second input is `O(n·m)`,
  where `n` and `m` are the two input sizes.
- Halving the search range each step (or recursing on half) contributes a
  `log n` factor.
- Sorting a collection costs `O(n log n)`.
- A hash map lookup, insert, or membership test is `O(1)` on average.
- Constant work outside of any loop is `O(1)` and gets absorbed.

When several parts run one after another, the largest one wins: an `O(n)` pass followed by an `O(n²)` pass is `O(n²)` overall. The same arithmetic in the other direction matters just as much: two sequential `O(n)` passes are still `O(n)`, not `O(n²)`. Nesting multiplies; sequence adds, and `n + n` does not grow any faster than `n`. Rewriting a nested loop as two full passes is a real optimization.

## Space complexity is the same idea

Everything above measures *time* (steps). **Space complexity** measures *extra memory* the same way. A solution that builds a hash map of every element uses `O(n)` extra space. One that uses a handful of variables uses `O(1)` extra space. The input itself is usually not counted, only the additional memory your approach allocates.

Many problems offer a time-space trade: spend `O(n)` memory to cut time from `O(n²)` down to `O(n)`. [Two Sum](../leetcode/two_sum.md) is the classic example, and the [Hashing guide](../patterns/hashing/intuition.md) is built entirely on that trade.

## The one-sentence summary

Big-O describes how work grows with input size, ignoring constants, so you can predict whether a solution scales before you ever run it.

---

*The `O(√n)` and `O(n·m)` classes and the sequential-passes clarification follow the [Big O Notation cheatsheet](https://neetcode.io/cheatsheets/big-o-notation) on NeetCode; the rest of this page is original to this project.*
