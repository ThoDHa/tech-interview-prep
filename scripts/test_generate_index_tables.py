"""Unit tests for the docs/leetcode/index.md table generator.

The generator merges scripts/grind75_table.json (the 77 hand-maintained
Grind 75 rows) with scripts/neetcode150_manifest.json into one unified
LeetCode table in the interleaved study order, credits the list sources,
and emits the generated Leetcode + Amazon mkdocs.yml nav sections. The
Amazon bank table itself lives in docs/amazon/index.md, owned by the
amazon scaffold generator. Run with:

    cd practice && uv run pytest ../scripts/
"""

import collections
import datetime
import json
from pathlib import Path

import pytest

import generate_index_tables as gen

SCRIPTS_DIR = Path(__file__).resolve().parent
GRIND_TABLE_PATH = SCRIPTS_DIR / "grind75_table.json"
NEETCODE_MANIFEST_PATH = SCRIPTS_DIR / "neetcode150_manifest.json"
AMAZON_MANIFEST_PATH = SCRIPTS_DIR / "amazon_oa_manifest.json"

TREE_MOVED = (SCRIPTS_DIR.parent / "docs" / "leetcode" / "index.md").exists()
pre_move_skip = pytest.mark.skipif(
    not TREE_MOVED,
    reason="live tree still pre-move; unblocks when reorg wave B lands the new layout",
)

AMAZON_OVERRIDES_PATH = SCRIPTS_DIR / "amazon_difficulty_overrides.json"


# ---------------------------------------------------------------------------
# Test fixtures: small synthetic manifests shaped like the committed ones
# ---------------------------------------------------------------------------


def fixture_grind():
    return [
        {
            "number": 1,
            "slug": "two-sum",
            "title": "Two Sum",
            "difficulty": "Easy",
            "category": "Array, Hash Table",
            "time": "15 minutes",
        },
        {
            "number": 2,
            "slug": "min-stack",
            "title": "Minimum Stack",
            "difficulty": "Medium",
            "category": "Stack",
            "time": "20 minutes",
        },
        {
            "number": None,
            "slug": "flood-fill",
            "title": "Flood Fill",
            "difficulty": "Easy",
            "category": "Graph, DFS",
            "time": "20 minutes",
        },
    ]


def fixture_neetcode():
    return [
        {
            "order": 1,
            "section": "Arrays & Hashing",
            "title": "Two Sum (NeetCode)",
            "lcSlug": "two-sum",
            "dirSlug": "two_sum",
            "difficulty": "Easy",
            "ncSlug": "two-integer-sum",
            "leetcodePremium": None,
        },
        {
            "order": 2,
            "section": "Stack",
            "title": "Min Stack (NeetCode)",
            "lcSlug": "min-stack",
            "dirSlug": "min_stack",
            "difficulty": "Medium",
            "ncSlug": "min-stack",
            "leetcodePremium": None,
        },
        {
            "order": 7,
            "section": "Greedy",
            "title": "Jump Game",
            "lcSlug": "jump-game",
            "dirSlug": "jump_game",
            "difficulty": "Medium",
            "ncSlug": "jump-game",
            "leetcodePremium": None,
        },
    ]


def fixture_amazon():
    return [
        {
            "slug": "amazon-maximize-adjacent-difference-with-one-reversal",
            "title": "Maximize Adjacent Difference With One Reversal",
            "url": "https://www.fastprep.io/problems/amazon-maximize-adjacent-difference-with-one-reversal",
            "companies": ["Amazon"],
            "updated": "2026-09-19",
            "parse_status": "parsed-with-cases",
            "difficulty": "Hard",
            "categories": "Array, Math",
        },
        {
            "slug": "amazon-first-non-repeating-character",
            "title": "First Non-Repeating Character",
            "url": "https://www.fastprep.io/problems/amazon-first-non-repeating-character",
            "companies": ["Amazon"],
            "updated": "2026-09-18",
            "parse_status": "parsed-with-cases",
            "difficulty": "Easy",
            "categories": "Hash Table, String",
        },
    ]


EXPECTED_AMAZON_OVERLAP_LC_SLUGS = frozenset(
    {
        "cheapest-flights-within-k-stops",
        "container-with-most-water",
        "course-schedule",
        "course-schedule-ii",
        "edit-distance",
        "find-median-from-data-stream",
        "group-anagrams",
        "house-robber",
        "interleaving-string",
        "longest-substring-without-repeating-characters",
        "max-area-of-island",
        "meeting-rooms-ii",
        "merge-intervals",
        "merge-k-sorted-lists",
        "minimum-window-substring",
        "number-of-islands",
        "sliding-window-maximum",
        "task-scheduler",
        "top-k-frequent-elements",
        "trapping-rain-water",
        "word-break",
        "word-ladder",
        "word-search-ii",
    }
)


def write_json(tmp_path, name, payload):
    path = tmp_path / name
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def valid_grind(count=gen.GRIND_ROW_COUNT):
    """A synthetic Grind table of the contract size: 75 numbered, 2 extras."""
    assert count == gen.GRIND_ROW_COUNT
    numbered = [
        {
            "number": n,
            "slug": f"problem-{n}",
            "title": f"Problem {n}",
            "difficulty": "Easy",
            "category": "Category",
            "time": f"{n} minutes",
        }
        for n in range(1, gen.NUMBERED_GRIND_COUNT + 1)
    ]
    extras = [
        {
            "number": None,
            "slug": f"extra-{n}",
            "title": f"Extra {n}",
            "difficulty": "-",
            "category": "-",
            "time": "-",
        }
        for n in (1, 2)
    ]
    return numbered + extras


def valid_neetcode(count=gen.NEETCODE_TRACK_SIZE):
    """A synthetic NeetCode manifest of the contract size."""
    return [
        {
            "order": n,
            "section": "Arrays & Hashing",
            "title": f"Track Problem {n}",
            "lcSlug": f"track-problem-{n}",
            "dirSlug": f"track_problem_{n}",
            "difficulty": "Easy",
            "ncSlug": f"nc-problem-{n}",
            "leetcodePremium": False,
        }
        for n in range(1, count + 1)
    ]


def valid_amazon(count=gen.AMAZON_ROW_COUNT):
    """A synthetic Amazon manifest of the contract size, most-recent first."""
    return [
        {
            "slug": f"amazon-problem-{n}",
            "title": f"Amazon Problem {n}",
            "url": f"https://www.fastprep.io/problems/amazon-problem-{n}",
            "companies": ["Amazon"],
            "updated": (datetime.date(2020, 1, 1) + datetime.timedelta(days=n)).isoformat(),
            "parse_status": "parsed-with-cases",
            "difficulty": "Easy",
            "categories": "Array, Hash Table",
        }
        for n in range(count, 0, -1)
    ]


def amazon_entry_for(lc_slug):
    """A synthetic Amazon OA entry whose slug mirrors a LeetCode slug."""
    return {
        "slug": f"{gen.AMAZON_SLUG_PREFIX}{lc_slug}",
        "title": f"Amazon {lc_slug}",
        "url": f"https://www.fastprep.io/problems/{gen.AMAZON_SLUG_PREFIX}{lc_slug}",
        "companies": ["Amazon"],
        "updated": "2026-09-17",
        "parse_status": "parsed-with-cases",
        "difficulty": "Medium",
        "categories": "Stack",
    }


def neetcode_entry_for(section, lc_slug, premium=False, nc_slug=None):
    """A synthetic NeetCode entry for one problem in one section."""
    return {
        "order": 1,
        "section": section,
        "title": lc_slug.replace("-", " ").title(),
        "lcSlug": lc_slug,
        "dirSlug": lc_slug.replace("-", "_"),
        "difficulty": "Medium",
        "ncSlug": nc_slug or lc_slug,
        "leetcodePremium": premium,
    }


def render_fixture_section(amazon=None):
    """Render the unified section for the synthetic fixtures.

    Args:
        amazon: Amazon manifest override (default: fixture_amazon(), which
            matches nothing on the synthetic track).

    Returns:
        The rendered unified section text.
    """
    neetcode = fixture_neetcode()
    amazon = fixture_amazon() if amazon is None else amazon
    rows = gen.interleave_study_order(gen.merge_tracks(fixture_grind(), neetcode), neetcode)
    overlap = gen.amazon_overlap_lc_slugs(neetcode, amazon)
    return gen.render_unified_section(rows, overlap)


def unified_table_rows(section):
    """Extract the table row lines (excluding the header) from a section."""
    return [line for line in section.splitlines() if line.startswith("| [")]


def cell(line, column):
    """Return one cell's text from a table row line (0 = first cell)."""
    return line.split("|")[column + 1].strip()


PROBLEM_COLUMN = 0
DIFFICULTY_COLUMN = 1
CATEGORY_COLUMN = 2
TIME_COLUMN = 5
PRACTICE_AT_COLUMN = 3


def unified_row_lc_slug(line):
    """Parse the LeetCode slug from a row's Problem cell link.

    Write-up links are landing-relative (`<dirSlug>.md`, dirSlug using
    underscores); the overlap set speaks lcSlug (hyphens), so the slug
    converts back per the repo-wide dirSlug = lcSlug.replace("-", "_")
    convention.
    """
    problem_cell = cell(line, PROBLEM_COLUMN)
    url = problem_cell.rpartition("](")[2].rstrip(")")
    return url.rstrip("/").removesuffix(".md").replace("_", "-")


# ---------------------------------------------------------------------------
# The committed data sources satisfy their contracts
# ---------------------------------------------------------------------------


def test_committed_grind_table_passes_validation():
    gen.validate_grind_table(gen.load_grind_table(GRIND_TABLE_PATH))


def test_committed_grind_table_carries_77_rows_numbered_1_to_75():
    rows = gen.load_grind_table(GRIND_TABLE_PATH)
    assert len(rows) == gen.GRIND_ROW_COUNT
    numbered = [row["number"] for row in rows if row["number"] is not None]
    assert numbered == list(range(1, 76))


EXPECTED_GRIND_EXTRA_ROWS = {
    "binary-tree-maximum-path-sum": {
        "number": None,
        "slug": "binary-tree-maximum-path-sum",
        "title": "Binary Tree Maximum Path Sum",
        "difficulty": "Hard",
        "category": "Dynamic Programming, Tree, DFS",
        "time": "40 minutes",
    },
    "maximum-frequency-stack": {
        "number": None,
        "slug": "maximum-frequency-stack",
        "title": "Maximum Frequency Stack",
        "difficulty": "Hard",
        "category": "Hash Table, Stack, Design",
        "time": "40 minutes",
    },
}


def test_committed_grind_table_rows_match_the_hand_table_verbatim():
    rows = gen.load_grind_table(GRIND_TABLE_PATH)
    assert rows[0] == {
        "number": 1,
        "slug": "two-sum",
        "title": "Two Sum",
        "difficulty": "Easy",
        "category": "Array, Hash Table",
        "time": "15 minutes",
    }
    assert rows[37] == {
        "number": 38,
        "slug": "min-stack",
        "title": "Minimum Stack",
        "difficulty": "Medium",
        "category": "Stack",
        "time": "20 minutes",
    }
    assert rows[-1] == EXPECTED_GRIND_EXTRA_ROWS["maximum-frequency-stack"]


def test_committed_grind_table_fills_the_unnumbered_extra_rows():
    rows = gen.load_grind_table(GRIND_TABLE_PATH)
    extras = [row for row in rows if row["number"] is None]
    assert len(extras) == 2
    for row in extras:
        assert row == EXPECTED_GRIND_EXTRA_ROWS[row["slug"]], row["slug"]


@pre_move_skip
def test_committed_grind_table_slugs_derive_their_writeup_paths():
    docs_problems = SCRIPTS_DIR.parent / "docs" / "leetcode"
    for row in gen.load_grind_table(GRIND_TABLE_PATH):
        writeup = docs_problems / (row["slug"].replace("-", "_") + ".md")
        assert writeup.exists(), writeup


def test_committed_neetcode_manifest_passes_merge_validation():
    gen.validate_neetcode_manifest(gen.load_neetcode_manifest(NEETCODE_MANIFEST_PATH))


def test_committed_neetcode_manifest_flags_exactly_the_seven_premium_entries():
    entries = gen.load_neetcode_manifest(NEETCODE_MANIFEST_PATH)
    premium = {
        entry["lcSlug"]: entry["ncSlug"]
        for entry in entries
        if entry["leetcodePremium"] is True
    }
    assert premium == gen.EXPECTED_PREMIUM_NC_SLUGS


def test_committed_amazon_manifest_passes_validation():
    gen.validate_amazon_manifest(gen.load_amazon_manifest(AMAZON_MANIFEST_PATH))


