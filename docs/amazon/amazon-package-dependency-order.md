# [Package Dependency Order](https://www.fastprep.io/problems/amazon-package-dependency-order)

**Medium** | **NN minutes** | **Graph, Depth First Search, Topological Sort**

You are given package dependency pairs and a target package. Each pair [package, dependency] means the package depends on that dependency.

Return an order in which to install the target package and all of its transitive dependencies so that every dependency appears before the package that needs it.

If there is a cyclic dependency among packages needed by the target package, return an empty array.

The source noted that multiple valid orders may exist. FastPrep uses this deterministic rule: process dependencies in the order they appear in the input pairs.

## Examples

### Example 1

**Input:** `dependencies = [["A","B"],["A","C"],["B","D"],["B","E"],["B","F"],["C","F"],["F","G"],["H","I"],["H","J"],["J","G"]]`, `target = "A"`

**Output:** `["D","E","G","F","B","C","A"]`

**Explanation:** The order installs D, E, and F before B; installs G before F; installs F before C; and installs both B and C before A.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-package-dependency-order; fill them in. -->

## Solutions

### Repeated Readiness Scan

#### Derivation

The most literal reading of "install every dependency before the package that needs it" replays the sentence: figure out which packages the target pulls in, then repeatedly sweep those packages, installing any whose dependencies are all already installed. A full sweep that installs nothing means the remaining packages wait on each other, which is the cycle report. The sweep order is the discovery order, and on this problem's example it reproduces the deterministic rule the source describes:

1. Parse `dependency_map` from the pairs, mapping each package to its
   dependencies in input order.
2. Collect `needed` by walking from `target` over `dependency_map` with a
   queue, so unrelated packages never enter the order.
3. Sweep `needed` in discovery order while `order` is shorter than `needed`:
   install every package whose dependencies are all in `installed`, appending
   to `order`.
4. Return `[]` when a sweep places nothing; otherwise return `order`.

#### Walkthrough

Example 1 has ten pairs but only seven packages the target `A` actually needs: discovery from `A` reaches `B`, `C`, `D`, `E`, `F`, `G` and never touches the `H, I, J` cluster. Four sweeps finish the job:

```text
needed (discovery order): A, B, C, D, E, F, G

pass 1   A needs B, C (none installed)    skip
         B needs D, E, F                  skip
         C needs F                        skip
         D needs nothing                  install   order [D]
         E needs nothing                  install   order [D, E]
         F needs G (not installed)        skip
         G needs nothing                  install   order [D, E, G]

pass 2   A, B, C                          skip (their needs are uninstalled)
         F needs G, now installed         install   order [D, E, G, F]

pass 3   A                                skip
         B needs D, E, F, all installed   install   order [D, E, G, F, B]
         C needs F, installed             install   order [D, E, G, F, B, C]

pass 4   A needs B, C, both installed     install   order [D, E, G, F, B, C, A]
```

Every dependency precedes its dependent, and the result matches the expected Output for Example 1. On a cycle such as `X -> Y -> X`, neither package ever finds its needs installed, a sweep places nothing, and the function returns `[]`.

#### Solution

