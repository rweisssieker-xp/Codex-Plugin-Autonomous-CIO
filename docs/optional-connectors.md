# Optional Connector Layer

The Autonomous CIO remains connector-neutral in version 0.1. It does not claim authenticated live access to Teams, Slack, mailboxes, calendars or document systems.

Instead, it includes optional connector profiles and adapter skills that can work with:

- pasted context
- local CSV/JSON/TXT/Markdown exports
- local export directories
- future MCP tools
- separately enabled Codex connectors with explicit user authorization

## Supported Optional Profiles

| Profile | Source | Primary use |
|---|---|---|
| `teams_messages` | Microsoft Teams messages or exports | Blockers, weak signals, owner language, escalation texture |
| `slack_messages` | Slack exports or pasted threads | Incident signals, decision fragments, blockers, sentiment shifts |
| `outlook_email` | Outlook mail exports or connector context | Approval requests, commitments, evidence references, escalations |
| `gmail_workspace` | Gmail or Google Workspace exports | Vendor messages, AI approvals, risk signals, evidence attachments |
| `outlook_calendar` | Calendar exports or connector context | Board dates, steering committees, decision deadlines |
| `sharepoint_documents` | SharePoint / OneDrive exports or excerpts | Policies, board packs, audit evidence, architecture notes |
| `jira_delivery` | Jira exports | Epics, blocked stories, release scope, delivery dependencies |
| `azure_devops_delivery` | Azure DevOps exports | Work items, release risk, defects, sprint pressure |
| `github_delivery` | GitHub issue/PR exports | Release risk, open defects, dependency changes |
| `servicenow_service` | ServiceNow exports | Incidents, changes, problems, CMDB CI and SLA exposure |
| `topdesk_service` | TOPdesk exports | Incidents, changes, problems, service health and SLA risk |
| `cmdb_assets` | CMDB or asset exports | Critical assets, owners, lifecycle risk, business services |
| `cloud_cost` | Azure/AWS/GCP/FinOps exports | Budget variance, forecast risk, tag gaps, optimization candidates |
| `security_findings` | Defender/Sentinel/Splunk/Qualys-style exports | Vulnerabilities, identity risk, control gaps, risk acceptance |
| `observability_monitoring` | Datadog/New Relic/AppDynamics/monitoring exports | Availability, latency, error rate, SLO and capacity pressure |
| `erp_sap` | ERP/SAP exports | Process risk, cutover status, finance controls, master data issues |
| `confluence_knowledge` | Confluence exports | Decision records, runbooks, architecture notes, knowledge gaps |
| `google_drive_documents` | Google Drive exports | Board packs, policies, audit evidence, spreadsheets and roadmaps |

## Adapter Skills

- `optional-connector-router`
- `teams-decision-signal-adapter`
- `slack-decision-signal-adapter`
- `email-executive-signal-adapter`
- `calendar-operating-rhythm-adapter`
- `delivery-work-management-adapter`
- `itsm-service-management-adapter`
- `cloud-finops-adapter`
- `security-risk-adapter`
- `enterprise-systems-adapter`
- `knowledge-document-adapter`

## Local Engine Examples

```text
python engine/cli.py connector-profiles
python engine/cli.py connector-readiness --path engine/examples
python engine/cli.py detect-connector-profile --input engine/examples/slack_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/slack_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/outlook_email_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/outlook_email_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/gmail_workspace_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/gmail_workspace_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/jira_delivery_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/jira_delivery_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/azure_devops_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/azure_devops_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/servicenow_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/servicenow_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/cloud_cost_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/cloud_cost_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/security_findings_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/security_findings_export.csv
python engine/cli.py detect-connector-profile --input engine/examples/erp_sap_export.csv
python engine/cli.py adapt-connector-export --input engine/examples/erp_sap_export.csv
```

## Marketplace-Safe Wording

Use:

- "Includes optional connector profiles and adapters for Teams, Slack, email, calendar, delivery, ITSM, cloud cost, security, ERP/SAP and document exports."
- "Live access requires separately enabled connectors and explicit user authorization."
- "Works with user-provided exports when live connectors are not available."
- "Connector readiness reports distinguish local export adapters from unavailable live connector contexts."

Avoid:

- "Automatically connects to Teams, Slack and email."
- "Reads your mailbox or messages."
- "Executes actions in collaboration tools."
