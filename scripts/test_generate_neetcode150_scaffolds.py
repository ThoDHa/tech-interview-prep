"""Unit tests for the NeetCode 150 manifest validator, metadata parser, and emitters.

The metadata fixtures under scripts/fixtures/ are trimmed copies of real
`getProblemMetadataFunctionHttp` responses (a clean problem, a LeetCode-premium
problem, a premium problem carrying LaTeX, and a null payload). Run with:

    cd practice && uv run pytest ../scripts/
"""

import ast
import json
import re
from pathlib import Path

import pytest

import generate_neetcode150_scaffolds as gen

SCRIPTS_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = SCRIPTS_DIR / "neetcode150_manifest.json"
FIXTURES_DIR = SCRIPTS_DIR / "fixtures"

CLEAN_METADATA = json.loads((FIXTURES_DIR / "neetcode_metadata_clean.json").read_text(encoding="utf-8"))
PREMIUM_METADATA = json.loads((FIXTURES_DIR / "neetcode_metadata_premium.json").read_text(encoding="utf-8"))
LATEX_METADATA = json.loads((FIXTURES_DIR / "neetcode_metadata_latex.json").read_text(encoding="utf-8"))
NULL_METADATA = json.loads((FIXTURES_DIR / "neetcode_metadata_null.json").read_text(encoding="utf-8"))


def loaded_manifest():
    return gen.load_manifest(MANIFEST_PATH)


def first_entry_copy(entries):
    return [dict(entries[0])]


# ---------------------------------------------------------------------------
# The committed manifest satisfies the track contract
# ---------------------------------------------------------------------------


def test_committed_manifest_passes_validation():
    gen.validate_manifest(loaded_manifest())


def test_committed_manifest_carries_150_ordered_entries():
    manifest = loaded_manifest()
    assert len(manifest) == gen.TRACK_SIZE
    assert [entry["order"] for entry in manifest] == list(range(1, gen.TRACK_SIZE + 1))


def test_committed_manifest_has_unique_lc_slugs():
    lc_slugs = [entry["lcSlug"] for entry in loaded_manifest()]
    assert len(set(lc_slugs)) == gen.TRACK_SIZE


def test_committed_manifest_has_unique_dir_slugs():
    dir_slugs = [entry["dirSlug"] for entry in loaded_manifest()]
    assert len(set(dir_slugs)) == gen.TRACK_SIZE


def test_committed_manifest_has_all_18_sections_in_canonical_order():
    sections = []
    for entry in loaded_manifest():
        if not sections or sections[-1] != entry["section"]:
            sections.append(entry["section"])
    assert sections == list(gen.SECTION_COUNTS)


def test_committed_manifest_difficulty_totals_match_the_track_counters():
    totals = {"Easy": 0, "Medium": 0, "Hard": 0}
    for entry in loaded_manifest():
        totals[entry["difficulty"]] += 1
    assert totals == gen.DIFFICULTY_TOTALS


def test_committed_manifest_maps_special_slugs_to_house_dir_names():
    by_lc_slug = {entry["lcSlug"]: entry["dirSlug"] for entry in loaded_manifest()}
    assert by_lc_slug["powx-n"] == "powx_n"
    assert by_lc_slug["number-of-1-bits"] == "number_of_1_bits"
    assert by_lc_slug["n-queens"] == "n_queens"


def test_committed_manifest_dir_slugs_all_derive_from_lc_slugs():
    for entry in loaded_manifest():
        assert entry["dirSlug"] == entry["lcSlug"].replace("-", "_")


def test_committed_manifest_entries_carry_every_required_field():
    for entry in loaded_manifest():
        assert set(gen.MANIFEST_FIELDS).issubset(entry)


# ---------------------------------------------------------------------------
# Validator rejections
# ---------------------------------------------------------------------------


def test_validate_manifest_rejects_wrong_entry_count():
    entries = loaded_manifest()
    entries.pop()
    with pytest.raises(gen.ManifestError, match="150"):
        gen.validate_manifest(entries)


def test_validate_manifest_rejects_out_of_order_entries():
    entries = loaded_manifest()
    entries[10]["order"], entries[11]["order"] = 12, 11
    with pytest.raises(gen.ManifestError, match="order"):
        gen.validate_manifest(entries)


def test_validate_manifest_rejects_duplicate_lc_slugs():
    entries = first_entry_copy(loaded_manifest())
    entries.append(dict(entries[0], order=2))
    with pytest.raises(gen.ManifestError, match="duplicate.*lcSlug"):
        gen.validate_manifest(entries)


def test_validate_manifest_rejects_unknown_section():
    entries = first_entry_copy(loaded_manifest())
    entries[0]["section"] = "Quantum Computing"
    with pytest.raises(gen.ManifestError, match="section"):
        gen.validate_manifest(entries)


def test_validate_manifest_rejects_wrong_section_counts():
    entries = loaded_manifest()
    entries[0]["section"] = "Two Pointers"
    with pytest.raises(gen.ManifestError, match="section counts"):
        gen.validate_manifest(entries)


def test_validate_manifest_rejects_wrong_difficulty_totals():
    entries = first_entry_copy(loaded_manifest())
    entries[0]["difficulty"] = "Hard"
    with pytest.raises(gen.ManifestError, match="difficulty"):
        gen.validate_manifest(entries)


def test_validate_manifest_rejects_unknown_difficulty_value():
    entries = first_entry_copy(loaded_manifest())
    entries[0]["difficulty"] = "Intermediate"
    with pytest.raises(gen.ManifestError, match="difficulty"):
        gen.validate_manifest(entries)


def test_validate_manifest_rejects_dir_slug_not_derived_from_lc_slug():
    entries = first_entry_copy(loaded_manifest())
    entries[0]["dirSlug"] = "wrong_name"
    with pytest.raises(gen.ManifestError, match="dirSlug"):
        gen.validate_manifest(entries)


def test_validate_manifest_rejects_missing_required_fields():
    entries = first_entry_copy(loaded_manifest())
    del entries[0]["ncSlug"]
    with pytest.raises(gen.ManifestError, match="ncSlug"):
        gen.validate_manifest(entries)


