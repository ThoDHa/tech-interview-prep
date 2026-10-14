# [Souvenir Shop Purchases](https://www.fastprep.io/problems/amazon-souvenir-shop-purchases)

**Medium** | **NN minutes** | **Array, Simulation, Binary Search, Math**

In an Amazon Souvenir Shop, a shopper visited a souvenir shop with items arranged on the shelf from left to right. The goal is to purchase as many items as possible within a given budget. Notably, the cost of each souvenir increases with each purchase.

Formally, given an array cost of size n, representing the initial cost of each item in the souvenir shop, and m representing the initial amount of money that the shopper has.

The first time a souvenir is bought its cost will be cost[i], the second time it will be 2 * cost[i], the third time it will be 3 * cost[i], and the jth time it will cost j * cost[i], and so on.

The shopper will buy items one by one from left to right, and when she reaches the last item she will go back to the start and repeat this operation until she runs out of money.

What is the number of items that the shopper will buy before she runs out of money?

## Examples

### Example 1

**Input:** `cost = [2, 5, 1, 1]`, `m = 18`

**Output:** `5`

**Explanation:** $23

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-souvenir-shop-purchases; fill them in. -->

## Solutions

The purchase price of an item depends only on how many times it has been
bought before, and the shopper always sweeps the shelf in the same order, so
the whole process is periodic: every item bought once per round, and round
`k` costing exactly `k` times the first round. Every approach below exploits
that rhythm to a different degree.

### Purchase Simulation

#### Derivation

The most literal reading: walk the shelf left to right, buy whatever the
current money affords at its current price, and when the shelf ends, start
over. The stopping rule is built into the sweep itself: prices only ever grow,
so the first item the shopper cannot afford ends the whole trip, and everything
bought before it is the answer:

1. Keep `multipliers`, one entry per item, starting at 1: the next purchase of
   item `position` costs `multipliers[position] * cost[position]`.
2. Sweep `position` from 0 upward; when `money` covers the price, subtract it,
   bump `multipliers[position]`, and count the purchase in `purchases`.
3. The first unaffordable price returns `purchases` immediately.

#### Walkthrough

Example 1, `cost = [2, 5, 1, 1]`, `money = 18`. Each line is one purchase
decision in sweep order:

```text
start            money = 18   multipliers = [1, 1, 1, 1]   purchases = 0
round 1, item 0  price 1 * 2 = 2   money 18 -> 16   purchases 1
round 1, item 1  price 1 * 5 = 5   money 16 -> 11   purchases 2
round 1, item 2  price 1 * 1 = 1   money 11 -> 10   purchases 3
round 1, item 3  price 1 * 1 = 1   money 10 ->  9   purchases 4
round 2, item 0  price 2 * 2 = 4   money  9 ->  5   purchases 5
round 2, item 1  price 2 * 5 = 10  money 5 < 10     stop
```

The first four purchases are one full round costing `2 + 5 + 1 + 1 = 9`; the
fifth is the cheapest item of round 2. Item 1 then asks for `2 * 5 = 10` and
the sweep stops with `purchases = 5`, the expected Output. (The page's `$23`
explanation reads as the same arithmetic from the other side: `$13` spent so
far plus the `$10` the sixth purchase would cost.)

#### Solution

The code is the sweep from the walkthrough: one pass per round, returning on
the first unaffordable price.

```python
from typing import List


class Solution:
    def solve(self, cost: List[int], money: int) -> int:
        """Return how many items the shopper buys before running out of money.

        Time:  O(purchases + n): every purchase is one subtraction, and the
            final partial sweep re-touches at most n items before stopping.
        Space: O(n) for one multiplier per item.
        """
        item_count = len(cost)
        purchases = 0
        multipliers = [1] * item_count
        while True:
            for position in range(item_count):
                price = multipliers[position] * cost[position]
                if money < price:
                    return purchases
                money -= price
                multipliers[position] += 1
                purchases += 1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(purchases + n)`

Every purchase costs one subtraction and one multiplier bump; the sweep stops
during its final partial pass over at most `n` items. With positive costs the
cheapest item's price grows without bound, so `purchases` is finite, though it
scales linearly with `money` when costs are small.

##### Space Complexity: `O(n)`

One multiplier per item; nothing else grows with the budget.

#### Key Insights

- The early return is correct because prices are strictly increasing per
  item: once an item is unaffordable, coming back after buying nothing cannot
  make it cheaper.
- The simulation is exactly what the statement describes, which makes it the
  reference implementation the faster approaches are checked against.
- Its runtime tracks the answer itself, so a long budget over a cheap shelf
  is where it hurts; that gap is what the arithmetic approaches close.

### Arithmetic Series Binary Search

#### Derivation

