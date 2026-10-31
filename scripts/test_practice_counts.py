"""Counts guard for the tree counts quoted on the practice workspace page.

docs/interview-prep/practice_workspace.md quotes tree counts as of October
2026: 91 of the 168 LeetCode folders carry a `reference.py`, and 17 of the
410 Amazon ones do. This guard re-counts the tree and fails on drift:
a wave landing that adds or removes problems or reference files must update
the page counts in the same change. Rewording the quoted sentence also
fails the guard on purpose, so the new wording and this regex are updated
together. Run with:

    cd practice && uv run pytest ../scripts/
"""

import re
from pathlib import Path
from typing import Tuple

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
PRACTICE_DIR = REPO_ROOT / "practice"
WORKSPACE_PAGE = REPO_ROOT / "docs" / "interview-prep" / "practice_workspace.md"
COUNT_SENTENCE = re.compile(
    r"(\d+) of the (\d+) LeetCode folders, (\d+) of the (\d+) Amazon ones,"
    r" as of October 2026"
)


def bank_reference_counts(bank: str) -> Tuple[int, int]:
    """Count one bank's problem folders and the folders carrying a reference file.

    A directory counts as a problem folder when it carries a cases.json or a
    reference.py, so a stray directory (e.g. a misplaced __pycache__) cannot
    inflate the folder total.

    Args:
        bank: Bank directory name under `practice/` (`leetcode` or `amazon`).

    Returns:
        A tuple of (reference.py file count, problem folder count) for the bank.
    """
    bank_dir = PRACTICE_DIR / bank
    reference_files = len(list(bank_dir.glob("*/reference.py")))
    problem_folders = [
        entry
        for entry in bank_dir.iterdir()
        if entry.is_dir()
        and ((entry / "cases.json").exists() or (entry / "reference.py").exists())
    ]
    return reference_files, len(problem_folders)


def test_workspace_page_reference_counts_match_the_tree():
    page = WORKSPACE_PAGE.read_text(encoding="utf-8")
    match = COUNT_SENTENCE.search(page)
    assert match, (
        "the practice workspace page no longer carries the expected count"
        " sentence ('N of the M LeetCode folders, N of the M Amazon ones, as"
        " of October 2026'); update COUNT_SENTENCE together with the page"
    )
    leetcode_reference, leetcode_folders = bank_reference_counts("leetcode")
    amazon_reference, amazon_folders = bank_reference_counts("amazon")
    quoted = (
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
        int(match.group(4)),
    )
    actual = (leetcode_reference, leetcode_folders, amazon_reference, amazon_folders)
    assert quoted == actual, (
        f"the practice workspace page counts {quoted} but the tree has"
        f" {actual} (reference.py files and folder totals per bank);"
        " update the page counts in the same change as the tree"
    )
