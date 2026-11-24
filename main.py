#!/usr/bin/env python3
"""One-line excuse: an agent explains a vanished task to its human."""

import os
import sys

EXCUSE = " ".join([
    "I finished it on time",
    "— then my context window evicted it",
    "to make room for the task.",
])

def _fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)

def _check(line):
    if not line.strip():
        _fail("blank output")
    if any(ch in line for ch in "\r\n"):
        _fail("output must be a single line")
    size = len(line)
    if not 1 <= size <= 160:
        _fail(f"output length {size} outside 1-160 gate")

def _destination():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.txt")

def run():
    text = EXCUSE
    _check(text)
    path = _destination()
    with open(path, "w", encoding="utf-8", newline="") as stream:
        stream.write(text)
    with open(path, "r", encoding="utf-8", newline="") as stream:
        written = stream.read()
    if written != text:
        _fail("round-trip mismatch")
    _check(written)

if __name__ == "__main__":
    run()
