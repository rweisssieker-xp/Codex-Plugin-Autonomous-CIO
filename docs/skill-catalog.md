# Skill Catalog

Use this catalog to route work to the right skill. Skills are connector-neutral in version 0.1 and operate on context provided by the user.

## Executive Command

- `autonomous-cio-orchestrator`: route broad executive requests to the right skill chain.
- `enterprise-briefing`: daily or weekly C-level briefing, top themes, decisions and actions.
- `enterprise-command-center`: cross-domain situation report with Green / Amber / Red status.
- `executive-reporting`: board, management, KPI, audit and portfolio report narratives.
- `crisis-command-mode`: active incident, outage, breach, regulatory or customer escalation.
- `autonomous-executive-memory`: decisions, assumptions, risks and commitments that must carry forward.

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
- `technical-debt-capitalizer`: technical debt translated into executive business risk.
- `zero-trust-executive-intelligence`: identity, access, asset and Zero Trust roadmap.
- `data-product-governance-intelligence`: data product ownership, quality, lineage and trust.
- `risk-compliance-intelligence`: risks, controls, audit readiness and countermeasures.
- `ai-governance-intelligence`: AI use-case risk, value, controls and approval path.
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
- Board approval: `board-challenger` -> `decision-debt-intelligence` -> `executive-reporting`.
- AI approval: `ai-governance-intelligence` -> `risk-compliance-intelligence` -> `autonomous-action-framework`.
- Architecture modernization: `technical-debt-capitalizer` -> `architecture-data-security-intelligence` -> `finance-investment-intelligence`.
- Operating model change: `organization-workforce-intelligence` -> `enterprise-friction-intelligence` -> `operating-model-simulator`.
- Executive truth review: `executive-truth-layer` -> `narrative-consistency-scanner` -> `confidence-heatmap-intelligence`.
- Risk propagation: `risk-chain-intelligence` -> `governance-gap-predictor` -> `autonomous-action-framework`.
- Board prep: `executive-q-and-a-simulator` -> `board-challenger` -> `decision-consequence-mapper`.
- Transformation value review: `transformation-value-tracker` -> `value-leakage-intelligence` -> `strategy-drift-intelligence`.
