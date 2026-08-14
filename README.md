# The Autonomous CIO

The Autonomous CIO is a local Codex plugin for AI-native executive decision intelligence. It turns user-provided enterprise context into governed CIO decision support: board-ready decision packets, CIO Autopilot Reviews, challenge questions, risk chains, action drafts, evidence gaps, ownership boundaries and reusable executive memory.

It is a skill-first MVP that works with provided context, local files and local exports. Version 0.1 does not claim authenticated live connector access, automatic persistence or external action execution.

## Positioning

**The Autonomous CIO makes enterprise decisions board-ready before leadership enters the room.**

It is designed for:

- CIOs, CISOs, COOs and CFO-facing technology leaders
- Enterprise architects and transformation leads
- PMO, risk, compliance and audit teams
- Executive operations and board-prep teams
- Technology leaders preparing steering, crisis, investment, vendor or AI governance decisions

## What It Produces

- CIO Autopilot Reviews
- Executive Decision Packets
- Board and steering briefings
- Risk-chain maps and early-warning views
- Evidence graphs and missing-evidence registers
- Action ledgers and escalation drafts
- Approval boundaries and human-control contracts
- Decision memory proposals
- Local dashboard and export packages

## Why It Is Different

The Autonomous CIO is not a dashboard, meeting summarizer or generic CIO chatbot.

| Traditional tool | What it usually does | What The Autonomous CIO does |
|---|---|---|
| Dashboard | Shows status | Turns status into decisions, escalations, safeguards and next actions |
| Meeting summarizer | Preserves discussion | Extracts decisions, debt, assumptions, risks, owners and follow-ups |
| Generic chatbot | Answers questions | Applies a CIO operating model across truth, risk, options, actions and memory |
| Risk register | Lists risks | Maps cascading risk chains across domains |
| Board prep document | Describes the situation | Pressure-tests the decision before leadership commits |

## Quick Start

Run a full local engine example:

```text
python engine/cli.py autopilot-review --input engine/examples/autopilot_review.json
```

Generate a compact daily CIO triage view:

```text
python engine/cli.py autopilot-review --input engine/examples/autopilot_review.json --format markdown --view compact
```

Generate a board-pack view:

```text
python engine/cli.py autopilot-review --input engine/examples/autopilot_review.json --format markdown --view board
```

Build an Executive Decision Packet:

```text
python engine/cli.py build-decision-packet --input engine/examples/board_prep.json
```

Run the 15-module unfair-advantage USP suite:

```text
python engine/cli.py unfair-advantage-usp-suite --input engine/examples/industrial_operating_review.json
```

Run the test suite:

```text
python -m unittest engine.tests.test_engine
```

Open the static local dashboard:

```text
visual-command-center/index.html
```

Start the local CIO OS web app:

```text
python app/server.py --port 8765
```

Seed a high-signal demo memory and export the Monday CIO brief:

```text
python scripts/seed-demo-memory.py --db .local-memory/autonomous_cio_demo.db
python engine/cli.py executive-weekly-brief --db .local-memory/autonomous_cio_demo.db --output-dir .local-export/weekly-brief --format both
```

## Repository Contents

| Path | Purpose |
|---|---|
| `.codex-plugin/plugin.json` | Codex plugin manifest |
| `skills/` | 133 connector-neutral Codex skills |
| `docs/` | Marketplace, architecture, proof, smoke-test and operating-model documentation |
| `templates/` | 102 reusable executive and governance templates |
| `engine/` | Local Python Decision Intelligence Engine |
| `engine/schemas/` | 163 JSON schemas for engine artifacts |
| `engine/examples/` | Demo inputs for board prep, crisis, AI governance and transformation scenarios |
| `app/` | Stdlib local CIO OS web app |
| `visual-command-center/` | Static local dashboard demo |
| `scripts/` | Smoke-test helpers |

## Flagship Workflow

The CIO Autopilot Review follows this operating loop:

```text
Signals -> Truth -> Decision -> Action Draft -> Memory -> Operating Rhythm
```

Markdown output views:

- `compact`: daily CIO triage with status, readiness, top attention, guarded autonomy and next actions.
- `board`: leadership pack with narrative, decision request, challenge questions, consequences, dissent, evidence gaps and human-control boundary.
- `full`: audit-friendly detail view with the complete disruptive USP layer.

## Core USPs

