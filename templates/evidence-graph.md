# Evidence Graph

Use this local template to connect claims, facts, sources and confidence. Version 0.1 uses user-provided context only.

## Claims

| Claim ID | Claim | Type | Confidence | Source Refs | Missing Evidence |
| --- | --- | --- | --- | --- | --- |
| CLM-001 |  | Fact / Inference / Assumption / Hypothesis | High / Medium / Low |  |  |
| CLM-DEMO-ERP-001 | ERP testing has not started because the test environment is late | Fact | High | Proof Pack meeting notes | Test environment recovery date |
| CLM-DEMO-ERP-002 | The go-live date is still credible | Hypothesis | Low | Sponsor narrative | Test plan, defect trend, vendor recovery plan |

## Relationships

| From | Relationship | To | Why It Matters | Confidence |
| --- | --- | --- | --- | --- |
| CLM-001 | supports / contradicts / depends on / weakens | CLM-002 |  | High / Medium / Low |
| CLM-DEMO-ERP-001 | weakens | CLM-DEMO-ERP-002 | Late testing reduces confidence in the target go-live date | High |
