#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a .wskin package from the skin/ source directory.

Usage:  python3 scripts/build.py
Output: <id>.wskin in the repository root.

The .wskin format is a plain ZIP archive with this layout:
    manifest.json
    skin.css
    assets/*
"""
import json
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "skin")


def main() -> int:
    manifest_path = os.path.join(SRC, "manifest.json")
    if not os.path.isfile(manifest_path):
        print(f"error: missing {manifest_path}", file=sys.stderr)
        return 1

    with open(manifest_path, encoding="utf-8") as fh:
        manifest = json.load(fh)

    skin_id = manifest["id"]
    version = manifest["version"]
    entry = manifest.get("entry", "skin.css")
    out = os.path.join(ROOT, f"{skin_id}.wskin")

    entries = [("manifest.json", manifest_path), (entry, os.path.join(SRC, entry))]

    assets_dir = os.path.join(SRC, "assets")
    if os.path.isdir(assets_dir):
        for name in sorted(os.listdir(assets_dir)):
            path = os.path.join(assets_dir, name)
            if os.path.isfile(path):
                entries.append((f"assets/{name}", path))

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for arcname, path in entries:
            zf.write(path, arcname)

    size = os.path.getsize(out)
    print(f"built {os.path.basename(out)}  version={version}  size={size}B")
    for arcname, _ in entries:
        print(f"  {arcname}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