The code is the discovery walk followed by the sweeping loop.

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, dependencies: List[List[str]], target: str) -> List[str]:
        """Return an install order for target and its transitive
        dependencies, [] on a cycle.

        Time:  O(V * (V + E)): at most V sweeps, each scanning every needed
            package and its dependency list once.
        Space: O(V + E) for the dependency map, the needed list, and the
            installed set.
        """
        dependency_map: dict[str, List[str]] = {}
        for package, dependency in dependencies:
            dependency_map.setdefault(package, []).append(dependency)

        needed: List[str] = []
        seen = {target}
        frontier = deque([target])
        while frontier:
            package = frontier.popleft()
            needed.append(package)
            for next_dependency in dependency_map.get(package, []):
                if next_dependency not in seen:
                    seen.add(next_dependency)
                    frontier.append(next_dependency)

        installed: set[str] = set()
        order: List[str] = []
        while len(order) < len(needed):
            placed_this_pass = False
            for package in needed:
                if package in installed:
                    continue
                if all(
                    next_dependency in installed
                    for next_dependency in dependency_map.get(package, [])
                ):
                    installed.add(package)
                    order.append(package)
                    placed_this_pass = True
            if not placed_this_pass:
                return []
        return order
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V × (V + E))`

Each sweep appends at least one package or aborts, so there are at most `V` sweeps; a sweep visits every needed package and re-reads its dependency edges until the placements run out, `O(V + E)` work per sweep.

##### Space Complexity: `O(V + E)`

`dependency_map` stores every pair, and `needed`, `seen`, and `installed` hold one entry per needed package.

#### Key Insights

- Discovery from the target does double duty: it bounds the work to packages the target needs and keeps the unrelated `H, I, J` cluster out of the answer.
- A full sweep with no placement is a cycle proof: every unplaced package waits on another unplaced package.
- Any fixed sweep order yields a valid install order; this one additionally matches the example's expected sequence because it installs packages in discovery order within each pass.

### DFS Postorder from the Target

#### Derivation

The readiness scan forgets which packages it already checked and re-asks every question every pass. The recursion it should remember is the dependency chain itself: a package may be installed the moment all of its dependencies have been installed, which is exactly what a [depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) postorder computes. Visit the package's dependencies first, in input-pair order, and append the package only after the visits return; the deterministic tie rule "process dependencies in the order they appear in the input pairs" is then not an extra rule but the natural iteration order of the loop:

1. Build `dependency_map` as before.
2. Track three `state` values per package: unset (untouched), `VISITING`
   (on the current dependency path), `VISITED` (emitted or cleared).
3. `visit(target)`: a `VISITING` dependency reports a cycle; a `VISITED` one
   returns immediately; otherwise mark `VISITING`, `visit` each dependency in
   `dependency_map` order, then mark `VISITED` and append to `order`.
4. Return `order` when the root visit succeeds, else `[]`.

#### Invariant

The `state` map partitions all packages into untouched, on the current path (`VISITING`), and finished (`VISITED`), and the append step preserves one ordering property:

```text
a package enters `order` only after every dependency reachable from it
has entered `order` (postorder), and `VISITING` marks exactly the
packages on the current root-to-leaf dependency path
```

The per-branch argument: visiting an unset package marks it `VISITING` before descending, so every edge on the active path points at a `VISITING` package; a `VISITED` dependency is already ordered and needs no work; and a `VISITING` dependency is an ancestor of the current call, meaning the path from it back down to here is a cycle, which is when the function reports failure. At the root call's exit, every package reachable from `target` was marked `VISITED` after its dependencies were appended, so `order` is a valid install order, and its length failing to cover `needed` never happens because a cycle returns `[]` from inside.

#### Walkthrough

Trace the recursion on Example 1. Each line is one call or one emission; indentation is call depth, and each package's dependencies are visited in the pair order they were parsed:

```text
visit A        state A = VISITING
  visit B      state B = VISITING
    visit D    no dependencies   state D = VISITED   emit D
    visit E    no dependencies   state E = VISITED   emit E
    visit F    state F = VISITING
      visit G  no dependencies   state G = VISITED   emit G
               F done            state F = VISITED   emit F
               B done            state B = VISITED   emit B
  visit C      state C = VISITING
    visit F    already VISITED -> return immediately
               C done            state C = VISITED   emit C
               A done            state A = VISITED   emit A
```

The emitted sequence `[D, E, G, F, B, C, A]` matches the expected Output for Example 1, and the `H, I, J` cluster is never visited because no dependency path from `A` reaches it. The second visit to `F` (from `C`) is the memoization beat: `F` is `VISITED`, so its subtree is not re-explored.

#### Solution

The code is the three-state visit from the walkthrough.

```python
from typing import List