def test_validate_manifest_reports_all_violations_not_only_the_first():
    entries = loaded_manifest()
    entries.pop()
    entries[0]["dirSlug"] = "wrong_name"
    with pytest.raises(gen.ManifestError) as error:
        gen.validate_manifest(entries)
    assert "150" in str(error.value)
    assert "dirSlug" in str(error.value)


def test_validate_manifest_does_not_mutate_its_input():
    entries = loaded_manifest()
    snapshot = json.loads(json.dumps(entries))
    gen.validate_manifest(entries)
    assert entries == snapshot


# ---------------------------------------------------------------------------
# Delta derivation (overlap keeps its files; partial overlap is an error)
# ---------------------------------------------------------------------------


def make_entry(lc_slug):
    return {
        "order": 1,
        "section": "Arrays & Hashing",
        "title": "T",
        "lcSlug": lc_slug,
        "dirSlug": lc_slug.replace("-", "_"),
        "ncSlug": lc_slug,
        "difficulty": "Easy",
        "leetcodePremium": None,
    }


def test_derive_delta_keeps_entries_without_docs_or_practice(tmp_path):
    docs_dir = tmp_path / "docs"
    practice_dir = tmp_path / "practice"
    entries = [make_entry("solo-problem")]
    delta = gen.derive_delta(entries, docs_dir=docs_dir, practice_dir=practice_dir)
    assert [entry["lcSlug"] for entry in delta] == ["solo-problem"]


def test_derive_delta_excludes_full_overlap_problems(tmp_path):
    docs_dir = tmp_path / "docs" / "problems"
    practice_dir = tmp_path / "practice"
    docs_dir.mkdir(parents=True)
    (practice_dir / "done_problem").mkdir(parents=True)
    (docs_dir / "done_problem.md").write_text("# done", encoding="utf-8")
    entries = [make_entry("done-problem"), make_entry("solo-problem")]
    delta = gen.derive_delta(entries, docs_dir=docs_dir, practice_dir=practice_dir)
    assert [entry["lcSlug"] for entry in delta] == ["solo-problem"]


def test_derive_delta_matches_docs_and_practice_membership_symmetrically(tmp_path):
    docs_dir = tmp_path / "docs" / "problems"
    practice_dir = tmp_path / "practice"
    docs_dir.mkdir(parents=True)
    practice_dir.mkdir(parents=True)
    (docs_dir / "solo_problem.md").write_text("# solo", encoding="utf-8")
    (docs_dir / "done_problem.md").write_text("# done", encoding="utf-8")
    (practice_dir / "done_problem").mkdir()
    entries = [make_entry("done-problem"), make_entry("solo-problem")]
    with pytest.raises(gen.ManifestError, match="solo-problem"):
        gen.derive_delta(entries, docs_dir=docs_dir, practice_dir=practice_dir)


def test_derive_delta_raises_on_partial_overlap(tmp_path):
    docs_dir = tmp_path / "docs" / "problems"
    practice_dir = tmp_path / "practice"
    docs_dir.mkdir(parents=True)
    (docs_dir / "half_problem.md").write_text("# half", encoding="utf-8")
    with pytest.raises(gen.ManifestError, match="half-problem"):
        gen.derive_delta(
            [make_entry("half-problem")], docs_dir=docs_dir, practice_dir=practice_dir
        )


# ---------------------------------------------------------------------------
# Metadata fetching (disk cache, polite delay, network off-switch)
# ---------------------------------------------------------------------------


def seed_metadata_cache(cache_dir, slug, payload):
    cache_dir.mkdir(parents=True, exist_ok=True)
    (cache_dir / f"{slug}.json").write_text(json.dumps(payload), encoding="utf-8")


def test_fetch_metadata_serves_cache_hits_without_network(tmp_path, monkeypatch):
    seed_metadata_cache(tmp_path / "cache", "anagram-groups", CLEAN_METADATA)
    monkeypatch.setattr(gen, "METADATA_CACHE_DIR", tmp_path / "cache")
    monkeypatch.setattr(
        gen, "urllib_request_urlopen", lambda *a, **k: pytest.fail("network touched")
    )
    metadata = gen.fetch_problem_metadata("anagram-groups", delay=False)
    assert metadata is not None
    assert metadata["id"] == "anagram-groups"


def test_fetch_metadata_post_fetches_misses_and_caches(tmp_path, monkeypatch):
    monkeypatch.setattr(gen, "METADATA_CACHE_DIR", tmp_path / "cache")
    slept = []
    monkeypatch.setattr(gen.time, "sleep", slept.append)

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self):
            return json.dumps(CLEAN_METADATA).encode("utf-8")

    captured = {}

    def fake_urlopen(request, timeout=None):
        captured["url"] = request.full_url
        captured["body"] = request.data
        return FakeResponse()

    monkeypatch.setattr(gen, "urllib_request_urlopen", fake_urlopen)
    metadata = gen.fetch_problem_metadata("anagram-groups")
    assert metadata["id"] == "anagram-groups"
    assert captured["url"] == gen.METADATA_URL
    assert json.loads(captured["body"]) == {"data": {"problemId": "anagram-groups"}}
    assert slept, "polite delay missing before a network fetch"
    assert (tmp_path / "cache" / "anagram-groups.json").exists()


def test_fetch_metadata_http_error_yields_none(tmp_path, monkeypatch):
    monkeypatch.setattr(gen, "METADATA_CACHE_DIR", tmp_path / "cache")
    monkeypatch.setattr(gen.time, "sleep", lambda _s: None)

    def fake_urlopen(request, timeout=None):
        raise gen.urllib.error.HTTPError(request.full_url, 403, "blocked", {}, None)

    monkeypatch.setattr(gen, "urllib_request_urlopen", fake_urlopen)
    assert gen.fetch_problem_metadata("blocked-problem", delay=False) is None
    assert not (tmp_path / "cache" / "blocked-problem.json").exists()


def test_fetch_metadata_without_network_never_leaves_the_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(gen, "METADATA_CACHE_DIR", tmp_path / "cache")
    assert gen.fetch_problem_metadata("never-fetched", network=False) is None
    assert not (tmp_path / "cache" / "never-fetched.json").exists()


