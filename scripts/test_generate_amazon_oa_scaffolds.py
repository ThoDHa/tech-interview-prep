"""Unit tests for the Amazon OA bank extractor and FastPrep page parser.

The fixtures under scripts/fixtures/ are trimmed copies of the cached bank
pages (Tech-OA-Interview-Questions) and one synthetic FastPrep problem page
shaped like the real server-rendered HTML. Run with:

    uv run --project practice python -m pytest scripts/
"""

import ast
import contextlib
import io
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import generate_amazon_oa_scaffolds as gen

SCRIPTS_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = SCRIPTS_DIR / "fixtures"
HARNESS_PATH = SCRIPTS_DIR.parent / "practice" / "harness.py"

BANK_PAGE = (FIXTURES_DIR / "bank_coding.md").read_text(encoding="utf-8")
BANK_PAGE_2 = (FIXTURES_DIR / "bank_coding_page_2.md").read_text(encoding="utf-8")
BANK_PAGE_3 = (FIXTURES_DIR / "bank_coding_page_3.md").read_text(encoding="utf-8")
FASTPREP_PAGE = (FIXTURES_DIR / "fastprep_problem.html").read_text(encoding="utf-8")

REAL_BANK_PAGES = [
    Path("/tmp/opencode/tech-oa/coding.md"),
    Path("/tmp/opencode/tech-oa/coding-page-2.md"),
    Path("/tmp/opencode/tech-oa/coding-page-3.md"),
]


# ---------------------------------------------------------------------------
# Bank row extraction
# ---------------------------------------------------------------------------


def test_parse_bank_rows_extracts_every_table_row():
    rows = gen.parse_bank_rows(BANK_PAGE)
    assert len(rows) == 6
    first = rows[0]
    assert first["companies"] == ["Stripe"]
    assert first["title"] == "Incident Monitor"
    assert first["slug"] == "stripe-incident-monitor"
    assert first["url"] == "https://www.fastprep.io/problems/stripe-incident-monitor"


def test_parse_bank_rows_normalizes_updated_date_stripping_emoji():
    rows = gen.parse_bank_rows(BANK_PAGE)
    assert rows[0]["updated"] == "2026-09-19"
    assert rows[4]["updated"] == "2026-09-17"
    assert rows[5]["updated"] == "2020-08-27"


def test_parse_bank_rows_splits_multi_company_cell():
    rows = gen.parse_bank_rows(BANK_PAGE)
    assert rows[4]["companies"] == ["Amazon", "Google"]


def test_parse_bank_rows_ignores_non_table_lines():
    rows = gen.parse_bank_rows(BANK_PAGE)
    # Header, alignment row, title, and link lines produce no rows.
    assert all(row["slug"] for row in rows)


# ---------------------------------------------------------------------------
# Manifest building: Amazon filter, dedup, recency ordering
# ---------------------------------------------------------------------------


@pytest.fixture
def seeded_docs_dir(tmp_path, monkeypatch):
    """Point the manifest's write-up reads at synthetic headers.

    build_manifest enriches each row from the write-up pinned at
    DOCS_DIR/<slug>.md; these tests feed fixture bank pages, so the
    directory must hold a synthetic write-up per fixture slug.
    """
    slugs = set()
    for page_text in (BANK_PAGE, BANK_PAGE_2, BANK_PAGE_3):
        for row in gen.parse_bank_rows(page_text):
            slugs.add(row["slug"])
    slug_headers = {
        "amazon-lru-query-result-cache": "**Medium** | **NN minutes** | **Design, Hash Table, Linked List, Simulation**",
        "amazon-maximize-adjacent-difference-with-one-reversal": "**Hard** | **NN minutes** | **Array, Greedy, Math**",
    }
    for slug in slugs:
        header = slug_headers.get(slug, "**Medium** | **NN minutes** | **Array, Math**")
        (tmp_path / f"{slug}.md").write_text(
            "# [Fixture](https://x)\n"
            "\n"
            f"{header}\n",
            encoding="utf-8",
        )
    monkeypatch.setattr(gen, "DOCS_DIR", tmp_path)
    return tmp_path



def test_build_manifest_keeps_only_amazon_tagged_rows(seeded_docs_dir):
    manifest = gen.build_manifest([BANK_PAGE, BANK_PAGE_2])
    assert {entry["slug"] for entry in manifest} == {
        "amazon-maximize-adjacent-difference-with-one-reversal",
        "amazon-inventory-allocation",
        "amazon-lru-query-result-cache",
        "amazon-currency-conversion-rate",
    }


def test_build_manifest_dedups_by_slug_keeping_most_recent(seeded_docs_dir):
    manifest = gen.build_manifest([BANK_PAGE, BANK_PAGE_2])
    entries = [e for e in manifest if e["slug"].endswith("one-reversal")]
    assert len(entries) == 1
    assert entries[0]["updated"] == "2026-09-19"


def test_build_manifest_merges_three_pages_with_dedup_and_exclusion(seeded_docs_dir):
    manifest = gen.build_manifest([BANK_PAGE, BANK_PAGE_2, BANK_PAGE_3])
    slugs = [entry["slug"] for entry in manifest]
    assert slugs[0] == "amazon-telemetry-aggregation-buffer"
    reversal = [
        entry for entry in manifest
        if entry["slug"] == "amazon-maximize-adjacent-difference-with-one-reversal"
    ]
    assert len(reversal) == 1
    assert reversal[0]["updated"] == "2026-09-19"
    assert "amazon-find-minimum-number-of-operations" not in slugs
    assert "uber-ride-surge-estimator" not in slugs


def test_build_manifest_drops_excluded_dead_page_slugs():
    page = (
        "| Company | OA / Interview Question | Practice | Updated |\n"
        "| :-- | :-- | :-: | :-- |\n"
        "|**Amazon**|[Get Min Cost Book](https://www.fastprep.io/problems/amazon-get-min-cost-book)"
        "|[![Practice][p]](https://www.fastprep.io/problems/amazon-get-min-cost-book)"
        "|🔥 Sep 21, 2026|\n"
    )
    assert gen.build_manifest([page]) == []


def test_build_manifest_sorts_most_recent_first(seeded_docs_dir):
    manifest = gen.build_manifest([BANK_PAGE, BANK_PAGE_2])
    updated = [entry["updated"] for entry in manifest]
    assert updated == sorted(updated, reverse=True)


def test_build_manifest_breaks_date_ties_by_slug_ascending(seeded_docs_dir):
    page = (
        "| Company | OA / Interview Question | Practice | Updated |\n"
        "| :-- | :-- | :-: | :-- |\n"
        "|**Amazon**|[Zeta Task](https://www.fastprep.io/problems/amazon-zeta-task)|[![Practice][p]](https://www.fastprep.io/problems/amazon-zeta-task)|Sep 19, 2026|\n"
        "|**Amazon**|[Alpha Task](https://www.fastprep.io/problems/amazon-alpha-task)|[![Practice][p]](https://www.fastprep.io/problems/amazon-alpha-task)|Sep 19, 2026|\n"
    )
    writeups = []
    for slug, title in (
        ("amazon-zeta-task", "Zeta Task"),
        ("amazon-alpha-task", "Alpha Task"),
    ):
        path = gen.DOCS_DIR / f"{slug}.md"
        path.write_text(
            f"# [{title}](https://www.fastprep.io/problems/{slug})\n"
            "\n"
            "**Medium** | **NN minutes** | **Array**\n",
            encoding="utf-8",
        )
        writeups.append(path)
    try:
        manifest = gen.build_manifest([page])
    finally:
        for path in writeups:
            path.unlink()
    assert [entry["slug"] for entry in manifest] == [
        "amazon-alpha-task",
        "amazon-zeta-task",
    ]


def test_build_manifest_entries_carry_required_fields(seeded_docs_dir):
    manifest = gen.build_manifest([BANK_PAGE])
    entry = next(e for e in manifest if e["slug"] == "amazon-lru-query-result-cache")
    assert entry["title"] == "LRU Cache for Query Results"
    assert entry["companies"] == ["Amazon", "Google"]
    assert entry["updated"] == "2026-09-17"
    assert entry["url"].startswith("https://www.fastprep.io/problems/")


def test_build_manifest_persists_the_writeup_header_difficulty_and_categories(seeded_docs_dir):
    manifest = gen.build_manifest([BANK_PAGE])
    entry = next(e for e in manifest if e["slug"] == "amazon-lru-query-result-cache")
    assert entry["difficulty"] == "Medium"
    assert entry["categories"] == "Design, Hash Table, Linked List, Simulation"
    reversal = next(
        e for e in manifest
        if e["slug"] == "amazon-maximize-adjacent-difference-with-one-reversal"
    )
    assert reversal["difficulty"] == "Hard"
    assert reversal["categories"] == "Array, Greedy, Math"


def test_build_manifest_maps_the_unknown_markers_to_none(seeded_docs_dir):
    page = (
        "| Company | OA / Interview Question | Practice | Updated |\n"
        "| :-- | :-- | :-: | :-- |\n"
        "|**Amazon**|[Mystery Task](https://www.fastprep.io/problems/amazon-mystery-task)"
        "|[![Practice][p]](https://www.fastprep.io/problems/amazon-mystery-task)"
        "|Sep 19, 2026|\n"
    )
    (gen.DOCS_DIR / "amazon-mystery-task.md").write_text(
        "# [Mystery Task](https://www.fastprep.io/problems/amazon-mystery-task)\n"
        "\n"
        "**unknown difficulty** | **NN minutes** | **unknown categories**\n",
        encoding="utf-8",
    )
    try:
        manifest = gen.build_manifest([page])
    finally:
        (gen.DOCS_DIR / "amazon-mystery-task.md").unlink()
    entry = manifest[0]
    assert entry["difficulty"] is None
    assert entry["categories"] is None


def test_build_manifest_bootstraps_a_never_scaffolded_slug_with_none_metadata(tmp_path, monkeypatch):
    monkeypatch.setattr(gen, "DOCS_DIR", tmp_path / "docs" / "amazon")
    monkeypatch.setattr(gen, "PRACTICE_DIR", tmp_path / "practice" / "amazon")
    page = (
        "| Company | OA / Interview Question | Practice | Updated |\n"
        "| :-- | :-- | :-: | :-- |\n"
        "|**Amazon**|[Brand New Task](https://www.fastprep.io/problems/amazon-brand-new-task)"
        "|[![Practice][p]](https://www.fastprep.io/problems/amazon-brand-new-task)"
        "|Sep 19, 2026|\n"
    )

    manifest = gen.build_manifest([page])

    assert [entry["slug"] for entry in manifest] == ["amazon-brand-new-task"]
    assert manifest[0]["difficulty"] is None
    assert manifest[0]["categories"] is None


def test_build_manifest_aborts_when_writeup_missing_but_practice_scaffolds_exist(tmp_path, monkeypatch):
    monkeypatch.setattr(gen, "DOCS_DIR", tmp_path / "docs" / "amazon")
    practice_dir = tmp_path / "practice" / "amazon"
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    (practice_dir / "amazon-half-built").mkdir(parents=True)
    page = (
        "| Company | OA / Interview Question | Practice | Updated |\n"
        "| :-- | :-- | :-: | :-- |\n"
        "|**Amazon**|[Half Built](https://www.fastprep.io/problems/amazon-half-built)"
        "|[![Practice][p]](https://www.fastprep.io/problems/amazon-half-built)"
        "|Sep 19, 2026|\n"
    )

    with pytest.raises(SystemExit, match="write-up not found"):
        gen.build_manifest([page])


def test_load_committed_manifest_aborts_naming_a_slug_missing_parse_status(tmp_path):
    """A committed manifest entry without parse_status aborts, naming it.

    The committed manifest classifies every slug, and an entry missing
    `parse_status` would silently flip the authored-protection predicates
    that read it; the load refuses the manifest and names the offending
    slug instead.
    """
    manifest_path = tmp_path / "amazon_oa_manifest.json"
    entries = [
        {"slug": "amazon-intact", "title": "Intact", "url": "https://x/intact", "parse_status": "parsed-with-cases"},
        {"slug": "amazon-hollow", "title": "Hollow", "url": "https://x/hollow", "parse_status": "parsed-with-cases"},
    ]
    del entries[1]["parse_status"]
    manifest_path.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")

    with pytest.raises(SystemExit, match="amazon-hollow"):
        gen.load_committed_manifest(manifest_path)


def test_load_committed_manifest_aborts_naming_the_index_when_the_slug_is_missing(tmp_path):
    """An entry without a slug is named by index, its only identity left."""
    manifest_path = tmp_path / "amazon_oa_manifest.json"
    entries = [
        {"slug": "amazon-intact", "title": "Intact", "url": "https://x/intact", "parse_status": "parsed-empty-cases"},
        {"title": "Headless", "url": "https://x/headless", "parse_status": "page-unparseable"},
    ]
    manifest_path.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")

    with pytest.raises(SystemExit, match=r"entry #1 is missing slug"):
        gen.load_committed_manifest(manifest_path)


def test_load_committed_manifest_accepts_the_committed_manifest():
    """The committed manifest passes the per-entry validation intact."""
    entries = gen.load_committed_manifest()

    assert entries
    assert all(
        {"slug", "title", "url", "parse_status"} <= set(entry) for entry in entries
    )


@pytest.mark.skipif(
    not all(path.exists() for path in REAL_BANK_PAGES),
    reason="cached bank pages not present (offline fixture-only run)",
)
def test_real_bank_pages_yield_413_unique_amazon_entries_and_410_manifest_entries(tmp_path, monkeypatch):
    texts = [path.read_text(encoding="utf-8") for path in REAL_BANK_PAGES]
    bank_slugs = {
        row["slug"]
        for text in texts
        for row in gen.parse_bank_rows(text)
        if gen.AMAZON_TAG in row["companies"]
    }
    assert len(bank_slugs) == 413
    # build_manifest enriches rows from the write-up headers, and the bank
    # leads the docs tree between syncs; synthetic headers keep the count
    # assertions independent of which scaffolds already exist.
    for slug in bank_slugs:
        (tmp_path / f"{slug}.md").write_text(
            "# [T](https://x)\n\n**Medium** | **NN minutes** | **Array**\n",
            encoding="utf-8",
        )
    monkeypatch.setattr(gen, "DOCS_DIR", tmp_path)
    manifest = gen.build_manifest(texts)
    assert len(manifest) == 410
    slugs = [entry["slug"] for entry in manifest]
    assert not set(slugs) & gen.EXCLUDED_SLUGS
    assert len(set(slugs)) == len(slugs)
    updated = [entry["updated"] for entry in manifest]
    assert updated == sorted(updated, reverse=True)