1. Decision Readiness Score: shows whether an executive decision is ready for Board or steering approval, or whether it is being pushed without enough evidence.
2. Evidence Graph: makes visible which claims are supported by facts and which are assumptions, hypotheses, narratives or missing evidence.
3. Risk Chain Map: shows how risks cascade across architecture, security, finance, vendors, operations and governance.
4. Decision Debt Radar: finds deferred, ownerless or implicit decisions before they block delivery.
5. Board Pressure Simulation: generates CFO, CISO, Audit, CEO, regulator and customer challenge questions before the meeting.
6. Value Leakage Detector: identifies transformation, vendor, cloud and project activity that consumes resources without enough measurable value.
7. Executive Memory Comparison: compares new updates against prior decisions, assumptions and open actions.
8. Autonomy Readiness Score: assesses whether an action can be automated or must stay under human approval because of risk, reversibility or control needs.
9. Governed Autonomy Layer: prepares actions, escalations and decision logs while keeping human approval, auditability and no uncontrolled execution.
10. CIO Autopilot Review: creates a complete operating review with decision packet, risk chain, evidence graph, attention budget, action ledger, memory update and autonomy gate.
11. Visual Command Center: turns decision readiness, evidence gaps, risk chains, decision debt and board pressure into a scannable local cockpit.
12. CIO Work Autonomy Map: shows which CIO tasks are automated, drafted, decision-supported or human-only.
13. Board Objection Simulator: pressure-tests decisions against CEO, CFO, CISO, Audit, regulator, customer and Board objections.
14. Decision Debt Ledger: converts delayed, implicit and ownerless decisions into clearance actions.
15. Truth Gap Detector: detects gaps between status narratives, facts, assumptions, contradictions and missing evidence.
16. Executive Time Saved Estimator: estimates which CIO, PMO, risk and board-prep work has already been prepared.
17. CIO Shadow Agenda: creates the real leadership agenda from weak signals, value risk, decision debt and truth gaps.
18. Autonomous Steering Pack Factory: turns mixed context into a decision-ready steering or board pack outline.
19. Risk Chain Forecast: forecasts likely next escalation if owners, evidence or decisions remain unresolved.
20. Strategic Drift Detector: finds initiatives drifting from strategy, value, architecture, security or adoption.
21. Human Control Contract: makes governed autonomy explicit and keeps high-risk execution under human approval.
22. Decision SLA Enforcer: assigns decision deadlines and escalation thresholds before decision debt becomes operating risk.
23. Vendor Exit Simulator: frames renegotiation, scope reduction, fallback and exit options for vendor dependency.
24. Regulatory Shock Simulator: builds a minimum response pack for sudden audit, regulator, customer or compliance scrutiny.
25. Cyber Business Impact Translator: turns cyber and control signals into business impact and executive choices.
26. Talent Criticality Radar: detects key-person, scarce-skill and owner-capacity risks.
27. Capital Allocation Copilot: converts budget, spend, forecast and value signals into funding trade-offs.
28. Post Decision Learning Loop: captures assumptions, outcomes, lessons and memory updates after decisions.
29. CIO OS Maturity Index: scores whether CIO work is ad hoc, a decision toolkit, governed copilot or operating system.
30. Stakeholder Alignment Matrix: prepares persona-specific alignment risks, messages and evidence needs.
31. Exception Waiver Factory: drafts governed waivers with scope, expiry, owner and compensating controls.
32. Policy as Code Readiness: identifies governance rules that could become codified controls later.
33. Benefits Realization Sentinel: detects value promises without owner, baseline, target or measurement date.
34. Operating Rhythm Autopilot: recommends cadence, rituals and prepared inputs from decision pressure.
35. Autonomous Escalation Drafts: prepares escalation messages and owner requests without sending them.
36. Executive Decision Backlog: turns scattered decision debt into prioritized backlog items with routing.
37. Enterprise Control Tower: shows decision readiness, board risk, evidence, truth gaps and decision debt as operating panels.
38. M&A Carve-out Readiness: prepares integration, separation and carve-out readiness questions.
39. Data Trust Radar: checks owner, metric definition, lineage, freshness and privacy controls for decision data.
40. Architecture Runway Guardian: protects architecture capacity, integration readiness and technical-debt guardrails.
41. Executive Narrative Generator: creates stakeholder-specific executive narratives without hiding uncertainty.
42. Autonomous Due Diligence Questions: generates targeted diligence questions with evidence needs.
43. Resilience Continuity Planner: drafts minimum continuity plans and first 24h actions.
44. Customer Trust Impact Radar: translates service, billing, outage and recovery signals into trust exposure.
45. AI Portfolio Governance: turns AI experiments into governed portfolio decisions.
46. Cost of Delay Calculator: estimates qualitative cost of not deciding.
47. Executive Commitment Tracker: tracks draft and prior commitments, owners, status and next checks.
48. Decision Rights Mapper: clarifies approver, accountable owner, contributors and approval mode.
49. OKR Strategy Fit Checker: checks whether work advances objectives, key results and value.
50. Risk Acceptance Docket: drafts owned, time-boxed risk acceptance items with evidence needs.
51. Service Health Sentinel: translates incidents, SLAs, outage and recovery signals into health posture.
52. Knowledge Continuity Planner: reduces key-person and critical-knowledge concentration risk.
53. Dependency Breakpoint Analyzer: identifies where enterprise dependencies can break execution.
54. Transformation Kill Criteria: defines stop, change and continue triggers for weak-value initiatives.
55. Vendor Negotiation Brief: prepares negotiation asks and fallback positions from vendor risk.
56. Compliance Evidence Pack: drafts audit/control evidence-package structure.
57. Board Decision Simulator: simulates board reactions to approval options.
58. Operating Risk Heatmap: turns delivery, finance, security, customer and capacity signals into a heatmap.
59. Autonomous Roadmap Reprioritizer: recommends what to promote, protect, pause or defer.
60. Audit Finding Predictor: predicts likely audit findings before evidence gaps become findings.
61. Platform Rationalization Advisor: recommends consolidation, retirement, renegotiation or stabilization.
62. Data Sovereignty Radar: detects privacy, residency, retention and cross-border transfer readiness gaps.
63. Operating Model Debt Ledger: captures unclear ownership, overloaded governance and decision bottlenecks.
64. Strategic Option Portfolio: compares options by value posture, risk posture and next evidence.
65. Executive Decision War Room: prepares roles, first 60 minutes and exit criteria for high-pressure decisions.
66. Decision Liability Shield: shows which approvals would be indefensible without evidence, owner, controls or escalation.
67. Executive Blind Spot Radar: detects hidden contradictions between positive narratives and risk, budget, control or dependency signals.
68. Commitment Integrity Score: checks whether dates, scope, budget, capacity, controls, owner, recovery and reversibility support the commitment.
69. Board Narrative Stress Test: tests planned Board wording against facts, missing evidence and CFO/CISO/Audit objections.
70. Autonomous Decision Memory Diff: compares current context with prior assumptions, debt, claims and overdue actions.
71. Value Realization Firewall: blocks expansion of weak-value initiatives until baseline, owner, adoption metric and value gate exist.
72. Risk-to-Cash Translator: turns technical, security, audit and delivery risks into directional business exposure.
73. Decision SLA Monitor: assigns decision deadlines before slow decisions become hidden operating risk.
74. Control Evidence Readiness: checks whether audit, security, finance, architecture or AI controls are evidence-ready.
75. Executive Attention Allocator: routes signals into act now, escalate, decide, delegate, monitor or ignore.
76. Scenario Kill-Switch: defines stop, pause, defer or re-scope criteria before commitments are made.
77. CIO Operating System Loop: closes the loop from signals to truth, risk chain, decision, action draft, memory and operating rhythm.
78. Industrial CIO Operating System: turns ERP, MES, QMS, PLM, OT, production, audit, vendor and customer-channel signals into one CIO operating view.
79. IT/OT Production Risk Command: maps shopfloor, integration, security, service and supplier risks into production-continuity decision gates.
80. QMS Audit Evidence Readiness: checks whether IT-enabled changes, validation, access, incidents and controls are evidence-ready for audit or customer scrutiny.
81. Connector Profile Catalog: defines safe signal contracts for Outlook, Teams, Slack, Gmail/Google Workspace, SharePoint, GitHub, TOPdesk and industrial file drops without live access.
82. Skill Orchestration Runtime: detects request type and domains, selects the skill chain and returns one integrated decision-support bundle.
83. LLM Extraction Contract: standardizes how Codex-host reasoning should classify facts, assumptions, weak signals, contradictions and evidence gaps.
84. Explicit Memory Store Inspection: reviews saved local memory for stale assumptions, open decisions and draft actions without automatic persistence.
85. Decision Export Package: writes local board, audit, steering, action-ledger and decision-log artifacts from one input.
86. Connector Export Adapter: converts real local CSV/JSON/TXT/Markdown exports from service, delivery, document, meeting and industrial systems into normalized decision signals.
87. Connector Profile Detection: detects likely connector profile from local export field names and content before adaptation.
88. Office Export Package: generates local `.docx` and `.pptx` board/steering artifacts without external libraries or cloud services.
89. Evidence Chain of Custody: makes executive evidence traceable by claim, source owner, verification status and missing chain links.
90. Decision Rollback Planner: defines rollback triggers and actions for approvals made under uncertainty.
91. Autonomy Risk Budget: keeps autonomous preparation bounded by risk, missing evidence and human-only controls.
92. Approval Boundary Mapper: makes action, approval and human-only boundaries explicit before governed execution is considered.
93. Evidence Expiry Monitor: flags stale-risk evidence and required refresh triggers before board, audit or approval use.
94. Residual Risk Contract: turns residual-risk acceptance into explicit owner, conditions, expiry and rollback terms.
95. Autonomy Stress Test: pressure-tests governed autonomy against stale evidence, missing approvals and human-control bypass risk.
96. Decision Consequence Ledger: maps first- and second-order consequences, watch metrics and reversal signals for each option.
97. Enterprise Friction Map: exposes decision, evidence, capacity, vendor and value friction slowing the enterprise operating system.
98. Strategic Optionality Engine: identifies options that preserve future choices under uncertainty instead of forcing premature commitment.
99. Control Debt Burndown: converts audit, access, privacy and control gaps into a prioritized evidence burndown plan.
100. Executive Dissent Synthesizer: turns CFO, CISO, COO, Audit, architecture and customer objections into stronger decision conditions.
101. Decision Backtest Simulator: compares current decisions against prior memory patterns and synthetic lessons before approval.
102. Governance Drift Detector: detects recurring exceptions, bypass pressure and unclear accountability before controls erode.
103. Budget Shock Absorber: prepares protect, freeze, renegotiate and stage-gate moves when budget pressure hits.
104. Vendor Leverage Index: scores vendor leverage from dependency, milestone, evidence and fallback signals.
105. Executive Narrative Diff: reconciles changed executive narratives before board, audit or customer communication.
106. Optional Connector Router: routes Teams, Slack, email, calendar and document exports to the right adapter profile.
107. Teams Decision Signal Adapter: converts Teams messages or exports into CIO decision, risk, owner and evidence signals.
108. Slack Decision Signal Adapter: converts Slack exports into blockers, incidents, owner language and decision fragments.
109. Email Executive Signal Adapter: converts Outlook or Gmail threads into approvals, commitments, evidence and escalation signals.
110. Calendar Operating Rhythm Adapter: converts calendar exports into decision pressure, governance cadence and prep gaps.
111. Delivery Work Management Adapter: converts Jira, Azure DevOps and GitHub exports into portfolio and roadmap signals.
112. ITSM Service Management Adapter: converts ServiceNow, TOPdesk and ITSM exports into service health and change-risk signals.
113. Cloud FinOps Adapter: converts Azure, AWS, GCP and cloud cost exports into budget and value-leakage signals.
114. Security Risk Adapter: converts Defender, Sentinel, Splunk, Qualys or security exports into business risk and control debt.
115. Enterprise Systems Adapter: converts ERP, SAP, CMDB and asset exports into process, dependency and modernization signals.
116. Knowledge Document Adapter: converts Confluence, Google Drive, SharePoint and document exports into evidence and memory signals.
117. Live Connector Layer Contract: standardizes export-first and optional authorized connector sources behind one SignalSource model.
118. SQLite Executive Memory: stores local decisions, assumptions, evidence, risk chains, actions, reviews and audit events in an explicit local DB.
119. Local CIO OS Web App: provides browser-based ingestion, packet building, policy checks, memory browsing, exports and eval access.
120. Governance Policy Engine: evaluates security, audit, AI governance, change-control, privacy and vendor-risk readiness.
121. Action Drafting Layer: drafts Outlook, Teams, TOPdesk, GitHub and board-pack payloads without sending or creating anything externally.
122. Eval Benchmark Suite: runs local regression cases for request type, score ranges, evidence separation and guardrails.
123. Industry Profile Layer: supports local risk tolerance, board style, systems, roles, KPIs and language preferences.
124. Interactive Decision Twin: simulates approve, defer, stop, re-scope, fund and rollback scenarios with score and risk deltas.
125. Evidence Quality Engine: scores evidence by source type, freshness, directness, completeness and conflicts.
126. Board Pack Export Builder: creates local board, audit, steering, docx and pptx artifacts from one context.
127. Decision SLA Monitor: detects overdue decisions, stale assumptions, stale evidence and aging draft actions from SQLite memory.
128. Multi-Input Bundle Ingestion: converts local folders of notes, exports, CSVs and JSON into one provenance-preserving source bundle.
129. User/Company Profile Layer: applies local non-secret preferences for risk, board style, systems, roles and output language.
130. Policy Approval Gates: maps accountable owner, approver, contributor, informed and human-only gates before execution.
131. Local Source Discovery: inventories local JSON, CSV, TXT and Markdown sources for safe ingestion.
132. Adaptive CIO Learning Loop: records explicit feedback, outcomes, board questions and skill-chain ratings in local memory.
133. Recommendation Backtest: compares recommendations against later outcomes and feedback.
134. Score Calibration Memory: derives local score-adjustment hints from outcome accuracy and accepted feedback.
135. Source Reputation Memory: scores local evidence sources by signal count and contradiction pressure.
136. Board Question Memory: stores real steering and board questions for sharper future pressure simulation.
137. Decision DNA: classifies local decision behavior such as slow, optimistic, risk-averse, vendor-dependent, evidence-driven and board-reactive.
138. Executive Accountability Graph: maps accountable owner, approver, contributor and informed relationships from context and memory.
139. Organizational Friction Score: scores friction from evidence gaps, owner gaps, budget pressure, vendor dependency and decision latency.
140. Decision Collision Detector: detects contradictory goals, decisions and constraints across context and local memory.
141. CIO Risk Appetite Twin: derives a local risk appetite profile from accepted feedback, decisions and outcomes.
142. Shadow Cost of Inaction: makes the cost of not deciding visible across audit, security, delivery, finance and customer domains.
143. Enterprise Decision Ledger: builds a chronological, audit-friendly ledger from decisions, assumptions, evidence, reviews and outcomes.
144. Control-to-Decision Traceability: links decisions to security, audit, AI governance, privacy and change-control evidence.
145. Vendor Truth Index: scores vendor signal quality against delays, milestones, weak evidence and dependency pressure.
146. Narrative Integrity Detector: detects positive executive narratives that conflict with facts, budget, testing or evidence gaps.
147. Decision Simulation Arena: compares approve, defer, re-scope, stop, fund and rollback scenarios side by side.
148. CIO Weekly Operating Autopilot: generates weekly operating focus from memory, stale assumptions, overdue actions and board risks.
149. Strategic Contradiction Radar: detects strategy/execution contradictions across roadmap, budget, security, architecture and work.
150. Autonomous Delegation Planner: drafts owner-specific delegation requests with evidence needs, due dates and escalation paths.
151. Executive Weekly Brief: exports the Monday CIO operating brief as Markdown and HTML from local decision memory.
152. Guided Demo Flow: seeds demo memory, builds packets, saves memory, records outcomes, generates the weekly brief and exports proof artifacts from one local UI.
153. Enterprise Operating Twin: builds a local CIO operating model across systems, owners, vendors, controls, risks and memory counts.
154. Autonomy Contract Engine: turns decision context into explicit suggest-only, draft-allowed, approval-required and human-only clauses.
155. Decision Chain of Custody: fingerprints the packet and traces facts, assumptions and missing evidence for audit-grade review.
156. Executive Attention Allocator: converts board risk, value leakage, decision debt, vendor pressure and control debt into a CIO attention budget.
157. Kill-Criteria Sentinel: makes stop, pause and re-scope triggers visible before transformation work drifts into default continuation.
158. Benefit Realization Memory: compares local decisions with recorded outcomes to expose unproven benefits.
159. Strategic Drift Early Warning: detects divergence between strategy, budget, security, architecture, vendors and operating execution.
160. Vendor Promise Backtester: challenges vendor commitments against weak signals, missing evidence and local outcome memory.
161. Decision Latency Cost Meter: scores the cost of delayed decisions and proposes a decision SLA.
162. Evidence Decay Forecast: predicts which evidence will become stale before board, audit or approval review.
163. Synthetic Executive Committee: simulates CEO, CFO, CISO, Audit Chair, COO and Board Director challenge pressure.
164. Control Debt Ledger: inventories security, audit, privacy, change and vendor control debt tied to the current decision.
165. Operating Rhythm Autopilot: turns local memory into weekly, monthly, quarterly and annual CIO operating cadences.
166. Enterprise Contradiction Memory: exposes recurring contradictions such as on-track narratives against testing, budget or control gaps.
167. CIO Replacement Surface Map: separates CIO work the plugin can prepare from approval-gated and human-only accountability.
168. LLM Extraction Pipeline: accepts host-LLM structured extraction or local fallback, validates the extraction and builds a schema-checked packet.
169. Runtime Schema Validation: validates local JSON outputs against engine schemas before release or review.
170. Memory Approval Queue: stages proposed memory updates for explicit approve/reject review before persistence.
171. Skill Suite Map: groups the skill catalog into product-frontdoor suites for board, crisis, AI governance, transformation, vendor and autonomy workflows.
172. Hardening Eval Report: adds release-blocking checks over local eval coverage, high-risk cases and guardrail regressions.
173. Local Release Package Builder: creates local release notes, manifest and zip package without external publication.

