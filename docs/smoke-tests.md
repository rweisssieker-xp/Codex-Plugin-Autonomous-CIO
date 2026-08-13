# The Autonomous CIO Smoke Tests

Use these prompts after installing or updating the plugin. Each test should produce the standard output contract, clearly separate evidence from assumptions, and avoid claiming live connector access.

## Local Engine Smoke Tests

Run:

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
python engine/cli.py detect-connector-profile --input engine/examples/slack_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/slack_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/outlook_email_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/outlook_email_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/gmail_workspace_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/gmail_workspace_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/jira_delivery_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/jira_delivery_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/azure_devops_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/azure_devops_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/servicenow_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/servicenow_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/cmdb_assets_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/cmdb_assets_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/cloud_cost_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/cloud_cost_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/security_findings_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/security_findings_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/observability_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/observability_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/erp_sap_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/erp_sap_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/confluence_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/confluence_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/google_drive_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/google_drive_export.csv
python engine/cli.py llm-extraction-contract --input engine/examples/industrial_operating_review.json
python engine/cli.py orchestrate --input engine/examples/industrial_operating_review.json
python engine/cli.py propose-memory-updates --input engine/examples/industrial_operating_review.json
python engine/cli.py inspect-memory --memory engine/examples/memory.json
python engine/cli.py export-package --input engine/examples/industrial_operating_review.json --output-dir .local-export/industrial-review
python engine/cli.py export-office-package --input engine/examples/industrial_operating_review.json --output-dir .local-export/office-review
python engine/cli.py init-memory-db --db .local-memory/autonomous_cio.db
python engine/cli.py migrate-memory-json --memory engine/examples/memory.json --db .local-memory/autonomous_cio.db
python engine/cli.py save-review --input engine/examples/board_prep.json --db .local-memory/autonomous_cio.db
python engine/cli.py query-memory --db .local-memory/autonomous_cio.db --query ERP
python engine/cli.py memory-aging --db .local-memory/autonomous_cio.db
python engine/cli.py sla-monitor --db .local-memory/autonomous_cio.db
python engine/cli.py sla-digest --db .local-memory/autonomous_cio.db
python engine/cli.py discover-sources --path engine/examples
python engine/cli.py pull-signals --input engine/examples/topdesk_export.csv
python engine/cli.py ingest-bundle --input engine/examples --db .local-memory/autonomous_cio.db
python engine/cli.py decision-twin --input engine/examples/industrial_operating_review.json --scenario defer
python engine/cli.py score-evidence --input engine/examples/industrial_operating_review.json
python engine/cli.py evaluate-policy --input engine/examples/ai_governance.json --policy ai-governance
python engine/cli.py approval-gates --input engine/examples/industrial_operating_review.json
python engine/cli.py governance-readiness --input engine/examples/industrial_operating_review.json
python engine/cli.py draft-actions --input engine/examples/board_prep.json --type email
python engine/cli.py build-board-pack --input engine/examples/board_prep.json --output-dir .local-export/board-pack --format both
python engine/cli.py run-evals --eval-dir engine/evals
python engine/cli.py eval-report --eval-dir engine/evals
python engine/cli.py init-profile --profile .local-memory/company-profile.json
python engine/cli.py apply-profile --input engine/examples/board_prep.json --profile .local-memory/company-profile.json
python engine/cli.py record-feedback --input engine/examples/learning_feedback.json --db .local-memory/autonomous_cio.db
python engine/cli.py record-outcome --input engine/examples/learning_outcome.json --db .local-memory/autonomous_cio.db
python engine/cli.py skill-chain-feedback --input engine/examples/skill_chain_feedback.json --db .local-memory/autonomous_cio.db
python engine/cli.py board-question-memory --input engine/examples/board_questions.json --db .local-memory/autonomous_cio.db
python engine/cli.py calibrate-scores --db .local-memory/autonomous_cio.db
python engine/cli.py learn-patterns --db .local-memory/autonomous_cio.db
python engine/cli.py source-reputation --db .local-memory/autonomous_cio.db
python engine/cli.py recommendation-backtest --db .local-memory/autonomous_cio.db
python engine/cli.py learning-digest --db .local-memory/autonomous_cio.db
python engine/cli.py decision-dna --db .local-memory/autonomous_cio.db
python engine/cli.py accountability-graph --input engine/examples/board_prep.json --db .local-memory/autonomous_cio.db
python engine/cli.py friction-score --input engine/examples/board_prep.json --db .local-memory/autonomous_cio.db
python engine/cli.py decision-collisions --input engine/examples/industrial_operating_review.json --db .local-memory/autonomous_cio.db
python engine/cli.py risk-appetite-twin --db .local-memory/autonomous_cio.db
python engine/cli.py board-memory --db .local-memory/autonomous_cio.db
python engine/cli.py shadow-cost-inaction --input engine/examples/board_prep.json
python engine/cli.py enterprise-decision-ledger --db .local-memory/autonomous_cio.db
python engine/cli.py control-decision-trace --input engine/examples/ai_governance.json --db .local-memory/autonomous_cio.db
python engine/cli.py vendor-truth-index --input engine/examples/industrial_operating_review.json --db .local-memory/autonomous_cio.db
python engine/cli.py narrative-integrity --input engine/examples/board_prep.json
python engine/cli.py simulation-arena --input engine/examples/board_prep.json
python engine/cli.py weekly-operating-autopilot --db .local-memory/autonomous_cio.db
python engine/cli.py strategic-contradictions --input engine/examples/industrial_operating_review.json --db .local-memory/autonomous_cio.db
python engine/cli.py delegation-planner --input engine/examples/board_prep.json
python engine/cli.py import-context --input engine/examples/sample_import.csv
python engine/cli.py build-from-file --input engine/examples/sample_import.csv
python engine/cli.py dashboard-from-file --input engine/examples/sample_import.csv
python engine/cli.py ingest-directory --input engine/examples
python engine/cli.py refresh-dashboard --input engine/examples/board_prep.json --output visual-command-center/demo-data.json
python engine/cli.py evaluate
python -m unittest discover engine/tests
python app/server.py --port 8765
```

Expected:

- valid JSON output for each CLI command
- autopilot review includes decision packet, attention budget, action ledger, autonomy gate, memory update and CIO replacement surface
- autopilot review Markdown supports `full`, `compact` and `board` views
- scores bounded from 0 to 100
- scorecard includes decision readiness, board risk, evidence confidence, value leakage and autonomy readiness
- evidence graph, risk chain, decision debt, memory comparison and board challenge signals are present in relevant outputs
- semantic model includes entities, claims, dependencies and decisions
- scenario simulation includes approve now, defer and approve with conditions
- audit trail includes score drivers and recommendation drivers
- dashboard data includes scores, graph metrics, scenario simulation and audit trail
- operating rhythm includes daily, weekly, monthly, board-prep, crisis and AI approval routines
- benchmark includes raw input quality, missing evidence rate and before/after comparison
- connector ingestion normalizes signals and builds a decision packet
- risk graph includes centrality and propagation paths
- trend delta includes score deltas, new risks and resolved risks when a prior packet is provided
- review export returns copy-ready Markdown or JSON content
- privacy scan returns findings, redacted context and data classification
- action governance returns risk level, approver role and automation eligibility
- assurance output includes all 15 advanced assurance features
- decision-defense output includes all 12 defensive executive USP features
- connector-profiles returns profile contracts without claiming live access
- detect-connector-profile identifies likely profile from local export fields and values
- adapt-connector-export converts local connector exports into normalized signals and a decision packet
- optional connector exports for Slack, Outlook Email and Gmail/Google Workspace are detected and adapted without live-access claims
- CIO-priority exports for Jira, Azure DevOps, ServiceNow, CMDB, cloud cost, security findings, observability, ERP/SAP, Confluence and Google Drive are detected and adapted without live-access claims
- llm-extraction-contract returns required fields, classification rules and sample extraction
- orchestrate returns selected skill chain plus integrated decision packet, autopilot review, action governance and memory proposal
- propose-memory-updates returns decision memory, assumption register, evidence graph, risk chain and action ledger proposals without writing
- inspect-memory returns local store counts, stale assumptions and open actions
- export-package writes board, audit, steering, action-ledger and decision-log artifacts to the requested local directory
- export-office-package writes local `.docx` and `.pptx` artifacts to the requested local directory
- SQLite memory commands initialize, migrate, save, query, age and monitor only the explicitly requested local DB path
- source discovery, pull-signals and ingest-bundle preserve local source provenance and avoid live-access claims
- decision-twin returns score deltas, risk-chain deltas, missing-evidence changes and reversibility
- score-evidence returns evidence quality, freshness, source weight and conflict scores
- policy, approval-gates and governance-readiness return decision-support gates without final legal, security or regulatory determinations
- draft-actions returns draft payloads with `executed: false`
- build-board-pack writes requested local artifacts only under the requested output directory
- eval runner reports 50 local cases and no guardrail failures
- local web app responds at `http://127.0.0.1:8765` when started
- adaptive learning commands record explicit local feedback and outcomes, produce calibration and backtest hints, and state that no external model is trained
- all 15 adaptive CIO OS USP modules return valid JSON, preserve guardrails and stay decision-support only
- import context converts CSV, JSON, TXT or Markdown into input context
- build-from-file converts local files directly into Executive Decision Packets
- dashboard-from-file and refresh-dashboard generate Visual Command Center JSON from real engine output
- ingest-directory converts local files into connector-shaped signals and an integrated decision packet
- evaluation passes all golden examples
- facts, assumptions, hypotheses and missing evidence in each output
- guardrails saying no live access, no automatic persistence and no executed actions
- static dashboard available at `visual-command-center/index.html`

