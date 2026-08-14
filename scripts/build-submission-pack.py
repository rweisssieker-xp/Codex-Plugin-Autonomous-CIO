#!/usr/bin/env python3
"""Build a marketplace submission pack for The Autonomous CIO."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import zipfile
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST_PLUGIN = ROOT / "dist" / "the-autonomous-cio"
SUBMISSION_DIR = ROOT / "dist" / "submission"
ZIP_PATH = SUBMISSION_DIR / "the-autonomous-cio-marketplace-plugin.zip"


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build-marketplace-package.py")], check=True)
    if SUBMISSION_DIR.exists():
        shutil.rmtree(SUBMISSION_DIR)
    SUBMISSION_DIR.mkdir(parents=True)

    _zip_plugin()
    _write_submission_manifest()
    _write_review_notes()
    print(
        json.dumps(
            {
                "submission_dir": str(SUBMISSION_DIR),
                "plugin_zip": str(ZIP_PATH),
                "zip_size_bytes": ZIP_PATH.stat().st_size,
                "review_notes": str(SUBMISSION_DIR / "REVIEW_NOTES.md"),
            },
            indent=2,
        )
    )


def _zip_plugin() -> None:
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(DIST_PLUGIN.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(DIST_PLUGIN.parent))


def _write_submission_manifest() -> None:
    manifest = json.loads((DIST_PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    payload = {
        "artifact": "The Autonomous CIO Marketplace Submission Pack",
        "generated_on": date.today().isoformat(),
        "plugin_name": manifest["name"],
        "plugin_version": manifest["version"],
        "plugin_zip": ZIP_PATH.name,
        "skill_count": len([path for path in (DIST_PLUGIN / "skills").iterdir() if path.is_dir()]),
        "frontdoor_skill": "autonomous-cio-orchestrator",
        "default_prompts": manifest["interface"]["defaultPrompt"],
        "validation_commands": [
            "python scripts/build-marketplace-package.py",
            "python scripts/build-submission-pack.py",
            "python C:\\Users\\weiss\\.codex\\skills\\.system\\plugin-creator\\scripts\\validate_plugin.py dist\\the-autonomous-cio",
            "node C:\\Users\\weiss\\.codex\\plugins\\cache\\openai-curated-remote\\plugin-eval\\0.1.2\\scripts\\plugin-eval.js analyze dist\\the-autonomous-cio --format markdown",
        ],
    }
    (SUBMISSION_DIR / "submission-manifest.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _write_review_notes() -> None:
    notes = """# The Autonomous CIO Submission Review Notes

## Package Boundary

`the-autonomous-cio-marketplace-plugin.zip` contains the lean Codex marketplace package under `the-autonomous-cio/`.
The source repository keeps the local Python runtime, examples, schemas, tests, dashboard and long-form docs outside the marketplace package.

## Front Door

The single implicit skill is `autonomous-cio-orchestrator`. It routes broad executive requests to explicit-only specialist skills and produces integrated decision-support outputs.

## Starter Prompts

- Turn these meeting notes and risk updates into an Executive Decision Packet.
- Challenge this decision like a CEO, CFO, CISO, Audit Chair and Board member.
- Find decision debt, value leakage and missing evidence in this portfolio update.

## Safety

- No live system access is claimed.
- No external action execution is claimed.
- Memory writes require explicit local paths in the runtime and are not part of automatic plugin behavior.
- High-risk legal, regulatory, HR, security and financial outputs are decision support only.

## Evidence

Run `python engine/cli.py run-evals --eval-dir engine/evals` for the 50-case golden scenario suite.
Run `python engine/cli.py orchestrator-evals --eval-dir engine/evals` for request-type and skill-chain checks.
Run `python engine/cli.py usage-benchmark --eval-dir engine/evals` for deterministic local token estimates.
"""
    (SUBMISSION_DIR / "REVIEW_NOTES.md").write_text(notes, encoding="utf-8")


if __name__ == "__main__":
    main()
