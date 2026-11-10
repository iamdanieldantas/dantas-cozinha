"""Build the browser-compatible dataset from domain JSON files.

Run: python scripts/build_dataset.py
Check without writing: python scripts/build_dataset.py --check
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ("site", "recipes", "school", "discovery", "curation")
OUTPUT = ROOT / "assets/data.js"


def assemble() -> dict:
    data = {}
    for domain in SOURCES:
        path = ROOT / "content" / f"{domain}.json"
        document = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            raise ValueError(f"{path}: expected JSON object")
        for key, value in document.items():
            if key in data:
                raise ValueError(f"Duplicate top-level key: {key}")
            data[key] = value
    return data


def render(data: dict) -> str:
    return "window.DANTAS_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail when generated JS is stale or differs semantically")
    args = parser.parse_args()
    try:
        data = assemble()
        from validate_dataset import validate
        errors = validate(data)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        expected = render(data)
        if args.check:
            from validate_dataset import load_dataset
            actual = load_dataset(OUTPUT)
            if actual != data:
                print("assets/data.js differs from content/*.json; run python scripts/build_dataset.py", file=sys.stderr)
                return 1
            print("Dataset synchronized with domain JSON sources.")
        else:
            OUTPUT.write_text(expected, encoding="utf-8")
            print(f"Generated {OUTPUT.relative_to(ROOT)}")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
