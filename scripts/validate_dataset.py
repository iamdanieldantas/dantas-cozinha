"""Validate the published editorial dataset without modifying it.

Usage: python scripts/validate_dataset.py
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
COLLECTIONS = ("recipes", "techniques", "workshops", "videos")
REQUIRED = {
    "recipes": ("id", "title", "ingredients", "steps"),
    "techniques": ("id", "title", "category"),
    "workshops": ("id", "name", "url"),
    "videos": ("id", "title", "url"),
}


def load_dataset(path: Path | None = None) -> dict:
    source = (path or ROOT / "assets/data.js").read_text(encoding="utf-8")
    match = re.fullmatch(r"\s*window\.DANTAS_DATA\s*=\s*(\{.*\})\s*;?\s*", source, re.DOTALL)
    if not match:
        raise ValueError("Expected window.DANTAS_DATA assignment containing JSON")
    data = json.loads(match.group(1))
    if not isinstance(data, dict):
        raise ValueError("Dataset root must be an object")
    return data


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for collection in COLLECTIONS:
        entries = data.get(collection)
        if not isinstance(entries, list):
            errors.append(f"{collection}: expected array")
            continue
        for index, entry in enumerate(entries):
            location = f"{collection}[{index}]"
            if not isinstance(entry, dict):
                errors.append(f"{location}: expected object")
                continue
            for field in REQUIRED[collection]:
                if field not in entry or entry[field] is None or entry[field] == "":
                    errors.append(f"{location}: missing {field}")
            identifier = entry.get("id")
            if not isinstance(identifier, str) or not identifier.strip():
                errors.append(f"{location}: invalid id")
            elif identifier in seen:
                errors.append(f"{location}: duplicate id {identifier}")
            else:
                seen.add(identifier)
            if collection == "recipes":
                if not isinstance(entry.get("ingredients"), list) or not entry["ingredients"]:
                    errors.append(f"{location}: ingredients must be nonempty array")
                if not isinstance(entry.get("steps"), list) or not entry["steps"]:
                    errors.append(f"{location}: steps must be nonempty array")
                servings = entry.get("servings")
                if not isinstance(servings, (int, float)) or isinstance(servings, bool) or servings <= 0:
                    errors.append(f"{location}: invalid servings")
            if collection == "techniques":
                blocks = entry.get("contentBlocks", [])
                if not isinstance(blocks, list):
                    errors.append(f"{location}: contentBlocks must be array when present")
            if collection in ("workshops", "videos"):
                url = entry.get("url")
                if not isinstance(url, str) or urlparse(url).scheme != "https" or not urlparse(url).netloc:
                    errors.append(f"{location}: invalid HTTPS URL")
                verified = entry.get("verifiedAt")
                if verified is not None and (not isinstance(verified, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", verified)):
                    errors.append(f"{location}: invalid verifiedAt")
    return errors


def main() -> int:
    try:
        errors = validate(load_dataset())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Dataset could not be parsed: {exc}", file=sys.stderr)
        return 1
    for error in errors:
        print("ERROR:", error, file=sys.stderr)
    if errors:
        print(f"Dataset rejected: {len(errors)} issue(s)", file=sys.stderr)
        return 1
    print("Dataset valid: recipes, techniques, workshops and videos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