class Solution:
    def solve(self, dependencies: List[List[str]], target: str) -> List[str]:
        """Return an install order for target and its transitive
        dependencies, [] on a cycle.

        Time:  O(V + E): each package reachable from the target is visited
            once and each dependency edge is relaxed at most twice (once per
            endpoint visit).
        Space: O(V + E) for the dependency map and state, plus O(V) recursion
            depth on a chain.
        """
        dependency_map: dict[str, List[str]] = {}
        for package, dependency in dependencies:
            dependency_map.setdefault(package, []).append(dependency)

        VISITING = 1
        VISITED = 2
        state: dict[str, int] = {}
        order: List[str] = []

        def visit(package: str) -> bool:
            status = state.get(package, 0)
            if status == VISITING:
                return False
            if status == VISITED:
                return True
            state[package] = VISITING
            for next_dependency in dependency_map.get(package, []):
                if not visit(next_dependency):
                    return False
            state[package] = VISITED
            order.append(package)
            return True

        return order if visit(target) else []
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V + E)`

Each package reachable from `target` transitions through the three states once, and each edge is examined during its source package's single visit; the `VISITED` short-circuit is what keeps repeat edges cheap.

##### Space Complexity: `O(V + E)`

`dependency_map` holds every pair, `state` one entry per touched package, and the recursion stack grows to the longest dependency chain, `O(V)`.

#### Key Insights

- Postorder is the "dependencies first" rule made mechanical: children (dependencies) are appended before the parent (dependent).
- The `VISITING` state is the whole cycle detector: meeting a package already on the current path means the graph needs the package to install itself.
- Iterating dependencies in parsed order makes the code's behavior literally the stated tie rule, which no queue-based reorder can claim by construction.
- The `VISITED` short-circuit is also the shared-subtree optimization: `F` is explored once even though both `B` and `C` depend on it.

### Kahn's Algorithm on the Needed Subgraph

#### Derivation

The DFS reads the tie rule directly but pays a recursion frame per package on the path. [Kahn's algorithm](https://en.wikipedia.org/wiki/Topological_sorting#Kahn%27s_algorithm) inverts the bookkeeping: each needed package counts its uninstalled dependencies in `pending`, and installing a package notifies its dependents, pushing any whose `pending` count reaches zero into a ready queue. Restricted to the packages the target needs, the queue drains in a valid install order, and a drained queue that covered fewer packages than `needed` is the cycle report. No recursion, at the cost of a reverse adjacency map and counters:

1. Collect `needed` from `target` as in the baseline.
2. Set `pending[package]` to its dependency count and build `dependents`,
   mapping each dependency to the packages waiting on it.
3. Seed a queue with every package whose `pending` count is zero; pop a
   package, append it to `order`, and decrement each dependent's count,
   enqueueing dependents that hit zero.
4. Return `order` when it covers all of `needed`, else `[]`.

#### Walkthrough

Example 1 restricts to `needed = [A, B, C, D, E, F, G]` with `pending = {A: 2, B: 3, C: 1, D: 0, E: 0, F: 1, G: 0}`:

```text
ready = [D, E, G]                                      order []
pop D   pending[B] 3 -> 2                              order [D]
pop E   pending[B] 2 -> 1                              order [D, E]
pop G   pending[F] 1 -> 0: push F        ready [F]     order [D, E, G]
pop F   pending[B] 1 -> 0: push B
        pending[C] 1 -> 0: push C          ready [B, C] order [D, E, G, F]
pop B   pending[A] 2 -> 1                                order [D, E, G, F, B]
pop C   pending[A] 1 -> 0: push A            ready [A]  order [D, E, G, F, B, C]
pop A                                                    order [D, E, G, F, B, C, A]
```

The queue drains after all seven packages are ordered, so the function returns `[D, E, G, F, B, C, A]`, matching the expected Output for Example 1. Had a cycle trapped two packages, their `pending` counts would never reach zero, `order` would fall short of `needed`, and the length check would return `[]`.

#### Solution

The code is the countdown: build the counters once, then let each install fire the packages it unblocks.

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, dependencies: List[List[str]], target: str) -> List[str]:
        """Return an install order for target and its transitive
        dependencies, [] on a cycle.

        Time:  O(V + E): discovery, counter setup, and the drain each touch
            every needed package and every dependency edge a constant number
            of times.
        Space: O(V + E) for the adjacency maps, counters, and queue.
        """
        dependency_map: dict[str, List[str]] = {}
        for package, dependency in dependencies:
            dependency_map.setdefault(package, []).append(dependency)

        needed: List[str] = []
        seen = {target}
        frontier = deque([target])
        while frontier:
            package = frontier.popleft()
            needed.append(package)
            for next_dependency in dependency_map.get(package, []):
                if next_dependency not in seen:
                    seen.add(next_dependency)
                    frontier.append(next_dependency)

        dependents: dict[str, List[str]] = {}
        pending = dict.fromkeys(needed, 0)
        for package in needed:
            package_dependencies = dependency_map.get(package, [])
            pending[package] = len(package_dependencies)
            for next_dependency in package_dependencies:
                dependents.setdefault(next_dependency, []).append(package)

        ready = deque(
            package for package in needed if pending[package] == 0
        )
        order: List[str] = []
        while ready:
            package = ready.popleft()
            order.append(package)
            for next_package in dependents.get(package, []):
                pending[next_package] -= 1
                if pending[next_package] == 0:
                    ready.append(next_package)
        return order if len(order) == len(needed) else []
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(V + E)`

