# [Loyal Customers Across Two Days](https://www.fastprep.io/problems/amazon-loyal-customers)

**Easy** | **NN minutes** | **Hash Table, Sorting**

You are given two arrays of website logs, dayOneLogs and dayTwoLogs. Each log entry contains exactly three strings in this order: timestamp, customerId, and pageId.

A customer is loyal when both conditions hold:

The customer appears in the logs on both days.On each day, the customer visits more than two distinct pages.Return the loyal customer IDs in lexicographically increasing order. Repeated visits to the same page count only once for that day.

## Examples

### Example 1

**Input:** `dayOneLogs = [["09:00","alice","home"],["09:05","alice","search"],["09:10","alice","checkout"],["10:00","bob","home"],["10:05","bob","search"],["10:10","bob","checkout"],["11:00","cara","home"],["11:05","cara","search"],["11:10","cara","checkout"]]`, `dayTwoLogs = [["09:00","alice","home"],["09:05","alice","offers"],["09:10","alice","checkout"],["10:00","bob","home"],["10:05","bob","search"],["12:00","dan","home"],["12:05","dan","search"],["12:10","dan","checkout"]]`

**Output:** `["alice"]`

**Explanation:** alice visits three distinct pages on each day. bob visits only two distinct pages on day two, cara is absent on day two, and dan is absent on day one.

### Example 2

**Input:** `dayOneLogs = [["1","cust-b","p1"],["2","cust-b","p2"],["3","cust-b","p3"],["4","cust-a","p1"],["5","cust-a","p2"],["6","cust-a","p3"]]`, `dayTwoLogs = [["7","cust-a","p4"],["8","cust-a","p5"],["9","cust-a","p6"],["10","cust-b","p4"],["11","cust-b","p5"],["12","cust-b","p6"]]`

**Output:** `["cust-a","cust-b"]`

**Explanation:** Both customers visit three distinct pages on each day. The returned IDs are sorted lexicographically.

## Constraints

- `Every log entry contains exactly three strings: timestamp, customerId, and pageId.`
- `Customer IDs and page IDs are compared exactly as provided.`
- `The timestamp does not affect whether a customer is loyal.`

## Solutions

### Repeated Scans

#### Derivation

The most literal reading of the problem: loyalty is a per-customer question, so collect the customers of day one, and for each of them re-read both log arrays to gather that customer's distinct pages. A customer qualifies when day two shows the customer at all and both days show more than two distinct pages:

1. Collect `day_one_customers`, the distinct customer IDs appearing in
   `dayOneLogs`.
2. For each `customer_id`, scan `dayOneLogs` collecting its distinct
   `page_id` values into `day_one_pages`, then scan `dayTwoLogs` the same way
   into `day_two_pages`.
3. A customer is loyal when `len(day_one_pages) > 2` and
   `len(day_two_pages) > 2`; the second test implicitly covers "appears on
   day two", because any appearance contributes at least one distinct page.
4. Append each loyal `customer_id` and return the list sorted
   lexicographically.

#### Walkthrough

Example 1, with each candidate customer taken from day one and both arrays scanned for it:

```text
alice   day one pages {home, search, checkout} -> 3 distinct
        day two pages {home, offers, checkout} -> 3 distinct   loyal
bob     day one pages {home, search, checkout} -> 3 distinct
        day two pages {home, search}           -> 2 distinct  not > 2
cara    day one pages {home, search, checkout} -> 3 distinct
        day two pages {}                       -> 0, absent   not loyal
dan     not among day one customers                           never checked
loyal = ["alice"]
```

The strict `> 2` test is what rejects `bob`: two distinct day-two pages fail it even though `bob` appears on both days. Only `alice` survives, and the sorted result is `["alice"]`, matching the expected Output.

#### Solution

The code is the per-customer re-scan from the walkthrough, with set comprehensions doing each day's page collection.

```python
from typing import List, Set


class Solution:
    def solve(self, dayOneLogs: List[List[str]], dayTwoLogs: List[List[str]]) -> List[str]:
        day_one_customers = {entry[1] for entry in dayOneLogs}
        loyal: List[str] = []
        for customer_id in sorted(day_one_customers):
            day_one_pages = self.collect_pages(dayOneLogs, customer_id)
            day_two_pages = self.collect_pages(dayTwoLogs, customer_id)
            if len(day_one_pages) > 2 and len(day_two_pages) > 2:
                loyal.append(customer_id)
        return loyal

    def collect_pages(self, logs: List[List[str]], customer_id: str) -> Set[str]:
        return {entry[2] for entry in logs if entry[1] == customer_id}
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(c × (n1 + n2) + c log c)`

Where `c` is the number of distinct day-one customers, `n1` and `n2` the log counts: each customer triggers two full scans, and the candidate IDs are sorted once. With `c` close to `n1` this degrades toward quadratic.

##### Space Complexity: `O(n1 + n2)`

The page sets held for one customer at a time, each bounded by its day's log count.

#### Key Insights

