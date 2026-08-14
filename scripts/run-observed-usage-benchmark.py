#!/usr/bin/env python3
"""Run local observed usage scenarios and write benchmark artifacts.

This measures actual local command execution time, exit status and deterministic
input/output token estimates. It does not claim Codex-host token usage.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / ".local-artifacts" / "observed-usage"
JSONL = OUT_DIR / "observed-usage.jsonl"
PLUGIN_EVAL_JSONL = OUT_DIR / "plugin-eval-observed-usage.jsonl"
SUMMARY = OUT_DIR / "observed-usage-summary.json"
STATIC_ACTIVE_TOKEN_BASELINE = 2616

SCENARIOS = [
    ("decision_packet_board", ["engine/cli.py", "build-decision-packet", "--input", "engine/examples/board_prep.json"]),
    ("autopilot_review", ["engine/cli.py", "autopilot-review", "--input", "engine/examples/autopilot_review.json"]),
    ("usp_suite", ["engine/cli.py", "unfair-advantage-usp-suite", "--input", "engine/examples/industrial_operating_review.json"]),
    ("orchestrator_evals", ["engine/cli.py", "orchestrator-evals", "--eval-dir", "engine/evals"]),
    ("usage_benchmark", ["engine/cli.py", "usage-benchmark", "--eval-dir", "engine/evals"]),
]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    with JSONL.open("w", encoding="utf-8") as handle:
        plugin_eval_handle = PLUGIN_EVAL_JSONL.open("w", encoding="utf-8")
        try:
            for name, args in SCENARIOS:
                record = run_scenario(name, args)
                records.append(record)
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
                plugin_eval_handle.write(json.dumps(to_plugin_eval_usage(record), ensure_ascii=False) + "\n")
        finally:
            plugin_eval_handle.close()
    summary = {
        "artifact": "Observed Local Usage Benchmark",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scenario_count": len(records),
        "passed_count": sum(1 for item in records if item["exit_code"] == 0),
        "failed_count": sum(1 for item in records if item["exit_code"] != 0),
        "average_duration_ms": round(sum(item["duration_ms"] for item in records) / len(records), 2),
        "average_estimated_output_tokens": round(sum(item["estimated_output_tokens"] for item in records) / len(records), 2),
        "jsonl": str(JSONL),
        "plugin_eval_observed_usage_jsonl": str(PLUGIN_EVAL_JSONL),
        "scope": "Observed local CLI runtime and deterministic token estimates; not Codex-host token usage.",
        "codex_usage_next_step": "Attach Codex or Responses API usage logs when available and compare them against this local baseline.",
        "records": records,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def run_scenario(name: str, args: list[str]) -> dict:
    started = time.perf_counter()
    proc = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True)
    duration_ms = round((time.perf_counter() - started) * 1000, 2)
    stdout = proc.stdout or ""
    stderr = proc.stderr or ""
    return {
        "scenario": name,
        "command": " ".join([sys.executable, *args]),
        "exit_code": proc.returncode,
        "duration_ms": duration_ms,
        "estimated_output_tokens": estimate_tokens(stdout),
        "estimated_input_tokens": STATIC_ACTIVE_TOKEN_BASELINE,
        "estimated_total_tokens": STATIC_ACTIVE_TOKEN_BASELINE + estimate_tokens(stdout),
        "estimated_error_tokens": estimate_tokens(stderr),
        "stdout_bytes": len(stdout.encode("utf-8")),
        "stderr_bytes": len(stderr.encode("utf-8")),
        "observed_usage_type": "local_cli_runtime",
        "codex_host_usage_supplied": False,
    }


def to_plugin_eval_usage(record: dict) -> dict:
    return {
        "id": f"local_{record['scenario']}",
        "usage": {
            "input_tokens": record["estimated_input_tokens"],
            "output_tokens": record["estimated_output_tokens"],
            "total_tokens": record["estimated_total_tokens"],
        },
        "metadata": {
            "scenario": record["scenario"],
            "observed_usage_type": "local_cli_harness_estimate",
            "codex_host_usage_supplied": False,
            "note": "Plugin-eval compatible local baseline. Replace with real Codex or Responses usage logs for production measurement.",
        },
    }


def estimate_tokens(text: str) -> int:
    return max(0, round(len(text) / 4))


if __name__ == "__main__":
    main()