def test_fetch_metadata_non_http_failure_raises_with_context(tmp_path, monkeypatch):
    monkeypatch.setattr(gen, "METADATA_CACHE_DIR", tmp_path / "cache")
    monkeypatch.setattr(gen.time, "sleep", lambda _s: None)
    monkeypatch.setattr(
        gen, "urllib_request_urlopen", lambda *a, **k: (_ for _ in ()).throw(OSError("dns"))
    )
    with pytest.raises(RuntimeError, match="dns"):
        gen.fetch_problem_metadata("anagram-groups", delay=False)


# ---------------------------------------------------------------------------
# Metadata parsing and description decomposition
# ---------------------------------------------------------------------------


def test_parse_metadata_returns_the_data_record():
    metadata = gen.parse_metadata(CLEAN_METADATA)
    assert metadata is not None
    assert metadata["id"] == "anagram-groups"
    assert metadata["difficulty"] == "Medium"


def test_parse_metadata_returns_none_for_null_payload():
    assert gen.parse_metadata(NULL_METADATA) is None
    assert gen.parse_metadata(None) is None
    assert gen.parse_metadata({}) is None


def test_parse_description_extracts_statement_prose_before_examples():
    parsed = gen.parse_description(CLEAN_METADATA["data"]["description"])
    assert parsed["statement"].startswith("Given an array of strings `strs`")
    assert parsed["statement"].endswith("the order of the characters can be different.")
    assert "**Example" not in parsed["statement"]


def test_parse_description_extracts_every_example_block():
    parsed = gen.parse_description(CLEAN_METADATA["data"]["description"])
    assert [example["index"] for example in parsed["examples"]] == [1, 2, 3]
    first = parsed["examples"][0]
    assert first["input"] == 'strs = ["act","pots","tops","cat","stop","hat"]'
    assert first["output"] == '[["hat"],["act", "cat"],["stop", "pots", "tops"]]'
    assert first["explanation"] == ""


def test_parse_description_keeps_example_explanations():
    parsed = gen.parse_description(PREMIUM_METADATA["data"]["description"])
    first = parsed["examples"][0]
    assert "Machine 1" in first["explanation"]
    assert "encode(strs)" in first["explanation"]


def test_parse_description_fenced_explanations_stay_out_of_the_input_output():
    parsed = gen.parse_description(PREMIUM_METADATA["data"]["description"])
    first = parsed["examples"][0]
    assert first["input"] == 'strs = ["Hello","World"]'
    assert first["output"] == '["Hello","World"]'
    # The explanation's Java snippet stays fenced (F3), not inline mid-paragraph.
    assert first["explanation"].startswith("```java")
    assert first["explanation"].endswith("```")
    assert "Explanation:" not in first["explanation"]


def test_parse_description_unfenced_explanation_prefix_is_stripped_once():
    description = (
        "Check a board.\n"
        "\n"
        "**Example 1:**\n"
        "\n"
        "```java\n"
        'Input: board = [["1","2"]]\n'
        "\n"
        "Output: true\n"
        "```\n"
        "\n"
        "Explanation: There are two 1's in the top-left 3x3 sub-box.\n"
        "\n"
        "**Constraints:**\n"
        "* `board.length == 9`"
    )
    parsed = gen.parse_description(description)
    example = parsed["examples"][0]
    assert example["explanation"] == "There are two 1's in the top-left 3x3 sub-box."
    assert "Explanation:" not in example["explanation"]


def test_parse_description_extracts_constraints_bullets():
    parsed = gen.parse_description(CLEAN_METADATA["data"]["description"])
    assert parsed["constraints"] == [
        "`1 <= strs.length <= 10000`.",
        "`0 <= strs[i].length <= 100`",
        "`strs[i]` is made up of lowercase English letters.",
    ]


def test_parse_description_extracts_follow_up_when_present():
    parsed = gen.parse_description(PREMIUM_METADATA["data"]["description"])
    assert parsed["follow_up"] == "Could you write a generalized algorithm to work on any possible set of characters?"
    clean = gen.parse_description(CLEAN_METADATA["data"]["description"])
    assert clean["follow_up"] == ""


def test_parse_description_preserves_the_latex_subset():
    parsed = gen.parse_description(LATEX_METADATA["data"]["description"])
    assert "$m \\times n$" in parsed["statement"]


def test_parse_description_drops_the_hint_accordions():
    for payload in (CLEAN_METADATA, PREMIUM_METADATA, LATEX_METADATA):
        parsed = gen.parse_description(payload["data"]["description"])
        text = json.dumps(parsed)
        assert "hint-accordion" not in text
        assert "Hint 1" not in text
        assert "NeetCode Pro" not in text
        assert "<details" not in text
        assert "<br" not in text


def test_parse_description_yields_empty_sections_for_garbage():
    parsed = gen.parse_description("")
    assert parsed["statement"] == ""
    assert parsed["examples"] == []
    assert parsed["constraints"] == []


# ---------------------------------------------------------------------------
# Starter-code signatures: function name and unassertable shapes
# ---------------------------------------------------------------------------


def test_function_name_comes_from_the_starter_code():
    metadata = gen.parse_metadata(CLEAN_METADATA)
    assert gen.function_name_from_starter(metadata) == "groupAnagrams"


def test_function_name_falls_back_to_solve_without_starter_code():
    assert gen.function_name_from_starter({"starterCode": {}}) == "solve"
    assert gen.function_name_from_starter(None) == "solve"


def test_cases_skips_any_order_outputs_naming_the_slug():
    result = gen.cases_from_metadata(gen.parse_metadata(CLEAN_METADATA), "group_anagrams")
    assert result.cases == []
    assert "group_anagrams" in result.skip_reason
    assert "any-order" in result.skip_reason


def test_cases_skips_multi_method_starters_naming_the_slug():
    metadata = gen.parse_metadata(PREMIUM_METADATA)
    result = gen.cases_from_metadata(metadata, "encode_and_decode_strings")
    assert result.cases == []
    assert "encode_and_decode_strings" in result.skip_reason
    assert "encode" in result.skip_reason


def test_cases_skips_in_place_mutation_naming_the_slug():
    metadata = gen.parse_metadata(LATEX_METADATA)
    result = gen.cases_from_metadata(metadata, "walls_and_gates")
    assert result.cases == []
    assert "walls_and_gates" in result.skip_reason
    assert "in-place" in result.skip_reason