- The presence condition is free: `len(day_two_pages) > 2` already implies the customer appears on day two, because every log entry carries a page.
- Collecting into a `set` deduplicates repeated visits automatically, which is exactly the statement's "repeated visits to the same page count only once".
- Sorting the candidate IDs up front makes the result ordering come free, since the loop appends in lexicographic order.
- The nested re-scan is the bottleneck: every customer pays for the whole log twice, which a single indexed pass per day removes.

### Hash Map with Page Sets

#### Derivation

The repeated-scan approach re-reads the logs once per customer, but one pass per day can index everything the loyalty test needs: a map from each customer ID to the set of pages that customer visited. After the two passes, the loyal customers are the intersection of the maps' key sets filtered by the distinct-page counts, so the whole question becomes two dictionary builds and one filter:

1. Build `day_one_pages` and `day_two_pages`, mapping customer ID to the set
   of `page_id` values, each in one pass over its log array.
2. Walk the keys of `day_one_pages`; a customer with no day-two entry fails
   the `get` default of an empty set.
3. Keep customers where both sets exceed two distinct pages.
4. Return the kept IDs sorted lexicographically.

#### Walkthrough

Example 1, in two build passes and one filter. The maps after each single pass over a day's logs:

```text
day_one_pages = {
  "alice": {home, search, checkout},
  "bob":   {home, search, checkout},
  "cara":  {home, search, checkout},
}
day_two_pages = {
  "alice": {home, offers, checkout},
  "bob":   {home, search},
  "dan":   {home, search, checkout},
}
```

The filter walks `day_one_pages` in lexicographic key order:

```text
alice   day one 3 > 2, day two 3 > 2          keep
bob     day one 3 > 2, day two 2, not > 2     drop
cara    day one 3 > 2, day two 0 (absent)     drop
```

`dan` is never visited: he is a day-two key only, and the filter walks day-one keys. The result is `["alice"]`, matching the expected Output. Example 2 builds two maps of two customers with three pages each, and every customer passes, yielding `["cust-a", "cust-b"]` in sorted order.

#### Solution

The code is the two index builds from the walkthrough plus the filter, with a `pages_by_customer` helper shared by both days.

```python
from typing import Dict, List, Set


class Solution:
    def solve(self, dayOneLogs: List[List[str]], dayTwoLogs: List[List[str]]) -> List[str]:
        day_one_pages = self.pages_by_customer(dayOneLogs)
        day_two_pages = self.pages_by_customer(dayTwoLogs)
        return sorted(
            customer_id
            for customer_id in day_one_pages
            if len(day_one_pages[customer_id]) > 2
            and len(day_two_pages.get(customer_id, set())) > 2
        )

    def pages_by_customer(self, logs: List[List[str]]) -> Dict[str, Set[str]]:
        pages: Dict[str, Set[str]] = {}
        for _, customer_id, page_id in logs:
            pages.setdefault(customer_id, set()).add(page_id)
        return pages
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n1 + n2 + m log m)`

Each log entry is processed once per its day's build; `m`, the number of loyal customers, bounds the final sort of already-distinct IDs.

##### Space Complexity: `O(n1 + n2)`

Both page maps together hold one set entry per log record, with duplicates absorbed by the sets.

#### Key Insights

- One pass per day replaces one pass per customer: indexing once turns the per-customer question into an `O(1)` dictionary lookup.
- `day_two_pages.get(customer_id, set())` encodes the presence condition without a separate membership test: an absent customer reads as zero distinct pages and fails the strict `> 2` check.
- The final sort is over loyal IDs only, which is the only sorting the problem actually requires; the maps themselves stay unordered.
- Set inserts average constant time, so the builds are linear; hashing the IDs and pages is the price the next solution refuses to pay.

### Sort and Group

#### Derivation

Hashing answers "which pages did this customer visit?" in average constant time, but it relies on hashing both the customer and page IDs. A comparison-based alternative achieves the same grouping by sorting: order each day's logs by `(customerId, pageId)`, and every customer's records become one contiguous group in which duplicate pages sit adjacent to each other. Counting distinct pages inside a group is then a single walk that increments only when the page differs from its predecessor, and the two sorted arrays are compared with two pointers that advance whichever day's current customer is smaller:

1. Sort each day's logs by `(customerId, pageId)` into
   `day_one_sorted` and `day_two_sorted`.
2. Walk both arrays with `one_pos` and `two_pos`; advance past the day's
   current customer whenever the two current customer IDs differ.
3. On a match, run `count_group_pages` on each side: it counts page changes
   within the group and returns the group's distinct-page count plus the
   position after the group.
4. A customer is loyal when both counts exceed two; append and continue.
5. Customers emerge in sorted order because both arrays are sorted, so no
   final sort is needed.

#### Walkthrough

Example 1, day one sorted by `(customerId, pageId)`, groups already contiguous:

```text
alice: checkout, home, search   (3 changes)   bob: checkout, home, search
cara: checkout, home, search
```

Day two sorts into `alice: checkout, home, offers`, `bob: home, search`, `dan: checkout, home, search`. The two-pointer walk:

```text
one_pos -> alice, two_pos -> alice   match
   day one group 3 distinct, day two group 3 distinct   loyal, append "alice"
one_pos -> bob, two_pos -> bob       match
   day one 3 distinct, day two 2 distinct               below threshold, skip
one_pos -> cara, two_pos -> dan      "cara" < "dan", advance one_pos
one_pos past end -> loop ends
```