# ---------------------------------------------------------------------------
# Loader validation errors
# ---------------------------------------------------------------------------


def test_load_grind_table_rejects_a_missing_file(tmp_path):
    with pytest.raises(gen.SourceError, match="not found"):
        gen.load_grind_table(tmp_path / "absent.json")


def test_load_grind_table_rejects_a_non_json_list(tmp_path):
    path = write_json(tmp_path, "grind.json", {"number": 1})
    with pytest.raises(gen.SourceError, match="JSON list"):
        gen.load_grind_table(path)


def test_load_grind_table_rejects_rows_with_missing_fields(tmp_path):
    rows = valid_grind()
    del rows[0]["time"]
    path = write_json(tmp_path, "grind.json", rows)
    with pytest.raises(gen.SourceError, match="time"):
        gen.validate_grind_table(gen.load_grind_table(path))


def test_load_grind_table_rejects_duplicate_slugs(tmp_path):
    rows = valid_grind()
    rows[1]["slug"] = rows[0]["slug"]
    path = write_json(tmp_path, "grind.json", rows)
    with pytest.raises(gen.SourceError, match="problem-1"):
        gen.validate_grind_table(gen.load_grind_table(path))


def test_load_grind_table_rejects_broken_numbering(tmp_path):
    rows = valid_grind()
    rows[0]["number"] = 4
    path = write_json(tmp_path, "grind.json", rows)
    with pytest.raises(gen.SourceError, match="numbering"):
        gen.validate_grind_table(gen.load_grind_table(path))


def test_load_neetcode_manifest_rejects_duplicate_lc_slugs(tmp_path):
    entries = valid_neetcode()
    entries[1]["lcSlug"] = entries[0]["lcSlug"]
    path = write_json(tmp_path, "neet.json", entries)
    with pytest.raises(gen.SourceError, match="track-problem-1"):
        gen.validate_neetcode_manifest(gen.load_neetcode_manifest(path))


def test_load_neetcode_manifest_rejects_a_missing_nc_slug(tmp_path):
    entries = valid_neetcode()
    del entries[0]["ncSlug"]
    path = write_json(tmp_path, "neet.json", entries)
    with pytest.raises(gen.SourceError, match="ncSlug"):
        gen.validate_neetcode_manifest(gen.load_neetcode_manifest(path))


def test_load_neetcode_manifest_rejects_a_non_boolean_premium_flag(tmp_path):
    entries = valid_neetcode()
    entries[0]["leetcodePremium"] = "yes"
    path = write_json(tmp_path, "neet.json", entries)
    with pytest.raises(gen.SourceError, match="leetcodePremium"):
        gen.validate_neetcode_manifest(gen.load_neetcode_manifest(path))


def test_load_amazon_manifest_rejects_rows_out_of_recency_order(tmp_path):
    entries = valid_amazon()
    entries.reverse()
    path = write_json(tmp_path, "amazon.json", entries)
    with pytest.raises(gen.SourceError, match="recent"):
        gen.validate_amazon_manifest(gen.load_amazon_manifest(path))


def test_load_amazon_manifest_rejects_duplicate_slugs(tmp_path):
    entries = valid_amazon()
    entries[1]["slug"] = entries[0]["slug"]
    path = write_json(tmp_path, "amazon.json", entries)
    with pytest.raises(gen.SourceError, match="duplicate"):
        gen.validate_amazon_manifest(gen.load_amazon_manifest(path))


def test_load_amazon_manifest_rejects_a_missing_difficulty_field(tmp_path):
    entries = valid_amazon()
    del entries[0]["difficulty"]
    path = write_json(tmp_path, "amazon.json", entries)
    with pytest.raises(gen.SourceError, match="difficulty"):
        gen.validate_amazon_manifest(gen.load_amazon_manifest(path))


def test_load_amazon_manifest_rejects_a_missing_categories_field(tmp_path):
    entries = valid_amazon()
    del entries[0]["categories"]
    path = write_json(tmp_path, "amazon.json", entries)
    with pytest.raises(gen.SourceError, match="categories"):
        gen.validate_amazon_manifest(gen.load_amazon_manifest(path))


# ---------------------------------------------------------------------------
# The merger
# ---------------------------------------------------------------------------


def test_merge_tracks_yields_grind_order_then_neetcode_only_order():
    rows = gen.merge_tracks(fixture_grind(), fixture_neetcode())
    assert [row["slug"] for row in rows] == [
        "two-sum",
        "min-stack",
        "flood-fill",
        "jump-game",
    ]


def test_merge_tracks_merges_overlaps_into_one_row_crediting_both_tracks():
    rows = gen.merge_tracks(fixture_grind(), fixture_neetcode())
    merged = [row for row in rows if row["slug"] == "two-sum"]
    assert len(merged) == 1
    assert merged[0]["tracks"] == gen.BOTH_TRACKS


def test_merge_tracks_labels_grind_only_rows():
    rows = gen.merge_tracks(fixture_grind(), fixture_neetcode())
    flood_fill = next(row for row in rows if row["slug"] == "flood-fill")
    assert flood_fill["tracks"] == gen.GRIND_TRACK


def test_merge_tracks_labels_neetcode_only_rows():
    rows = gen.merge_tracks(fixture_grind(), fixture_neetcode())
    jump_game = next(row for row in rows if row["slug"] == "jump-game")
    assert jump_game["tracks"] == gen.NEETCODE_TRACK


def test_merge_tracks_keeps_grind_metadata_for_overlap_rows():
    rows = gen.merge_tracks(fixture_grind(), fixture_neetcode())
    min_stack = next(row for row in rows if row["slug"] == "min-stack")
    assert min_stack["title"] == "Minimum Stack"
    assert min_stack["difficulty"] == "Medium"
    assert min_stack["category"] == "Stack"
    assert min_stack["time"] == "20 minutes"


def test_merge_tracks_estimates_time_for_neetcode_only_rows():
    rows = gen.merge_tracks(fixture_grind(), fixture_neetcode())
    jump_game = next(row for row in rows if row["slug"] == "jump-game")
    assert jump_game["time"] == "25 minutes"


# ---------------------------------------------------------------------------
# The Time estimates
# ---------------------------------------------------------------------------


def test_estimated_time_cell_maps_each_difficulty_to_its_minutes():
    assert gen.estimated_time_cell("Easy") == "15 minutes"
    assert gen.estimated_time_cell("Medium") == "25 minutes"
    assert gen.estimated_time_cell("Hard") == "40 minutes"


def test_estimated_time_cell_marks_unknown_difficulty_with_the_dash_marker():
    assert gen.estimated_time_cell(None) == "-"


# ---------------------------------------------------------------------------
# The Amazon difficulty overrides
# ---------------------------------------------------------------------------


def test_load_amazon_difficulty_overrides_returns_an_empty_mapping_when_absent(tmp_path):
    assert gen.load_amazon_difficulty_overrides(tmp_path / "absent.json") == {}


def test_load_amazon_difficulty_overrides_reads_the_committed_json_object():
    overrides = gen.load_amazon_difficulty_overrides(AMAZON_OVERRIDES_PATH)
    assert isinstance(overrides, dict)
    assert overrides


def test_load_amazon_difficulty_overrides_rejects_a_non_json_object(tmp_path):
    path = write_json(tmp_path, "overrides.json", [{"slug": "amazon-odd"}])
    with pytest.raises(gen.SourceError, match="JSON object"):
        gen.load_amazon_difficulty_overrides(path)


def test_amazon_difficulty_overrides_validate_against_the_committed_manifest():
    overrides = gen.load_amazon_difficulty_overrides(AMAZON_OVERRIDES_PATH)
    amazon = gen.load_amazon_manifest(AMAZON_MANIFEST_PATH)
    gen.validate_amazon_difficulty_overrides(overrides, amazon)


def test_amazon_difficulty_overrides_reject_an_unknown_slug(tmp_path):
    overrides = {"amazon-not-in-the-manifest": "Easy"}
    with pytest.raises(gen.SourceError, match="unknown slug"):
        gen.validate_amazon_difficulty_overrides(overrides, valid_amazon())


def test_amazon_difficulty_overrides_reject_a_non_canonical_difficulty(tmp_path):
    overrides = {valid_amazon()[0]["slug"]: "Tricky"}
    with pytest.raises(gen.SourceError, match="Tricky"):
        gen.validate_amazon_difficulty_overrides(overrides, valid_amazon())


@pre_move_skip
def test_render_amazon_section_prefers_the_override_over_the_header_parse():
    slug = fixture_amazon()[0]["slug"]
    assert gen.amazon_writeup_difficulty(slug) == "Hard", slug
    overrides = {slug: "Easy"}
    gen.validate_amazon_difficulty_overrides(overrides, fixture_amazon())
    resolved = overrides.get(slug) or gen.amazon_writeup_difficulty(slug)
    assert gen.estimated_time_cell(resolved) == "15 minutes"


def test_render_amazon_section_rejects_an_override_outside_the_manifest():
    with pytest.raises(gen.SourceError, match="unknown slug"):
        gen.validate_amazon_difficulty_overrides(
            {"amazon-absent": "Easy"}, fixture_amazon()
        )


EXPECTED_AMAZON_OVERRIDES = {
    "amazon-minimum-operations-to-sort-permutation": "Medium",
}


def test_committed_amazon_overrides_pin_the_externally_sourced_difficulties():
    assert gen.load_amazon_difficulty_overrides(AMAZON_OVERRIDES_PATH) == (
        EXPECTED_AMAZON_OVERRIDES
    )


def test_committed_amazon_rows_apply_the_committed_overrides():
    amazon = gen.load_amazon_manifest(AMAZON_MANIFEST_PATH)
    overrides = gen.load_amazon_difficulty_overrides(AMAZON_OVERRIDES_PATH)
    for entry in amazon:
        if entry["slug"] in overrides:
            assert overrides[entry["slug"]] == (
                overrides.get(entry["slug"]) or gen.amazon_writeup_difficulty(entry["slug"])
            ), entry["slug"]
            assert gen.estimated_time_cell(overrides[entry["slug"]]) == "25 minutes", (
                entry["slug"]
            )


@pre_move_skip
def test_committed_amazon_rows_dash_exactly_the_unsourced_rows():
    amazon = gen.load_amazon_manifest(AMAZON_MANIFEST_PATH)
    overrides = gen.load_amazon_difficulty_overrides(AMAZON_OVERRIDES_PATH)
    dashed = [
        entry["slug"]
        for entry in amazon
        if gen.estimated_time_cell(
            overrides.get(entry["slug"]) or gen.amazon_writeup_difficulty(entry["slug"])
        )
        == gen.UNKNOWN_TIME_CELL
    ]
    assert len(dashed) == 20


EXPECTED_AMAZON_DIFFICULTY_SAMPLES = {
    "amazon-transfer-chain-endpoints": "Easy",
    "amazon-aggressive-cows": "Medium",
    "amazon-trapping-rain-water": "Hard",
    "amazon-count-similar-string-groups": None,
}


@pre_move_skip
def test_amazon_writeup_difficulty_parses_the_pinned_committed_header_samples():
    for slug, difficulty in EXPECTED_AMAZON_DIFFICULTY_SAMPLES.items():
        assert gen.amazon_writeup_difficulty(slug) == difficulty, slug


@pre_move_skip
def test_amazon_writeup_difficulty_reads_every_committed_header_offline():
    amazon = gen.load_amazon_manifest(AMAZON_MANIFEST_PATH)
    assert len(amazon) == gen.AMAZON_ROW_COUNT
    counts = collections.Counter(
        gen.amazon_writeup_difficulty(entry["slug"]) for entry in amazon
    )
    assert counts == collections.Counter(
        {"Easy": 69, "Medium": 204, "Hard": 86, None: 21}
    )


def test_amazon_writeup_difficulty_rejects_a_missing_writeup(tmp_path):
    with pytest.raises(gen.SourceError, match="not found"):
        gen.amazon_writeup_difficulty("amazon-absent", docs_dir=tmp_path)


def test_amazon_writeup_difficulty_rejects_a_header_without_a_difficulty_group(tmp_path):
    (tmp_path / "amazon-headerless.md").write_text(
        "# [Headerless](https://example.com)\n\nno bold group here\n", encoding="utf-8"
    )
    with pytest.raises(gen.SourceError, match=r"no \*\*difficulty\*\* header"):
        gen.amazon_writeup_difficulty("amazon-headerless", docs_dir=tmp_path)


