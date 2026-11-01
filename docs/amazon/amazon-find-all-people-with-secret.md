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

## Deriving the Solution

Two statement clauses shape everything: a meeting connects its participants only at its own time, and sharing inside one time is instantaneous regardless of input order. Together they mean the timeline falls apart into independent time groups: process the distinct times in increasing order, and inside a group, ask only who is reachable from the current holders through that group's meetings. Nothing earlier can re-open, nothing later can reach back.

1. **Start literal.** Simulate the definition: for each time in increasing order, sweep that time's meetings repeatedly until a full pass teaches nobody, then move on: see [Timestamp-Swept Simulation](#timestamp-swept-simulation).
2. **Replace the re-sweeping.** The fixpoint loop re-reads unchanged meetings to learn what a graph traversal states directly: the group's participants and edges form a small graph, and one breadth-first sweep from the holders in that graph reaches exactly the new learners: see [Per-Time BFS on Meeting Groups](#per-time-bfs-on-meeting-groups).

## Solutions

### Timestamp-Swept Simulation

#### Derivation

The most literal transcription of the statement keeps a set of holders and replays the timeline. Grouping meetings by time is unavoidable (the input order lies about causality), but inside a time group the simulation can be naive: sweep the group's meetings, teach the counterpart whenever one side holds the secret, and repeat until a full sweep teaches nobody. The repetition is what makes the simulation honest about instant sharing: in a chain of same-time meetings listed backwards, each pass advances the secret one position along the chain until a final pass changes nothing. Once every time has stabilized, the holders are the answer:

1. Seed `holders` with person `0` and `firstPerson`.
2. For each distinct time in increasing order, collect that time's meetings.
3. Sweep the meetings: when exactly one participant holds the secret, add the other and mark the sweep changed.
4. Repeat step 3 until a sweep changes nothing, then advance to the next time.
5. Return the holders in ascending order.

#### Walkthrough

Example 2, `n = 5`, `meetings = [[2,3,1],[1,2,2],[3,4,3]]`, `firstPerson = 1`:

```text
holders {0, 1}
time 1  meetings [(2,3)]      neither holds; sweep clean, no change
time 2  meetings [(1,2)]      1 holds -> 2 learns    holders {0, 1, 2}
time 3  meetings [(3,4)]      neither holds (3 never learned; the time-2
                              meeting does not reactivate the past)

answer [0, 1, 2]
```

The time-1 meeting taught nobody and the time-3 meeting stays dead even though person 3 met person 2 earlier at time 1, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def findAllPeople(self, n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
        holders = {0, firstPerson}
        for time in sorted({t for _, _, t in meetings}):
            edges = [(x, y) for x, y, t in meetings if t == time]
            changed = True
            while changed:
                changed = False
                for x, y in edges:
                    if x in holders and y not in holders:
                        holders.add(y)
                        changed = True
                    elif y in holders and x not in holders:
                        holders.add(x)
                        changed = True
        return sorted(holders)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m^2 + n log n)`

Each sweep reads its group's meetings once, and a group re-sweeps until a full pass changes nothing, so a group of `k` meetings costs `k` per pass times however many passes it takes. The pass count is not a constant: a chain of `k` same-time meetings listed in reverse needs roughly one pass per chain position as the secret walks the chain, plus one final pass that changes nothing, each pass reading all `k` edges. One group holding all `m` meetings as such a chain makes the worst case quadratic: `O(m^2 + n log n)`, with the final sort of holders contributing the `O(n log n)`. Typical inputs scatter meetings across many small groups that stabilize after a pass or two, which behaves linearly per group; that is the typical shape of the input, not the bound.

##### Space Complexity: `O(m + n)`

The holder set and the per-group edge lists.

#### Key Insights

- The fixpoint sweep is the statement's instantaneous-sharing rule made executable: no meeting inside a time group is "too late" until a full pass changes nothing.
- Processing times in increasing order is not an optimization but the semantics: a person who learns the secret at time `t` cannot propagate through meetings at earlier times.
- The per-meeting membership tests are where the cost hides; a chain of same-time meetings listed in reverse order defeats a single pass, which is exactly what the re-sweep repairs and the next approach replaces with a queue.

### Per-Time BFS on Meeting Groups

#### Derivation

The re-sweeping simulation re-reads meetings whose endpoints cannot change to discover what graph search states outright: inside one time group, the participants and their meetings form a graph, and the new learners are exactly the group members reachable from the holders already in the group. So for each time group in increasing order: build that group's adjacency, seed a queue with the group members who already hold the secret, and run one breadth-first sweep; everyone reached joins the holders permanently. Each meeting edge is built once and traversed at most once per direction, and no group is ever revisited because later times cannot affect earlier ones:

1. Put `0` and `firstPerson` into `holders`; group meetings into `by_time`.
2. For each time in increasing order: build `adjacency` over the group's participants.
3. Seed the queue with the group's members that are already in `holders`.
4. Breadth-first: every neighbor not in `holders` joins and enqueues.
5. Return `holders` in ascending order.

#### Walkthrough

Example 1, `n = 6`, `meetings = [[2,3,5],[1,2,5],[4,5,6]]`, `firstPerson = 1`. The input order lists the `(2,3)` link before `(1,2)`, which the grouping erases:

```text
holders {0, 1}
time 5  group edges: 2-3, 1-2      adjacency: 1: [2], 2: [3, 1], 3: [2]
        seed: 1 (holds)            queue [1]
        visit 1  -> 2 learns       holders {0, 1, 2}
        visit 2  -> 3 learns       holders {0, 1, 2, 3}