# ---------------------------------------------------------------------------
# FastPrep page parsing
# ---------------------------------------------------------------------------


def test_extract_problem_record_reassembles_next_flight_payloads():
    problem = gen.extract_problem_record(FASTPREP_PAGE)
    assert problem is not None
    assert problem["id"] == "amazon-maximize-adjacent-difference-with-one-reversal"
    assert problem["title"] == "Maximize Adjacent Difference With One Reversal"
    assert problem["difficulty"] == "hard"
    assert problem["functionName"] == "solve"


def test_extract_problem_record_returns_none_without_flight_data():
    assert gen.extract_problem_record("<html><body>no data</body></html>") is None


# ---------------------------------------------------------------------------
# Example-to-cases conversion (the cases contract)
# ---------------------------------------------------------------------------


def test_cases_from_record_parses_json_representable_example():
    problem = gen.extract_problem_record(FASTPREP_PAGE)
    result = gen.cases_from_record(problem)
    assert result.function_name == "solve"
    assert result.skip_reason is None
    assert result.cases == [
        {"id": "example_1", "args": [[2, 3, 1, 5, 4]], "expected": 10}
    ]


def test_cases_from_record_parses_quoted_string_inputs():
    problem = dict(
        gen.extract_problem_record(FASTPREP_PAGE),
        functionName="minLength",
        examples=[
            {
                "id": 2,
                "inputText": [
                    {"inputName": "s", "inputValue": "'abcabc'", "inputType": "string"},
                ],
                "outputText": "3",
                "outputType": "int",
            }
        ],
    )
    result = gen.cases_from_record(problem)
    assert result.cases == [{"id": "example_2", "args": ["abcabc"], "expected": 3}]


def test_cases_from_record_skips_tree_typed_inputs_naming_the_slug():
    problem = dict(
        gen.extract_problem_record(FASTPREP_PAGE),
        id="amazon-some-tree-problem",
        examples=[
            {
                "id": 1,
                "inputText": [
                    {"inputName": "root", "inputValue": "[1,2,3]", "inputType": "TreeNode"}
                ],
                "outputText": "2",
                "outputType": "int",
            }
        ],
    )
    result = gen.cases_from_record(problem)
    assert result.cases == []
    assert "amazon-some-tree-problem" in result.skip_reason


def test_cases_from_record_skips_unparseable_output_naming_the_slug():
    problem = dict(
        gen.extract_problem_record(FASTPREP_PAGE),
        id="amazon-prose-output",
        examples=[
            {
                "id": 1,
                "inputText": [
                    {"inputName": "n", "inputValue": "5", "inputType": "int"}
                ],
                "outputText": "any valid ordering is accepted",
                "outputType": "string",
            }
        ],
    )
    result = gen.cases_from_record(problem)
    assert result.cases == []
    assert "amazon-prose-output" in result.skip_reason


def test_cases_from_record_skips_design_operation_sequences():
    problem = dict(
        gen.extract_problem_record(FASTPREP_PAGE),
        id="amazon-lru-query-result-cache",
        examples=[
            {
                "id": 1,
                "inputText": [
                    {"inputName": "operations", "inputValue": '["LRUCache","put"]', "inputType": "string[]"},
                    {"inputName": "arguments", "inputValue": "[[2],[1,1]]", "inputType": "integer[][]"},
                ],
                "outputText": "[null,null]",
                "outputType": "long[]",
            }
        ],
    )
    result = gen.cases_from_record(problem)
    assert result.cases == []
    assert "amazon-lru-query-result-cache" in result.skip_reason


def test_cases_from_record_skips_tree_typed_outputs_naming_the_slug():
    problem = dict(
        gen.extract_problem_record(FASTPREP_PAGE),
        id="amazon-tree-output",
        examples=[
            {
                "id": 1,
                "inputText": [
                    {"inputName": "levelOrder", "inputValue": "[3,9,20]", "inputType": "int[]"},
                    {"inputName": "inorder", "inputValue": "[9,3,20]", "inputType": "int[]"},
                ],
                "outputText": "[3,9,20,null,null,15,7]",
                "outputType": "TreeNode",
            }
        ],
    )
    result = gen.cases_from_record(problem)
    assert result.cases == []
    assert "amazon-tree-output" in result.skip_reason
    assert "TreeNode" in result.skip_reason


def test_cases_from_record_rejects_null_anywhere_including_dict_values():
    problem = dict(
        gen.extract_problem_record(FASTPREP_PAGE),
        id="amazon-nullish",
        examples=[
            {
                "id": 1,
                "inputText": [
                    {"inputName": "grid", "inputValue": '{"a": [1, null]}', "inputType": "any"}
                ],
                "outputText": "1",
                "outputType": "int",
            }
        ],
    )
    result = gen.cases_from_record(problem)
    assert result.cases == []
    assert "amazon-nullish" in result.skip_reason


def test_cases_from_record_skips_examples_with_no_inputs():
    problem = dict(
        gen.extract_problem_record(FASTPREP_PAGE),
        id="amazon-no-input-example",
        examples=[
            {"id": 1, "inputText": [], "outputText": "1", "outputType": "int"}
        ],
    )
    result = gen.cases_from_record(problem)
    assert result.cases == []
    assert "amazon-no-input-example" in result.skip_reason


# ---------------------------------------------------------------------------
# Scaffold rendering (structural conventions)
# ---------------------------------------------------------------------------


