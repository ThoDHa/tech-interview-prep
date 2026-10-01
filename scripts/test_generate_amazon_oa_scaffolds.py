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
from pathlib import Path

import pytest

import generate_amazon_oa_scaffolds as gen

SCRIPTS_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = SCRIPTS_DIR / "fixtures"

BANK_PAGE = (FIXTURES_DIR / "bank_coding.md").read_text(encoding="utf-8")
BANK_PAGE_2 = (FIXTURES_DIR / "bank_coding_page_2.md").read_text(encoding="utf-8")
FASTPREP_PAGE = (FIXTURES_DIR / "fastprep_problem.html").read_text(encoding="utf-8")

REAL_BANK_PAGES = [
    Path("/tmp/opencode/tech-oa/coding.md"),
    Path("/tmp/opencode/tech-oa/coding-page-2.md"),
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


def test_build_manifest_keeps_only_amazon_tagged_rows():
    manifest = gen.build_manifest([BANK_PAGE, BANK_PAGE_2])
    assert {entry["slug"] for entry in manifest} == {
        "amazon-maximize-adjacent-difference-with-one-reversal",
        "amazon-inventory-allocation",
        "amazon-lru-query-result-cache",
        "amazon-currency-conversion-rate",
    }


def test_build_manifest_dedups_by_slug_keeping_most_recent():
    manifest = gen.build_manifest([BANK_PAGE, BANK_PAGE_2])
    entries = [e for e in manifest if e["slug"].endswith("one-reversal")]
    assert len(entries) == 1
    assert entries[0]["updated"] == "2026-09-19"


def test_build_manifest_sorts_most_recent_first():
    manifest = gen.build_manifest([BANK_PAGE, BANK_PAGE_2])
    updated = [entry["updated"] for entry in manifest]
    assert updated == sorted(updated, reverse=True)


def test_build_manifest_breaks_date_ties_by_slug_ascending():
    page = (
        "| Company | OA / Interview Question | Practice | Updated |\n"
        "| :-- | :-- | :-: | :-- |\n"
        "|**Amazon**|[Zeta Task](https://www.fastprep.io/problems/amazon-zeta-task)|[![Practice][p]](https://www.fastprep.io/problems/amazon-zeta-task)|Sep 19, 2026|\n"
        "|**Amazon**|[Alpha Task](https://www.fastprep.io/problems/amazon-alpha-task)|[![Practice][p]](https://www.fastprep.io/problems/amazon-alpha-task)|Sep 19, 2026|\n"
    )
    manifest = gen.build_manifest([page])
    assert [entry["slug"] for entry in manifest] == [
        "amazon-alpha-task",
        "amazon-zeta-task",
    ]


def test_build_manifest_entries_carry_required_fields():
    manifest = gen.build_manifest([BANK_PAGE])
    entry = next(e for e in manifest if e["slug"] == "amazon-lru-query-result-cache")
    assert entry["title"] == "LRU Cache for Query Results"
    assert entry["companies"] == ["Amazon", "Google"]
    assert entry["updated"] == "2026-09-17"
    assert entry["url"].startswith("https://www.fastprep.io/problems/")


@pytest.mark.skipif(
    not all(path.exists() for path in REAL_BANK_PAGES),
    reason="cached bank pages not present (offline fixture-only run)",
)
def test_real_bank_pages_yield_350_unique_amazon_entries():
    texts = [path.read_text(encoding="utf-8") for path in REAL_BANK_PAGES]
    manifest = gen.build_manifest(texts)
    assert len(manifest) == 350
    slugs = [entry["slug"] for entry in manifest]
    assert len(set(slugs)) == 350
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
    assert "solutions branch" in text


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
    docs_dir = tmp_path / "docs" / "problems" / "amazon_oa"
    practice_dir = tmp_path / "practice" / "amazon_oa"
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


def test_html_to_markdown_strips_leading_indentation_from_every_line():
    rendered = gen.html_to_markdown(
        "<div class=\"wrap\"><p>First paragraph</p><p>  Second paragraph\n"
        "        continues on an indented source line</p></div>"
    )
    assert not any(line.startswith("    ") for line in rendered.splitlines())
    assert rendered == "First paragraph\n\nSecond paragraph\ncontinues on an indented source line"


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


def test_emit_scaffolds_skips_uncached_slugs_without_overwriting(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs" / "problems" / "amazon_oa"
    practice_dir = tmp_path / "practice" / "amazon_oa"
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
    docs_dir = tmp_path / "docs" / "problems" / "amazon_oa"
    practice_dir = tmp_path / "practice" / "amazon_oa"
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
    docs_dir = tmp_path / "docs" / "problems" / "amazon_oa"
    practice_dir = tmp_path / "practice" / "amazon_oa"
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


def test_main_check_mode_does_not_rewrite_manifest(tmp_path, monkeypatch):
    monkeypatch.setattr(
        gen,
        "DEFAULT_BANK_PAGES",
        [FIXTURES_DIR / "bank_coding.md", FIXTURES_DIR / "bank_coding_page_2.md"],
    )
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text('[{"slug": "amazon-x", "parse_status": "parsed-with-cases"}]', encoding="utf-8")
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
# Scaffold path depth (from practice/amazon_oa/<slug>/ the write-up sits
# three levels up, not two)
# ---------------------------------------------------------------------------


def test_render_solution_stub_links_writeup_at_amazon_depth():
    problem = gen.extract_problem_record(FASTPREP_PAGE)
    entry = {"slug": problem["id"], "title": problem["title"], "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    text = gen.render_solution_stub(entry, problem, gen.cases_from_record(problem))
    assert (
        "Write-up & approaches: ../../../docs/problems/amazon_oa/"
        f"{entry['slug']}.md" in text
    )
    assert "approaches: ../../docs/" not in text


def test_render_test_links_writeup_at_amazon_depth():
    entry = {"slug": "amazon-depth", "title": "T", "url": "https://x", "companies": ["Amazon"], "updated": "2026-09-19"}
    text = gen.render_test(entry, function_name="solve", cases=[], skip_reason="no parseable examples for amazon-depth")
    assert (
        "The worked approaches live in ../../../docs/problems/amazon_oa/amazon-depth.md." in text
    )
    assert "live in ../../docs/" not in text


def test_render_index_links_practice_directory_with_absolute_repo_url():
    text = gen.render_index([{"slug": "amazon-x", "title": "X", "url": "https://x/x", "companies": ["Amazon"], "updated": "2026-09-19"}])
    assert (
        "[`practice/amazon_oa/`](https://github.com/ThoDHa/tech-interview-prep/tree/main/practice/amazon_oa/)"
        in text
    )
    assert "../../../practice" not in text


# ---------------------------------------------------------------------------
# Manifest-driven --check (works with no /tmp scratch, catches stale files)
# ---------------------------------------------------------------------------


def write_scaffold_set(tmp_path, entry):
    """Emit the four scaffolds for `entry` under the tmp dirs."""
    docs_dir = tmp_path / "docs" / "problems" / "amazon_oa"
    practice_dir = tmp_path / "practice" / "amazon_oa"
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
    monkeypatch.setattr(gen, "DOCS_DIR", tmp_path / "docs" / "problems" / "amazon_oa")
    monkeypatch.setattr(gen, "PRACTICE_DIR", tmp_path / "practice" / "amazon_oa")


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
    assert "practice/amazon_oa/amazon-gone/solution.py" in captured.getvalue()


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
    fragments = gen.expected_scaffold_fragments(entry)
    rendered = gen.render_all(entry, None, gen.unparsed_page_cases(entry["slug"]), "")
    for path, fragment in fragments.items():
        assert rendered[path].startswith(fragment), path


def test_main_warns_when_bank_pages_are_absent_and_slugs_are_skipped(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(gen, "DEFAULT_BANK_PAGES", [tmp_path / "absent" / "coding.md"])
    manifest_path = tmp_path / "amazon_oa_manifest.json"
    manifest_path.write_text(
        json.dumps([UNPARSEABLE_ENTRY], indent=2) + "\n", encoding="utf-8"
    )
    monkeypatch.setattr(gen, "MANIFEST_PATH", manifest_path)
    monkeypatch.setattr(gen, "FASTPREP_CACHE_DIR", tmp_path / "empty-cache")
    mkdocs_path = tmp_path / "mkdocs.yml"
    mkdocs_path.write_text(
        'nav:\n  - Home: index.md\n  - Problems:\n    - "Amazon OA":'
        " problems/amazon_oa/index.md\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(gen, "MKTABS_PATH", mkdocs_path)
    redirect_check_paths(tmp_path, monkeypatch)
    assert gen.main([]) == 0
    out = capsys.readouterr().out
    assert "amazon-gone" in out
    assert "warning:" in out


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