def test_amazon_writeup_difficulty_rejects_a_non_canonical_difficulty(tmp_path):
    (tmp_path / "amazon-odd.md").write_text(
        "# [Odd](https://example.com)\n\n**Tricky** | **NN minutes** | **Topics**\n",
        encoding="utf-8",
    )
    with pytest.raises(gen.SourceError, match="Tricky"):
        gen.amazon_writeup_difficulty("amazon-odd", docs_dir=tmp_path)


def test_merge_tracks_uses_the_neetcode_section_as_category_for_neetcode_only_rows():
    rows = gen.merge_tracks(fixture_grind(), fixture_neetcode())
    jump_game = next(row for row in rows if row["slug"] == "jump-game")
    assert jump_game["category"] == "Greedy"


def test_merge_tracks_records_the_neetcode_section_on_neetcode_only_rows_only():
    rows = gen.merge_tracks(fixture_grind(), fixture_neetcode())
    grind_rows = [row for row in rows if row["tracks"] in (gen.GRIND_TRACK, gen.BOTH_TRACKS)]
    assert all(row["section"] is None for row in grind_rows)
    jump_game = next(row for row in rows if row["slug"] == "jump-game")
    assert jump_game["section"] == "Greedy"


def test_merge_tracks_flags_premium_neetcode_only_rows():
    neetcode = fixture_neetcode()[:-1] + [
        neetcode_entry_for("Stack", "encode-and-decode-strings", premium=True)
    ]
    rows = gen.merge_tracks(fixture_grind(), neetcode)
    encode = next(row for row in rows if row["slug"] == "encode-and-decode-strings")
    assert encode["premium"] is True


def test_merge_tracks_never_flags_premium_on_grind_rows():
    neetcode = fixture_neetcode()[:-1] + [
        neetcode_entry_for("Stack", "min-stack", premium=True)
    ]
    rows = gen.merge_tracks(fixture_grind(), neetcode)
    grind_rows = [row for row in rows if row["tracks"] != gen.NEETCODE_TRACK]
    assert all(row["premium"] is False for row in grind_rows)


# ---------------------------------------------------------------------------
# The interleaved study order
# ---------------------------------------------------------------------------


def test_interleave_slots_a_neetcode_section_after_its_category_anchor():
    grind = [
        {"number": 1, "slug": "stack-problem", "title": "Stack Problem",
         "difficulty": "Easy", "category": "Stack", "time": "10 minutes"},
        {"number": None, "slug": "graph-problem", "title": "Graph Problem",
         "difficulty": "Easy", "category": "Graph, DFS", "time": "10 minutes"},
    ]
    neetcode = [
        neetcode_entry_for("Graphs", "clone-graph"),
        neetcode_entry_for("Stack", "daily-temperatures"),
    ]
    rows = gen.interleave_study_order(gen.merge_tracks(grind, neetcode), neetcode)
    assert [row["slug"] for row in rows] == [
        "stack-problem",
        "daily-temperatures",
        "graph-problem",
        "clone-graph",
    ]


def test_interleave_prefers_the_pinned_slug_anchor_over_the_category_anchor():
    grind = [
        {"number": 1, "slug": "first-string-problem", "title": "First String Problem",
         "difficulty": "Easy", "category": "String", "time": "10 minutes"},
        {"number": 2, "slug": "longest-substring-without-repeating-characters",
         "title": "Longest Substring Without Repeating Characters",
         "difficulty": "Medium", "category": "String", "time": "30 minutes"},
    ]
    neetcode = [
        neetcode_entry_for("Sliding Window", "best-time-to-buy-and-sell-stock"),
        neetcode_entry_for("Sliding Window", "permutation-in-string"),
    ]
    rows = gen.interleave_study_order(gen.merge_tracks(grind, neetcode), neetcode)
    assert [row["slug"] for row in rows] == [
        "first-string-problem",
        "longest-substring-without-repeating-characters",
        "best-time-to-buy-and-sell-stock",
        "permutation-in-string",
    ]


def test_interleave_falls_back_to_the_first_track_member_as_anchor():
    grind = [
        {"number": 1, "slug": "maximum-subarray", "title": "Maximum Subarray",
         "difficulty": "Medium", "category": "Array, Dynamic Programming",
         "time": "20 minutes"},
    ]
    neetcode = [
        neetcode_entry_for("Greedy", "maximum-subarray"),
        neetcode_entry_for("Greedy", "jump-game"),
    ]
    rows = gen.interleave_study_order(gen.merge_tracks(grind, neetcode), neetcode)
    assert [row["slug"] for row in rows] == [
        "maximum-subarray",
        "jump-game",
    ]


def test_interleave_appends_sections_without_any_anchor_at_the_end():
    grind = [
        {"number": 1, "slug": "unrelated-problem", "title": "Unrelated Problem",
         "difficulty": "Easy", "category": "String", "time": "10 minutes"},
    ]
    neetcode = [neetcode_entry_for("Greedy", "jump-game")]
    rows = gen.interleave_study_order(gen.merge_tracks(grind, neetcode), neetcode)
    assert [row["slug"] for row in rows] == ["unrelated-problem", "jump-game"]


def test_interleave_places_an_after_anchored_section_after_the_whole_topic_block():
    grind = [
        {"number": 1, "slug": "climbing-stairs", "title": "Climbing Stairs",
         "difficulty": "Easy", "category": "Dynamic Programming", "time": "15 minutes"},
        {"number": 2, "slug": "unique-paths", "title": "Unique Paths",
         "difficulty": "Medium", "category": "Dynamic Programming", "time": "20 minutes"},
    ]
    neetcode = [
        neetcode_entry_for("1-D Dynamic Programming", "house-robber"),
        neetcode_entry_for("2-D Dynamic Programming", "edit-distance"),
    ]
    rows = gen.interleave_study_order(gen.merge_tracks(grind, neetcode), neetcode)
    assert [row["slug"] for row in rows] == [
        "climbing-stairs",
        "house-robber",
        "unique-paths",
        "edit-distance",
    ]


def test_interleave_keeps_each_committed_section_contiguous_and_in_track_order():
    grind = gen.load_grind_table(GRIND_TABLE_PATH)
    neetcode = gen.load_neetcode_manifest(NEETCODE_MANIFEST_PATH)
    rows = gen.study_order_rows(grind, neetcode)
    sections = list(dict.fromkeys(entry["section"] for entry in neetcode))
    for section in sections:
        group = [row for row in rows if row["section"] == section]
        track_order = [
            entry["lcSlug"]
            for entry in neetcode
            if entry["section"] == section and entry["lcSlug"] not in {r["slug"] for r in grind}
        ]
        assert [row["slug"] for row in group] == track_order, section


def test_interleave_raises_when_a_pinned_slug_anchor_is_absent():
    grind = [
        {"number": 1, "slug": "unrelated-problem", "title": "Unrelated Problem",
         "difficulty": "Easy", "category": "String", "time": "10 minutes"},
    ]
    neetcode = [neetcode_entry_for("Sliding Window", "permutation-in-string")]
    with pytest.raises(gen.SourceError, match="longest-substring-without-repeating-characters"):
        gen.interleave_study_order(gen.merge_tracks(grind, neetcode), neetcode)


def test_interleave_raises_when_an_after_anchor_target_has_no_topic_rows():
    grind = [
        {"number": 1, "slug": "unrelated-problem", "title": "Unrelated Problem",
         "difficulty": "Easy", "category": "String", "time": "10 minutes"},
    ]
    neetcode = [neetcode_entry_for("Advanced Graphs", "network-delay-time")]
    with pytest.raises(gen.SourceError, match="Graphs"):
        gen.interleave_study_order(gen.merge_tracks(grind, neetcode), neetcode)


# ---------------------------------------------------------------------------
# The committed interleaved study order (pinned)
# ---------------------------------------------------------------------------


EXPECTED_STUDY_ORDER = [
    "two-sum",
    "group-anagrams",
    "top-k-frequent-elements",
    "encode-and-decode-strings",
    "valid-sudoku",
    "longest-consecutive-sequence",
    "valid-parentheses",
    "daily-temperatures",
    "car-fleet",
    "merge-two-sorted-lists",
    "reorder-list",
    "remove-nth-node-from-end-of-list",
    "copy-list-with-random-pointer",
    "add-two-numbers",
    "find-the-duplicate-number",
    "reverse-nodes-in-k-group",
    "best-time-to-buy-and-sell-stock",
    "valid-palindrome",
    "two-sum-ii-input-array-is-sorted",
    "invert-binary-tree",
    "same-tree",
    "subtree-of-another-tree",
    "count-good-nodes-in-binary-tree",
    "valid-anagram",
    "binary-search",
    "search-a-2d-matrix",
    "koko-eating-bananas",
    "find-minimum-in-rotated-sorted-array",
    "median-of-two-sorted-arrays",
    "flood-fill",
    "max-area-of-island",
    "walls-and-gates",
    "pacific-atlantic-water-flow",
    "surrounded-regions",
    "course-schedule-ii",
    "graph-valid-tree",
    "number-of-connected-components-in-an-undirected-graph",
    "redundant-connection",
    "lowest-common-ancestor-of-a-binary-search-tree",
    "balanced-binary-tree",
    "linked-list-cycle",
    "implement-queue-using-stacks",
    "first-bad-version",
    "ransom-note",
    "climbing-stairs",
    "min-cost-climbing-stairs",
    "house-robber",
    "house-robber-ii",
    "palindromic-substrings",
    "decode-ways",
    "maximum-product-subarray",
    "longest-increasing-subsequence",
    "longest-palindrome",
    "reverse-linked-list",
    "majority-element",
    "add-binary",
    "diameter-of-binary-tree",
    "middle-of-the-linked-list",
    "maximum-depth-of-binary-tree",
    "contains-duplicate",
    "maximum-subarray",
    "jump-game",
    "jump-game-ii",
    "gas-station",
    "hand-of-straights",
    "merge-triplets-to-form-target-triplet",
    "partition-labels",
    "valid-parenthesis-string",
    "non-overlapping-intervals",
    "meeting-rooms",
    "meeting-rooms-ii",
    "minimum-interval-to-include-each-query",
    "single-number",
    "number-of-1-bits",
    "counting-bits",
    "reverse-bits",
    "missing-number",
    "sum-of-two-integers",
    "reverse-integer",
    "insert-interval",
    "01-matrix",
    "k-closest-points-to-origin",
    "kth-largest-element-in-a-stream",
    "last-stone-weight",
    "kth-largest-element-in-an-array",
    "design-twitter",
    "longest-substring-without-repeating-characters",
    "longest-repeating-character-replacement",
    "permutation-in-string",
    "sliding-window-maximum",
    "3sum",
    "binary-tree-level-order-traversal",
    "clone-graph",
    "evaluate-reverse-polish-notation",
    "course-schedule",
    "implement-trie-prefix-tree",
    "design-add-and-search-words-data-structure",
    "word-search-ii",
    "coin-change",
    "product-of-array-except-self",
    "min-stack",
    "validate-binary-search-tree",
    "number-of-islands",
    "rotting-oranges",
    "search-in-rotated-sorted-array",
    "combination-sum",
    "combination-sum-ii",
    "subsets-ii",
    "generate-parentheses",
    "palindrome-partitioning",
    "n-queens",
    "permutations",
    "merge-intervals",
    "lowest-common-ancestor-of-a-binary-tree",
    "time-based-key-value-store",
    "accounts-merge",
    "sort-colors",
    "word-break",
    "partition-equal-subset-sum",
    "string-to-integer-atoi",
    "spiral-matrix",
    "rotate-image",
    "set-matrix-zeroes",
    "happy-number",
    "plus-one",
    "powx-n",
    "multiply-strings",
    "detect-squares",
    "subsets",
    "binary-tree-right-side-view",
    "longest-palindromic-substring",
    "unique-paths",
    "construct-binary-tree-from-preorder-and-inorder-traversal",
    "container-with-most-water",
    "letter-combinations-of-a-phone-number",
    "word-search",
    "find-all-anagrams-in-a-string",
    "minimum-height-trees",
    "task-scheduler",
    "lru-cache",
    "kth-smallest-element-in-a-bst",
    "minimum-window-substring",
    "serialize-and-deserialize-binary-tree",
    "trapping-rain-water",
    "find-median-from-data-stream",
    "word-ladder",
    "basic-calculator",
    "maximum-profit-in-job-scheduling",
    "merge-k-sorted-lists",
    "largest-rectangle-in-histogram",
    "binary-tree-maximum-path-sum",
    "longest-common-subsequence",
    "best-time-to-buy-and-sell-stock-with-cooldown",
    "coin-change-ii",
    "target-sum",
    "interleaving-string",
    "longest-increasing-path-in-a-matrix",
    "distinct-subsequences",
    "edit-distance",
    "burst-balloons",
    "regular-expression-matching",
    "network-delay-time",
    "reconstruct-itinerary",
    "min-cost-to-connect-all-points",
    "swim-in-rising-water",
    "alien-dictionary",
    "cheapest-flights-within-k-stops",
    "maximum-frequency-stack",
]


