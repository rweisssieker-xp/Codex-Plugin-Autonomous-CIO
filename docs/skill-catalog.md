# Skill Catalog

Use this catalog to route work to the right skill. Skills are connector-neutral in version 0.1 and operate on context provided by the user.

## Preferred Routing Model

Use suites first. Specialist skills are modules inside the suite, not the first visible choice.

| Suite | Primary Skill | Use When |
| --- | --- | --- |
| Executive Operating System | `autonomous-cio-operating-review` | broad CIO review, monthly review, Board in 48h, mixed context |
| Executive Decision Intelligence | `executive-decision-packet` | approval, trade-off, decision, risk acceptance, commitment |
| Board And Narrative Defense | `board-challenger` | narrative must survive CEO/CFO/CISO/Audit/Board pressure |
| Risk, Resilience And Controls | `risk-chain-intelligence` | cascading risk, crisis, audit, security, compliance, resilience |
| Transformation, Portfolio And Value | `transformation-value-tracker` | value leakage, portfolio trade-offs, spend, benefits, roadmap |
| Industrial IT/OT, Quality And Manufacturing | `industrial-cio-operating-system` | regulated production, ERP/MES/QMS/PLM, IT/OT risk, audit evidence, continuity |
| Architecture, Data, AI And Vendor | `architecture-data-security-intelligence` | architecture, technical debt, data trust, AI governance, vendor |
| Organization, Operating Model And Knowledge | `organization-workforce-intelligence` | ownership, capacity, operating model debt, talent, knowledge |

See `docs/skill-suites.md` for the grouped specialist modules.

## Signature Workflows

