$scriptDir = $PSScriptRoot
if (-not $scriptDir) { $scriptDir = (Get-Location).Path }
$baseDir = (Get-Item $scriptDir).Parent.FullName

$termsFile = Join-Path $baseDir "figures\terms.json"
$terms = Get-Content -LiteralPath $termsFile -Raw -Encoding UTF8 | ConvertFrom-Json

$files = Get-ChildItem -LiteralPath (Join-Path $baseDir "manuscript") -Filter "*.md" | Sort-Object Name

$report = @()

foreach ($f in $files) {
    $raw = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    $lines = [System.IO.File]::ReadAllLines($f.FullName, [System.Text.Encoding]::UTF8)
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        foreach ($t in $terms) {
            if ($line.Contains($t)) {
                $report += [PSCustomObject]@{
                    File = $f.Name
                    Line = $i + 1
                    Term = $t
                    Snippet = $line.Trim()
                }
            }
        }
    }
}

$json = $report | ConvertTo-Json -Depth 3
[System.IO.File]::WriteAllText((Join-Path $baseDir "figures\extreme_report.json"), $json, [System.Text.Encoding]::UTF8)
Write-Host ("Report generated. Total hits: " + $report.Count)