## AI Signature Mechanism

The signature mechanism is the Decision Intelligence Loop:

```text
Signals -> Truth -> Risk Chain -> Options -> Actions -> Memory
```

1. Signals: extract weak and strong signals from provided updates, notes, exports and reports.
2. Truth: classify facts, inferences, assumptions, hypotheses, political framing and missing evidence.
3. Risk Chain: connect cascading dependencies across enterprise domains.
4. Options: compare choices by impact, urgency, confidence, reversibility, value and readiness.
5. Actions: prepare draft tasks, escalations, approvals, decision logs and communication language.
6. Memory: structure decisions, assumptions, risks and commitments that should carry forward.

The signature output is the Executive Decision Packet, supported by the dedicated `executive-decision-packet` skill. The flagship operating workflow is the Autonomous CIO Operating Review, supported by `autonomous-cio-operating-review`, which adds enterprise status, attention budget, action ledger, autonomy gate, memory update, CIO replacement surface, CIO work autonomy map, board objections, decision debt ledger, truth gaps, shadow agenda, risk forecast, decision SLA, vendor exit simulation, regulatory shock readiness, cyber business impact, talent criticality, capital allocation, post-decision learning, CIO OS maturity, stakeholder alignment, exception waiver drafting, policy-as-code readiness, benefits realization, operating rhythm autopilot, escalation drafts, executive decision backlog, enterprise control tower, carve-out readiness, data trust, architecture runway, executive narrative, due-diligence questions, resilience continuity, customer trust, AI portfolio governance, cost of delay, executive commitments, decision rights, OKR strategy fit, risk acceptance docket, service health, knowledge continuity, dependency breakpoints, transformation kill criteria, vendor negotiation brief, compliance evidence pack, board decision simulation, operating risk heatmap, roadmap reprioritization, audit finding prediction, platform rationalization, data sovereignty, operating-model debt, strategic option portfolio, decision war room, evidence chain of custody, decision rollback planner, autonomy risk budget, approval boundary mapping, evidence expiry monitoring, residual risk contracting, autonomy stress testing, decision consequence ledger, enterprise friction mapping, strategic optionality, control debt burndown, executive dissent synthesis, decision backtesting, governance drift detection, budget shock absorption, vendor leverage indexing, executive narrative diffing and human-control contract.

