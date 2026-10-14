"""Encode and Decode Strings — https://leetcode.com/problems/encode-and-decode-strings/

Write-up & approaches: ../../docs/problems/encode_and_decode_strings.md

Canonical reference implementation: the write-up's optimal approach
(length-prefixed encoding), kept next to the harness so authored cases stay
falsifiable. Your own attempt lives in solution.py.

  uv run python encode_and_decode_strings/reference.py   # debug one case (see below)
  uv run pytest encode_and_decode_strings/               # run the test sets
"""

from typing import List


class Solution:
    def encode(self, strs: List[str]) -> str:
        """Prefix each string with its length and a separator.

        The decoder reads digits up to the separator as a count, so the
        payload's own characters are never interpreted, whatever they hold.

        Time:  O(total): every character is written once.
        Space: O(total): the encoded output is at least as long as the input.
        """
        return "".join(f"{len(s)}#{s}" for s in strs)

    def decode(self, s: str) -> List[str]:
        """Scan length prefixes and slice each payload out of the stream.

        Time:  O(total): the read position advances once per character.
        Space: O(total): the decoded list holds every input character.
        """
        decoded = []
        position = 0
        while position < len(s):
            delimiter = s.index("#", position)
            length = int(s[position:delimiter])
            start = delimiter + 1
            decoded.append(s[start : start + length])
            position = start + length
        return decoded


if __name__ == "__main__":
    # Debug playground: set a breakpoint in encode/decode above, then run this
    # file. cases.json is empty (multi-method starter), so a literal example
    # stands in.
    strs = ["Hello", "World"]
    encoded = Solution().encode(strs)
    print(f"args = {strs}")
    print(f"encoded: {encoded!r}")
    print(f"decoded: {Solution().decode(encoded)}")
