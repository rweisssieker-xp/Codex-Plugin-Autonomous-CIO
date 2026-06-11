# Sales-Style Architecture

The Autonomous CIO now mirrors the strongest Sales plugin pattern while keeping its executive-decision domain.

## Pattern Adopted

- `skills/index`: broad router and orientation surface.
- `skills/user-context`: mandatory preflight and plugin-scoped context layer.
- focused workflow skills: `autonomous-cio-operating-review`, `executive-decision-packet`, `executive-truth-layer`, `risk-chain-intelligence`, `decision-scenario-intelligence`, `board-challenger`, `autonomous-action-framework`, `autonomous-executive-memory`.
- suite routing: eight user-facing suites group the specialist skills so the product does not feel like a flat catalog.
- shared source categories instead of hard-coded connectors.
- first-run and next-step guidance in user-facing workflows.
- one concrete next action after substantive outputs.
- local preflight script returning a structured `cio_preflight` envelope.

## Why

The previous structure had many powerful skills but could feel like a large catalog. The Sales-style structure adds:

- clear front door
- reusable user context
- source-category mapping
- consistent routing
- focused workflow ownership
- predictable handoffs
- action-oriented continuation

## Local Preflight

Run:

```text
python skills/user-context/scripts/cio_preflight.py --workflow index
```

The script reads:

```text
$CODEX_HOME/state/plugins/the-autonomous-cio/the-autonomous-cio/user-context.md
```

If no saved context exists, workflows still proceed from user-provided context.

## State Boundary

The user-context layer stores preferences, source pointers and reusable conventions. It does not store secrets, raw sensitive records, connector credentials, automatic persistence claims or external execution permissions.
