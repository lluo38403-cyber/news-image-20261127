#!/usr/bin/env python3
"""Entry point for news-image-20261127.

Copies the front-page image this repository ships (entry.png) to the
grader's output directory and checks it before finishing: it must be a
whole PNG, 1024 by 1024 pixels, and no bigger than 1 MiB. Standard
library only -- the grading sandbox installs nothing.
"""

import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def read_png_size(path):
    """Return (width, height) from a PNG's IHDR chunk, stdlib only."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("first chunk is not IHDR")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")

    size = os.path.getsize(SOURCE)
    if size > MAX_BYTES:
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB cap")
    width, height = read_png_size(SOURCE)
    if (width, height) != (1024, 1024):
        raise SystemExit(f"entry.png is {width}x{height}, must be 1024x1024")

    shutil.copyfile(SOURCE, target)
    with open(SOURCE, "rb") as fh:
        source_digest = hashlib.sha256(fh.read()).hexdigest()
    with open(target, "rb") as fh:
        target_digest = hashlib.sha256(fh.read()).hexdigest()
    if source_digest != target_digest:
        raise SystemExit("copied entry.png does not match the source bytes")
    print(f"wrote {target}: {width}x{height}, {size} bytes, "
          f"sha256 {target_digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
