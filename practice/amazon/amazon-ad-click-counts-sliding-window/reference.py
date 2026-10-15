"""Recent Advertisement Click Counts — https://www.fastprep.io/problems/amazon-ad-click-counts-sliding-window

Write-up & approaches: ../../../docs/amazon/amazon-ad-click-counts-sliding-window.md
Reference implementation of the write-up's recommended Per-Ad Deque Sliding
Window solution, kept next to the harness so authored cases stay
falsifiable. Your own attempt lives in solution.py.

  uv run python amazon-ad-click-counts-sliding-window/reference.py   # replay the example
  uv run pytest amazon-ad-click-counts-sliding-window/               # run the test sets
"""

from collections import defaultdict, deque
from typing import DefaultDict, Deque, List


class AdClickCounter:
    def __init__(self, k_minutes: int) -> None:
        """Size the window at `60 * kMinutes` seconds and start empty logs.

        Time:  O(1): one multiplication and one empty map.
        Space: O(1): no clicks recorded yet.
        """
        self.window_size = 60 * k_minutes
        self.clicks_by_ad: DefaultDict[str, Deque[int]] = defaultdict(deque)

    def click(self, ad_id: str, timestamp: int) -> None:
        """Record one click at the end of the advertisement's deque.

        Time:  O(1): one dict lookup and one deque append.
        Space: O(1) per call: one timestamp retained until it expires.
        """
        self.clicks_by_ad[ad_id].append(timestamp)

    def count(self, ad_id: str, timestamp: int) -> int:
        """Evict clicks older than the inclusive window, then report how
        many remain for `ad_id`.

        Time:  O(1) amortized: each click is evicted at most once across
            the whole run, so the popleft loop amortizes to constant work
            per query.
        Space: O(w) for `w` clicks still inside the advertisement's
            latest window.
        """
        oldest_allowed = timestamp - self.window_size + 1
        ad_clicks = self.clicks_by_ad[ad_id]
        while ad_clicks and ad_clicks[0] < oldest_allowed:
            ad_clicks.popleft()
        return len(ad_clicks)


if __name__ == "__main__":
    # Debug playground: cases.json is empty (design-operation starter), so
    # Example 1's operation sequence stands in.
    counter = AdClickCounter(1)
    counter.click("shoes", 100)
    counter.click("books", 120)
    counter.click("shoes", 159)
    print(counter.count("shoes", 160))
    print(counter.count("books", 180))
    print(counter.count("shoes", 220))
