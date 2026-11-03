"""Counts guard for the tree counts quoted on README and the practice workspace page.

README and docs/interview-prep/practice_workspace.md quote tree counts as of
October 2026: the bank totals (410 Amazon problems, 168 LeetCode folders),
the write-up wave progress (213 of 410), the compiled PDF page count (578 =
168 + 410), the workspace reference-file counts (91 of 168, 47 of 410), the
cases-only Amazon folder count (363 of 410), the reference-test Amazon
folder count (47 of 410), and the fresh-clone skip floor
(over 3,100). This guard re-counts the tree and fails on drift: a wave
landing that adds or removes problems, write-ups, or case files must update
the quoted counts in the same change. The skip floor is proven twice: the
collected total is the cheap first gate, and a static recount of the skip
items on the stub tree (per-case items in folders whose solution still
raises NotSolved plus firing module-level skips) proves the floor sits
below the stub skip population. Constructor-only cases of a counted stub
(an implemented `__init__` per the design-class exemplar) pass a run while
the recount still counts them, so the recount bounds the run's skips from
above and the collected-total gate carries the lower-bound proof.
Rewording a quoted sentence also fails the guard on purpose, so the new
wording and these regexes are updated together. Run with:

    cd practice && uv run pytest ../scripts/
"""

import ast
import pytest
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

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


def amazon_reference_test_folders() -> int:
    """Count the Amazon folders carrying a `cases_full.json` and a reference test.

    The workspace page's second counts sentence names these as the folders
    that run their whole set under a plain `uv run pytest amazon/<slug>/`:
    the `cases_full.json` gauntlet plus the `test_reference_<slug>.py`
    module replaying it against `reference.py`.
    """
    return sum(
        1
        for folder in (PRACTICE_DIR / "amazon").iterdir()
        if folder.is_dir()
        and (folder / "cases_full.json").exists()
        and any(folder.glob("test_reference_*.py"))
    )


def collect_workspace_items_stdout() -> str:
    """Collect the practice workspace's test items in a subprocess.

    The workspace skip floor claims a property of a full fresh-clone run;
    collecting the workspace's items (no execution) recounts it. The same
    interpreter runs so the workspace's own environment applies, and the
    cache provider stays off so the collection writes nothing.

    Returns:
        pytest's collection output for the workspace.

    Raises:
        AssertionError: When the collection fails.
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
    return completed.stdout


def collect_workspace_test_items() -> int:
    """Count the practice workspace's collected test items.

    Returns:
        The number of test items the workspace collects.

    Raises:
        AssertionError: When the collection fails or reports no count.
    """
    collected_output = collect_workspace_items_stdout()
    match = re.search(r"(\d+) tests collected", collected_output)
    assert match, f"collection output carried no count: {collected_output[-1000:]}"
    return int(match.group(1))


def function_raises_not_solved(function_node: ast.FunctionDef) -> bool:
    """Check whether a function's body is a docstring plus `raise NotSolved`."""
    body = function_node.body
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        body = body[1:]
    return (
        len(body) == 1
        and isinstance(body[0], ast.Raise)
        and isinstance(body[0].exc, ast.Name)
        and body[0].exc.id == "NotSolved"
        and body[0].cause is None
    )


def folder_solution_raises_not_solved(folder: Path) -> bool:
    """Check whether a problem folder's solution stub is still untouched.

    One public entry point whose body is a docstring plus `raise NotSolved`
    marks the folder a fresh-clone stub whose per-case items all skip.
    Implemented scaffolding does not disqualify a folder: design classes
    ship with a working `__init__` (min_stack and the other design
    skeletons), and some stubs carry provided-API helpers that stay
    implemented forever (first_bad_version's `isBadVersion`), so private
    and dunder names stay out of the entry points.

    Args:
        folder: Problem folder under `practice/leetcode` or `practice/amazon`
            carrying a `solution.py`.

    Returns:
        True when at least one public entry point still raises NotSolved.
    """
    solution_tree = ast.parse((folder / "solution.py").read_text(encoding="utf-8"))
    for node in solution_tree.body:
        if isinstance(node, ast.ClassDef):
            entry_points = [
                child for child in node.body if isinstance(child, ast.FunctionDef)
            ]
        elif isinstance(node, ast.FunctionDef):
            entry_points = [node]
        else:
            continue
        for entry_point in entry_points:
            if entry_point.name.startswith("_"):
                continue
            if function_raises_not_solved(entry_point):
                return True
    return False


