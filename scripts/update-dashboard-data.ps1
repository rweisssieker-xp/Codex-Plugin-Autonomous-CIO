param(
    [string] $InputPath = "engine\examples\board_prep.json",
    [string] $OutputPath = "visual-command-center\demo-data.json"
)

$ErrorActionPreference = "Stop"

python engine\cli.py refresh-dashboard --input $InputPath --output $OutputPath

Write-Output "Dashboard data refreshed: $OutputPath"