def test_cases_skips_structural_annotations_naming_the_slug():
    metadata = dict(
        gen.parse_metadata(CLEAN_METADATA),
        starterCode={
            "python": (
                "class Solution:\n"
                "    def addTwoNumbers(self, l1: Optional[ListNode], "
                "l2: Optional[ListNode]) -> Optional[ListNode]:\n"
            )
        },
    )
    result = gen.cases_from_metadata(metadata, "add_two_numbers")
    assert result.cases == []
    assert "add_two_numbers" in result.skip_reason


def test_cases_parses_scalar_examples_when_assertable():
    metadata = dict(
        gen.parse_metadata(CLEAN_METADATA),
        description=(
            "Given an integer array `nums`, return the k most frequent elements.\n"
            "\n"
            "**Example 1:**\n"
            "\n"
            "```java\n"
            "Input: nums = [1,1,1,2,2,3], k = 2\n"
            "\n"
            "Output: [1,2]\n"
            "```\n"
            "\n"
            "**Example 2:**\n"
            "\n"
            "```java\n"
            "Input: nums = [1], k = 1\n"
            "\n"
            "Output: [1]\n"
            "```\n"
            "\n"
            "**Constraints:**\n"
            "* `1 <= nums.length <= 10^5`"
        ),
        starterCode={
            "python": "class Solution:\n    def topKFrequent(self, nums: List[int], k: int) -> List[int]:\n"
        },
    )
    result = gen.cases_from_metadata(metadata, "top_k_frequent_elements")
    assert result.skip_reason is None
    assert result.function_name == "topKFrequent"
    assert result.cases == [
        {"id": "example_1", "args": [[1, 1, 1, 2, 2, 3], 2], "expected": [1, 2]},
        {"id": "example_2", "args": [[1], 1], "expected": [1]},
    ]


def test_cases_parses_anonymous_grid_inputs():
    metadata = dict(
        gen.parse_metadata(CLEAN_METADATA),
        description=(
            "Given an `m x n` grid, return the number of islands.\n"
            "\n"
            "**Example 1:**\n"
            "\n"
            "```java\n"
            'Input: grid = [["1","1"],["0","0"]]\n'
            "\n"
            "Output: 1\n"
            "```\n"
        ),
        starterCode={
            "python": "class Solution:\n    def numIslands(self, grid: List[List[str]]) -> int:\n"
        },
    )
    result = gen.cases_from_metadata(metadata, "number_of_islands")
    assert result.cases == [
        {"id": "example_1", "args": [[["1", "1"], ["0", "0"]]], "expected": 1}
    ]


def test_cases_rejects_null_anywhere_in_the_example():
    metadata = dict(
        gen.parse_metadata(CLEAN_METADATA),
        description=(
            "Traverse.\n\n**Example 1:**\n\n```java\nInput: root = [1,2]\n\n"
            "Output: [1,null,2]\n```\n"
        ),
        starterCode={
            "python": "class Solution:\n    def traverse(self, root: Optional[int]) -> List[int]:\n"
        },
    )
    result = gen.cases_from_metadata(metadata, "nullish_problem")
    assert result.cases == []
    assert "nullish_problem" in result.skip_reason


def test_cases_rejects_free_text_output():
    metadata = dict(
        gen.parse_metadata(CLEAN_METADATA),
        description=(
            "Explain.\n\n**Example 1:**\n\n```java\nInput: s = \"abc\"\n\n"
            "Output: a valid ordering\n```\n"
        ),
        starterCode={
            "python": "class Solution:\n    def explain(self, s: str) -> str:\n"
        },
    )
    result = gen.cases_from_metadata(metadata, "prose_problem")
    assert result.cases == []
    assert "prose_problem" in result.skip_reason


def test_cases_skips_examples_with_no_input_block():
    metadata = dict(
        gen.parse_metadata(CLEAN_METADATA),
        description="Odd.\n\n**Example 1:**\n\n```java\nOutput: 1\n```\n",
        starterCode={"python": "class Solution:\n    def odd(self) -> int:\n"},
    )
    result = gen.cases_from_metadata(metadata, "no_input_problem")
    assert result.cases == []
    assert "no_input_problem" in result.skip_reason


# ---------------------------------------------------------------------------
# Scaffold rendering (structural conventions)
# ---------------------------------------------------------------------------


def writeup_entry():
    return {
        "order": 4,
        "section": "Arrays & Hashing",
        "title": "Group Anagrams",
        "lcSlug": "group-anagrams",
        "dirSlug": "group_anagrams",
        "ncSlug": "anagram-groups",
        "difficulty": "Medium",
        "leetcodePremium": None,
    }


def test_render_writeup_follows_template_section_order():
    metadata = gen.parse_metadata(CLEAN_METADATA)
    text = gen.render_writeup(writeup_entry(), metadata)
    headings = re.findall(r"^#+ .*$", text, flags=re.M)
    assert headings[0] == "# [Group Anagrams](https://leetcode.com/problems/group-anagrams/)"
    assert "## Examples" in headings
    assert "## Constraints" in headings
    assert headings.index("## Examples") < headings.index("## Constraints")
    assert "## Solutions" in headings
    assert headings.index("## Constraints") < headings.index("## Solutions")
    assert "main later" in text


def test_render_writeup_references_template_as_sibling():
    text = gen.render_writeup(writeup_entry(), gen.parse_metadata(CLEAN_METADATA))
    assert "See _TEMPLATE.md for the" in text
    assert "See ../_TEMPLATE.md" not in text


def test_render_writeup_renders_the_metadata_line():
    metadata = gen.parse_metadata(CLEAN_METADATA)
    text = gen.render_writeup(writeup_entry(), metadata)
    assert "**Medium** | **NN minutes** | **Array, Hash Table, String, Sorting**" in text


def test_render_writeup_uses_manifest_difficulty_and_topic_placeholder_when_metadata_is_absent():
    text = gen.render_writeup(writeup_entry(), None)
    assert "**Medium** | **NN minutes** | **unknown topics**" in text
    assert "Statement not parseable" in text
    assert "Examples not parseable" in text
    assert "Constraints not parseable" in text