- Decision Readiness Score: use the local engine `score` command or `executive-decision-packet` skill when leadership needs to know whether an approval is evidence-ready.
- Evidence Graph: use `executive-truth-layer`, `confidence-heatmap-intelligence` and the local engine `extract-evidence-graph` command.
- Risk Chain Map: use `risk-chain-intelligence` and the local engine `map-risk-chain` command.
- Decision Debt Radar: use `decision-debt-intelligence` and `autonomous-executive-memory`.
- Board Pressure Simulation: use `board-challenger` and `executive-q-and-a-simulator`.
- Value Leakage Detector: use `value-leakage-intelligence` and `transformation-value-tracker`.
- Executive Memory Comparison: use `autonomous-executive-memory` and the local engine `compare-memory` command.
- Autonomy Readiness Score: use `autonomous-action-framework` with the local scorecard's autonomy readiness signal.
- Governed Autonomy Layer: use `autonomous-action-framework` to draft actions without external execution.
- Visual Command Center: open `visual-command-center/index.html` for the static local cockpit.
- CIO Work Autonomy Map: use `cio-work-autonomy-map` to show what CIO work is automated, drafted, decision-supported or human-only.
- Board Objection Simulator: use `board-objection-simulator` for hard CEO, CFO, CISO, Audit, regulator, customer and Board pressure testing.
- Decision Debt Ledger: use `decision-debt-ledger` to clear delayed, implicit, repeated or ownerless decisions.
- Truth Gap Detector: use `truth-gap-detector` to expose gaps between status narratives and evidence.
- Executive Time Saved Estimator: use `executive-time-saved-estimator` to estimate prepared CIO, PMO, risk and board-prep work.
- CIO Shadow Agenda: use `cio-shadow-agenda` to identify what leadership should really discuss.
- Autonomous Steering Pack Factory: use `autonomous-steering-pack-factory` to turn context into a steering or Board pack outline.
- Risk Chain Forecast: use `risk-chain-forecast` to forecast likely next escalations.
- Strategic Drift Detector: use `strategic-drift-detector` to detect value, architecture, security or adoption drift.
- Human Control Contract: use `human-control-contract` to define autonomy levels, approvals and human-only boundaries.
- Decision SLA Enforcer: use `decision-sla-enforcer` to assign decision deadlines and breach thresholds.
- Vendor Exit Simulator: use `vendor-exit-simulator` for renegotiation, fallback, lock-in and exit options.
- Regulatory Shock Simulator: use `regulatory-shock-simulator` to prepare audit, regulator, customer or compliance response packs.
- Cyber Business Impact Translator: use `cyber-business-impact-translator` to convert security findings into business decisions.
- Talent Criticality Radar: use `talent-criticality-radar` for key-person, owner-capacity and scarce-skill risk.
- Capital Allocation Copilot: use `capital-allocation-copilot` for budget, spend, forecast and funding trade-offs.
- Post Decision Learning Loop: use `post-decision-learning-loop` after major decisions to update memory and assumptions.
- CIO OS Maturity Index: use `cio-os-maturity-index` to score CIO operating-system maturity.
- Stakeholder Alignment Matrix: use `stakeholder-alignment-matrix` to pre-align CEO, CFO, CISO, Audit, regulator, customer and sponsor perspectives.
- Exception Waiver Factory: use `exception-waiver-factory` to draft governed waivers with owner, expiry and compensating controls.
- Policy as Code Readiness: use `policy-as-code-readiness` to identify governance rules that could become codified checks later.
- Benefits Realization Sentinel: use `benefits-realization-sentinel` to detect benefit promises without measurable evidence.
- Operating Rhythm Autopilot: use `operating-rhythm-autopilot` to define cadence, rituals and prepared inputs.
- Autonomous Escalation Drafts: use `autonomous-escalation-drafts` to prepare escalation messages without sending them.
- Executive Decision Backlog: use `executive-decision-backlog` to prioritize open leadership decisions.
- Enterprise Control Tower: use `enterprise-control-tower` for operating-panel status across readiness, risk, evidence, truth gaps and decision debt.
- M&A Carve-out Readiness: use `ma-carveout-readiness` for integration, separation or carve-out due diligence.
- Data Trust Radar: use `data-trust-radar` to check whether data behind decisions is trustworthy enough.
- Architecture Runway Guardian: use `architecture-runway-guardian` to protect architecture capacity and integration readiness.
- Executive Narrative Generator: use `executive-narrative-generator` to create board, CEO, CFO, CISO/Audit and customer narratives.
- Autonomous Due Diligence Questions: use `autonomous-due-diligence-questions` to generate targeted diligence questions with evidence needs.
- Resilience Continuity Planner: use `resilience-continuity-planner` for outage, recovery, incident and continuity planning.
- Customer Trust Impact Radar: use `customer-trust-impact-radar` to translate operational signals into customer trust exposure.
- AI Portfolio Governance: use `ai-portfolio-governance` to govern AI use cases as a portfolio.
- Cost of Delay Calculator: use `cost-of-delay-calculator` to make the cost of not deciding visible.
- Executive Commitment Tracker: use `executive-commitment-tracker` to track commitments from reviews and memory.
- Decision Rights Mapper: use `decision-rights-mapper` to clarify who can approve, accept, contribute or decide.
- OKR Strategy Fit Checker: use `okr-strategy-fit-checker` to validate objective, key-result and value fit.
- Risk Acceptance Docket: use `risk-acceptance-docket` to draft owned and time-boxed risk acceptance.
- Service Health Sentinel: use `service-health-sentinel` to translate incidents, SLA and outage signals into health posture.
- Knowledge Continuity Planner: use `knowledge-continuity-planner` for critical know-how and backup-owner planning.
- Dependency Breakpoint Analyzer: use `dependency-breakpoint-analyzer` to find where dependencies can break execution.
- Transformation Kill Criteria: use `transformation-kill-criteria` to define stop/change/continue triggers.
- Vendor Negotiation Brief: use `vendor-negotiation-brief` to prepare negotiation asks and fallback position.
- Compliance Evidence Pack: use `compliance-evidence-pack` to draft audit/control evidence-package structure.
- Board Decision Simulator: use `board-decision-simulator` to simulate likely board reaction to options.
- Operating Risk Heatmap: use `operating-risk-heatmap` for Green/Amber/Red cross-domain risk view.
- Autonomous Roadmap Reprioritizer: use `autonomous-roadmap-reprioritizer` to recommend promote/protect/pause decisions.
- Audit Finding Predictor: use `audit-finding-predictor` to predict likely audit findings before review.
- Platform Rationalization Advisor: use `platform-rationalization-advisor` for consolidation, retirement or stabilization options.
- Data Sovereignty Radar: use `data-sovereignty-radar` for privacy, residency, retention and cross-border readiness.
- Operating Model Debt Ledger: use `operating-model-debt-ledger` to capture unclear ownership and governance debt.
- Strategic Option Portfolio: use `strategic-option-portfolio` to compare value/risk posture across options.
- Executive Decision War Room: use `executive-decision-war-room` for roles, first 60 minutes and exit criteria.
- Evidence Chain of Custody: use `evidence-chain-of-custody` to make evidence traceable before board or audit use.
- Decision Rollback Planner: use `decision-rollback-planner` when approvals need reversal triggers or fallback actions.
- Autonomy Risk Budget: use `autonomy-risk-budget` to limit autonomous preparation by risk, missing evidence and human-only controls.
- Approval Boundary Mapper: use `approval-boundary-mapper` to separate draft, approval-ready and human-only action boundaries.
- Evidence Expiry Monitor: use `evidence-expiry-monitor` to flag stale-risk evidence before board, audit or approval use.
- Residual Risk Contract: use `residual-risk-contract` to structure owner, conditions, expiry and rollback terms for residual risk.
- Autonomy Stress Test: use `autonomy-stress-test` to test governed autonomy against evidence, approval and human-control failure modes.
- Decision Consequence Ledger: use `decision-consequence-ledger` to map first- and second-order consequences for each option.
- Enterprise Friction Map: use `enterprise-friction-map` to identify decision, evidence, capacity, vendor and value friction.
- Strategic Optionality Engine: use `strategic-optionality-engine` to preserve future choices under uncertainty.
- Control Debt Burndown: use `control-debt-burndown` to prioritize audit, access, privacy and control evidence closure.
- Executive Dissent Synthesizer: use `executive-dissent-synthesizer` to turn executive objections into stronger decision conditions.
- Decision Backtest Simulator: use `decision-backtest-simulator` to compare current decisions against prior memory and lessons.
- Governance Drift Detector: use `governance-drift-detector` to detect recurring exceptions, bypass pressure and unclear ownership.
- Budget Shock Absorber: use `budget-shock-absorber` to prepare CIO trade-offs under budget or forecast pressure.
- Vendor Leverage Index: use `vendor-leverage-index` to score negotiation leverage from vendor dependency and evidence signals.
- Executive Narrative Diff: use `executive-narrative-diff` to reconcile changed executive narratives before communication.
- Optional Connector Router: use `optional-connector-router` to select Teams, Slack, email, calendar or document adapter workflows.
- Teams Decision Signal Adapter: use `teams-decision-signal-adapter` for Teams message exports or pasted threads.
- Slack Decision Signal Adapter: use `slack-decision-signal-adapter` for Slack exports or pasted threads.
- Email Executive Signal Adapter: use `email-executive-signal-adapter` for Outlook or Gmail exports and email threads.
- Calendar Operating Rhythm Adapter: use `calendar-operating-rhythm-adapter` for calendar exports, board dates and steering cadence.
- Delivery Work Management Adapter: use `delivery-work-management-adapter` for Jira, Azure DevOps and GitHub delivery exports.
- ITSM Service Management Adapter: use `itsm-service-management-adapter` for ServiceNow, TOPdesk and ITSM ticket exports.
- Cloud FinOps Adapter: use `cloud-finops-adapter` for Azure, AWS, GCP or FinOps cost exports.
- Security Risk Adapter: use `security-risk-adapter` for vulnerability, SIEM, identity and control-finding exports.
- Enterprise Systems Adapter: use `enterprise-systems-adapter` for ERP/SAP, CMDB, asset and application portfolio exports.
- Knowledge Document Adapter: use `knowledge-document-adapter` for Confluence, Google Drive, SharePoint and document inventories.
- Industrial CIO Operating System: use `industrial-cio-operating-system` when IT leadership context spans ERP, MES, QMS, PLM, OT, production continuity, audit evidence, vendor exposure and digital customer impact.
- IT/OT Production Risk Command: use `it-ot-production-risk-command` to map shopfloor, integration, security, service and vendor risk into production decision gates.
- QMS Audit Evidence Readiness: use `qms-audit-evidence-readiness` to check whether change, validation, access, incident and control evidence can survive audit or customer scrutiny.
- Decision Intelligence Loop: `enterprise-signal-ranking` -> `executive-truth-layer` -> `risk-chain-intelligence` -> `decision-scenario-intelligence` -> `executive-decision-packet` -> `autonomous-action-framework` -> `autonomous-executive-memory`.
- Executive Decision Packet: use `executive-decision-packet` when mixed context must become one decision-ready artifact with decision needed, facts vs assumptions, risk chain, options, board challenge questions, recommendation, missing evidence and draft next steps.
- Boardroom Challenger: `board-challenger` -> `executive-q-and-a-simulator` -> `decision-consequence-mapper`.
- AI Approval Readiness: `ai-governance-intelligence` -> `assumption-mining-engine` -> `governance-gap-predictor` -> `risk-compliance-intelligence` -> `executive-decision-packet`.
- Transformation Value Control: `transformation-value-tracker` -> `value-leakage-intelligence` -> `decision-debt-intelligence` -> `strategy-drift-intelligence` -> `executive-decision-packet`.

