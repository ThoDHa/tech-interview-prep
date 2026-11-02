"""Find Word-Multiset Windows — https://www.fastprep.io/problems/amazon-word-multiset-window-search

Write-up & approaches: ../../../docs/amazon/amazon-word-multiset-window-search.md

Reference implementation of the write-up's recommended Match-Count
Sliding Window solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-word-multiset-window-search/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-word-multiset-window-search/              # run the test sets
"""

from typing import Dict, List

from harness import pick_case


class Solution:
    def wordWindowStarts(self, textWords: List[str], targetWords: List[str]) -> List[int]:
        """Return every ascending start index whose consecutive window of
        `len(targetWords)` text words carries exactly the target's word
        multiset, order-free and multiplicity-exact.

        A count map holds the target's needed counts, a second map the
        current window's counts, and a `mismatched` tally counts the
        distinct words whose two counts differ. Each slide changes
        exactly two counts, the word leaving and the word entering, and
        every count update reconciles the tally in O(1) average, so a
        window is compared by reading one integer instead of re-sorting.

        Args:
            textWords: The tokenized text; its length bounds the target's.
            targetWords: The nonempty target multiset, whose length is
                the window size.

        Returns:
            The ascending start indices of the matching windows.

        Time:  O(n + k): one average-constant map update per word
            entering or leaving the window, plus building the target's
            counts, where n = len(textWords) and k = len(targetWords).
        Space: O(n + k): the two count maps hold at most the distinct
            words of the input, plus the result list.
        """
        needed: Dict[str, int] = {}
        for word in targetWords:
            needed[word] = needed.get(word, 0) + 1

        window_size = len(targetWords)
        window: Dict[str, int] = {}
        for word in textWords[:window_size]:
            window[word] = window.get(word, 0) + 1
        mismatched = sum(
            1
            for word in set(window) | set(needed)
            if window.get(word, 0) != needed.get(word, 0)
        )

        def add(word: str) -> None:
            nonlocal mismatched
            if window.get(word, 0) == needed.get(word, 0):
                mismatched += 1
            window[word] = window.get(word, 0) + 1
            if window[word] == needed.get(word, 0):
                mismatched -= 1

        def remove(word: str) -> None:
            nonlocal mismatched
            if window[word] == needed.get(word, 0):
                mismatched += 1
            window[word] -= 1
            if window[word] == needed.get(word, 0):
                mismatched -= 1

        starts: List[int] = []
        if mismatched == 0:
            starts.append(0)
        for start in range(1, len(textWords) - window_size + 1):
            remove(textWords[start - 1])
            add(textWords[start + window_size - 1])
            if mismatched == 0:
                starts.append(start)
        return starts


if __name__ == "__main__":
    # Debug playground: set a breakpoint in wordWindowStarts above, then
    # run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().wordWindowStarts(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