def test_render_writeup_notes_the_neetcode_fallback_for_premium():
    metadata = dict(gen.parse_metadata(PREMIUM_METADATA))
    entry = dict(
        writeup_entry(),
        title="Encode and Decode Strings",
        lcSlug="encode-and-decode-strings",
        dirSlug="encode_and_decode_strings",
        ncSlug="string-encode-and-decode",
        leetcodePremium=True,
    )
    text = gen.render_writeup(entry, metadata)
    assert "LeetCode Premium" in text
    assert "https://neetcode.io/problems/string-encode-and-decode" in text


def test_render_writeup_has_no_premium_note_for_free_problems():
    text = gen.render_writeup(writeup_entry(), gen.parse_metadata(CLEAN_METADATA))
    assert "LeetCode Premium" not in text


def test_render_writeup_renders_examples_in_house_style():
    metadata = gen.parse_metadata(CLEAN_METADATA)
    text = gen.render_writeup(writeup_entry(), metadata)
    assert "### Example 1" in text
    assert '**Input:** `strs = ["act","pots","tops","cat","stop","hat"]`' in text
    assert '**Output:** `[["hat"],["act", "cat"],["stop", "pots", "tops"]]`' in text


def test_render_writeup_fences_multiline_example_inputs():
    metadata = gen.parse_metadata(LATEX_METADATA)
    entry = dict(
        writeup_entry(),
        title="Walls And Gates",
        lcSlug="walls-and-gates",
        dirSlug="walls_and_gates",
        ncSlug="islands-and-treasure",
    )
    text = gen.render_writeup(entry, metadata)
    example_one = text.split("### Example 1")[1].split("### Example 2")[0]
    assert "**Input:**" in example_one
    assert "```" in example_one
    assert "  [2147483647,-1,0,2147483647]," in example_one
    assert not re.search(r"\*\*Input:\*\* `\[", example_one)


def test_render_writeup_keeps_multiline_output_in_the_fence():
    metadata = gen.parse_metadata(LATEX_METADATA)
    entry = dict(
        writeup_entry(),
        title="Walls And Gates",
        lcSlug="walls-and-gates",
        dirSlug="walls_and_gates",
        ncSlug="islands-and-treasure",
    )
    text = gen.render_writeup(entry, metadata)
    example_one = text.split("### Example 1")[1].split("### Example 2")[0]
    assert "[3,-1,0,1]," in example_one


def test_render_writeup_renders_constraints_as_bullets():
    metadata = gen.parse_metadata(CLEAN_METADATA)
    text = gen.render_writeup(writeup_entry(), metadata)
    assert "- `1 <= strs.length <= 10000`." in text


def test_render_writeup_renders_follow_up_section_when_present():
    metadata = gen.parse_metadata(PREMIUM_METADATA)
    entry = dict(writeup_entry(), title="Encode and Decode Strings", lcSlug="encode-and-decode-strings", dirSlug="encode_and_decode_strings")
    text = gen.render_writeup(entry, metadata)
    headings = re.findall(r"^## .*$", text, flags=re.M)
    assert "## Follow-up" in headings
    assert headings.index("## Follow-up") < headings.index("## Solutions")
    assert "generalized algorithm" in text


def test_render_writeup_has_no_follow_up_section_when_absent():
    text = gen.render_writeup(writeup_entry(), gen.parse_metadata(CLEAN_METADATA))
    assert "## Follow-up" not in text


def test_render_solution_stub_matches_house_style():
    metadata = gen.parse_metadata(CLEAN_METADATA)
    cases = gen.CasesResult("groupAnagrams", [{"id": "example_1", "args": [["a"]], "expected": [["a"]]}], None)
    text = gen.render_solution_stub(writeup_entry(), metadata, cases)
    assert text.startswith('"""Group Anagrams — https://leetcode.com/problems/group-anagrams/')
    assert "Write-up & approaches: ../../../docs/leetcode/group_anagrams.md" in text
    assert "from harness import NotSolved, pick_case" in text
    assert "raise NotSolved" in text
    assert "def groupAnagrams(self, strs" in text
    assert 'CASE = "example_1"' in text


def test_render_solution_stub_star_args_when_signature_unknown():
    cases = gen.CasesResult("solve", [], "no cases for group_anagrams")
    text = gen.render_solution_stub(writeup_entry(), None, cases)
    assert "def solve(self, *args)" in text


def test_render_solution_stub_avoids_python_keywords_in_signature():
    metadata = dict(
        gen.parse_metadata(CLEAN_METADATA),
        description=(
            "Filter.\n\n**Example 1:**\n\n```java\nInput: class = [1], from = 2\n\n"
            "Output: 3\n```\n"
        ),
    )
    cases = gen.cases_from_metadata(metadata, "keyword_problem")
    assert cases.cases, "keyword-named inputs should still parse into cases"
    text = gen.render_solution_stub(writeup_entry(), metadata, cases)
    assert "def " in text
    module = ast.parse(text)
    assert module is not None


def test_render_cases_file_always_writes_json():
    text = gen.render_cases_file(gen.CasesResult("solve", [], "reason"))
    assert json.loads(text) == []
    text = gen.render_cases_file(gen.CasesResult("solve", [{"id": "example_1", "args": [1], "expected": 1}], None))
    assert json.loads(text) == [{"id": "example_1", "args": [1], "expected": 1}]


def test_render_test_skips_empty_cases_naming_the_slug():
    text = gen.render_test(writeup_entry(), "groupAnagrams", [], "no assertable cases for group_anagrams")
    assert "pytest.skip" in text
    assert "group_anagrams" in text
    assert "len(CASES) == 0" in text


def test_render_test_parametrizes_when_cases_exist():
    cases = [{"id": "example_1", "args": [[1]], "expected": 1}]
    text = gen.render_test(writeup_entry(), "groupAnagrams", cases, None)
    assert "@pytest.mark.parametrize" in text
    assert ".groupAnagrams" in text
    assert "NotSolved" in text


def test_render_test_embeds_python_literals_not_json():
    cases = [{"id": "example_1", "args": [[1, 2]], "expected": [1, None, 2]}]
    text = gen.render_test(writeup_entry(), "groupAnagrams", cases, None)
    module = ast.parse(text)
    cases_node = next(
        node.value
        for node in module.body
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "CASES"
    )
    assert ast.literal_eval(cases_node) == cases