## Executive Command

- `autonomous-cio-orchestrator`: route broad executive requests to the right skill chain.
- `enterprise-briefing`: daily or weekly C-level briefing, top themes, decisions and actions.
- `enterprise-command-center`: cross-domain situation report with Green / Amber / Red status.
- `executive-reporting`: board, management, KPI, audit and portfolio report narratives.
- `executive-decision-packet`: signature decision artifact for board, crisis, AI approval, transformation and portfolio decisions.
- `crisis-command-mode`: active incident, outage, breach, regulatory or customer escalation.
- `autonomous-executive-memory`: decisions, assumptions, risks and commitments that must carry forward.
- `autonomous-cio-operating-review`: flagship autopilot review with the full disruptive USP layer.

## Strategy and Decisions

- `strategy-drift-intelligence`: strategy vs execution, budget, architecture and governance drift.
- `decision-debt-intelligence`: unresolved, deferred, implicit or ownerless decisions.
- `decision-scenario-intelligence`: option comparison and what-if scenario analysis.
- `enterprise-pre-mortem`: future failure simulation and prevention plan.
- `board-challenger`: critical challenge of proposals before approval.
- `executive-truth-layer`: facts, assumptions, narratives, politics, evidence and gaps.
- `management-attention-optimizer`: what leaders should ignore, monitor, delegate, decide, escalate or act on.
- `assumption-mining-engine`: critical assumptions hidden in plans, business cases and roadmaps.
- `narrative-consistency-scanner`: contradictions between reports, budgets, roadmaps and decisions.
- `executive-q-and-a-simulator`: board, audit, CEO, CFO, CISO and regulator question simulation.
- `decision-consequence-mapper`: second- and third-order effects of leadership decisions.
- `board-objection-simulator`: hard objection simulation and weak-answer risk.
- `decision-debt-ledger`: decision-debt register and clearance plan.
- `truth-gap-detector`: status narrative versus evidence gap detection.
- `cio-shadow-agenda`: real executive agenda from hidden pressure signals.
- `autonomous-steering-pack-factory`: steering and board-pack factory.
- `risk-chain-forecast`: next-escalation forecast from risk chains.
- `strategic-drift-detector`: stop/change/continue gate for drift.
- `decision-sla-enforcer`: decision deadline and escalation enforcement.
- `vendor-exit-simulator`: vendor fallback, renegotiation and exit simulation.
- `regulatory-shock-simulator`: audit, regulator and customer evidence shock preparation.
- `post-decision-learning-loop`: assumption, outcome and memory update cycle.
- `cio-os-maturity-index`: CIO operating-system maturity scoring.
- `stakeholder-alignment-matrix`: persona-specific alignment risks and messages.
- `exception-waiver-factory`: governed waiver packet drafting.
- `policy-as-code-readiness`: future codified governance check readiness.
- `operating-rhythm-autopilot`: executive cadence and ritual preparation.
- `autonomous-escalation-drafts`: escalation drafts under human approval.
- `executive-decision-backlog`: prioritized executive decision backlog.
- `enterprise-control-tower`: decision operating panel.
- `ma-carveout-readiness`: M&A, separation and carve-out readiness.
- `executive-narrative-generator`: stakeholder-specific executive narrative.
- `autonomous-due-diligence-questions`: targeted diligence questions and evidence asks.
- `resilience-continuity-planner`: continuity plan and first 24h actions.
- `customer-trust-impact-radar`: customer trust risk and posture.
- `cost-of-delay-calculator`: qualitative cost of delay and next decision gate.
- `executive-commitment-tracker`: commitments, owners, status and next checks.
- `decision-rights-mapper`: decision rights and approval mode.
- `okr-strategy-fit-checker`: objective, key-result and value fit.
- `risk-acceptance-docket`: risk acceptance owner, expiry and evidence.
- `service-health-sentinel`: operational service health posture.
- `knowledge-continuity-planner`: key-person and knowledge continuity.
- `dependency-breakpoint-analyzer`: dependency failure modes and stabilizers.
- `transformation-kill-criteria`: stop/change/continue thresholds.
- `vendor-negotiation-brief`: vendor negotiation asks and fallback.
- `compliance-evidence-pack`: compliance evidence package draft.
- `board-decision-simulator`: board option reaction simulation.
- `operating-risk-heatmap`: cross-domain operating risk map.
- `autonomous-roadmap-reprioritizer`: roadmap promote/protect/pause recommendation.