def load_solution_target_names(tree: ast.Module) -> Tuple[Set[str], Set[str]]:
    """Split a test module's `load_solution` targets by which file they load.

    `solution = load_solution(__file__)` loads the learner's stub, whose
    calls turn into NotSolved skips; a second argument (e.g.
    `reference = load_solution(__file__, "reference.py")`) loads a worked
    reference whose tests pass on a fresh clone.

    Args:
        tree: The test module's parsed AST.

    Returns:
        A tuple of (stub-side target names, reference-side target names).
    """
    solution_names: Set[str] = set()
    reference_names: Set[str] = set()
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        value = node.value
        if not (
            isinstance(value, ast.Call)
            and isinstance(value.func, ast.Name)
            and value.func.id == "load_solution"
        ):
            continue
        target_names = {
            target.id for target in node.targets if isinstance(target, ast.Name)
        }
        if len(value.args) > 1 or value.keywords:
            reference_names |= target_names
        else:
            solution_names |= target_names
    return solution_names, reference_names


def unconditional_skip_statement(function_node: ast.FunctionDef) -> bool:
    """Check whether a function's direct statements call `pytest.skip`.

    Only direct child statements count: a skip guarded by an `if` or a
    `try` (the NotSolved catch form) is conditional and stays out. The
    design-bridge modules call `pytest.skip` unconditionally per case,
    so their items skip regardless of the solution's state.
    """
    return any(
        isinstance(statement, ast.Expr)
        and isinstance(statement.value, ast.Call)
        and isinstance(statement.value.func, ast.Attribute)
        and statement.value.func.attr == "skip"
        for statement in function_node.body
    )


def module_stub_skip_functions(module_file: Path) -> Set[str]:
    """Name a test module's test functions whose items skip on the stub tree.

    A test function's items are fresh-clone skips when its body, or any
    module-level helper it reaches, references a stub-side `load_solution`
    target (the NotSolved catch turns the call into a skip) or calls
    `pytest.skip` unconditionally. Functions exercising only a reference
    pass on a fresh clone and stay out, so a shared module such as the
    leetcode reference folders' `test_solution` plus `test_reference_cases`
    pair contributes only its solution-side items.

    Args:
        module_file: The test module's path.

    Returns:
        The names of test functions whose collected items skip on a
        fresh clone.
    """
    module_tree = ast.parse(module_file.read_text(encoding="utf-8"))
    solution_names, _reference_names = load_solution_target_names(module_tree)
    helpers = {
        node.name: node for node in module_tree.body if isinstance(node, ast.FunctionDef)
    }

    def reaches_skip(function_node: ast.FunctionDef) -> bool:
        reachable = [function_node]
        visited_names = {function_node.name}
        pending = [function_node]
        while pending:
            current = pending.pop()
            for inner in ast.walk(current):
                if not (isinstance(inner, ast.Call) and isinstance(inner.func, ast.Name)):
                    continue
                callee_name = inner.func.id
                if callee_name in helpers and callee_name not in visited_names:
                    visited_names.add(callee_name)
                    reachable.append(helpers[callee_name])
                    pending.append(helpers[callee_name])
        return any(
            solution_names.intersection(
                inner.id
                for inner in ast.walk(reachable_node)
                if isinstance(inner, ast.Name)
            )
            or unconditional_skip_statement(reachable_node)
            for reachable_node in reachable
        )

    return {
        node.name
        for node in module_tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name.startswith("test")
        and reaches_skip(node)
    }


def module_cases_literal_length(tree: ast.Module) -> Optional[int]:
    """Return the length of a test module's literal `CASES` list, if it has one."""
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "CASES"
                for target in node.targets
            )
            and isinstance(node.value, ast.List)
        ):
            return len(node.value.elts)
    return None


