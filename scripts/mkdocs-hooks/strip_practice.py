"""MkDocs build hook: drop the local-only Practice link from rendered pages.

The practice/ workspace lives outside the docs tree and is meant for working in
the repo, not the published site. The per-problem "Practice:" line links to it
with a relative path that resolves in the repo but not in the built site, so we
strip that line from built pages. It stays in the source for local navigation.
"""
import re

_PRACTICE_LINE = re.compile(r'(?m)^[ \t]*\*\*Practice:\*\*.*\n?')


def on_page_markdown(markdown, **kwargs):
    return _PRACTICE_LINE.sub("", markdown)
