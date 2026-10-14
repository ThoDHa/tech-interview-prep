# [Permutations](https://leetcode.com/problems/permutations/)

**Medium** | **25 minutes** | **Array, Backtracking**

**Pattern:** [Backtracking](../patterns/backtracking_exploration/intuition.md)

**Algorithm:** [Backtracking](https://en.wikipedia.org/wiki/Backtracking) · [Permutation](https://en.wikipedia.org/wiki/Permutation) · [Heap's algorithm](https://en.wikipedia.org/wiki/Heap%27s_algorithm)

**Practice:** [`practice/permutations/solution.py`](../../practice/permutations/solution.py)

Given an array `nums` of distinct integers, return all the possible permutations. You can return the answer in any order.

## Examples

### Example 1

**Input:** `nums = [1,2,3]`

**Output:** `[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]`

### Example 2

**Input:** `nums = [0,1]`

**Output:** `[[0,1],[1,0]]`

### Example 3

**Input:** `nums = [1]`

**Output:** `[[1]]`

## Constraints

- `1 <= nums.length <= 6`
- `-10 <= nums[i] <= 10`
- All the integers of `nums` are unique.

## Deriving the Solution

A permutation is built one position at a time: each position takes some element that no earlier position has taken. Every solution below enumerates the same decision tree of `n!` leaves; they differ in how "already taken" is tracked and in whether the tree is walked recursively or grown generation by generation.

1. **Start literal.** Fill positions left to right, trying every number not yet
   in the partial result and undoing each choice after exploring it. Checking "not yet used" by scanning the partial list costs `O(n)` per choice: see [Backtracking with Path Building](#backtracking-with-path-building).
2. **Spot the waste.** The scan re-derives information the recursion already
   had in hand. Recording it in a boolean array turns the check into an `O(1)` lookup: see [Backtracking with Used Array](#backtracking-with-used-array).
3. **Fold the bookkeeping into the array.** Even the flags are redundant: swap
   each chosen element to the front of `nums`, and the split between a fixed prefix and a free suffix does the used-tracking with no extra structure at all: see [Backtracking with Index Swapping](#backtracking-with-index-swapping).
4. **Build up instead of backtracking.** Recursion is not required: the
   permutations of `k` numbers arise by inserting the `k`-th number into every slot of every permutation of the first `k - 1`, at the price of holding each full generation in memory: see [Iterative Build-Up](#iterative-build-up).
5. **Minimize the change between outputs.** All the above rebuild a path prefix
   between outputs. Heap's algorithm arranges the recursion so consecutive permutations differ by a single swap, the minimal-change classic: see [Heap's Algorithm](#heaps-algorithm).
6. **Or let the library enumerate.** `itertools.permutations` implements the
   whole enumeration in C; it goes last because it hides the algorithm being taught: see [Built-in itertools.permutations](#built-in-itertoolspermutations).

## Solutions

### Backtracking with Path Building

#### Derivation

Ask how a single permutation would be written down by hand: pick some element first, then some element not yet picked, and so on until every element is placed. To produce *all* permutations, each such choice point must try every remaining candidate in turn, which is exactly the classic [backtracking](https://en.wikipedia.org/wiki/Backtracking) template: extend one partial result, recurse, then undo the extension, the choose, explore, unchoose pattern. The resulting decision tree has `n!` leaves, one per permutation; each root-to-leaf path corresponds to one ordering of the input:

1. Maintain a `current` list holding the partial permutation under
   construction.
2. When `current` reaches the length of `nums`, a complete permutation has been
   formed, so append a copy to `result`.
3. Otherwise, iterate over `nums` and skip any number already present in
   `current` (the `num not in current` scan).
4. Choose a number by appending it, explore by recursing with
   `backtrack(current)`, then unchoose by popping it so the next iteration starts from a clean slate.

#### Formula

Each position consumes one unused number, so the branching factor shrinks by one at every depth. The leaf count is the [factorial](https://en.wikipedia.org/wiki/Factorial):

$$ n \times (n-1) \times \dots \times 1 = n! $$

```text
n * (n - 1) * ... * 1 = n!
```

The recursion tree is wider than its leaf count suggests. At depth `k` there is one node per ordered arrangement of `k` distinct elements, so the total node count is:

$$ \sum_{k=0}^{n} \frac{n!}{(n-k)!} \ = \ n! \sum_{j=0}^{n} \frac{1}{j!} \ \approx \ e \cdot n! $$

```text
sum over k = 0 to n of n! / (n - k)!
    = n! * (sum over j = 0 to n of 1 / j!)
    approximately e * n!
```

The interior nodes only add a constant factor of about \(e \approx 2.718\) over the \(n!\) leaves, which is why the bound is quoted as \(O(n! \times n)\): the tree's shape contributes nothing asymptotically, and the \(n\) comes from copying each finished permutation.

#### Walkthrough

Let us watch this first solution run on Example 1, `nums = [1,2,3]`. The trace below is an indented call tree: each line is one `backtrack(current)` call, showing the value of `current` when that call begins. Indentation marks recursion depth. A call iterates `num` over `1, 2, 3` in order, skips any `num` already in `current`, and for each survivor it appends, recurses, then pops (the choose, explore, unchoose cycle). When `current` reaches length `3`, a copy is appended to `result`.

```text
backtrack([])
├─ choose 1 -> backtrack([1])
│  ├─ choose 2 -> backtrack([1,2])
│  │  └─ choose 3 -> backtrack([1,2,3])  -> length 3, append [1,2,3]
│  └─ choose 3 -> backtrack([1,3])
│     └─ choose 2 -> backtrack([1,3,2])  -> length 3, append [1,3,2]
├─ choose 2 -> backtrack([2])
│  ├─ choose 1 -> backtrack([2,1])
│  │  └─ choose 3 -> backtrack([2,1,3])  -> length 3, append [2,1,3]
│  └─ choose 3 -> backtrack([2,3])
│     └─ choose 1 -> backtrack([2,3,1])  -> length 3, append [2,3,1]
└─ choose 3 -> backtrack([3])
   ├─ choose 1 -> backtrack([3,1])
   │  └─ choose 2 -> backtrack([3,1,2])  -> length 3, append [3,1,2]
   └─ choose 2 -> backtrack([3,2])
      └─ choose 1 -> backtrack([3,2,1])  -> length 3, append [3,2,1]
```

Reading one branch end to end: `backtrack([])` first appends `1`, recurses into `backtrack([1])`, which appends `2` and recurses into `backtrack([1,2])`, which appends `3` to reach `[1,2,3]`. That call sees `len(current) == 3`, so it appends a copy and returns. Control unwinds: `backtrack([1,2])` pops `3` and has no more numbers to try, so it returns; `backtrack([1])` pops `2`, then tries `3` next, producing `[1,3,2]`. The same unwind-and-retry repeats across the `2` and `3` branches.

Appending in iteration order, `result` fills as `[1,2,3]`, then `[1,3,2]`, `[2,1,3]`, `[2,3,1]`, `[3,1,2]`, and finally `[3,2,1]`. The returned value is `[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]`, which matches the expected Output for Example 1.

#### Solution

The code is the choose, explore, unchoose cycle from the walkthrough, with the length test as the leaf check.

```python
from typing import List


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result: List[List[int]] = []

        def backtrack(current: List[int]) -> None:
            if len(current) == len(nums):
                result.append(current[:])
                return
            for num in nums:
                if num not in current:
                    current.append(num)
                    backtrack(current)
                    current.pop()

        backtrack([])
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n! × n)`

There are `n!` permutations to generate. Each completed permutation costs `O(n)` to copy into the result. The `num not in current` membership scan is also `O(n)`, but it does not change the asymptotic bound that is already dominated by the `n!` leaf count times the `O(n)` work per leaf.

##### Space Complexity: `O(n)`

The recursion depth is at most `n`, and `current` holds at most `n` elements. The output itself is not counted toward auxiliary space.

#### Key Insights

- The choose, explore, unchoose template is the most narratable backtracking pattern and extends naturally to subsets, combinations, and permutations with duplicates.
- Appending `current[:]` rather than `current` is essential; storing the live reference would let later mutations corrupt results already saved.
- The `num not in current` guard keeps the code short and readable, trading an `O(n)` scan for not having to track a separate used structure.

### Backtracking with Used Array

#### Derivation

The path-building recursion pays an `O(n)` toll at every choice point: the `num not in current` scan re-reads the whole partial permutation to answer a yes/no question the recursion could simply remember. Record the answer instead. A boolean array `used`, parallel to `nums`, marks by index which elements are already placed, turning the check into an `O(1)` lookup. Indexing by position rather than value also keeps the approach correct if the problem were later relaxed to allow duplicate values:

1. Keep a `path` list for the partial permutation and a `used` boolean array
   parallel to `nums`.
2. When `path` is full (`len(path) == n`), append a copy to `result`.
3. For each index `i`, skip it when `used[i]` is `True`; otherwise place
   `nums[i]`.
4. Mark `used[i] = True` before recursing and reset it to `False` afterward to
   restore state.

#### Walkthrough

Let us run the first branch on Example 1, `nums = [1,2,3]`, watching `path` and `used` move in lockstep (`T`/`F` abbreviate `True`/`False`). Each line is one event; indentation marks recursion depth:

```text
backtrack()                    path = []       used = [F,F,F]
  i=0: place nums[0]=1         path = [1]      used = [T,F,F]
    i=0: used[0] -> skip
    i=1: place nums[1]=2       path = [1,2]    used = [T,T,F]
      i=0, i=1: used -> skip
      i=2: place nums[2]=3     path = [1,2,3]  used = [T,T,T]  -> append [1,2,3]
      pop, used[2] = False     path = [1,2]    used = [T,T,F]
    pop, used[1] = False       path = [1]      used = [T,F,F]
    i=2: place nums[2]=3       path = [1,3]    used = [T,F,T]
      i=1: place nums[1]=2     path = [1,3,2]  used = [T,T,T]  -> append [1,3,2]
      pop, used[1] = False     path = [1,3]    used = [T,F,T]
    pop, used[2] = False       path = [1]      used = [T,F,F]
  pop, used[0] = False         path = []       used = [F,F,F]
```

Every pop restores `used` along with `path`, so when the top level moves on to `i=1` the state is exactly as it started, and the `2`-first and `3`-first branches unfold the same way. The tree is the same one drawn in the [Backtracking with Path Building](#backtracking-with-path-building) walkthrough, and `result` fills in the same order, ending as `[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]`, the expected Output for Example 1.

#### Solution

The code is the same tree walk with the membership scan replaced by `used` flag flips.

```python
from typing import List


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result: List[List[int]] = []
        n = len(nums)
        path: List[int] = []
        used = [False] * n

        def backtrack() -> None:
            if len(path) == n:
                result.append(path[:])
                return
            for i in range(n):
                if used[i]:
                    continue
                path.append(nums[i])
                used[i] = True
                backtrack()
                path.pop()
                used[i] = False

        backtrack()
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n! × n)`

The algorithm still visits `n!` leaves and copies an `n`-element permutation at each one. The constant `O(1)` `used` lookup removes the linear membership scan, improving the constant factor without changing the asymptotic bound.

##### Space Complexity: `O(n)`

The recursion stack, the `path`, and the `used` array are each `O(n)`. Output space is not counted.

#### Key Insights

- Tracking usage by index with an `O(1)` boolean lookup is strictly faster than the `O(n)` `num not in current` scan.
- Indexing by position rather than value generalizes cleanly to inputs that contain duplicates.
- The recursion remains shallow, bounded by `n`, so stack usage is never a concern within the constraints.

### Backtracking with Index Swapping

#### Derivation

The used array is still a second structure to keep synchronized, and `path` is a third copy of information the input array could carry itself. Both disappear under one observation: if the chosen elements are kept at the *front* of `nums`, the array splits into a fixed prefix `nums[0..start-1]` of placed elements and a free suffix `nums[start..n-1]` of remaining candidates. Choosing a candidate is then just a swap into position `start`, and the partition itself plays the role of the `used` array, which is why no auxiliary tracking structure is needed:

1. When `start` reaches `n`, every position is fixed, so append a copy of
   `nums`.
2. For each `i` from `start` to `n - 1`, swap `nums[i]` into position `start`.
3. Recurse on `start + 1` to fix the next position.
4. Swap back to restore the array before trying the next candidate.

#### Walkthrough

Let us follow `nums` itself mutate on Example 1, `nums = [1,2,3]`. Each line shows the array after a swap, with the fixed prefix left of the `|` bar:

```text
backtrack(0)
  i=0 swap(0,0)      [|1,2,3] -> [1|2,3]
    i=1 swap(1,1)    [1|2,3] -> [1,2|3]
      i=2 swap(2,2)  -> [1,2,3|]   append [1,2,3], swap back
    i=2 swap(1,2)    [1|2,3] -> [1,3|2]
      i=2 swap(2,2)  -> [1,3,2|]   append [1,3,2], swap back
    swap back        -> [1|2,3]
  swap back          -> [|1,2,3]
  i=1 swap(0,1)      [|1,2,3] -> [2|1,3]
    i=1 swap(1,1)    -> [2,1|3]
      i=2 swap(2,2)  -> [2,1,3|]   append [2,1,3], swap back
    i=2 swap(1,2)    [2|1,3] -> [2,3|1]
      i=2 swap(2,2)  -> [2,3,1|]   append [2,3,1], swap back
    swap back        -> [2|1,3]
  swap back          -> [|1,2,3]
  i=2 swap(0,2)      [|1,2,3] -> [3|2,1]
    i=1 swap(1,1)    -> [3,2|1]
      i=2 swap(2,2)  -> [3,2,1|]   append [3,2,1], swap back
    i=2 swap(1,2)    [3|2,1] -> [3,1|2]
      i=2 swap(2,2)  -> [3,1,2|]   append [3,1,2], swap back
    swap back        -> [3|2,1]
  swap back          -> [|1,2,3]
```

The `3`-first branch shows why the emission order differs from the other backtracking variants: swapping `3` to the front leaves the suffix as `[2, 1]`, not `[1, 2]`, so `[3,2,1]` is emitted before `[3,1,2]`. The final `result` is `[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,2,1],[3,1,2]]`: the same six permutations as Example 1's expected Output in a different order, which the problem allows. Every swap has a matching swap-back, so `nums` ends restored to `[1,2,3]`.

#### Solution

The code is the swap, recurse, swap-back cycle from the walkthrough.

```python
from typing import List


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result: List[List[int]] = []
        n = len(nums)

        def backtrack(start: int) -> None:
            if start == n:
                result.append(nums[:])
                return
            for i in range(start, n):
                nums[start], nums[i] = nums[i], nums[start]
                backtrack(start + 1)
                nums[start], nums[i] = nums[i], nums[start]

        backtrack(0)
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n! × n)`

The recursion produces `n!` complete arrangements, and copying each `n`-element arrangement into the result costs `O(n)`.

##### Space Complexity: `O(n)`

Only the recursion stack, bounded by `n`, is used beyond the output. There is no extra `path` or `used` allocation per call.

#### Key Insights

- The fixed-prefix partition encodes which elements are still available, eliminating the `used` array entirely.
- The approach mutates the input array; the symmetric swap-back is what keeps state consistent across sibling recursive calls.
- It is the most space-frugal backtracking variant here, at the cost of being the least obvious to read.

### Iterative Build-Up

#### Derivation

All three backtracking variants lean on recursion. To remove it, change what is grown: instead of extending one partial [permutation](https://en.wikipedia.org/wiki/Permutation) at a time, hold the complete set of permutations of the numbers processed so far and extend the whole generation at once. A permutation of `k` numbers arises from exactly one permutation of the first `k - 1` numbers by inserting the `k`-th number into one of its `k` slots, so inserting the new number everywhere in everything enumerates each longer permutation exactly once:

1. Seed `result` with one empty permutation, `[[]]`.
2. For each `num` in `nums`, create an empty `new_result`.
3. For every existing `perm`, insert `num` at each of its `len(perm) + 1`
   positions (`perm[:i] + [num] + perm[i:]`), appending each to `new_result`.
4. Replace `result` with `new_result` and continue; after the last number,
   `result` holds all `n!` permutations.

#### Walkthrough

Let us grow the generations on Example 1, `nums = [1,2,3]`. Each round takes every existing `perm` and sprouts `len(perm) + 1` children, one per insertion slot:

```text
start      result = [[]]
num = 1    [] -> [1]                            result = [[1]]
num = 2    [1] -> [2,1] [1,2]                   result = [[2,1], [1,2]]
num = 3    [2,1] -> [3,2,1] [2,3,1] [2,1,3]
           [1,2] -> [3,1,2] [1,3,2] [1,2,3]
           result = [[3,2,1], [2,3,1], [2,1,3], [3,1,2], [1,3,2], [1,2,3]]
```

Reading the `num = 3` round: `[2,1]` has three slots (before the `2`, between the two, after the `1`), and inserting `3` into each yields `[3,2,1]`, `[2,3,1]`, `[2,1,3]`. The final generation holds all `3! = 6` permutations of Example 1's expected Output, in insertion order rather than backtracking order; the problem accepts any order.

#### Solution

The code is the round structure from the walkthrough: one generation per number.

```python
from typing import List


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = [[]]
        for num in nums:
            new_result = []
            for perm in result:
                for i in range(len(perm) + 1):
                    new_result.append(perm[:i] + [num] + perm[i:])
            result = new_result
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n! × n)`

After processing `k` numbers there are `k!` permutations, and inserting the next number creates `k + 1` new lists per permutation, each costing `O(k)` to build by slicing. Summed across all rounds the work is dominated by the final `O(n! × n)` term.

##### Space Complexity: `O(n! × n)`

Each round holds the full set of permutations built so far, and the final round materializes all `n!` permutations of length `n` simultaneously.

#### Key Insights

- Permutations can be generated bottom-up without recursion, which avoids any call-stack depth concern.
- The insertion trick is correct because inserting one new element at every position of every shorter permutation enumerates each longer permutation exactly once.
- The tradeoff is memory: unlike the backtracking variants, every intermediate generation is held in full.

### Heap's Algorithm

#### Derivation

Every earlier approach rebuilds a path prefix between outputs. The classic [minimal-change permutation generator](https://en.wikipedia.org/wiki/Heap%27s_algorithm) published by B. R. Heap in 1963 asks for something stronger: produce each permutation from the previous one by a single swap of two elements. (The name refers to its author and has nothing to do with the heap data structure: no priority queue or heap property appears anywhere in the algorithm.)

1. `generate(k)` emits every permutation of the first `k` positions of `nums`
   while leaving `nums[k..n-1]` untouched.
2. When `k == 1`, the arrangement is fully determined, so snapshot `nums[:]`
   into `result`.
3. Otherwise run `k` rounds: each round recurses with `generate(k - 1)`, then
   performs exactly one swap to move a fresh element into position `k - 1` before the next round. No swap follows the final round.
4. The swap is parity-dependent: when `k` is even, swap `nums[i]` (the loop
   index) with `nums[k - 1]`; when `k` is odd, always swap `nums[0]` with `nums[k - 1]`.

The parity rule is the subtle heart of the algorithm. The recursive calls leave the first `k - 1` elements rearranged in a way that depends on whether `k - 1` is even or odd, and the two swap choices are calibrated to that behavior: an inductive argument shows each choice moves an element that has not yet occupied position `k - 1` into that slot, so every element takes the last position exactly once across the `k` rounds.

#### Walkthrough

Let us run `generate(3)` on Example 1, `nums = [1,2,3]`. Each line is one event: either a snapshot at `k == 1` or the single swap that follows a round. The `k = 2` calls swap with the even rule (`nums[i]` with `nums[k - 1]`, and `i` is always `0` there); the top-level `k = 3` call swaps with the odd rule (`nums[0]` with `nums[2]`):

```text
emit [1,2,3]                          first leaf: nums untouched
k=2, i=0: swap nums[0], nums[1]       nums = [2,1,3]
emit [2,1,3]
k=3, i=0: swap nums[0], nums[2]       nums = [3,1,2]   (odd rule)
emit [3,1,2]
k=2, i=0: swap nums[0], nums[1]       nums = [1,3,2]
emit [1,3,2]
k=3, i=1: swap nums[0], nums[2]       nums = [2,3,1]   (odd rule)
emit [2,3,1]
k=2, i=0: swap nums[0], nums[1]       nums = [3,2,1]
emit [3,2,1]                          last leaf: no swap follows
```

Every adjacent pair of emissions differs by exactly one transposition, the minimal-change property. The six snapshots are the six permutations of Example 1's expected Output, in Heap's order rather than backtracking order; the problem accepts any order. Note that `nums` finishes as `[3,2,1]`: the algorithm does not restore the input.

#### Solution

The code is the walkthrough's emit-then-swap cadence, with the parity test choosing each swap's left operand.

```python
from typing import List


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result: List[List[int]] = []

        def generate(k: int) -> None:
            if k == 1:
                result.append(nums[:])
                return
            for i in range(k):
                generate(k - 1)
                if i < k - 1:
                    if k % 2 == 0:
                        nums[i], nums[k - 1] = nums[k - 1], nums[i]
                    else:
                        nums[0], nums[k - 1] = nums[k - 1], nums[0]

        generate(len(nums))
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n! × n)`

There are `n!` permutations, and snapshotting each `n`-element arrangement costs `O(n)`. The generation machinery itself is cheaper than that: only one swap separates consecutive permutations, so the swap work amortizes to `O(1)` per permutation, and the total is dominated by the mandatory copy at each leaf.

##### Space Complexity: `O(n)`

The recursion depth is `n`, and the algorithm permutes `nums` in place with no auxiliary tracking structures. Output space is not counted.

#### Key Insights

- Heap's algorithm is a minimal-change enumeration: consecutive outputs differ by a single transposition, the permutation analogue of a Gray code, which is why the generation work amortizes to `O(1)` swaps per permutation.
- That property makes it a systems and CS-classics tool more than an interview answer: it shines when a consumer can update its state incrementally after one swap (re-evaluating a cost function over the arrangement, exhaustive testing over orderings) instead of materializing every output. Sedgewick's classic survey of permutation generation methods singled it out as among the most efficient. In an interview, backtracking is the expected demonstration.
- Its emission order differs from the backtracking approaches' order, and that is fine here: the problem accepts any order, and the practice tests canonicalize by sorting the outer list of permutations before comparing.
- Like the index-swapping approach, it mutates the input array, and it does not restore the original order when it finishes.

### Built-in itertools.permutations

#### Derivation

When demonstrating the algorithm is not the point, the standard library already ships the enumeration: [`itertools.permutations`](https://docs.python.org/3/library/itertools.html) generates every ordering of the input in C. Each yielded item is a tuple, so a comprehension converts them to lists to match the expected return type. This is the most concise option but is generally not acceptable in interviews, since it hides the algorithm the question is asking you to demonstrate:

1. Call `permutations(nums)` to obtain an iterator over all orderings as
   tuples.
2. Convert each tuple to a list and collect them into the result.

#### Walkthrough

Here the library is the technique, so the trace is of its documented behavior: `permutations` fills positions left to right, taking the candidates for each position in input order, exactly like the path-building tree walked earlier. On Example 1, `nums = [1,2,3]`:

```text
permutations(nums) yields   (1,2,3)  (1,3,2)  (2,1,3)  (2,3,1)  (3,1,2)  (3,2,1)
list(perm) converts to      [1,2,3]  [1,3,2]  [2,1,3]  [2,3,1]  [3,1,2]  [3,2,1]
```

Because the input is already sorted, this is lexicographic order, and the collected result `[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]` matches Example 1's expected Output exactly.

#### Solution

The code is one comprehension over the library's iterator.

```python
from typing import List


from itertools import permutations

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        return [list(perm) for perm in permutations(nums)]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n! × n)`

The library produces `n!` tuples, and converting each `n`-length tuple to a list costs `O(n)`. The asymptotic bound matches the hand-written approaches, with smaller constant factors from the C implementation.

##### Space Complexity: `O(n! × n)`

The returned list stores all `n!` permutations of length `n`. The generator itself uses only `O(n)` internal state.

#### Key Insights

- The standard library does the core work, so this is ranked last despite being the shortest.
- It is ideal for production code where conciseness and constant-factor speed matter more than demonstrating the algorithm.
- Remembering to convert tuples to lists is the only real subtlety.

## Comparison of Solutions

### Time Complexity

- **Backtracking with Path Building**: `O(n! × n)` - `n!` permutations, each `O(n)` to copy, with an additional `O(n)` membership scan that does not change the bound.
- **Backtracking with Used Array**: `O(n! × n)` - same leaf count and copy cost, with the membership scan replaced by an `O(1)` lookup.
- **Backtracking with Index Swapping**: `O(n! × n)` - `n!` arrangements, each `O(n)` to copy.
- **Iterative Build-Up**: `O(n! × n)` - each round inserts the next number into every existing permutation, dominated by the final `O(n! × n)` term.
- **Heap's Algorithm**: `O(n! × n)` - one swap per new permutation amortizes to `O(1)` generation work; the `O(n)` snapshot per output dominates.
- **Built-in itertools.permutations**: `O(n! × n)` - same theoretical bound with optimized C constant factors.

### Space Complexity

- **Backtracking with Path Building**: `O(n)` - recursion stack plus the `current` path.
- **Backtracking with Used Array**: `O(n)` - recursion stack, `path`, and `used` array.
- **Backtracking with Index Swapping**: `O(n)` - recursion stack only, with no auxiliary tracking.
- **Iterative Build-Up**: `O(n! × n)` - holds every intermediate generation of permutations in full.
- **Heap's Algorithm**: `O(n)` - recursion stack only; permutations are generated in place with no auxiliary tracking.
- **Built-in itertools.permutations**: `O(n! × n)` - for storing the result; the generator uses `O(n)` internal state.

### Trade-offs

- **Backtracking with Path Building**: Clearest to narrate and extends to duplicates, at the cost of an `O(n)` membership scan per choice.
- **Backtracking with Used Array**: Removes the membership scan with an `O(1)` lookup, adding one small auxiliary array.
- **Backtracking with Index Swapping**: The most space-frugal variant, but it mutates the input and is the least intuitive to read.
- **Iterative Build-Up**: Recursion-free and easy to reason about, but it holds every intermediate generation in memory.
- **Heap's Algorithm**: Minimal-change generation with a single swap between consecutive permutations, but the parity rule is opaque, it mutates the input, and the emission order is unintuitive.
- **Built-in itertools.permutations**: Concise and fast, but hides the algorithm and is unsuitable for interviews.

### When to Use Each

- **Backtracking with Path Building** (recommended): Best for interviews and learning. The choose, explore, unchoose template is the clearest to explain.
- **Backtracking with Used Array**: When you want the same clarity with a better constant factor, or anticipate generalizing to duplicate values.
- **Backtracking with Index Swapping**: When space is at a premium and mutating the input array is acceptable.
- **Iterative Build-Up**: When a non-recursive construction is preferred and the extra intermediate memory is acceptable.
- **Heap's Algorithm**: When consecutive permutations should differ minimally, such as incrementally re-evaluating a function of the arrangement after each swap; it is a CS classic rather than an expected interview answer.
- **Built-in itertools.permutations**: For production code where performance and conciseness matter more than demonstrating algorithmic knowledge.

### Optimization Notes

- Since every approach shares the `O(n! × n)` time floor, optimization here is about space and clarity rather than asymptotic speed.
- The path-building membership scan is the one avoidable cost: swapping it for an indexed `used` array turns an `O(n)` check into `O(1)`.
- When mutating the input is acceptable, the index-swapping approach removes the per-call `path` allocation entirely.
- Heap's algorithm pushes generation cost to its floor, one swap per permutation, but the mandatory `O(n)` copy per output means the overall `O(n! × n)` bound does not budge.
- A key pitfall across the backtracking variants is appending the live working list instead of a copy; always append `path[:]` or `current[:]` so later mutations do not corrupt stored results.
