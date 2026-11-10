"""Check a conservative static JS/CSS transfer-size budget.

Does not replace field Lighthouse measurements. Run from repository root.
"""
from pathlib import Path
import gzip
import sys

ROOT=Path(__file__).resolve().parents[1]
BUDGETS={
    "assets/app.js": 18_000,
    "assets/data.js": 45_000,
    "assets/styles.css": 14_000,
}


def audit():
    failures=[]
    for name,budget in BUDGETS.items():
        raw=(ROOT/name).read_bytes()
        compressed=len(gzip.compress(raw,compresslevel=9,mtime=0))
        print(f"{name}: {compressed} gzip bytes / {budget} budget")
        if compressed>budget:
            failures.append(name)
    return failures


if __name__=="__main__":
    failed=audit()
    if failed:
        print("Exceeded budgets: "+", ".join(failed),file=sys.stderr)
    raise SystemExit(bool(failed))