## Portfolio, Finance and Value

- `project-portfolio-intelligence`: delivery, schedule, budget, resource and dependency risks.
- `finance-investment-intelligence`: cost trends, investment cases, forecast risk and savings.
- `value-leakage-intelligence`: spend, capacity or technology that fails to produce enough value.
- `transformation-readiness-intelligence`: readiness to execute major change.

## Operations and Organization

- `process-operations-intelligence`: process, service quality, recurring issues and root causes.
- `organization-workforce-intelligence`: responsibilities, overload, role risk and knowledge islands.
- `enterprise-friction-intelligence`: slow decisions, handoff delay, duplicated work and governance drag.
- `operating-model-simulator`: role, team, governance and accountability change simulation.

## Architecture, Data, Security and Compliance

- `enterprise-knowledge-intelligence`: enterprise entity and relationship mapping.
- `architecture-data-security-intelligence`: systems, data flows, technical risk and critical assets.
- `industrial-cio-operating-system`: CIO operating review for regulated production, IT/OT, ERP/MES/QMS/PLM, vendor and customer-channel dependencies.
- `it-ot-production-risk-command`: production risk chains across IT, OT, shopfloor interfaces, security, operations and suppliers.
- `qms-audit-evidence-readiness`: QMS, validation, change-control and audit-evidence readiness for IT-enabled operations.
- `technical-debt-capitalizer`: technical debt translated into executive business risk.
- `zero-trust-executive-intelligence`: identity, access, asset and Zero Trust roadmap.
- `cyber-business-impact-translator`: security findings translated into executive business impact.
- `data-trust-radar`: data owner, metric, lineage, freshness and privacy trust checks.
- `architecture-runway-guardian`: architecture capacity, integration and technical-debt guardrails.
- `data-product-governance-intelligence`: data product ownership, quality, lineage and trust.
- `risk-compliance-intelligence`: risks, controls, audit readiness and countermeasures.
- `ai-governance-intelligence`: AI use-case risk, value, controls and approval path.
- `ai-portfolio-governance`: AI use-case portfolio governance and approval gates.
- `vendor-ecosystem-intelligence`: vendor dependency, lock-in, cost and exit risk.
- `risk-chain-intelligence`: cascading risk paths across enterprise domains.
- `governance-gap-predictor`: future control, audit and governance gaps.
- `security-business-translator`: security findings translated into business decisions.
- `regulatory-horizon-scanner`: upcoming regulatory pressure and preparation needs.