The simulation never notices that whole rounds repeat. Round `k` costs each
item `k * cost[position]`, so the total price of round `k` is `k * round_cost`
where `round_cost = sum(cost)`, and finishing `k` rounds costs
`round_cost * (1 + 2 + ... + k) = round_cost * k * (k + 1) / 2`, an arithmetic
series. Affording `k` complete rounds is monotone: if `k` rounds fit in
`money`, so do all fewer. That monotone predicate invites binary search for
the largest `complete_rounds` with `round_cost * complete_rounds *
(complete_rounds + 1) // 2 <= money`. Everything after the last full round is
one partial sweep at multiplier `complete_rounds + 1`, which the simulation
already knows how to do:

1. Compute `round_cost = sum(cost)`.
2. Binary search `complete_rounds` over `0..money // round_cost`: probe
   `probe_rounds = (low_rounds + high_rounds + 1) // 2`, keep it when
   `round_cost * probe_rounds * (probe_rounds + 1) // 2 <= money`, else lower
   `high_rounds`.
3. Set `remaining_money = money - round_cost * complete_rounds *
   (complete_rounds + 1) // 2`.
4. Sweep the partial round: `purchases` starts at
   `item_count * complete_rounds`, and each item whose price
   `multiplier * price_base` fits buys once and lowers `remaining_money`;
   stop at the first unaffordable price.

#### Walkthrough

Example 1 again: `round_cost = 9`, so at most `18 // 9 = 2` complete rounds
are in play. The search over `0..2` probes twice:

```text
probe 1: probe_rounds = (0 + 2 + 1) // 2 = 1;  9 * 1 * 2 // 2 = 9  <= 18  -> low_rounds = 1
probe 2: probe_rounds = (1 + 2 + 1) // 2 = 2;  9 * 2 * 3 // 2 = 27 >  18  -> high_rounds = 1
search ends: complete_rounds = 1, remaining_money = 18 - 9 = 9, multiplier = 2

partial round:
  item 0: price 2 * 2 = 4   buys, purchases 4 + 1 = 5, remaining_money 9 -> 5
  item 1: price 2 * 5 = 10  unaffordable -> stop
```

One probe proves round 2 unaffordable as a whole (`27 > 18`) without pricing
its items, and the partial sweep finds the single extra purchase. The function
returns `4 + 1 = 5`, the expected Output.

#### Solution

The code is the search over complete rounds plus the partial sweep, both
driven by the arithmetic series total.

```python
from typing import List


class Solution:
    def solve(self, cost: List[int], money: int) -> int:
        """Return how many items the shopper buys before running out of money.

        Time:  O(n + log(money / sum(cost))): one summation, a binary search
            over complete-round counts with constant-time probes, and one
            final partial sweep over the items.
        Space: O(1) beyond the input.
        """
        item_count = len(cost)
        round_cost = sum(cost)

        low_rounds, high_rounds = 0, money // round_cost
        while low_rounds < high_rounds:
            probe_rounds = (low_rounds + high_rounds + 1) // 2
            if round_cost * probe_rounds * (probe_rounds + 1) // 2 <= money:
                low_rounds = probe_rounds
            else:
                high_rounds = probe_rounds - 1
        complete_rounds = low_rounds
        remaining_money = (
            money - round_cost * complete_rounds * (complete_rounds + 1) // 2
        )

        purchases = item_count * complete_rounds
        multiplier = complete_rounds + 1
        for price_base in cost:
            price = multiplier * price_base
            if remaining_money < price:
                break
            remaining_money -= price
            purchases += 1
        return purchases
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + log(money / sum(cost)))`

Summing the costs is linear; the binary search halves a range of at most
`money / round_cost` candidates with constant-time probes; the partial sweep
touches at most `n` items once.

##### Space Complexity: `O(1)`

A handful of integer accumulators; no structure grows with input or budget.

#### Key Insights

- Charging every item of round `k` a factor `k` collapses a whole round into
  the constant `round_cost * k`, which is what turns a long simulation into
  one logarithmic search.
- The upper bound `money // round_cost` is safe: affording round
  `money // round_cost + 1` alone would already cost more than `money`.
- Binary search needs a monotone predicate, and "can afford the first `k`
  complete rounds" is monotone because the total is strictly increasing in
  `k`; the ceiling division `(low_rounds + high_rounds + 1) // 2` biases the
  probe upward so the search terminates on the keep side.

### Closed-Form Round Count

#### Derivation

The binary search probes several candidates for a quantity algebra already
names: the largest `k` with `k * (k + 1) / 2 <= money / round_cost` is a
triangular-number inversion, solved exactly by an integer square root. With
`Q = money // round_cost`, that count is `complete_rounds =
(isqrt(8 * Q + 1) - 1) // 2`, because `k * (k + 1) / 2 <= Q` holds exactly
when `(2k + 1)^2 <= 8Q + 1`. The integer square root never overestimates, so
the formula is exact for every budget, and the partial sweep after it is the
same three lines as before:

1. Compute `round_cost = sum(cost)` and `Q = money // round_cost`.
2. Set `complete_rounds = (isqrt(8 * Q + 1) - 1) // 2` and
   `remaining_money = money - round_cost * complete_rounds *
   (complete_rounds + 1) // 2`.
