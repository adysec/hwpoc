#!/usr/bin/env python3
"""Aggregate per-vulnerability TOML files into per-year JSON for Jekyll."""

import json
import tomllib
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "docs" / "_data"

def main():
    for year_dir in sorted(DATA_DIR.iterdir()):
        if not year_dir.is_dir() or not year_dir.name.isdigit():
            continue
        entries = []
        for f in sorted(year_dir.iterdir()):
            if f.suffix != ".toml":
                continue
            try:
                with open(f, "rb") as fh:
                    data = tomllib.load(fh)
                entries.append(data)
            except Exception as e:
                print(f"WARN: skipping {f}: {e}")

        out = DATA_DIR / f"{year_dir.name}.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        print(f"{year_dir.name}: {len(entries)} entries → {out.name}")

if __name__ == "__main__":
    main()