The adjacent-duplicate rule never fires in this example because every visit is to a distinct page; a repeated entry like a second `home` for `alice` would sit next to the first and not increment the count. The result is `["alice"]`, matching the expected Output.

#### Solution

The code is the two-pointer walk from the walkthrough, with `count_group_pages` carrying the adjacent-duplicate rule.

```python
from typing import List, Tuple


class Solution:
    def solve(self, dayOneLogs: List[List[str]], dayTwoLogs: List[List[str]]) -> List[str]:
        day_one_sorted = sorted(dayOneLogs, key=lambda entry: (entry[1], entry[2]))
        day_two_sorted = sorted(dayTwoLogs, key=lambda entry: (entry[1], entry[2]))
        loyal: List[str] = []
        one_pos, two_pos = 0, 0
        while one_pos < len(day_one_sorted) and two_pos < len(day_two_sorted):
            one_customer = day_one_sorted[one_pos][1]
            two_customer = day_two_sorted[two_pos][1]
            if one_customer < two_customer:
                one_pos += 1
            elif one_customer > two_customer:
                two_pos += 1
            else:
                one_count, one_pos = self.count_group_pages(day_one_sorted, one_pos)
                two_count, two_pos = self.count_group_pages(day_two_sorted, two_pos)
                if one_count > 2 and two_count > 2:
                    loyal.append(one_customer)
        return loyal

    def count_group_pages(self, sorted_logs: List[List[str]], group_start: int) -> Tuple[int, int]:
        customer_id = sorted_logs[group_start][1]
        distinct_pages = 0
        position = group_start
        while position < len(sorted_logs) and sorted_logs[position][1] == customer_id:
            if (position == group_start
                    or sorted_logs[position][2] != sorted_logs[position - 1][2]):
                distinct_pages += 1
            position += 1
        return distinct_pages, position
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n1 log n1 + n2 log n2)`

Sorting dominates; the group walks afterwards touch every log entry a constant number of times.

##### Space Complexity: `O(n1 + n2)`

The sorted copies of both log arrays; the group walk itself uses only scalar counters.

#### Key Insights

- Sorting by `(customerId, pageId)` turns distinct-page counting into an adjacency test: duplicates are neighbors, so "count page changes" replaces any per-customer set.
- The two-pointer merge over sorted customers is the same skeleton as merging two sorted lists: advance the smaller side, work only on matches.
- No hashing and no final sort: loyal IDs come out in lexicographic order because both inputs were sorted.
- The asymptotic cost is the sort's `log` factor over the hash map's linear builds, which is the honest price of a comparison-only approach.

## Comparison of Solutions

### Time Complexity

- **Repeated Scans**: `O(c × (n1 + n2) + c log c)` - two full log scans per distinct day-one customer, plus one sort of the candidate IDs.
- **Hash Map with Page Sets**: `O(n1 + n2 + m log m)` - one indexed pass per day plus a sort of the loyal IDs.
- **Sort and Group**: `O(n1 log n1 + n2 log n2)` - two sorts dominate; group walks and the two-pointer merge are linear.

### Space Complexity

- **Repeated Scans**: `O(n1 + n2)` - one customer's page sets at a time, plus the candidate ID set.
- **Hash Map with Page Sets**: `O(n1 + n2)` - both page maps, one set entry per log record.
- **Sort and Group**: `O(n1 + n2)` - the sorted copies of the two log arrays.

### Trade-offs

- **Repeated Scans**: the most direct transcription of the statement and hard to get wrong, but the per-customer re-scan degrades toward quadratic as the customer count grows.
- **Hash Map with Page Sets**: linear builds and an `O(1)` lookup per customer make it the fastest in practice, at the cost of hashing both ID spaces.
- **Sort and Group**: avoids hashing entirely and needs no post-sort of the result, but pays a `log` factor and requires the adjacent-duplicate rule to be remembered when a group is counted.

### When to Use Each

- **Hash Map with Page Sets (Recommended)**: the interview answer: one pass per day, a two-line filter, and the best complexity for realistic log volumes.
- **Sort and Group**: when IDs cannot be hashed cheaply, when the logs already arrive sorted by customer, or in a comparison-only or streaming setting where grouping by contiguity is natural.
- **Repeated Scans**: for tiny inputs, as a cross-check oracle, or as the first spoken step that establishes the loyalty conditions before optimizing.

### Optimization Notes

- The strict threshold matters: both distinct-page counts must exceed two, and a customer with exactly two distinct pages on either day (like `bob` in Example 1) must fail; an off-by-one to `>= 2` passes him wrongly.
- `day_two_pages.get(customer_id, set())` folds the presence test into the count check; in the two-pointer version, presence is enforced by the pointer match itself.
- In the hash-map version, sorting only the loyal survivors (already distinct IDs) beats sorting either day's full customer list.
- The sort-and-group key `(entry[1], entry[2])` must include the page ID: sorting by customer alone still groups correctly, but duplicates would no longer be adjacent and the distinct count would need a set after all.
