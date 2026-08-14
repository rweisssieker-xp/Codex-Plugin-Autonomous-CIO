# Evaluation and Release

This repository separates the engineering workspace from the lean marketplace package.

## Golden Scenarios

The deterministic golden suite lives in `engine/evals/golden_cases.json` and covers 50 CIO scenarios across board prep, crisis command, AI approval, transformation value, portfolio decisions, vendor pressure, audit evidence and operating risk.

Run:

```text
python engine/cli.py run-evals --eval-dir engine/evals
```

Each case checks request type, score range, guardrails and the decision-output rubric:

- facts separated
- assumptions labeled
- hypotheses labeled
- missing evidence present
- decision needed clear
- recommended action present
- board questions present
- no live-action claim

## Orchestrator Chain Evals

Run:

```text
python engine/cli.py orchestrator-evals --eval-dir engine/evals
```

This validates that the front door detects the request type and includes the required specialist skills in the selected chain.

## Usage Benchmark

Run:

```text
python engine/cli.py usage-benchmark --eval-dir engine/evals
```

This creates deterministic local token estimates for input, output, selected skill count, missing evidence count and board-question count. It is not a substitute for observed Codex usage logs; it is the local baseline to compare real runs against.

## Marketplace Package

Run:

```text
python scripts/build-marketplace-package.py
```

This creates `dist/the-autonomous-cio`, the lean package used for marketplace evaluation. It keeps all 133 skills, with `autonomous-cio-orchestrator` as the single implicit front door and 132 explicit-only specialist skills.

## Submission Pack

Run:

```text
python scripts/build-submission-pack.py
```

This creates `dist/submission/the-autonomous-cio-marketplace-plugin.zip` plus review notes and a submission manifest.

## Plugin Evaluation

Run plugin evaluation against the generated package, not the source repo:

```text
node C:\Users\weiss\.codex\plugins\cache\openai-curated-remote\plugin-eval\0.1.2\scripts\plugin-eval.js analyze dist\the-autonomous-cio --format markdown
```

Expected result: `100/100`, grade `A`, low risk, no fails and no warnings.

## CI

GitHub Actions runs unit tests, golden evals, orchestrator evals, usage benchmark, hardening evals, marketplace package build and submission-pack build.
