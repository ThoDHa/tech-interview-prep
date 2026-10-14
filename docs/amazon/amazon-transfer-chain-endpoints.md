# [Initial and Final Accounts in a Transfer Chain](https://www.fastprep.io/problems/amazon-transfer-chain-endpoints)

**Easy** | **NN minutes** | **Array, Hash Table, Graph**

You are given directed account-transfer pairs [from, to] in arbitrary order. Together they form one non-branching chain containing every pair exactly once.

Return [initialAccount, finalAccount], where the initial account has no incoming transfer and the final account has no outgoing transfer.

## Examples

### Example 1

**Input:** `transfers = [[222,111],[111,333],[444,222]]`

**Output:** `[444,333]`

**Explanation:** The complete chain is 444 to 222 to 111 to 333.

### Example 2

**Input:** `transfers = [[1,2]]`

**Output:** `[1,2]`

**Explanation:** A one-transfer chain exposes both endpoints directly.

### Example 3

**Input:** `transfers = [[3,4],[1,3],[4,8]]`

**Output:** `[1,8]`

**Explanation:** Input order does not affect the recovered endpoints.

## Constraints

- `1 ≤ transfers.length ≤ 100000.`
- `Every transfer contains two distinct integer account IDs.`
- `The pairs form exactly one acyclic chain with no branches.`

## Solutions

### Brute Force Endpoint Scan

#### Derivation

The statement defines the two endpoints by a property, not by a position in the input: the initial account never appears as a receiver, the final account never appears as a sender. The literal reading therefore tests the property directly. Every transfer contributes two candidates, its sender for the initial role and its receiver for the final role, and each candidate is settled by one full scan of the pairs:

1. Walk the transfers. For each `candidate_initial = transfer[0]`, scan every pair
   watching `other[1]`; any match means the candidate receives a transfer and is
   disqualified as initial.
2. Symmetrically, for each `candidate_final = transfer[1]`, scan every pair
   watching `other[0]`; any match means the candidate sends a transfer and is
   disqualified as final.
3. Record the two survivors in `initial_account` and `final_account` and return
   them as a pair.

The chain guarantee promises exactly one survivor per role, so no special cases are needed; the cost is the issue. Each of the `n` transfers triggers two scans of `n` pairs, which is quadratic and impractical at the stated `10^5` bound.

#### Walkthrough

Let us run the scan on Example 1: `transfers = [[222,111],[111,333],[444,222]]`, whose chain is `444 → 222 → 111 → 333`. Each row is one candidate test; the inner scan looks for a disqualifying pair:

| candidate | role | disqualifying pair found | verdict |
| --- | --- | --- | --- |
| `222` (sends in `[222,111]`) | initial | `[444,222]` delivers to `222` | not initial |
| `111` (receives in `[222,111]`) | final | `[111,333]` sends from `111` | not final |
| `111` (sends in `[111,333]`) | initial | `[222,111]` delivers to `111` | not initial |
| `333` (receives in `[111,333]`) | final | none: no pair sends from `333` | `final_account = 333` |
| `444` (sends in `[444,222]`) | initial | none: no pair delivers to `444` | `initial_account = 444` |
| `222` (receives in `[444,222]`) | final | `[222,111]` sends from `222` | not final |