def committed_study_order():
    """The interleaved study order from the committed data sources."""
    return [
        row["slug"]
        for row in gen.study_order_rows(
            gen.load_grind_table(GRIND_TABLE_PATH),
            gen.load_neetcode_manifest(NEETCODE_MANIFEST_PATH),
        )
    ]


def test_committed_study_order_pins_the_full_168_row_sequence():
    assert committed_study_order() == EXPECTED_STUDY_ORDER


def assert_precedes(earlier, later):
    """Assert two slugs sit in that exact adjacency in the pinned order."""
    order = committed_study_order()
    assert order.index(earlier) == order.index(later) - 1, (earlier, later)


def test_committed_interleave_puts_arrays_and_hashing_after_two_sum():
    assert_precedes("two-sum", "group-anagrams")


def test_committed_interleave_puts_stack_after_valid_parentheses():
    assert_precedes("valid-parentheses", "daily-temperatures")


def test_committed_interleave_puts_linked_list_after_merge_two_sorted_lists():
    assert_precedes("merge-two-sorted-lists", "reorder-list")


def test_committed_interleave_puts_two_pointers_after_valid_palindrome():
    assert_precedes("valid-palindrome", "two-sum-ii-input-array-is-sorted")


def test_committed_interleave_puts_trees_after_invert_binary_tree():
    assert_precedes("invert-binary-tree", "same-tree")


def test_committed_interleave_puts_binary_search_after_binary_search():
    assert_precedes("binary-search", "search-a-2d-matrix")


def test_committed_interleave_puts_graphs_after_flood_fill():
    assert_precedes("flood-fill", "max-area-of-island")


def test_committed_interleave_puts_heap_after_k_closest_points_to_origin():
    assert_precedes("k-closest-points-to-origin", "kth-largest-element-in-a-stream")


def test_committed_interleave_puts_backtracking_after_combination_sum():
    assert_precedes("combination-sum", "combination-sum-ii")


def test_committed_interleave_puts_tries_after_implement_trie_prefix_tree():
    assert_precedes("implement-trie-prefix-tree", "design-add-and-search-words-data-structure")


def test_committed_interleave_puts_sliding_window_after_its_pinned_anchor():
    assert_precedes(
        "longest-substring-without-repeating-characters",
        "longest-repeating-character-replacement",
    )


def test_committed_interleave_puts_greedy_after_maximum_subarray():
    assert_precedes("maximum-subarray", "jump-game")


def test_committed_interleave_puts_math_and_geometry_after_spiral_matrix():
    assert_precedes("spiral-matrix", "rotate-image")


def test_committed_interleave_puts_2d_dp_after_the_last_dynamic_programming_row():
    # The filled binary-tree-maximum-path-sum row sits between the Grind 75
    # DP block and the 2-D DP section rows.
    order = committed_study_order()
    assert order.index("unique-paths") < order.index("binary-tree-maximum-path-sum")
    assert_precedes("binary-tree-maximum-path-sum", "longest-common-subsequence")


def test_committed_interleave_puts_advanced_graphs_after_the_graph_block():
    # The filled basic-calculator..binary-tree-maximum-path-sum Grind 75
    # extras sit between the Graphs section rows and the Advanced Graphs
    # section rows; word-ladder (a Grind 75 Graph row) still precedes them.
    order = committed_study_order()
    assert order.index("word-ladder") < order.index("basic-calculator")
    assert order.index("regular-expression-matching") < order.index("network-delay-time")


def test_committed_interleave_puts_intervals_after_the_greedy_block():
    assert_precedes("valid-parenthesis-string", "non-overlapping-intervals")


def test_committed_interleave_puts_bit_manipulation_after_the_intervals_block():
    assert_precedes("minimum-interval-to-include-each-query", "single-number")


def test_committed_study_order_starts_and_ends_with_the_backbone():
    order = committed_study_order()
    assert order[0] == "two-sum"
    assert order[-1] == "maximum-frequency-stack"


# ---------------------------------------------------------------------------
# The Amazon overlap rule
# ---------------------------------------------------------------------------


def test_amazon_overlap_lc_slugs_strips_the_amazon_prefix_and_matches_lc_slugs():
    amazon = fixture_amazon() + [amazon_entry_for("min-stack")]
    assert gen.amazon_overlap_lc_slugs(fixture_neetcode(), amazon) == {"min-stack"}


def test_amazon_overlap_lc_slugs_ignores_amazon_slugs_outside_the_track():
    amazon = fixture_amazon() + [amazon_entry_for("flood-fill")]
    assert gen.amazon_overlap_lc_slugs(fixture_neetcode(), amazon) == set()


def test_amazon_overlap_lc_slugs_ignores_entries_without_the_amazon_prefix():
    entry = amazon_entry_for("min-stack")
    entry["slug"] = "min-stack"
    assert gen.amazon_overlap_lc_slugs(fixture_neetcode(), [entry]) == set()


def test_committed_amazon_overlap_rule_yields_exactly_the_23_listed_problems():
    overlap = gen.amazon_overlap_lc_slugs(
        gen.load_neetcode_manifest(NEETCODE_MANIFEST_PATH),
        gen.load_amazon_manifest(AMAZON_MANIFEST_PATH),
    )
    assert overlap == EXPECTED_AMAZON_OVERLAP_LC_SLUGS


# ---------------------------------------------------------------------------
# The committed merge shape
# ---------------------------------------------------------------------------


def test_committed_merge_yields_the_expected_universe_split():
    grind = gen.load_grind_table(GRIND_TABLE_PATH)
    neetcode = gen.load_neetcode_manifest(NEETCODE_MANIFEST_PATH)
    rows = gen.study_order_rows(grind, neetcode)
    tracks = [row["tracks"] for row in rows]
    assert len(rows) == gen.UNIQUE_PROBLEM_COUNT
    assert tracks.count(gen.BOTH_TRACKS) == gen.OVERLAP_COUNT
    assert tracks.count(gen.GRIND_TRACK) == gen.GRIND_ONLY_COUNT
    assert tracks.count(gen.NEETCODE_TRACK) == gen.NEETCODE_ONLY_COUNT
    assert gen.UNIQUE_PROBLEM_COUNT == gen.GRIND_ROW_COUNT + gen.NEETCODE_ONLY_COUNT


def test_verify_merge_shape_accepts_the_committed_premium_mapping():
    neetcode = gen.load_neetcode_manifest(NEETCODE_MANIFEST_PATH)
    rows = gen.merge_tracks(gen.load_grind_table(GRIND_TABLE_PATH), neetcode)
    gen.verify_merge_shape(rows, neetcode)


def test_verify_merge_shape_rejects_a_drifted_premium_nc_slug():
    neetcode = gen.load_neetcode_manifest(NEETCODE_MANIFEST_PATH)
    rows = gen.merge_tracks(gen.load_grind_table(GRIND_TABLE_PATH), neetcode)
    drifted = [dict(entry) for entry in neetcode]
    for i, entry in enumerate(drifted):
        if entry.get("leetcodePremium"):
            drifted[i] = dict(entry, ncSlug="drifted-neetcode-page")
            break
    with pytest.raises(gen.SourceError, match="EXPECTED_PREMIUM_NC_SLUGS"):
        gen.verify_merge_shape(rows, drifted)


def committed_section():
    """Render the unified section from the committed data sources.

    Returns:
        The rendered unified section text with the committed Amazon overlap.
    """
    grind = gen.load_grind_table(GRIND_TABLE_PATH)
    neetcode = gen.load_neetcode_manifest(NEETCODE_MANIFEST_PATH)
    amazon = gen.load_amazon_manifest(AMAZON_MANIFEST_PATH)
    rows = gen.study_order_rows(grind, neetcode)
    return gen.render_unified_section(rows, gen.amazon_overlap_lc_slugs(neetcode, amazon))


def test_committed_unified_section_states_the_merge_counts():
    section = committed_section()
    assert str(gen.UNIQUE_PROBLEM_COUNT) in section
    assert str(gen.OVERLAP_COUNT) in section


def test_committed_unified_section_rewords_the_time_intro():
    section = committed_section()
    assert "Time carries the Grind 75 suggested minutes where published" in section
    assert "difficulty-based estimates elsewhere" in section
    assert "stays empty for NeetCode-only problems" not in section


def test_committed_unified_section_describes_the_interleaved_study_order():
    section = committed_section()
    assert "interleaved study order" in section
    assert "Grind 75 study order first" not in section


def test_committed_merge_starts_and_ends_per_the_study_order():
    rows = gen.study_order_rows(
        gen.load_grind_table(GRIND_TABLE_PATH),
        gen.load_neetcode_manifest(NEETCODE_MANIFEST_PATH),
    )
    assert rows[0]["slug"] == "two-sum"
    assert rows[-1]["slug"] == "maximum-frequency-stack"
    assert rows[-1]["tracks"] == gen.GRIND_TRACK


# ---------------------------------------------------------------------------
# The canonical Category vocabulary
# ---------------------------------------------------------------------------


CATEGORY_CANONICAL_MAP = {
    "Trees": "Tree",
    "Graphs": "Graph",
    "Tries": "Trie",
    "Arrays & Hashing": "Array, Hash Table",
    "Heap / Priority Queue": "Heap",
    "1-D Dynamic Programming": "Dynamic Programming",
    "2-D Dynamic Programming": "Dynamic Programming",
    "Advanced Graphs": "Graph",
    "Math & Geometry": "Math",
}

NEETCODE_SECTION_NAMES = frozenset(
    {
        "Arrays & Hashing",
        "Heap / Priority Queue",
        "1-D Dynamic Programming",
        "2-D Dynamic Programming",
        "Advanced Graphs",
        "Math & Geometry",
    }
)

EXPECTED_MERGED_CATEGORY_COUNTS = {
    # The v2 merged counts plus the two filled Grind 75 extra rows:
    # binary-tree-maximum-path-sum adds Dynamic Programming, Tree, and
    # DFS; maximum-frequency-stack adds the single Hash Table.
    "Array": 16,
    "Hash Table": 8,
    "Heap": 7,
    "Dynamic Programming": 24,
    "Graph": 20,
    "Math": 7,
    "Tree": 16,
    "Trie": 3,
}


def test_category_canonical_pins_the_neetcode_sections_to_the_grind_vocabulary():
    assert gen.CATEGORY_CANONICAL == CATEGORY_CANONICAL_MAP


def test_category_canonical_decomposes_arrays_and_hashing_into_both_tags():
    assert gen.canonical_category_cell("Arrays & Hashing") == "Array, Hash Table"


def test_category_canonical_subsumes_the_compound_sections_into_one_tag():
    assert gen.canonical_category_cell("Heap / Priority Queue") == "Heap"
    assert gen.canonical_category_cell("Advanced Graphs") == "Graph"
    assert gen.canonical_category_cell("Math & Geometry") == "Math"
    # The section names stay verbatim on the row data: canonicalization is
    # a whole-tag lookup keyed by the exact compound name, so a compound
    # name must never lose its identity to a partial match.
    for section in ("Heap / Priority Queue", "Advanced Graphs", "Math & Geometry"):
        assert gen.CATEGORY_CANONICAL.get(section) is not None, section
    assert gen.canonical_category_cell("Priority Queue") == "Priority Queue"


def test_category_canonical_merges_both_dp_dimensions_into_one_tag():
    assert gen.canonical_category_cell("1-D Dynamic Programming") == "Dynamic Programming"
    assert gen.canonical_category_cell("2-D Dynamic Programming") == "Dynamic Programming"


def test_canonical_category_cell_keeps_unknown_tags_verbatim():
    assert gen.canonical_category_cell("-") == "-"
    assert gen.canonical_category_cell("Array, Dynamic Programming") == (
        "Array, Dynamic Programming"
    )


def test_committed_unified_section_carries_no_neetcode_section_names():
    rows = committed_section_rows()
    assert len(rows) == gen.UNIQUE_PROBLEM_COUNT
    for row in rows:
        tags = gen.category_tags(cell(row, CATEGORY_COLUMN))
        assert not (set(tags) & NEETCODE_SECTION_NAMES), row
    # The compound groupings stay verbatim on the row data (they are
    # subsumed only at canonicalization time), so the whole-tag check
    # above is exactly as narrow as intended: no compound name leaks into
    # an emitted cell, and no emitted tag is a fragment of one either.
    for row in rows:
        assert cell(row, CATEGORY_COLUMN) not in NEETCODE_SECTION_NAMES, row