def test_render_writeup_follows_template_section_order():
    problem = gen.extract_problem_record(FASTPREP_PAGE)
    entry = {"slug": problem["id"], "title": problem["title"], "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    text = gen.render_writeup(entry, problem)
    headings = re.findall(r"^#+ .*$", text, flags=re.M)
    assert headings[0].startswith("# [")
    assert "## Examples" in headings
    assert "## Constraints" in headings
    assert headings.index("## Examples") < headings.index("## Constraints")
    assert "## Solutions" in headings
    assert "main later" in text


def test_render_writeup_uses_placeholder_metadata_when_absent():
    problem = dict(gen.extract_problem_record(FASTPREP_PAGE), difficulty=None, topics=[])
    entry = {"slug": problem["id"], "title": problem["title"], "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    text = gen.render_writeup(entry, problem)
    assert "unknown difficulty" in text


def seed_cache(monkeypatch, cache_dir, *slugs):
    cache_dir.mkdir(parents=True, exist_ok=True)
    for slug in slugs:
        (cache_dir / f"{slug}.html").write_text("<html>cached</html>", encoding="utf-8")
    monkeypatch.setattr(gen, "FASTPREP_CACHE_DIR", cache_dir)


def test_emit_scaffolds_tolerates_unparseable_pages(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs" / "amazon"
    practice_dir = tmp_path / "practice" / "amazon"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    seed_cache(monkeypatch, tmp_path / "cache", "amazon-gone")
    monkeypatch.setattr(
        gen,
        "fetch_problem_page",
        lambda slug, cache_dir=None, delay=True, network=True: "<html>no payload</html>",
    )
    entry = {"slug": "amazon-gone", "title": "Gone", "url": "https://x/gone", "companies": ["Amazon"], "updated": "2026-09-19"}
    stats = gen.emit_scaffolds([entry], fetch=False)
    assert stats["generated"] == 1
    assert stats["parse_failures"] == ["amazon-gone"]
    assert stats["cases_empty"] == 1
    writeup = (docs_dir / "amazon-gone.md").read_text(encoding="utf-8")
    assert "Statement not parseable" in writeup
    test_text = (practice_dir / "amazon-gone" / "test_amazon-gone.py").read_text(encoding="utf-8")
    assert "amazon-gone" in test_text
    assert json.loads((practice_dir / "amazon-gone" / "cases.json").read_text()) == []


def test_fetch_problem_page_without_network_never_leaves_the_cache(tmp_path):
    slug = "amazon-cached"
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    (cache_dir / f"{slug}.html").write_text("<html>cached</html>", encoding="utf-8")
    assert gen.fetch_problem_page(slug, cache_dir=cache_dir, network=False) == "<html>cached</html>"
    missed = gen.fetch_problem_page("amazon-never-fetched", cache_dir=cache_dir, network=False)
    assert "amazon-never-fetched" in missed
    assert not (cache_dir / "amazon-never-fetched.html").exists()


# ---------------------------------------------------------------------------
# Fix-round regressions (review findings R2-R10, S2)
# ---------------------------------------------------------------------------


CHECK_SIMILAR_PASSWORDS_CACHE = Path("/tmp/opencode/fastprep-cache/check-similar-passwords.html")


def test_split_constraints_one_bullet_per_list_item():
    raw = (
        "<ul><li><code>2 &lt;= n &lt;= 1000</code></li>"
        "<li><code>1 &lt;= grid[i][j] &lt;= 100</code></li>"
        "<li>All values are unique.</li></ul>"
    )
    assert gen.split_constraints(raw) == [
        "2 <= n <= 1000",
        "1 <= grid[i][j] <= 100",
        "All values are unique.",
    ]


def test_split_constraints_preserves_superscript_bounds():
    raw = "<ul><li><code>1 &lt;= arr.length &lt;= 10<sup>5</sup></code></li>" "<li><code>1 &lt;= arr[i] &lt;= 10<sup>9</sup></code></li></ul>"
    assert gen.split_constraints(raw) == ["1 <= arr.length <= 10^5", "1 <= arr[i] <= 10^9"]


@pytest.mark.skipif(
    not CHECK_SIMILAR_PASSWORDS_CACHE.exists(),
    reason="cached check-similar-passwords page not present (offline run)",
)
def test_split_constraints_on_real_cached_page_has_no_glued_bounds():
    problem = gen.extract_problem_record(CHECK_SIMILAR_PASSWORDS_CACHE.read_text(encoding="utf-8"))
    glued = gen.split_constraints(problem["constraints"])
    assert len(glued) >= 4
    assert not any(re.search(r"[0-9][A-Za-z]{3,}", item) for item in glued)
    assert any("10^5" in item for item in glued)


def test_html_to_markdown_decodes_all_entities():
    assert gen.html_to_markdown("a &lt; b &gt; c &amp; d &quot;e&quot; f&le;g &#39;h&#39;") == (
        "a < b > c & d \"e\" f≤g 'h'"
    )


def test_html_to_markdown_renders_paragraph_breaks_and_strips_comments():
    assert gen.html_to_markdown("<p>One</p><p>Two</p><!-- x -->") == "One\n\nTwo"


def test_html_to_markdown_separates_a_run_in_heading_from_the_next_block():
    """A heading between blocks never glues to the neighboring prose.

    Shaped like the real bank pages whose statements carry `<h3>` run-in
    headings (`Optimization follow-upAfter` was the rendered join before
    the block-join fix). Inline markup inside one paragraph is legitimate
    emphasis and stays bare.
    """
    fragment = (
        "<p>Solve the base case first.</p>"
        "<h3>Optimization follow-up</h3>"
        "<p>After a correct simple implementation, explain the trade-offs.</p>"
    )

    rendered = gen.html_to_markdown(fragment)

    assert rendered == (
        "Solve the base case first.\n\n"
        "Optimization follow-up\n\n"
        "After a correct simple implementation, explain the trade-offs."
    )


def test_html_to_markdown_puts_each_list_item_on_its_own_line():
    """A `<ul>` of method specs renders one line per `<li>`, not one blob."""
    fragment = (
        "<p>Operations:</p>"
        "<ul><li><code>add_ip</code>: add the address.</li>"
        "<li><code>remove_ip</code>: remove the address.</li></ul>"
    )

    rendered = gen.html_to_markdown(fragment)

    assert "add_ip: add the address.\nremove_ip: remove the address." in rendered
    assert ".remove_ip" not in rendered


def test_html_to_markdown_keeps_a_raw_less_than_a_later_tag_would_eat():
    """A raw `<` in prose that opens no tag survives the tag strips.

    Shaped like the real find-max-value statement (`where 0 ≤ i < n)`
    followed by `<strong>Input Parameters:</strong>`): the generic strip
    used to swallow from the raw `<` through `<strong`'s `>`, deleting
    every clause in between.
    """
    fragment = (
        "<li>For every row i (where 0 ≤ i < n), the count must not surpass limit[i].</li>"
        "<li>If picking exactly x elements is impossible, return -1.</li>"
        "<p><strong>Input Parameters:</strong></p>"
    )

    rendered = gen.html_to_markdown(fragment)

    assert rendered == (
        "For every row i (where 0 ≤ i < n), the count must not surpass limit[i].\n"
        "If picking exactly x elements is impossible, return -1.\n\n"
        "Input Parameters:"
    )


def test_html_to_markdown_strips_only_the_real_tag_next_to_a_raw_less_than():
    """A raw `<` directly before a real tag leaves the tag, keeps the `<`.

    Shaped like the real find-requests-in-queue statement (`while time <
    <code>wait[i]</code>`): the generic strip used to eat `< <code` as one
    tag and render `time wait[i]`.
    """
    rendered = gen.html_to_markdown(
        "<li>It must be processed while time < <code>wait[i]</code>.</li>"
    )

    assert rendered == "It must be processed while time < wait[i]."


def test_html_to_markdown_strips_leading_indentation_from_every_line():
    rendered = gen.html_to_markdown(
        "<div class=\"wrap\"><p>First paragraph</p><p>  Second paragraph\n"
        "        continues on an indented source line</p></div>"
    )
    assert not any(line.startswith("    ") for line in rendered.splitlines())
    assert rendered == "First paragraph\n\nSecond paragraph\ncontinues on an indented source line"


def test_strip_contributor_chrome_removes_leading_special_thanks_line():
    statement = (
        "Special thanks: A special thank you to a lovely, amazing fren who "
        "shared that this question appeared again on September 21, 2026! 💜\n"
        "\n"
        "The manager of the Amazon warehouse has decided to make changes to "
        "the inventory."
    )
    assert gen.strip_contributor_chrome(statement) == (
        "The manager of the Amazon warehouse has decided to make changes to "
        "the inventory."
    )


def test_strip_contributor_chrome_removes_mid_statement_credit():
    statement = (
        "Balance the quality across products.\n"
        "\n"
        "Special thanks: 🍓 1000 thanks to spike for spike's incredible help! 🥑\n"
        "\n"
        "Return the minimum number of moves."
    )
    assert gen.strip_contributor_chrome(statement) == (
        "Balance the quality across products.\n\nReturn the minimum number of moves."
    )


def test_strip_contributor_chrome_keeps_plain_statements_untouched():
    statement = (
        "Given an array of integers, find the longest strictly increasing\n"
        "subsequence and return its length. A contributing factor is the\n"
        "choice of starting element."
    )
    assert gen.strip_contributor_chrome(statement) == statement


def test_render_writeup_strips_contributor_chrome_from_the_statement():
    problem = dict(
        gen.extract_problem_record(FASTPREP_PAGE),
        problemStatement=(
            "<p>Special thanks: Nick contributed this problem.</p>"
            "<p>Amazon would like to enforce a password policy.</p>"
        ),
    )
    entry = {"slug": problem["id"], "title": problem["title"], "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    text = gen.render_writeup(entry, problem)
    assert "Special thanks" not in text
    assert "Amazon would like to enforce a password policy." in text


def test_resolve_statement_recovers_statement_from_rendered_page():
    record = {"problemStatement": "$23"}
    page = (
        "<section><div class=\"fp-statement-content\">"
        "<p>Amazon would like to enforce a password policy.</p>"
        "</div></section>"
    )
    statement = gen.html_to_markdown(gen.resolve_statement(record, page))
    assert "password policy" in statement


def test_resolve_statement_prefers_record_when_plausible():
    record = {"problemStatement": "<p>A full statement well past the plausibility threshold.</p>"}
    assert gen.resolve_statement(record, "<div class=\"fp-statement-content\"><p>other</p></div>") == record["problemStatement"]


def test_resolve_statement_falls_back_to_record_when_no_rendered_section():
    record = {"problemStatement": "$23"}
    assert gen.resolve_statement(record, "<html><body>empty</body></html>") == "$23"


def test_render_writeup_placeholder_when_statement_implausible_and_unrecoverable():
    entry = {"slug": "amazon-shredded", "title": "T", "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    text = gen.render_writeup(entry, {"problemStatement": "$23"}, statement_html="$23")
    assert "Statement not parseable" in text
    assert "$23" not in text


# ---------------------------------------------------------------------------
# Write-up header metadata (difficulty, categories)
# ---------------------------------------------------------------------------


def write_header_fixture(tmp_path, header):
    """One synthetic write-up carrying `header` at the pinned line 3."""
    path = tmp_path / "amazon-header-fixture.md"
    path.write_text(
        "# [Header Fixture](https://x)\n"
        "\n"
        f"{header}\n",
        encoding="utf-8",
    )
    return path


def test_parse_difficulty_line_reads_the_pinned_header():
    path = write_header_fixture(
        tmp_path_factory(), "**Medium** | **NN minutes** | **Array, Greedy, Math**"
    )
    parsed = gen.parse_difficulty_line(path)
    assert parsed == {"difficulty": "Medium", "categories": "Array, Greedy, Math"}


def tmp_path_factory():
    """A throwaway directory for header fixtures outside pytest's tmp_path."""
    import tempfile

    directory = Path(tempfile.mkdtemp())
    return directory


def test_parse_difficulty_line_maps_the_unknown_markers_to_none():
    path = write_header_fixture(
        tmp_path_factory(), "**unknown difficulty** | **NN minutes** | **unknown categories**"
    )
    parsed = gen.parse_difficulty_line(path)
    assert parsed == {"difficulty": None, "categories": None}


def test_parse_difficulty_line_rejects_a_missing_writeup(tmp_path):
    with pytest.raises(SystemExit, match="not found"):
        gen.parse_difficulty_line(tmp_path / "amazon-absent.md")


def test_parse_difficulty_line_rejects_a_headerless_writeup(tmp_path):
    path = write_header_fixture(tmp_path, "no bold groups here")
    with pytest.raises(SystemExit, match="difficulty"):
        gen.parse_difficulty_line(path)


def test_signature_args_suffixes_python_keywords():
    problem = {
        "examples": [
            {
                "inputText": [
                    {"inputName": "class", "inputValue": "1", "inputType": "int"},
                    {"inputName": "size", "inputValue": "2", "inputType": "int"},
                ]
            }
        ]
    }
    assert gen._signature_args(problem) == ", class_, size"


def test_render_writeup_single_comma_separated_input_line():
    problem = dict(
        gen.extract_problem_record(FASTPREP_PAGE),
        examples=[
            {
                "id": 1,
                "inputText": [
                    {"inputName": "values", "inputValue": "[2,3]", "inputType": "int[]"},
                    {"inputName": "k", "inputValue": "1", "inputType": "int"},
                ],
                "outputText": "3",
                "outputType": "int",
            }
        ],
    )
    entry = {"slug": problem["id"], "title": problem["title"], "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    text = gen.render_writeup(entry, problem)
    input_lines = [line for line in text.splitlines() if line.startswith("**Input:**")]
    assert input_lines == ["**Input:** `values = [2,3]`, `k = 1`"]


def test_render_all_covers_every_scaffold_file():
    problem = gen.extract_problem_record(FASTPREP_PAGE)
    entry = {"slug": problem["id"], "title": problem["title"], "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    parsed_cases = gen.cases_from_record(problem)
    rendered = gen.render_all(entry, problem, parsed_cases, problem["problemStatement"])
    assert set(rendered) == {
        gen.DOCS_DIR / f"{problem['id']}.md",
        gen.PRACTICE_DIR / problem["id"] / "solution.py",
        gen.PRACTICE_DIR / problem["id"] / "cases.json",
        gen.PRACTICE_DIR / problem["id"] / f"test_{problem['id']}.py",
    }


def test_render_constraints_falls_back_to_the_override_bullets_when_the_parse_yields_none():
    bullets = gen.render_constraints(
        {"title": "Effort"},
        "amazon-minimize-effort",
        constraints_overrides={"amazon-minimize-effort": ["N/A (FastPrep lists no constraints)"]},
    )
    assert bullets == ["- `N/A (FastPrep lists no constraints)`", ""]


def test_render_constraints_keeps_the_placeholder_when_no_override_addresses_the_slug():
    bullets = gen.render_constraints(
        None,
        "amazon-unlisted",
        constraints_overrides={"amazon-minimize-effort": ["N/A (FastPrep lists no constraints)"]},
    )
    assert bullets == [
        "<!-- Constraints not parseable from FastPrep for amazon-unlisted; fill them in. -->",
        "",
    ]


def test_render_constraints_prefers_the_parsed_constraints_over_the_override():
    bullets = gen.render_constraints(
        {"constraints": "1 <= n <= 50"},
        "amazon-minimize-effort",
        constraints_overrides={"amazon-minimize-effort": ["N/A (FastPrep lists no constraints)"]},
    )
    assert bullets == ["- `1 <= n <= 50`", ""]


def test_load_constraints_overrides_missing_file_is_the_empty_mapping(tmp_path):
    assert gen.load_constraints_overrides(tmp_path / "absent.json") == {}


def test_load_constraints_overrides_rejects_a_non_object_file(tmp_path):
    path = tmp_path / "overrides.json"
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(SystemExit, match="must be a JSON object"):
        gen.load_constraints_overrides(path)


def test_load_constraints_overrides_rejects_a_non_list_entry(tmp_path):
    path = tmp_path / "overrides.json"
    path.write_text(json.dumps({"amazon-minimize-effort": "N/A"}), encoding="utf-8")
    with pytest.raises(SystemExit, match="amazon-minimize-effort"):
        gen.load_constraints_overrides(path)


def test_load_constraints_overrides_rejects_a_non_string_bullet(tmp_path):
    path = tmp_path / "overrides.json"
    path.write_text(json.dumps({"amazon-minimize-effort": ["ok", 3]}), encoding="utf-8")
    with pytest.raises(SystemExit, match="amazon-minimize-effort"):
        gen.load_constraints_overrides(path)


def test_committed_constraints_overrides_reference_manifest_slugs_with_bullet_strings():
    overrides = gen.load_constraints_overrides()
    manifest_slugs = {entry["slug"] for entry in gen.load_committed_manifest()}
    assert overrides, "the committed file exists; an empty object would not fill the two pages"
    for slug, bullets in overrides.items():
        assert slug in manifest_slugs, f"override names unknown slug {slug}"
        assert bullets and all(isinstance(text, str) and text.strip() for text in bullets)


def test_emit_scaffolds_renders_override_constraints_into_a_placeholder_writeup(tmp_path, monkeypatch):
    """The regeneration fills a FastPrep-empty Constraints section from the committed overrides.

    A placeholder write-up whose page parses to a problem with no
    constraints data re-renders with the committed override bullets in its
    Constraints section; the placeholder comment is gone and the practice
    folder takes its normal path (the case data parses).
    """
    docs_dir = tmp_path / "docs" / "amazon"
    practice_dir = tmp_path / "practice" / "amazon"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    seed_cache(monkeypatch, tmp_path / "cache", "amazon-effort")
    overrides_path = tmp_path / "overrides.json"
    overrides_path.write_text(
        json.dumps({"amazon-effort": ["N/A (FastPrep lists no constraints)"]}), encoding="utf-8"
    )
    monkeypatch.setattr(gen, "CONSTRAINTS_OVERRIDES_PATH", overrides_path)
    monkeypatch.setattr(
        gen,
        "fetch_problem_page",
        lambda slug, cache_dir=None, delay=True, network=True: FASTPREP_PAGE,
    )
    entry = {"slug": "amazon-effort", "title": "Effort", "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}

    stats = gen.emit_scaffolds([entry], fetch=False)

    writeup = (docs_dir / "amazon-effort.md").read_text(encoding="utf-8")
    section = writeup.split("## Constraints", 1)[1].split("## Solutions", 1)[0]
    assert "- `N/A (FastPrep lists no constraints)`" in section
    assert "Constraints not parseable from FastPrep" not in writeup
    assert stats["cases_conflicted"] == []
    assert stats["generated"] == 1


def test_emit_scaffolds_skips_uncached_slugs_without_overwriting(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs" / "amazon"
    practice_dir = tmp_path / "practice" / "amazon"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)

    cached_entry = {"slug": "amazon-cached", "title": "Cached", "url": "https://x/cached", "companies": ["Amazon"], "updated": "2026-09-19"}
    uncached_entry = {"slug": "amazon-uncached", "title": "Uncached", "url": "https://x/uncached", "companies": ["Amazon"], "updated": "2026-09-19"}
    good_cases = [{"id": "example_1", "args": [1], "expected": 1}]
    seed_cache(monkeypatch, tmp_path / "cache", "amazon-cached")
    monkeypatch.setattr(
        gen,
        "fetch_problem_page",
        lambda slug, cache_dir=None, delay=True, network=True: FASTPREP_PAGE,
    )
    (practice_dir / "amazon-uncached").mkdir(parents=True)
    (practice_dir / "amazon-uncached" / "cases.json").write_text(json.dumps(good_cases), encoding="utf-8")

    stats = gen.emit_scaffolds([cached_entry, uncached_entry], fetch=False)
    assert stats["skipped_no_cache"] == ["amazon-uncached"]
    assert "parse_status" not in uncached_entry
    assert stats["generated"] == 1
    assert json.loads((practice_dir / "amazon-uncached" / "cases.json").read_text()) == good_cases
    assert json.loads((practice_dir / "amazon-cached" / "cases.json").read_text()) != []


def test_emit_scaffolds_total_cache_loss_preserves_manifest_parse_status(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs" / "amazon"
    practice_dir = tmp_path / "practice" / "amazon"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    monkeypatch.setattr(gen, "FASTPREP_CACHE_DIR", tmp_path / "cache")

    entries = [
        {"slug": "amazon-a", "title": "A", "url": "https://x/a", "companies": ["Amazon"], "updated": "2026-09-19", "parse_status": "parsed-with-cases"},
        {"slug": "amazon-b", "title": "B", "url": "https://x/b", "companies": ["Amazon"], "updated": "2026-09-19", "parse_status": "page-unparseable"},
    ]
    stats = gen.emit_scaffolds(entries, fetch=False)
    assert stats["generated"] == 0
    assert stats["skipped_no_cache"] == ["amazon-a", "amazon-b"]
    assert [entry["parse_status"] for entry in entries] == ["parsed-with-cases", "page-unparseable"]


def test_emit_scaffolds_records_parse_status_on_entries(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs" / "amazon"
    practice_dir = tmp_path / "practice" / "amazon"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    seed_cache(monkeypatch, tmp_path / "cache", "amazon-ok", "amazon-dead")
    monkeypatch.setattr(
        gen,
        "fetch_problem_page",
        lambda slug, cache_dir=None, delay=True, network=True: (
            FASTPREP_PAGE if slug == "amazon-ok" else "<html>no payload</html>"
        ),
    )
    entry = {"slug": "amazon-ok", "title": "Ok", "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    dead_entry = {"slug": "amazon-dead", "title": "Dead", "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    stats = gen.emit_scaffolds([entry, dead_entry], fetch=False)
    assert stats["generated"] == 2
    assert entry["parse_status"] == "parsed-with-cases"
    assert dead_entry["parse_status"] == "page-unparseable"


def test_emit_scaffolds_transient_guard_keeps_committed_cases_when_a_parsed_with_cases_slug_parses_empty_live(tmp_path, monkeypatch):
    """A transiently dead live parse cannot wipe a case-parsed folder.

    A committed `parsed-with-cases` slug whose live parse yields no problem
    and no cases (transient 404, empty parse) keeps its practice files and
    parse_status; the write-up still takes its normal path and the run log
    names the slug under `transient_parse_guard` for a manual decision.
    """
    docs_dir = tmp_path / "docs" / "amazon"
    practice_dir = tmp_path / "practice" / "amazon"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    seed_cache(monkeypatch, tmp_path / "cache", "amazon-ok")
    monkeypatch.setattr(
        gen,
        "fetch_problem_page",
        lambda slug, cache_dir=None, delay=True, network=True: gen.FETCH_FAILED_MARKER_TEMPLATE.format(
            error_code=404, slug=slug
        ),
    )
    problem = gen.extract_problem_record(FASTPREP_PAGE)
    parsed_cases = gen.cases_from_record(problem)
    assert parsed_cases.cases, "fixture must parse to non-empty cases"
    entry = {"slug": "amazon-ok", "title": "Ok", "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19", "parse_status": "parsed-with-cases"}
    statement_html = gen.resolve_statement(problem, FASTPREP_PAGE)
    for path, content in gen.render_all(entry, problem, parsed_cases, statement_html).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    committed_cases = (practice_dir / "amazon-ok" / "cases.json").read_text(encoding="utf-8")
    committed_stub = (practice_dir / "amazon-ok" / "solution.py").read_text(encoding="utf-8")
    committed_test = (practice_dir / "amazon-ok" / "test_amazon-ok.py").read_text(encoding="utf-8")
    stale_placeholder = gen.render_writeup(entry, problem, statement_html)
    (docs_dir / "amazon-ok.md").write_text(stale_placeholder, encoding="utf-8")

    stats = gen.emit_scaffolds([entry], fetch=False)

    slug_dir = practice_dir / "amazon-ok"
    assert stats["transient_parse_guard"] == ["amazon-ok"]
    assert stats["cases_preserved"] == []
    assert stats["cases_conflicted"] == []
    assert (slug_dir / "cases.json").read_text(encoding="utf-8") == committed_cases
    assert (slug_dir / "solution.py").read_text(encoding="utf-8") == committed_stub
    assert (slug_dir / "test_amazon-ok.py").read_text(encoding="utf-8") == committed_test
    assert entry["parse_status"] == "parsed-with-cases"
    assert stats["generated"] == 1
    assert stats["writeups_preserved_dead_page"] == ["amazon-ok"]
    assert (docs_dir / "amazon-ok.md").read_text(encoding="utf-8") == stale_placeholder


def test_emit_scaffolds_held_slug_with_a_dead_page_never_fetches_and_changes_nothing(tmp_path, monkeypatch):
    """A held slug is a no-op even when its upstream page is dead.

    Fetch-new-only sync: a slug present in the committed manifest is never
    fetched, parsed, or re-emitted, so a 404 upstream changes nothing
    locally; the death and guard machinery stays unreached for it.
    """
    docs_dir = tmp_path / "docs" / "amazon"
    practice_dir = tmp_path / "practice" / "amazon"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    entry = {
        "slug": "amazon-gone",
        "title": "Gone",
        "url": "https://x/gone",
        "companies": ["Amazon"],
        "updated": "2026-09-19",
        "parse_status": "page-unparseable",
    }
    write_scaffold_set(tmp_path, entry)
    committed_files = {
        docs_dir / "amazon-gone.md",
        practice_dir / "amazon-gone" / "solution.py",
        practice_dir / "amazon-gone" / "cases.json",
        practice_dir / "amazon-gone" / "test_amazon-gone.py",
    }
    committed = {path: path.read_text(encoding="utf-8") for path in committed_files}
    calls = []

    def spy(slug, cache_dir=None, delay=True, network=True):
        calls.append(slug)
        return gen.FETCH_FAILED_MARKER_TEMPLATE.format(error_code=404, slug=slug)

    monkeypatch.setattr(gen, "fetch_problem_page", spy)

    stats = gen.emit_scaffolds([entry], fetch=True, held_slugs={"amazon-gone"})

    assert calls == []
    for path, text in committed.items():
        assert path.read_text(encoding="utf-8") == text
    assert stats["held_skipped"] == ["amazon-gone"]
    assert stats["generated"] == 0
    assert stats["parse_failures"] == []
    assert stats["transient_parse_guard"] == []
    assert stats["writeups_preserved"] == []
    assert stats["writeups_preserved_dead_page"] == []
    assert stats["death_merge_union"] == []
    assert stats["cases_preserved"] == []
    assert stats["cases_conflicted"] == []
    assert entry["parse_status"] == "page-unparseable"


def authored_writeup(entry: dict) -> str:
    """Render a placeholder write-up for `entry`, then hand-author its body."""
    placeholder = gen.render_writeup(entry, None, "")
    placeholder_comment = (
        f"{gen.WRITEUP_PLACEHOLDER_MARKER} the worked derivation and write-up land\n"
        "     on main later. See ../../leetcode/_TEMPLATE.md for the\n"
        "     expected layout, naming, and ordering conventions. -->"
    )
    authored = placeholder.replace(placeholder_comment, "Hand-authored derivation prose.", 1)
    assert gen.WRITEUP_PLACEHOLDER_MARKER not in authored
    return authored


def test_emit_scaffolds_preserves_an_authored_writeup_and_reports_it(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs" / "amazon"
    practice_dir = tmp_path / "practice" / "amazon"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    seed_cache(monkeypatch, tmp_path / "cache", "amazon-ok")
    monkeypatch.setattr(
        gen,
        "fetch_problem_page",
        lambda slug, cache_dir=None, delay=True, network=True: FASTPREP_PAGE,
    )
    entry = {"slug": "amazon-ok", "title": "Ok", "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    authored = authored_writeup(entry)
    docs_dir.mkdir(parents=True)
    (docs_dir / "amazon-ok.md").write_text(authored, encoding="utf-8")

    stats = gen.emit_scaffolds([entry], fetch=False)

    assert (docs_dir / "amazon-ok.md").read_text(encoding="utf-8") == authored
    assert stats["writeups_preserved"] == ["amazon-ok"]
    assert stats["generated"] == 1


def test_emit_scaffolds_refreshes_a_still_placeholder_writeup(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs" / "amazon"
    practice_dir = tmp_path / "practice" / "amazon"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    seed_cache(monkeypatch, tmp_path / "cache", "amazon-ok")
    monkeypatch.setattr(
        gen,
        "fetch_problem_page",
        lambda slug, cache_dir=None, delay=True, network=True: FASTPREP_PAGE,
    )
    entry = {"slug": "amazon-ok", "title": "Ok", "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    stale_placeholder = gen.render_writeup(entry, None, "")
    docs_dir.mkdir(parents=True)
    (docs_dir / "amazon-ok.md").write_text(stale_placeholder, encoding="utf-8")

    stats = gen.emit_scaffolds([entry], fetch=False)

    problem = gen.extract_problem_record(FASTPREP_PAGE)
    statement_html = gen.resolve_statement(problem, FASTPREP_PAGE)
    fresh_placeholder = gen.render_writeup(entry, problem, statement_html)
    committed = (docs_dir / "amazon-ok.md").read_text(encoding="utf-8")
    assert committed == fresh_placeholder
    assert committed != stale_placeholder
    assert gen.WRITEUP_PLACEHOLDER_MARKER in committed
    assert stats["writeups_preserved"] == []
    assert stats["generated"] == 1


def test_preserve_writeup_on_death_keeps_archived_sections_and_fills_marker_holes():
    """The merge keeps non-marker sections and fills only the marker holes."""
    entry = {"slug": "amazon-gone", "title": "Gone", "url": "https://x/gone"}
    fresh = gen.render_writeup(entry, None, "")
    fresh_constraints_marker = (
        "<!-- Constraints not parseable from FastPrep for amazon-gone; fill them in. -->"
    )
    committed = fresh.replace(
        "<!-- Statement not parseable from FastPrep; fill it in. -->",
        "Archived statement surviving the page death.",
        1,
    ).replace(
        "<!-- Examples not parseable from FastPrep for amazon-gone; fill them in. -->",
        "### Example 1\n\n**Input:** `n = 2`\n\n**Output:** `3`",
        1,
    ).replace(
        fresh_constraints_marker,
        fresh_constraints_marker.replace(" them in.", " them in"),
        1,
    )

    merged = gen.preserve_writeup_on_death(committed, fresh)

    assert "Archived statement surviving the page death." in merged
    assert "### Example 1" in merged
    assert fresh_constraints_marker in merged
    assert fresh_constraints_marker.replace(" them in.", " them in") not in merged
    assert merged.endswith(fresh[fresh.index("## Solutions") :])
    assert merged != fresh


def test_preserve_writeup_on_death_returns_the_fresh_placeholder_for_a_pure_placeholder():
    """A committed write-up with every section still a marker adds nothing."""
    entry = {"slug": "amazon-gone", "title": "Gone", "url": "https://x/gone"}
    fresh = gen.render_writeup(entry, None, "")

    assert gen.preserve_writeup_on_death(fresh, fresh) == fresh


def test_preserve_writeup_on_death_union_keeps_a_committed_only_section():
    """A committed heading outside the fresh template survives the merge.

    The fresh-driven loop fills the template's own sections; a committed
    section whose heading the fresh render lacks is appended after them
    instead of being silently dropped, and a second merge is byte-stable,
    so the carried archive section survives every future run.
    """
    entry = {"slug": "amazon-gone", "title": "Gone", "url": "https://x/gone"}
    fresh = gen.render_writeup(entry, None, "")
    committed_only_section = "## Archived round trace\n\nHand-added trace table.\n\n"
    committed = fresh.rstrip() + "\n\n" + committed_only_section

    merged = gen.preserve_writeup_on_death(committed, fresh)

    assert "## Archived round trace" in merged
    assert "Hand-added trace table." in merged
    assert merged.index("## Archived round trace") > merged.index("## Solutions")
    assert merged == fresh + committed_only_section
    assert gen.preserve_writeup_on_death(merged, fresh) == merged


def test_preserve_writeup_on_death_union_drops_a_committed_only_marker_hole():
    """A committed-only section holding nothing but markers is not kept.

    The union carries content; a marker hole with no fresh counterpart is
    a scaffold remnant, and resurrecting it would pin placeholder noise
    into the archived write-up.
    """
    entry = {"slug": "amazon-gone", "title": "Gone", "url": "https://x/gone"}
    fresh = gen.render_writeup(entry, None, "")
    marker_hole = f"## Retired drill\n\n{gen.WRITEUP_PLACEHOLDER_MARKER} gone. -->\n\n"
    committed = fresh.rstrip() + "\n\n" + marker_hole

    merged = gen.preserve_writeup_on_death(committed, fresh)

    assert "## Retired drill" not in merged
    assert merged == fresh
    assert gen.preserve_writeup_on_death(merged, fresh) == merged


def test_emit_scaffolds_preserves_a_dead_page_writeups_archived_sections(tmp_path, monkeypatch):
    """A dead page must not re-render a committed write-up's archived body.

    The committed write-up still carries the Solutions scaffold marker (so
    it is not authored) but holds the archived statement: emission keeps it
    and reports the slug, and a second pass over the result is byte-stable,
    which is the property that lets a restored write-up survive every
    future wave.
    """
    docs_dir = tmp_path / "docs" / "amazon"
    practice_dir = tmp_path / "practice" / "amazon"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    seed_cache(monkeypatch, tmp_path / "cache", "amazon-gone")
    monkeypatch.setattr(
        gen,
        "fetch_problem_page",
        lambda slug, cache_dir=None, delay=True, network=True: "<html>dead page</html>",
    )
    entry = {"slug": "amazon-gone", "title": "Gone", "url": "https://x/gone", "companies": ["Amazon"], "updated": "2026-09-19"}
    committed = gen.render_writeup(entry, None, "").replace(
        "<!-- Statement not parseable from FastPrep; fill it in. -->",
        "Archived statement surviving the page death.",
        1,
    )
    docs_dir.mkdir(parents=True)
    (docs_dir / "amazon-gone.md").write_text(committed, encoding="utf-8")

    stats = gen.emit_scaffolds([entry], fetch=False)

    preserved = (docs_dir / "amazon-gone.md").read_text(encoding="utf-8")
    assert preserved == committed
    assert "Archived statement surviving the page death." in preserved
    assert stats["writeups_preserved_dead_page"] == ["amazon-gone"]
    assert entry["parse_status"] == "page-unparseable"

    stats = gen.emit_scaffolds([entry], fetch=False)

    assert (docs_dir / "amazon-gone.md").read_text(encoding="utf-8") == committed
    assert stats["writeups_preserved_dead_page"] == ["amazon-gone"]


def test_emit_scaffolds_logs_a_carried_committed_only_section_in_the_death_merge(tmp_path, monkeypatch):
    """The run log names a committed-only section the death merge carries.

    A dead page whose committed write-up holds a heading outside the fresh
    template keeps that section in the archived file, and the emission
    stat names the slug and heading so the union stays auditable.
    """
    docs_dir = tmp_path / "docs" / "amazon"
    practice_dir = tmp_path / "practice" / "amazon"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    seed_cache(monkeypatch, tmp_path / "cache", "amazon-gone")
    monkeypatch.setattr(
        gen,
        "fetch_problem_page",
        lambda slug, cache_dir=None, delay=True, network=True: gen.FETCH_FAILED_MARKER_TEMPLATE.format(
            error_code=404, slug=slug
        ),
    )
    entry = {"slug": "amazon-gone", "title": "Gone", "url": "https://x/gone", "companies": ["Amazon"], "updated": "2026-09-19"}
    committed_only_section = "## Archived round trace\n\nHand-added trace table.\n\n"
    committed = gen.render_writeup(entry, None, "").rstrip() + "\n\n" + committed_only_section
    docs_dir.mkdir(parents=True)
    (docs_dir / "amazon-gone.md").write_text(committed, encoding="utf-8")

    stats = gen.emit_scaffolds([entry], fetch=False)

    preserved = (docs_dir / "amazon-gone.md").read_text(encoding="utf-8")
    assert preserved == gen.render_writeup(entry, None, "") + committed_only_section
    assert "Hand-added trace table." in preserved
    assert stats["writeups_preserved_dead_page"] == ["amazon-gone"]
    assert stats["death_merge_union"] == ["amazon-gone: ## Archived round trace"]
    assert entry["parse_status"] == "page-unparseable"


def test_check_stays_green_for_a_death_preserved_writeup(tmp_path, monkeypatch):
    """The check pins the Solutions block of a death-preserved write-up.

    The archived statement is archive-owned (tampering with it stays green);
    the Solutions scaffold block is generator-owned (drift there fails).
    """
    redirect_check_paths(tmp_path, monkeypatch)
    entry = dict(UNPARSEABLE_ENTRY)
    fresh = gen.render_writeup(entry, None, "")
    committed = fresh.replace(
        "<!-- Statement not parseable from FastPrep; fill it in. -->",
        "Archived statement surviving the page death.",
        1,
    )
    write_scaffold_set(tmp_path, entry)
    (gen.DOCS_DIR / "amazon-gone.md").write_text(committed, encoding="utf-8")
    (gen.DOCS_DIR / "index.md").write_text(gen.render_index([entry]), encoding="utf-8")

    assert gen.check([entry]) == 0

    tampered_solutions = committed.replace(
        f"{gen.WRITEUP_PLACEHOLDER_MARKER} the worked derivation and write-up land",
        f"{gen.WRITEUP_PLACEHOLDER_MARKER} drifted scaffold text",
        1,
    )
    assert gen.WRITEUP_PLACEHOLDER_MARKER in tampered_solutions
    (gen.DOCS_DIR / "amazon-gone.md").write_text(tampered_solutions, encoding="utf-8")
    assert gen.check([entry]) == 1

    tampered_statement = committed.replace(
        "Archived statement surviving the page death.",
        "Hand-edited archive text.",
        1,
    )
    (gen.DOCS_DIR / "amazon-gone.md").write_text(tampered_statement, encoding="utf-8")
    assert gen.check([entry]) == 0


def test_check_stays_green_for_a_death_preserved_writeup_with_a_carried_section(tmp_path, monkeypatch):
    """The check stays green when a dead page carries a committed section.

    The union appends a committed-only section after the Solutions block,
    and the required Solutions-tail fragment remains a substring of the
    carried file, so the carried archive never flags the write-up stale;
    drift in the pinned Solutions block still fails.
    """
    redirect_check_paths(tmp_path, monkeypatch)
    entry = dict(UNPARSEABLE_ENTRY)
    fresh = gen.render_writeup(entry, None, "")
    committed_only_section = "## Archived round trace\n\nHand-added trace table.\n\n"
    committed = (
        fresh.replace(
            "<!-- Statement not parseable from FastPrep; fill it in. -->",
            "Archived statement surviving the page death.",
            1,
        ).rstrip()
        + "\n\n"
        + committed_only_section
    )
    write_scaffold_set(tmp_path, entry)
    (gen.DOCS_DIR / "amazon-gone.md").write_text(committed, encoding="utf-8")
    (gen.DOCS_DIR / "index.md").write_text(gen.render_index([entry]), encoding="utf-8")

    assert gen.check([entry]) == 0

    tampered_solutions = committed.replace(
        f"{gen.WRITEUP_PLACEHOLDER_MARKER} the worked derivation and write-up land",
        f"{gen.WRITEUP_PLACEHOLDER_MARKER} drifted scaffold text",
        1,
    )
    assert gen.WRITEUP_PLACEHOLDER_MARKER in tampered_solutions
    (gen.DOCS_DIR / "amazon-gone.md").write_text(tampered_solutions, encoding="utf-8")
    assert gen.check([entry]) == 1

    dropped_section = committed.replace(committed_only_section, "", 1)
    (gen.DOCS_DIR / "amazon-gone.md").write_text(dropped_section, encoding="utf-8")
    assert gen.check([entry]) == 0


def test_check_pins_an_authored_dead_page_writeups_title_line(tmp_path, monkeypatch):
    """A fully authored write-up on a dead page is pinned on its title line.

    The pin is the manifest-derived `# [Title](url)` line, matching the
    parsed-entry convention: a pin on the committed file's own first line
    is always true and would never catch a write-up retitled away from the
    manifest. The body below the title line stays hand-editable.
    """
    redirect_check_paths(tmp_path, monkeypatch)
    entry = dict(UNPARSEABLE_ENTRY)
    fresh = gen.render_writeup(entry, None, "")
    committed = re.sub(
        rf"{re.escape(gen.WRITEUP_PLACEHOLDER_MARKER)}.*?-->",
        "Fully authored derivation.",
        fresh,
        flags=re.S,
    )
    assert gen.WRITEUP_PLACEHOLDER_MARKER not in committed
    write_scaffold_set(tmp_path, entry)
    (gen.DOCS_DIR / "amazon-gone.md").write_text(committed, encoding="utf-8")
    (gen.DOCS_DIR / "index.md").write_text(gen.render_index([entry]), encoding="utf-8")

    expectation = gen.expected_scaffold_fragments(entry)[gen.DOCS_DIR / "amazon-gone.md"]
    assert expectation.prefix == "# [Gone](https://x/gone)\n"

    assert gen.check([entry]) == 0

    retitled = committed.replace(
        "# [Gone](https://x/gone)", "# [Renamed Problem](https://x/gone)", 1
    )
    (gen.DOCS_DIR / "amazon-gone.md").write_text(retitled, encoding="utf-8")
    assert gen.check([entry]) == 1

    edited_body = committed.replace("Fully authored derivation.", "Rewritten derivation.", 1)
    (gen.DOCS_DIR / "amazon-gone.md").write_text(edited_body, encoding="utf-8")
    assert gen.check([entry]) == 0


def design_operations_problem(slug: str) -> dict:
    """Build a parsed problem whose examples are design-operation sequences.

    Shaped like the real promoted tree/design problems: the page parses,
    but no example converts to `==`-assertable harness cases.
    """
    return dict(
        gen.extract_problem_record(FASTPREP_PAGE),
        id=slug,
        examples=[
            {
                "id": 1,
                "inputText": [
                    {"inputName": "operations", "inputValue": '["LRUCache","put"]', "inputType": "string[]"},
                    {"inputName": "arguments", "inputValue": "[[2],[1,1]]", "inputType": "integer[][]"},
                ],
                "outputText": "[null,null]",
                "outputType": "long[]",
            }
        ],
    )


def seed_authored_cases_folder(practice_dir: Path, slug: str, cases: list) -> None:
    """Write a converted (hand-owned) practice folder for `slug`."""
    slug_dir = practice_dir / slug
    slug_dir.mkdir(parents=True, exist_ok=True)
    (slug_dir / "cases.json").write_text(json.dumps(cases, indent=2) + "\n", encoding="utf-8")
    (slug_dir / "solution.py").write_text("hand-authored stub\n", encoding="utf-8")
    (slug_dir / f"test_{slug}.py").write_text("hand-authored test module\n", encoding="utf-8")


def test_emit_scaffolds_preserves_authored_cases_for_a_parsed_empty_entry(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs" / "amazon"
    practice_dir = tmp_path / "practice" / "amazon"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    seed_cache(monkeypatch, tmp_path / "cache", "amazon-lru-query-result-cache")
    design_problem = design_operations_problem("amazon-lru-query-result-cache")
    monkeypatch.setattr(gen, "extract_problem_record", lambda page_html: design_problem)
    entry = {"slug": "amazon-lru-query-result-cache", "title": "LRU", "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    authored_cases = [{"id": "case_1", "args": [["LRUCache", "put", "get"], [[2], [1, 1], [1]], [None, None, 1]]}]
    seed_authored_cases_folder(practice_dir, "amazon-lru-query-result-cache", authored_cases)

    stats = gen.emit_scaffolds([entry], fetch=False)

    slug_dir = practice_dir / "amazon-lru-query-result-cache"
    assert stats["cases_preserved"] == ["amazon-lru-query-result-cache"]
    assert entry["parse_status"] == "parsed-empty-cases"
    assert json.loads((slug_dir / "cases.json").read_text(encoding="utf-8")) == authored_cases
    assert (slug_dir / "solution.py").read_text(encoding="utf-8") == "hand-authored stub\n"
    assert (slug_dir / "test_amazon-lru-query-result-cache.py").read_text(encoding="utf-8") == "hand-authored test module\n"


def test_emit_scaffolds_refreshes_an_empty_cases_json_folder(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs" / "amazon"
    practice_dir = tmp_path / "practice" / "amazon"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    seed_cache(monkeypatch, tmp_path / "cache", "amazon-lru-query-result-cache")
    design_problem = design_operations_problem("amazon-lru-query-result-cache")
    monkeypatch.setattr(gen, "extract_problem_record", lambda page_html: design_problem)
    entry = {"slug": "amazon-lru-query-result-cache", "title": "LRU", "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    seed_authored_cases_folder(practice_dir, "amazon-lru-query-result-cache", [])

    stats = gen.emit_scaffolds([entry], fetch=False)

    slug_dir = practice_dir / "amazon-lru-query-result-cache"
    assert stats["cases_preserved"] == []
    assert stats["cases_empty"] == 1
    assert json.loads((slug_dir / "cases.json").read_text(encoding="utf-8")) == []
    parsed_cases = gen.cases_from_record(design_problem)
    statement_html = gen.resolve_statement(design_problem, "<html>cached</html>")
    assert (slug_dir / "test_amazon-lru-query-result-cache.py").read_text(encoding="utf-8") == gen.render_test(
        entry, parsed_cases.function_name, parsed_cases.cases, parsed_cases.skip_reason
    )


def test_emit_scaffolds_reports_cases_conflicted_when_upstream_parse_meets_authored_cases(tmp_path, monkeypatch):
    """A live non-empty parse over an authored cases.json is named.

    The overwrite itself stays the default (the upstream refresh is
    authoritative); the stat exists so the wave log names which folders'
    hand-authored cases were replaced instead of passing silently.
    """
    docs_dir = tmp_path / "docs" / "amazon"
    practice_dir = tmp_path / "practice" / "amazon"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    seed_cache(monkeypatch, tmp_path / "cache", "amazon-ok")
    monkeypatch.setattr(
        gen,
        "fetch_problem_page",
        lambda slug, cache_dir=None, delay=True, network=True: FASTPREP_PAGE,
    )
    entry = {"slug": "amazon-ok", "title": "Ok", "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19", "parse_status": "parsed-empty-cases"}
    seed_authored_cases_folder(practice_dir, "amazon-ok", [{"id": "case_1", "args": [["hand"], [1]], "expected": [2]}])

    stats = gen.emit_scaffolds([entry], fetch=False)

    problem = gen.extract_problem_record(FASTPREP_PAGE)
    parsed_cases = gen.cases_from_record(problem)
    assert parsed_cases.cases, "fixture must parse to non-empty cases"
    assert stats["cases_conflicted"] == ["amazon-ok"]
    assert stats["cases_preserved"] == []
    assert entry["parse_status"] == "parsed-with-cases"
    slug_dir = practice_dir / "amazon-ok"
    assert (slug_dir / "cases.json").read_text(encoding="utf-8") == gen.render_cases_file(
        parsed_cases
    )


def test_emit_scaffolds_names_only_hand_owned_cases_in_cases_conflicted(tmp_path, monkeypatch):
    """cases_conflicted fires only for hand-authored case sets meeting upstream cases.

    A `parsed-with-cases` entry's non-empty cases.json is the generator's
    own last render, so a full run over the committed bank (hundreds of
    such folders) must stay silent for them; only a hand-authored case set
    under a non-pwc committed parse_status names a real overwrite.
    """
    docs_dir = tmp_path / "docs" / "amazon"
    practice_dir = tmp_path / "practice" / "amazon"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    seed_cache(monkeypatch, tmp_path / "cache", "amazon-ok", "amazon-authored")
    monkeypatch.setattr(
        gen,
        "fetch_problem_page",
        lambda slug, cache_dir=None, delay=True, network=True: FASTPREP_PAGE,
    )
    problem = gen.extract_problem_record(FASTPREP_PAGE)
    parsed_cases = gen.cases_from_record(problem)
    assert parsed_cases.cases, "fixture must parse to non-empty cases"

    generator_owned_entry = {
        "slug": "amazon-ok",
        "title": "Ok",
        "url": "https://x",
        "companies": ["Amazon"],
        "updated": "2026-09-19",
        "parse_status": "parsed-with-cases",
    }
    statement_html = gen.resolve_statement(problem, FASTPREP_PAGE)
    for path, content in gen.render_all(
        generator_owned_entry, problem, parsed_cases, statement_html
    ).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    authored_entry = {
        "slug": "amazon-authored",
        "title": "Authored",
        "url": "https://x",
        "companies": ["Amazon"],
        "updated": "2026-09-19",
        "parse_status": "parsed-empty-cases",
    }
    seed_authored_cases_folder(
        practice_dir, "amazon-authored", [{"id": "case_1", "args": [["hand"], [1]], "expected": [2]}]
    )

    stats = gen.emit_scaffolds([generator_owned_entry, authored_entry], fetch=False)

    assert stats["cases_conflicted"] == ["amazon-authored"]
    assert stats["cases_preserved"] == []
    assert generator_owned_entry["parse_status"] == "parsed-with-cases"
    assert (practice_dir / "amazon-ok" / "cases.json").read_text(
        encoding="utf-8"
    ) == gen.render_cases_file(parsed_cases)
    assert (practice_dir / "amazon-authored" / "cases.json").read_text(
        encoding="utf-8"
    ) == gen.render_cases_file(parsed_cases)


def test_main_seeds_committed_parse_status_before_emission(tmp_path, monkeypatch, seeded_docs_dir, capsys):
    """A bank-present run classifies folders from the committed manifest.

    The committed manifest classifies, the bank pages enrich: a built
    entry carries no parse_status, so without seeding it from the commit
    before emission, every generator-owned `parsed-with-cases` folder's
    non-empty cases.json counted as hand-authored and the wave log named
    a conflict for it. The seed must leave brand-new slugs (absent from
    the committed manifest) unclassified — emission classifies them from
    the live parse itself.
    """
    monkeypatch.setattr(
        gen,
        "DEFAULT_BANK_PAGES",
        [
            FIXTURES_DIR / "bank_coding.md",
            FIXTURES_DIR / "bank_coding_page_2.md",
            FIXTURES_DIR / "bank_coding_page_3.md",
        ],
    )
    target_slug = gen.extract_problem_record(FASTPREP_PAGE)["id"]
    manifest_path = tmp_path / "amazon_oa_manifest.json"
    manifest_path.write_text(
        json.dumps(
            [
                {
                    "slug": target_slug,
                    "title": "Maximize Adjacent Difference With One Reversal",
                    "url": f"https://www.fastprep.io/problems/{target_slug}",
                    "companies": ["Amazon"],
                    "updated": "2026-09-19",
                    "difficulty": "Hard",
                    "categories": "Array, Greedy, Math",
                    "parse_status": "parsed-with-cases",
                }
            ],
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(gen, "MANIFEST_PATH", manifest_path)
    monkeypatch.setattr(gen, "PRACTICE_DIR", tmp_path / "practice" / "amazon")
    monkeypatch.setattr(
        gen,
        "fetch_problem_page",
        lambda slug, cache_dir=None, delay=True, network=True: FASTPREP_PAGE,
    )
    committed_manifest = json.loads(
        (SCRIPTS_DIR / "amazon_oa_manifest.json").read_text(encoding="utf-8")
    )
    committed_pwc_slug = next(
        entry["slug"]
        for entry in committed_manifest
        if entry.get("parse_status") == "parsed-with-cases"
    )
    shutil.copytree(
        SCRIPTS_DIR.parent / "practice" / "amazon" / committed_pwc_slug,
        gen.PRACTICE_DIR / target_slug,
    )
    copied_cases = json.loads(
        (gen.PRACTICE_DIR / target_slug / "cases.json").read_text(encoding="utf-8")
    )
    assert copied_cases, "fixture premise: the committed folder's cases.json is non-empty"
    mkdocs_path = tmp_path / "mkdocs.yml"
    mkdocs_path.write_text(
        "nav:\n  - Home: index.md\n  - Problems:\n    - Leetcode:\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(gen, "MKTABS_PATH", mkdocs_path)
    seen = {}
    real_emit = gen.emit_scaffolds

    def spy_emit(entries, fetch=True, held_slugs=()):
        seen["entries"] = [dict(entry) for entry in entries]
        return real_emit(entries, fetch=fetch, held_slugs=held_slugs)

    monkeypatch.setattr(gen, "emit_scaffolds", spy_emit)

    assert gen.main([]) == 0

    out = capsys.readouterr().out
    assert "practice cases conflicted" not in out
    seeded = {entry["slug"]: entry for entry in seen["entries"]}
    assert seeded[target_slug]["parse_status"] == "parsed-with-cases"
    brand_new = [slug for slug in seeded if slug != target_slug]
    assert brand_new, "fixture premise: the bank carries slugs the committed manifest omits"
    assert all("parse_status" not in seeded[slug] for slug in brand_new)


def test_check_stays_green_for_an_authored_cases_folder(tmp_path, monkeypatch):
    redirect_check_paths(tmp_path, monkeypatch)
    entry = dict(UNPARSEABLE_ENTRY, slug="amazon-lru-query-result-cache", parse_status="parsed-empty-cases")
    write_scaffold_set(tmp_path, entry)
    (gen.DOCS_DIR / "index.md").write_text(gen.render_index([entry]), encoding="utf-8")
    slug_dir = gen.PRACTICE_DIR / "amazon-lru-query-result-cache"
    authored_cases = [{"id": "case_1", "args": [["LRUCache"]], "expected": [None]}]
    (slug_dir / "cases.json").write_text(json.dumps(authored_cases, indent=2) + "\n", encoding="utf-8")
    (slug_dir / "solution.py").write_text("hand-authored stub\n", encoding="utf-8")
    (slug_dir / "test_amazon-lru-query-result-cache.py").write_text("hand-authored test module\n", encoding="utf-8")

    assert gen.check([entry]) == 0

    (gen.DOCS_DIR / "amazon-lru-query-result-cache.md").write_text(
        "# Different Problem (https://x/other)\n", encoding="utf-8"
    )
    assert gen.check([entry]) == 1


def test_check_exempts_an_authored_cases_folder_on_a_page_unparseable_entry(tmp_path, monkeypatch):
    redirect_check_paths(tmp_path, monkeypatch)
    entry = dict(UNPARSEABLE_ENTRY, slug="amazon-lru-query-result-cache", parse_status="page-unparseable")
    write_scaffold_set(tmp_path, entry)
    (gen.DOCS_DIR / "index.md").write_text(gen.render_index([entry]), encoding="utf-8")
    slug_dir = gen.PRACTICE_DIR / "amazon-lru-query-result-cache"
    authored_cases = [{"id": "case_1", "args": [["LRUCache"]], "expected": [None]}]
    (slug_dir / "cases.json").write_text(json.dumps(authored_cases, indent=2) + "\n", encoding="utf-8")
    (slug_dir / "solution.py").write_text("hand-authored stub\n", encoding="utf-8")
    (slug_dir / "test_amazon-lru-query-result-cache.py").write_text("hand-authored test module\n", encoding="utf-8")

    assert gen.check([entry]) == 0

    (slug_dir / "test_amazon-lru-query-result-cache.py").unlink()
    assert gen.check([entry]) == 1

    (slug_dir / "solution.py").unlink()
    assert gen.check([entry]) == 1

    (slug_dir / "solution.py").write_text("hand-authored stub\n", encoding="utf-8")
    (slug_dir / "test_amazon-lru-query-result-cache.py").write_text("hand-authored test module\n", encoding="utf-8")
    assert gen.check([entry]) == 0


def committed_authored_cases_slugs():
    """List committed slugs whose manifest status is caseless but whose
    cases.json holds authored (non-empty) cases: the folders the generator
    must preserve byte-for-byte."""
    manifest = json.loads((SCRIPTS_DIR / "amazon_oa_manifest.json").read_text(encoding="utf-8"))
    slugs = []
    for entry in manifest:
        cases_path = SCRIPTS_DIR.parent / "practice" / "amazon" / entry["slug"] / "cases.json"
        parsed = gen._json_list_file(cases_path)
        if entry.get("parse_status") != "parsed-with-cases" and parsed:
            slugs.append(entry["slug"])
    return sorted(slugs)


def test_full_run_simulation_leaves_authored_cases_folders_byte_identical(tmp_path, monkeypatch):
    """Run the real emission over the real authored-cases folders.

    The committed folders are copied to a temp DOCS/PRACTICE pair (the real
    tree stays read-only) and every preserved file must come out
    byte-identical. Slugs with a cached FastPrep page simulate the real
    parse; the dead (HTTP 404) slugs get the exact failure marker the
    fetcher produces, so their page-unparseable path runs offline too.
    """
    slugs = committed_authored_cases_slugs()
    assert slugs, "no authored-cases folders committed"
    manifest = json.loads((SCRIPTS_DIR / "amazon_oa_manifest.json").read_text(encoding="utf-8"))
    entries = [dict(entry) for entry in manifest if entry["slug"] in set(slugs)]
    repo_practice = SCRIPTS_DIR.parent / "practice" / "amazon"
    repo_docs = SCRIPTS_DIR.parent / "docs" / "amazon"

    docs_dir = tmp_path / "docs" / "amazon"
    practice_dir = tmp_path / "practice" / "amazon"
    docs_dir.mkdir(parents=True)
    cache_dir = tmp_path / "fastprep-cache"
    cache_dir.mkdir(parents=True)
    for slug in slugs:
        shutil.copytree(repo_practice / slug, practice_dir / slug)
        shutil.copy2(repo_docs / f"{slug}.md", docs_dir / f"{slug}.md")
        cached_page = gen.FASTPREP_CACHE_DIR / f"{slug}.html"
        if cached_page.exists():
            shutil.copy2(cached_page, cache_dir / f"{slug}.html")
        else:
            (cache_dir / f"{slug}.html").write_text(
                gen.FETCH_FAILED_MARKER_TEMPLATE.format(error_code=404, slug=slug),
                encoding="utf-8",
            )
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    monkeypatch.setattr(gen, "FASTPREP_CACHE_DIR", cache_dir)

    stats = gen.emit_scaffolds(entries, fetch=True)

    assert sorted(stats["cases_preserved"]) == slugs
    for slug in slugs:
        repo_slug_dir = repo_practice / slug
        tmp_slug_dir = practice_dir / slug
        repo_files = sorted(path.relative_to(repo_slug_dir) for path in repo_slug_dir.rglob("*") if path.is_file())
        tmp_files = sorted(path.relative_to(tmp_slug_dir) for path in tmp_slug_dir.rglob("*") if path.is_file())
        assert repo_files == tmp_files, slug
        for relative in repo_files:
            assert (repo_slug_dir / relative).read_bytes() == (tmp_slug_dir / relative).read_bytes(), (
                f"{slug}/{relative}"
            )
        assert (repo_docs / f"{slug}.md").read_bytes() == (docs_dir / f"{slug}.md").read_bytes(), slug


def test_main_check_mode_does_not_rewrite_manifest(tmp_path, monkeypatch, seeded_docs_dir):
    monkeypatch.setattr(
        gen,
        "DEFAULT_BANK_PAGES",
        [FIXTURES_DIR / "bank_coding.md", FIXTURES_DIR / "bank_coding_page_2.md"],
    )

    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        '[{"slug": "amazon-x", "title": "X", "url": "https://x", "parse_status": "parsed-with-cases"}]',
        encoding="utf-8",
    )
    monkeypatch.setattr(gen, "MANIFEST_PATH", manifest_path)
    monkeypatch.setattr(gen, "check", lambda manifest: 0)
    writes = []
    real_write = gen.write_manifest

    def spy(manifest):
        writes.append(len(manifest))
        real_write(manifest)

    monkeypatch.setattr(gen, "write_manifest", spy)
    assert gen.main(["--check"]) == 0
    assert writes == []

    monkeypatch.setattr(gen, "write_manifest", real_write)
    assert gen.main(["--manifest-only"]) == 0
    assert (tmp_path / "manifest.json").exists()


def test_write_manifest_fills_parse_status_on_unclassified_entries(tmp_path, monkeypatch):
    """The manifest writer leaves no entry for the strict load to refuse.

    The strict load aborts on any entry missing slug, title, url, or
    parse_status, and the write paths can hold slugs emission never
    classified (beyond --limit, a --no-fetch skip, a --manifest-only
    bootstrap), so the writer itself completes the shape: an unclassified
    entry gains parse_status None and the file reloads cleanly.
    """
    manifest_path = tmp_path / "amazon_oa_manifest.json"
    monkeypatch.setattr(gen, "MANIFEST_PATH", manifest_path)
    classified = {
        "slug": "amazon-intact",
        "title": "Intact",
        "url": "https://x/intact",
        "companies": ["Amazon"],
        "updated": "2026-09-19",
        "difficulty": None,
        "categories": None,
        "parse_status": "parsed-with-cases",
    }
    unclassified = {
        "slug": "amazon-fresh",
        "title": "Fresh",
        "url": "https://x/fresh",
        "companies": ["Amazon"],
        "updated": "2026-09-20",
        "difficulty": None,
        "categories": None,
    }

    gen.write_manifest([classified, unclassified])

    entries = gen.load_committed_manifest(manifest_path)
    assert entries[0]["parse_status"] == "parsed-with-cases"
    assert entries[1]["parse_status"] is None


def test_manifest_only_bootstrap_write_round_trips_through_the_strict_loader(
    tmp_path, monkeypatch, seeded_docs_dir
):
    """A --manifest-only run over grown bank pages stays reloadable.

    The bootstrap flow builds the manifest before any scaffold exists:
    bank slugs absent from the committed manifest reach the write with no
    classification, and the next run's strict load must accept the file
    with those slugs held unclassified for a full run to classify.
    """
    monkeypatch.setattr(
        gen,
        "DEFAULT_BANK_PAGES",
        [FIXTURES_DIR / "bank_coding.md", FIXTURES_DIR / "bank_coding_page_2.md"],
    )
    manifest_path = tmp_path / "amazon_oa_manifest.json"
    manifest_path.write_text(
        json.dumps(
            [
                {
                    "slug": "amazon-inventory-allocation",
                    "title": "Inventory Allocation",
                    "url": "https://www.fastprep.io/problems/amazon-inventory-allocation",
                    "companies": ["Amazon"],
                    "updated": "2026-09-18",
                    "difficulty": None,
                    "categories": None,
                    "parse_status": "parsed-with-cases",
                }
            ],
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(gen, "MANIFEST_PATH", manifest_path)

    assert gen.main(["--manifest-only"]) == 0

    entries = gen.load_committed_manifest(manifest_path)
    status_by_slug = {entry["slug"]: entry["parse_status"] for entry in entries}
    assert status_by_slug["amazon-inventory-allocation"] == "parsed-with-cases"
    assert status_by_slug["amazon-maximize-adjacent-difference-with-one-reversal"] is None
    assert status_by_slug["amazon-lru-query-result-cache"] is None
    assert status_by_slug["amazon-currency-conversion-rate"] is None


def test_limit_run_write_round_trips_through_the_strict_loader(
    tmp_path, monkeypatch, seeded_docs_dir
):
    """A --limit run writes the full manifest, still reloadable.

    Emission classifies only the limited slice while the write persists
    every entry: a bank slug beyond the limit is new to the committed
    manifest, lands unclassified in the file, and the next run's strict
    load must accept it.
    """
    monkeypatch.setattr(
        gen,
        "DEFAULT_BANK_PAGES",
        [FIXTURES_DIR / "bank_coding.md", FIXTURES_DIR / "bank_coding_page_2.md"],
    )
    target_slug = gen.extract_problem_record(FASTPREP_PAGE)["id"]
    manifest_path = tmp_path / "amazon_oa_manifest.json"
    manifest_path.write_text(
        json.dumps(
            [
                {
                    "slug": target_slug,
                    "title": "Maximize Adjacent Difference With One Reversal",
                    "url": f"https://www.fastprep.io/problems/{target_slug}",
                    "companies": ["Amazon"],
                    "updated": "2026-09-19",
                    "difficulty": "Hard",
                    "categories": "Array, Greedy, Math",
                    "parse_status": "parsed-with-cases",
                }
            ],
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(gen, "MANIFEST_PATH", manifest_path)
    monkeypatch.setattr(gen, "PRACTICE_DIR", tmp_path / "practice" / "amazon")
    monkeypatch.setattr(gen, "FASTPREP_CACHE_DIR", tmp_path / "fastprep-cache")
    monkeypatch.setattr(
        gen,
        "fetch_problem_page",
        lambda slug, cache_dir=None, delay=True, network=True: FASTPREP_PAGE,
    )
    mkdocs_path = tmp_path / "mkdocs.yml"
    mkdocs_path.write_text(
        "nav:\n  - Home: index.md\n  - Problems:\n    - Leetcode:\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(gen, "MKTABS_PATH", mkdocs_path)

    assert gen.main(["--limit", "1"]) == 0

    entries = gen.load_committed_manifest(manifest_path)
    status_by_slug = {entry["slug"]: entry["parse_status"] for entry in entries}
    assert status_by_slug[target_slug] == "parsed-with-cases"
    assert status_by_slug["amazon-inventory-allocation"] is None
    assert status_by_slug["amazon-currency-conversion-rate"] is None


def test_no_fetch_run_write_round_trips_through_the_strict_loader(
    tmp_path, monkeypatch, seeded_docs_dir
):
    """A --no-fetch run keeps its unclassified skips reloadable.

    A slug with no cached page is skipped before any classification, yet
    the run still writes the whole manifest: the skipped new slug leaves
    without a parse_status and the next run's strict load must accept it
    while the cache-hit slug carries its live classification.
    """
    monkeypatch.setattr(
        gen,
        "DEFAULT_BANK_PAGES",
        [FIXTURES_DIR / "bank_coding.md", FIXTURES_DIR / "bank_coding_page_2.md"],
    )
    target_slug = gen.extract_problem_record(FASTPREP_PAGE)["id"]
    manifest_path = tmp_path / "amazon_oa_manifest.json"
    manifest_path.write_text(
        json.dumps(
            [
                {
                    "slug": target_slug,
                    "title": "Maximize Adjacent Difference With One Reversal",
                    "url": f"https://www.fastprep.io/problems/{target_slug}",
                    "companies": ["Amazon"],
                    "updated": "2026-09-19",
                    "difficulty": "Hard",
                    "categories": "Array, Greedy, Math",
                    "parse_status": "parsed-with-cases",
                }
            ],
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(gen, "MANIFEST_PATH", manifest_path)
    monkeypatch.setattr(gen, "PRACTICE_DIR", tmp_path / "practice" / "amazon")
    cache_dir = tmp_path / "fastprep-cache"
    cache_dir.mkdir()
    (cache_dir / f"{target_slug}.html").write_text(FASTPREP_PAGE, encoding="utf-8")
    monkeypatch.setattr(gen, "FASTPREP_CACHE_DIR", cache_dir)
    mkdocs_path = tmp_path / "mkdocs.yml"
    mkdocs_path.write_text(
        "nav:\n  - Home: index.md\n  - Problems:\n    - Leetcode:\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(gen, "MKTABS_PATH", mkdocs_path)

    assert gen.main(["--no-fetch"]) == 0

    entries = gen.load_committed_manifest(manifest_path)
    status_by_slug = {entry["slug"]: entry["parse_status"] for entry in entries}
    assert status_by_slug[target_slug] == "parsed-with-cases"
    assert status_by_slug["amazon-inventory-allocation"] is None
    assert status_by_slug["amazon-lru-query-result-cache"] is None


def test_render_test_skips_empty_cases_naming_the_slug():
    entry = {"slug": "amazon-empty-cases", "title": "T", "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    text = gen.render_test(entry, function_name="solve", cases=[], skip_reason="no parseable examples for amazon-empty-cases")
    assert "pytest.skip" in text
    assert "amazon-empty-cases" in text
    assert "len(CASES) == 0" in text


def test_render_test_parametrizes_when_cases_exist():
    entry = {"slug": "amazon-has-cases", "title": "T", "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    cases = [{"id": "example_1", "args": [[1]], "expected": 1}]
    text = gen.render_test(entry, function_name="solve", cases=cases, skip_reason=None)
    assert "@pytest.mark.parametrize" in text
    assert ".solve" in text


def test_render_test_embeds_python_literals_not_json():
    cases = [{"id": "example_1", "args": [[3, 9, 20]], "expected": [3, 9, 20, None, None, 15, 7]}]
    text = gen.render_test(
        entry={"slug": "amazon-tree-out", "title": "T", "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"},
        function_name="solve",
        cases=cases,
        skip_reason=None,
    )
    module = ast.parse(text)
    cases_node = next(
        node.value
        for node in module.body
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "CASES"
    )
    embedded = ast.literal_eval(cases_node)
    assert embedded == cases


# ---------------------------------------------------------------------------
# Scaffold path depth (from practice/amazon/<slug>/ the write-up sits
# three levels up, not two)
# ---------------------------------------------------------------------------


def test_render_solution_stub_links_writeup_at_amazon_depth():
    problem = gen.extract_problem_record(FASTPREP_PAGE)
    entry = {"slug": problem["id"], "title": problem["title"], "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    text = gen.render_solution_stub(entry, problem, gen.cases_from_record(problem))
    assert (
        "Write-up & approaches: ../../../docs/amazon/"
        f"{entry['slug']}.md" in text
    )
    assert "approaches: ../../../docs/problems/" not in text


def test_render_test_links_writeup_at_amazon_depth():
    entry = {"slug": "amazon-depth", "title": "T", "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    text = gen.render_test(entry, function_name="solve", cases=[], skip_reason="no parseable examples for amazon-depth")
    assert (
        "The worked approaches live in ../../../docs/amazon/amazon-depth.md." in text
    )
    assert "live in ../../../docs/problems/" not in text


# ---------------------------------------------------------------------------
# Solution stub case defaults (no-cases fallback, non-degenerate preference)
# ---------------------------------------------------------------------------


def test_render_solution_stub_with_no_cases_guards_the_debug_block_behind_the_guidance():
    entry = {"slug": "amazon-empty", "title": "T", "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    text = gen.render_solution_stub(entry, None, gen.unparsed_page_cases("amazon-empty"), "")
    assert "CASE = None" in text
    assert (
        "no cases authored yet; add cases to cases.json or cases_full.json,"
        " then set CASE to an id" in text
    )
    assert "if CASE is None:" in text
    assert "pick_case(__file__, CASE)" in text
    assert 'CASE = "example_1"' not in text
    ast.parse(text)


def test_no_cases_stub_runs_the_debug_block_once_cases_and_case_are_authored(tmp_path):
    entry = {"slug": "amazon-debug", "title": "T", "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    text = gen.render_solution_stub(entry, None, gen.unparsed_page_cases("amazon-debug"), "")
    (tmp_path / "solution.py").write_text(
        text.replace("CASE = None", 'CASE = "example_1"').replace(
            "raise NotSolved", "return sum(args)"
        ),
        encoding="utf-8",
    )
    (tmp_path / "harness.py").write_text(HARNESS_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "cases.json").write_text("[]", encoding="utf-8")
    (tmp_path / "cases_full.json").write_text(
        json.dumps([{"id": "example_1", "args": [1, 2], "expected": 3}]), encoding="utf-8"
    )

    completed = subprocess.run(
        [sys.executable, "solution.py"], cwd=tmp_path, capture_output=True, text=True, timeout=60
    )

    assert completed.returncode == 0, completed.stderr
    assert "no cases authored yet" not in completed.stdout
    assert "case example_1: args = [1, 2]" in completed.stdout
    assert "expected: 3" in completed.stdout
    assert "got:      3" in completed.stdout


def test_render_solution_stub_default_case_prefers_first_non_degenerate_case():
    entry = {"slug": "amazon-degenerate", "title": "T", "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    cases = [
        {"id": "example_1", "args": [[]], "expected": 0},
        {"id": "example_2", "args": [[3, 1, 2]], "expected": 2},
    ]
    text = gen.render_solution_stub(entry, None, gen.CasesResult("solve", cases, None), "")
    assert 'CASE = "example_2"' in text
    assert 'CASE = "example_1"' not in text


def test_pick_default_case_id_falls_back_to_first_when_every_case_is_degenerate():
    cases = [
        {"id": "example_1", "args": [[]], "expected": 0},
        {"id": "example_2", "args": [""], "expected": 0},
        {"id": "example_3", "args": [0], "expected": 0},
    ]
    assert gen.pick_default_case_id(cases) == "example_1"


def test_pick_default_case_id_returns_none_without_cases():
    assert gen.pick_default_case_id([]) is None


def test_render_index_names_practice_directory_as_inline_code():
    entry = {
        "slug": "amazon-x",
        "title": "X",
        "url": "https://x/x",
        "companies": ["Amazon"],
        "updated": "2026-09-19",
        "difficulty": "Hard",
        "categories": "Array, Greedy, Math",
    }
    text = gen.render_index([entry], difficulty_overrides={})
    assert "`practice/amazon/`" in text
    assert "https://github.com/ThoDHa" not in text
    assert "../../../practice" not in text


def test_render_index_orders_the_catalog_columns():
    entry = {
        "slug": "amazon-x",
        "title": "X",
        "url": "https://x/x",
        "companies": ["Amazon", "Google"],
        "updated": "2026-09-19",
        "difficulty": "Hard",
        "categories": "Array, Greedy, Math",
    }
    text = gen.render_index([entry], difficulty_overrides={})
    header = next(line for line in text.splitlines() if line.startswith("| Problem"))
    assert [name.strip() for name in header.strip("|").split("|")] == [
        "Problem",
        "Difficulty",
        "Category",
        "Time",
        "Companies",
        "Updated",
    ]
    row = next(line for line in text.splitlines() if line.startswith("| [X]"))
    assert row == (
        "| [X](amazon-x.md) | Hard | Array, Greedy, Math"
        " | 40 minutes | Amazon, Google | 2026-09-19 |"
    )


def test_render_index_estimates_time_from_the_difficulty():
    entries = [
        dict(
            INDEX_INDEX_ENTRY,
            slug="amazon-easy",
            title="Easy One",
            difficulty="Easy",
        ),
        dict(
            INDEX_INDEX_ENTRY,
            slug="amazon-medium",
            title="Medium One",
            difficulty="Medium",
        ),
    ]
    text = gen.render_index(entries, difficulty_overrides={})
    rows = [line for line in text.splitlines() if line.startswith("| [")]
    time_cells = [row.strip("|").split("|")[-3].strip() for row in rows]
    assert time_cells == [
        "15 minutes",
        "25 minutes",
    ]


def test_render_index_applies_the_difficulty_overrides():
    entry = dict(INDEX_INDEX_ENTRY, difficulty="Hard")
    text = gen.render_index(
        [entry], difficulty_overrides={entry["slug"]: "Easy"}
    )
    row = next(line for line in text.splitlines() if line.startswith("| [X]"))
    assert "| Easy |" in row
    assert "| 15 minutes |" in row


def test_render_index_dashes_the_unknown_rows():
    entry = dict(INDEX_INDEX_ENTRY, difficulty=None, categories=None)
    text = gen.render_index([entry], difficulty_overrides={})
    row = next(line for line in text.splitlines() if line.startswith("| [X]"))
    assert row.endswith("| - | - | - | Amazon | 2026-09-19 |")


INDEX_INDEX_ENTRY = {
    "slug": "amazon-x",
    "title": "X",
    "url": "https://x/x",
    "companies": ["Amazon"],
    "updated": "2026-09-19",
    "parse_status": "parsed-with-cases",
    "difficulty": "Hard",
    "categories": "Array, Greedy, Math",
}


# ---------------------------------------------------------------------------
# Manifest-driven --check (works with no /tmp scratch, catches stale files)
# ---------------------------------------------------------------------------


def write_scaffold_set(tmp_path, entry):
    """Emit the four scaffolds for `entry` under the tmp dirs."""
    docs_dir = tmp_path / "docs" / "amazon"
    practice_dir = tmp_path / "practice" / "amazon"
    docs_dir.mkdir(parents=True, exist_ok=True)
    slug = entry["slug"]
    (docs_dir / f"{slug}.md").write_text(
        gen.render_writeup(entry, None, ""), encoding="utf-8"
    )
    (practice_dir / slug).mkdir(parents=True, exist_ok=True)
    (practice_dir / slug / "solution.py").write_text(
        gen.render_solution_stub(entry, None, gen.unparsed_page_cases(slug), ""),
        encoding="utf-8",
    )
    (practice_dir / slug / "cases.json").write_text(
        gen.render_cases_file(gen.unparsed_page_cases(slug)), encoding="utf-8"
    )
    (practice_dir / slug / f"test_{slug}.py").write_text(
        gen.render_test(entry, "solve", [], f"FastPrep page for {slug} did not parse"),
        encoding="utf-8",
    )


def redirect_check_paths(tmp_path, monkeypatch):
    """Point every path `check()` reads at the tmp tree."""
    monkeypatch.setattr(gen, "DOCS_DIR", tmp_path / "docs" / "amazon")
    monkeypatch.setattr(gen, "PRACTICE_DIR", tmp_path / "practice" / "amazon")


UNPARSEABLE_ENTRY = {
    "slug": "amazon-gone",
    "title": "Gone",
    "url": "https://x/gone",
    "companies": ["Amazon"],
    "updated": "2026-09-19",
    "parse_status": "page-unparseable",
}


def test_check_green_with_no_tmp_scratch(tmp_path, monkeypatch):
    redirect_check_paths(tmp_path, monkeypatch)
    write_scaffold_set(tmp_path, UNPARSEABLE_ENTRY)
    (gen.DOCS_DIR / "index.md").write_text(gen.render_index([UNPARSEABLE_ENTRY]), encoding="utf-8")
    assert gen.check([UNPARSEABLE_ENTRY]) == 0


def test_check_names_a_genuinely_stale_scaffold(tmp_path, monkeypatch):
    redirect_check_paths(tmp_path, monkeypatch)
    write_scaffold_set(tmp_path, UNPARSEABLE_ENTRY)
    (gen.DOCS_DIR / "index.md").write_text(gen.render_index([UNPARSEABLE_ENTRY]), encoding="utf-8")
    stub = gen.PRACTICE_DIR / "amazon-gone" / "solution.py"
    stub.write_text(
        gen.render_solution_stub(UNPARSEABLE_ENTRY, None, gen.unparsed_page_cases("amazon-gone"), "")
        .replace("NotSolved", "NotSolvedV2"),
        encoding="utf-8",
    )
    assert gen.check([UNPARSEABLE_ENTRY]) == 1
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        gen.check([UNPARSEABLE_ENTRY])
    assert "practice/amazon/amazon-gone/solution.py" in captured.getvalue()


def test_check_flags_missing_scaffolds_and_missing_cases_json(tmp_path, monkeypatch):
    redirect_check_paths(tmp_path, monkeypatch)
    write_scaffold_set(tmp_path, UNPARSEABLE_ENTRY)
    (gen.DOCS_DIR / "index.md").write_text(gen.render_index([UNPARSEABLE_ENTRY]), encoding="utf-8")
    (gen.PRACTICE_DIR / "amazon-gone" / "cases.json").unlink()
    entry = dict(UNPARSEABLE_ENTRY, slug="amazon-missing", title="Missing", url="https://x/m")
    assert gen.check([UNPARSEABLE_ENTRY, entry]) == 1


def test_check_flags_malformed_cases_json(tmp_path, monkeypatch):
    redirect_check_paths(tmp_path, monkeypatch)
    write_scaffold_set(tmp_path, UNPARSEABLE_ENTRY)
    (gen.DOCS_DIR / "index.md").write_text(gen.render_index([UNPARSEABLE_ENTRY]), encoding="utf-8")
    (gen.PRACTICE_DIR / "amazon-gone" / "cases.json").write_text("{not json", encoding="utf-8")
    assert gen.check([UNPARSEABLE_ENTRY]) == 1


def test_check_parsed_entry_requires_generator_owned_fragments(tmp_path, monkeypatch):
    redirect_check_paths(tmp_path, monkeypatch)
    entry = dict(UNPARSEABLE_ENTRY, slug="amazon-parsed", parse_status="parsed-with-cases")
    write_scaffold_set(tmp_path, entry)
    (gen.DOCS_DIR / "index.md").write_text(gen.render_index([entry]), encoding="utf-8")
    assert gen.check([entry]) == 0
    (gen.DOCS_DIR / "amazon-parsed.md").write_text(
        "# Different Problem (https://x/other)\n", encoding="utf-8"
    )
    assert gen.check([entry]) == 1


def test_expected_parsed_entry_fragments_stay_prefixes_of_the_renderer_output():
    entry = dict(UNPARSEABLE_ENTRY, slug="amazon-parsed", parse_status="parsed-with-cases")
    expectations = gen.expected_scaffold_fragments(entry)
    rendered = gen.render_all(entry, None, gen.unparsed_page_cases(entry["slug"]), "")
    for path, expectation in expectations.items():
        assert rendered[path].startswith(expectation.prefix), path
        for fragment in expectation.required:
            assert fragment in rendered[path], path


def test_check_catches_a_retired_command_path_in_a_parsed_stub(tmp_path, monkeypatch):
    redirect_check_paths(tmp_path, monkeypatch)
    entry = dict(UNPARSEABLE_ENTRY, slug="amazon-parsed", parse_status="parsed-with-cases")
    write_scaffold_set(tmp_path, entry)
    (gen.DOCS_DIR / "index.md").write_text(gen.render_index([entry]), encoding="utf-8")
    stub = gen.PRACTICE_DIR / "amazon-parsed" / "solution.py"
    text = stub.read_text(encoding="utf-8")
    stub.write_text(text.replace("uv run python amazon/amazon-parsed/solution.py", "uv run python amazon_oa/amazon-parsed/solution.py"), encoding="utf-8")
    assert gen.check([entry]) == 1


def test_main_check_falls_back_to_committed_manifest_without_bank_pages(tmp_path, monkeypatch):
    monkeypatch.setattr(gen, "DEFAULT_BANK_PAGES", [tmp_path / "absent" / "coding.md"])
    manifest_path = tmp_path / "amazon_oa_manifest.json"
    manifest_path.write_text(
        json.dumps([UNPARSEABLE_ENTRY], indent=2) + "\n", encoding="utf-8"
    )
    monkeypatch.setattr(gen, "MANIFEST_PATH", manifest_path)
    redirect_check_paths(tmp_path, monkeypatch)
    write_scaffold_set(tmp_path, UNPARSEABLE_ENTRY)
    (gen.DOCS_DIR / "index.md").write_text(gen.render_index([UNPARSEABLE_ENTRY]), encoding="utf-8")
    seen = {}

    def spy(manifest):
        seen["entries"] = manifest
        return 0

    monkeypatch.setattr(gen, "check", spy)
    assert gen.main(["--check"]) == 0
    assert seen["entries"] == [UNPARSEABLE_ENTRY]


def test_main_with_explicit_missing_bank_page_errors():
    with pytest.raises(SystemExit, match="bank page not found"):
        gen.main(["--bank-page", "/nonexistent/bank.md", "--check"])


SYNC_BANK_PAGE = """# Coding OA bank, sync fixture (trimmed)

| Company | OA / Interview Question | Practice | Updated |
| :-- | :-- | :-: | :-- |
|**Amazon**|[Brand New Problem](https://www.fastprep.io/problems/amazon-brand-new-problem)|[![Practice][p]](https://www.fastprep.io/problems/amazon-brand-new-problem)|🔥 Nov 1, 2026|
|**Amazon**|[Held Old](https://www.fastprep.io/problems/amazon-held-old)|[![Practice][p]](https://www.fastprep.io/problems/amazon-held-old)|🔥 Nov 2, 2026|
"""

HELD_ENTRY = {
    "slug": "amazon-held-old",
    "title": "Held Old",
    "url": "https://www.fastprep.io/problems/amazon-held-old",
    "companies": ["Amazon"],
    "updated": "2026-09-18",
    "parse_status": "page-unparseable",
}


def redirect_sync_run(tmp_path, monkeypatch, bank_text, manifest_entries):
    """Point every path an online `main()` run reads and writes at tmp_path."""
    bank_path = tmp_path / "coding.md"
    bank_path.write_text(bank_text, encoding="utf-8")
    monkeypatch.setattr(gen, "DEFAULT_BANK_PAGES", [bank_path])
    manifest_path = tmp_path / "amazon_oa_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest_entries, indent=2) + "\n", encoding="utf-8"
    )
    monkeypatch.setattr(gen, "MANIFEST_PATH", manifest_path)
    monkeypatch.setattr(gen, "FASTPREP_CACHE_DIR", tmp_path / "cache")
    mkdocs_path = tmp_path / "mkdocs.yml"
    mkdocs_path.write_text(
        'nav:\n  - Home: index.md\n  - Problems:\n    - Leetcode:\n'
        '      - "Amazon OA": amazon/index.md\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(gen, "MKTABS_PATH", mkdocs_path)
    redirect_check_paths(tmp_path, monkeypatch)
    return manifest_path


def scaffold_texts(slug):
    """Snapshot the four scaffold files of one slug for untouched checks."""
    return {
        gen.DOCS_DIR / f"{slug}.md": (gen.DOCS_DIR / f"{slug}.md").read_text(encoding="utf-8"),
        gen.PRACTICE_DIR / slug / "solution.py": (gen.PRACTICE_DIR / slug / "solution.py").read_text(encoding="utf-8"),
        gen.PRACTICE_DIR / slug / "cases.json": (gen.PRACTICE_DIR / slug / "cases.json").read_text(encoding="utf-8"),
        gen.PRACTICE_DIR / slug / f"test_{slug}.py": (gen.PRACTICE_DIR / slug / f"test_{slug}.py").read_text(encoding="utf-8"),
    }


def test_main_sync_fetches_and_scaffolds_a_new_slug_exactly_as_before(tmp_path, monkeypatch, capsys):
    """Fetch-new-only sync scaffolds a slug absent from the committed manifest."""
    manifest_path = redirect_sync_run(tmp_path, monkeypatch, SYNC_BANK_PAGE, [HELD_ENTRY])
    write_scaffold_set(tmp_path, HELD_ENTRY)
    held_committed = scaffold_texts(HELD_ENTRY["slug"])
    calls = []

    def spy(slug, cache_dir=None, delay=True, network=True):
        calls.append(slug)
        return FASTPREP_PAGE

    monkeypatch.setattr(gen, "fetch_problem_page", spy)

    assert gen.main([]) == 0

    assert calls == ["amazon-brand-new-problem"]
    assert (gen.DOCS_DIR / "amazon-brand-new-problem.md").exists()
    assert (gen.PRACTICE_DIR / "amazon-brand-new-problem" / "solution.py").exists()
    cases = json.loads(
        (gen.PRACTICE_DIR / "amazon-brand-new-problem" / "cases.json").read_text(encoding="utf-8")
    )
    assert cases
    out = capsys.readouterr().out
    assert "scaffolds: 1 generated" in out
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_slug = {entry["slug"]: entry for entry in manifest}
    assert by_slug["amazon-brand-new-problem"]["parse_status"] == "parsed-with-cases"
    for path, text in held_committed.items():
        assert path.read_text(encoding="utf-8") == text


def test_main_sync_fetches_and_classifies_a_null_status_manifest_slug(tmp_path, monkeypatch, capsys):
    """A committed null parse_status does not hold: the sync heals it.

    A --manifest-only bootstrap, a --limit overshoot, or a --no-fetch
    skip can write a slug into the manifest before any classification.
    Such an entry stays fetchable: the next bank-available run fetches
    its live page, scaffolds it, and classifies it, while genuinely
    classified committed slugs stay held and untouched.
    """
    null_status_entry = {
        "slug": "amazon-brand-new-problem",
        "title": "Brand New Problem",
        "url": "https://www.fastprep.io/problems/amazon-brand-new-problem",
        "companies": ["Amazon"],
        "updated": "2026-09-20",
        "difficulty": None,
        "categories": None,
        "parse_status": None,
    }
    manifest_path = redirect_sync_run(
        tmp_path, monkeypatch, SYNC_BANK_PAGE, [HELD_ENTRY, null_status_entry]
    )
    write_scaffold_set(tmp_path, HELD_ENTRY)
    held_committed = scaffold_texts(HELD_ENTRY["slug"])
    calls = []

    def spy(slug, cache_dir=None, delay=True, network=True):
        calls.append(slug)
        return FASTPREP_PAGE

    monkeypatch.setattr(gen, "fetch_problem_page", spy)

    assert gen.main([]) == 0

    assert calls == ["amazon-brand-new-problem"]
    assert (gen.DOCS_DIR / "amazon-brand-new-problem.md").exists()
    cases = json.loads(
        (gen.PRACTICE_DIR / "amazon-brand-new-problem" / "cases.json").read_text(encoding="utf-8")
    )
    assert cases
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_slug = {entry["slug"]: entry for entry in manifest}
    assert by_slug["amazon-brand-new-problem"]["parse_status"] == "parsed-with-cases"
    assert by_slug["amazon-held-old"]["parse_status"] == "page-unparseable"
    for path, text in held_committed.items():
        assert path.read_text(encoding="utf-8") == text
    out = capsys.readouterr().out
    assert "held (committed copies authoritative, untouched): 1" in out


def test_main_sync_refreshes_a_held_slug_bank_row_without_fastprep_fetches(tmp_path, monkeypatch, capsys):
    """A held slug's manifest row refreshes from the bank row alone.

    The bank row carries the row data (title, companies, dates), so a date
    change lands in the manifest with zero FastPrep fetches and the held
    scaffolds stay byte-identical.
    """
    bank_text = (
        "# Coding OA bank, held-only sync fixture (trimmed)\n\n"
        "| Company | OA / Interview Question | Practice | Updated |\n"
        "| :-- | :-- | :-: | :-- |\n"
        "|**Amazon**|[Held Old](https://www.fastprep.io/problems/amazon-held-old)"
        "|[![Practice][p]](https://www.fastprep.io/problems/amazon-held-old)"
        "|🔥 Nov 2, 2026|\n"
    )
    manifest_path = redirect_sync_run(tmp_path, monkeypatch, bank_text, [HELD_ENTRY])
    write_scaffold_set(tmp_path, HELD_ENTRY)
    held_committed = scaffold_texts(HELD_ENTRY["slug"])
    calls = []

    def spy(slug, cache_dir=None, delay=True, network=True):
        calls.append(slug)
        return FASTPREP_PAGE

    monkeypatch.setattr(gen, "fetch_problem_page", spy)

    assert gen.main([]) == 0

    assert calls == []
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest == [
        {
            "slug": "amazon-held-old",
            "title": "Held Old",
            "url": "https://www.fastprep.io/problems/amazon-held-old",
            "companies": ["Amazon"],
            "updated": "2026-11-02",
            "difficulty": None,
            "categories": None,
            "parse_status": "page-unparseable",
        }
    ]
    for path, text in held_committed.items():
        assert path.read_text(encoding="utf-8") == text
    out = capsys.readouterr().out
    assert "held (committed copies authoritative, untouched): 1" in out


def test_main_without_bank_pages_leaves_held_slugs_untouched_as_no_ops(tmp_path, monkeypatch, capsys):
    """Offline fallback: every committed slug is held and emission is a no-op.

    The bank pages are absent, so the manifest is the committed hold list;
    the run refreshes nothing, fetches nothing, and keeps every scaffold
    byte-identical.
    """
    monkeypatch.setattr(gen, "DEFAULT_BANK_PAGES", [tmp_path / "absent" / "coding.md"])
    manifest_path = tmp_path / "amazon_oa_manifest.json"
    manifest_path.write_text(
        json.dumps([UNPARSEABLE_ENTRY], indent=2) + "\n", encoding="utf-8"
    )
    monkeypatch.setattr(gen, "MANIFEST_PATH", manifest_path)
    monkeypatch.setattr(gen, "FASTPREP_CACHE_DIR", tmp_path / "empty-cache")
    mkdocs_path = tmp_path / "mkdocs.yml"
    mkdocs_path.write_text(
        'nav:\n  - Home: index.md\n  - Problems:\n    - Leetcode:\n'
        '      - "Amazon OA": amazon/index.md\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(gen, "MKTABS_PATH", mkdocs_path)
    redirect_check_paths(tmp_path, monkeypatch)
    write_scaffold_set(tmp_path, UNPARSEABLE_ENTRY)
    committed = scaffold_texts(UNPARSEABLE_ENTRY["slug"])
    committed_manifest = manifest_path.read_text(encoding="utf-8")
    calls = []

    def spy(slug, cache_dir=None, delay=True, network=True):
        calls.append(slug)
        return FASTPREP_PAGE

    monkeypatch.setattr(gen, "fetch_problem_page", spy)

    assert gen.main([]) == 0

    assert calls == []
    for path, text in committed.items():
        assert path.read_text(encoding="utf-8") == text
    assert manifest_path.read_text(encoding="utf-8") == committed_manifest
    out = capsys.readouterr().out
    assert "held (committed copies authoritative, untouched): 1" in out


def test_main_no_fetch_regenerates_a_new_slug_from_cache_and_skips_an_uncached_one(tmp_path, monkeypatch, capsys):
    """--no-fetch stays the offline safety net for new slugs only.

    A new slug with a cached page scaffolds from the cache without network;
    a new slug without one is skipped with its scaffolds absent, and the
    held slug is untouched throughout.
    """
    bank_text = SYNC_BANK_PAGE.replace(
        "[Held Old](https://www.fastprep.io/problems/amazon-held-old)",
        "[Uncached New](https://www.fastprep.io/problems/amazon-uncached-new)",
    )
    redirect_sync_run(tmp_path, monkeypatch, bank_text, [HELD_ENTRY])
    write_scaffold_set(tmp_path, HELD_ENTRY)
    held_committed = scaffold_texts(HELD_ENTRY["slug"])
    seed_cache(monkeypatch, tmp_path / "cache", "amazon-brand-new-problem")
    calls = []

    def spy(slug, cache_dir=None, delay=True, network=True):
        calls.append((slug, network))
        return "<html>cached</html>"

    monkeypatch.setattr(gen, "fetch_problem_page", spy)

    assert gen.main(["--no-fetch"]) == 0

    assert calls == [("amazon-brand-new-problem", False)]
    assert (gen.DOCS_DIR / "amazon-brand-new-problem.md").exists()
    assert not (gen.DOCS_DIR / "amazon-uncached-new.md").exists()
    for path, text in held_committed.items():
        assert path.read_text(encoding="utf-8") == text
    out = capsys.readouterr().out
    assert "amazon-uncached-new" in out
    assert "skipped" in out
