# [Available Recipes from Initial Supplies](https://www.fastprep.io/problems/amazon-available-recipes-from-supplies)

**Medium** | **NN minutes** | **Graph, Topological Sort, Hash Table**

You are given distinct recipe names in recipes. Row ingredients[i] lists everything needed to make recipes[i]. An ingredient can be an initial supply, another recipe, or a name that is unavailable.

Every initial supplies item is available in unlimited quantity. Whenever every ingredient of a recipe is available, that recipe also becomes available in unlimited quantity and can be used by other recipes. A recipe with no ingredients is available immediately. Recipe-to-recipe dependencies form a directed acyclic graph.

Return every recipe that can eventually become available, in the original order of recipes. Ingredients are never consumed. Initial supplies have distinct names and do not include recipe names.

## Examples

### Example 1

**Input:** `recipes = ["bread","sandwich"]`, `ingredients = [["flour","water"],["bread","ham"]]`, `supplies = ["flour","water","ham"]`

**Output:** `["bread","sandwich"]`

**Explanation:** Bread becomes available first, so it can then enable sandwich.

### Example 2

**Input:** `recipes = ["cake","icing","tea"]`, `ingredients = [["flour","icing"],["sugar"],["water"]]`, `supplies = ["sugar","water"]`

**Output:** `["icing","tea"]`

**Explanation:** Icing and tea are available, but missing flour keeps cake unavailable.

### Example 3

**Input:** `recipes = ["meal","base"]`, `ingredients = [["base"],[]]`, `supplies = []`

**Output:** `["meal","base"]`

**Explanation:** The empty base recipe is immediately available. Return the completed recipes in input order, even though base is enabled first.

## Constraints

- `0 <= recipes.length <= 200 and ingredients.length == recipes.length.`
- `0 <= supplies.length <= 1000.`
- `Names contain from 1 through 20 lowercase ASCII letters.`
- `Every ingredient row contains distinct names; the total number of ingredient references is at most 10000.`
- `Recipe names and supply names are distinct within each array and no recipe name is an initial supply.`
- `The graph formed by references from one recipe to another is acyclic.`

## Deriving the Solution

The statement defines availability recursively (a recipe joins the supplies the moment its last ingredient joins), which is a restatement of a topological order: a recipe can only be decided after every recipe it references is decided. Every approach below therefore computes the same fixed point; they differ in how often they re-ask "which recipes just became available?". One statement detail survives into every approach: the answer is reported in the original order of `recipes`, never in the order recipes become available.

