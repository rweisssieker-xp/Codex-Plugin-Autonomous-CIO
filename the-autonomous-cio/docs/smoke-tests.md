# The Autonomous CIO Smoke Tests

Use these prompts after installing or updating the plugin. Each test should produce the standard output contract, clearly separate evidence from assumptions, and avoid claiming live connector access.

## autonomous-cio-orchestrator

Prompt:

```text
Use autonomous-cio-orchestrator. Choose the right workflow and produce an integrated executive artifact:
ERP is red, privileged access gaps remain open, audit evidence is incomplete, two architects are overloaded, cloud spend is 18% above forecast, and leadership needs a board update in 48 hours.
```

Expected:

- selected skill chain
- integrated executive summary
- risks and dependencies
- decisions needed
- next 24h / 7d / 30d actions

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