Visible AI mechanisms include evidence classification, weak signal ranking, contradiction detection, risk propagation, decision debt mining, board pressure simulation, value leakage detection, memory comparison, autonomy readiness scoring and visual decision intelligence.

## Unfair Advantage USP Suite

The local runtime exposes 15 explicit market-facing CIO OS modules through `python engine/cli.py unfair-advantage-usp-suite --input ...`:

1. Executive Blind Spot Radar: detects leadership gaps that are absent from the update but expected for the decision.
2. Decision Latency Cost Engine: names the compounding pressure created by non-decisions.
3. Board Trust Score: scores whether the packet is likely to earn board confidence or challenge.
4. CIO Replacement Map: separates AI-preparable CIO work from human-only accountability.
5. Executive Narrative Firewall: blocks optimistic claims that conflict with evidence gaps or negative facts.
6. Vendor Leverage Intelligence: detects when vendor dependency, weak evidence or owner gaps increase vendor power.
7. Risk-to-Cash Translator: turns technical, control and delivery risks into directional business exposure.
8. Strategic Drift Early Warning: finds strategy, budget, architecture and execution drift before more spend is approved.
9. Accountability Gap Detector: finds decisions, risks and evidence gaps without owner, approver or review date.
10. Evidence Decay Monitor: flags stale or missing evidence before board, audit or approval use.
11. Autonomy Boundary Engine: defines what AI may prepare, what needs approval and what remains human-only.
12. Executive Attention Allocator: turns signals into the CIO weekly attention agenda.
13. Portfolio Cannibalization Detector: detects initiatives competing for the same budget, capacity or business attention.
14. Decision Chain of Custody: traces facts, assumptions, missing evidence and recommendations.
15. Synthetic Executive Committee: pressure-tests decisions through CEO, CFO, CISO, Audit, COO and Board lenses.

