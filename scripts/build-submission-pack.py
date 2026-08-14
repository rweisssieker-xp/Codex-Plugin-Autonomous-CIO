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
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build-marketplace-package.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    if SUBMISSION_DIR.exists():
        shutil.rmtree(SUBMISSION_DIR)
    SUBMISSION_DIR.mkdir(parents=True)

    _zip_plugin()
    _write_submission_manifest()
    _write_review_notes()
    _write_publishing_handoff()
    _copy_promotion_kit()
    print(
        json.dumps(
            {
                "submission_dir": str(SUBMISSION_DIR),
                "plugin_zip": str(ZIP_PATH),
                "zip_size_bytes": ZIP_PATH.stat().st_size,
                "review_notes": str(SUBMISSION_DIR / "REVIEW_NOTES.md"),
                "publishing_handoff": str(SUBMISSION_DIR / "PUBLISHING_HANDOFF.md"),
                "promotion_kit": str(SUBMISSION_DIR / "NEUTRAL_PROMOTION_KIT.md"),
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
            "python scripts/run-observed-usage-benchmark.py",
            "python scripts/run-coverage-artifact.py",
            "python scripts/build-submission-assets.py",
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
Run `python scripts/run-observed-usage-benchmark.py` for observed local CLI runtime records.
Run `python scripts/run-coverage-artifact.py` for `.local-artifacts/coverage/coverage.xml`.
Run `python scripts/build-submission-assets.py` for screenshots, proof story, board-pack examples and submission checklist.
"""
    (SUBMISSION_DIR / "REVIEW_NOTES.md").write_text(notes, encoding="utf-8")


def _write_publishing_handoff() -> None:
    handoff = """# Publishing Handoff

## Start Here

1. Plugin entrypoint: `autonomous-cio-orchestrator`.
2. Primary prompt: `Turn this update into an Executive Decision Packet.`
3. Local proof command: `python engine/cli.py unfair-advantage-usp-suite --input engine/examples/industrial_operating_review.json`.
4. Submission ZIP: `the-autonomous-cio-marketplace-plugin.zip`.
5. Optional proof assets: `.local-artifacts/submission-assets/`.

## Human Upload Gate

The repository can build, validate and package the marketplace submission locally. Actual marketplace upload still requires a human publisher account and cannot be completed by the local runtime.

## Files to Upload or Attach

- Plugin ZIP: `the-autonomous-cio-marketplace-plugin.zip`
- Review notes: `REVIEW_NOTES.md`
- Submission manifest: `submission-manifest.json`
- Optional assets: run `python scripts/build-submission-assets.py` and attach `.local-artifacts/submission-assets/`

## Evidence to Run Before Upload

```text
python scripts/run-engine-smoke-tests.ps1
python scripts/run-observed-usage-benchmark.py
python scripts/run-coverage-artifact.py
python scripts/build-submission-assets.py
node C:\\Users\\weiss\\.codex\\plugins\\cache\\openai-curated-remote\\plugin-eval\\0.1.2\\scripts\\plugin-eval.js analyze dist\\the-autonomous-cio --observed-usage .local-artifacts\\observed-usage\\plugin-eval-observed-usage.jsonl --format markdown
```

Expected plugin-eval result: 100/100, Grade A, low risk, 0 fail, 0 warn.

## Claim Boundary

- Connector-neutral and local-first.
- No live system access without separately authorized host connectors.
- No automatic persistence.
- No external action execution.
- Decision support only for legal, regulatory, HR, security and financial matters.
"""
    (SUBMISSION_DIR / "PUBLISHING_HANDOFF.md").write_text(handoff, encoding="utf-8")


def _copy_promotion_kit() -> None:
    source = ROOT / "docs" / "neutral-promotion-kit.md"
    target = SUBMISSION_DIR / "NEUTRAL_PROMOTION_KIT.md"
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


if __name__ == "__main__":
    main()
