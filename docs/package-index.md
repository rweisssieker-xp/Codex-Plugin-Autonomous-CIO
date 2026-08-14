# Package Index

## Plugin Metadata

| Field | Value |
|---|---|
| Name | `the-autonomous-cio` |
| Display name | `The Autonomous CIO` |
| Version | `0.1.0` |
| Category | `Productivity` |
| Architecture | Skill-first, connector-neutral |

## Primary Entry Points

| Entry point | Use for |
|---|---|
| `autonomous-cio-orchestrator` | Broad executive requests and automatic skill-chain selection |
| `autonomous-cio-operating-review` | Full governed CIO Autopilot Review |
| `executive-decision-packet` | Board, crisis, AI approval, transformation and portfolio decisions |
| `engine/cli.py autopilot-review` | Reproducible local CIO Autopilot Review outputs |
| `engine/cli.py orchestrator-evals` | Request-type and skill-chain regression checks |
| `engine/cli.py usage-benchmark` | Local usage baseline for golden scenarios |
| `app/server.py` | Local stdlib CIO OS web app |
| `visual-command-center/index.html` | Static local dashboard demo |

## Package Contents

| Area | Count / Contents |
|---|---|
| Skills | 133 skills in `skills/` |
| Docs | 32 docs in `docs/` |
| Templates | 102 templates in `templates/` |
| Schemas | 162 JSON schemas in `engine/schemas/` |
| Engine | Local Python Decision Intelligence Engine |
| Web app | Local stdlib CIO OS app |
| Dashboard | Static Visual Command Center |
| Examples | Board prep, crisis, AI governance, transformation, industrial and connector-export examples |
| Runtime dependencies | Stdlib-only `requirements.txt` |

## Capability Groups

### Executive Decision Readiness

- CIO Autopilot Review
- Executive Decision Packet
- Decision Readiness Score
- Decision Debt Radar
- Decision Consequence Ledger
- Decision Backtest Simulator
- Decision SLA Monitor
- Executive Narrative Diff

### Evidence, Risk and Governance

- Evidence Graph
- Risk Chain Map
- Evidence Chain of Custody
- Evidence Expiry Monitor
- Risk Acceptance Docket
- Residual Risk Contract
- Control Debt Burndown
- Audit Finding Predictor
- Governance Drift Detector

### Board and Leadership Pressure Testing

- Board Pressure Simulation
- Boardroom Challenger AI
- Executive Decision Assurance
- Executive Decision Defense
- Executive Dissent Synthesizer
- Board Narrative Stress Test
- Executive Blind Spot Radar
- Commitment Integrity Score

### Governed Autonomy

- Governed Autonomy Layer
- Autonomy Readiness Score
- Autonomy Gate
- Autonomy Risk Budget
- Autonomy Stress Test
- Approval Boundary Mapper
- Human Control Contract
- CIO Replacement Surface
- CIO Work Autonomy Map

### Portfolio, Value and Operations

- Value Leakage Detector
- Budget Shock Absorber
- Vendor Leverage Index
- Vendor Exit Simulator
- Strategic Optionality Engine
- Enterprise Friction Map
- Operating Risk Heatmap
- Autonomous Roadmap Reprioritizer
- Benefits Realization Sentinel

### Architecture, Security, Data and AI

- Architecture Runway Guardian
- Cyber Business Impact Translator
- Data Trust Radar
- Data Sovereignty Radar
- Platform Rationalization Advisor
- AI Portfolio Governance
- AI governance approval readiness
- Security-to-business translation

### Local Runtime and Export Layer

- Skill Orchestration Runtime
- Connector Profile Catalog
- Connector Export Adapter
- Connector Profile Detection
- LLM Extraction Contract
- Explicit Memory Store Inspection
- Decision Export Package
- Office Export Package
- SQLite Executive Memory
- Policy Engine and Approval Gates
- Evidence Quality Engine
- Interactive Decision Twin
- Decision SLA Monitor
- Eval Benchmark Suite
- Orchestrator Chain Eval Suite
- Usage Benchmark Baseline
- Local CIO OS Web App
- User/Company Profile Layer
- Action Drafting Layer
- Adaptive CIO Learning Loop
- Recommendation Backtest
- Score Calibration Memory
- Source Reputation Memory
- Board Question Memory
- Decision DNA
- Executive Accountability Graph
- Organizational Friction Score
- Decision Collision Detector
- CIO Risk Appetite Twin
- Shadow Cost of Inaction
- Enterprise Decision Ledger
- Control-to-Decision Traceability
- Vendor Truth Index
- Narrative Integrity Detector
- Decision Simulation Arena
- CIO Weekly Operating Autopilot
- Executive Weekly Brief
- Guided Demo Flow
- Enterprise Operating Twin
- Autonomy Contract Engine
- Decision Chain of Custody
- Executive Attention Allocator
- Kill-Criteria Sentinel
- Benefit Realization Memory
- Strategic Drift Early Warning
- Vendor Promise Backtester
- Decision Latency Cost Meter
- Evidence Decay Forecast
- Synthetic Executive Committee
- Control Debt Ledger
- Operating Rhythm Autopilot
- Enterprise Contradiction Memory
- CIO Replacement Surface Map
- LLM Extraction Pipeline
- Runtime Schema Validation
- Memory Approval Queue
- Skill Suite Map
- Hardening Eval Report
- Local Release Package Builder
- Marketplace Submission Pack Builder
- Strategic Contradiction Radar
- Autonomous Delegation Planner
- Local file and directory ingestion
- Optional Teams, Slack, Outlook Email, Gmail/Google Workspace and Calendar adapter profiles
- Optional Jira, Azure DevOps, ServiceNow, CMDB, cloud cost, security, observability, ERP/SAP, Confluence and Google Drive adapter profiles

## Autopilot Review Views

| View | Command | Best for |
|---|---|---|
| `compact` | `python engine/cli.py autopilot-review --input engine/examples/autopilot_review.json --format markdown --view compact` | Daily CIO triage |
| `board` | `python engine/cli.py autopilot-review --input engine/examples/autopilot_review.json --format markdown --view board` | Leadership and board packs |
| `full` | `python engine/cli.py autopilot-review --input engine/examples/autopilot_review.json --format markdown --view full` | Audit-friendly detail |

## Review Notes

- No authenticated live connector access in version 0.1.
- No production MCP server in version 0.1; an optional MCP-compatible adapter is included for local development.
- No hosted app UI in version 0.1; the app is local-only and served from `127.0.0.1`.
- No external-service action execution; action commands produce drafts only.
- No automatic persistent memory; SQLite memory writes require explicit local DB paths.
- Works only on user-provided context and local files.