## Disruptive use cases

- Find decision debt before it becomes delivery failure.
- Expose value leakage hidden across projects, vendors, architecture and operations.
- Convert fragmented updates into board-ready decision packets.
- Detect strategy drift between stated priorities, budgets, projects and governance behavior.
- Challenge investment, AI, vendor and transformation proposals before steering approval.
- Build crisis command views that distinguish known facts, unknowns, decisions and communication needs.
- Run industrial CIO operating reviews across IT/OT, ERP/MES/QMS, production continuity, audit evidence and vendor exposure without naming or depending on a specific company.

## MVP boundaries

- No authenticated live data connectors in version 0.1; connector profiles and local file/directory ingestion are included.
- No production MCP server in version 0.1; only an optional local MCP-compatible adapter for the Decision Intelligence Engine.
- No hosted web app in version 0.1; the local web app is stdlib-only and runs on `127.0.0.1`.
- Skills must clearly separate evidence, assumptions, hypotheses and missing data.
- External actions are prepared as drafts only and are not executed automatically.

## Standard input contract

Provide any mix of:

- goal and target audience
- time period and organization unit
- meeting notes or document excerpts
- project, risk, KPI, ticket, budget or architecture exports
- relevant decisions, constraints, risk tolerance and preferred output format

## Standard output contract

