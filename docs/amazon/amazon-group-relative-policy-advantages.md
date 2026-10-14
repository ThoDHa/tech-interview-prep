# [Group-Relative Policy Advantages](https://www.fastprep.io/problems/amazon-group-relative-policy-advantages)

**Medium** | **NN minutes** | **Array, Hash Table, Math, Simulation**

Compute group-relative advantages for sampled policy responses. Response i belongs to groupIds[i] and receives the integer reward correctnessRewards[i] + formatRewards[i].

Within each group, compute the population mean and population standard deviation of the combined rewards. The advantage of a response is (reward - mean) / standardDeviation. When a group's standard deviation is zero, every response in that group has advantage zero.

Return the advantages in original response order, formatted to exactly six decimal places.

## Examples

### Example 1

**Input:** `groupIds = [0,0,1,1,1]`, `correctnessRewards = [1,0,1,1,0]`, `formatRewards = [1,0,0,1,0]`

**Output:** `["1.000000","-1.000000","0.000000","1.224745","-1.224745"]`

**Explanation:** Each prompt group is normalized independently after correctness and format rewards are combined.

### Example 2

**Input:** `groupIds = [7,7]`, `correctnessRewards = [1,1]`, `formatRewards = [0,0]`

**Output:** `["0.000000","0.000000"]`

**Explanation:** Equal rewards have zero variance, so both normalized advantages are zero.

## Constraints

- `2 <= groupIds.length <= 100000`
- `All three arrays have the same length.`
- `Each group ID appears at least twice.`
- `-100 <= correctnessRewards[i], formatRewards[i] <= 100`

## Solutions

### Membership Scan per Response

#### Derivation

The advantage of a response needs exactly two group statistics: the population mean and the population standard deviation of the combined rewards inside its group. The baseline recomputes those statistics on demand: for response `position`, walk the whole array once, gathering the rewards of every response whose `groupIds` entry matches, then take the mean, the population standard deviation (root mean squared deviation from that mean), and the quotient `(reward - mean) / standardDeviation`, with the zero-deviation group yielding advantage zero by the statement's rule:

1. Combine `correctnessRewards` and `formatRewards` entrywise into `rewards`.
2. For each position, scan all positions collecting its group's rewards.
3. Normalize with the population statistics; substitute `0.000000` when the deviation is zero.

#### Walkthrough

Example 1, `groupIds = [0,0,1,1,1]`, combined rewards `[2, 0, 1, 2, 0]`. For position 0, the scan collects group 0's rewards `[2, 0]`: mean `1`, deviations `[1, -1]`, population standard deviation `sqrt((1 + 1) / 2) = 1`, advantages `(2 - 1) / 1 = 1.000000` and `(0 - 1) / 1 = -1.000000`. For group 1, the scan collects `[1, 2, 0]`: mean `1`, squared deviations `[0, 1, 1]`, deviation `sqrt(2 / 3) = 0.816497`, advantages `0.000000`, `1.224745`, `-1.224745`. Example 2's single group has rewards `[1, 1]`: deviation zero, so both outputs are `0.000000` by rule, matching.

#### Solution

```python
from math import sqrt
from typing import List


class Solution:
    def solve(
        self,
        groupIds: List[int],
        correctnessRewards: List[int],
        formatRewards: List[int],
    ) -> List[str]:
        """Return group-relative advantages formatted to six decimals.

        Time:  O(n^2): each of the n responses rescans all n group entries.
        Space: O(n): one gathered reward list per response.
        """
        rewards = [
            correctness + formatting
            for correctness, formatting in zip(correctnessRewards, formatRewards)
        ]
        outputs: List[str] = []
        for position in range(len(rewards)):
            group = [
                rewards[other]
                for other in range(len(rewards))
                if groupIds[other] == groupIds[position]
            ]
            mean = sum(group) / len(group)
            deviation = sqrt(
                sum((reward - mean) ** 2 for reward in group) / len(group)
            )
            if deviation == 0:
                outputs.append("0.000000")
            else:
                outputs.append(f"{(rewards[position] - mean) / deviation:.6f}")
        return outputs
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n` responses triggers a full `O(n)` membership scan plus an `O(group size)` statistics pass.

##### Space Complexity: `O(n)`