def test_render_all_covers_every_scaffold_file(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs" / "problems"
    practice_dir = tmp_path / "practice"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    metadata = gen.parse_metadata(CLEAN_METADATA)
    cases = gen.cases_from_metadata(metadata, "group_anagrams")
    rendered = gen.render_all(writeup_entry(), metadata, cases)
    assert set(rendered) == {
        docs_dir / "group_anagrams.md",
        practice_dir / "group_anagrams" / "solution.py",
        practice_dir / "group_anagrams" / "cases.json",
        practice_dir / "group_anagrams" / "test_group_anagrams.py",
    }


# ---------------------------------------------------------------------------
# Emission: parse_status, premium recording, no-overwrite guard
# ---------------------------------------------------------------------------


def test_emit_scaffolds_emits_and_records_status(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs" / "problems"
    practice_dir = tmp_path / "practice"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    monkeypatch.setattr(gen, "METADATA_CACHE_DIR", tmp_path / "cache")
    seed_metadata_cache(tmp_path / "cache", "anagram-groups", CLEAN_METADATA)
    entry = writeup_entry()
    stats = gen.emit_scaffolds([entry], fetch=False)
    assert stats["generated"] == 1
    assert stats["cases_empty"] == 1
    assert entry["parse_status"] == "parsed-empty-cases"
    assert entry["leetcodePremium"] is False
    writeup = (docs_dir / "group_anagrams.md").read_text(encoding="utf-8")
    assert "Group Anagrams" in writeup
    assert json.loads((practice_dir / "group_anagrams" / "cases.json").read_text()) == []
    test_text = (practice_dir / "group_anagrams" / "test_group_anagrams.py").read_text(encoding="utf-8")
    assert "group_anagrams" in test_text


def test_emit_scaffolds_skips_uncached_without_overwriting(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs" / "problems"
    practice_dir = tmp_path / "practice"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    monkeypatch.setattr(gen, "METADATA_CACHE_DIR", tmp_path / "cache")
    good_cases = [{"id": "example_1", "args": [1], "expected": 1}]
    (practice_dir / "uncached_problem").mkdir(parents=True)
    (practice_dir / "uncached_problem" / "cases.json").write_text(
        json.dumps(good_cases), encoding="utf-8"
    )
    entry = dict(writeup_entry(), lcSlug="uncached-problem", dirSlug="uncached_problem")
    stats = gen.emit_scaffolds([entry], fetch=False)
    assert stats["skipped_no_cache"] == ["uncached_problem"]
    assert stats["generated"] == 0
    assert "parse_status" not in entry
    assert json.loads((practice_dir / "uncached_problem" / "cases.json").read_text()) == good_cases


def test_emit_scaffolds_marks_unparseable_metadata(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs" / "problems"
    practice_dir = tmp_path / "practice"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    monkeypatch.setattr(gen, "METADATA_CACHE_DIR", tmp_path / "cache")
    seed_metadata_cache(tmp_path / "cache", "gone-problem", NULL_METADATA)
    entry = dict(writeup_entry(), lcSlug="gone-problem", dirSlug="gone_problem", ncSlug="gone-problem")
    stats = gen.emit_scaffolds([entry], fetch=False)
    assert stats["generated"] == 1
    assert stats["parse_failures"] == ["gone_problem"]
    assert entry["parse_status"] == "metadata-unparseable"
    writeup = (docs_dir / "gone_problem.md").read_text(encoding="utf-8")
    assert "Statement not parseable" in writeup


def test_emit_scaffolds_records_premium_flag(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs" / "problems"
    practice_dir = tmp_path / "practice"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    monkeypatch.setattr(gen, "METADATA_CACHE_DIR", tmp_path / "cache")
    seed_metadata_cache(tmp_path / "cache", "string-encode-and-decode", PREMIUM_METADATA)
    entry = dict(writeup_entry(), lcSlug="encode-and-decode-strings", dirSlug="encode_and_decode_strings", ncSlug="string-encode-and-decode")
    stats = gen.emit_scaffolds([entry], fetch=False)
    assert stats["generated"] == 1
    assert entry["leetcodePremium"] is True


# ---------------------------------------------------------------------------
# Home-page ownership and mkdocs nav group
# ---------------------------------------------------------------------------


def sample_manifest(n=3):
    return [
        {
            "order": 1,
            "section": "Arrays & Hashing",
            "title": "Contains Duplicate",
            "lcSlug": "contains-duplicate",
            "dirSlug": "contains_duplicate",
            "ncSlug": "duplicate-integer",
            "difficulty": "Easy",
            "leetcodePremium": None,
        },
        {
            "order": 2,
            "section": "Arrays & Hashing",
            "title": "Valid Anagram",
            "lcSlug": "valid-anagram",
            "dirSlug": "valid_anagram",
            "ncSlug": "is-anagram",
            "difficulty": "Easy",
            "leetcodePremium": None,
        },
        {
            "order": 3,
            "section": "Two Pointers",
            "title": "Two Sum II",
            "lcSlug": "two-sum-ii-input-array-is-sorted",
            "dirSlug": "two_sum_ii_input_array_is_sorted",
            "ncSlug": "two-sum-ii-input-array-is-sorted",
            "difficulty": "Medium",
            "leetcodePremium": None,
        },
    ][:n]


def test_the_mkdocs_nav_is_owned_by_the_index_tables_generator():
    # The nested NeetCode 150 nav group was superseded by the flat
    # LeetCode subsection (scripts/generate_index_tables.py); nav emission
    # and its --check must not creep back into this generator.
    assert not hasattr(gen, "ensure_nav_group")
    assert not hasattr(gen, "check_site_integration")
    assert not hasattr(gen, "nav_group_entries")
    assert not hasattr(gen, "MKDOCS_PATH")
    assert not hasattr(gen, "NAV_GROUP_MARKER")
    assert not hasattr(gen, "NAV_GROUP_HEADER")


def test_the_docs_index_tables_are_owned_by_the_index_tables_generator():
    # The neet150 marker section was superseded by the unified table
    # (scripts/generate_index_tables.py); the index ownership must not
    # creep back into this generator.
    source = (SCRIPTS_DIR / "generate_neetcode150_scaffolds.py").read_text(encoding="utf-8")
    assert "INDEX_PATH" not in source
    assert not hasattr(gen, "render_index_section")
    assert not hasattr(gen, "write_index_section")
    assert not hasattr(gen, "INDEX_PATH")
    assert not hasattr(gen, "INDEX_SECTION_START")


# ---------------------------------------------------------------------------
# Idempotency check and CLI wiring
# ---------------------------------------------------------------------------


def test_check_mode_passes_on_a_fresh_tree(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs" / "problems"
    practice_dir = tmp_path / "practice"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    monkeypatch.setattr(gen, "METADATA_CACHE_DIR", tmp_path / "cache")
    seed_metadata_cache(tmp_path / "cache", "anagram-groups", CLEAN_METADATA)
    entry = writeup_entry()
    gen.emit_scaffolds([entry], fetch=False)
    assert gen.check([entry]) == 0


def test_check_mode_fails_when_files_drift(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs" / "problems"
    practice_dir = tmp_path / "practice"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    monkeypatch.setattr(gen, "METADATA_CACHE_DIR", tmp_path / "cache")
    seed_metadata_cache(tmp_path / "cache", "anagram-groups", CLEAN_METADATA)
    entry = writeup_entry()
    gen.emit_scaffolds([entry], fetch=False)
    (practice_dir / "group_anagrams" / "cases.json").write_text(
        '[{"id": "tampered", "args": [1], "expected": 1}]\n', encoding="utf-8"
    )
    assert gen.check([entry]) == 1


def test_main_check_mode_does_not_rewrite_the_manifest(tmp_path, monkeypatch):
    monkeypatch.setattr(gen, "MANIFEST_PATH", MANIFEST_PATH)
    reads = []
    real_load = gen.load_manifest

    def spy(path=None):
        reads.append(path)
        return real_load(path or MANIFEST_PATH)

    monkeypatch.setattr(gen, "load_manifest", spy)
    monkeypatch.setattr(gen, "check", lambda entries: 0)
    assert gen.main(["--check"]) == 0
    assert len(reads) == 1


def test_main_runs_the_full_pipeline_shape(tmp_path, monkeypatch, capsys):
    docs_dir = tmp_path / "docs" / "problems"
    practice_dir = tmp_path / "practice"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    monkeypatch.setattr(gen, "METADATA_CACHE_DIR", tmp_path / "cache")
    monkeypatch.setattr(gen, "MANIFEST_PATH", MANIFEST_PATH)
    monkeypatch.setattr(
        gen, "derive_delta", lambda entries: [writeup_entry()]
    )
    seed_metadata_cache(tmp_path / "cache", "anagram-groups", CLEAN_METADATA)
    exit_code = gen.main([])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "delta: 1 problems to scaffold" in out
    assert "generated" in out


def test_emit_scaffolds_premium_note_lands_in_the_writeup(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs" / "problems"
    practice_dir = tmp_path / "practice"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    monkeypatch.setattr(gen, "METADATA_CACHE_DIR", tmp_path / "cache")
    seed_metadata_cache(tmp_path / "cache", "string-encode-and-decode", PREMIUM_METADATA)
    entry = dict(
        writeup_entry(),
        lcSlug="encode-and-decode-strings",
        dirSlug="encode_and_decode_strings",
        ncSlug="string-encode-and-decode",
        leetcodePremium=None,
    )
    stats = gen.emit_scaffolds([entry], fetch=False)
    assert stats["generated"] == 1
    writeup = (docs_dir / "encode_and_decode_strings.md").read_text(encoding="utf-8")
    assert "LeetCode Premium" in writeup
    # Regeneration is stable: check() compares clean.
    assert gen.check([entry]) == 0


# ---------------------------------------------------------------------------
# Fix round regressions (review findings F1-F5, S2)
# ---------------------------------------------------------------------------


def any_order_variants_metadata(statement, explanation=""):
    example = (
        "**Example 1:**\n\n```java\nInput: n = 2\n\nOutput: [0,1]\n```\n"
    )
    if explanation:
        example += f"\n**Explanation:** {explanation}\n"
    return dict(
        gen.parse_metadata(CLEAN_METADATA),
        description=f"{statement}\n\n{example}\n\n**Constraints:**\n* `1 <= n <= 10`",
        starterCode={
            "python": "class Solution:\n    def findOrder(self, n: int) -> List[int]:\n"
        },
    )


@pytest.mark.parametrize(
    "phrasing",
    [
        "If there are many valid answers, return **any** of them.",
        "If there are multiple valid answers you can return any of them.",
        "You may return the answer in any order.",
    ],
)
def test_cases_any_order_statement_variants_yield_empty_cases(phrasing):
    metadata = any_order_variants_metadata(phrasing)
    result = gen.cases_from_metadata(metadata, "phrasing_problem")
    assert result.cases == []
    assert "phrasing_problem" in result.skip_reason


def test_cases_any_order_in_explanation_yields_empty_cases():
    metadata = any_order_variants_metadata(
        "Return the ordering.",
        explanation="The ordering [0,1] would still be accepted.",
    )
    result = gen.cases_from_metadata(metadata, "explained_problem")
    assert result.cases == []
    assert "explained_problem" in result.skip_reason


def test_cases_exact_wording_still_yields_cases_without_any_order():
    metadata = any_order_variants_metadata(
        "Return the ordering; the answer is guaranteed unique."
    )
    result = gen.cases_from_metadata(metadata, "unique_problem")
    assert result.skip_reason is None
    assert result.cases


def test_cases_from_parsed_reports_the_metadata_reason_when_metadata_is_none():
    result = gen.cases_from_parsed(
        {"statement": "", "examples": [], "constraints": [], "follow_up": ""},
        None,
        "nullish_problem",
    )
    assert result.cases == []
    assert result.skip_reason == "metadata did not parse for nullish_problem"


def test_cases_from_parsed_treats_a_none_parsed_description_as_empty():
    metadata = gen.parse_metadata(CLEAN_METADATA)
    result = gen.cases_from_parsed(None, metadata, "empty_description_problem")
    assert result.cases == []
    assert result.skip_reason == "no examples in the description for empty_description_problem"


def test_cases_multi_output_word_search_shape_yields_empty_cases():
    metadata = dict(
        gen.parse_metadata(CLEAN_METADATA),
        description=(
            "Given a 2-D grid of characters `board` and a list of strings "
            "`words`, return all words that are present in the grid.\n"
            "\n"
            "**Example 1:**\n"
            "\n"
            "```java\n"
            'Input: board = [["a","b"]], words = ["ab"]\n'
            "\n"
            'Output: ["ab"]\n'
            "```\n"
            "\n"
            "**Constraints:**\n"
            "* `1 <= board.length <= 5`"
        ),
        starterCode={
            "python": (
                "class Solution:\n"
                "    def findWords(self, board: List[List[str]], "
                "words: List[str]) -> List[str]:\n"
            )
        },
    )
    result = gen.cases_from_metadata(metadata, "word_search_ii")
    assert result.cases == []
    assert "word_search_ii" in result.skip_reason


def test_parse_description_follow_up_before_examples_is_bounded():
    description = (
        "Given a matrix, zero out rows and columns.\n"
        "\n"
        "**Follow-up:** Could you solve it using O(1) space?\n"
        "\n"
        "**Example 1:**\n"
        "\n"
        "```java\n"
        "Input: matrix = [[0,1],[1,0]]\n"
        "\n"
        "Output: [[0,0],[0,0]]\n"
        "```\n"
        "\n"
        "**Constraints:**\n"
        "* `m == matrix.length`"
    )
    parsed = gen.parse_description(description)
    assert parsed["follow_up"] == "Could you solve it using O(1) space?"
    assert len(parsed["examples"]) == 1
    assert parsed["examples"][0]["input"] == "matrix = [[0,1],[1,0]]"
    assert parsed["examples"][0]["output"] == "[[0,0],[0,0]]"
    assert parsed["constraints"] == ["`m == matrix.length`"]
    assert "Example" not in parsed["follow_up"]
    assert "imagedelivery" not in json.dumps(parsed)


def test_parse_description_follow_up_after_constraints_is_bounded():
    description = (
        "Encode strings.\n"
        "\n"
        "**Example 1:**\n"
        "\n"
        "```java\n"
        'Input: strs = ["a"]\n'
        "\n"
        'Output: ["a"]\n'
        "```\n"
        "\n"
        "**Constraints:**\n"
        "* `0 <= strs.length < 100`\n"
        "\n"
        "**Follow up:** Could you write a generalized algorithm?\n"
    )
    parsed = gen.parse_description(description)
    assert parsed["follow_up"] == "Could you write a generalized algorithm?"
    assert parsed["examples"][0]["input"] == 'strs = ["a"]'


def test_render_writeup_explanation_drops_fences_and_broken_bold():
    description = (
        "Encode.\n"
        "\n"
        "**Example 1:**\n"
        "\n"
        "```java\n"
        'Input: strs = ["a"]\n'
        "\n"
        'Output: ["a"]\n'
        "```\n"
        "\n"
        "**Explanation:** **\n"
        "```java\n"
        "Solution solution = new Solution();\n"
        "solution.encode(strs);\n"
        "```\n"
        "\n"
        "**Constraints:**\n"
        "* `0 <= strs.length < 100`"
    )
    metadata = dict(gen.parse_metadata(PREMIUM_METADATA), description=description)
    entry = dict(writeup_entry(), lcSlug="encode-and-decode-strings", dirSlug="encode_and_decode_strings")
    text = gen.render_writeup(entry, metadata)
    assert "**Explanation:** **" not in text
    example_one = text.split("### Example 1")[1].split("## Constraints")[0]
    assert "Solution solution = new Solution();" in example_one
    assert "```" in example_one


def test_fetch_metadata_corrupt_cache_falls_through_to_refetch(tmp_path, monkeypatch):
    monkeypatch.setattr(gen, "METADATA_CACHE_DIR", tmp_path / "cache")
    monkeypatch.setattr(gen.time, "sleep", lambda _s: None)
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir(parents=True)
    (cache_dir / "anagram-groups.json").write_text('{"data": {"id": "trunc', encoding="utf-8")

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self):
            return json.dumps(CLEAN_METADATA).encode("utf-8")

    monkeypatch.setattr(
        gen, "urllib_request_urlopen", lambda request, timeout=None: FakeResponse()
    )
    metadata = gen.fetch_problem_metadata("anagram-groups", delay=False)
    assert metadata is not None
    assert metadata["id"] == "anagram-groups"
    assert json.loads((cache_dir / "anagram-groups.json").read_text()) == CLEAN_METADATA


def test_render_all_accepts_a_pre_parsed_description(tmp_path, monkeypatch):
    docs_dir = tmp_path / "docs" / "problems"
    practice_dir = tmp_path / "practice"
    monkeypatch.setattr(gen, "DOCS_DIR", docs_dir)
    monkeypatch.setattr(gen, "PRACTICE_DIR", practice_dir)
    metadata = gen.parse_metadata(CLEAN_METADATA)
    parsed = gen.parse_description(str(metadata.get("description") or ""))
    cases = gen.cases_from_parsed(parsed, metadata, "group_anagrams")
    rendered = gen.render_all(writeup_entry(), metadata, cases, parsed=parsed)
    assert set(rendered) == {
        docs_dir / "group_anagrams.md",
        practice_dir / "group_anagrams" / "solution.py",
        practice_dir / "group_anagrams" / "cases.json",
        practice_dir / "group_anagrams" / "test_group_anagrams.py",
    }
    writeup = rendered[docs_dir / "group_anagrams.md"]
    assert "## Examples" in writeup


def test_render_writeup_fenced_explanation_is_its_own_block():
    text = gen.render_writeup(
        dict(
            writeup_entry(),
            title="Encode and Decode Strings",
            lcSlug="encode-and-decode-strings",
            dirSlug="encode_and_decode_strings",
        ),
        gen.parse_metadata(PREMIUM_METADATA),
    )
    example_one = text.split("### Example 1")[1].split("### Example 2")[0]
    assert "**Explanation:** **" not in example_one
    explanation_block = example_one.split("**Explanation:**", 1)[1]
    assert explanation_block.lstrip().startswith("```java")
    assert "Solution solution = new Solution();" in explanation_block
    assert example_one.count("```") % 2 == 0