## Proactive Discovery and Action

- `autonomous-insight-engine`: weak signals, anomalies, trends and hidden opportunities.
- `autonomous-action-framework`: tasks, escalations, approvals, notifications and decision logs.
- `enterprise-signal-ranking`: weak and strong signal prioritization by executive relevance.
- `confidence-heatmap-intelligence`: evidence strength and uncertainty heatmap.
- `transformation-value-tracker`: realized value versus activity and spend.
- `portfolio-cannibalization-detector`: projects competing for the same resources, budgets or target states.
- `autonomous-meeting-intelligence`: decisions, risks, actions and assumptions from meeting notes.
- `cio-work-autonomy-map`: CIO task replacement and autonomy map.
- `executive-time-saved-estimator`: prepared-work and time-saved estimate.
- `human-control-contract`: governed autonomy boundary and approval contract.
- `talent-criticality-radar`: scarce-role and key-person operating risk.
- `capital-allocation-copilot`: executive funding and value trade-offs.
- `benefits-realization-sentinel`: benefit owner, baseline, target and value gate control.

## Routing Defaults

- If the user asks "what matters most?", use `enterprise-command-center`.
- If the user asks "what should leadership know today?", use `enterprise-briefing`.
- If the user asks "why are we slow?", use `enterprise-friction-intelligence`.
- If the user asks "what could fail?", use `enterprise-pre-mortem`.
- If the user asks "is this AI use case safe?", use `ai-governance-intelligence`.
- If the user asks "should we approve this?", use `board-challenger` then `decision-scenario-intelligence`.

