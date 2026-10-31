"""Counts guard for the tree counts quoted on README and the practice workspace page.

README and docs/interview-prep/practice_workspace.md quote tree counts as of
October 2026: the bank totals (410 Amazon problems, 168 LeetCode folders),
the write-up wave progress (183 of 410), the compiled PDF page count (578 =
168 + 410), the workspace reference-file counts (91 of 168, 17 of 410), the
cases-only Amazon folder count (393 of 410), and the fresh-clone skip floor
(over 3,100). This guard re-counts the tree and fails on drift: a wave
landing that adds or removes problems, write-ups, or case files must update
the quoted counts in the same change. Rewording a quoted sentence also fails
the guard on purpose, so the new wording and these regexes are updated
together. Run with:

    cd practice && uv run pytest ../scripts/
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import Tuple

import generate_amazon_oa_scaffolds as gen

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
PRACTICE_DIR = REPO_ROOT / "practice"
WORKSPACE_PAGE = REPO_ROOT / "docs" / "interview-prep" / "practice_workspace.md"
README_PATH = REPO_ROOT / "README.md"
AMAZON_WRITEUP_DIR = REPO_ROOT / "docs" / "amazon"
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


def bank_problem_folders(bank: str) -> int:
    """Count one bank's problem folders under `practice/`.

    Args:
        bank: Bank directory name under `practice/` (`leetcode` or `amazon`).

    Returns:
        The bank's problem-folder total, per `bank_reference_counts`.
    """
    return bank_reference_counts(bank)[1]


def authored_amazon_writeups() -> int:
    """Count the Amazon write-ups that have left the placeholder state.

    The README wave count names the bank write-ups a human has worked;
    `docs/amazon/index.md` is generator-owned and never counts. The
    placeholder marker is the generator's own authorship test, shared
    with emission so the recount cannot drift from the code it guards.
    """
    writeups = (path for path in AMAZON_WRITEUP_DIR.glob("*.md") if path.name != "index.md")
    return sum(
        1 for path in writeups
        if gen.WRITEUP_PLACEHOLDER_MARKER not in path.read_text(encoding="utf-8")
    )


def amazon_cases_full_folders() -> int:
    """Count the Amazon problem folders carrying a `cases_full.json`."""
    return len(list((PRACTICE_DIR / "amazon").glob("*/cases_full.json")))


def collect_workspace_test_items() -> int:
    """Collect the practice workspace's test items in a subprocess.

    The workspace skip floor claims a property of a full fresh-clone run;
    collecting the workspace's items (no execution) recounts it. The same
    interpreter runs so the workspace's own environment applies, and the
    cache provider stays off so the collection writes nothing.

    Returns:
        The number of test items the workspace collects.

    Raises:
        AssertionError: When the collection fails or reports no count.
    """
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider"],
        cwd=PRACTICE_DIR,
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert completed.returncode == 0, (
        "collecting the workspace failed; fix the suites before trusting"
        f" any count quoted about them: {completed.stderr[-1000:]}"
    )
    match = re.search(r"(\d+) tests collected", completed.stdout)
    assert match, f"collection output carried no count: {completed.stdout[-1000:]}"
    return int(match.group(1))


def test_readme_bank_total_matches_the_tree():
    page = README_PATH.read_text(encoding="utf-8")
    match = re.search(
        r"online-assessment questions \((\d+) problems as of October 2026", page
    )
    assert match, (
        "README no longer carries the expected bank-total sentence ('(N)"
        " problems as of October 2026' on the Amazon OA bullet); update the"
        " sentence together with this regex"
    )
    quoted = int(match.group(1))
    actual = bank_problem_folders("amazon")
    assert quoted == actual, (
        f"README counts {quoted} Amazon problems but the tree has {actual};"
        " update the README count in the same change as the tree"
    )


def test_readme_writeup_wave_count_matches_the_tree():
    page = README_PATH.read_text(encoding="utf-8")
    match = re.search(
        r"Amazon OA write-ups land in waves, (\d+) of (\d+) as of October 2026",
        page,
    )
    assert match, (
        "README no longer carries the expected wave-progress sentence"
        " ('Amazon OA write-ups land in waves, N of M as of October 2026');"
        " update the sentence together with this regex"
    )
    quoted = (int(match.group(1)), int(match.group(2)))
    actual = (authored_amazon_writeups(), bank_problem_folders("amazon"))
    assert quoted == actual, (
        f"README counts {quoted} but the tree has {actual} (authored Amazon"
        " write-ups and bank total); update the README count in the same"
        " change as the tree"
    )


def test_readme_compiled_page_count_matches_the_tree():
    page = README_PATH.read_text(encoding="utf-8")
    match = re.search(
        r"lists all (\d+) problem pages \(as of October 2026\): the (\d+)"
        r" LeetCode track pages in study order, then the (\d+) Amazon OA"
        r" bank pages",
        page,
    )
    assert match, (
        "README no longer carries the expected compiled-page sentence (all"
        " N problem pages: the M LeetCode track pages, then the K Amazon OA"
        " bank pages); update the sentence together with this regex"
    )
    quoted_total, quoted_leetcode, quoted_amazon = (
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
    )
    leetcode_folders = bank_problem_folders("leetcode")
    amazon_folders = bank_problem_folders("amazon")
    assert quoted_leetcode == leetcode_folders, (
        f"README counts {quoted_leetcode} LeetCode track pages but the tree"
        f" has {leetcode_folders}; update the README count in the same"
        " change as the tree"
    )
    assert quoted_amazon == amazon_folders, (
        f"README counts {quoted_amazon} Amazon OA bank pages but the tree"
        f" has {amazon_folders}; update the README count in the same"
        " change as the tree"
    )
    assert quoted_total == leetcode_folders + amazon_folders, (
        f"README totals {quoted_total} problem pages but its own components"
        f" sum to {leetcode_folders + amazon_folders}; update the README"
        " count in the same change as the tree"
    )
    second_mention = re.search(r"Combine all (\d+) problem pages", page)
    assert second_mention, (
        "README no longer carries the 'Combine all N problem pages'"
        " sentence; update it together with this regex"
    )
    assert int(second_mention.group(1)) == quoted_total, (
        f"README's combine sentence counts {second_mention.group(1)} problem"
        f" pages but its compiled-page sentence counts {quoted_total}; the"
        " two quotes must move together"
    )


def test_workspace_page_cases_only_count_matches_the_tree():
    page = WORKSPACE_PAGE.read_text(encoding="utf-8")
    match = re.search(
        r"Amazon problems use no markers: (\d+) of the (\d+) ship only"
        r" `cases\.json`",
        page,
    )
    assert match, (
        "the practice workspace page no longer carries the expected"
        " cases-only sentence ('Amazon problems use no markers: N of the M"
        " ship only `cases.json`'); update the sentence together with this"
        " regex"
    )
    amazon_folders = bank_problem_folders("amazon")
    quoted = (int(match.group(1)), int(match.group(2)))
    actual = (amazon_folders - amazon_cases_full_folders(), amazon_folders)
    assert quoted == actual, (
        f"the practice workspace page counts {quoted} but the tree has"
        f" {actual} (Amazon folders without a cases_full.json, and the bank"
        " total); update the page counts in the same change as the tree"
    )


def test_workspace_page_skip_floor_holds_against_the_workspace():
    page = WORKSPACE_PAGE.read_text(encoding="utf-8")
    match = re.search(r"wall of skips, over ([\d,]+) across the workspace", page)
    assert match, (
        "the practice workspace page no longer carries the expected skip"
        " sentence ('a wall of skips, over N across the workspace'); update"
        " the sentence together with this regex"
    )
    floor = int(match.group(1).replace(",", ""))
    collected = collect_workspace_test_items()
    assert collected > floor, (
        f"the practice workspace page claims over {floor} skips but the"
        f" workspace collects only {collected} test items; lower the quoted"
        " floor in the same change as the tree"
    )