Both endpoints survive exactly once and the function returns `[444, 333]`, matching the expected Output. (Example 2's single transfer `[1,2]` works with two empty disqualification scans, returning `[1, 2]`.)

#### Solution

The code is the candidate test from the walkthrough: every transfer proposes its two endpoints, and a full scan settles each proposal.

```python
from typing import List


class Solution:
    def solve(self, transfers: List[List[int]]) -> List[int]:
        initial_account = -1
        final_account = -1

        for transfer in transfers:
            candidate_initial = transfer[0]
            has_incoming = False
            for other in transfers:
                if other[1] == candidate_initial:
                    has_incoming = True
                    break
            if not has_incoming:
                initial_account = candidate_initial

            candidate_final = transfer[1]
            has_outgoing = False
            for other in transfers:
                if other[0] == candidate_final:
                    has_outgoing = True
                    break
            if not has_outgoing:
                final_account = candidate_final

        return [initial_account, final_account]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n` transfers proposes two candidates and each proposal is settled by a scan over all `n` pairs.

##### Space Complexity: `O(1)`

Only the two result slots and the loop candidates; no auxiliary structure.

#### Key Insights

- The endpoint definitions ("no incoming", "no outgoing") are directly executable, which makes this the correctness reference for the faster versions.
- Every candidate test rediscovers membership facts the previous scan already saw: account `111` is re-examined as receiver over and over.
- Quadratic time is disqualifying at the stated bound of `10^5` pairs.

### Net-Degree Count

#### Derivation

The brute force keeps asking "does this account receive?" as if the answer were unknown, when a single pass could record it for every account at once. Graph vocabulary names the fix: count each account's degree activity, where sending one transfer contributes `+1` and receiving one contributes `-1`. Under the chain guarantee each account sends at most once and receives at most once, so a running `balance` over one dictionary classifies every account in a single pass: the initial account is the one with balance `+1` (one outgoing, no incoming), the final account is the one with balance `-1` (one incoming, no outgoing), and every interior account nets `0`:

1. Allocate an empty dictionary `balance`.
2. For each `[sender, receiver]` pair, increment `balance[sender]` and decrement
   `balance[receiver]`, creating entries on first touch with `dict.get`.
3. Scan `balance`: the account whose balance is `+1` is `initial_account`, the
   one whose balance is `-1` is `final_account`.
4. Return `[initial_account, final_account]`.

The degree view also generalizes: with branching allowed, an account could hold a larger balance, and the count would be the tool that detects it. Here the one-chain constraint pins both extremes at magnitude `1`.

#### Walkthrough

Let us build `balance` for Example 1: `transfers = [[222,111],[111,333],[444,222]]`. Each transfer touches two entries; the table shows the dictionary after each touch:

```text
[222,111]   222: +1            balance = {222: 1, 111: -1}
            111: -1            (entry exists, now -1)
[111,333]   111: +1            balance = {222: 1, 111: 0, 333: -1}
            333: -1
[444,222]   444: +1            balance = {222: 0, 111: 0, 333: -1, 444: 1}
            222: -1            (entry exists, back to 0)
```

The interior accounts `222` and `111` each send once and receive once, so their balances cancel to `0`. Exactly one account holds `+1` (`444`, which only sends) and exactly one holds `-1` (`333`, which only receives), so the scan returns `[444, 333]`, matching the expected Output. (Example 3 nets the same way: `1` ends at `+1`, `8` at `-1`, giving `[1, 8]`.)

#### Solution

The code is the two-touch loop from the walkthrough, then a scan that reads off the two extremes.

```python
from typing import List


class Solution:
    def solve(self, transfers: List[List[int]]) -> List[int]:
        balance = {}
        for sender, receiver in transfers:
            balance[sender] = balance.get(sender, 0) + 1
            balance[receiver] = balance.get(receiver, 0) - 1

        for account, account_balance in balance.items():
            if account_balance == 1:
                initial_account = account
            elif account_balance == -1:
                final_account = account

        return [initial_account, final_account]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass touches each pair twice, then one pass reads the dictionary, which holds at most `2n` accounts.

##### Space Complexity: `O(n)`

The `balance` dictionary stores one entry per distinct account, at most `2n`.

#### Key Insights

- One pass computing per-account balances replaces the brute force's repeated membership questions; each account is asked about once and answered in constant time thereafter.
- The balance encoding (`+1` initial, `-1` final, `0` interior) is the in-degree/out-degree distinction collapsed into a single integer, which is what keeps the dictionary flat.
- The chain guarantee is what makes magnitudes exactly `1`; without it, balances would need range checks to separate endpoints from hubs.

### Hash Set Difference

#### Derivation

The degree bookkeeping can be handed to the standard library entirely. The initial account is characterized by set membership alone: it is in the set of senders and not in the set of receivers. The final account is the mirror image. So build the two sets, then let [set difference](https://en.wikipedia.org/wiki/Set_(mathematics)#Complements) perform the classification, no per-account loop left to write:

1. Collect `senders = {transfer[0]}` and `receivers = {transfer[1]}` over all pairs.
2. `senders - receivers` is the set of accounts that send but never receive; the
   chain guarantee makes it a singleton holding `initial_account`.
3. `receivers - senders` is the singleton holding `final_account`.
4. Pop both and return them in order.

This is the same membership insight as the Net-Degree Count with the counters erased: where the dictionary recorded how many times an account sent minus received, the sets record only whether it ever did, which is all the endpoint test needs under the no-branching constraint.

#### Walkthrough

Let us fill the two sets for Example 1: `transfers = [[222,111],[111,333],[444,222]]`. Sets grow as each pair is consumed; repeats are absorbed silently:

```text
[222,111]   senders = {222}          receivers = {111}
[111,333]   senders = {222, 111}     receivers = {111, 333}
[444,222]   senders = {222, 111, 444}   receivers = {111, 333, 222}
```

Neither set saw a repeat on this input, though the structure permits one (every interior account appears in both). The differences isolate the endpoints in both directions:

```text
senders - receivers    = {222, 111, 444} - {111, 333, 222} = {444}
receivers - senders    = {111, 333, 222} - {222, 111, 444} = {333}
```

Popping the singletons yields `[444, 333]`, matching the expected Output. (Example 2 degenerates gracefully: `senders = {1}`, `receivers = {2}`, differences `{1}` and `{2}`, result `[1, 2]`.)

#### Solution

The code is the two-set build and the two differences, nothing else.

```python
from typing import List


class Solution:
    def solve(self, transfers: List[List[int]]) -> List[int]:
        senders = {transfer[0] for transfer in transfers}
        receivers = {transfer[1] for transfer in transfers}

        initial_account = (senders - receivers).pop()
        final_account = (receivers - senders).pop()
        return [initial_account, final_account]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Two comprehension passes build the sets and each set difference is linear in the set sizes.

##### Space Complexity: `O(n)`

Two sets holding at most `n` accounts each.

#### Key Insights

- Under the one-chain constraint, "never receives" is exactly "in senders but not receivers", so membership sets carry the full endpoint test and the counting can be dropped.
- `pop()` on the singleton differences is safe only because the problem guarantees exactly one chain; on arbitrary graphs both differences could hold many accounts or be empty.
- The degree-count version keeps strictly more information (the balances), which is what a branching-input variant would need; this version trades that headroom for the shortest possible code.

## Comparison of Solutions

### Time Complexity

- **Brute Force Endpoint Scan**: `O(n^2)` - two full scans per transfer to settle each candidate endpoint.
- **Net-Degree Count**: `O(n)` - one pass to build balances, one pass to read the extremes.
- **Hash Set Difference**: `O(n)` - two passes to build the sets, linear-time differences.

### Space Complexity

- **Brute Force Endpoint Scan**: `O(1)` - result slots only.
- **Net-Degree Count**: `O(n)` - one dictionary entry per distinct account, at most `2n`.
- **Hash Set Difference**: `O(n)` - two membership sets, at most `n` accounts each.

### Trade-offs

- **Brute Force Endpoint Scan**: needs no auxiliary memory and mirrors the definitions verbatim, but quadratic time is unusable at the stated input size.
- **Net-Degree Count**: single-pass and generalizes naturally to inputs with branching (balances beyond `±1` flag hubs), at the cost of carrying counts the problem never asks about.
- **Hash Set Difference**: the shortest and most declarative expression, but it bakes the one-chain guarantee into `.pop()` and would fail loudly, not gracefully, on branching input.

### When to Use Each

- **Net-Degree Count (Recommended)**: the interview default: linear, one obvious pass, and the degree framing shows the interviewer you see the graph under the array.
- **Hash Set Difference**: when the interviewer wants the tightest implementation and the one-chain constraint is explicitly trusted.
- **Brute Force Endpoint Scan**: for tiny inputs or as the baseline the linear versions are tested against.

### Optimization Notes

- All three approaches work on the input in its arbitrary order; no sorting or chaining is ever needed because the endpoints are degree properties, not position properties.
- A common temptation is to build the chain first (a successor dictionary walked from the initial account); that is strictly more work, since finding the initial account to start the walk already requires one of the endpoint tests above.
- If the input could contain several chains, the set differences would hold one pair per chain, and the degree map would hold one `+1`/`-1` pair per chain; both structures extend to that variant without a redesign.