Most skills produce:

- Executive Summary
- Situation
- Key Findings
- Detected Dependencies
- Risks & Early Warnings
- Opportunities
- Decision Options
- Recommended Actions
- Owners / Suggested Accountability
- Evidence & Assumptions
- Missing Data
- Next 24h / 7d / 30d Actions

## Operating system files

- `docs/skill-catalog.md`: maps leadership jobs to the right skill.
- `docs/skill-suites.md`: groups the specialist skills into eight user-facing suites.
- `docs/skill-operating-contract.md`: shared handoff contract so skills behave as one operating system.
- `skills/index`: Sales-style router/frontdoor for broad Autonomous CIO requests.
- `skills/user-context`: Sales-style preflight and plugin-scoped context layer.
- `docs/autonomous-cio-operating-model.md`: governed CIO operating-system model.
- `docs/autonomy-policy.md`: L0-L4 autonomy levels and human-only boundaries.
- `docs/cio-autopilot-playbook.md`: flagship Autopilot Review workflow.
- `docs/cio-replacement-surface.md`: what can be automated, drafted, decision-supported and human-only.
- `docs/scoring-model.md`: common scoring language for urgency, impact, risk and confidence.
- `docs/decision-intelligence-engine.md`: local Python runtime, CLI, optional MCP adapter, scores and visual command center.
- `docs/prompt-pack.md`: ready-to-use prompts for executive, crisis, risk, AI governance and transformation work.
- `docs/playbooks.md`: chained workflows for Board prep, crisis, AI approval, transformation and monthly CIO reviews.
- `docs/proof-pack.md`: demo inputs and expected output shapes that prove the Decision Intelligence Loop.
- `docs/optional-connectors.md`: optional Teams, Slack, email, calendar and document connector profiles.
- `templates/executive-briefing.md`: reusable briefing format.
- `templates/executive-decision-packet.md`: signature decision artifact format.
- `templates/command-center-report.md`: reusable enterprise situation report format.
- `templates/decision-memo.md`: reusable decision memo format.
- `templates/risk-action-register.md`: reusable risk-to-action register.
- `templates/board-pack-outline.md`: reusable board-pack structure.
- `templates/executive-operating-review.md`: reusable monthly operating review.
- `templates/decision-memory.md`: phase-2 starter template for reusable executive decisions.
- `templates/assumption-register.md`: phase-2 starter template for assumptions that need validation.
- `templates/evidence-graph.md`: phase-2 starter template for claims, evidence and confidence.
- `templates/risk-chain-map.md`: phase-2 starter template for cascading risk paths.
- `templates/action-ledger.md`: phase-2 starter template for draft actions and approvals.