def module_level_skip_fires(module_file: Path) -> bool:
    """Decide statically whether a test module's module-level skip fires.

    A module-level skip contributes exactly one skipped item to a run.
    The generated forms are a bare `pytest.skip(..., allow_module_level=True)`
    and one guarded by `if len(CASES) == 0:` over a literal `CASES` list:
    the bare form fires, the guarded form fires only when the committed
    `CASES` literal is empty, and a skip under any other guard resolves
    to not firing so the recount stays a lower bound.

    Args:
        module_file: The test module's path.

    Returns:
        True when the module contributes a skipped item on the committed tree.
    """
    module_tree = ast.parse(module_file.read_text(encoding="utf-8"))
    cases_length = module_cases_literal_length(module_tree)

    def is_empty_cases_guard(test_node: ast.expr) -> bool:
        return (
            isinstance(test_node, ast.Compare)
            and isinstance(test_node.left, ast.Call)
            and isinstance(test_node.left.func, ast.Name)
            and test_node.left.func.id == "len"
            and len(test_node.left.args) == 1
            and isinstance(test_node.left.args[0], ast.Name)
            and test_node.left.args[0].id == "CASES"
            and len(test_node.comparators) == 1
            and isinstance(test_node.comparators[0], ast.Constant)
            and test_node.comparators[0].value == 0
        )

    def scan(statements: List[ast.stmt], guard_state: int) -> bool:
        guard_bare, guard_empty_cases, guard_unrecognized = 0, 1, 2
        for statement in statements:
            if isinstance(statement, ast.If):
                if is_empty_cases_guard(statement.test):
                    child_state = max(guard_state, guard_empty_cases)
                else:
                    child_state = max(guard_state, guard_unrecognized)
                if scan(statement.body, child_state) or scan(statement.orelse, guard_state):
                    return True
                continue
            if not (
                isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call)
            ):
                continue
            call = statement.value
            if not (
                isinstance(call.func, ast.Attribute)
                and call.func.attr == "skip"
                and any(
                    keyword.arg == "allow_module_level" and keyword.value
                    for keyword in call.keywords
                )
            ):
                continue
            if guard_state == guard_bare:
                return True
            if guard_state == guard_empty_cases and cases_length == 0:
                return True
        return False

    return scan(module_tree.body, 0)


def stub_skip_items_by_module() -> Dict[str, int]:
    """Count each test module's per-case skip items, without execution.

    One collection pass supplies every test function's item count;
    `module_stub_skip_functions` decides which functions' items skip on
    the committed stub tree. Reference-only functions' items (which pass
    on a fresh clone) stay out by construction.

    Returns:
        A mapping of module path relative to `practice/` to the number of
        that module's items that skip on a fresh clone.
    """
    collected_output = collect_workspace_items_stdout()
    items_per_function: Dict[Tuple[str, str], int] = {}
    for line in collected_output.splitlines():
        parts = line.split("::")
        if len(parts) < 2 or not parts[0].endswith(".py"):
            continue
        module_path = parts[0]
        function_name = parts[1].split("[", 1)[0]
        function_key = (module_path, function_name)
        items_per_function[function_key] = items_per_function.get(function_key, 0) + 1
    skip_functions_cache: Dict[str, Set[str]] = {}
    items_by_module: Dict[str, int] = {}
    for (module_path, function_name), item_count in items_per_function.items():
        if module_path not in skip_functions_cache:
            module_file = PRACTICE_DIR / module_path
            skip_functions_cache[module_path] = module_stub_skip_functions(module_file)
        if function_name in skip_functions_cache[module_path]:
            items_by_module[module_path] = items_by_module.get(module_path, 0) + item_count
    return items_by_module


def workspace_skip_recount() -> int:
    """Recount the workspace's fresh-clone skips statically, without a run.

    Sums the two skip classes the page's floor claims: the per-case items
    of every folder whose solution entry points still raise NotSolved
    (design-class methods included), plus one item per test module whose
    module-level skip fires. Item counts come from a single collection
    pass, so nothing executes. Unrecognized skip shapes resolve to zero.
    Constructor-only cases of a counted stub (an implemented `__init__`
    per the design-class exemplar) pass a run while the recount still
    counts them, so the recount bounds a fresh-clone run's skips from
    above by exactly those items; the collected-total gate keeps the
    floor's lower-bound proof.

    Returns:
        The static count of skip items on the committed tree.
    """
    stub_items = stub_skip_items_by_module()
    recount = 0
    for bank in ("leetcode", "amazon"):
        bank_dir = PRACTICE_DIR / bank
        for folder in bank_dir.iterdir():
            if not folder.is_dir() or not (folder / "solution.py").exists():
                continue
            if folder_solution_raises_not_solved(folder):
                recount += stub_items.get(f"{bank}/{folder.name}/test_{folder.name}.py", 0)
        for module_file in bank_dir.glob("*/test_*.py"):
            if module_level_skip_fires(module_file):
                recount += 1
    return recount


