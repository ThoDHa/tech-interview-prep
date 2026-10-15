"""Environment Variable Store and Substitution — https://www.fastprep.io/problems/amazon-environment-variable-substitution

Write-up & approaches: ../../../docs/amazon/amazon-environment-variable-substitution.md
Reference implementation of the write-up's recommended Character Scanner
with Store Lookup solution, kept next to the harness so authored cases
stay falsifiable. Your own attempt lives in solution.py.
"""

KEY_CHARACTERS = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
)


def is_placeholder_key(candidate: str) -> bool:
    """Return whether `candidate` is a nonempty run of letters, digits,
    or underscores, the key shape the constraints declare.
    """
    return bool(candidate) and all(
        character in KEY_CHARACTERS for character in candidate
    )


class EnvironmentStore:
    def __init__(self) -> None:
        """Start an empty variable store.

        Time:  O(1): one empty dict.
        Space: O(1): nothing stored yet.
        """
        self.store: dict[str, str] = {}

    def set(self, key: str, value: str) -> None:
        """Store or overwrite the value for `key`.

        Time:  O(1) expected: one dict assignment.
        Space: O(1) per new key.
        """
        self.store[key] = value

    def get(self, key: str) -> str | None:
        """Return the stored value for `key`, or None when missing.

        Time:  O(1) expected: one dict read.
        Space: O(1).
        """
        return self.store.get(key)

    def parse(self, text: str) -> str:
        """Scan `text` once, replacing every complete %KEY% placeholder
        whose key exists and keeping missing placeholders unchanged.

        A well-formed but missing key is consumed as a whole chunk, so
        its closing % cannot masquerade as the next opener; a malformed
        candidate (such as the empty text between adjacent % marks)
        emits a single % and resumes one character later. Values enter
        the output and are never re-scanned, which is the statement's
        one-pass rule.

        Time:  O(l) for a text of length l: literal runs move by whole
            slices, placeholder chunks are skipped in one jump, and each
            store lookup hashes only the candidate key.
        Space: O(l): the pieces and the joined result hold at most the
            input text.
        """
        pieces: list[str] = []
        scan_position = 0
        while scan_position < len(text):
            if text[scan_position] != "%":
                next_placeholder = text.find("%", scan_position)
                if next_placeholder == -1:
                    pieces.append(text[scan_position:])
                    break
                pieces.append(text[scan_position:next_placeholder])
                scan_position = next_placeholder
                continue
            closing_index = text.find("%", scan_position + 1)
            if closing_index == -1:
                pieces.append(text[scan_position:])
                break
            candidate = text[scan_position + 1:closing_index]
            if is_placeholder_key(candidate):
                pieces.append(
                    self.store.get(
                        candidate, text[scan_position:closing_index + 1]
                    )
                )
                scan_position = closing_index + 1
            else:
                pieces.append("%")
                scan_position += 1
        return "".join(pieces)


if __name__ == "__main__":
    # Debug playground: cases.json is empty (design-operation starter), so
    # Example 1's operation sequence stands in.
    store = EnvironmentStore()
    store.set("NAME", "Tom")
    print(store.parse("Hello I am %NAME%"))
    print(store.get("MISSING"))
    print(store.parse("%MISSING%"))