1. **Start literal.** Sweep the recipe list again and again; any recipe whose ingredients are all available joins the supply set; stop when a full sweep changes nothing: see [Repeated Availability Sweeps](#repeated-availability-sweeps).
2. **Release instead of re-scanning.** The sweeps re-read unchanged rows every round; counting what each recipe still waits on and queueing exactly the recipes whose count reaches zero touches every reference once: see [Topological Release Queue](#topological-release-queue).

## Solutions

### Repeated Availability Sweeps

#### Derivation

The most literal reading of "whenever every ingredient of a recipe is available, that recipe also becomes available" is to simulate the sentence until it stops doing anything. Sweep the recipes; a recipe whose ingredient list is inside the current supply set joins the set; repeat until a full sweep enrolls nothing new. The loop must run because one sweep can enable recipes that unlock others later in the list, and it must stop because each round either grows the set or proves the fixed point reached. The available recipes, reported in input order, are the answer:

1. Copy `supplies` into an `available` set.
2. Sweep `recipes` in order: when a recipe is not yet available and every ingredient is in `available`, add it and mark the round changed.
3. Repeat step 2 while any round changed.
4. Return the recipes whose names are in `available`, in input order.

#### Walkthrough

Example 1, `recipes = ["bread", "sandwich"]`, `supplies = ["flour", "water", "ham"]`. One row per enrolled recipe:

```text
sweep 1  bread:     flour, water available     -> available = {flour, water, ham, bread}    changed
         sandwich: bread, ham available       -> available = {..., bread, sandwich}        changed
sweep 2  nothing new -> stop

available recipes in input order: ["bread", "sandwich"]
```

Both recipes enroll during the first sweep and the second sweep confirms the fixed point, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def findAvailableRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        available = set(supplies)
        changed = True
        while changed:
            changed = False
            for name, needed in zip(recipes, ingredients):
                if name not in available and all(item in available for item in needed):
                    available.add(name)
                    changed = True
        return [name for name in recipes if name in available]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rounds * references)`

Each sweep re-reads every ingredient reference, and a chain of `r` recipes can take `r` rounds to fully enroll, so a long dependency chain costs quadratic work: up to `200 * 10000` reference reads at this problem's bounds.

##### Space Complexity: `O(recipes + supplies)`

One set holding every available name.

#### Key Insights

- The sweep is the statement's fixed-point definition with no graph vocabulary at all; its correctness is immediate.
- The cost is re-reading rows that have not changed: a recipe with one missing ingredient is re-tested once per round until that ingredient appears.
- Reporting in input order is a final filtered pass, independent of the order in which recipes enrolled.

### Topological Release Queue

#### Derivation

The sweeps waste their time on unchanged rows. What actually matters per recipe is a single number: how many of its ingredients are not yet available. Initialize that count per recipe (supplies cost nothing; a permanently unavailable name counts and never releases), and record, for every recipe-named ingredient, which recipes wait on it. A recipe whose count starts at zero is immediately available and enters a queue; completing a recipe decrements each dependent's count, and every count that reaches zero enqueues its recipe. Each reference is read once to build the counts and decremented at most once afterward, which is exactly one pass over the input:

1. Put `supplies` into `available`.
2. For each recipe, count its ingredients outside `available` into `outstanding[index]`; for recipe-named ingredients, append `index` to `dependents[ingredient]`.
3. Seed a queue with every index whose count is zero.
4. Pop an index, mark it completed, decrement `outstanding` of its dependents, and enqueue every dependent whose count reaches zero.
5. Return the completed recipes in input order.

#### Walkthrough

Example 3, `recipes = ["meal", "base"]`, `ingredients = [["base"], []]`, `supplies = []`. The queue release order and the reported order differ, which is the point:

```text
outstanding  meal: 1 (base),   base: 0 (no ingredients)
queue seed   [base]
pop base     completed; dependents[base] = [meal]
             meal outstanding 1 -> 0 -> enqueue
pop meal     completed
queue empty  stop

reported in input order: ["meal", "base"]
```

`base` completed first but `meal` is reported first, matching the expected Output and pinning the input-order rule.

#### Solution

The code is the walkthrough's ledger: one outstanding count per recipe, one reverse adjacency for recipe-named references, and a queue that releases dependents as counts hit zero.

```python
from collections import deque
from typing import DefaultDict, List


class Solution:
    def findAvailableRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        available = set(supplies)
        recipe_names = set(recipes)

        outstanding: List[int] = []
        dependents: DefaultDict[str, List[int]] = DefaultDict(list)
        for index, (name, needed) in enumerate(zip(recipes, ingredients)):
            count = 0
            for ingredient in needed:
                if ingredient not in available:
                    count += 1
                    if ingredient in recipe_names:
                        dependents[ingredient].append(index)
            outstanding.append(count)

        ready = deque(index for index, count in enumerate(outstanding) if count == 0)
        completed = [False] * len(recipes)
        while ready:
            index = ready.popleft()
            completed[index] = True
            for dependent in dependents[recipes[index]]:
                outstanding[dependent] -= 1
                if outstanding[dependent] == 0:
                    ready.append(dependent)
        return [name for index, name in enumerate(recipes) if completed[index]]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(recipes + supplies + references)`

Building the counts reads every reference once, seeding the queue scans the counts, and each release decrements one reference's dependent edge at most once.

##### Space Complexity: `O(recipes + references)`

The outstanding counts and completion flags are per recipe; `dependents` holds one entry per recipe-named reference.

#### Key Insights

- The outstanding count is a topological indegree in disguise: recipe-to-recipe references form a DAG, and the queue is Kahn's algorithm releasing in dependency order.
- Permanently unavailable names are handled by doing nothing: they sit in `outstanding` forever, so their recipes never enqueue and their dependents never release.
- The statement's graph is acyclic by contract, so no cycle detection is needed; a count that never reaches zero means an unavailable ingredient, not a deadlock.

## Comparison of Solutions

### Time Complexity

- **Repeated Availability Sweeps**: `O(rounds * references)` - up to one full sweep per chain depth.
- **Topological Release Queue**: `O(recipes + supplies + references)` - one build pass plus one release per reference.

### Space Complexity

- **Repeated Availability Sweeps**: `O(recipes + supplies)` - one availability set.
- **Topological Release Queue**: `O(recipes + references)` - counts, flags, and the reverse adjacency.

### Trade-offs

- **Repeated Availability Sweeps**: the shortest honest transcription of the statement with no auxiliary structures; the price is quadratic behavior on dependency chains, tolerable here (`200 * 10000`) but the wrong habit.
- **Topological Release Queue**: one linear pass and a queue, scaling to the statement's caps without breaking a sweat; the price is the count ledger and reverse adjacency bookkeeping.

### When to Use Each

- **Repeated Availability Sweeps**: as the derivation baseline, or in a quick script where the input is known to be nearly flat.
- **Topological Release Queue (Recommended)**: the answer to give in an interview: it names the structure (topological release) that the statement hints at with its acyclicity contract and its enablement cascade.

### Optimization Notes

- The queue version never re-reads an ingredient row; if recipes are added incrementally, the same ledger extends to streaming updates by pushing new references onto the counts.
- `outstanding` could count only recipe-named and unavailable-name ingredients while supplies are filtered at build time; the code above already skips supplies during the count, so no post-filtering pass is needed.
- The input-order report is one filtered comprehension; sorting anything would be a bug, since the statement asks for `recipes` order, not alphabetical or enablement order.