Discovery visits each needed package and edge once, the setup pass re-reads each package's dependency list once, and the drain performs one decrement per edge and one enqueue and dequeue per package.

##### Space Complexity: `O(V + E)`

The dependency and dependent maps store every edge, and `pending`, `ready`, and `order` hold one entry per needed package.

#### Key Insights

- The `pending` countdown turns "are all dependencies installed?" from a repeated scan into a single integer comparison at notification time.
- Cycle detection is the length check: packages inside a cycle never reach `pending == 0`, so a short `order` is the entire proof.
- The queue's emission order is governed by discovery order and arrival time, not literally by input-pair order; on this example it coincides with the DFS postorder, but the DFS is the variant that implements the stated tie rule by construction.
- Building both `pending` and `dependents` in one pass over `needed` keeps the setup linear even though the maps point in opposite directions.

## Comparison of Solutions

### Time Complexity

- **Repeated Readiness Scan**: `O(V × (V + E))` - up to `V` full sweeps over packages and edges.
- **DFS Postorder from the Target**: `O(V + E)` - one three-state visit per package, each edge relaxed from its source once.
- **Kahn's Algorithm on the Needed Subgraph**: `O(V + E)` - one decrement per edge, one enqueue and dequeue per package.

### Space Complexity

- **Repeated Readiness Scan**: `O(V + E)` - dependency map plus the needed and installed sets.
- **DFS Postorder from the Target**: `O(V + E)` - dependency map and state, with an `O(V)` recursion stack.
- **Kahn's Algorithm on the Needed Subgraph**: `O(V + E)` - two adjacency maps, counters, and the queue.

### Trade-offs

- **Repeated Readiness Scan**: the statement acted out step by step and trivially correct, but it re-tests every unplaced package on every pass.
- **DFS Postorder from the Target**: linear, directly encodes the input-pair tie rule, and needs no reverse edges; recursion depth grows with the longest dependency chain.
- **Kahn's Algorithm on the Needed Subgraph**: linear without recursion, so deep chains cannot overflow the call stack, but it carries reverse-adjacency and counter bookkeeping and its emission order is queue-driven rather than rule-driven.

### When to Use Each

- **Repeated Readiness Scan**: tiny inputs, or as the spoken first step that defines the readiness condition before optimizing it.
- **DFS Postorder from the Target** (Recommended): the interview default: one pass, the tie rule falls out of the loop order, and cycle detection is one state value.
- **Kahn's Algorithm on the Needed Subgraph**: when recursion depth is a concern (very long dependency chains) or when the codebase already maintains in-degree counters.

### Optimization Notes

- Restricting every algorithm to the packages discovered from `target` is the biggest constant-factor win on inputs like Example 1, where most of the pairs are irrelevant; sorting the whole graph would also give unrelated packages a say in the output.
- The DFS's `VISITED` short-circuit keeps shared subtrees cheap; dropping it turns the linear visit exponential on diamond-shaped dependency graphs.
- Kahn's variant balances duplicate pairs for free: a duplicated edge inflates both the `pending` count and the `dependents` entries, so the decrements still land.
- In an online assessment, expect the follow-up "how do you detect the cycle's members?": the DFS's `VISITING` path is the starting point, since the packages on the path between the two `VISITING` hits are exactly the cycle.
