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
from product_hardening import build_llm_extraction_pipeline, build_release_package, list_memory_update_queue, queue_memory_updates, review_memory_update, run_hardening_evals, skill_suite_map  # noqa: E402
from source_connectors import ingest_source_bundle  # noqa: E402
from office_export import build_board_pack  # noqa: E402
from eval_runner import run_evals  # noqa: E402
from decision_behavior import build_decision_dna  # noqa: E402
from enterprise_operating_intelligence import build_executive_weekly_brief, build_weekly_operating_autopilot  # noqa: E402
from executive_autonomy_innovation import allocate_executive_attention, backtest_vendor_promises, build_autonomy_contract_engine, build_benefit_realization_memory, build_control_debt_ledger, build_decision_chain_of_custody, build_enterprise_contradiction_memory, build_enterprise_operating_twin, build_kill_criteria_sentinel, build_operating_rhythm_autopilot_v2, detect_strategic_drift_early_warning, forecast_evidence_decay, map_cio_replacement_surface, measure_decision_latency_cost, simulate_synthetic_executive_committee  # noqa: E402
from governed_execution_intelligence import build_delegation_planner, build_enterprise_decision_ledger, detect_narrative_integrity, run_decision_simulation_arena  # noqa: E402
from learning_loop import learning_digest, record_feedback, record_outcome  # noqa: E402
from learning_loop import board_question_memory, record_skill_chain_feedback  # noqa: E402


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
        if parsed.path == "/api/hardening-evals":
            self._json(run_hardening_evals(str(ENGINE / "evals")))
            return
        if parsed.path == "/api/skill-suites":
            self._json(skill_suite_map())
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
        if parsed.path == "/api/executive-weekly-brief":
            qs = parse_qs(parsed.query)
            db = qs.get("db", [str(ROOT / ".local-memory" / "autonomous_cio.db")])[0]
            fmt = qs.get("format", ["markdown"])[0]
            self._json(build_executive_weekly_brief(db, None, fmt))
            return
        if parsed.path == "/api/enterprise-ledger":
            qs = parse_qs(parsed.query)
            db = qs.get("db", [str(ROOT / ".local-memory" / "autonomous_cio.db")])[0]
            self._json(build_enterprise_decision_ledger(db))
            return
        if parsed.path == "/api/benefit-realization-memory":
            qs = parse_qs(parsed.query)
            db = qs.get("db", [str(ROOT / ".local-memory" / "autonomous_cio.db")])[0]
            self._json(build_benefit_realization_memory(db))
            return
        if parsed.path == "/api/operating-rhythm-autopilot-v2":
            qs = parse_qs(parsed.query)
            db = qs.get("db", [str(ROOT / ".local-memory" / "autonomous_cio.db")])[0]
            self._json(build_operating_rhythm_autopilot_v2(db))
            return
        if parsed.path == "/api/memory-update-queue":
            qs = parse_qs(parsed.query)
            db = qs.get("db", [str(ROOT / ".local-memory" / "autonomous_cio.db")])[0]
            status = qs.get("status", ["Pending"])[0]
            self._json(list_memory_update_queue(db, status))
            return
        return super().do_GET()

    def do_POST(self):  # noqa: N802
        try:
            payload = self._payload()
            if self.path == "/api/ingest":
                self._json(ingest_source_bundle(payload["input"], payload.get("db"), payload.get("profile", "auto")))
            elif self.path == "/api/decision-packet":
                self._json(build_decision_packet(payload.get("context", payload)))
            elif self.path == "/api/llm-extraction-pipeline":
                self._json(build_llm_extraction_pipeline(payload.get("context", payload)))
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
            elif self.path == "/api/queue-memory-updates":
                db = payload.get("db", str(ROOT / ".local-memory" / "autonomous_cio.db"))
                self._json(queue_memory_updates(payload.get("context", payload), db))
            elif self.path == "/api/review-memory-update":
                db = payload.get("db", str(ROOT / ".local-memory" / "autonomous_cio.db"))
                self._json(review_memory_update(db, int(payload["id"]), payload.get("decision", "Approved"), payload.get("reviewer", "CIO office")))
            elif self.path == "/api/seed-demo-memory":
                db = payload.get("db", str(ROOT / ".local-memory" / "autonomous_cio_demo.db"))
                init_memory_db(db)
                for name in ("industrial_operating_review.json", "board_prep.json", "ai_governance.json", "transformation_value.json"):
                    save_review_to_db(_load_example(name), db)
                record_feedback(_load_example("learning_feedback.json"), db)
                record_outcome(_load_example("learning_outcome.json"), db)
                record_skill_chain_feedback(_load_example("skill_chain_feedback.json"), db)
                board_question_memory(_load_example("board_questions.json"), db)
                self._json({"artifact": "Demo Memory Seeded", "db_path": db, "reviews_seeded": 4, "facts": ["Seeded local demo memory."], "assumptions": [], "hypotheses": ["Demo data is synthetic and local."], "missing_evidence": [], "confidence": "High", "recommended_action": {"recommendation": "Generate the Executive Weekly Brief from the seeded demo memory.", "owner": "CIO office", "timebox": "Now"}, "guardrails": ["Uses local demo data only.", "Does not claim live system access.", "Does not execute external actions."]})
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
            elif self.path == "/api/enterprise-operating-twin":
                self._json(build_enterprise_operating_twin(payload.get("context", payload), payload.get("db")))
            elif self.path == "/api/autonomy-contract":
                self._json(build_autonomy_contract_engine(payload.get("context", payload), payload.get("db")))
            elif self.path == "/api/decision-chain-custody":
                self._json(build_decision_chain_of_custody(payload.get("context", payload), payload.get("db")))
            elif self.path == "/api/executive-attention":
                self._json(allocate_executive_attention(payload.get("context", payload), payload.get("db")))
            elif self.path == "/api/kill-criteria-sentinel":
                self._json(build_kill_criteria_sentinel(payload.get("context", payload), payload.get("db")))
            elif self.path == "/api/strategic-drift-warning":
                self._json(detect_strategic_drift_early_warning(payload.get("context", payload), payload.get("db")))
            elif self.path == "/api/vendor-promise-backtest":
                self._json(backtest_vendor_promises(payload.get("context", payload), payload.get("db")))
            elif self.path == "/api/decision-latency-cost":
                self._json(measure_decision_latency_cost(payload.get("context", payload), payload.get("db")))
            elif self.path == "/api/evidence-decay-forecast":
                self._json(forecast_evidence_decay(payload.get("context", payload), payload.get("db")))
            elif self.path == "/api/synthetic-executive-committee":
                self._json(simulate_synthetic_executive_committee(payload.get("context", payload), payload.get("db")))
            elif self.path == "/api/control-debt-ledger":
                self._json(build_control_debt_ledger(payload.get("context", payload), payload.get("db")))
            elif self.path == "/api/enterprise-contradiction-memory":
                self._json(build_enterprise_contradiction_memory(payload.get("context", payload), payload.get("db")))
            elif self.path == "/api/cio-replacement-surface-map":
                self._json(map_cio_replacement_surface(payload.get("context", payload), payload.get("db")))
            elif self.path == "/api/export-weekly-brief":
                db = payload.get("db", str(ROOT / ".local-memory" / "autonomous_cio.db"))
                output_dir = payload.get("output_dir", str(ROOT / ".local-export" / "weekly-brief"))
                self._json(build_executive_weekly_brief(db, output_dir, payload.get("format", "both")))
            elif self.path == "/api/build-release-package":
                output_dir = payload.get("output_dir", str(ROOT / ".local-export" / "release"))
                self._json(build_release_package(output_dir))
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


def _load_example(name):
    return json.loads((ENGINE / "examples" / name).read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