## Local Decision Intelligence Engine

The package includes a local Python runtime in `engine/` for reproducible demo and smoke-test outputs. In Codex plugin usage, the Codex host LLM performs semantic extraction and executive reasoning; the local engine turns that structured context into deterministic scores, graphs, packets, memory updates, dashboard data and export packages. It can build Executive Decision Packets, score decision readiness, map risk chains, extract evidence graphs, compare provided context with local memory examples, inspect local memory stores, orchestrate skill chains, define connector profiles, ingest local files/directories, run policy checks, simulate decision-twin scenarios, draft actions, write local SQLite memory, build board packs and regenerate Visual Command Center data.

```text
python engine/cli.py build-decision-packet --input engine/examples/board_prep.json
python engine/cli.py autopilot-review --input engine/examples/autopilot_review.json
python engine/cli.py autopilot-review --input engine/examples/industrial_operating_review.json
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
python engine/cli.py init-memory-db --db .local-memory/autonomous_cio.db
python engine/cli.py ingest-bundle --input engine/examples --db .local-memory/autonomous_cio.db
python engine/cli.py decision-twin --input engine/examples/industrial_operating_review.json --scenario defer
python engine/cli.py score-evidence --input engine/examples/industrial_operating_review.json
python engine/cli.py evaluate-policy --input engine/examples/ai_governance.json --policy ai-governance
python engine/cli.py approval-gates --input engine/examples/industrial_operating_review.json
python engine/cli.py governance-readiness --input engine/examples/industrial_operating_review.json
python engine/cli.py draft-actions --input engine/examples/board_prep.json --type email
python engine/cli.py build-board-pack --input engine/examples/board_prep.json --output-dir .local-export/board-pack --format both
python engine/cli.py sla-monitor --db .local-memory/autonomous_cio.db
python engine/cli.py run-evals --eval-dir engine/evals
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
python engine/cli.py executive-weekly-brief --db .local-memory/autonomous_cio.db --output-dir .local-export/weekly-brief --format both
python engine/cli.py strategic-contradictions --input engine/examples/industrial_operating_review.json --db .local-memory/autonomous_cio.db
python engine/cli.py delegation-planner --input engine/examples/board_prep.json
python engine/cli.py import-context --input engine/examples/sample_import.csv
python engine/cli.py build-from-file --input engine/examples/sample_import.csv
python engine/cli.py dashboard-from-file --input engine/examples/sample_import.csv
python engine/cli.py ingest-directory --input engine/examples
python engine/cli.py refresh-dashboard --input engine/examples/board_prep.json --output visual-command-center/demo-data.json
python engine/cli.py save-memory --input engine/examples/board_prep.json --memory .local-memory/demo-memory.json
python engine/cli.py evaluate
```

