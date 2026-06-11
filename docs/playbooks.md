# Playbooks

These playbooks combine skills into repeatable executive workflows. Version 0.1 executes them as reasoning workflows over user-provided context.

## Governed CIO Autopilot Playbook

Use for broad CIO operating reviews, Board in 48h requests, monthly operating reviews and mixed enterprise context.

Skill chain:

1. `autonomous-cio-operating-review`
2. `executive-decision-packet`
3. `risk-chain-intelligence`
4. `autonomous-action-framework`
5. `autonomous-executive-memory`

Engine command:

```text
python engine/cli.py autopilot-review --input engine/examples/autopilot_review.json
```

Output:

- decision readiness
- enterprise status
- evidence graph
- risk chain
- attention budget
- action ledger
- autonomy gate
- memory update
- CIO replacement surface

## Decision Intelligence Loop Playbook

Use when mixed context needs to become one decision-ready executive artifact, especially for board decisions, go-live approvals, crisis trade-offs, AI approvals and transformation funding gates.

Skill chain:

1. `enterprise-signal-ranking`
2. `executive-truth-layer`
3. `risk-chain-intelligence`
4. `decision-scenario-intelligence`
5. `executive-decision-packet`
6. `autonomous-action-framework`
7. `autonomous-executive-memory`

Output:

- Executive Decision Packet
- request type and selected skill chain
- decision needed
- facts vs assumptions
- risk chain
- options
- board challenge questions
- recommended action
- missing evidence
- draft next steps

## Board Prep Playbook

Use for board meetings, supervisory reviews, investment approvals and major risk acceptances.

Skill chain:

1. `executive-truth-layer`
2. `board-challenger`
3. `executive-q-and-a-simulator`
4. `decision-consequence-mapper`
5. `executive-reporting`

Output:

- board narrative
- decision requests
- strongest risks and counterarguments
- likely board questions
- missing evidence
- approval safeguards

## Crisis Command Playbook

Use for outages, cyber events, customer escalations, regulatory events and executive incidents.

Skill chain:

1. `crisis-command-mode`
2. `risk-chain-intelligence`
3. `management-attention-optimizer`
4. `autonomous-action-framework`
5. `enterprise-briefing`

Output:

- situation report
- command roles
- known facts and unknowns
- cascading risk paths
- decision and communication plan
- 1h / 4h / 24h / 7d actions

## AI Approval Playbook

Use for AI use cases, model/provider decisions, internal copilots and automation proposals.

Skill chain:

1. `ai-governance-intelligence`
2. `assumption-mining-engine`
3. `governance-gap-predictor`
4. `risk-compliance-intelligence`
5. `autonomous-action-framework`

Output:

- value and risk assessment
- data and model risk
- required controls
- approval recommendation
- governance gaps
- action register

## Transformation Control Playbook

Use for ERP, operating-model, cloud, data, AI, security or enterprise architecture transformations.

Skill chain:

1. `transformation-readiness-intelligence`
2. `strategy-drift-intelligence`
3. `enterprise-pre-mortem`
4. `transformation-value-tracker`
5. `decision-debt-intelligence`

Output:

- readiness scorecard
- strategy drift findings
- failure scenarios
- value realization risks
- blocked decisions
- corrective actions

## Monthly CIO Operating Review

Use for a recurring executive review of portfolio, operations, finance, risk, architecture, security and organization.

Skill chain:

1. `enterprise-signal-ranking`
2. `enterprise-command-center`
3. `project-portfolio-intelligence`
4. `architecture-data-security-intelligence`
5. `finance-investment-intelligence`
6. `executive-reporting`

Output:

- domain status
- top priorities
- top decisions
- portfolio health
- architecture/security risks
- financial deviations
- board-ready summary

## Vendor and Sourcing Risk Playbook

Use for major vendor decisions, renewals, outsourcing reviews and platform lock-in concerns.

Skill chain:

1. `vendor-ecosystem-intelligence`
2. `technical-debt-capitalizer`
3. `finance-investment-intelligence`
4. `risk-chain-intelligence`
5. `board-challenger`

Output:

- dependency map
- lock-in and exit risks
- cost exposure
- technical/business risk
- negotiation or exit recommendations

## Meeting-to-Action Playbook

Use after steering committees, operating reviews, incident calls and executive meetings.

Skill chain:

1. `autonomous-meeting-intelligence`
2. `decision-debt-intelligence`
3. `autonomous-executive-memory`
4. `autonomous-action-framework`

Output:

- decisions
- open decisions
- risks and assumptions
- action register
- executive memory update
