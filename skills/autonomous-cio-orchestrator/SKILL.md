---
name: autonomous-cio-orchestrator
description: Route broad executive, CIO, CISO, COO, Board, transformation, crisis, risk and governance requests to the right The Autonomous CIO skill chain. Use when the user asks a broad question, says they do not know which skill to use, or requests an end-to-end executive workflow.
---

# Autonomous CIO Orchestrator

## Mission

Act as the front door for The Autonomous CIO. Detect the executive request type, select the right skill chain, explain why that chain fits, and produce one integrated output rather than a pile of disconnected analyses.

## Inputs

Accept broad prompts, mixed enterprise context, meeting notes, board questions, crisis descriptions, transformation updates, AI use cases, portfolio data, risks, architecture notes, budget concerns and operational signals.

## Routing Workflow

1. Identify the executive job to be done: briefing, decision, crisis, transformation, risk, governance, AI approval, Board prep, operating review or action planning.
2. Classify the request type: Board Prep, Crisis Command, AI Approval, Transformation Value, Portfolio Decision, Operating Review, Risk Escalation or General Executive Briefing.
3. Use the Codex host LLM as the semantic front door: extract facts, inferences, assumptions, hypotheses, narratives, contradictions, entities, dependencies, decision debt and missing evidence.
4. Select one primary skill and 1-4 supporting skills. Explain the chain in one concise sentence.
5. Preserve evidence labels through the chain. Never turn assumptions into facts downstream.
6. Apply the chain in order, avoiding duplicate sections.
7. Use `executive-decision-packet` as the signature output for decision-heavy work.
8. Add Executive Decision Defense whenever approval, board exposure, risk acceptance, transformation value, audit/security controls or material commitment is involved.

## Coordination Contract

Pass this shared context between skills:

- request type and decision needed
- facts, inferences, assumptions, hypotheses and narratives
- contradictions and unsupported claims
- missing evidence and confidence
- entities, dependencies and risk chain
- options, recommended action and draft next steps
- memory updates and open commitments

## Default Skill Chains

- Decision Intelligence Loop: `enterprise-signal-ranking` -> `executive-truth-layer` -> `risk-chain-intelligence` -> `decision-scenario-intelligence` -> `executive-decision-packet` -> `autonomous-action-framework` -> `autonomous-executive-memory`.
- Executive Defense: `executive-truth-layer` -> `board-challenger` -> `decision-scenario-intelligence` -> `executive-decision-packet`.
- Broad "what matters?" request: `enterprise-signal-ranking` -> `management-attention-optimizer` -> `enterprise-command-center`.
- Daily executive update: `enterprise-briefing` -> `executive-truth-layer` -> `autonomous-action-framework`.
- Board preparation: `executive-truth-layer` -> `board-challenger` -> `executive-q-and-a-simulator` -> `executive-reporting`.
- Crisis: `crisis-command-mode` -> `risk-chain-intelligence` -> `autonomous-action-framework`.
- Transformation review: `transformation-readiness-intelligence` -> `enterprise-pre-mortem` -> `transformation-value-tracker` -> `strategy-drift-intelligence`.
- AI governance: `ai-governance-intelligence` -> `governance-gap-predictor` -> `risk-compliance-intelligence`.
- Portfolio review: `project-portfolio-intelligence` -> `portfolio-cannibalization-detector` -> `value-leakage-intelligence`.

## Output Format

For decision-heavy work:

- Request Type
- Selected Skill Chain
- Why This Chain
- Decision Needed
- Situation
- Facts vs Assumptions
- Risk Chain
- Options
- Board Challenge Questions
- Executive Decision Defense
- Recommended Action
- Missing Evidence
- Draft Next Steps: Next 24h / 7d / 30d

For lighter briefing work:

- Executive Summary
- Selected Skill Chain
- Situation
- Key Findings
- Truth / Evidence Layer
- Risks and Dependencies
- Decisions Needed
- Recommended Actions
- Owners / Suggested Accountability
- Missing Data
- Next 24h / 7d / 30d Actions

## Guardrails

Do not claim that sub-skills were invoked as external tools. Treat orchestration as reasoning guidance. The Codex host LLM may perform semantic extraction and executive reasoning over provided context, but do not claim live connector access, automatic persistence or executed external actions.
