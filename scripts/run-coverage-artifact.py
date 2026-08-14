#!/usr/bin/env python3
"""Generate a stdlib-only coverage artifact for local Python engine tests."""

from __future__ import annotations

import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
OUT_DIR = ROOT / ".local-artifacts" / "coverage"
TRACE_DIR = OUT_DIR / "trace"
COVERAGE_XML = OUT_DIR / "coverage.xml"
SUMMARY_JSON = OUT_DIR / "coverage-summary.json"


def main() -> None:
    if TRACE_DIR.exists():
        for child in TRACE_DIR.glob("*"):
            if child.is_file():
                child.unlink()
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        "-m",
        "trace",
        "--count",
        "--coverdir",
        str(TRACE_DIR),
        str(ROOT / "engine" / "tests" / "test_engine.py"),
    ]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    files = collect_cover_files()
    summary = build_summary(files, proc.returncode)
    write_cobertura(summary)
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if proc.returncode:
        print(proc.stdout, file=sys.stdout)
        print(proc.stderr, file=sys.stderr)
        raise SystemExit(proc.returncode)


def collect_cover_files() -> list[Path]:
    return sorted(path for path in TRACE_DIR.rglob("*.cover") if path.is_file())


def build_summary(files: list[Path], exit_code: int) -> dict:
    packages = []
    total_lines = 0
    total_hits = 0
    for cover in files:
        module_name = cover.stem
        if not (ENGINE / f"{module_name}.py").is_file() and not module_name.startswith("test_"):
            continue
        lines = cover.read_text(encoding="utf-8", errors="ignore").splitlines()
        executable = 0
        hit = 0
        for line in lines:
            stripped = line[:10].strip()
            if stripped == ">>>>>>":
                executable += 1
            else:
                try:
                    count = int(stripped.rstrip(":"))
                except ValueError:
                    continue
                executable += 1
                if count > 0:
                    hit += 1
        if executable:
            total_lines += executable
            total_hits += hit
            packages.append({"file": str(cover.relative_to(TRACE_DIR)), "covered_lines": hit, "executable_lines": executable, "line_rate": round(hit / executable, 4)})
    line_rate = round(total_hits / total_lines, 4) if total_lines else 0
    return {
        "artifact": "Local Coverage Artifact",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "test_exit_code": exit_code,
        "coverage_xml": str(COVERAGE_XML),
        "trace_dir": str(TRACE_DIR),
        "covered_lines": total_hits,
        "executable_lines": total_lines,
        "line_rate": line_rate,
        "files": packages,
        "scope": "Stdlib trace coverage for local engine unit tests.",
    }


def write_cobertura(summary: dict) -> None:
    coverage = ET.Element(
        "coverage",
        {
            "line-rate": str(summary["line_rate"]),
            "branch-rate": "0",
            "version": "stdlib-trace",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
    sources = ET.SubElement(coverage, "sources")
    ET.SubElement(sources, "source").text = str(ROOT)
    packages = ET.SubElement(coverage, "packages")
    package = ET.SubElement(packages, "package", {"name": "engine", "line-rate": str(summary["line_rate"]), "branch-rate": "0"})
    classes = ET.SubElement(package, "classes")
    for item in summary["files"]:
        cls = ET.SubElement(classes, "class", {"name": item["file"], "filename": item["file"], "line-rate": str(item["line_rate"]), "branch-rate": "0"})
        ET.SubElement(cls, "methods")
        ET.SubElement(cls, "lines")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(coverage).write(COVERAGE_XML, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