## Multi-Skill Chains

- Crisis: `crisis-command-mode` -> `enterprise-briefing` -> `autonomous-action-framework`.
- Transformation review: `transformation-readiness-intelligence` -> `enterprise-pre-mortem` -> `decision-scenario-intelligence`.
- Board approval: `board-challenger` -> `decision-debt-intelligence` -> `executive-decision-packet` -> `executive-reporting`.
- AI approval: `ai-governance-intelligence` -> `risk-compliance-intelligence` -> `autonomous-action-framework`.
- Architecture modernization: `technical-debt-capitalizer` -> `architecture-data-security-intelligence` -> `finance-investment-intelligence`.
- Industrial operating review: `industrial-cio-operating-system` -> `it-ot-production-risk-command` -> `qms-audit-evidence-readiness` -> `executive-decision-packet`.
- Operating model change: `organization-workforce-intelligence` -> `enterprise-friction-intelligence` -> `operating-model-simulator`.
- Executive truth review: `executive-truth-layer` -> `narrative-consistency-scanner` -> `confidence-heatmap-intelligence`.
- Risk propagation: `risk-chain-intelligence` -> `governance-gap-predictor` -> `executive-decision-packet` -> `autonomous-action-framework`.
- Board prep: `executive-q-and-a-simulator` -> `board-challenger` -> `decision-consequence-mapper`.
- Transformation value review: `transformation-value-tracker` -> `value-leakage-intelligence` -> `strategy-drift-intelligence`.