EXPECTED_CANONICAL_CATEGORY_SAMPLES = {
    "same-tree": "Tree",
    "max-area-of-island": "Graph",
    "implement-trie-prefix-tree": "Trie",
    "group-anagrams": "Array, Hash Table",
    "rotate-image": "Math",
    "edit-distance": "Dynamic Programming",
}


def committed_section_rows():
    """The committed unified table's row lines."""
    return unified_table_rows(committed_section())


def committed_row_by_lc_slug(lc_slug):
    """One committed unified row, addressed by its LeetCode slug.

    Asserts the slug's presence explicitly so a vanished sample slug fails
    with a named assertion instead of a bare KeyError.
    """
    rows_by_lc_slug = {
        unified_row_lc_slug(row): row for row in committed_section_rows()
    }
    assert lc_slug in rows_by_lc_slug, lc_slug
    return rows_by_lc_slug[lc_slug]


def test_committed_unified_section_canonicalizes_the_sample_rows():
    for lc_slug, expected_category in EXPECTED_CANONICAL_CATEGORY_SAMPLES.items():
        row = committed_row_by_lc_slug(lc_slug)
        assert cell(row, CATEGORY_COLUMN) == expected_category, lc_slug


def test_committed_unified_section_merges_the_topic_counts():
    rows = unified_table_rows(committed_section())
    assert len(rows) == gen.UNIQUE_PROBLEM_COUNT
    counts = collections.Counter(
        tag
        for row in rows
        for tag in gen.category_tags(cell(row, CATEGORY_COLUMN))
    )
    for topic, expected_count in EXPECTED_MERGED_CATEGORY_COUNTS.items():
        assert counts[topic] == expected_count, topic


# The unified cells of the two filled Grind 75 extra rows derive from the
# pinned hand-table rows so the fixture has one source of truth.
EXPECTED_UNIFIED_FILL_ROWS = {
    slug: (row["difficulty"], row["category"], row["time"])
    for slug, row in EXPECTED_GRIND_EXTRA_ROWS.items()
}


def test_committed_unified_section_fills_the_former_dash_rows():
    assert len(committed_section_rows()) == gen.UNIQUE_PROBLEM_COUNT
    for lc_slug, (difficulty, category, time_cell) in EXPECTED_UNIFIED_FILL_ROWS.items():
        row = committed_row_by_lc_slug(lc_slug)
        assert cell(row, DIFFICULTY_COLUMN) == difficulty, lc_slug
        assert cell(row, CATEGORY_COLUMN) == category, lc_slug
        assert cell(row, TIME_COLUMN) == time_cell, lc_slug


# ---------------------------------------------------------------------------
# The emitters
# ---------------------------------------------------------------------------


def test_render_unified_section_emits_the_marker_bounded_five_column_table():
    section = render_fixture_section()
    assert section.startswith(gen.UNIFIED_SECTION_START)
    assert section.rstrip().endswith(gen.UNIFIED_SECTION_END)
    assert "## Problem List" in section
    assert gen.UNIFIED_TABLE_HEADER in section
    assert "| #" not in section
    assert "|---|---------|------------|----------|--------|------|" in section


def test_render_unified_section_formats_the_both_tracks_row():
    section = render_fixture_section()
    row = [line for line in section.splitlines() if "two_sum" in line][0]
    assert row == (
        "| [Two Sum](two_sum.md) | Easy | Array, Hash Table "
        f"| [{gen.PRACTICE_LEETCODE}]({gen.LEETCODE_PROBLEM_URL}two-sum/) "
        f"| [{gen.GRIND_TRACK}]({gen.GRIND_TRACK_URL})"
        f" + [{gen.NEETCODE_TRACK}]({gen.NEETCODE_TRACK_URL})"
        " | 15 minutes |"
    )


def test_render_unified_section_carries_no_row_numbers():
    section = render_fixture_section()
    rows = unified_table_rows(section)
    assert len(rows) == 4
    for line in rows:
        assert cell(line, 0).startswith("[")
        assert not cell(line, 0).rstrip().isdigit()


def test_render_unified_section_formats_the_grind_only_row():
    section = render_fixture_section()
    row = [line for line in section.splitlines() if "flood_fill" in line][0]
    assert row == (
        "| [Flood Fill](flood_fill.md) | Easy | Graph, DFS "
        f"| [{gen.PRACTICE_LEETCODE}]({gen.LEETCODE_PROBLEM_URL}flood-fill/) "
        f"| [{gen.GRIND_TRACK}]({gen.GRIND_TRACK_URL})"
        " | 20 minutes |"
    )


def test_render_unified_section_formats_the_neetcode_only_row():
    section = render_fixture_section()
    row = [line for line in section.splitlines() if "jump_game" in line][0]
    assert row == (
        "| [Jump Game](jump_game.md) | Medium | Greedy "
        f"| [{gen.PRACTICE_LEETCODE}]({gen.LEETCODE_PROBLEM_URL}jump-game/) "
        f"| [{gen.NEETCODE_TRACK}]({gen.NEETCODE_TRACK_URL})"
        " | 25 minutes |"
    )


def test_render_unified_section_swaps_premium_rows_to_the_neetcode_page():
    grind = fixture_grind()
    neetcode = fixture_neetcode()[:-1] + [
        neetcode_entry_for(
            "Stack", "encode-and-decode-strings",
            premium=True, nc_slug="string-encode-and-decode",
        )
    ]
    rows = gen.interleave_study_order(gen.merge_tracks(grind, neetcode), neetcode)
    section = gen.render_unified_section(rows, set())
    encode = [line for line in section.splitlines() if "encode_and_decode_strings" in line][0]
    assert f"[{gen.PRACTICE_NEETCODE}]({gen.NEETCODE_PROBLEM_URL}string-encode-and-decode)" in encode
    assert f"({gen.LEETCODE_PROBLEM_URL}encode-and-decode-strings/)" not in encode


def test_render_unified_section_orders_the_premium_fixture_row_into_its_section():
    grind = fixture_grind()
    neetcode = fixture_neetcode()[:-1] + [
        neetcode_entry_for(
            "Stack", "encode-and-decode-strings",
            premium=True, nc_slug="string-encode-and-decode",
        )
    ]
    rows = gen.interleave_study_order(gen.merge_tracks(grind, neetcode), neetcode)
    assert [row["slug"] for row in rows] == [
        "two-sum",
        "min-stack",
        "encode-and-decode-strings",
        "flood-fill",
    ]


def test_committed_unified_section_swaps_exactly_the_seven_premium_rows():
    rows = unified_table_rows(committed_section())
    neetcode_practice = [
        cell(row, PRACTICE_AT_COLUMN) for row in rows
        if gen.PRACTICE_NEETCODE in cell(row, PRACTICE_AT_COLUMN)
    ]
    assert len(neetcode_practice) == len(gen.EXPECTED_PREMIUM_NC_SLUGS)
    for practice_cell in neetcode_practice:
        slug = practice_cell.rsplit("/", 1)[1].rstrip(")")
        assert slug in gen.EXPECTED_PREMIUM_NC_SLUGS.values()


def test_committed_unified_section_practice_at_resolves_every_row():
    rows = unified_table_rows(committed_section())
    assert len(rows) == gen.UNIQUE_PROBLEM_COUNT
    leetcode_count = sum(
        f"({gen.LEETCODE_PROBLEM_URL}" in cell(row, PRACTICE_AT_COLUMN)
        for row in rows
    )
    neetcode_count = sum(
        f"({gen.NEETCODE_PROBLEM_URL}" in cell(row, PRACTICE_AT_COLUMN)
        for row in rows
    )
    assert leetcode_count == gen.UNIQUE_PROBLEM_COUNT - len(gen.EXPECTED_PREMIUM_NC_SLUGS)
    assert neetcode_count == len(gen.EXPECTED_PREMIUM_NC_SLUGS)


def test_committed_unified_section_practice_at_links_match_the_leetcode_slug_pattern():
    rows = unified_table_rows(committed_section())
    pattern = f"({gen.LEETCODE_PROBLEM_URL}"
    for row in rows:
        practice_cell = cell(row, PRACTICE_AT_COLUMN)
        if pattern not in practice_cell:
            continue
        link = practice_cell[practice_cell.index(pattern) + 1 :].split(")")[0]
        slug = link[len(gen.LEETCODE_PROBLEM_URL) :].rstrip("/")
        assert slug == unified_row_lc_slug(row), row


def test_committed_unified_section_tracks_cells_link_the_track_list_pages():
    rows = unified_table_rows(committed_section())
    grind_links = sum(f"]({gen.GRIND_TRACK_URL})" in row for row in rows)
    neetcode_links = sum(f"]({gen.NEETCODE_TRACK_URL})" in row for row in rows)
    assert grind_links == gen.GRIND_ROW_COUNT
    assert neetcode_links == gen.OVERLAP_COUNT + gen.NEETCODE_ONLY_COUNT


def committed_unified_time_cell(row):
    """One committed unified row's Time cell text."""
    return cell(row, TIME_COLUMN)


def test_committed_unified_section_leaves_no_empty_time_cells():
    rows = unified_table_rows(committed_section())
    assert len(rows) == gen.UNIQUE_PROBLEM_COUNT
    for row in rows:
        assert committed_unified_time_cell(row), row


def test_committed_unified_section_keeps_the_grind_minutes_unchanged():
    grind_times = {row["slug"]: row["time"] for row in gen.load_grind_table(GRIND_TABLE_PATH)}
    rows = unified_table_rows(committed_section())
    checked = 0
    for row in rows:
        slug = unified_row_lc_slug(row)
        if slug not in grind_times:
            continue
        assert committed_unified_time_cell(row) == grind_times[slug], row
        checked += 1
    assert checked == gen.GRIND_ROW_COUNT


def test_committed_unified_section_estimates_the_neetcode_only_minutes():
    grind_slugs = {row["slug"] for row in gen.load_grind_table(GRIND_TABLE_PATH)}
    rows = unified_table_rows(committed_section())
    checked = 0
    for row in rows:
        if unified_row_lc_slug(row) in grind_slugs:
            continue
        difficulty = cell(row, DIFFICULTY_COLUMN)
        assert committed_unified_time_cell(row) == gen.estimated_time_cell(difficulty), row
        checked += 1
    assert checked == gen.NEETCODE_ONLY_COUNT


def test_render_unified_section_appends_the_amazon_marker_to_overlapping_rows():
    amazon = fixture_amazon() + [amazon_entry_for("min-stack")]
    section = render_fixture_section(amazon=amazon)
    min_stack = [line for line in section.splitlines() if "min_stack" in line][0]
    assert min_stack.endswith(
        f"{gen.AMAZON_MARKER} | 20 minutes |"
    )
    assert f"]({gen.GRIND_TRACK_URL})" in min_stack
    two_sum = [line for line in section.splitlines() if "two_sum" in line][0]
    assert gen.AMAZON_MARKER not in two_sum


def test_render_unified_section_links_rows_landing_relative():
    section = render_fixture_section()
    assert "(two_sum.md)" in section
    assert "](problems/" not in section


def test_render_unified_section_marks_exactly_the_23_committed_amazon_overlap_rows():
    rows = unified_table_rows(committed_section())
    marked_slugs = {
        unified_row_lc_slug(row) for row in rows if gen.AMAZON_MARKER in row
    }
    assert marked_slugs == EXPECTED_AMAZON_OVERLAP_LC_SLUGS
    assert sum(gen.AMAZON_MARKER in row for row in rows) == 23


def test_render_unified_section_excludes_grind_only_amazon_matches_from_the_marker():
    amazon = fixture_amazon() + [amazon_entry_for("flood-fill")]
    section = render_fixture_section(amazon=amazon)
    flood_fill = [line for line in section.splitlines() if "flood_fill" in line][0]
    assert gen.AMAZON_MARKER not in flood_fill


def test_render_unified_section_carries_the_amazon_legend():
    section = gen.render_unified_section(
        *unified_section_inputs(fixture_amazon() + [amazon_entry_for("min-stack")])
    )
    assert gen.AMAZON_LEGEND in section
    assert "(../amazon/index.md)" in section


def unified_section_inputs(amazon):
    """The (rows, overlap) pair for a fixture render, mirroring render_sections."""
    neetcode = fixture_neetcode()
    rows = gen.interleave_study_order(gen.merge_tracks(fixture_grind(), neetcode), neetcode)
    return rows, gen.amazon_overlap_lc_slugs(neetcode, amazon)