3. Sweep the partial round at multiplier `complete_rounds + 1`, stopping at
   the first unaffordable price, and return the purchase count.

#### Walkthrough

Example 1: `round_cost = 9` and `Q = 18 // 9 = 2`, so the formula gives
`complete_rounds = (isqrt(17) - 1) // 2 = (4 - 1) // 2 = 1`:

```text
Q = 2        candidates: k = 1 -> 1  <= 2 (holds),  k = 2 -> 3  > 2 (fails)
isqrt(8 * 2 + 1) = isqrt(17) = 4,  complete_rounds = (4 - 1) // 2 = 1
remaining_money = 18 - 9 * 1 * 2 // 2 = 9,  multiplier = 2

partial round:
  item 0: price 2 * 2 = 4   buys, purchases 4 + 1 = 5, remaining_money 9 -> 5
  item 1: price 2 * 5 = 10  unaffordable -> stop
```

The square root lands on the same `complete_rounds = 1` the binary search
found by probing, and the identical partial sweep buys the fifth item. The
function returns `5`, the expected Output.

#### Solution

The code swaps the binary search for one integer square root, keeping the
partial sweep unchanged.

```python
from math import isqrt
from typing import List


class Solution:
    def solve(self, cost: List[int], money: int) -> int:
        """Return how many items the shopper buys before running out of money.

        Time:  O(n): one summation, one integer square root, and one partial
            sweep over the items.
        Space: O(1) beyond the input.
        """
        item_count = len(cost)
        round_cost = sum(cost)
        complete_rounds = (isqrt(8 * (money // round_cost) + 1) - 1) // 2
        remaining_money = (
            money - round_cost * complete_rounds * (complete_rounds + 1) // 2
        )

        purchases = item_count * complete_rounds
        multiplier = complete_rounds + 1
        for price_base in cost:
            price = multiplier * price_base
            if remaining_money < price:
                break
            remaining_money -= price
            purchases += 1
        return purchases
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The summation and the partial sweep are linear; `isqrt` on machine-sized
integers is constant work.

##### Space Complexity: `O(1)`

The same handful of accumulators as the binary search; the formula replaces
its loop, not its memory.

#### Key Insights

- Inverting a monotone sum twice gives one closed form: rounds are counted by
  a triangular number, and `isqrt` is its exact inverse over integers.
- The floor divisions do the correctness work: `8 * Q + 1` is never a perfect
  square when `Q` sits between two triangular numbers, and the outer floor
  pulls the estimate down to the true count.
- This is the binary search with its loop replaced by algebra; the partial
  sweep stays because the leftover money does not follow a formula cheaply.

## Comparison of Solutions

### Time Complexity

- **Purchase Simulation**: `O(purchases + n)` - one step per purchase plus a
  final partial sweep; the answer itself grows with the budget.
- **Arithmetic Series Binary Search**: `O(n + log(money / sum(cost)))` - linear
  summation, logarithmic round search, one partial sweep.
- **Closed-Form Round Count**: `O(n)` - linear summation, one square root, one
  partial sweep.

### Space Complexity

- **Purchase Simulation**: `O(n)` - one multiplier per item.
- **Arithmetic Series Binary Search**: `O(1)` - constant-size accumulators.
- **Closed-Form Round Count**: `O(1)` - constant-size accumulators.

### Trade-offs

- **Purchase Simulation**: the direct transcription of the rules, correct for
  any pricing scheme (including prices that change by arbitrary rules), but
  its runtime is the answer, which a large budget punishes.
- **Arithmetic Series Binary Search**: commits to the round structure the
  pricing implies and buys a logarithmic round count; the search loop is one
  more mechanism to justify.
- **Closed-Form Round Count**: the same commitment with the loop replaced by
  one `isqrt` line, the fastest and shortest, but the triangular-number
  inversion is the least self-evident step on the page.

### When to Use Each

- **Purchase Simulation**: when the pricing rule might not be linear in the
  purchase count, or as the oracle that validates the other two.
- **Arithmetic Series Binary Search**: the recommended interview answer: it
  states the round insight, scales to any budget, and its monotone-probe
  structure is easy to explain.
- **Closed-Form Round Count**: when the budget is astronomically large or the
  sweep must be constant-time; present it as the binary search's algebraic
  shortcut, derived after the search version.

### Optimization Notes

- The partial sweep after `complete_rounds` touches at most `n` items once,
  so the whole non-simulation family is effectively "one pass plus the round
  count"; nothing else on the page can be shaved.
- Guard the division by `round_cost`: the sweep assumes at least one item with
  a positive cost, which the shop's pricing guarantees.
- A common pitfall is simulating with `while money > 0` as the only stop
  condition; the loop must stop on the first unaffordable price, because
  leftover money never rolls over to a later, more expensive item.

