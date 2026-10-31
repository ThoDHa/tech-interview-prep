# [Find All People with the Secret](https://www.fastprep.io/problems/amazon-find-all-people-with-secret)

**Hard** | **NN minutes** | **Graph, Breadth First Search, Sorting**

There are n people labeled from 0 to n - 1. At time 0, person 0 shares a secret with firstPerson.

Each row [x, y, time] in meetings describes a meeting between people x and y. If either knows the secret at that time, the other learns it. Sharing is instantaneous: the secret can travel through a chain of meetings at the same time, regardless of their input order.

People retain the secret after learning it, but a meeting connects its participants only at its own time. Return all people who know the secret after every meeting, sorted in ascending order.

## Examples

### Example 1

**Input:** `n = 6`, `meetings = [[2,3,5],[1,2,5],[4,5,6]]`, `firstPerson = 1`

**Output:** `[0,1,2,3]`

**Explanation:** At time 5, person 1 shares through person 2 to person 3, even though the second link is listed first. Neither participant at time 6 knows the secret.

### Example 2

**Input:** `n = 5`, `meetings = [[2,3,1],[1,2,2],[3,4,3]]`, `firstPerson = 1`

**Output:** `[0,1,2]`

**Explanation:** The meeting at time 1 shares no secret. Person 2 learns it at time 2, but that does not reactivate the past meeting with person 3.

### Example 3

**Input:** `n = 4`, `meetings = []`, `firstPerson = 3`

**Output:** `[0,3]`

**Explanation:** Without meetings, only the two initial holders know the secret.

## Constraints

- `For this exercise, assume 2 <= n <= 10^5 and 0 <= meetings.length <= 10^5.`
- `Every meeting is [x,y,time], where 0 <= x,y < n, x != y, and 1 <= time <= 10^9.`
- `1 <= firstPerson < n.`
- `Meetings may be unsorted, repeat the same participants, or share a timestamp.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
