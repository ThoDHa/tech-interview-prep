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

### Enumerate Every Contiguous Split

#### Derivation

An allocation is fully described by where the `students - 1` dividers sit among the `n - 1` gaps between books. The baseline enumerates every divider placement recursively: extend the current student's run one book at a time, recurse for the remaining students, and track the largest load in each complete split:

1. If `students > len(pages)`, no nonempty split exists; return `-1`.
2. Recurse over divider positions, carrying the running maximum load.
3. Return the smallest maximum seen.

#### Walkthrough

Example 1, `pages = [12,34,67,90]`, `students = 2`, tries divider positions after book 1, 2, and 3: splits `[12],[34,67,90]` with maximum 191, `[12,34],[67,90]` with maximum 157, and `[12,34,67],[90]` with maximum 113. The smallest maximum is `113`, matching the expected output. Example 3, two books and three students, fails the nonempty-split guard immediately with `-1`.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, pages: List[int], students: int) -> int:
        """Return the minimum possible maximum load over contiguous splits.

        Time:  O(C(n - 1, students - 1) * n): every divider placement.
        Space: O(students) recursion depth.
        """
        if students > len(pages):
            return -1
        book_count = len(pages)

        def explore(start: int, remaining: int, load: int, best: List[int]) -> None:
            if remaining == 1:
                best[0] = min(best[0], max(load, sum(pages[start:])))
                return
            running = 0
            for divider in range(start, book_count - remaining + 1):
                running += pages[divider]
                explore(divider + 1, remaining - 1, max(load, running), best)

        best = [float("inf")]
        explore(0, students, 0, best)
        return int(best[0])
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(C(n - 1, students - 1) * n)`

The divider placements grow combinatorially; only toy inputs run this rung.

##### Space Complexity: `O(students)`

The recursion depth tracks the remaining students.

#### Key Insights

- The `-1` guard is structural: nonempty contiguous groups need at least one book per student.
- The enumeration is the definition, which makes it the oracle for the binary-search rung.

### Binary Search on the Maximum Load

#### Derivation

The feasibility question "can the books be split so no student reads more than `limit` pages?" is monotone: any load ceiling that works also works when raised. That monotonicity invites binary search over the answer. Feasibility itself is greedy: sweep books left to right, keep handing the current student books until adding one more would exceed `limit`, then start the next student. The greedy never wastes capacity, so the student count it produces is the minimum needed for that ceiling:

1. Search between `lo = max(pages)` (each book must fit one student) and `hi = sum(pages)` (one student takes all).
2. For a candidate ceiling, count the greedy student requirement.
3. The count is at most `students` exactly when the ceiling is feasible; shrink the window until it closes.

#### Walkthrough

Example 1, `pages = [12,34,67,90]`, `students = 2`: the search window opens at `[90, 203]`. Ceiling 146: the greedy gives student 1 books `12, 34, 67` (adding 90 exceeds 146), student 2 gets `90`: two students, feasible. Ceiling 112: the greedy needs three students because `12 + 34 + 67 = 113 > 112` already forces a split before book 3 lands, infeasible. Ceiling 113: `12 + 34 + 67 = 113` fits, then `90`: feasible, and the window closes at `113`, the expected output.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, pages: List[int], students: int) -> int:
        """Return the minimum possible maximum load over contiguous splits.

        Time:  O(n * log(sum(pages))): log-sum binary search rounds, each
            one greedy linear scan.
        Space: O(1) beyond the input.
        """

        def students_needed(limit: int) -> int:
            count = 1
            running = 0
            for book in pages:
                if running + book > limit:
                    count += 1
                    running = book
                else:
                    running += book
            return count

        if students > len(pages):
            return -1
        low, high = max(pages), sum(pages)
        while low < high:
            middle = (low + high) // 2
            if students_needed(middle) <= students:
                high = middle
            else:
                low = middle + 1
        return low
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * log(sum(pages)))`

Roughly `log2(10^5 * 10^6)` greedy scans, each linear.

##### Space Complexity: `O(1)`

The scan keeps two counters.

#### Key Insights

- Monotone feasibility turns an optimization over exponentially many splits into a search over load ceilings.
- The greedy is optimal per ceiling because postponing a split can only increase later loads.
- `max(pages)` as the lower bound encodes "one book cannot be split"; it also guarantees the greedy never stalls on an oversized single book.

## Comparison of Solutions

### Time Complexity

- **Enumerate Every Contiguous Split**: `O(C(n - 1, students - 1) * n)` - toy scale.
- **Binary Search on the Maximum Load**: `O(n * log(sum(pages)))` - the production rung at `n <= 100000`.

### Space Complexity

- **Enumerate Every Contiguous Split**: `O(students)`.
- **Binary Search on the Maximum Load**: `O(1)`.

### Trade-offs

- The enumeration states the definition outright; the search needs the monotonicity argument to be trusted.
- The binary search answers "best ceiling", and the greedy split realizing it is recovered in the same scan.

### When to Use Each

- **Enumerate Every Contiguous Split**: cross-checking the search on small random inputs.
- **Binary Search on the Maximum Load**: at the stated constraints.

### Optimization Notes

- A dynamic-programming rung `O(n^2 * students)` sits between the two and also answers exact split positions, but it cannot run at `n = 100000`.
- The greedy scan can early-exit once the student count exceeds the budget.
