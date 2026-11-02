# [Minimum Completion Time for DAG Dependencies](https://www.fastprep.io/problems/amazon-minimum-dag-completion-time)

**Medium** | **NN minutes** | **Graph, Topological Sort, Dynamic Programming**

Each task has a positive duration. A dependency [before,after] means task after may start only after task before finishes. The dependency graph is acyclic.

Any number of currently available tasks may run in parallel. Return the minimum time needed to finish every task.

## Examples

### Example 1

**Input:** `durations = [3,2,5]`, `dependencies = [[0,2],[1,2]]`

**Output:** `8`

**Explanation:** Tasks 0 and 1 run together; task 2 then finishes at time 8.

### Example 2

**Input:** `durations = [2,4,3,7]`, `dependencies = [[0,1],[0,2]]`

**Output:** `7`

**Explanation:** The independent seven-unit task is the final task to finish.

### Example 3

**Input:** `durations = []`, `dependencies = []`

**Output:** `0`

**Explanation:** No tasks require zero time.

## Constraints

- `0 <= durations.length <= 100000.`
- `1 <= durations[i] <= 10^9.`
- `The dependency graph is a DAG.`

## Deriving the Solution

Because a task may start the instant its last dependency finishes and any number of tasks may run at once, the minimum total time is not a scheduling choice at all: each task's finish time is forced to be its duration on top of the latest finish among its dependencies, and the answer is the largest forced finish. Reading the statement this way turns "minimize" into "propagate", and the only question left is how to propagate in an order that touches each task after its dependencies.

