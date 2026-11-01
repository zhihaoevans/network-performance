#!/usr/bin/env python3
"""Validate local inline Markdown links and fence balance without network access."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
FENCE = re.compile(r"^\s*(" + chr(96) + r"{3,}|~{3,})")


def check(root):
    errors = []
    docs = sorted(root.rglob("*.md"))
    for path in docs:
        if any(p.startswith(".") for p in path.relative_to(root).parts):
            continue
        fenced, fence_char, fence_size = False, "", 0
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            marker = FENCE.match(line)
            if marker:
                token = marker.group(1)
                if not fenced:
                    fenced, fence_char, fence_size = True, token[0], len(token)
                elif token[0] == fence_char and len(token) >= fence_size:
                    fenced = False
                continue
            if fenced:
                continue
            for match in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", line):
                target = match.group(1).strip()
                if target.startswith("<") and target.endswith(">"):
                    target = target[1:-1]
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                dest = (path.parent / unquote(parsed.path)).resolve()
                try:
                    dest.relative_to(root.resolve())
                except ValueError:
                    errors.append(f"{path.relative_to(root)}:{number}: link escapes repo: {target}")
                    continue
                if not dest.exists():
                    errors.append(f"{path.relative_to(root)}:{number}: missing: {target}")
        if fenced:
            errors.append(f"{path.relative_to(root)}: unclosed code fence")
    return docs, errors


def main():
    docs, errors = check(ROOT)
    for error in errors:
        print(error, file=sys.stderr)
    print(f"Checked {len(docs)} Markdown files; {len(errors)} errors.")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
