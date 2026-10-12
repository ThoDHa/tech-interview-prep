# [E-commerce Notification Router](https://www.fastprep.io/problems/amazon-ecommerce-notification-router)

**Easy** | **NN minutes** | **Array, String, Simulation**

Implement the routing decision for a batch of e-commerce notifications. For notification i, preferredChannels[i] is the user's preferred channel and priorities[i] is either NORMAL or URGENT.

A NORMAL notification routes only to the user's preferred channel.An URGENT notification routes to all channels in the fixed order EMAIL, SMS, PUSH.Return one channel array per notification. Implement only the routing decisions; delivery handlers and delivery success are outside this task.

## Examples

### Example 1

**Input:** `preferredChannels = ["EMAIL","SMS","PUSH"]`, `priorities = ["NORMAL","URGENT","NORMAL"]`

**Output:** `[["EMAIL"],["EMAIL","SMS","PUSH"],["PUSH"]]`

**Explanation:** The normal notifications use their preferences, while the urgent notification is sent through all three routing channels.

### Example 2

**Input:** `preferredChannels = ["PUSH"]`, `priorities = ["URGENT"]`

**Output:** `[["EMAIL","SMS","PUSH"]]`

**Explanation:** Urgency overrides the preferred channel and selects every channel in canonical order.

### Example 3

**Input:** `preferredChannels = ["SMS","EMAIL"]`, `priorities = ["NORMAL","NORMAL"]`

**Output:** `[["SMS"],["EMAIL"]]`

**Explanation:** Each normal notification produces exactly one route.

## Constraints

- `1 <= preferredChannels.length == priorities.length <= 10^5.`
- `Every preferred channel is EMAIL, SMS, or PUSH.`
- `Every priority is NORMAL or URGENT.`

## Solutions

### Inline Conditional Chain

#### Derivation

The most literal reading of the routing rule is to decide each notification on its own: look at the priority, and either wrap the user's preferred channel alone or emit every channel in the fixed order. The rules are a two-way branch, so a plain `if`/`else` inside one loop over the notifications mirrors the statement line for line:

1. Start `routes` as an empty list, one slot per notification.
2. Walk `preferredChannels` and `priorities` in lockstep with `zip`, naming each
   pair `preferred_channel` and `priority`.
3. When `priority == "NORMAL"`, append `[preferred_channel]`.
4. Otherwise the notification is `URGENT`: append `["EMAIL", "SMS", "PUSH"]`, the
   fixed canonical order.
5. Return `routes`.

#### Walkthrough

Example 1, `preferredChannels = ["EMAIL","SMS","PUSH"]`, `priorities = ["NORMAL","URGENT","NORMAL"]`:

```text
notification 0   NORMAL, preferred EMAIL   -> routes = [["EMAIL"]]
notification 1   URGENT, preferred SMS     -> routes = [["EMAIL"], ["EMAIL","SMS","PUSH"]]
notification 2   NORMAL, preferred PUSH    -> routes = [["EMAIL"], ["EMAIL","SMS","PUSH"], ["PUSH"]]
```

Each notification produces exactly one route list, so the returned value is `[["EMAIL"],["EMAIL","SMS","PUSH"],["PUSH"]]`, matching the expected Output. Example 3 behaves the same way with two `NORMAL` rows, and Example 2 shows the urgent branch firing on its own: `["PUSH"]` preferred, `["EMAIL","SMS","PUSH"]` returned, because urgency overrides the preference.

#### Solution

The code is the walkthrough's lockstep loop with its two-way branch:

```python
from typing import List


class Solution:
    def solve(self, preferredChannels: List[str], priorities: List[str]) -> List[List[str]]:
        """Return one route list per notification.

        Time:  O(n): each notification takes one branch test and one constant-
            size route build (one channel, or the fixed three).
        Space: O(n) for the output list; auxiliary space is O(1).
        """
        routes: List[List[str]] = []
        for preferred_channel, priority in zip(preferredChannels, priorities):
            if priority == "NORMAL":
                routes.append([preferred_channel])
            else:
                routes.append(["EMAIL", "SMS", "PUSH"])
        return routes
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every notification costs one string comparison and one list build of size one or three, both constants.

##### Space Complexity: `O(n)`

The output holds one route per notification; beyond it the loop uses no growing bookkeeping.

#### Key Insights

- The two priorities define a total branch: `NORMAL` keeps the preference, everything else (`URGENT`) broadcasts, so no validation of the priority string is needed inside the loop.
- Each route list must be freshly built (`[preferred_channel]`, the literal): sharing one mutable list between notifications would let a later delivery handler mutate another notification's route.
- The canonical order `EMAIL, SMS, PUSH` lives inline here, which is fine for a one-off but is exactly what the next approach extracts.

### Precomputed Route Table

#### Derivation

The inline chain rebuilds the urgent route for every urgent notification and keeps the canonical channel order buried in the loop body. The observation that tidies both: routes depend only on the `(priority, preferred_channel)` pair, and the constraints bound channels to three values and priorities to two, so at most six distinct routes exist. Build each distinct route once into an immutable tuple keyed by that pair, and serve every notification by copying from the table; adding a channel then means editing one constant, and the fixed order is declared exactly once:

1. Declare `urgent_route = ("EMAIL", "SMS", "PUSH")`, the canonical order.
2. Start `route_table` as an empty dictionary keyed by `(priority, preferred_channel)`
   and `routes` as an empty list.
3. For each notification, form `route_key`; on a table miss, store
   `urgent_route` for `URGENT` or the one-channel tuple `(preferred_channel,)`
   for `NORMAL`.
4. Append `list(route_table[route_key])`: the copy keeps each notification's
   route independent.
5. Return `routes`.

#### Walkthrough

Example 1 again, `preferredChannels = ["EMAIL","SMS","PUSH"]`, `priorities = ["NORMAL","URGENT","NORMAL"]`. Each line shows the table state after the notification:

```text
notification 0  key ("NORMAL", "EMAIL")  miss -> store ("EMAIL",)                -> route ["EMAIL"]
notification 1  key ("URGENT", "SMS")    miss -> store ("EMAIL","SMS","PUSH")   -> route ["EMAIL","SMS","PUSH"]
notification 2  key ("NORMAL", "PUSH")   miss -> store ("PUSH",)                -> route ["PUSH"]
```

All three keys are distinct, so each row fills one new table entry, and the returned list is `[["EMAIL"],["EMAIL","SMS","PUSH"],["PUSH"]]`, matching the expected Output. The decisive beat is what a repeated key buys: routing a second `"NORMAL"`/`"EMAIL"` batch of any size copies the already-stored tuple and never rebuilds the route, which is why Example 3's two `NORMAL` notifications each cost one lookup.

#### Solution

The code is the walkthrough's miss-then-copy loop over the shared table:

```python
from typing import Dict, List, Tuple


class Solution:
    def solve(self, preferredChannels: List[str], priorities: List[str]) -> List[List[str]]:
        """Return one route list per notification.

        Time:  O(n): each notification is one dictionary lookup plus one list
            copy of constant size (at most the three fixed channels).
        Space: O(n) for the output; the table holds at most the six distinct
            (priority, channel) routes, so auxiliary space is O(1).
        """
        urgent_route = ("EMAIL", "SMS", "PUSH")
        route_table: Dict[Tuple[str, str], Tuple[str, ...]] = {}
        routes: List[List[str]] = []

        for preferred_channel, priority in zip(preferredChannels, priorities):
            route_key = (priority, preferred_channel)
            if route_key not in route_table:
                if priority == "URGENT":
                    route_table[route_key] = urgent_route
                else:
                    route_table[route_key] = (preferred_channel,)
            routes.append(list(route_table[route_key]))

        return routes
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each notification performs one dictionary probe and one constant-size list copy; the at-most-six table builds happen once each.

##### Space Complexity: `O(n)`

The output dominates. The table is auxiliary and bounded: three channels times two priorities caps it at six entries.

#### Key Insights

- Keying by `(priority, preferred_channel)` collapses the branch into data: the loop no longer knows how many channels exist or what the urgent order is.
- Immutable tuples let one route serve many notifications safely; the per-notification `list(...)` copy preserves the independent-lists guarantee the inline chain already had.
- The asymptotics do not move (`O(n)` either way): the wins are the single declaration point for the channel order and one build per distinct route instead of per notification.

## Comparison of Solutions

### Time Complexity

- **Inline Conditional Chain**: `O(n)` - one branch test and one constant-size route build per notification.
- **Precomputed Route Table**: `O(n)` - one dictionary probe and one constant-size copy per notification.

### Space Complexity

- **Inline Conditional Chain**: `O(n)` - the output list; no auxiliary structure.
- **Precomputed Route Table**: `O(n)` - the output list plus an auxiliary table capped at six entries.

### Trade-offs

- **Inline Conditional Chain**: the shortest expression of the rule and allocation-free beyond the output, but the canonical channel order and the rebuild-every-time behavior live inside the loop.
- **Precomputed Route Table**: centralizes the channel order in one constant and builds each distinct route once, at the cost of a small table and an extra copy per notification.

### When to Use Each

- **Inline Conditional Chain (Recommended)**: the interview default for this task: the rules are a two-way branch, and the code reads like the statement.
- **Precomputed Route Table**: when the routing policy may grow (more channels, more priorities) or the same routes are requested across many batches and route construction is worth amortizing.

### Optimization Notes

- Both approaches walk `preferredChannels` and `priorities` with one `zip`; a misplaced index into two parallel arrays is the classic bug this removes.
- The `list(route_table[route_key])` copy is not optional: handing the same list object to several notifications couples their delivery handlers, which the statement explicitly places outside this task but real handlers would mutate.
- If the channel set ever grows, the table approach needs only the `urgent_route` constant edited; the inline chain needs its literal found and updated in the loop body.
