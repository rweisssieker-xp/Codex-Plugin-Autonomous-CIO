# CIO Autopilot Playbook

Use this playbook when leadership asks for a full CIO operating view rather than a narrow analysis.

## Trigger Prompts

- Run the CIO review.
- Make the enterprise decision-ready.
- Prepare the Board in 48 hours.
- What should the CIO decide this week?
- Turn this status folder into actions and memory.

## Skill Chain

1. `autonomous-cio-operating-review`
2. `executive-decision-packet`
3. `risk-chain-intelligence`
4. `management-attention-optimizer`
5. `autonomous-action-framework`
6. `autonomous-executive-memory`

## Engine Command

```text
python engine/cli.py autopilot-review --input engine/examples/autopilot_review.json
python engine/cli.py autopilot-review --input engine/examples --memory engine/examples/memory.json
python engine/cli.py autopilot-review --input engine/examples/autopilot_review.json --format markdown
```

## Output Review Checklist

- Is the decision needed explicit?
- Are facts separated from assumptions?
- Are missing evidence and owners visible?
- Does the risk chain show business impact?
- Are Board questions tough enough?
- Are draft actions classified by autonomy level?
- Does the memory update avoid automatic persistence claims?
- Is the operating rhythm actionable for 24h, 7d and 30d?
