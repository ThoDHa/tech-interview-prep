# [Allocate Minimum Pages](https://www.fastprep.io/problems/amazon-allocate-minimum-pages)

**Hard** | **NN minutes** | **Array, Binary Search, Greedy**

You are given an array pages, where pages[i] is the number of pages in the i-th book, and an integer students.

Allocate every book to exactly one student so that:

Each student receives at least one book.Each student receives one contiguous group of books.The original book order is preserved.Return the minimum possible value of the maximum pages assigned to any student. Return -1 when there are more students than books.

## Examples

### Example 1

**Input:** `pages = [12,34,67,90]`, `students = 2`

**Output:** `113`

**Explanation:** Allocate [12,34,67] and [90]. The larger load is 113, and no valid split has a smaller maximum.

### Example 2

**Input:** `pages = [10,20,30,40]`, `students = 2`

**Output:** `60`

**Explanation:** The optimal groups are [10,20,30] and [40].

### Example 3

**Input:** `pages = [10,20]`, `students = 3`

**Output:** `-1`

**Explanation:** Three nonempty contiguous groups cannot be formed from two books.

## Constraints

- `1 <= pages.length <= 100000.`
- `1 <= pages[i] <= 10^6.`
- `1 <= students <= 100000.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
