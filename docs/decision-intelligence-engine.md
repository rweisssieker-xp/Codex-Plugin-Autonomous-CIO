# Decision Intelligence Engine

The Decision Intelligence Engine is a local Python runtime for The Autonomous CIO. It turns provided JSON, CSV, Markdown and text context into reproducible Executive Decision Packets, scorecards, evidence graphs, risk-chain maps, memory comparisons and Visual Command Center data.

Version 0.1 remains connector-neutral. In plugin usage, Codex itself is the LLM layer for semantic extraction and reasoning. The local Python engine does not call external services on its own, does not persist memory automatically and does not execute actions.

## Local Interfaces

```text
python engine/cli.py build-decision-packet --input engine/examples/board_prep.json
python engine/cli.py autopilot-review --input engine/examples/autopilot_review.json
python engine/cli.py autopilot-review --input engine/examples --memory engine/examples/memory.json
python engine/cli.py autopilot-review --input engine/examples/autopilot_review.json --format markdown
python engine/cli.py autopilot-review --input engine/examples/autopilot_review.json --format markdown --view compact
python engine/cli.py autopilot-review --input engine/examples/autopilot_review.json --format markdown --view board
python engine/cli.py score --input engine/examples/board_prep.json
python engine/cli.py map-risk-chain --input engine/examples/crisis.json
python engine/cli.py extract-evidence-graph --input engine/examples/ai_governance.json
python engine/cli.py compare-memory --input engine/examples/transformation_value.json --memory engine/examples/memory.json
python engine/cli.py semantic-model --input engine/examples/board_prep.json
python engine/cli.py simulate-scenarios --input engine/examples/board_prep.json
python engine/cli.py audit-trail --input engine/examples/board_prep.json
python engine/cli.py dashboard-data --input engine/examples/board_prep.json
python engine/cli.py operating-rhythm --input engine/examples/board_prep.json
python engine/cli.py benchmark --input engine/examples/board_prep.json
python engine/cli.py ingest-signals --input engine/examples/connector_signals.json
python engine/cli.py risk-graph --input engine/examples/board_prep.json
python engine/cli.py trend-delta --input engine/examples/board_prep_with_prior.json
python engine/cli.py export-review --input engine/examples/board_prep.json --format markdown
python engine/cli.py privacy-scan --input engine/examples/ai_governance.json
python engine/cli.py action-governance --input engine/examples/board_prep.json
python engine/cli.py assurance --input engine/examples/board_prep.json
python engine/cli.py assurance --input engine/examples/board_prep_llm_extracted.json
python engine/cli.py decision-defense --input engine/examples/board_prep.json
python engine/cli.py connector-profiles
python engine/cli.py detect-connector-profile --input engine/examples/industrial_file_drop.csv
python engine/cli.py adapt-connector-export --input engine/examples/topdesk_export.csv
python engine/cli.py llm-extraction-contract --input engine/examples/industrial_operating_review.json
python engine/cli.py orchestrate --input engine/examples/industrial_operating_review.json
python engine/cli.py propose-memory-updates --input engine/examples/industrial_operating_review.json
python engine/cli.py inspect-memory --memory engine/examples/memory.json
python engine/cli.py export-package --input engine/examples/industrial_operating_review.json --output-dir .local-export/industrial-review
python engine/cli.py export-office-package --input engine/examples/industrial_operating_review.json --output-dir .local-export/office-review
python engine/cli.py import-context --input engine/examples/sample_import.csv
python engine/cli.py build-from-file --input engine/examples/sample_import.csv
python engine/cli.py dashboard-from-file --input engine/examples/sample_import.csv
python engine/cli.py ingest-directory --input engine/examples
python engine/cli.py refresh-dashboard --input engine/examples/board_prep.json --output visual-command-center/demo-data.json
python engine/cli.py save-memory --input engine/examples/board_prep.json --memory .local-memory/demo-memory.json
python engine/cli.py evaluate
```

## Optional MCP Adapter

`engine/mcp_server.py` exposes MCP-compatible wrapper functions when the MCP Python package is installed. Without that optional dependency, use the CLI or import `engine/decision_intelligence_engine.py` directly.

Planned tool names:

- `build_decision_packet`
- `build_autopilot_review`
- `build_autopilot_review_from_file`
- `score_decision_readiness`
- `map_risk_chain`
- `extract_evidence_graph`
- `compare_with_memory`
- `extract_semantic_model`
- `simulate_scenarios`
- `build_audit_trail`
- `generate_dashboard_data`
- `build_decision_packet_from_file`
- `generate_dashboard_data_from_file`
- `refresh_dashboard_data`
- `ingest_source_directory`
- `generate_operating_rhythm`
- `benchmark_decision_quality`
- `ingest_connector_signals`
- `analyze_risk_graph`
- `compare_packet_trend`
- `export_review_artifact`
- `export_autopilot_review_artifact`
- `scan_privacy`
- `action_governance`
- `build_decision_assurance`
- `build_executive_decision_defense`
- `import_context_file`
- `save_packet_to_memory`
- `inspect_memory_store`
- `connector_profile_catalog`
- `detect_connector_profile`
- `adapt_connector_export`
- `build_llm_extraction_contract`
- `run_skill_orchestrator`
- `propose_memory_updates`
- `export_decision_package`
- `export_office_package`
- `evaluate_golden_examples`

