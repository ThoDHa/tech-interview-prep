"""Accounts Merge: https://leetcode.com/problems/accounts-merge/

Write-up & approaches: ../../docs/problems/accounts_merge.md

Given a list of accounts where each `accounts[i]` is `[name, email1, email2, ...]`,
merge accounts that share any common email and return each merged account as the
name followed by its emails in sorted order (accounts in any order).

  uv run python accounts_merge/solution.py     # debug one case (see CASE below)
  uv run pytest accounts_merge/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


def _canon(accounts: List[List[str]]) -> List[List[str]]:
    # Answer order is not fixed: sort emails within each account, then sort accounts.
    return sorted([acc[0]] + sorted(acc[1:]) for acc in accounts)


if __name__ == "__main__":
    # Debug playground: set a breakpoint in accountsMerge above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().accountsMerge(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {_canon(case['expected'])}")
    print(f"got:      {_canon(result)}")
