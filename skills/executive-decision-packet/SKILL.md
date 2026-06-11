---
name: executive-decision-packet
description: Convert mixed enterprise context into the signature Executive Decision Packet with decision needed, facts vs assumptions, risk chain, options, board challenge questions, recommendation, missing evidence and draft next steps.
---

# Executive Decision Packet

## Mission

Create the signature decision artifact for The Autonomous CIO. Turn meeting notes, risk registers, budget updates, project status, architecture context, security findings, AI proposals or crisis signals into one governed executive decision packet.

## Inputs

Accept mixed enterprise context, including meeting notes, risk registers, budget updates, portfolio status, audit findings, security concerns, AI use cases, vendor updates, architecture constraints, crisis notes and explicit decision requests.

## Workflow

1. Identify the request type: Board Prep, Crisis Command, AI Approval, Transformation Value, Portfolio Decision, Operating Review, Risk Escalation or General Executive Decision.
2. State the selected reasoning chain and why it fits.
3. Use the Codex host LLM as the primary semantic extraction layer: classify facts, inferences, assumptions, hypotheses, narratives, contradictions, entities, dependencies and missing evidence.
4. Rank weak and strong signals by executive relevance, impact, urgency, dependency reach and uncertainty.
5. Map the risk chain from signal to dependency, amplifier, business impact and decision pressure.
6. Identify decision debt, contradictions, value leakage and governance gaps.
7. Compare options by benefit, risk, dependency, reversibility and confidence.
8. Simulate board pressure from CEO, CFO, CISO, Audit, regulator, customer or employee perspectives as relevant.
9. Add Executive Decision Defense when approval, board exposure, risk acceptance, transformation value, audit/security controls or material commitment is involved.
10. Recommend the action, safeguards, owner and first move.
11. Prepare draft next steps for 24h, 7d and 30d without claiming external execution.

## Executive Decision Defense

Include these sections when relevant:

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

## Local Engine Support

When working in the local repository, `engine/cli.py` can generate reproducible outputs for this format. The Codex skill layer may provide an `llm_extraction` object to the local engine; the engine then uses that structured LLM extraction for deterministic scoring, risk mapping and dashboard generation. If no `llm_extraction` is provided, the engine falls back to local heuristics.

Treat the engine as a local support artifact only; do not imply live data access, automatic persistence or external action execution.

## LLM Extraction Contract

When preparing engine-ready context, populate this optional object:

```json
{
  "llm_extraction": {
    "facts": [],
    "inferences": [],
    "assumptions": [],
    "hypotheses": [],
    "narratives": [],
    "contradictions": [],
    "entities": [],
    "dependencies": [],
    "missing_evidence": []
  }
}
```

## Handoff Rules

- From `executive-truth-layer`, preserve facts, assumptions, narratives, contradictions and missing evidence exactly.
- From `risk-chain-intelligence`, preserve: signal -> dependency -> amplifier -> business impact -> decision pressure.
- From `decision-scenario-intelligence`, preserve options, reversibility, sensitivities and kill criteria.
- From `board-challenger`, preserve hardest questions and weak-answer risks.
- To `autonomous-action-framework`, pass only draft actions with owner, approval and evidence gates.
- To `autonomous-executive-memory`, pass decisions, assumptions, commitments and unresolved evidence gaps.

## Output Format

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

## Guardrails

Do not claim live system access, automatic persistence or executed external actions. Treat legal, regulatory, HR, security and financial conclusions as decision support, not final specialist determinations. Make confidence and missing evidence visible.
