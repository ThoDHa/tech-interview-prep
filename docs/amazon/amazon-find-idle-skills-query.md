# [Find Idle Skill Query](https://www.fastprep.io/problems/amazon-find-idle-skills-query)

**Medium** | **NN minutes** | **Hash Table, Binary Search**

The Amazon Alexa development team needs to analyze request logs across numSkills skills.

The skills are identified by the integers from 1 through numSkills. Each entry requestLogs[i] = [skillId, timestamp] records one request to a skill at the given time.

For each value queryTimes[i], consider the inclusive time interval [queryTimes[i] - timeWindow, queryTimes[i]]. A skill is idle, or stale, for that query when it has no request in the interval.

Return an array containing the number of idle skills for every query, in the original query order. If every skill has at least one request in a query's interval, the answer for that query is 0.

## Examples

### Example 1

**Input:** `numSkills = 3`, `requestLogs = [[1, 3], [2, 6], [1, 5]]`, `queryTimes = [10, 11]`, `timeWindow = 5`

**Output:** `[1, 2]`

**Explanation:** For query time 10, the inclusive interval is [5, 10]. Skills 1 and 2 have requests in that interval, so only skill 3 is idle and the answer is 1.

For query time 11, the interval is [6, 11]. Only skill 2 has a request in that interval, so skills 1 and 3 are idle and the answer is 2.

### Example 2

**Input:** `numSkills = 6`, `requestLogs = [[3, 2], [4, 3], [2, 6], [6, 3]]`, `queryTimes = [3, 2, 6]`, `timeWindow = 2`

**Output:** `[3, 5, 5]`

**Explanation:** At query time 3, skills 3, 4, and 6 are active in [1, 3], leaving 3 idle. At query time 2, only skill 3 is active in [0, 2], leaving 5 idle. At query time 6, only skill 2 is active in [4, 6], leaving 5 idle.

### Example 3

**Input:** `numSkills = 6`, `requestLogs = [[3, 2], [4, 3], [2, 6], [6, 3]]`, `queryTimes = [1, 2, 3, 4, 5, 6]`, `timeWindow = 1`

**Output:** `[6, 5, 3, 4, 6, 5]`

**Explanation:** The inclusive windows are [0,1], [1,2], [2,3], [3,4], [4,5], and [5,6]. Their active-skill counts are 0, 1, 3, 2, 0, and 1, so subtracting from 6 gives [6, 5, 3, 4, 6, 5].

## Constraints

- `1 ≤ numSkills ≤ 10^5`
- `1 ≤ requestLogs.length ≤ 10^5`
- `1 ≤ queryTimes.length ≤ 10^5`
- `1 ≤ requestLogs[i][0] ≤ numSkills`
- `1 ≤ requestLogs[i][1] ≤ 10^5`
- `1 ≤ queryTimes[i] ≤ 10^5`
- `1 ≤ timeWindow ≤ 10^5`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
