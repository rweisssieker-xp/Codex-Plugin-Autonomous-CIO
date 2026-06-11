# Autonomy Policy

The Autonomous CIO uses governed autonomy levels for every draft action.

## Levels

- `L0 Observe`: summarize, classify and score only.
- `L1 Advise`: recommend decisions and options.
- `L2 Draft`: draft tasks, escalations, approvals and messages.
- `L3 Ready for Governed Execution`: eligible for future connector execution only with explicit user approval.
- `L4 Human-Only`: human accountability required; no automation.

## Human-Only Domains

Actions stay `L4 Human-Only` when they involve:

- legal or regulatory determinations
- HR or personnel consequences
- financial reporting or irreversible spending commitments
- security incidents, breaches, privileged access or control exceptions
- compliance and audit sign-off
- external customer or regulator commitments

## Required Fields

Every action governance item must include:

- `autonomy_level`
- `required_approval`
- `reversibility`
- `risk_level`
- `cannot_automate_reasons`
- `audit_event`

## Default Rule

When uncertain, downgrade autonomy. The plugin may draft and advise, but it must not imply execution.
