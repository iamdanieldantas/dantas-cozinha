"""Harness de execução controlada: valida, testa, relata e bloqueia falhas."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "_reports" / "harness-report.json"


def execute_step(name: str, command: list[str], timeout: int) -> dict:
    started = time.monotonic()
    try:
        proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=timeout, check=False)
        result = {
            "step": name,
            "command": command,
            "ok": proc.returncode == 0,
            "exit_code": proc.returncode,
            "stdout_tail": proc.stdout[-8000:],
            "stderr_tail": proc.stderr[-8000:],
        }
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        result = {"step": name, "command": command, "ok": False, "exit_code": None,
                  "stdout_tail": "", "stderr_tail": str(exc)}
    result["duration_seconds"] = round(time.monotonic() - started, 2)
    print(("[OK] " if result["ok"] else "[FALHOU] ") + name
          + " (" + str(result["duration_seconds"]) + "s)", flush=True)
    if not result["ok"]:
        print(result["stderr_tail"] or result["stdout_tail"], file=sys.stderr, flush=True)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="QA harness Dantas Cozinha")
    parser.add_argument("--mode", choices=["review", "release"], default="review")
    parser.add_argument("--browser", action="store_true")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    report_path = args.report if args.report.is_absolute() else ROOT / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    report = {
        "mode": args.mode, "started_at": started,
        "git_ref": os.getenv("GITHUB_REF", "local"),
        "git_sha": os.getenv("GITHUB_SHA", "local"),
        "approval_required_before_merge": True,
        "approved_by_harness": False,
        "steps": [], "ok": False,
    }

    # Evita uso acidental da rotina de release fora de main.
    if args.mode == "release" and os.getenv("GITHUB_REF") != "refs/heads/main":
        report["steps"].append({"step": "guard-main", "ok": False,
                                "stderr_tail": "Release permitido somente em refs/heads/main."})
    else:
        plan = [
            ("content-contract", [sys.executable, "-m", "harness.validate_content"], 45),
            ("unit-tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests",
                            "-p", "test_*.py", "-v"], 180),
            ("javascript-app", ["node", "--check", "assets/app.js"], 45),
            ("javascript-data", ["node", "--check", "assets/data.js"], 45),
        ]
        if args.browser:
            plan.append(("browser-smoke", [sys.executable, "tests/browser_smoke.py"], 240))
        for name, command, timeout in plan:
            result = execute_step(name, command, timeout)
            report["steps"].append(result)

    report["ok"] = bool(report["steps"]) and all(s["ok"] for s in report["steps"])
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary_file = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as summary:
            summary.write("\n## Dantas Cozinha — Harness " + args.mode + "\n")
            summary.write("**Resultado:** " + ("Aprovado nos testes" if report["ok"] else "Falhou") + "\n\n")
            summary.write("| Etapa | Resultado | Duração |\n|---|---|---|\n")
            for step in report["steps"]:
                summary.write("| " + step["step"] + " | "
                              + ("OK" if step["ok"] else "FALHOU") + " | "
                              + str(step.get("duration_seconds", "-")) + "s |\n")
            summary.write("\nAprovação humana de PR ainda é necessária para integrar alterações.\n")
    print("Relatório:", report_path)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