## Scorecard

## Autopilot Review Views

The `autopilot-review` command supports three Markdown views:

- `--view compact`: daily CIO triage with status, readiness, top attention, guarded autonomy, missing evidence and next actions.
- `--view board`: board-pack view with narrative, decision request, recommended motion, challenge questions, consequences, dissent, evidence gaps and human-control boundary.
- `--view full`: complete audit-friendly review with the full disruptive USP layer. This remains the default for backward compatibility.

Scores are directional decision-support signals from `0` to `100`.

- `decision_readiness`: evidence strength, option clarity, owner clarity, dependency visibility, reversibility and missing-evidence penalty.
- `board_risk`: impact, urgency, contradiction severity, financial/security/audit exposure and confidence penalty.
- `evidence_confidence`: direct facts, inferred claims, source count, missing evidence and contradiction count.
- `value_leakage`: spend pressure, weak outcome evidence, duplicated work, adoption gap and owner gap.
- `autonomy_readiness`: action clarity, approval requirement, high-risk domain exposure, reversibility and human-control need.

## Ten Product USPs

- CIO Autopilot Review
- Decision Readiness Score
- Evidence Graph
- Risk Chain Map
- Decision Debt Radar
- Board Pressure Simulation
- Value Leakage Detector
- Executive Memory Comparison
- Autonomy Readiness Score
- Governed Autonomy Layer
- Visual Command Center
- CIO Replacement Surface

## Core Intelligence Layer

- Semantic extraction identifies enterprise entities, claims, dependencies and open decisions from the provided context.
- Graph metrics summarize node count, edge count, critical dependency, blast-radius domains and systemic risk level.
- Adaptive board personas generate role-specific pressure questions for CEO, CFO, CISO, Audit, Regulator and Customer lenses.
- Scenario simulation compares approve now, defer and approve with conditions by risk delta, value delta, cost of waiting, reversibility and confidence sensitivity.
- Audit trail records score drivers, score explanations, recommendation drivers and the source scope.
- Operating rhythm generation converts a decision packet into daily, weekly, monthly, board-prep, crisis and AI approval routines.
- Decision quality benchmarking compares raw context quality against structured decision-packet readiness.
- Risk graph analysis computes local centrality and propagation paths from signals to dependencies and business impacts.
- Trend delta compares current scores and weak signals against a provided prior packet.
- Review export creates a copy-ready Markdown or JSON artifact for board, audit or steering review.
- Privacy scan flags likely secrets, email addresses and phone-like identifiers, then returns a redacted context view.
- Action governance assigns risk level, autonomy level, reversibility, required approval, automation eligibility and cannot-automate reasons to draft actions.
- Local memory store can be explicitly updated with `save-memory`; no memory is saved automatically.
- Golden evaluation checks deterministic examples against expected request types and score ranges.

## Executive Decision Assurance

`python engine/cli.py assurance --input engine/examples/board_prep.json` returns the full advanced assurance layer:

- optional LLM extraction hook with heuristic fallback
- entity resolution
- causal decision graph
- counterfactual simulation
- decision twin
- board question coverage score
- narrative risk detector
- decision anti-pattern library
- red team / blue team mode
- executive attention budget
- decision latency tracker
- value-at-risk estimate
- governance control map
- meeting-to-decision diff
- decision packet quality grade

`engine/examples/board_prep_llm_extracted.json` shows the Codex-plugin path: the host LLM populates `llm_extraction`, and the engine returns `llm_extraction_layer.mode = provided_llm_output`. Standalone CLI usage without that field returns `heuristic_fallback`.

## Executive Decision Defense

`python engine/cli.py decision-defense --input engine/examples/board_prep.json` returns the defensive executive layer:

- Decision Liability Shield
- Executive Blind Spot Radar
- Commitment Integrity Score
- Board Narrative Stress Test
- Autonomous Decision Memory Diff
- Value Realization Firewall
- Risk-to-Cash Translator
- Decision SLA Monitor
- Control Evidence Readiness
- Executive Attention Allocator
- Scenario Kill-Switch
- CIO Operating System Loop

## Governed CIO Autopilot Review

`python engine/cli.py autopilot-review --input engine/examples/autopilot_review.json` returns the full governed CIO operating review:

- Executive Decision Packet
- Decision Readiness
- Enterprise Status
- Evidence Graph
- Risk Chain
- Attention Budget
- Board Questions
- Decision Twin
- Action Ledger
- Autonomy Gate
- Memory Update and optional Memory Diff
- CIO Replacement Surface
- Privacy Scan
- Executive Decision Assurance
- Operating Rhythm