Open `visual-command-center/index.html` for a local dashboard with JSON upload, JSON export, decision scores, evidence heatmap, risk chain, decision debt, board pressure, operating rhythm, benchmark, trend delta, quality grade, value-at-risk, board coverage, anti-patterns, attention budget, decision packet preview, memory update proposal, connector profile view and export readiness.

Start `python app/server.py --port 8765` for the local CIO OS web app at `http://127.0.0.1:8765`. It exposes local-only endpoints for source-bundle ingestion, decision packets, memory browsing, policy evaluation, governance readiness, board-pack export and eval reports. It uses no framework, no network dependency and no external execution.

The adaptive learning loop is explicit and local: feedback, outcomes, board questions and skill-chain ratings are written only to the provided SQLite DB. The engine does not train a model or update external state; it produces calibration hints, learned patterns, source reputation, recommendation backtests, Decision DNA, Risk Appetite Twin, Board Memory and weekly CIO operating snapshots for the next review.

For a complete product demo, start the local web app, click `Seed Demo Memory`, then `Weekly Brief`. The app renders the Executive Weekly Brief as a readable executive artifact and can export Markdown and HTML proof files.

The engine also includes connector-ready signal contracts for Teams, Slack, Outlook Email, Gmail/Google Workspace, Outlook Calendar, SharePoint, Google Drive, Confluence, Jira, Azure DevOps, GitHub, ServiceNow, TOPdesk, CMDB/assets, cloud cost, security findings, observability, ERP/SAP and finance CSV sources. Version 0.1 has real local file and directory ingestion plus profile-specific export adapters for local CSV/JSON/TXT/Markdown files, but no authenticated live SaaS connectors.

`requirements.txt` is intentionally stdlib-only. `scripts/run-engine-smoke-tests.ps1` runs the local engine smoke suite and plugin validator.

## Disruptive intelligence layer

The expanded skill set adds an enterprise nervous system around the Decision Intelligence Loop:

- strategy drift detection across portfolio, budget, architecture and execution
- decision debt discovery for unresolved choices and blocked accountability
- pre-mortem simulation before transformation failure becomes visible
- crisis command mode for incidents, outages, regulatory events and executive escalations
- AI governance reviews for internal AI initiatives
- vendor ecosystem intelligence for lock-in, concentration and exit risk
- value leakage detection across spend, capacity and technology investments
- enterprise friction analysis for structural drag and slow decision systems
- autonomous executive memory for recurring decisions, assumptions and follow-ups
- truth-layer classification of facts, assumptions, narratives, politics and missing evidence
- attention routing into ignore, monitor, delegate, decide, escalate and act-now categories
- risk-chain propagation across project, architecture, security, compliance, finance and operations
- boardroom Q&A simulation for Audit, CEO, CFO, CISO and regulator perspectives
- transformation value tracking that detects activity without value realization
- orchestration logic that selects the right skill chain for ambiguous executive requests
- governed CIO autopilot review from mixed context
- CIO replacement surface that separates automated preparation, drafted work, decision support and human-only accountability

## Roadmap

Phase 2 now includes explicit SQLite Executive Memory and adaptive learning records. Phase 3 includes local intelligence tools, scoring, policy checks, decision-twin simulation, evals and score calibration. Phase 4 has export-first connector profiles and source-bundle ingestion. Phase 5 includes static and local-web command-center surfaces. Phase 6 adds governed draft workflows, approval gates, recommendation backtests and audit-friendly local memory.
