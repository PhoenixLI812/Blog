$scriptDir = $PSScriptRoot
if (-not $scriptDir) { $scriptDir = (Get-Location).Path }
$baseDir = (Get-Item $scriptDir).Parent.FullName

$files = Get-ChildItem -LiteralPath (Join-Path $baseDir "manuscript") | ForEach-Object {
    [PSCustomObject]@{
        Name = $_.Name
        Length = $_.Length
    }
}

$json = $files | ConvertTo-Json -Depth 2
[System.IO.File]::WriteAllText((Join-Path $baseDir "figures\manuscript_files.json"), $json, [System.Text.Encoding]::UTF8)
Write-Host "Wrote file list to manuscript_files.json"
