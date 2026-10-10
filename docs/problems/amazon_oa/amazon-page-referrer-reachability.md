# [Page Referrer Reachability](https://www.fastprep.io/problems/amazon-page-referrer-reachability)

**Medium** | **NN minutes** | **Graph, Breadth First Search, Depth First Search, Hash Table**

You are given a list of web traffic records. Each record is represented as a two-element string array [url, referrer]:

url is the page that a visitor reached.referrer is the page the visitor came from. An empty string represents a direct arrival with no referrer.Every record whose referrer is non-empty creates a directed movement from referrer to url. The reverse movement is not implied.

You are also given query = [start, target]. Return true if target is reachable from start by following zero or more recorded movements. Therefore, return true when start and target are the same page. Otherwise, return false.

Direct-arrival records do not create additional movements.

## Examples

### Example 1

**Input:** `records = [["/catalog","/home"],["/item/7","/catalog"],["/cart","/item/7"]]`, `query = ["/home","/cart"]`

**Output:** `true`

**Explanation:** The records create the directed path /home to /catalog to /item/7 to /cart.

### Example 2

**Input:** `records = [["/pricing","/home"],["/signup","/pricing"]]`, `query = ["/pricing","/home"]`

**Output:** `false`

**Explanation:** The record creates a movement from /home to /pricing, but not the reverse movement requested by the query.

### Example 3

**Input:** `records = [["/landing",""],["/account","/landing"]]`, `query = ["/account","/account"]`

**Output:** `true`

**Explanation:** A page is reachable from itself without following an edge.

## Constraints

- `1 <= records.length <= 2 * 10^5.`
- `Every row in records contains exactly two strings in the order [url, referrer].`
- `Every url, start, and target is non-empty and has length at most 100.`
- `Every referrer is either an empty string or a page URL of length at most 100.`
- `query.length == 2.`
- `Page URLs are compared exactly and are case-sensitive.`
- `The records may contain repeated movements and directed cycles.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