## Autonomous CIO Operating Review

Prompt:

```text
Use autonomous-cio-operating-review. Run the governed CIO autopilot review:
ERP remains targeted for 30 September, testing has not started, vendor milestones slipped twice, privileged access remediation is incomplete, change-control audit evidence is missing, cloud spend is 18% above forecast, and Board update is due in 48 hours.
```

Expected:

- decision readiness
- enterprise status
- risk chain
- attention budget
- action ledger
- autonomy gate
- memory update

## Decision Intelligence Loop Demo

Prompt:

```text
Use autonomous-cio-orchestrator. Build an Executive Decision Packet from this mixed context.

Meeting notes:
- ERP steering committee says go-live is still targeted for 30 September.
- Testing has not started because the test environment is late.
- Vendor missed two integration milestones.
- The same two architects support ERP, IAM remediation and CRM rollout.
- Sponsor wants to avoid another board escalation.

Risk register:
- R-17: ERP test readiness, Red, owner PMO, mitigation not approved.
- R-22: Privileged access remediation dependency, Amber, owner CISO office.
- R-31: Change-control audit evidence incomplete, Amber, owner IT controls.

Budget update:
- ERP contingency reserve is 82% consumed.
- Cloud migration spend is 18% above forecast.
- No additional architecture capacity is funded.

Board need:
- Decide whether to approve go-live, defer go-live, or approve only with conditions.
```

