# Enterprise Memory Schema

Current SQLite memory schema version: `1.3`.

Version `1.3` adds `pending_memory_updates` so proposed memory changes can be queued, reviewed and explicitly approved or rejected before persistence into durable decision memory.

This file documents the intended phase-2 memory model. Version 0.1 does not persist data and does not claim live system access.

## Entity Types

- `person`
- `team`
- `role`
- `project`
- `application`
- `process`
- `risk`
- `control`
- `document`
- `kpi`
- `vendor`
- `data_object`
- `decision`
- `action`

## Relationship Types

- `owns`
- `depends_on`
- `approves`
- `operates`
- `funds`
- `implements`
- `controls`
- `mitigates`
- `documents`
- `consumes_data_from`
- `creates_risk_for`
- `blocks`
- `escalates_to`

## Common Fields

```json
{
  "id": "stable-id",
  "type": "project",
  "name": "ERP Modernization",
  "summary": "Short human-readable context",
  "owner": "Team or role",
  "status": "Green | Amber | Red | Unknown",
  "confidence": "High | Medium | Low",
  "source_refs": ["document-or-user-context-reference"],
  "tags": ["finance", "risk", "architecture"],
  "last_observed": "YYYY-MM-DD"
}
```

## Relationship Shape

```json
{
  "from": "entity-id",
  "to": "entity-id",
  "type": "depends_on",
  "summary": "Why the relationship matters",
  "criticality": "High | Medium | Low",
  "confidence": "High | Medium | Low",
  "evidence": "Source note or quote summary"
}
```

## Future MCP Tool Candidates

- `search_enterprise_context(query, filters)`
- `map_dependencies(entity_id, depth)`
- `score_risk(risk_context)`
- `build_briefing(scope, period, audience)`
- `compare_scenarios(options, constraints)`
- `assemble_report(report_type, audience, sources)`
