"""Rendered-site smoke gate, run against the sources a build consumes.

A full mkdocs build takes about 100 seconds, far too slow for every
scripts-suite run, so this module inspects the build inputs directly:
the extra_css / extra_javascript declarations in mkdocs.yml, the shipped
JavaScript, and the docs markdown tree. That closes the casualty class
the October 2026 audit named: a sort gate reintroduced on a retired
landing, an asset entry whose file has gone missing, or a docs-internal
link carrying a retired path (problems/, amazon_oa, interview_prep,
system_design) all shipped silently before, because nothing inspected
what the site renders. Landing pages carry the extra assets site-wide
via mkdocs.yml rather than per-page tags, so "the landings reference the
assets" reduces here to: the assets are declared, the files exist under
docs/, and the gated landing pages exist. What this shape cannot see is
render-time path rewriting by mkdocs, plugins, or the theme; that stays
with the manual `mkdocs build --strict` verification step.

Run with:

    cd practice && uv run pytest ../scripts/
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
MKDOCS_CONFIG_PATH = REPO_ROOT / "mkdocs.yml"

# Path spellings the reorg retired: the docs problems/ tree moved to
# leetcode/, and the underscore directory names became hyphenated.
RETIRED_JS_TOKENS = ("/problems/", "amazon_oa", "interview_prep", "system_design")
RETIRED_LINK_TOKENS = ("problems/", "amazon_oa", "interview_prep", "system_design")
RETIRED_TEXT_TOKENS = ("amazon_oa", "interview_prep", "system_design")
LIVE_GATE_TOKENS = ("/leetcode/", "/amazon/")

# The pages the bank-landing gate in tablesort-init.js serves, spelled
# as docs-tree paths to match mkdocs.yml.
BANK_LANDING_PAGES = ("leetcode/index.md", "amazon/index.md")
GATE_SCRIPT = "javascripts/tablesort-init.js"
EXTRA_ASSET_DIRECTIVES = ("extra_css", "extra_javascript")

_HAS_URL_SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
_MARKDOWN_LINK_TARGET = re.compile(r"\]\(([^)\s]+)")
_LIST_ITEM = re.compile(r"^  - (\S+)\s*$")


def _directive_entries(config_text: str, directive: str) -> list[str]:
    """Return the list items under a top-level mkdocs.yml directive.

    Args:
        config_text: Full text of mkdocs.yml.
        directive: Top-level key whose flat list to read, e.g. extra_css.

    Returns:
        The directive's list items in file order; empty when the
        directive is absent or declares no items. The practice venv has
        no YAML parser and the two directives are flat lists, so a line
        scan reads each entry until the first line that is neither a
        list item nor blank.
    """
    entries: list[str] = []
    inside_directive = False
    for line in config_text.splitlines():
        if not inside_directive:
            inside_directive = line.rstrip() == f"{directive}:"
            continue
        item = _LIST_ITEM.match(line)
        if item is not None:
            entries.append(item.group(1))
        elif line.strip() != "":
            break
    return entries


def _local_entries(entries: list[str]) -> list[str]:
    """Filter an extra-assets list down to docs-tree paths, dropping URLs."""
    return [entry for entry in entries if not _HAS_URL_SCHEME.match(entry)]


def test_extra_asset_files_exist_under_docs():
    config_text = MKDOCS_CONFIG_PATH.read_text(encoding="utf-8")
    for directive in EXTRA_ASSET_DIRECTIVES:
        local_entries = _local_entries(_directive_entries(config_text, directive))
        assert local_entries, f"mkdocs.yml {directive} declares no local files"
        for entry in local_entries:
            assert (DOCS_DIR / entry).is_file(), (
                f"mkdocs.yml {directive} references missing file {entry}"
            )


def test_bank_landing_pages_exist_for_the_javascript_gate():
    for landing in BANK_LANDING_PAGES:
        assert (DOCS_DIR / landing).is_file(), (
            f"bank landing {landing} is gone; the {GATE_SCRIPT} gate would serve no page"
        )


def test_tablesort_gate_targets_the_bank_landings():
    gate_text = (DOCS_DIR / GATE_SCRIPT).read_text(encoding="utf-8")
    for token in LIVE_GATE_TOKENS:
        assert f'endsWith("{token}")' in gate_text, (
            f"{GATE_SCRIPT} no longer gates on {token}"
        )


def test_shipped_javascript_carries_no_retired_tokens():
    config_text = MKDOCS_CONFIG_PATH.read_text(encoding="utf-8")
    for entry in _local_entries(
        _directive_entries(config_text, "extra_javascript")
    ):
        text = (DOCS_DIR / entry).read_text(encoding="utf-8")
        for token in RETIRED_JS_TOKENS:
            assert token not in text, f"{entry} carries retired token {token!r}"


def test_docs_sources_carry_no_retired_internal_link_targets():
    violations: list[str] = []
    for page in sorted(DOCS_DIR.rglob("*.md")):
        text = page.read_text(encoding="utf-8")
        for target in _MARKDOWN_LINK_TARGET.findall(text):
            if _HAS_URL_SCHEME.match(target):
                continue
            for token in RETIRED_LINK_TOKENS:
                if token in target:
                    violations.append(f"{page.relative_to(REPO_ROOT)}: {target}")
    assert not violations, "retired tokens in docs-internal links:\n" + "\n".join(
        violations
    )


def test_sources_and_config_carry_no_bare_retired_tokens():
    violations: list[str] = []
    source_paths = [MKDOCS_CONFIG_PATH, *sorted(DOCS_DIR.rglob("*.md"))]
    for text_path in source_paths:
        text = text_path.read_text(encoding="utf-8")
        for token in RETIRED_TEXT_TOKENS:
            if token in text:
                violations.append(f"{text_path.relative_to(REPO_ROOT)}: {token}")
    assert not violations, "retired underscore tokens in sources:\n" + "\n".join(
        violations
    )


@pytest.mark.parametrize("landing", BANK_LANDING_PAGES)
def test_landing_tables_carry_problem_and_difficulty_columns(landing):
    """Both landings keep the header columns the JS modules assume.

    The filter module's filterable shape is a Problem column plus a
    Difficulty column, and tablesort's minutes comparator expects Time
    cells; either landing dropping a column would silently strand the
    modules that exist to serve it.
    """
    text = (DOCS_DIR / landing).read_text(encoding="utf-8")
    assert "| Problem |" in text, f"{landing} lost its Problem column header"
    assert "| Difficulty |" in text, f"{landing} lost its Difficulty column header"