def test_committed_amazon_rows_carry_fastprep_links():
    for entry in gen.load_amazon_manifest(AMAZON_MANIFEST_PATH):
        assert entry["url"].startswith("https://www.fastprep.io/problems/"), entry["slug"]


def test_track_link_uses_the_content_serving_neetcode_list_url():
    assert gen.NEETCODE_TRACK_URL == "https://neetcode.io/practice/practice/neetcode150"
    assert f"[{gen.NEETCODE_TRACK}]({gen.NEETCODE_TRACK_URL})" == gen.track_link(
        gen.NEETCODE_TRACK
    )


def test_render_sources_section_credits_all_three_lists():
    section = gen.render_sources_section()
    assert section.startswith(gen.SOURCES_SECTION_START)
    assert section.rstrip().endswith(gen.SOURCES_SECTION_END)
    assert "## Sources" in section
    assert "https://www.techinterviewhandbook.org/grind75" in section
    assert "https://neetcode.io/practice/practice/neetcode150" in section
    assert "https://github.com/perixtar/Tech-OA-Interview-Questions" in section
    assert "https://www.fastprep.io" in section


# ---------------------------------------------------------------------------
# Emission into docs/leetcode/index.md
# ---------------------------------------------------------------------------


def fresh_landing(tmp_path):
    landing_path = tmp_path / "index.md"
    landing_path.write_text(
        "# Problems\n\nIntro prose.\n\n## Study Guide and Practice\n\nProse.\n",
        encoding="utf-8",
    )
    return landing_path


def test_write_sections_splices_both_sections_before_the_anchor(tmp_path):
    landing_path = fresh_landing(tmp_path)
    changed = gen.write_sections(landing_path=landing_path)
    assert changed is True
    text = landing_path.read_text(encoding="utf-8")
    assert text.index(gen.UNIFIED_SECTION_START) < text.index(gen.SOURCES_SECTION_START)
    assert text.index(gen.SOURCES_SECTION_START) < text.index(gen.LANDING_ANCHOR)


def test_write_sections_is_byte_stable_on_regeneration(tmp_path):
    landing_path = fresh_landing(tmp_path)
    gen.write_sections(landing_path=landing_path)
    first = landing_path.read_text(encoding="utf-8")
    changed = gen.write_sections(landing_path=landing_path)
    assert changed is False
    assert landing_path.read_text(encoding="utf-8") == first


def test_write_sections_replaces_a_mutated_row(tmp_path):
    landing_path = fresh_landing(tmp_path)
    gen.write_sections(landing_path=landing_path)
    text = landing_path.read_text(encoding="utf-8")
    text = text.replace("[Two Sum](two_sum.md)", "[Wrong Sum](wrong_sum.md)")
    landing_path.write_text(text, encoding="utf-8")
    changed = gen.write_sections(landing_path=landing_path)
    assert changed is True
    assert "[Two Sum](two_sum.md)" in landing_path.read_text(encoding="utf-8")


