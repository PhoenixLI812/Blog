$scriptDir = $PSScriptRoot
if (-not $scriptDir) { $scriptDir = (Get-Location).Path }
$baseDir = (Get-Item $scriptDir).Parent.FullName

$files = Get-ChildItem -LiteralPath (Join-Path $baseDir "manuscript") -Filter "*.md" | Sort-Object Name

$results = @()
foreach ($f in $files) {
    $lines = [System.IO.File]::ReadAllLines($f.FullName, [System.Text.Encoding]::UTF8)
    $total = $lines.Count
    
    # Get first 10 non-empty lines
    $first10 = ($lines | Where-Object { $_.Trim() -ne "" } | Select-Object -First 5) -join " `n "
    
    # Get last 5 non-empty lines
    $last5 = ($lines | Where-Object { $_.Trim() -ne "" } | Select-Object -Last 5) -join " `n "
    
    $results += [PSCustomObject]@{
        File = $f.Name
        TotalLines = $total
        Start = $first10
        End = $last5
    }
}

$json = $results | ConvertTo-Json -Depth 3
[System.IO.File]::WriteAllText((Join-Path $baseDir "figures\chapters_head_tail.json"), $json, [System.Text.Encoding]::UTF8)
Write-Host "Exported head and tail of all chapters."
