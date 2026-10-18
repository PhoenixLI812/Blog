$baseDir = "c:\Users\Administrator\Desktop\半导体见顶了吗？"
$jsonFile = Join-Path $baseDir "figures\images_manifest.json"
$items = Get-Content -LiteralPath $jsonFile -Raw -Encoding UTF8 | ConvertFrom-Json

foreach ($item in $items) {
    $prefix = $item.prefix
    $svgFile = $item.svg
    $caption = $item.caption
    
    $searchPattern = Join-Path $baseDir "manuscript\$prefix*.md"
    $mdFiles = Get-ChildItem -Path $searchPattern
    if ($mdFiles.Count -eq 0) {
        Write-Output ("No MD file: " + $prefix)
        continue
    }
    $mdFile = $mdFiles[0]
    $svgPath = Join-Path $baseDir "figures\$svgFile"
    if (-not (Test-Path $svgPath)) {
        Write-Output ("No SVG: " + $svgFile)
        continue
    }
    
    $bytes = [System.IO.File]::ReadAllBytes($svgPath)
    $b64 = [System.Convert]::ToBase64String($bytes)
    $dataUri = "data:image/svg+xml;base64," + $b64
    
    $raw = [System.IO.File]::ReadAllText($mdFile.FullName, [System.Text.Encoding]::UTF8)
    if ($raw.Contains($dataUri)) {
        Write-Output ("Already injected: " + $prefix)
        continue
    }
    
    $tag = "![" + $caption + "](" + $dataUri + ")`n*" + $caption + "*`n`n"
    $firstCode = $raw.IndexOf("```")
    if ($firstCode -gt 0) {
        $updated = $raw.Substring(0, $firstCode) + $tag + $raw.Substring($firstCode)
        [System.IO.File]::WriteAllText($mdFile.FullName, $updated, [System.Text.Encoding]::UTF8)
        Write-Output ("Injected " + $svgFile + " into " + $prefix)
    } else {
        Write-Output ("No code fence: " + $prefix)
    }
}
