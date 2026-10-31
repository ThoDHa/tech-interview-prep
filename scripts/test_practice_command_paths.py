"""Layout guard for command lines embedded in practice sources.

Commands embedded in practice docstrings and prose resolve from `practice/`,
so every `uv run python|pytest` path argument must start with a bank
directory (`leetcode/`, `amazon/`). The root tooling is invoked from
`practice/` itself and is allowlisted by bare filename; the tokens after an
allowlisted root tool are that tool's own arguments, not command paths.
Flags may precede the paths (`uv run pytest -m full leetcode/<slug>/`), a
token carrying a backtick ends an inline-code span, and one invocation may
carry several paths: every token after the tool name is classified, flags
are skipped (a value-taking flag consumes its value too), and every
remaining token must conform. Run with:

    cd practice && uv run pytest ../scripts/
"""

import re
import textwrap
from pathlib import Path
from typing import Iterator, List

SCRIPTS_DIR = Path(__file__).resolve().parent
PRACTICE_DIR = SCRIPTS_DIR.parent / "practice"

ALLOWED_ROOT_FILES = {"progress.py", "test_progress.py"}
COMMAND = re.compile(r"uv run (?:python|pytest)\b")
BANK_PREFIXED = re.compile(r"^(?:leetcode|amazon)/")
COMMAND_END = re.compile(r"^(?:#|&&|\|\||[;|<>])")
# A token carrying a backtick closes an inline-code span: the command ends
# with that token, and the prose after it is not part of the invocation.
INLINE_CODE_END = "`"
# Flags that consume the following token as their value, so the value is not
# mistaken for a path argument; any other `-` token is treated as value-free.
# A value-taking flag missing here fails safe: its value reads as a path and
# is flagged, and the flag then lands in this set.
VALUE_TAKING_FLAGS = {
    "-c",
    "-k",
    "-m",
    "-n",
    "-o",
    "-p",
    "-r",
    "-W",
    "-X",
    "--capture",
    "--color",
    "--deselect",
    "--maxfail",
    "--rootdir",
    "--tb",
    "--timeout",
    "--verbosity",
}


def command_path_violations(root: Path = PRACTICE_DIR) -> List[str]:
    """Collect every embedded command path that is neither bank-prefixed nor allowlisted."""
    violations = []
    for path in sorted(root.rglob("*.py")):
        # Hidden and virtualenv directories hold environment-owned content
        # (`.venv` site-packages alone is hundreds of files), not the repo
        # sources this guard protects.
        directory_parts = path.relative_to(root).parts[:-1]
        if any(part.startswith(".") or part == "venv" for part in directory_parts):
            continue
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            for match in COMMAND.finditer(line):
                violations.extend(
                    f"{path}: line {line_number}: {token}"
                    for token in command_path_tokens(line, match.end())
                    if not path_token_conforms(token)
                )
    return violations


def command_path_tokens(line: str, start: int) -> Iterator[str]:
    """Yield the path tokens of one `uv run python|pytest` invocation.

    Walks the whitespace-separated tokens after the tool name, stopping at a
    comment, shell control token, closing inline-code backtick, or allowlisted
    root tool (its remaining tokens are its own arguments); flags are
    skipped, and the value of a value-taking flag is consumed with it.

    Args:
        line: The full source line containing the invocation.
        start: Offset just past the matched `uv run python|pytest` prefix.

    Returns:
        Path tokens in line order.
    """
    tokens = line[start:].split()
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if COMMAND_END.match(token):
            return
        if not token.startswith("-"):
            yield token
            if token in ALLOWED_ROOT_FILES:
                return
        elif "=" not in token and token in VALUE_TAKING_FLAGS:
            index += 1
        if INLINE_CODE_END in token:
            return
        index += 1


def path_token_conforms(token: str) -> bool:
    """Report whether one command path token resolves from `practice/`."""
    return token in ALLOWED_ROOT_FILES or bool(BANK_PREFIXED.match(token))


def test_embedded_command_paths_use_bank_prefix_or_root_allowlist():
    violations = command_path_violations()
    assert not violations, "\n".join(violations)


def test_flag_only_command_leaves_no_path_to_flag(tmp_path):
    _write_scratch(
        tmp_path,
        """
        Run pieces of the workspace:

            uv run pytest -q
            uv run pytest -m full
            uv run python -m harness
        """,
    )
    assert command_path_violations(tmp_path) == []


def test_inline_code_span_ends_the_invocation(tmp_path):
    _write_scratch(
        tmp_path,
        """
        echo "Try `uv run pytest -q` from practice/ to reproduce."
        echo "run `uv run pytest leetcode/two_sum/` first"
        echo "run `uv run pytest scratch.py` never"
        """,
    )
    violations = command_path_violations(tmp_path)
    assert [violation.split(": ")[-1] for violation in violations] == ["scratch.py`"]


def test_root_tool_arguments_are_not_command_paths(tmp_path):
    _write_scratch(
        tmp_path,
        """
            uv run python progress.py scan
            uv run python progress.py rate two_sum shaky
        """,
    )
    assert command_path_violations(tmp_path) == []


def test_flag_form_command_still_guards_the_path(tmp_path):
    _write_scratch(
        tmp_path,
        """
            uv run pytest -m full scratch.py
            uv run pytest -m full leetcode/two_sum/
        """,
    )
    assert command_path_violations(tmp_path) == [
        f"{tmp_path / 'problem.py'}: line 2: scratch.py"
    ]


def test_every_path_token_of_one_invocation_is_guarded(tmp_path):
    _write_scratch(
        tmp_path,
        """
            uv run pytest leetcode/two_sum/ scratch.py amazon/lru_cache/
        """,
    )
    assert command_path_violations(tmp_path) == [
        f"{tmp_path / 'problem.py'}: line 2: scratch.py"
    ]


def test_second_invocation_on_a_line_is_guarded(tmp_path):
    _write_scratch(
        tmp_path,
        """
            uv run pytest leetcode/two_sum/ && uv run pytest scratch.py | tee out
        """,
    )
    assert command_path_violations(tmp_path) == [
        f"{tmp_path / 'problem.py'}: line 2: scratch.py"
    ]


def _write_scratch(root: Path, body: str) -> None:
    problem = root / "problem.py"
    problem.write_text(textwrap.dedent(body), encoding="utf-8")
