"""Unit tests for the progress tracker's canonical order parser and layout
discovery.

The canonical order comes from the problem table the index-tables
generator emits into docs/leetcode/index.md. Discovery is pinned against
a tmp bank-shaped tree (leetcode/ and amazon/ subdirs) and the flat
fallback layout. Run with:

    cd practice && uv run pytest test_progress.py
"""

import progress
import pytest


@pytest.fixture
def patch_docs_index(tmp_path, monkeypatch):
    """Point the tracker at a caller-written landing page."""

    def _patch(text):
        index = tmp_path / "index.md"
        index.write_text(text, encoding="utf-8")
        monkeypatch.setattr(progress, "DOCS_INDEX", index)
        return index

    return _patch


@pytest.fixture
def patch_practice_dir(tmp_path, monkeypatch):
    """Point the tracker's practice root at a caller-built tree."""

    def _patch():
        monkeypatch.setattr(progress, "PRACTICE_DIR", tmp_path)
        return tmp_path

    return _patch


UNIFIED_TABLE = """\
# Problems

<!-- unified-leetcode:start -->
## Problem List

| Problem | Difficulty | Category | Practice at | Tracks | Time |
|---|---------|------------|----------|--------|------|
| [Two Sum](two_sum.md) | Easy | Array, Hash Table | [LeetCode](https://leetcode.com/problems/two-sum/) | [Grind 75](https://www.techinterviewhandbook.org/grind75?order=grind75-order) + [NeetCode 150](https://neetcode.io/practice/neetcode150) | 15 minutes |
| [Daily Temperatures](daily_temperatures.md) | Medium | Stack | [LeetCode](https://leetcode.com/problems/daily-temperatures/) | [NeetCode 150](https://neetcode.io/practice/neetcode150) |  |
| [Implement Trie (Prefix Tree)](implement_trie_prefix_tree.md) | Medium | Trie | [LeetCode](https://leetcode.com/problems/implement-trie-prefix-tree/) | [Grind 75](https://www.techinterviewhandbook.org/grind75?order=grind75-order) + [NeetCode 150](https://neetcode.io/practice/neetcode150) | 35 minutes |

Rows marked · Amazon OA also appear in the [Amazon OA bank](../amazon/index.md).
<!-- unified-leetcode:end -->
"""


def test_discover_problems_descends_the_bank_directories(patch_practice_dir):
    practice_root = patch_practice_dir()
    for bank, slug in (("leetcode", "two_sum"), ("amazon", "amazon-word-break")):
        problem_dir = practice_root / bank / slug
        problem_dir.mkdir(parents=True)
        (problem_dir / "solution.py").write_text("", encoding="utf-8")
    assert progress.discover_problems() == ["amazon-word-break", "two_sum"]


def test_discover_problems_ignores_bank_children_without_solution_py(patch_practice_dir):
    practice_root = patch_practice_dir()
    stale_bank = practice_root / "not_a_bank"
    stale_bank.mkdir()
    (stale_bank / "stray_problem").mkdir()
    solved_dir = practice_root / "amazon" / "amazon-ok"
    solved_dir.mkdir(parents=True)
    (solved_dir / "solution.py").write_text("", encoding="utf-8")
    assert progress.discover_problems() == ["amazon-ok"]


def test_discover_problems_falls_back_to_the_flat_layout(patch_practice_dir):
    practice_root = patch_practice_dir()
    flat_dir = practice_root / "two_sum"
    flat_dir.mkdir()
    (flat_dir / "solution.py").write_text("", encoding="utf-8")
    assert progress.discover_problems() == ["two_sum"]


def test_canonical_order_reads_table_rows_in_appearance_order(patch_docs_index):
    patch_docs_index(UNIFIED_TABLE)
    assert progress.canonical_order(
        ["daily_temperatures", "two_sum", "implement_trie_prefix_tree"]
    ) == ["two_sum", "daily_temperatures", "implement_trie_prefix_tree"]


def test_canonical_order_appends_problems_missing_from_the_table(patch_docs_index):
    patch_docs_index(UNIFIED_TABLE)
    assert progress.canonical_order(["two_sum", "zz_extra", "aa_extra"]) == [
        "two_sum",
        "aa_extra",
        "zz_extra",
    ]


def test_canonical_order_tolerates_titles_with_parentheses(patch_docs_index):
    patch_docs_index(UNIFIED_TABLE)
    assert "implement_trie_prefix_tree" in progress.canonical_order(
        ["implement_trie_prefix_tree"]
    )


def test_canonical_order_falls_back_to_alphabetical_when_the_table_is_missing(
    patch_docs_index,
):
    patch_docs_index("# Problems\n\nNo table here.\n")
    assert progress.canonical_order(["bb", "aa"]) == ["aa", "bb"]


def test_canonical_order_falls_back_when_the_file_is_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(progress, "DOCS_INDEX", tmp_path / "absent.md")
    assert progress.canonical_order(["bb", "aa"]) == ["aa", "bb"]


def test_statuses_from_report_strips_the_bank_segment_from_classnames(tmp_path):
    report = tmp_path / "report.xml"
    report.write_text(
        '<testsuite name="pytest">\n'
        '  <testcase classname="leetcode.two_sum.test_two_sum" name="test_two_sum_example_1"/>\n'
        '  <testcase classname="amazon.amazon-word-break.test_amazon-word-break" name="test_example_1"/>\n'
        '  <testcase classname="test_progress" name="test_canonical_order_reads_table_rows_in_appearance_order"/>\n'
        "</testsuite>\n",
        encoding="utf-8",
    )
    statuses = progress.statuses_from_report(report, ["two_sum", "amazon_word_break"])
    assert statuses == {"two_sum": "solved", "amazon_word_break": "unsolved"}


def test_committed_landing_page_orders_the_full_problem_universe():
    known = progress.discover_problems()
    ordered = progress.canonical_order(known)
    assert len(ordered) == len(known)
    assert set(ordered) == set(known)
    assert ordered[0] == "two_sum"
