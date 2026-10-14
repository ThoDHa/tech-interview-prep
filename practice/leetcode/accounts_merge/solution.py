"""Accounts Merge: https://leetcode.com/problems/accounts-merge/

Write-up & approaches: ../../../docs/leetcode/accounts_merge.md

Given a list of accounts where each `accounts[i]` is `[name, email1, email2, ...]`,
merge accounts that share any common email and return each merged account as the
name followed by its emails in sorted order (accounts in any order).

  uv run python accounts_merge/solution.py     # debug one case (see CASE below)
  uv run pytest accounts_merge/                # run the test sets
"""

from collections import defaultdict
from typing import List

from harness import NotSolved, pick_case


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        graph = defaultdict(set)
        owner = {}

        for account in accounts:
            name = account[0]
            first = account[1]
            for email in account[1:]:
                owner[email] = name
                graph[first].add(email)
                graph[email].add(first)

        visited = set()

        def dfs(start: str) -> list:
            stack = [start]
            component = []

            while stack:
                email = stack.pop()
                if email in visited:
                    continue
                visited.add(email)
                component.append(email)
                for neighbor in graph[email]:
                    if neighbor not in visited:
                        stack.append(neighbor)
            return component

        result = []
        for email in graph:
            if email not in visited:
                component = dfs(email)

                result.append([owner[email]] + sorted(component))

        return result


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
