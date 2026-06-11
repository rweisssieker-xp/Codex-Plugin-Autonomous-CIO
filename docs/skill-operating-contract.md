# Skill Operating Contract

All The Autonomous CIO skills should behave as one decision operating system, not as isolated prompts. Use this contract whenever a skill participates in a chain.

## Shared Input Model

Preserve these fields when available:

- `request_type`
- `decision_needed`
- `facts`
- `inferences`
- `assumptions`
- `hypotheses`
- `narratives`
- `contradictions`
- `missing_evidence`
- `entities`
- `dependencies`
- `risk_chain`
- `options`
- `recommended_action`
- `draft_next_steps`
- `memory_updates`

## Shared Output Contract

Every substantial output should include:

- decision or executive question being answered
- facts vs assumptions
- evidence confidence
- missing evidence
- risk chain or impact path
- decision debt
- options or actions
- owner / suggested accountability
- board or stakeholder challenge
- next 24h / 7d / 30d moves when action is implied
- guardrails and human approval boundary

## Chain Handoff Rules

- `autonomous-cio-orchestrator` identifies request type and selected chain.
- `enterprise-signal-ranking` ranks what matters.
- `executive-truth-layer` classifies evidence and contradictions.
- `risk-chain-intelligence` maps propagation and business impact.
- `decision-scenario-intelligence` compares options and sensitivities.
- `board-challenger` stress-tests the preferred option and narrative.
- `executive-decision-packet` assembles the signature artifact.
- `autonomous-action-framework` turns recommendations into draft actions only.
- `autonomous-executive-memory` captures decisions, assumptions and commitments for later reuse.

## Executive Defense Add-On

When the request involves approval, board preparation, risk acceptance, transformation spend or executive commitment, add:

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

## Safety Boundary

Skills may use the Codex host LLM for semantic extraction and executive reasoning over provided context. They must not claim live connector access, automatic persistence or external execution unless a future explicit tool and user approval are available.
