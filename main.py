#!/usr/bin/env python3
"""One Line to Stop the Scroll — make.fun bounty u-febri-yudila-one-line-to-stop-the-scroll-e8b18425.

Writes one line of text to $MAKEFUN_OUTPUT_DIR/entry.txt (default
/output). The line is the whole entry: a single sentence meant to make
a stranger stop scrolling and smile. Pure standard library, fully
deterministic: the same bytes on every run.
"""

import os
import sys
import tempfile

# The line: the reader has just scrolled past the usual feed — an ex,
# an absurd wedding, ads for things already owned — and this is the one
# thing today that is not trying to sell them anything.
LINE = (
    "You just scrolled past your ex, a man marrying a pizza, "
    "and three ads for socks you already own. Stop here — "
    "this line is the only thing today that isn't selling you something."
)

MAX_CHARS = 200


def check_line(line: str) -> str:
    """Return the line unchanged, or raise ValueError if it breaks the gate."""
    if not line.strip():
        raise ValueError("entry line is blank")
    if line != line.strip():
        raise ValueError("entry line has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be exactly one line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"entry is {len(line)} chars, over the {MAX_CHARS} limit")
    line.encode("utf-8")  # raises if the text is not valid UTF-8
    return line


def write_entry(line: str) -> str:
    """Write the line to entry.txt atomically; return the path written."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    payload = line.encode("utf-8")
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
        os.replace(tmp_path, target)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    with open(target, "rb") as handle:
        if handle.read() != payload:
            raise ValueError("entry.txt does not match the line")
    return target


def main() -> int:
    try:
        line = check_line(LINE)
        target = write_entry(line)
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {len(line)} chars to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
