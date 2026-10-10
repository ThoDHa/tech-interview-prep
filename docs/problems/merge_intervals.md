# [Merge Intervals](https://leetcode.com/problems/merge-intervals/)

**Medium** | **30 minutes** | **Array, Sorting**

**Pattern:** [Interval](../patterns/interval/intuition.md)

**Algorithm:** [Sorting algorithm](https://en.wikipedia.org/wiki/Sorting_algorithm) · [Sweep line algorithm](https://en.wikipedia.org/wiki/Sweep_line_algorithm) · [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search)

**Practice:** [`practice/merge_intervals/solution.py`](../../practice/merge_intervals/solution.py)

Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals and return an array of the non-overlapping intervals that cover all the intervals in the input. Touching intervals such as `[1,4]` and `[4,5]` are considered overlapping. The answer may be returned in any order.

## Examples

### Example 1

**Input:** `intervals = [[1,3],[2,6],[8,10],[15,18]]`

**Output:** `[[1,6],[8,10],[15,18]]`

**Explanation:** Intervals `[1,3]` and `[2,6]` overlap, so they merge into `[1,6]`.

### Example 2

**Input:** `intervals = [[1,4],[4,5]]`

**Output:** `[[1,5]]`

**Explanation:** Intervals `[1,4]` and `[4,5]` touch at `4`, so they merge into `[1,5]`.

## Constraints

- `1 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= start_i <= end_i <= 10^4`

