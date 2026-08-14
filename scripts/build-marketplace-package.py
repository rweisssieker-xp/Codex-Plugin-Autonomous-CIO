#!/usr/bin/env python3
"""Build a lean Codex marketplace package from the full source repository.

The source repo intentionally contains runtime code, docs, schemas, tests and demos.
Marketplace evaluation should run against the installable plugin package, not the
full engineering workspace. This builder keeps the package local-first and skill
complete while excluding runtime/demo files that are not loaded by Codex as skills.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "dist" / "the-autonomous-cio"
LEGAL_DOCS = ("privacy-policy.md", "terms-of-service.md")
FRONTDOOR_SKILL = "autonomous-cio-orchestrator"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the lean marketplace plugin package.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Output directory for the generated plugin package.",
    )
    return parser.parse_args()


def copy_manifest(target: Path) -> dict:
    source = ROOT / ".codex-plugin" / "plugin.json"
    manifest = json.loads(source.read_text(encoding="utf-8"))
    manifest["skills"] = "./skills/"

    manifest_dir = target / ".codex-plugin"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    (manifest_dir / "plugin.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest


def skill_display_name(skill_name: str) -> str:
    return " ".join(part.upper() if part in {"ai", "cio", "ciso", "it", "ot", "qms"} else part.capitalize()
                    for part in skill_name.split("-"))


def minified_agent_yaml(skill_name: str) -> str:
    display = skill_display_name(skill_name)
    return (
        "interface:\n"
        f"  display_name: \"{display}\"\n"
        "  short_description: \"Explicit-only.\"\n"
        "policy:\n"
        "  allow_implicit_invocation: false\n"
    )


def copy_skills(target: Path) -> tuple[int, int]:
    source_root = ROOT / "skills"
    target_root = target / "skills"
    copied = 0
    explicit_only = 0

    for skill_root in sorted(path for path in source_root.iterdir() if path.is_dir()):
        skill_md = skill_root / "SKILL.md"
        if not skill_md.is_file():
            continue

        package_skill = target_root / skill_root.name
        package_skill.mkdir(parents=True, exist_ok=True)
        shutil.copy2(skill_md, package_skill / "SKILL.md")
        copied += 1

        if skill_root.name != FRONTDOOR_SKILL:
            agents_dir = package_skill / "agents"
            agents_dir.mkdir(parents=True, exist_ok=True)
            (agents_dir / "openai.yaml").write_text(
                minified_agent_yaml(skill_root.name),
                encoding="utf-8",
            )
            explicit_only += 1

    return copied, explicit_only


def copy_legal_docs(target: Path) -> int:
    docs_target = target / "docs"
    docs_target.mkdir(parents=True, exist_ok=True)
    copied = 0
    for name in LEGAL_DOCS:
        source = ROOT / "docs" / name
        if source.is_file():
            shutil.copy2(source, docs_target / name)
            copied += 1
    return copied


def main() -> None:
    args = parse_args()
    output = Path(args.output).resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    manifest = copy_manifest(output)
    skill_count, explicit_only = copy_skills(output)
    legal_doc_count = copy_legal_docs(output)

    summary = {
        "package": str(output),
        "manifest_name": manifest["name"],
        "skills": skill_count,
        "implicit_frontdoor": FRONTDOOR_SKILL,
        "explicit_only_skills": explicit_only,
        "legal_docs": legal_doc_count,
        "excluded_from_package": [
            "engine runtime",
            "local web app",
            "visual command center demo",
            "schemas",
            "examples",
            "tests",
            "long-form docs",
            "templates",
            "orchestrator scratch files",
        ],
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