1. **Start literal.** Simulate the statement word by word: in each round, start every task whose dependencies are all finished, record its finish time, and repeat until nothing is left; the answer is the latest finish: correct, but each round rescans every task, `O(n * (n + m))` worst case: see [Round-Based Availability Simulation](#round-based-availability-simulation).
2. **Spot the waste.** A task becomes ready exactly once, yet every round re-tests every unfinished task for readiness, and the rounds themselves just re-discover what the dependency edges already encode: a task is ready when its remaining indegree hits zero.
3. **Fix it with an order.** Maintain each task's indegree, start from the zero-indegree tasks, and process tasks in an order that always defers a task until every predecessor has fixed its finish time: a queue of exactly the ready tasks: see [Topological Longest-Path Dynamic Programming](#topological-longest-path-dynamic-programming).

## Solutions

### Round-Based Availability Simulation

#### Derivation

The statement's most literal reading: time only moves when a running task finishes, so simulate it in rounds. One round is one simultaneous batch:

1. Look at every unfinished task whose dependencies have all finished; those tasks all start now, in parallel.
2. Each such task finishes at the largest finish time among its dependencies (or time zero with none) plus its own duration.
3. Mark the batch finished and repeat with the next batch, until every task has run.
4. The answer is the largest finish time recorded; an empty task list finishes at `0`.

This is the definition written down, so it is also the independent oracle the faster approach is checked against: it shares no mechanism (no queue, no indegree counters, no processing order beyond "ready now") with the topological propagation below.

#### Walkthrough

Example 1 (`durations = [3,2,5]`, `dependencies = [[0,2],[1,2]]`), batch by batch:

```text
batch 1   ready: 0, 1 (no dependencies)     finish: 0 -> 3, 1 -> 2
batch 2   ready: 2 (0 and 1 finished)       start = max(3, 2) = 3   finish: 2 -> 3 + 5 = 8
all done  answer = max(3, 2, 8) = 8
```

The two roots overlap and the join stacks on the later one, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def minimumCompletionTime(self, durations: List[int], dependencies: List[List[int]]) -> int:
        count = len(durations)
        finished = [False] * count
        finish_time = [0] * count
        remaining_dependencies = [
            [before for before, after in dependencies if after == task]
            for task in range(count)
        ]
        for _ in range(count):
            ready = [
                task
                for task in range(count)
                if not finished[task]
                and all(finished[before] for before in remaining_dependencies[task])
            ]
            for task in ready:
                start = max(
                    (finish_time[before] for before in remaining_dependencies[task]),
                    default=0,
                )
                finish_time[task] = start + durations[task]
            for task in ready:
                finished[task] = True
        return max(finish_time, default=0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * (n + m))`

Up to `n` rounds (a chain forces one batch per round), and each round rescans all `n` tasks and their dependency lists for a total edge work of `m` per round.

##### Space Complexity: `O(n + m)`

The per-task dependency lists, finish times, and flags.

#### Key Insights

- Parallelism makes greedy scheduling optimal for free: starting every ready task immediately can never delay anything, so the simulation's outcome is the minimum by definition, not by an argument.
- The rounds are a topological order computed by brute force: each batch is one topological layer, and a chain of length `n` shows the worst case of one layer per round.
- The answer is a max over forced finish times, never a choice between schedules; the only real work is evaluating every task's start late enough.

### Topological Longest-Path Dynamic Programming

#### Derivation

The simulation re-finds ready tasks by scanning; the dependency edges already say when a task becomes ready. A task's finish time is fixed the moment its last predecessor finishes, so process tasks in any order that never runs a task before its predecessors: a topological order. Then one pass fixes every finish time:

1. Build the successor lists and each task's indegree (its number of unprocessed predecessors).
2. Seed a queue with the zero-indegree tasks; their start is time zero.
3. Pop a task, add its own duration to the start it accumulated, and push that finish time into each successor: a successor's start becomes the max over its predecessors' finish times.
4. A task enters the queue exactly when its indegree drops to zero, which is precisely when the last predecessor has fixed the task's start.
5. The answer is the largest finish time over all tasks, `0` for an empty list.

#### Recurrence

Let `finish[v]` be task `v`'s finish time and `pred(v)` its dependency predecessors:

$$ \text{finish}[v] = \text{durations}[v] + \max_{u \in \text{pred}(v)} \text{finish}[u] $$

with the empty maximum read as `0`, so source tasks finish at their own duration. The answer is `max` over all `\text{finish}[v]`.

#### Walkthrough

Example 1 (`durations = [3,2,5]`, `dependencies = [[0,2],[1,2]]`), the queue pass:

```text
indegrees:          0:0   1:0   2:2
queue seed: [0, 1]
pop 0   finish[0] = 0 + 3 = 3    push 3 into 2 (start 3), indegree 2 -> 1
pop 1   finish[1] = 0 + 2 = 2    start 2 = max(start 2, 2) = 3, indegree 1 -> 0, enqueue
pop 2   finish[2] = 3 + 5 = 8
answer = max(3, 2, 8) = 8
```

Matching the expected Output, with each task visited exactly once.

#### Solution

```python
from typing import List
from collections import deque


class Solution:
    def minimumCompletionTime(self, durations: List[int], dependencies: List[List[int]]) -> int:
        count = len(durations)
        graph = [[] for _ in range(count)]
        indegree = [0] * count
        for before, after in dependencies:
            graph[before].append(after)
            indegree[after] += 1

        finish = [0] * count
        queue = deque(task for task in range(count) if indegree[task] == 0)
        while queue:
            task = queue.popleft()
            finish[task] += durations[task]
            for next_task in graph[task]:
                finish[next_task] = max(finish[next_task], finish[task])
                indegree[next_task] -= 1
                if indegree[next_task] == 0:
                    queue.append(next_task)
        return max(finish, default=0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + m)`

Every task enters the queue once and every edge relaxes its successor exactly once.

##### Space Complexity: `O(n + m)`

The successor lists, indegrees, finish times, and queue.

#### Key Insights

- Longest path in a DAG is well-defined precisely because no cycles exist, and Kahn's order visits every task after all its predecessors, which is the only ordering the recurrence needs.
- The finish times double as the start times of successors: propagating `max` is the whole algorithm, and `durations[v]` is added exactly once, when the task is popped.
- Duplicated dependency edges are harmless here: the indegree counts each duplicate, and each duplicate's relaxation is a `max` that changes nothing.
- Durations up to `10^9` and chains up to `10^5` tasks make the total reach `10^14`, which is why the accumulator is a plain integer and never a running clock advanced one tick at a time.

## Comparison of Solutions

### Time Complexity

- **Round-Based Availability Simulation**: `O(n * (n + m))` - every round rescans every task and edge.
- **Topological Longest-Path Dynamic Programming**: `O(n + m)` - one visit per task, one relaxation per edge.

### Space Complexity

- **Round-Based Availability Simulation**: `O(n + m)` - dependency lists, finish times, and flags.
- **Topological Longest-Path Dynamic Programming**: `O(n + m)` - successor lists, indegrees, finish times, and queue.

### Trade-offs

- **Round-Based Availability Simulation**: the statement transcribed directly, and the independent checker for the DP; the rescan-per-round cost rules it out at scale.
- **Topological Longest-Path Dynamic Programming (Recommended)**: the same propagation with the search for ready tasks replaced by an indegree counter, linear in the graph size.

### When to Use Each

- **Round-Based Availability Simulation**: for small inputs, and always as the oracle in tests: if the two ever disagree, the queue version is the one that broke.
- **Topological Longest-Path Dynamic Programming (Recommended)**: the interview answer: it is the standard longest-path-on-a-DAG pattern with the answer read off the maximum finish.

### Optimization Notes

- **Topological Longest-Path Dynamic Programming** is the recommended choice: linear time, and the finish array needs no extra start array because a successor's accumulated value is its start.
- The same recurrence falls out of a memoized DFS over the predecessor edges; the iterative Kahn form avoids recursion depth limits on a `10^5` chain.
- The empty task list is the one input where the answer is not any task's finish: `max(..., default=0)` covers it in one expression.