Expected:

- Request Type: Board Prep or Portfolio Decision
- Selected Skill Chain using the Decision Intelligence Loop
- Why This Chain
- Decision Needed
- Facts vs Assumptions
- Risk Chain
- Options
- Board Challenge Questions
- Recommended Action
- Missing Evidence
- Draft Next Steps: Next 24h / 7d / 30d

## autonomous-cio-orchestrator

Prompt:

```text
Use autonomous-cio-orchestrator. Choose the right workflow and produce an integrated executive artifact:
ERP is red, privileged access gaps remain open, audit evidence is incomplete, two architects are overloaded, cloud spend is 18% above forecast, and leadership needs a board update in 48 hours.
```

Expected:

- request type
- selected skill chain
- why this chain
- integrated executive summary
- risks and dependencies
- decisions needed
- next 24h / 7d / 30d actions

## Board Prep Proof

Prompt:

```text
Use autonomous-cio-orchestrator. Build an Executive Decision Packet for a board technology update.
Context: ERP is Red, CRM is Amber, IAM remediation is Green but architect constrained. Cloud spend is 18% above forecast. Q3 change-control evidence is incomplete. Leadership wants to state that delivery is broadly under control.
```

Expected:

- evidence classification
- weak signal ranking
- contradiction detection
- board pressure simulation
- decision packet output

## Crisis Command Proof

Prompt:

```text
Use autonomous-cio-orchestrator. Build an Executive Decision Packet for this crisis.
Billing integration outage affects key customers. Root cause unknown. Security impact unclear. Operations has no ETA. Sales is escalating and asks for customer messaging within two hours.
```

Expected:

- crisis request type
- known facts and unknowns
- risk propagation
- command roles
- 1h / 4h / 24h draft next steps

## AI Governance Approval Proof

Prompt:

```text
Use autonomous-cio-orchestrator. Build an Executive Decision Packet for this AI approval.
Support wants to summarize customer tickets with an LLM using historical incident text, customer names and resolution notes. No data owner has approved it. The business case claims 20% productivity improvement, but no baseline exists.
```

Expected:

- AI approval request type
- value hypothesis and missing baseline
- data risk and owner gap
- governance-gap prediction
- approve with conditions or defer recommendation

## Transformation Value Leakage Proof

Prompt:

```text
Use autonomous-cio-orchestrator. Build an Executive Decision Packet for transformation value leakage.
Cloud migration is 18% above forecast. ERP reserve is nearly consumed. Three automation workstreams report activity but no adoption metrics. Vendor workshops increased, but cycle time and incident volume have not improved.
```

Expected:

- transformation value request type
- value leakage detection
- decision debt mining
- benefit gates
- recovery actions and missing evidence

## enterprise-briefing

Prompt:

```text
Use enterprise-briefing. Create an executive briefing for the CIO from this context:
- ERP modernization is 6 weeks behind.
- Security found critical identity gaps in privileged access.
- Finance reports cloud spend 18% above forecast.
- PMO says two key architects are overloaded.
- Audit preparation for Q3 lacks evidence for change controls.
```

