# [Optimal Interval Difference](https://www.fastprep.io/problems/amazon-optimal-interval-difference)

**Medium** | **NN minutes** | **Intervals, Sorting**

AMZ Interval Collection (A group of problems focused on operations involving intervals :) - 



Optimal Interval Difference

Merge Intervals (Intern, NG)

Find Overlapping Times (Intern)

Get Maximum Sum Find Overlapping Times (Full-Time)

Task Scheduler (Full-Time)

Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.



In the Optimal Interval Difference problem, you are given an array of intervals, where each interval is represented as [start[i], end[i]]. Your task is to find the minimum difference between the start and end points of the common overlapping intervals. That is from the set of intervals obtained after merging the overlapping intervals, compute the difference between the start [i-1] and end[i] points for each interval after sorting and return the minimum of those differences. For example, if intervals are (1,5), (7,9) and (2,4), then after merging the intervals we get (1,5) and (7,9). And the minimum difference between them is 7-5=2.



Input Format



The first line of input contains an integer N, denoting the number of intervals. The next N lines contain two space-separated integers each, representing the start and end points of the intervals.



Output Format



Print a single integer representing the minimum difference between the start and end points of the common overlapping intervals.

## Examples

### Example 1

**Input:** `intervals = [[1, 4], [2, 5], [8, 11]]`

**Output:** `3`

**Explanation:** 🦖

## Constraints

- `:)`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