time 6  group edges: 4-5           seed: nobody holds

answer [0, 1, 2, 3]
```

The single sweep reached 3 through the backwards-listed chain, and the time-6 group seeded nobody, matching the expected Output.

#### Solution

The code is the walkthrough per group: build `adjacency`, seed the queue from `holders`, and let the sweep absorb the group.

```python
from collections import defaultdict, deque
from typing import DefaultDict, List


class Solution:
    def findAllPeople(self, n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
        holders = {0, firstPerson}
        by_time: DefaultDict[int, List[List[int]]] = defaultdict(list)
        for person, other, time in meetings:
            by_time[time].append([person, other])

        for time in sorted(by_time):
            adjacency: DefaultDict[int, List[int]] = defaultdict(list)
            for person, other in by_time[time]:
                adjacency[person].append(other)
                adjacency[other].append(person)

            frontier = deque(member for member in adjacency if member in holders)
            while frontier:
                person = frontier.popleft()
                for neighbor in adjacency[person]:
                    if neighbor not in holders:
                        holders.add(neighbor)
                        frontier.append(neighbor)
        return sorted(holders)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m log m + n log n)`

Grouping sorts the `m` meetings, each edge enters its adjacency twice and is traversed at most twice inside its group, and the final sort of the holder set costs `O(n log n)` in the worst case, when everyone ends up a holder.

##### Space Complexity: `O(m)`

The grouped map and the largest group's adjacency dominate; the queue never exceeds one group's participants.

#### Key Insights

- Building the group's adjacency converts the fixpoint's repeated membership tests into a visited-marked traversal: one sweep reaches the whole instant-sharing chain, in any input order.
- Seeding from `holders` (not from person 0) keeps the invariant honest: a group seeded with nobody is skipped in `O(group)` and stays that way.
- Groups never interact, so the sort is the only super-linear step; everything else is linear in the meeting count.

## Comparison of Solutions

### Time Complexity

- **Timestamp-Swept Simulation**: `O(m^2 + n log n)` - each time group re-sweeps until stable, so a long same-time chain compounds quadratically.
- **Per-Time BFS on Meeting Groups**: `O(m log m + n log n)` - one sort plus one traversal per meeting edge.

### Space Complexity

- **Timestamp-Swept Simulation**: `O(m + n)` - holders plus per-group edge lists.
- **Per-Time BFS on Meeting Groups**: `O(m)` - grouped map, per-group adjacency, holders.

### Trade-offs

- **Timestamp-Swept Simulation**: the statement's own words as code, with no structures beyond a holder set; the price is repeated group sweeps that degrade on dense same-time chains.
- **Per-Time BFS on Meeting Groups**: the queue makes instant-sharing chains cost one edge each, which is what carries the `10^5` bounds; the price is building a throwaway adjacency per group.

### When to Use Each

- **Timestamp-Swept Simulation**: as the derivation baseline, or when the timeline is nearly one meeting per time and the fixpoint never repeats.
- **Per-Time BFS on Meeting Groups (Recommended)**: the answer to give in an interview: it names the two clauses that decompose the problem (time groups, instant sharing) and pays linear work per meeting.

### Optimization Notes

- A union-find variant merges each time group's participants, then rolls back unions of members that did not reach a holder; it shares the `O(m log m)` bound and avoids the per-group adjacency, at the price of a rollback-capable structure.
- The seeded BFS can skip building `adjacency` for groups whose seed set is empty, saving the throwaway map on dead groups; the code above keeps the map unconditional for simplicity.
- The final `sorted(holders)` is a comparison sort; replacing it with one linear sweep over the label range `0..n - 1` would collect the holders in `O(n)` if the last logarithm ever mattered at `n = 10^5`.