Expected:

- top management priorities
- decisions needed
- early warnings
- next 24h / 7d / 30d actions

## project-portfolio-intelligence

Prompt:

```text
Use project-portfolio-intelligence. Assess this portfolio:
Project A: CRM rollout, amber, vendor delay, go-live in 5 weeks.
Project B: ERP upgrade, red, budget overrun, missing test environment.
Project C: IAM remediation, green, dependent on architecture team.
Budget reserve is nearly consumed and the same two experts support all projects.
```

Expected:

- Red / Amber / Green assessment
- cross-project dependencies
- resource and budget risks
- prioritization recommendation

## process-operations-intelligence

Prompt:

```text
Use process-operations-intelligence. Analyze these service signals:
Incident volume is stable, but major incidents repeat for billing integrations.
Mean time to resolve increased from 9h to 16h.
Most delays happen between support and application teams.
Known-error documentation is incomplete.
```

Expected:

- bottlenecks
- cause clusters
- service-quality risks
- improvement actions

## architecture-data-security-intelligence

Prompt:

```text
Use architecture-data-security-intelligence. Review this technology context:
Three customer-data systems duplicate master data.
Two legacy integrations are undocumented.
Privileged access is manually reviewed.
Data ownership is unclear for reporting tables.
The core order platform has no tested failover procedure.
```

Expected:

- critical assets and dependencies
- data governance risks
- security and resilience risks
- modernization actions

## enterprise-command-center

Prompt:

```text
Use enterprise-command-center. Build an enterprise situation report from this context:
Portfolio: ERP red, CRM amber, IAM green but architect constrained.
Operations: recurring billing incidents and rising MTTR.
Finance: cloud spend 18% over forecast.
Compliance: Q3 audit evidence for change controls incomplete.
Security: privileged access review gaps.
Architecture: duplicate customer master data and undocumented integrations.
```

Expected:

- domain Green / Amber / Red view
- top 10 management priorities
- top 5 escalations
- top 5 decisions needed
- command-center action plan

## strategy-drift-intelligence

Prompt:

```text
Use strategy-drift-intelligence. Compare this stated strategy with current execution:
Strategy: reduce complexity, improve resilience, consolidate customer data.
Execution: three new point solutions approved, duplicate customer systems remain, resilience testing postponed, cloud spend rising.
```

Expected:

- drift findings
- root causes
- decision and governance corrections

## enterprise-pre-mortem

Prompt:

```text
Use enterprise-pre-mortem. Assume the ERP transformation failed 9 months from now. Explain the most likely failure paths from this context:
budget reserve is low, test environment is late, architects are overloaded, vendor milestones slipped twice, steering decisions are delayed.
```

Expected:

- failure scenarios
- leading indicators
- preventive actions

## crisis-command-mode

Prompt:

```text
Use crisis-command-mode. Create an executive crisis command view:
Billing integration outage affects key customers. Root cause unknown. Security impact unclear. Operations has no ETA. Sales is escalating.
```

Expected:

- situation
- command structure
- decisions needed
- communications and next actions

## ai-governance-intelligence

Prompt:

```text
Use ai-governance-intelligence. Assess this AI use case:
Support wants to summarize customer tickets with an LLM using historical incident text, customer names and resolution notes. No data owner has approved it yet.
```

Expected:

- value/risk assessment
- data and compliance concerns
- controls and approval path

## executive-truth-layer

Prompt:

```text
Use executive-truth-layer. Classify this update:
The program is broadly on track, but testing has not started, the test environment is late, the budget reserve is nearly consumed, and vendor milestones slipped twice. Leadership expects no go-live impact.
```

Expected:

- facts
- assumptions
- unsupported claims
- contradictions
- missing evidence

## management-attention-optimizer

Prompt:

```text
Use management-attention-optimizer. Triage these signals:
Critical privileged access gaps, low-severity UI backlog, duplicate customer data systems, delayed ERP testing, minor office printer issue, cloud spend 18% above forecast.
```

Expected:

- act now / escalate / decide / delegate / monitor / ignore routing
- evidence and confidence

## risk-chain-intelligence

Prompt:

```text
Use risk-chain-intelligence. Map cascading risks:
ERP test environment is delayed. Same architects support IAM remediation. Privileged access gaps remain open. Q3 audit evidence for change controls is incomplete.
```

Expected:

- propagation paths
- amplifiers
- trigger points
- containment actions

## executive-q-and-a-simulator

Prompt:

```text
Use executive-q-and-a-simulator. Prepare tough Board, CFO, CISO and Audit questions for this proposal:
Approve ERP go-live despite delayed testing, budget reserve depletion and incomplete change-control evidence.
```

Expected:

- likely questions
- weak answer risks
- missing evidence
- pre-meeting actions
