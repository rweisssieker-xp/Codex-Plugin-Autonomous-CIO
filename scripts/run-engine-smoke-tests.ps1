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
python engine\cli.py orchestrate --input engine\examples\industrial_operating_review.json | Out-Null
python engine\cli.py propose-memory-updates --input engine\examples\industrial_operating_review.json | Out-Null
python engine\cli.py inspect-memory --memory engine\examples\memory.json | Out-Null
$exportDir = Join-Path $env:TEMP "acio-export-package-smoke"
if (Test-Path $exportDir) { Remove-Item -LiteralPath $exportDir -Recurse -Force }
python engine\cli.py export-package --input engine\examples\industrial_operating_review.json --output-dir $exportDir | Out-Null
$officeDir = Join-Path $env:TEMP "acio-office-export-smoke"
if (Test-Path $officeDir) { Remove-Item -LiteralPath $officeDir -Recurse -Force }
python engine\cli.py export-office-package --input engine\examples\industrial_operating_review.json --output-dir $officeDir | Out-Null
python engine\cli.py build-from-file --input engine\examples\sample_import.csv | Out-Null
python engine\cli.py dashboard-from-file --input engine\examples\sample_import.csv | Out-Null
python engine\cli.py ingest-directory --input engine\examples | Out-Null
python engine\cli.py refresh-dashboard --input engine\examples\board_prep.json --output visual-command-center\demo-data.json | Out-Null
python engine\cli.py evaluate | Out-Null
python -m unittest discover engine/tests
python -m unittest discover skills/user-context/tests
python C:\Users\weiss\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py "C:\tmp\Codex Plugin Autonomous CIO"

Write-Output "Engine smoke tests passed."