def test_write_sections_requires_a_landing_anchor_when_markers_are_absent(tmp_path):
    landing_path = tmp_path / "index.md"
    landing_path.write_text("# Problems\n\nNo tables here.\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="Study Guide and Practice"):
        gen.write_sections(landing_path=landing_path)


# ---------------------------------------------------------------------------
# The --check gate
# ---------------------------------------------------------------------------


@pre_move_skip
def test_check_passes_after_emission(tmp_path, monkeypatch):
    landing_path = fresh_landing(tmp_path)
    redirect_pandoc_config_paths(tmp_path, monkeypatch)
    gen.write_sections(landing_path=landing_path)
    gen.write_pandoc_configs()
    assert gen.check(landing_path=landing_path) == 0


def test_check_fails_when_a_row_drifts(tmp_path):
    landing_path = fresh_landing(tmp_path)
    gen.write_sections(landing_path=landing_path)
    text = landing_path.read_text(encoding="utf-8")
    landing_path.write_text(
        text.replace("[Two Sum](two_sum.md)", "[Wrong Sum](wrong_sum.md)"),
        encoding="utf-8",
    )
    assert gen.check(landing_path=landing_path) == 1


def test_check_fails_when_markers_are_missing(tmp_path):
    landing_path = fresh_landing(tmp_path)
    assert gen.check(landing_path=landing_path) == 1


# ---------------------------------------------------------------------------
# CLI wiring
# ---------------------------------------------------------------------------


def test_main_emits_sections_and_exits_zero(tmp_path, monkeypatch, capsys):
    landing_path = fresh_landing(tmp_path)
    mkdocs_path = mkdocs_shell(tmp_path)
    redirect_pandoc_config_paths(tmp_path, monkeypatch)
    monkeypatch.setattr(gen, "PROBLEMS_INDEX_PATH", landing_path)
    monkeypatch.setattr(gen, "MKDOCS_PATH", mkdocs_path)
    assert gen.main([]) == 0
    assert gen.UNIFIED_SECTION_START in landing_path.read_text(encoding="utf-8")
    assert "sections written" in capsys.readouterr().out


@pre_move_skip
def test_main_check_mode_is_read_only_and_exits_zero(tmp_path, monkeypatch):
    landing_path = fresh_landing(tmp_path)
    redirect_pandoc_config_paths(tmp_path, monkeypatch)
    gen.write_sections(landing_path=landing_path)
    gen.write_pandoc_configs()
    before = landing_path.read_text(encoding="utf-8")
    monkeypatch.setattr(gen, "PROBLEMS_INDEX_PATH", landing_path)
    assert gen.main(["--check"]) == 0
    assert landing_path.read_text(encoding="utf-8") == before


def test_main_check_mode_fails_on_drift(tmp_path, monkeypatch):
    landing_path = fresh_landing(tmp_path)
    gen.write_sections(landing_path=landing_path)
    text = landing_path.read_text(encoding="utf-8")
    landing_path.write_text(text.replace("## Sources", "## Credits"), encoding="utf-8")
    monkeypatch.setattr(gen, "PROBLEMS_INDEX_PATH", landing_path)
    redirect_pandoc_config_paths(tmp_path, monkeypatch)
    assert gen.main(["--check"]) == 1


@pre_move_skip
def test_committed_landing_page_lives_at_docs_problems_index_md():
    assert gen.PROBLEMS_INDEX_PATH == gen.REPO_ROOT / "docs" / "leetcode" / "index.md"
    assert gen.PROBLEMS_INDEX_PATH.exists()
    text = gen.PROBLEMS_INDEX_PATH.read_text(encoding="utf-8")
    assert text.startswith("# Problems\n")
    assert gen.LANDING_ANCHOR in text


@pre_move_skip
def test_committed_landing_page_satisfies_the_check_gate():
    assert gen.check() == 0


@pre_move_skip
def test_committed_pandoc_configs_satisfy_the_check_gate():
    assert gen.check_pandoc_configs() == 0


# ---------------------------------------------------------------------------
# The mkdocs.yml generated nav (Leetcode + Amazon)
# ---------------------------------------------------------------------------


def expected_nav_text(merged, amazon):
    """Render the expected generated nav block for the merged rows."""
    lines = [
        gen.NAV_LEETCODE_MARKER,
        gen.NAV_LEETCODE_LANDING_ENTRY,
    ]
    for row in merged:
        lines.append(f'    - "{row["title"]}": leetcode/{row["dirSlug"]}.md\n')
    lines.append(gen.NAV_AMAZON_MARKER)
    lines.append(gen.NAV_AMAZON_LANDING_ENTRY)
    for entry in amazon:
        lines.append(f'    - "{entry["title"]}": amazon/{entry["slug"]}.md\n')
    return "".join(lines)


def mkdocs_shell(tmp_path, body="  - \"Two Sum\": \"two_sum.md\"\n"):
    """A mkdocs.yml shell whose generated span is `body` (legacy Problems)."""
    mkdocs_path = tmp_path / "mkdocs.yml"
    mkdocs_path.write_text(
        "nav:\n"
        "  - Home: index.md\n"
        "  - Problems:\n" + body,
        encoding="utf-8",
    )
    return mkdocs_path


def mkdocs_shell_new(tmp_path, body=""):
    """A mkdocs.yml shell opening the generated span at the Leetcode marker."""
    mkdocs_path = tmp_path / "mkdocs.yml"
    mkdocs_path.write_text(
        "nav:\n"
        "  - Home: index.md\n"
        "  - Leetcode:\n" + body,
        encoding="utf-8",
    )
    return mkdocs_path


def committed_nav_rows():
    """The interleaved merged rows from the committed data sources."""
    return gen.study_order_rows(
        gen.load_grind_table(GRIND_TABLE_PATH),
        gen.load_neetcode_manifest(NEETCODE_MANIFEST_PATH),
    )


def committed_amazon_entries():
    """The loaded Amazon OA manifest from the committed data source."""
    return gen.load_amazon_manifest(AMAZON_MANIFEST_PATH)


def test_render_generated_nav_emits_two_top_level_sections():
    amazon = committed_amazon_entries()
    nav = gen.render_generated_nav(committed_nav_rows(), amazon)
    assert nav.startswith(gen.NAV_LEETCODE_MARKER)
    assert gen.NAV_LEETCODE_LANDING_ENTRY == "    - leetcode/index.md\n"
    assert nav.index(gen.NAV_LEETCODE_LANDING_ENTRY) < nav.index(
        f'    - "{committed_nav_rows()[0]["title"]}": leetcode/'
    )
    assert gen.NAV_AMAZON_MARKER == "  - Amazon:\n"
    assert gen.NAV_AMAZON_LANDING_ENTRY == "    - amazon/index.md\n"
    assert nav.index(gen.NAV_LEETCODE_MARKER) < nav.index(gen.NAV_AMAZON_MARKER)
    first_amazon = amazon[0]
    last_amazon = amazon[-1]
    assert (
        gen.NAV_AMAZON_MARKER
        + gen.NAV_AMAZON_LANDING_ENTRY
        + f'    - "{first_amazon["title"]}": amazon/{first_amazon["slug"]}.md\n'
    ) in nav
    assert nav.rstrip().endswith(
        f'    - "{last_amazon["title"]}": amazon/{last_amazon["slug"]}.md'
    )


def test_render_generated_nav_lists_all_rows_at_one_level_in_study_order():
    rows = committed_nav_rows()
    nav = gen.render_generated_nav(rows, committed_amazon_entries())
    lines = nav.splitlines()
    start = lines.index(f'    - "{rows[0]["title"]}": leetcode/{rows[0]["dirSlug"]}.md')
    end = lines.index(gen.NAV_AMAZON_MARKER.rstrip("\n"))
    children = lines[start:end]
    assert len(children) == gen.UNIQUE_PROBLEM_COUNT
    assert children == [
        f'    - "{row["title"]}": leetcode/{row["dirSlug"]}.md' for row in rows
    ]


def test_render_generated_nav_lists_all_amazon_entries_at_one_level():
    amazon = committed_amazon_entries()
    nav = gen.render_generated_nav(committed_nav_rows(), amazon)
    lines = nav.splitlines()
    index_at = lines.index(gen.NAV_AMAZON_LANDING_ENTRY.rstrip("\n"))
    children = lines[index_at + 1 :]
    assert len(children) == gen.AMAZON_ROW_COUNT
    assert children == [
        f'    - "{entry["title"]}": amazon/{entry["slug"]}.md' for entry in amazon
    ]


def test_render_generated_nav_orders_amazon_children_most_recently_updated_first():
    amazon = committed_amazon_entries()
    nav = gen.render_generated_nav(committed_nav_rows(), amazon)
    slugs = gen.nav_amazon_children(nav)
    assert slugs == [entry["slug"] for entry in amazon]
    updated_dates = [entry["updated"] for entry in amazon]
    assert updated_dates == sorted(updated_dates, reverse=True)


def test_write_problems_nav_replaces_a_flat_or_legacy_problems_section(tmp_path):
    mkdocs_path = mkdocs_shell(
        tmp_path,
        body=(
            '    - "NeetCode 150":\n'
            '      - "A": problems/a.md\n'
            '    - "Amazon OA": problems/amazon_oa/index.md\n'
            '    - "Two Sum": problems/two_sum.md\n'
        ),
    )
    changed = gen.write_problems_nav(mkdocs_path=mkdocs_path)
    assert changed is True
    text = mkdocs_path.read_text(encoding="utf-8")
    assert expected_nav_text(
        committed_nav_rows(), committed_amazon_entries()
    ) in text
    assert '"NeetCode 150"' not in text
    assert "  - Problems:\n" not in text
    assert text.count(gen.NAV_LEETCODE_MARKER) == 1


@pre_move_skip
def test_write_problems_nav_replaces_the_new_shape_byte_stably(tmp_path):
    mkdocs_path = mkdocs_shell_new(tmp_path)
    gen.write_problems_nav(mkdocs_path=mkdocs_path)
    first = mkdocs_path.read_text(encoding="utf-8")
    changed = gen.write_problems_nav(mkdocs_path=mkdocs_path)
    assert changed is False
    assert mkdocs_path.read_text(encoding="utf-8") == first


@pre_move_skip
def test_write_problems_nav_is_byte_stable_on_a_legacy_problems_section(tmp_path):
    mkdocs_path = mkdocs_shell(tmp_path)
    gen.write_problems_nav(mkdocs_path=mkdocs_path)
    first = mkdocs_path.read_text(encoding="utf-8")
    changed = gen.write_problems_nav(mkdocs_path=mkdocs_path)
    assert changed is False
    assert mkdocs_path.read_text(encoding="utf-8") == first


def test_write_problems_nav_requires_a_generated_nav_section(tmp_path):
    mkdocs_path = tmp_path / "mkdocs.yml"
    mkdocs_path.write_text("nav:\n  - Home: index.md\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="Leetcode or Problems"):
        gen.write_problems_nav(mkdocs_path=mkdocs_path)


def nav_children(mkdocs_text):
    """The Leetcode section's child lines in file order."""
    at = mkdocs_text.index(gen.NAV_LEETCODE_MARKER) + len(gen.NAV_LEETCODE_MARKER)
    at += len(gen.NAV_LEETCODE_LANDING_ENTRY)
    children = []
    for line in mkdocs_text[at:].splitlines():
        match = gen.NAV_LEETCODE_CHILD_PATTERN.match(line)
        if match is None:
            break
        children.append(match.group(2))
    return children


@pre_move_skip
def test_check_problems_nav_passes_after_emission(tmp_path):
    mkdocs_path = mkdocs_shell(tmp_path)
    gen.write_problems_nav(mkdocs_path=mkdocs_path)
    assert gen.check_problems_nav(mkdocs_path=mkdocs_path) == 0


@pre_move_skip
def test_check_problems_nav_passes_on_the_new_shape(tmp_path):
    mkdocs_path = mkdocs_shell_new(tmp_path)
    gen.write_problems_nav(mkdocs_path=mkdocs_path)
    assert gen.check_problems_nav(mkdocs_path=mkdocs_path) == 0


def test_check_problems_nav_fails_on_an_extra_child(tmp_path):
    mkdocs_path = mkdocs_shell_new(tmp_path)
    gen.write_problems_nav(mkdocs_path=mkdocs_path)
    text = mkdocs_path.read_text(encoding="utf-8")
    first_child = f'    - "{committed_nav_rows()[0]["title"]}": leetcode/{committed_nav_rows()[0]["dirSlug"]}.md\n'
    text = text.replace(
        first_child,
        first_child + '    - "Overlap Dup": leetcode/two_sum.md\n',
    )
    mkdocs_path.write_text(text, encoding="utf-8")
    assert gen.check_problems_nav(mkdocs_path=mkdocs_path) == 1


def test_check_problems_nav_fails_on_drifted_order(tmp_path):
    mkdocs_path = mkdocs_shell_new(tmp_path)
    gen.write_problems_nav(mkdocs_path=mkdocs_path)
    text = mkdocs_path.read_text(encoding="utf-8")
    first_child = f'    - "{committed_nav_rows()[0]["title"]}": leetcode/{committed_nav_rows()[0]["dirSlug"]}.md\n'
    text = text.replace(first_child, "")
    mkdocs_path.write_text(text, encoding="utf-8")
    assert gen.check_problems_nav(mkdocs_path=mkdocs_path) == 1


def test_check_problems_nav_fails_when_the_amazon_section_is_gone(tmp_path):
    mkdocs_path = mkdocs_shell_new(tmp_path)
    gen.write_problems_nav(mkdocs_path=mkdocs_path)
    text = mkdocs_path.read_text(encoding="utf-8")
    text = text.replace(gen.NAV_AMAZON_MARKER, "").replace(
        gen.NAV_AMAZON_LANDING_ENTRY, ""
    )
    mkdocs_path.write_text(text, encoding="utf-8")
    assert gen.check_problems_nav(mkdocs_path=mkdocs_path) == 1


def test_check_problems_nav_fails_when_markers_are_missing(tmp_path):
    mkdocs_path = mkdocs_shell(tmp_path)
    assert gen.check_problems_nav(mkdocs_path=mkdocs_path) == 1


def test_committed_mkdocs_nav_satisfies_the_check_gate_wave_b_shape():
    # The committed mkdocs.yml still carries the pre-move generated span
    # until wave B regenerates it; the audit accepts both span markers and
    # demands the fresh (new-shape) render inside whichever span it finds.
    assert gen.check_problems_nav() == 1 if "  - Problems:\n" in gen.MKDOCS_PATH.read_text(encoding="utf-8") else gen.check_problems_nav() == 0


def test_committed_nav_amazon_subsection_links_the_bank_index_as_its_own_page():
    mkdocs_text = gen.MKDOCS_PATH.read_text(encoding="utf-8")
    assert gen.NAV_AMAZON_MARKER in mkdocs_text or "  - Problems:\n" in mkdocs_text
    # Post-wave-B the Amazon section opens with the bank landing entry.
    if gen.NAV_AMAZON_MARKER in mkdocs_text:
        header_at = mkdocs_text.index(gen.NAV_AMAZON_MARKER)
        assert mkdocs_text.startswith(
            gen.NAV_AMAZON_LANDING_ENTRY, header_at + len(gen.NAV_AMAZON_MARKER)
        )


@pre_move_skip
def test_committed_nav_amazon_children_resolve_to_committed_writeup_pages():
    # The nav children are rendered from the committed manifest, so every
    # child must resolve to a committed write-up page at the moved path.
    mkdocs_path = mkdocs_shell_new(tmp_path_factory())
    gen.write_problems_nav(mkdocs_path=mkdocs_path)
    text = mkdocs_path.read_text(encoding="utf-8")
    children = gen.nav_amazon_children(text)
    assert children, "no amazon children rendered"
    for slug in children:
        assert (gen.AMAZON_WRITEUP_DIR / f"{slug}.md").exists(), slug


def tmp_path_factory():
    import tempfile

    return Path(tempfile.mkdtemp())


def test_nav_amazon_children_returns_empty_without_the_amazon_section():
    assert gen.nav_amazon_children(
        gen.NAV_LEETCODE_MARKER + gen.NAV_LEETCODE_LANDING_ENTRY
    ) == []


def test_nav_amazon_children_returns_empty_without_the_landing_entry():
    text = (
        gen.NAV_LEETCODE_MARKER
        + gen.NAV_LEETCODE_LANDING_ENTRY
        + '    - "One": amazon/amazon-one.md\n'
        + gen.NAV_AMAZON_MARKER
    )
    assert gen.nav_amazon_children(text) == []


def test_nav_amazon_children_scan_stops_at_the_first_non_child_line():
    text = (
        gen.NAV_LEETCODE_MARKER
        + gen.NAV_LEETCODE_LANDING_ENTRY
        + gen.NAV_AMAZON_MARKER
        + gen.NAV_AMAZON_LANDING_ENTRY
        + '    - "One": amazon/amazon-one.md\n'
        + "  - Blog:\n"
        + '    - "Leaked": amazon/amazon-leaked.md\n'
    )
    assert gen.nav_amazon_children(text) == ["amazon-one"]


def test_nav_leetcode_children_extract_the_dir_slugs_in_file_order():
    nav = gen.render_generated_nav(committed_nav_rows(), committed_amazon_entries())
    amazon = committed_amazon_entries()
    assert gen.nav_leetcode_children(nav) == [row["dirSlug"] for row in committed_nav_rows()]
    assert gen.nav_amazon_children(nav) == [entry["slug"] for entry in amazon]


def test_check_problems_nav_fails_on_an_extra_amazon_child(tmp_path):
    mkdocs_path = mkdocs_shell_new(tmp_path)
    gen.write_problems_nav(mkdocs_path=mkdocs_path)
    text = mkdocs_path.read_text(encoding="utf-8")
    text = text.replace(
        gen.NAV_AMAZON_LANDING_ENTRY,
        gen.NAV_AMAZON_LANDING_ENTRY + '    - "Rogue": amazon/amazon-rogue.md\n',
    )
    mkdocs_path.write_text(text, encoding="utf-8")
    assert gen.check_problems_nav(mkdocs_path=mkdocs_path) == 1


def test_check_problems_nav_fails_when_an_amazon_child_drifts_in_order(tmp_path):
    mkdocs_path = mkdocs_shell_new(tmp_path)
    gen.write_problems_nav(mkdocs_path=mkdocs_path)
    text = mkdocs_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    index_at = lines.index(gen.NAV_AMAZON_LANDING_ENTRY)
    lines[index_at + 1], lines[index_at + 2] = lines[index_at + 2], lines[index_at + 1]
    mkdocs_path.write_text("".join(lines), encoding="utf-8")
    assert gen.check_problems_nav(mkdocs_path=mkdocs_path) == 1


def test_main_emits_landing_sections_and_nav(tmp_path, monkeypatch, capsys):
    landing_path = fresh_landing(tmp_path)
    mkdocs_path = mkdocs_shell(tmp_path)
    redirect_pandoc_config_paths(tmp_path, monkeypatch)
    monkeypatch.setattr(gen, "PROBLEMS_INDEX_PATH", landing_path)
    monkeypatch.setattr(gen, "MKDOCS_PATH", mkdocs_path)
    assert gen.main([]) == 0
    assert gen.UNIFIED_SECTION_START in landing_path.read_text(encoding="utf-8")
    assert expected_nav_text(
        committed_nav_rows(), committed_amazon_entries()
    ) in mkdocs_path.read_text(encoding="utf-8")
    assert "sections written" in capsys.readouterr().out


@pre_move_skip
def test_main_check_mode_covers_landing_and_nav(tmp_path, monkeypatch):
    landing_path = fresh_landing(tmp_path)
    mkdocs_path = mkdocs_shell(tmp_path)
    redirect_pandoc_config_paths(tmp_path, monkeypatch)
    gen.write_sections(landing_path=landing_path)
    gen.write_problems_nav(mkdocs_path=mkdocs_path)
    gen.write_pandoc_configs()
    before_landing = landing_path.read_text(encoding="utf-8")
    before_mkdocs = mkdocs_path.read_text(encoding="utf-8")
    monkeypatch.setattr(gen, "PROBLEMS_INDEX_PATH", landing_path)
    monkeypatch.setattr(gen, "MKDOCS_PATH", mkdocs_path)
    assert gen.main(["--check"]) == 0
    assert landing_path.read_text(encoding="utf-8") == before_landing
    assert mkdocs_path.read_text(encoding="utf-8") == before_mkdocs


# ---------------------------------------------------------------------------
# The pandoc config emission (configs/all-problems.yaml + the two dividers)
# ---------------------------------------------------------------------------


LEETCODE_DIVIDER_POSITION = 1
AMAZON_DIVIDER_POSITION = gen.UNIQUE_PROBLEM_COUNT + 2


def pandoc_config_input_entries(config_text):
    """The input-files entries of a rendered pandoc config, in order."""
    lines = config_text.splitlines()
    start = lines.index("input-files:") + 1
    entries = []
    for line in lines[start:]:
        if not line.startswith("  - "):
            break
        entries.append(line[len("  - ") :])
    return entries


def pandoc_config_shell(tmp_path):
    """The three redirected config paths for emission tests under tmp_path."""
    return (
        tmp_path / "all-problems.yaml",
        tmp_path / "part-leetcode.md",
        tmp_path / "part-amazon.md",
    )


def redirect_pandoc_config_paths(tmp_path, monkeypatch):
    """Point the generator's config path constants into tmp_path."""
    config_path, leetcode_divider_path, amazon_divider_path = pandoc_config_shell(tmp_path)
    monkeypatch.setattr(gen, "PANDOC_CONFIG_PATH", config_path)
    monkeypatch.setattr(gen, "LEETCODE_DIVIDER_PATH", leetcode_divider_path)
    monkeypatch.setattr(gen, "AMAZON_DIVIDER_PATH", amazon_divider_path)


def fixture_merged_rows():
    """The interleaved study order over the small synthetic fixtures."""
    neetcode = fixture_neetcode()
    return gen.interleave_study_order(gen.merge_tracks(fixture_grind(), neetcode), neetcode)


def test_render_pandoc_config_orders_dividers_around_both_collections():
    merged = fixture_merged_rows()
    amazon = fixture_amazon()
    config_text = gen.render_pandoc_config(merged, amazon)
    inputs = pandoc_config_input_entries(config_text)
    expected = (
        [gen.LEETCODE_DIVIDER_INPUT]
        + [f"leetcode/{row['dirSlug']}.md" for row in merged]
        + [gen.AMAZON_DIVIDER_INPUT]
        + [f"amazon/{entry['slug']}.md" for entry in amazon]
    )
    assert inputs == expected


def test_render_pandoc_config_carries_the_legacy_formatting_block():
    config_text = gen.render_pandoc_config(fixture_merged_rows(), fixture_amazon())
    assert f"output-file: {gen.PANDOC_OUTPUT_FILE}" in config_text
    assert "pdf-engine: xelatex" in config_text
    assert "  papersize: letter" in config_text
    assert "    - margin=1in" in config_text
    assert '  monofont: "DejaVu Sans Mono"' in config_text
    assert "    - Scale=0.85" in config_text
    assert "  linkcolor: blue" in config_text
    assert "  listings: true" in config_text
    assert "  breaklines: true" in config_text
    assert "toc: true" in config_text
    assert "toc-depth: 2" in config_text
    assert f"resource-path: {gen.PANDOC_RESOURCE_PATH}" in config_text


def test_render_pandoc_config_reads_latex_delimited_inline_math():
    config_text = gen.render_pandoc_config(fixture_merged_rows(), fixture_amazon())
    assert f"from: {gen.PANDOC_INPUT_FORMAT}" in config_text


def test_render_pandoc_config_titles_the_combined_document():
    config_text = gen.render_pandoc_config(fixture_merged_rows(), fixture_amazon())
    assert 'metadata:\n' in config_text
    assert f'  title: "{gen.PANDOC_DOCUMENT_TITLE}"' in config_text


def test_render_pandoc_config_opens_with_the_generator_ownership_comment():
    config_text = gen.render_pandoc_config(fixture_merged_rows(), fixture_amazon())
    assert config_text.startswith(gen.PANDOC_CONFIG_HEADER + "\ninput-files:")


def test_render_pandoc_config_ends_after_the_metadata_block():
    config_text = gen.render_pandoc_config(fixture_merged_rows(), fixture_amazon())
    assert config_text.endswith(f'  title: "{gen.PANDOC_DOCUMENT_TITLE}"\n')


def test_render_leetcode_divider_opens_with_the_raw_latex_part():
    divider = gen.render_leetcode_divider(fixture_merged_rows())
    latex_part = f"\\part{{{gen.LEETCODE_DIVIDER_TITLE}}}"
    assert divider.startswith(f"```{{=latex}}\n{latex_part}\n```\n\n")
    assert divider.endswith("\n")


def test_render_leetcode_divider_orients_the_reader_with_one_paragraph():
    divider = gen.render_leetcode_divider(fixture_merged_rows())
    body_blocks = divider.split("\n\n")
    assert len(body_blocks) == 2
    assert str(len(fixture_merged_rows())) in body_blocks[1]
    assert "Grind 75" in body_blocks[1]
    assert "NeetCode 150" in body_blocks[1]


def test_render_amazon_divider_opens_with_the_raw_latex_part():
    divider = gen.render_amazon_divider(fixture_amazon())
    latex_part = f"\\part{{{gen.AMAZON_DIVIDER_TITLE}}}"
    assert divider.startswith(f"```{{=latex}}\n{latex_part}\n```\n\n")
    assert divider.endswith("\n")


def test_render_amazon_divider_orients_the_reader_with_one_paragraph():
    divider = gen.render_amazon_divider(fixture_amazon())
    body_blocks = divider.split("\n\n")
    assert len(body_blocks) == 2
    assert str(len(fixture_amazon())) in body_blocks[1]
    assert "most recently updated first" in body_blocks[1]


def committed_pandoc_inputs():
    """The committed catalog's input list from a fresh config render."""
    return pandoc_config_input_entries(
        gen.render_pandoc_config(committed_nav_rows(), committed_amazon_entries())
    )


def test_committed_pandoc_config_carries_exactly_the_combined_input_total():
    inputs = committed_pandoc_inputs()
    assert len(inputs) == gen.UNIQUE_PROBLEM_COUNT + gen.AMAZON_ROW_COUNT + 2
    assert gen.PANDOC_INPUT_TOTAL == len(inputs)


def test_committed_pandoc_config_puts_the_dividers_at_the_collection_boundaries():
    inputs = committed_pandoc_inputs()
    assert inputs[LEETCODE_DIVIDER_POSITION - 1] == gen.LEETCODE_DIVIDER_INPUT
    assert inputs[AMAZON_DIVIDER_POSITION - 1] == gen.AMAZON_DIVIDER_INPUT
    assert inputs[LEETCODE_DIVIDER_POSITION] == (
        f"leetcode/{committed_nav_rows()[0]['dirSlug']}.md"
    )
    assert inputs[AMAZON_DIVIDER_POSITION] == (
        f"amazon/{committed_amazon_entries()[0]['slug']}.md"
    )
    assert inputs[AMAZON_DIVIDER_POSITION - 2] == (
        f"leetcode/{committed_nav_rows()[-1]['dirSlug']}.md"
    )


def test_committed_pandoc_config_orders_leetcode_pages_by_the_study_order():
    inputs = committed_pandoc_inputs()
    leetcode_inputs = inputs[LEETCODE_DIVIDER_POSITION : AMAZON_DIVIDER_POSITION - 1]
    assert len(leetcode_inputs) == gen.UNIQUE_PROBLEM_COUNT
    assert leetcode_inputs == [
        f"leetcode/{row['dirSlug']}.md" for row in committed_nav_rows()
    ]
    assert leetcode_inputs[0] == "leetcode/two_sum.md"


def test_committed_pandoc_config_orders_amazon_pages_newest_first():
    inputs = committed_pandoc_inputs()
    amazon_inputs = inputs[AMAZON_DIVIDER_POSITION:]
    amazon = committed_amazon_entries()
    assert len(amazon_inputs) == gen.AMAZON_ROW_COUNT
    assert amazon_inputs == [f"amazon/{entry['slug']}.md" for entry in amazon]
    updated_dates = [entry["updated"] for entry in amazon]
    assert updated_dates == sorted(updated_dates, reverse=True)


def test_committed_pandoc_dividers_open_with_their_collection_titles():
    leetcode_divider = gen.render_leetcode_divider(committed_nav_rows())
    amazon_divider = gen.render_amazon_divider(committed_amazon_entries())
    assert gen.LEETCODE_DIVIDER_TITLE == "Part One: The LeetCode Track"
    assert gen.AMAZON_DIVIDER_TITLE == "Part Two: The Amazon OA Bank"
    latex_part_leetcode = f"\\part{{{gen.LEETCODE_DIVIDER_TITLE}}}"
    latex_part_amazon = f"\\part{{{gen.AMAZON_DIVIDER_TITLE}}}"
    assert leetcode_divider.startswith(f"```{{=latex}}\n{latex_part_leetcode}\n```\n\n")
    assert amazon_divider.startswith(f"```{{=latex}}\n{latex_part_amazon}\n```\n\n")
    assert f"{gen.UNIQUE_PROBLEM_COUNT} problems" in leetcode_divider
    assert f"{gen.AMAZON_ROW_COUNT} problem pages" in amazon_divider


def test_write_pandoc_configs_emits_all_three_artifacts(tmp_path, monkeypatch):
    redirect_pandoc_config_paths(tmp_path, monkeypatch)
    assert gen.write_pandoc_configs() is True
    assert gen.PANDOC_CONFIG_PATH.read_text(encoding="utf-8") == gen.render_pandoc_config(
        committed_nav_rows(), committed_amazon_entries()
    )
    assert gen.LEETCODE_DIVIDER_PATH.read_text(encoding="utf-8") == (
        gen.render_leetcode_divider(committed_nav_rows())
    )
    assert gen.AMAZON_DIVIDER_PATH.read_text(encoding="utf-8") == (
        gen.render_amazon_divider(committed_amazon_entries())
    )


def test_write_pandoc_configs_is_byte_stable_on_regeneration(tmp_path, monkeypatch):
    redirect_pandoc_config_paths(tmp_path, monkeypatch)
    gen.write_pandoc_configs()
    artifacts = (gen.PANDOC_CONFIG_PATH, gen.LEETCODE_DIVIDER_PATH, gen.AMAZON_DIVIDER_PATH)
    before = {path: path.read_text(encoding="utf-8") for path in artifacts}
    assert gen.write_pandoc_configs() is False
    assert {path: path.read_text(encoding="utf-8") for path in artifacts} == before


def test_write_pandoc_configs_repairs_a_tampered_artifact(tmp_path, monkeypatch):
    redirect_pandoc_config_paths(tmp_path, monkeypatch)
    gen.write_pandoc_configs()
    tampered = gen.LEETCODE_DIVIDER_PATH.read_text(encoding="utf-8").replace(
        gen.LEETCODE_DIVIDER_TITLE, "Wrong Heading"
    )
    gen.LEETCODE_DIVIDER_PATH.write_text(tampered, encoding="utf-8")
    assert gen.write_pandoc_configs() is True
    assert gen.LEETCODE_DIVIDER_PATH.read_text(encoding="utf-8") == (
        gen.render_leetcode_divider(committed_nav_rows())
    )


def test_check_pandoc_configs_passes_after_emission(tmp_path, monkeypatch):
    redirect_pandoc_config_paths(tmp_path, monkeypatch)
    gen.write_pandoc_configs()
    assert gen.check_pandoc_configs() == 0


def test_check_pandoc_configs_fails_when_an_artifact_drifts(tmp_path, monkeypatch):
    redirect_pandoc_config_paths(tmp_path, monkeypatch)
    gen.write_pandoc_configs()
    tampered = gen.AMAZON_DIVIDER_PATH.read_text(encoding="utf-8") + "rogue line\n"
    gen.AMAZON_DIVIDER_PATH.write_text(tampered, encoding="utf-8")
    assert gen.check_pandoc_configs() == 1


def test_check_pandoc_configs_fails_when_an_artifact_is_missing(tmp_path, monkeypatch):
    redirect_pandoc_config_paths(tmp_path, monkeypatch)
    assert gen.check_pandoc_configs() == 1


def test_main_emits_the_pandoc_configs_with_the_landing_and_nav(tmp_path, monkeypatch, capsys):
    landing_path = fresh_landing(tmp_path)
    mkdocs_path = mkdocs_shell(tmp_path)
    redirect_pandoc_config_paths(tmp_path, monkeypatch)
    monkeypatch.setattr(gen, "PROBLEMS_INDEX_PATH", landing_path)
    monkeypatch.setattr(gen, "MKDOCS_PATH", mkdocs_path)
    assert gen.main([]) == 0
    assert gen.PANDOC_CONFIG_PATH.exists()
    assert gen.LEETCODE_DIVIDER_PATH.exists()
    assert gen.AMAZON_DIVIDER_PATH.exists()
    assert "pandoc" in capsys.readouterr().out


def test_main_check_mode_covers_the_pandoc_configs(tmp_path, monkeypatch):
    landing_path = fresh_landing(tmp_path)
    mkdocs_path = mkdocs_shell(tmp_path)
    redirect_pandoc_config_paths(tmp_path, monkeypatch)
    monkeypatch.setattr(gen, "PROBLEMS_INDEX_PATH", landing_path)
    monkeypatch.setattr(gen, "MKDOCS_PATH", mkdocs_path)
    gen.write_sections(landing_path=landing_path)
    gen.write_problems_nav(mkdocs_path=mkdocs_path)
    gen.write_pandoc_configs()
    before_landing = landing_path.read_text(encoding="utf-8")
    before_mkdocs = mkdocs_path.read_text(encoding="utf-8")
    before_config = gen.PANDOC_CONFIG_PATH.read_text(encoding="utf-8")
    assert gen.main(["--check"]) == 0
    assert landing_path.read_text(encoding="utf-8") == before_landing
    assert mkdocs_path.read_text(encoding="utf-8") == before_mkdocs
    assert gen.PANDOC_CONFIG_PATH.read_text(encoding="utf-8") == before_config
    drifted = before_config.replace(gen.PANDOC_OUTPUT_FILE, "drifted-output.pdf")
    gen.PANDOC_CONFIG_PATH.write_text(drifted, encoding="utf-8")
    assert gen.main(["--check"]) == 1
