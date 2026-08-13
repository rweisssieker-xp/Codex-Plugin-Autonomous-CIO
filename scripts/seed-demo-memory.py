"""Seed a local Autonomous CIO demo memory database."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from learning_loop import board_question_memory, record_feedback, record_outcome, record_skill_chain_feedback  # noqa: E402
from memory_store import init_memory_db, save_review_to_db  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed local demo memory for The Autonomous CIO")
    parser.add_argument("--db", default=str(ROOT / ".local-memory" / "autonomous_cio_demo.db"), help="SQLite DB path")
    args = parser.parse_args()
    db_path = args.db
    init_memory_db(db_path)
    for name in ("industrial_operating_review.json", "board_prep.json", "ai_governance.json", "transformation_value.json"):
        save_review_to_db(_load("examples", name), db_path)
    record_feedback(_load("examples", "learning_feedback.json"), db_path)
    record_outcome(_load("examples", "learning_outcome.json"), db_path)
    record_skill_chain_feedback(_load("examples", "skill_chain_feedback.json"), db_path)
    board_question_memory(_load("examples", "board_questions.json"), db_path)
    print(json.dumps({"artifact": "Demo Memory Seeded", "db_path": db_path, "reviews_seeded": 4, "guardrails": ["Local demo data only.", "No live system access.", "No external actions executed."]}, indent=2))
    return 0


def _load(folder: str, name: str):
    return json.loads((ENGINE / folder / name).read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