The gathered group list grows with the largest group.

#### Key Insights

- The zero-deviation rule is a division guard with defined output: equal rewards normalize to zero, not to an error.
- Population statistics (divide by the count) rather than sample statistics (divide by the count minus one) are what the statement fixes.

### One Grouping Pass

#### Derivation

The membership of a response never changes, so rescanning for it is pure repetition. A dictionary from group identifier to the list of member positions turns `n` scans into one walk: pass over the arrays once, appending each position to its group's list. A second walk over the groups computes each group's mean and population deviation once, stored in a dictionary keyed by group identifier. A final walk over the positions reads its group's cached statistics and formats the advantage. Every array entry is touched a constant number of times:

1. One pass builds `members: group identifier to positions`.
2. One pass over `members` computes and stores mean and deviation per group.
3. One pass over positions formats `(reward - mean) / deviation`, guarding zero deviation.

#### Walkthrough

Example 1 again: the grouping pass collects `members[0] = [0, 1]` and `members[1] = [2, 3, 4]`. The statistics pass computes for group 0 mean `1` and deviation `1`, for group 1 mean `1` and deviation `sqrt(2 / 3)`. The formatting pass reads those cached numbers and emits `1.000000, -1.000000, 0.000000, 1.224745, -1.224745` in original order, matching the expected output without any repeated scanning.

#### Solution

```python
from math import sqrt
from typing import Dict, List


class Solution:
    def solve(
        self,
        groupIds: List[int],
        correctnessRewards: List[int],
        formatRewards: List[int],
    ) -> List[str]:
        """Return group-relative advantages formatted to six decimals.

        Time:  O(n): one grouping pass, one statistics pass over each
            group once, one formatting pass.
        Space: O(n): the member lists plus per-group statistics.
        """
        rewards = [
            correctness + formatting
            for correctness, formatting in zip(correctnessRewards, formatRewards)
        ]
        members: Dict[int, List[int]] = {}
        for position, group in enumerate(groupIds):
            members.setdefault(group, []).append(position)
        statistics: Dict[int, List[float]] = {}
        for group, positions in members.items():
            group_rewards = [rewards[position] for position in positions]
            mean = sum(group_rewards) / len(group_rewards)
            deviation = sqrt(
                sum((reward - mean) ** 2 for reward in group_rewards)
                / len(group_rewards)
            )
            statistics[group] = [mean, deviation]
        outputs: List[str] = []
        for position, group in enumerate(groupIds):
            mean, deviation = statistics[group]
            if deviation == 0:
                outputs.append("0.000000")
            else:
                outputs.append(f"{(rewards[position] - mean) / deviation:.6f}")
        return outputs
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Grouping, statistics, and formatting each touch every response once; dictionary operations are constant time per entry.

##### Space Complexity: `O(n)`

The member lists and the statistics map together scale with the number of responses.

#### Key Insights

- Grouping first converts "find my group" from a scan into a lookup; the response order is preserved by formatting in the original indexing.
- Per-group statistics are computed once and shared by every member, which is the entire gap between `O(n^2)` and `O(n)`.
- The running sums variant (`sum` and `sum of squares`) avoids the inner list rebuild for statistics; the list form keeps the mean and deviation readable and is equally linear.

## Comparison of Solutions

### Time Complexity

- **Membership Scan per Response**: `O(n^2)` - each response rescans the array for its group.
- **One Grouping Pass**: `O(n)` - each response is touched a constant number of times.

### Space Complexity

- **Membership Scan per Response**: `O(n)` per response for the gathered group.
- **One Grouping Pass**: `O(n)` total for member lists and statistics.

### Trade-offs

- The baseline needs no auxiliary dictionaries and mirrors the statement sentence by sentence.
- The linear rung is shorter to verify once the dictionary discipline is trusted, and it is the only rung that survives `n = 100000`.

### When to Use Each

- **Membership Scan per Response**: toy inputs and cross-checking the linear rung in tests.
- **One Grouping Pass**: any input at the stated constraints.

### Optimization Notes

- Population variance via `sum of squares` minus `mean squared` trades a second pass for numerical sensitivity to large rewards; the two-pass form used here stays exact for these bounds.
- The zero-deviation guard belongs at formatting time so the cached statistics stay purely numeric.
