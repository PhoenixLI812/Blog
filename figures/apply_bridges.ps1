$scriptDir = $PSScriptRoot
if (-not $scriptDir) { $scriptDir = (Get-Location).Path }
$baseDir = (Get-Item $scriptDir).Parent.FullName

$jsonFile = Join-Path $baseDir "figures\bridges.json"
$items = Get-Content -LiteralPath $jsonFile -Raw -Encoding UTF8 | ConvertFrom-Json

$successCount = 0
$failCount = 0

foreach ($item in $items) {
    $fName = $item.file
    $search = $item.search
    $bridge = $item.bridge
    
    $filePath = Join-Path $baseDir ("manuscript\" + $fName)
    if (-not (Test-Path $filePath)) {
        Write-Host ("File not found: " + $fName)
        $failCount++
        continue
    }
    
    $raw = [System.IO.File]::ReadAllText($filePath, [System.Text.Encoding]::UTF8)
    
    # Normalize newlines to LF for matching
    $rawLF = $raw.Replace("`r`n", "`n")
    $searchLF = $search.Replace("`r`n", "`n")
    $bridgeLF = $bridge.Replace("`r`n", "`n")
    
    if ($rawLF.Contains($searchLF)) {
        $updatedLF = $rawLF.Replace($searchLF, $bridgeLF)
        $updatedCRLF = $updatedLF.Replace("`n", "`r`n")
        [System.IO.File]::WriteAllText($filePath, $updatedCRLF, [System.Text.Encoding]::UTF8)
        $successCount++
        Write-Host ("Applied bridge in " + $fName)
    } else {
        Write-Host ("Search block NOT found in " + $fName)
        $failCount++
    }
}

Write-Host ("Bridges applied. Success: {0}, Failed: {1}" -f $successCount, $failCount)
