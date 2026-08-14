#!/usr/bin/env python3
"""Build local marketplace submission assets."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / ".local-artifacts" / "submission-assets"


def main() -> None:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)
    write_outputs()
    write_proof_story()
    write_submission_checklist()
    screenshot_results = make_screenshots()
    summary = {
        "artifact": "Marketplace Submission Assets",
        "output_dir": str(OUT_DIR),
        "assets": sorted(str(path.relative_to(OUT_DIR)) for path in OUT_DIR.rglob("*") if path.is_file()),
        "screenshots": screenshot_results,
    }
    (OUT_DIR / "asset-manifest.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def write_outputs() -> None:
    commands = {
        "executive-decision-packet.json": ["engine/cli.py", "build-decision-packet", "--input", "engine/examples/board_prep.json"],
        "unfair-advantage-usp-suite.json": ["engine/cli.py", "unfair-advantage-usp-suite", "--input", "engine/examples/industrial_operating_review.json"],
        "usage-benchmark.json": ["engine/cli.py", "usage-benchmark", "--eval-dir", "engine/evals"],
    }
    for name, args in commands.items():
        proc = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True, check=True)
        (OUT_DIR / name).write_text(proc.stdout, encoding="utf-8")
    board_dir = OUT_DIR / "board-pack"
    subprocess.run(
        [sys.executable, "engine/cli.py", "build-board-pack", "--input", "engine/examples/board_prep.json", "--output-dir", str(board_dir), "--format", "both"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def write_proof_story() -> None:
    story = """# Before/After Proof Story

## Before

Leadership receives fragmented meeting notes, risk updates and budget signals. The update says delivery is broadly under control, but testing has not started, audit evidence is incomplete and the budget reserve is nearly consumed.

## After

The Autonomous CIO creates an Executive Decision Packet, separates facts from assumptions, maps the risk chain, exposes missing evidence, simulates board pressure, assigns next evidence requests and runs the Unfair Advantage CIO USP Suite.

## Proof

- Executive Decision Packet: `executive-decision-packet.json`
- USP Suite: `unfair-advantage-usp-suite.json`
- Board Pack export: `board-pack/`
- Usage baseline: `usage-benchmark.json`

## Safety Boundary

The assets use local demo inputs only. They do not claim live system access, automatic persistence or external action execution.
"""
    (OUT_DIR / "before-after-proof-story.md").write_text(story, encoding="utf-8")


def write_submission_checklist() -> None:
    checklist = """# Marketplace Submission Checklist

- Package built: `python scripts/build-submission-pack.py`
- Plugin validator passed on source and dist package.
- Plugin eval target: `dist/the-autonomous-cio`
- Expected Plugin Eval: 100/100, Grade A, low risk, 0 fail, 0 warn.
- Coverage artifact: `.local-artifacts/coverage/coverage.xml`
- Observed local usage: `.local-artifacts/observed-usage/observed-usage-summary.json`
- Submission assets: `.local-artifacts/submission-assets/`
- Actual marketplace upload still requires a human with the appropriate publishing account.
"""
    (OUT_DIR / "marketplace-submission-checklist.md").write_text(checklist, encoding="utf-8")


def make_screenshots() -> list[dict]:
    browser = find_browser()
    targets = [
        ("local-app.png", ROOT / "app" / "static" / "index.html"),
        ("visual-command-center.png", ROOT / "visual-command-center" / "index.html"),
    ]
    results = []
    if not browser:
        (OUT_DIR / "screenshot-plan.md").write_text("No Edge/Chrome executable was found. Open the HTML targets and capture screenshots manually.\n", encoding="utf-8")
        return [{"created": False, "reason": "No Edge/Chrome executable found"}]
    for filename, html in targets:
        output = OUT_DIR / filename
        proc = subprocess.run(
            [
                browser,
                "--headless",
                "--disable-gpu",
                "--window-size=1440,1100",
                f"--screenshot={output}",
                html.as_uri(),
            ],
            capture_output=True,
            text=True,
        )
        results.append({"file": str(output), "created": output.exists(), "exit_code": proc.returncode})
    return results


def find_browser() -> str | None:
    candidates = [
        shutil.which("msedge"),
        shutil.which("chrome"),
        shutil.which("chromium"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    return None


if __name__ == "__main__":
    main()
