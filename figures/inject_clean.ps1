$scriptDir = $PSScriptRoot
if (-not $scriptDir) { $scriptDir = (Get-Location).Path }
$baseDir = (Get-Item $scriptDir).Parent.FullName
if (-not (Test-Path (Join-Path $baseDir "manuscript"))) {
    $baseDir = (Get-Location).Path
}

$nl = [Environment]::NewLine
$jsonFile = Join-Path $baseDir "figures\images_manifest.json"
$items = Get-Content -LiteralPath $jsonFile -Raw -Encoding UTF8 | ConvertFrom-Json

foreach ($item in $items) {
    $prefix = $item.prefix
    $svgFile = $item.svg
    $caption = $item.caption
    
    $mdFiles = Get-ChildItem -Path (Join-Path $baseDir ("manuscript\" + $prefix + "*.md"))
    if ($mdFiles.Count -eq 0) {
        Write-Host "No MD file for $prefix"
        continue
    }
    $mdFile = $mdFiles[0]
    $svgPath = Join-Path $baseDir ("figures\" + $svgFile)
    if (-not (Test-Path $svgPath)) {
        Write-Host "No SVG file: $svgFile"
        continue
    }
    
    $bytes = [System.IO.File]::ReadAllBytes($svgPath)
    $b64 = [System.Convert]::ToBase64String($bytes)
    $dataUri = "data:image/svg+xml;base64," + $b64
    
    $raw = [System.IO.File]::ReadAllText($mdFile.FullName, [System.Text.Encoding]::UTF8)
    if ($raw.Contains($dataUri)) {
        Write-Host "Already injected: $prefix"
        continue
    }
    
    $tag = "![" + $caption + "](" + $dataUri + ")" + $nl + "*" + $caption + "*" + $nl + $nl
    $fence = [string]::new([char]96, 3)
    $firstCode = $raw.IndexOf($fence)
    if ($firstCode -gt 0) {
        $p1 = $raw.Substring(0, $firstCode)
        $p2 = $raw.Substring($firstCode)
        $updated = $p1 + $tag + $p2
        [System.IO.File]::WriteAllText($mdFile.FullName, $updated, [System.Text.Encoding]::UTF8)
        Write-Host "Injected $svgFile into $prefix"
    } else {
        Write-Host "No code fence: $prefix"
    }
}
