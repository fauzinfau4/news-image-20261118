#!/usr/bin/env python3
"""news-image-20261118 entry: copy the baked-in image to the output dir.

The image (entry.png, drawn by draw.py) sums up the world news of
Wednesday 18 November 2026. Copying fixed bytes keeps both graded runs
byte-identical with no network access. Standard library only.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.png")
    # MAKEFUN_OUTPUT_DIR is a directory in the grader; tolerate a file path.
    if out_dir.endswith(".png"):
        dest = out_dir
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    else:
        os.makedirs(out_dir, exist_ok=True)
        dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(os.path.join(HERE, "entry.png"), dest)


if __name__ == "__main__":
    main()
