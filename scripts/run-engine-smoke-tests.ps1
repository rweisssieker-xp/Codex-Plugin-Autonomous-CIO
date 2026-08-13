$ErrorActionPreference = "Stop"

python engine\cli.py build-decision-packet --input engine\examples\board_prep.json | Out-Null
python engine\cli.py score --input engine\examples\board_prep.json | Out-Null
python engine\cli.py map-risk-chain --input engine\examples\crisis.json | Out-Null
python engine\cli.py extract-evidence-graph --input engine\examples\ai_governance.json | Out-Null
python engine\cli.py semantic-model --input engine\examples\board_prep.json | Out-Null
python engine\cli.py simulate-scenarios --input engine\examples\board_prep.json | Out-Null
python engine\cli.py audit-trail --input engine\examples\board_prep.json | Out-Null
python engine\cli.py dashboard-data --input engine\examples\board_prep.json | Out-Null
python engine\cli.py operating-rhythm --input engine\examples\board_prep.json | Out-Null
python engine\cli.py benchmark --input engine\examples\board_prep.json | Out-Null
python engine\cli.py ingest-signals --input engine\examples\connector_signals.json | Out-Null
python engine\cli.py risk-graph --input engine\examples\board_prep.json | Out-Null
python engine\cli.py trend-delta --input engine\examples\board_prep_with_prior.json | Out-Null
python engine\cli.py export-review --input engine\examples\board_prep.json --format markdown | Out-Null
python engine\cli.py privacy-scan --input engine\examples\ai_governance.json | Out-Null
python engine\cli.py action-governance --input engine\examples\board_prep.json | Out-Null
python engine\cli.py assurance --input engine\examples\board_prep.json | Out-Null
python engine\cli.py assurance --input engine\examples\board_prep_llm_extracted.json | Out-Null
python engine\cli.py decision-defense --input engine\examples\board_prep.json | Out-Null
python engine\cli.py autopilot-review --input engine\examples\industrial_operating_review.json | Out-Null
python engine\cli.py connector-profiles | Out-Null
python engine\cli.py detect-connector-profile --input engine\examples\industrial_file_drop.csv | Out-Null
python engine\cli.py adapt-connector-export --input engine\examples\topdesk_export.csv | Out-Null
python engine\cli.py llm-extraction-contract --input engine\examples\industrial_operating_review.json | Out-Null
python engine\cli.py llm-extraction-pipeline --input engine\examples\industrial_operating_review.json | Out-Null
python engine\cli.py orchestrate --input engine\examples\industrial_operating_review.json | Out-Null
python engine\cli.py propose-memory-updates --input engine\examples\industrial_operating_review.json | Out-Null
python engine\cli.py inspect-memory --memory engine\examples\memory.json | Out-Null
$exportDir = Join-Path $env:TEMP "acio-export-package-smoke"
if (Test-Path $exportDir) { Remove-Item -LiteralPath $exportDir -Recurse -Force }
python engine\cli.py export-package --input engine\examples\industrial_operating_review.json --output-dir $exportDir | Out-Null
$officeDir = Join-Path $env:TEMP "acio-office-export-smoke"
if (Test-Path $officeDir) { Remove-Item -LiteralPath $officeDir -Recurse -Force }
python engine\cli.py export-office-package --input engine\examples\industrial_operating_review.json --output-dir $officeDir | Out-Null
python engine\cli.py decision-twin --input engine\examples\industrial_operating_review.json --scenario defer | Out-Null
python engine\cli.py score-evidence --input engine\examples\industrial_operating_review.json | Out-Null
python engine\cli.py evaluate-policy --input engine\examples\ai_governance.json --policy ai-governance | Out-Null
python engine\cli.py approval-gates --input engine\examples\industrial_operating_review.json | Out-Null
python engine\cli.py governance-readiness --input engine\examples\industrial_operating_review.json | Out-Null
python engine\cli.py draft-actions --input engine\examples\board_prep.json --type email | Out-Null
$dbPath = Join-Path $env:TEMP "acio-memory-smoke.db"
if (Test-Path $dbPath) { Remove-Item -LiteralPath $dbPath -Force }
python engine\cli.py init-memory-db --db $dbPath | Out-Null
python scripts\seed-demo-memory.py --db $dbPath | Out-Null
python engine\cli.py queue-memory-updates --input engine\examples\board_prep.json --db $dbPath | Out-Null
python engine\cli.py list-memory-update-queue --db $dbPath | Out-Null
python engine\cli.py review-memory-update --db $dbPath --id 1 --decision Approved --reviewer "Smoke test" | Out-Null
python engine\cli.py migrate-memory-json --memory engine\examples\memory.json --db $dbPath | Out-Null
python engine\cli.py save-review --input engine\examples\board_prep.json --db $dbPath | Out-Null
python engine\cli.py query-memory --db $dbPath --query ERP | Out-Null
python engine\cli.py memory-aging --db $dbPath | Out-Null
python engine\cli.py sla-monitor --db $dbPath | Out-Null
python engine\cli.py sla-digest --db $dbPath | Out-Null
python engine\cli.py record-feedback --input engine\examples\learning_feedback.json --db $dbPath | Out-Null
python engine\cli.py record-outcome --input engine\examples\learning_outcome.json --db $dbPath | Out-Null
python engine\cli.py skill-chain-feedback --input engine\examples\skill_chain_feedback.json --db $dbPath | Out-Null
python engine\cli.py board-question-memory --input engine\examples\board_questions.json --db $dbPath | Out-Null
python engine\cli.py calibrate-scores --db $dbPath | Out-Null
python engine\cli.py learn-patterns --db $dbPath | Out-Null
python engine\cli.py source-reputation --db $dbPath | Out-Null
python engine\cli.py recommendation-backtest --db $dbPath | Out-Null
python engine\cli.py learning-digest --db $dbPath | Out-Null
python engine\cli.py decision-dna --db $dbPath | Out-Null
python engine\cli.py risk-appetite-twin --db $dbPath | Out-Null
python engine\cli.py board-memory --db $dbPath | Out-Null
python engine\cli.py accountability-graph --input engine\examples\board_prep.json --db $dbPath | Out-Null
python engine\cli.py friction-score --input engine\examples\board_prep.json --db $dbPath | Out-Null
python engine\cli.py decision-collisions --input engine\examples\industrial_operating_review.json --db $dbPath | Out-Null
python engine\cli.py strategic-contradictions --input engine\examples\industrial_operating_review.json --db $dbPath | Out-Null
python engine\cli.py shadow-cost-inaction --input engine\examples\board_prep.json | Out-Null
python engine\cli.py enterprise-decision-ledger --db $dbPath | Out-Null
python engine\cli.py control-decision-trace --input engine\examples\ai_governance.json --db $dbPath | Out-Null
python engine\cli.py vendor-truth-index --input engine\examples\industrial_operating_review.json --db $dbPath | Out-Null
python engine\cli.py narrative-integrity --input engine\examples\board_prep.json | Out-Null
python engine\cli.py simulation-arena --input engine\examples\board_prep.json | Out-Null
python engine\cli.py weekly-operating-autopilot --db $dbPath | Out-Null
$weeklyBriefDir = Join-Path $env:TEMP "acio-weekly-brief-smoke"
if (Test-Path $weeklyBriefDir) { Remove-Item -LiteralPath $weeklyBriefDir -Recurse -Force }
python engine\cli.py executive-weekly-brief --db $dbPath --output-dir $weeklyBriefDir --format both | Out-Null
python engine\cli.py delegation-planner --input engine\examples\board_prep.json | Out-Null
python engine\cli.py enterprise-operating-twin --input engine\examples\industrial_operating_review.json --db $dbPath | Out-Null
python engine\cli.py autonomy-contract --input engine\examples\industrial_operating_review.json --db $dbPath | Out-Null
python engine\cli.py decision-chain-custody --input engine\examples\industrial_operating_review.json --db $dbPath | Out-Null
python engine\cli.py executive-attention --input engine\examples\industrial_operating_review.json --db $dbPath | Out-Null
python engine\cli.py kill-criteria-sentinel --input engine\examples\board_prep.json --db $dbPath | Out-Null
python engine\cli.py benefit-realization-memory --db $dbPath | Out-Null
python engine\cli.py strategic-drift-warning --input engine\examples\industrial_operating_review.json --db $dbPath | Out-Null
python engine\cli.py vendor-promise-backtest --input engine\examples\industrial_operating_review.json --db $dbPath | Out-Null
python engine\cli.py decision-latency-cost --input engine\examples\industrial_operating_review.json --db $dbPath | Out-Null
python engine\cli.py evidence-decay-forecast --input engine\examples\industrial_operating_review.json --db $dbPath | Out-Null
python engine\cli.py synthetic-executive-committee --input engine\examples\industrial_operating_review.json --db $dbPath | Out-Null
python engine\cli.py control-debt-ledger --input engine\examples\industrial_operating_review.json --db $dbPath | Out-Null
python engine\cli.py operating-rhythm-autopilot-v2 --db $dbPath | Out-Null
python engine\cli.py enterprise-contradiction-memory --input engine\examples\board_prep.json --db $dbPath | Out-Null
python engine\cli.py cio-replacement-surface-map --input engine\examples\industrial_operating_review.json --db $dbPath | Out-Null
python engine\cli.py discover-sources --path engine\examples | Out-Null
python engine\cli.py pull-signals --input engine\examples\topdesk_export.csv | Out-Null
python engine\cli.py ingest-bundle --input engine\examples --db $dbPath | Out-Null
$profilePath = Join-Path $env:TEMP "acio-profile-smoke.json"
if (Test-Path $profilePath) { Remove-Item -LiteralPath $profilePath -Force }
python engine\cli.py init-profile --profile $profilePath | Out-Null
python engine\cli.py apply-profile --input engine\examples\board_prep.json --profile $profilePath | Out-Null
$boardPackDir = Join-Path $env:TEMP "acio-board-pack-smoke"
if (Test-Path $boardPackDir) { Remove-Item -LiteralPath $boardPackDir -Recurse -Force }
python engine\cli.py build-board-pack --input engine\examples\board_prep.json --output-dir $boardPackDir --format both | Out-Null
python engine\cli.py run-evals --eval-dir engine\evals | Out-Null
python engine\cli.py eval-report --eval-dir engine\evals | Out-Null
python engine\cli.py hardening-evals --eval-dir engine\evals | Out-Null
python engine\cli.py skill-suites | Out-Null
$schemaOutput = Join-Path $env:TEMP "acio-schema-output.json"
$schemaJson = python engine\cli.py llm-extraction-pipeline --input engine\examples\board_prep.json
[System.IO.File]::WriteAllText($schemaOutput, ($schemaJson -join [Environment]::NewLine), [System.Text.UTF8Encoding]::new($false))
python engine\cli.py validate-schema --input $schemaOutput --schema llm-extraction-pipeline.schema.json | Out-Null
$releaseDir = Join-Path $env:TEMP "acio-release-package-smoke"
if (Test-Path $releaseDir) { Remove-Item -LiteralPath $releaseDir -Recurse -Force }
python engine\cli.py build-release-package --output-dir $releaseDir | Out-Null
python engine\cli.py build-from-file --input engine\examples\sample_import.csv | Out-Null
python engine\cli.py dashboard-from-file --input engine\examples\sample_import.csv | Out-Null
python engine\cli.py ingest-directory --input engine\examples | Out-Null
python engine\cli.py refresh-dashboard --input engine\examples\board_prep.json --output visual-command-center\demo-data.json | Out-Null
python engine\cli.py evaluate | Out-Null
$webPort = 18765
$webProc = Start-Process -FilePath "python" -ArgumentList "app\server.py --port $webPort" -WorkingDirectory (Get-Location) -PassThru -WindowStyle Hidden
try {
  Start-Sleep -Seconds 2
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/evals" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/hardening-evals" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/skill-suites" -UseBasicParsing | Out-Null
  $seedPayload = @{ db = $dbPath } | ConvertTo-Json -Compress
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/seed-demo-memory" -Method Post -Body $seedPayload -ContentType "application/json" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/decision-dna?db=$dbPath" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/weekly-operating-autopilot?db=$dbPath" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/executive-weekly-brief?db=$dbPath" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/enterprise-ledger?db=$dbPath" -UseBasicParsing | Out-Null
  $webPayload = '{"context":{"decision_request":"Prepare a board decision on ERP go-live","context":["Testing has not started because the environment is late.","Audit evidence for change control is incomplete.","Budget reserve is nearly consumed."]}}'
  $webPayloadWithDb = '{"db":"' + ($dbPath -replace '\\','\\') + '","context":{"decision_request":"Prepare a board decision on ERP go-live","context":["Testing has not started because the environment is late.","Audit evidence for change control is incomplete.","Budget reserve is nearly consumed.","Vendor milestone slipped and recovery evidence is missing."]}}'
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/simulation-arena" -Method Post -Body $webPayload -ContentType "application/json" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/llm-extraction-pipeline" -Method Post -Body $webPayload -ContentType "application/json" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/queue-memory-updates" -Method Post -Body $webPayloadWithDb -ContentType "application/json" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/memory-update-queue?db=$dbPath" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/delegation-planner" -Method Post -Body $webPayload -ContentType "application/json" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/narrative-integrity" -Method Post -Body $webPayload -ContentType "application/json" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/enterprise-operating-twin" -Method Post -Body $webPayloadWithDb -ContentType "application/json" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/autonomy-contract" -Method Post -Body $webPayloadWithDb -ContentType "application/json" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/decision-chain-custody" -Method Post -Body $webPayloadWithDb -ContentType "application/json" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/executive-attention" -Method Post -Body $webPayloadWithDb -ContentType "application/json" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/kill-criteria-sentinel" -Method Post -Body $webPayloadWithDb -ContentType "application/json" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/benefit-realization-memory?db=$dbPath" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/strategic-drift-warning" -Method Post -Body $webPayloadWithDb -ContentType "application/json" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/vendor-promise-backtest" -Method Post -Body $webPayloadWithDb -ContentType "application/json" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/decision-latency-cost" -Method Post -Body $webPayloadWithDb -ContentType "application/json" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/evidence-decay-forecast" -Method Post -Body $webPayloadWithDb -ContentType "application/json" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/synthetic-executive-committee" -Method Post -Body $webPayloadWithDb -ContentType "application/json" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/control-debt-ledger" -Method Post -Body $webPayloadWithDb -ContentType "application/json" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/operating-rhythm-autopilot-v2?db=$dbPath" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/enterprise-contradiction-memory" -Method Post -Body $webPayloadWithDb -ContentType "application/json" -UseBasicParsing | Out-Null
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/cio-replacement-surface-map" -Method Post -Body $webPayloadWithDb -ContentType "application/json" -UseBasicParsing | Out-Null
  $weeklyExportPayload = @{ db = $dbPath; output_dir = "$weeklyBriefDir-web"; format = "both" } | ConvertTo-Json -Compress
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/export-weekly-brief" -Method Post -Body $weeklyExportPayload -ContentType "application/json" -UseBasicParsing | Out-Null
  $releasePayload = @{ output_dir = "$releaseDir-web" } | ConvertTo-Json -Compress
  Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/api/build-release-package" -Method Post -Body $releasePayload -ContentType "application/json" -UseBasicParsing | Out-Null
} finally {
  if ($webProc -and -not $webProc.HasExited) { Stop-Process -Id $webProc.Id -Force }
}
python -m unittest discover engine/tests
python -m unittest discover skills/user-context/tests
python C:\Users\weiss\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py "C:\tmp\Codex Plugin Autonomous CIO"

Write-Output "Engine smoke tests passed."
