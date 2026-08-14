# Marketplace Quality Checklist

## Manifest

- Plugin name is normalized: `the-autonomous-cio`.
- Display name is human-readable: `The Autonomous CIO`.
- Description and long description explain the value without claiming live access.
- `defaultPrompt` uses exactly 3 outcome-oriented starter prompts and each is below 128 characters.
- Manifest does not reference missing logo, icon, screenshot, MCP or app files.
- Manifest validates with the plugin validator.

## Marketplace Entry

- Personal marketplace entry name matches plugin manifest name.
- Source path is `./plugins/the-autonomous-cio`.
- `policy.installation` is `AVAILABLE`.
- `policy.authentication` is `ON_INSTALL`.
- Category is `Productivity`.

## Skill Quality

- Every skill has YAML front matter with `name` and `description`.
- Skill names are kebab-case and match directory intent.
- Skills define mission, inputs, workflow, output format and guardrails.
- Skills are connector-neutral and do not claim live system access.
- High-risk domains include uncertainty and specialist-review language.

## User Experience

- Orchestrator skill routes broad requests.
- Flagship `autonomous-cio-operating-review` skill routes broad CIO autopilot work.
- Skill catalog explains when to use each skill.
- Playbooks provide end-to-end executive workflows.
- Prompt pack provides copy-ready examples.
- Templates make outputs repeatable.
- Smoke tests cover the main workflows.
- Local engine examples produce reproducible Executive Decision Packets.
- Static visual command center demonstrates scores, evidence heatmap, risk chain, decision debt, decision packet preview, memory proposal, connector profile view and export readiness.
- Local connector profiles are documented as signal contracts, not live integrations.
- Local export package generation writes only to user-specified paths.
- Skill orchestration output explains why a chain was selected.

## Safety

- Facts, assumptions, hypotheses and missing data are explicitly separated.
- External actions are drafts only.
- No claims of legal, compliance, security or financial final authority.
- No secrets are included in source files.
