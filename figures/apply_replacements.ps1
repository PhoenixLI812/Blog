$scriptDir = $PSScriptRoot
if (-not $scriptDir) { $scriptDir = (Get-Location).Path }
$baseDir = (Get-Item $scriptDir).Parent.FullName

$jsonFile = Join-Path $baseDir "figures\objective_replacements.json"
$items = Get-Content -LiteralPath $jsonFile -Raw -Encoding UTF8 | ConvertFrom-Json

$successCount = 0
$failCount = 0

foreach ($item in $items) {
    $fName = $item.file
    $search = $item.search
    $replace = $item.replace
    
    $filePath = Join-Path $baseDir ("manuscript\" + $fName)
    if (-not (Test-Path $filePath)) {
        Write-Host ("File not found: " + $fName)
        $failCount++
        continue
    }
    
    $raw = [System.IO.File]::ReadAllText($filePath, [System.Text.Encoding]::UTF8)
    if ($raw.Contains($search)) {
        $updated = $raw.Replace($search, $replace)
        [System.IO.File]::WriteAllText($filePath, $updated, [System.Text.Encoding]::UTF8)
        $successCount++
        Write-Host ("Replaced in " + $fName)
    } else {
        Write-Host ("Search text NOT found in " + $fName + ": " + $search.Substring(0, [Math]::Min(30, $search.Length)))
        $failCount++
    }
}

Write-Host ("Done. Success: {0}, Failed: {1}" -f $successCount, $failCount)