Use `--memory <path>` to compare against prior decision memory. Use `--format markdown` for a board-readable export. Use a directory path to ingest local `.json`, `.csv`, `.txt` and `.md` files into one review.

## Connector-Ready Signal Contract

`engine/schemas/connector-signal.schema.json` defines the future signal shape for Teams, Slack, Outlook Email, Gmail/Google Workspace, Outlook Calendar, SharePoint, Google Drive, Confluence, Jira, Azure DevOps, GitHub, ServiceNow, TOPdesk, CMDB/assets, cloud cost, security findings, observability, ERP/SAP, finance CSV and manual input. Version 0.1 ships the contract, demo examples and a real local directory/file ingestion path; it does not authenticate to or read from external SaaS systems.

`python engine/cli.py connector-profiles` returns profile contracts for Outlook Calendar, Outlook Email, Teams messages, Slack messages, Gmail/Google Workspace, SharePoint documents, Google Drive documents, Confluence knowledge, GitHub delivery, Jira delivery, Azure DevOps delivery, TOPdesk service, ServiceNow service, CMDB assets, cloud cost, security findings, observability monitoring, ERP/SAP and industrial file drops. These profiles state expected fields, signal types, safe mode and decision use; they do not claim live connector access.

`python engine/cli.py detect-connector-profile --input engine/examples/industrial_file_drop.csv` detects the likely signal profile from a local CSV/JSON/TXT/Markdown export.

`python engine/cli.py adapt-connector-export --input engine/examples/topdesk_export.csv` converts a real local export into normalized connector-shaped signals and builds an Executive Decision Packet from them. Use `--profile <name>` to override auto-detection.

`python engine/cli.py ingest-signals --input engine/examples/connector_signals.json` normalizes connector-shaped demo signals and produces a decision packet from them.

`python engine/cli.py ingest-directory --input engine/examples` reads local `.json`, `.csv`, `.txt` and `.md` files, normalizes them into connector-shaped signals and produces a decision packet. This converts the former connector mock into a real local source adapter while preserving the no-live-access boundary.

`python engine/cli.py build-from-file --input engine/examples/sample_import.csv` imports a local file and immediately builds an Executive Decision Packet.

## Orchestration, Extraction and Memory

`python engine/cli.py orchestrate --input engine/examples/industrial_operating_review.json` detects request type and domains, selects the skill chain and returns an integrated bundle with Executive Decision Packet, Autopilot Review, Action Governance, Memory Update Proposal and LLM Extraction Contract.

`python engine/cli.py llm-extraction-contract --input engine/examples/industrial_operating_review.json` returns the Codex-host extraction standard: required output fields, classification rules and a sample extraction from the provided context.

`python engine/cli.py propose-memory-updates --input engine/examples/industrial_operating_review.json` returns suggested decision memory, assumption register, evidence graph, risk chain map and action ledger entries without writing them.

`python engine/cli.py inspect-memory --memory engine/examples/memory.json` inspects a local memory JSON file for counts, stale assumptions and open or overdue actions.

## Export Package

`python engine/cli.py export-package --input engine/examples/industrial_operating_review.json --output-dir .local-export/industrial-review` writes a local artifact package:

- `executive_decision_packet.json`
- `autonomous_cio_operating_review.json`
- `board_pack.md`
- `audit_evidence_pack.md`
- `steering_committee_deck_outline.md`
- `action_ledger.csv`
- `decision_log.json`

`python engine/cli.py export-office-package --input engine/examples/industrial_operating_review.json --output-dir .local-export/office-review` writes local Office-compatible artifacts:

- `board_decision_pack.docx`
- `steering_committee_deck.pptx`

## Output Invariant

Every engine output includes:

- `facts`
- `assumptions`
- `hypotheses`
- `missing_evidence`
- `confidence`
- `recommended_action`
- `guardrails`

## Visual Command Center

Open `visual-command-center/index.html` locally to inspect the dashboard. It reads `visual-command-center/demo-data.json` when browser security allows local fetch, and falls back to embedded demo data otherwise. Users can load an Engine JSON output, including orchestration outputs or connector profile catalogs, reset to demo data or export the current dashboard JSON.

`python engine/cli.py refresh-dashboard --input engine/examples/board_prep.json --output visual-command-center/demo-data.json` regenerates the dashboard data from the engine. This makes the dashboard data a reproducible local output instead of a hand-maintained mock.

The dashboard shows:

- Decision Readiness Score
- Evidence Confidence Heatmap
- Risk Chain Map
- Decision Debt Radar
- Board Risk Meter
- Value Leakage Panel
- Operating Rhythm
- Decision Quality Benchmark
- Trend Delta
- Decision Packet Quality Grade
- Decision Packet Preview
- Memory Update Proposal
- Connector Profile View
- Export Readiness
- Value-at-Risk Panel
- Board Question Coverage
- Decision Anti-Patterns
- Executive Attention Budget

## Safety Boundary

The engine is an analysis aid. It does not replace expert legal, regulatory, HR, security or financial review. It should make missing evidence and confidence visible whenever it recommends action.
