"""Local stdlib web app for The Autonomous CIO."""

from __future__ import annotations

import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
STATIC = Path(__file__).resolve().parent / "static"
sys.path.insert(0, str(ENGINE))

from decision_intelligence_engine import build_decision_packet, generate_dashboard_data, export_decision_package  # noqa: E402
from memory_store import init_memory_db, query_memory_db, save_review_to_db  # noqa: E402
from policy_engine import evaluate_policy, governance_readiness  # noqa: E402
from source_connectors import ingest_source_bundle  # noqa: E402
from office_export import build_board_pack  # noqa: E402
from eval_runner import run_evals  # noqa: E402
from decision_behavior import build_decision_dna  # noqa: E402
from enterprise_operating_intelligence import build_weekly_operating_autopilot  # noqa: E402
from governed_execution_intelligence import build_delegation_planner, build_enterprise_decision_ledger, detect_narrative_integrity, run_decision_simulation_arena  # noqa: E402
from learning_loop import learning_digest, record_feedback, record_outcome  # noqa: E402


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC), **kwargs)

    def do_GET(self):  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/memory":
            qs = parse_qs(parsed.query)
            db = qs.get("db", [str(ROOT / ".local-memory" / "autonomous_cio.db")])[0]
            query = qs.get("query", [""])[0]
            self._json(query_memory_db(db, query))
            return
        if parsed.path == "/api/evals":
            self._json(run_evals(str(ENGINE / "evals")))
            return
        if parsed.path == "/api/learning":
            qs = parse_qs(parsed.query)
            db = qs.get("db", [str(ROOT / ".local-memory" / "autonomous_cio.db")])[0]
            self._json(learning_digest(db))
            return
        if parsed.path == "/api/decision-dna":
            qs = parse_qs(parsed.query)
            db = qs.get("db", [str(ROOT / ".local-memory" / "autonomous_cio.db")])[0]
            self._json(build_decision_dna(db))
            return
        if parsed.path == "/api/weekly-operating-autopilot":
            qs = parse_qs(parsed.query)
            db = qs.get("db", [str(ROOT / ".local-memory" / "autonomous_cio.db")])[0]
            self._json(build_weekly_operating_autopilot(db))
            return
        if parsed.path == "/api/enterprise-ledger":
            qs = parse_qs(parsed.query)
            db = qs.get("db", [str(ROOT / ".local-memory" / "autonomous_cio.db")])[0]
            self._json(build_enterprise_decision_ledger(db))
            return
        return super().do_GET()

    def do_POST(self):  # noqa: N802
        try:
            payload = self._payload()
            if self.path == "/api/ingest":
                self._json(ingest_source_bundle(payload["input"], payload.get("db"), payload.get("profile", "auto")))
            elif self.path == "/api/decision-packet":
                self._json(build_decision_packet(payload.get("context", payload)))
            elif self.path == "/api/dashboard":
                self._json(generate_dashboard_data(payload.get("context", payload)))
            elif self.path == "/api/policy":
                self._json(evaluate_policy(payload.get("context", payload), payload.get("policy", "security")))
            elif self.path == "/api/governance":
                self._json(governance_readiness(payload.get("context", payload)))
            elif self.path == "/api/export":
                output_dir = payload.get("output_dir", str(ROOT / ".local-export" / "web"))
                self._json(export_decision_package(payload.get("context", payload), output_dir))
            elif self.path == "/api/board-pack":
                output_dir = payload.get("output_dir", str(ROOT / ".local-export" / "web-board-pack"))
                self._json(build_board_pack(payload.get("context", payload), output_dir, payload.get("format", "both")))
            elif self.path == "/api/save-review":
                db = payload.get("db", str(ROOT / ".local-memory" / "autonomous_cio.db"))
                init_memory_db(db)
                self._json(save_review_to_db(payload.get("context", payload), db))
            elif self.path == "/api/record-feedback":
                db = payload.get("db", str(ROOT / ".local-memory" / "autonomous_cio.db"))
                self._json(record_feedback(payload.get("feedback", payload), db))
            elif self.path == "/api/record-outcome":
                db = payload.get("db", str(ROOT / ".local-memory" / "autonomous_cio.db"))
                self._json(record_outcome(payload.get("outcome", payload), db))
            elif self.path == "/api/simulation-arena":
                self._json(run_decision_simulation_arena(payload.get("context", payload)))
            elif self.path == "/api/delegation-planner":
                self._json(build_delegation_planner(payload.get("context", payload)))
            elif self.path == "/api/narrative-integrity":
                self._json(detect_narrative_integrity(payload.get("context", payload)))
            else:
                self.send_error(404, "unknown API endpoint")
        except Exception as exc:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(exc)}).encode("utf-8"))

    def _payload(self):
        length = int(self.headers.get("Content-Length", "0"))
        data = self.rfile.read(length).decode("utf-8") if length else "{}"
        return json.loads(data or "{}")

    def _json(self, payload):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Local Autonomous CIO web app")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    STATIC.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Serving The Autonomous CIO at http://127.0.0.1:{args.port}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
