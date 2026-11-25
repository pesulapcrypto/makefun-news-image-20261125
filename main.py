#!/usr/bin/env python3
"""THE MARKET BELL — entrypoint (Akun 12, News Image 20261125).

The bell rings once. entry.png is the finished page; this program
carries it to /output/entry.png exactly as it stands and does
nothing else. Standard library only.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    os.makedirs("/output", exist_ok=True)
    dst = os.path.join("/output", "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