def bank_solutions_still_raise_not_solved() -> bool:
    """Check whether every bank folder's solution is still a NotSolved stub.

    Walks the same solution-carrying folder population
    `workspace_skip_recount` counts and applies the same stub predicate,
    so the scaffold-state check and the recount stay in step by
    construction. The state holds on a fresh clone of main and breaks
    the moment a solution entry point gets implemented.

    Returns:
        True while no bank folder has left the scaffold stub state.
    """
    for bank in ("leetcode", "amazon"):
        bank_dir = PRACTICE_DIR / bank
        for folder in bank_dir.iterdir():
            if not folder.is_dir() or not (folder / "solution.py").exists():
                continue
            if not folder_solution_raises_not_solved(folder):
                return False
    return True


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


def test_workspace_page_reference_test_count_matches_the_tree():
    page = WORKSPACE_PAGE.read_text(encoding="utf-8")
    match = re.search(
        r"and the (\d+) that also carry"
        r" `cases_full\.json` and a reference test",
        page,
    )
    assert match, (
        "the practice workspace page no longer carries the expected"
        " reference-test sentence ('the N that also carry `cases_full.json`"
        " and a reference test'); update the sentence together with this"
        " regex"
    )
    quoted = int(match.group(1))
    actual = amazon_reference_test_folders()
    assert quoted == actual, (
        f"the practice workspace page counts {quoted} but the tree has"
        f" {actual} (Amazon folders carrying both a cases_full.json and a"
        " reference test); update the page counts in the same change as"
        " the tree"
    )


def workspace_page_skip_floor(page: str) -> int:
    """Extract the skip floor quoted on the practice workspace page.

    Args:
        page: The page text carrying the 'wall of skips, over N' sentence.

    Returns:
        The quoted floor as an integer.

    Raises:
        AssertionError: When the page no longer carries the sentence.
    """
    match = re.search(r"wall of skips, over ([\d,]+) across the workspace", page)
    assert match, (
        "the practice workspace page no longer carries the expected skip"
        " sentence ('a wall of skips, over N across the workspace'); update"
        " the sentence together with this regex"
    )
    return int(match.group(1).replace(",", ""))


def test_workspace_page_skip_floor_holds_against_the_workspace():
    page = WORKSPACE_PAGE.read_text(encoding="utf-8")
    floor = workspace_page_skip_floor(page)
    collected = collect_workspace_test_items()
    assert collected > floor, (
        f"the practice workspace page claims over {floor} skips but the"
        f" workspace collects only {collected} test items; lower the quoted"
        " floor in the same change as the tree"
    )


def test_workspace_page_skip_floor_below_the_static_skip_recount():
    """Prove the page's floor below the static recount on the stub tree.

    Branch dependence: the floor ("over 3,100") describes the scaffold
    bank a fresh clone of main hands out, while the recount is
    tree-relative. Implemented solution.py files (the owner's solved
    set on the practice branch) drop their folders from the stub
    population, and the recount tracks a run's skips through that
    change within the documented constructor-only delta, so the
    consistency proof holds in every tree state while only the all-stub
    scaffold still clears the floor. The floor comparison therefore
    applies while every bank solution still raises NotSolved; a tree
    past that state skips the claim instead of failing it.
    """
    page = WORKSPACE_PAGE.read_text(encoding="utf-8")
    floor = workspace_page_skip_floor(page)
    if not bank_solutions_still_raise_not_solved():
        pytest.skip(
            "the tree is past the scaffold state the floor describes:"
            " implemented solutions turned their stub skips into passes,"
            " so the over-N floor claim no longer applies to this tree"
        )
    recount = workspace_skip_recount()
    assert recount > floor, (
        f"the practice workspace page claims over {floor} skips but the"
        f" static recount counts only {recount} fresh-clone skip items"
        " (per-case items on stubs plus firing module-level skips); lower"
        " the quoted floor in the same change as the tree"
    )
